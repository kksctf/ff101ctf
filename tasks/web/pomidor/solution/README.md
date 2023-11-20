# pomidor

## category
`Web`

## desc
```
                       ,
                      /.\
                    //_`\
                _.-`| \ ``._
            .-''`-.       _.'`.
          .'      / /'\/`.\    `. 
        /   .    |/         `.  \
        '   /                  \  ;
      :   '            \       : :
      ;  ;             ;      /  .
        ' :             .     '  /
        \ \           /       .'
          `.`        .'      .'
            `-..___....----`
```

## flag

`ptctf{pomidori_pomidori_10m4103$}`

## Solve

Изучив исходники сервиса (или потыкавшись в него браузером) обратим внимание, что
ручка получения помидора по прямой ссылке не проверяет авторизацию пользователя.
Генерация прямой ссылки обратима.
```go
func generatePomidorToken(p *Pomidor) string {
	token := md5.Sum([]byte(fmt.Sprintf("%s:%s:%d:%d", os.Getenv("POMIDOR_SALT"), p.Username, p.ID, p.IsPrivate)))
	return hex.EncodeToString(token[:])
}
```
В этом сниппете видно, что прямая ссылка состоит из строки, все данные в которой известны,
кроме соли. При этом, на соль наложены серьезные ограничения - она обязана быть длины 3.
```go
if len(os.Getenv("POMIDOR_SALT")) != 3 {
    panic(errors.New("Bad POMIDOR_SALT (must be 3 chars)"))
}
```
Также, можно найти "целевой" помидор:
```go
pomidorsDB = append(pomidorsDB, &Pomidor{Username: "admin", ID: 1337, IsPrivate: true, Data: os.Getenv("FLAG")})
```
Значит, нужно составить прямую ссылку для юзера `admin`, ID `1337`, флага приватности `true` и неизвестной нам соли.

Важно заметить, что в форматной строке `"%s:%s:%d:%d"` есть проблема - в golang при
подстановке bool в спецификатор `%d` получается не 0 или 1 (и не true\false), а строка вида
`%!d(bool=true)` или `%!d(bool=false)`. Проверить, какая именно строка попадает внутрь md5 можно с помощью небольшой программки:
```go
package main

import "fmt"

func main () {
    fmt.Printf("%s:%s:%d:%d", "salt", "admin", 2, false)
}
```

```bash
$ go run /tmp/brek.go
salt:admin:2:%!d(bool=false)
```

При регистрации на сервисе нам выдается 5 случайных помидоров и прямые ссылки на них. С помощью такой ссылки сбрутим соль `"pom"`. Сгенерируем ссылку для строки `pom:admin:1337:%!d(bool=true)` (`30eccb26d26fb66d723a259f77370a21`) и получим флаг внутри тега `<img>`.

Солвер: [solve.py](solve.py)