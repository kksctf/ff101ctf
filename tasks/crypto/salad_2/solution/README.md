# Салат II
Author: `@greg0r0`

## Desc
Слышали ли вы про синдром борща? Ну это если собрать N поваров и попросить приготовить борщ, то у всех окажутся разные рецепты...

С салатом Цезарь работает так же, правда вариаций рецепта, наверное, поменьше.

[data.enc](../public/data.enc)

## Flag

```
ptctf{d0_y0u_pr3f3r_ch1ck3n_0r_shr1mps}
```

## Solve

Шифр Цезаря, но алфавитом является не классический английский алфавит, а таблица ASCII. Вообще выглядит как уцуцуга, но Desc должен давать очень жирный хинт что это вариация цезаря.

```
#!/usr/bin/env python

f = open('./data.enc', "rb")
flag = f.read().decode("latin-1")
f.close()

for k in range(256):
    flag_c = ""
    for ch in flag:
        n = (ord(ch) + k) % 256
        flag_c += chr(n)
    if flag_c.startswith('ptctf'):
        print(flag_c)
        break

```