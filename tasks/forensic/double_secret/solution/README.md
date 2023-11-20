# Двойное дно
Author: `@greg0r0`

## Desc

Этот котик явно слишком много знает. Сможешь узнать секрет кота Бориса?

[mem.task.png](./public/mem.task.png)

## Flag

```
ptctf{s3cr3t_0f_B0r1s_1s_g00d_n1ght_sl33p}
```

## Solve

На самой картинке ничего нет. В целом, необходимо сделать три шага:
1) Посмотреть в метаданные и увидеть строку `Very_secret_key = GSnLMxTGTCXilKhFCSZbLVDMSttdyUow` в ключе `Comment`. А еще можно увидеть Waning:
```
Comment                         : Very_secret_key = GSnLMxTGTCXilKhFCSZbLVDMSttdyUow
Warning                         : [minor] Trailer data after PNG IEND chunk
```
2) Что означает, что файл не заканчивается на чанке IEND (конец картинки). Да и котик больно много весит для своих габаритов. Пройдемся binwalk и увидим, что к концу картинки конкатенирован zip-контейнер под паролем.
3) При помощи `binwalk -e` вытаскиваем архив, применяем пароль, сдаем флаг.
