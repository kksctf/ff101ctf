# ROX
Author: `@chiukki`

## Desc
Помогите Алисе-путешественнице расшифровать эту сотню двойных сообщений от Боба

`nc {server_addr}:2802`

## Flag

```
ptctf{byt3s_0p3r4t10ns_4r3_s0_cr4zy}
```

## Solve

[solver.py](./solver.py)

Возможно, самое сложное, это додуматься до преобразования "чистого" питоновского языка через `ast.literal_eval`

И, само собой, при работе с подобными тасками, дабы избежать неуспевания получения данных от сервера, важно знать про `recvuntil()`
