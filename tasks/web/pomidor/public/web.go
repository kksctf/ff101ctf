package main

import (
	"crypto/md5"
	"encoding/base64"
	"encoding/hex"
	"errors"
	"flag"
	"fmt"
	"html/template"
	"math/rand"
	"net/http"
	"os"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/jwtauth"
	"github.com/lestrrat-go/jwx/jwt"
)

var tokenAuth *jwtauth.JWTAuth

var jwtSecret = os.Getenv("JWT_SECRET")

func init() {
	tokenAuth = jwtauth.New("HS256", []byte(jwtSecret), nil)
}

func makeToken(username string) string {
	_, tokenString, _ := tokenAuth.Encode(map[string]interface{}{"username": username})
	return tokenString
}

func loggedInRedirector(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token, _, _ := jwtauth.FromContext(r.Context())

		if token != nil && jwt.Validate(token) == nil {
			http.Redirect(w, r, "/profile", 302)
		}

		next.ServeHTTP(w, r)
	})
}

func unloggedInRedirector(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token, _, _ := jwtauth.FromContext(r.Context())

		if token == nil || jwt.Validate(token) != nil {
			http.Redirect(w, r, "/login", 302)
		}

		next.ServeHTTP(w, r)
	})
}

// User ...
type User struct {
	Username string
	Password string
}

// PageData ...
type PageData struct {
	User *User
}

// PomidorData ...
type PomidorData struct {
	User     *User
	Pomidors []*Pomidor
}

// Pomidor ...
type Pomidor struct {
	Username  string
	ID        int
	IsPrivate bool
	Data      string
	Token     string
}

var usersDB = []*User{
	{Username: "admin", Password: os.Getenv("ADMIN_PASSWORD")},
}
var pomidorsDB = []*Pomidor{}

func enrichPomidorDb(username string, amount int) {
	entries, err := os.ReadDir("./pomidors")
	if err != nil {
		panic(err)
	}
	rand.Shuffle(len(entries), func(i, j int) { entries[i], entries[j] = entries[j], entries[i] })
	for id, entry := range entries {
		if id >= amount {
			break
		}
		if entry.Type().IsRegular() {
			jpeg, err := os.ReadFile(fmt.Sprintf("./pomidors/%s", entry.Name()))
			if err != nil {
				panic(err)
			}
			isPrivate := false
			if username == "admin" {
				isPrivate = rand.Int()&4 == 0
			}

			newPomidor := Pomidor{Username: username, ID: id, IsPrivate: isPrivate, Data: base64.StdEncoding.EncodeToString(jpeg)}
			newPomidor.Token = generatePomidorToken(&newPomidor)
			pomidorsDB = append(pomidorsDB, &newPomidor)
		}
	}
}

func getUser(username string) (*User, error) {
	for _, u := range usersDB {
		if u.Username == username {
			return u, nil
		}
	}
	return nil, errors.New("user not found")
}

func getPomidor(username string, id int) (*Pomidor, error) {
	for _, p := range pomidorsDB {
		if p.Username == username && p.ID == id {
			return p, nil
		}
	}
	return nil, errors.New("pomidor not found")
}

func generatePomidorToken(p *Pomidor) string {
	token := md5.Sum([]byte(fmt.Sprintf("%s:%s:%d:%d", os.Getenv("POMIDOR_SALT"), p.Username, p.ID, p.IsPrivate)))
	return hex.EncodeToString(token[:])
}

func parseTemplates(r *http.Request, templates []string) (*template.Template, *PageData) {
	_, claims, _ := jwtauth.FromContext(r.Context())

	templates = append(templates, []string{"templates/partials/navbar.html", "templates/partials/bootstrap.html"}...)
	tmpl := template.Must(template.ParseFiles(templates...))

	data := &PageData{
		User: nil,
	}

	if claims["username"] != nil {
		data.User = &User{
			Username: claims["username"].(string),
		}
	}

	return tmpl, data
}

func main() {
	flag.Parse()

	if len(os.Getenv("POMIDOR_SALT")) != 3 {
		panic(errors.New("Bad POMIDOR_SALT (must be 3 chars)"))
	}

	enrichPomidorDb("admin", 50)
	pomidorsDB = append(pomidorsDB, &Pomidor{Username: "admin", ID: 1337, IsPrivate: true, Data: os.Getenv("FLAG")})
	p, _ := getPomidor("admin", 1337)
	p.Token = generatePomidorToken(p)

	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)

	fs := http.FileServer(http.Dir("static"))
	r.Handle("/static/*", http.StripPrefix("/static/", fs))

	r.Group(func(r chi.Router) {
		r.Use(middleware.Throttle(1))
		r.Post("/register", func(w http.ResponseWriter, r *http.Request) {
			r.ParseForm()
			username := r.PostForm.Get("username")
			password := r.PostForm.Get("password")

			if username == "" || password == "" {
				http.Error(w, "Missing username or password.", http.StatusBadRequest)
				return
			}

			if user, err := getUser(username); err == nil {
				http.Error(w, fmt.Sprintf("Username %s already taken.", user.Username), http.StatusForbidden)
				return
			}

			usersDB = append(usersDB, &User{username, password})
			enrichPomidorDb(username, 5)

			http.Redirect(w, r, "/login", http.StatusSeeOther)
		})

		r.Post("/login", func(w http.ResponseWriter, r *http.Request) {
			r.ParseForm()
			username := r.PostForm.Get("username")
			password := r.PostForm.Get("password")

			if username == "" || password == "" {
				http.Error(w, "Missing username or password.", http.StatusBadRequest)
				return
			}

			user, err := getUser(username)
			if err != nil {
				http.Error(w, err.Error(), http.StatusNotFound)
				return
			}

			if user.Password != password {
				http.Error(w, "Invalid password.", http.StatusForbidden)
				return
			}

			token := makeToken(username)

			http.SetCookie(w, &http.Cookie{
				HttpOnly: true,
				Expires:  time.Now().Add(1 * time.Hour),
				SameSite: http.SameSiteLaxMode,
				Name:     "jwt",
				Value:    token,
			})

			http.Redirect(w, r, "/profile", http.StatusSeeOther)
		})
		r.Post("/logout", func(w http.ResponseWriter, r *http.Request) {
			http.SetCookie(w, &http.Cookie{
				HttpOnly: true,
				MaxAge:   -1,
				SameSite: http.SameSiteLaxMode,
				Name:     "jwt",
				Value:    "",
			})

			http.Redirect(w, r, "/", http.StatusSeeOther)
		})
	})

	r.Group(func(r chi.Router) {
		r.Use(jwtauth.Verifier(tokenAuth))

		r.Get("/", func(w http.ResponseWriter, r *http.Request) {
			tmpl, data := parseTemplates(r, []string{"templates/pages/index.html"})

			tmpl.ExecuteTemplate(w, "home", data)
		})
	})

	r.Group(func(r chi.Router) {
		r.Use(jwtauth.Verifier(tokenAuth))

		r.Use(loggedInRedirector)

		r.Get("/register", func(w http.ResponseWriter, r *http.Request) {
			tmpl, data := parseTemplates(r, []string{"templates/pages/register.html"})

			tmpl.ExecuteTemplate(w, "register", data)
		})

		r.Get("/login", func(w http.ResponseWriter, r *http.Request) {
			tmpl, data := parseTemplates(r, []string{"templates/pages/login.html"})

			tmpl.ExecuteTemplate(w, "login", data)
		})
	})

	r.Group(func(r chi.Router) {
		r.Use(jwtauth.Verifier(tokenAuth))

		r.Use(unloggedInRedirector)

		r.Get("/profile", func(w http.ResponseWriter, r *http.Request) {
			tmpl, data := parseTemplates(r, []string{"templates/pages/profile.html"})

			tmpl.ExecuteTemplate(w, "profile", data)
		})

		r.Route("/pomidors", func(r chi.Router) {
			r.Get("/my", func(w http.ResponseWriter, r *http.Request) {
				tmpl, data := parseTemplates(r, []string{"templates/pages/pomidors.html"})

				var pomidors PomidorData
				pomidors.User = data.User
				for _, p := range pomidorsDB {
					if p.Username == data.User.Username {
						pomidors.Pomidors = append(pomidors.Pomidors, p)
					}
				}

				tmpl.ExecuteTemplate(w, "pomidors", &pomidors)
			})

			r.Get("/all", func(w http.ResponseWriter, r *http.Request) {
				tmpl, data := parseTemplates(r, []string{"templates/pages/pomidors.html"})

				var pomidors PomidorData
				pomidors.User = data.User
				for _, p := range pomidorsDB[:] {
					if !p.IsPrivate || p.Username == data.User.Username {
						pomidors.Pomidors = append(pomidors.Pomidors, p)
					}
				}

				tmpl.ExecuteTemplate(w, "pomidors", &pomidors)
			})

			r.Get("/random", func(w http.ResponseWriter, r *http.Request) {
				tmpl, data := parseTemplates(r, []string{"templates/pages/random.html"})

				var pomidors PomidorData
				pomidors.User = data.User

				wantToGenerate := 25

				for i := 0; i < wantToGenerate; {
					idx := rand.Int() % len(pomidorsDB)
					chosen := pomidorsDB[idx]
					if !chosen.IsPrivate {
						pomidors.Pomidors = append(pomidors.Pomidors, chosen)
						i++
					}
				}

				tmpl.ExecuteTemplate(w, "pomidors", &pomidors)
			})

			r.Route("/{token}", func(r chi.Router) {
				r.Get("/", func(w http.ResponseWriter, r *http.Request) {
					tmpl, data := parseTemplates(r, []string{"templates/pages/pomidors.html"})

					var pomidors PomidorData
					pomidors.User = data.User
					if pomidorToken := chi.URLParam(r, "token"); pomidorToken != "" {
						for _, p := range pomidorsDB {
							if p.Token == pomidorToken {
								pomidors.Pomidors = append(pomidors.Pomidors, p)
							}
						}
					}

					if len(pomidors.Pomidors) == 0 {
						http.Error(w, "Invalid link.", http.StatusNotFound)
						return
					}

					tmpl.ExecuteTemplate(w, "pomidors", &pomidors)
				})
			})
		})
	})

	http.ListenAndServe(":3333", r)
}
