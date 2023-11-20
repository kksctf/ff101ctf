FROM golang:1.21-alpine

WORKDIR /app

COPY go.mod go.sum ./
COPY static ./static
COPY templates ./templates
COPY pomidors ./pomidors

RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /app/web

CMD ["/app/web"]