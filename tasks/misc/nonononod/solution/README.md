# Nonononod
Author: `@chiukki`

## Desc
Пожалуйста, используйте наш калькулятор правильно. И не выходите за рамки дозволенного.

`http://{server_addr}:5689/`

## Flag

```
ptctf{l3t_m3_0ut_0f_h3r3}
```

## Solve

tl;dr; PyJail

В начале указана инструкция - пробуем написать в форму "gcd(1,2)" и получаем ответ.
Написав любую другую белиберду будет ошибка "Нет такой функции".
Из чего можно предположить, что нам надо вызвать какую-то функцию (подсказка есть в инструкции)
Функция get_flag() даст ответ "Скажи волшебное слово"
Написав get_flag("please") ты получаешь флаг :)
