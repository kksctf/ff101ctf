# Роботы
Author: `@greg0r0`

## Desc

> В категории Web обычно находятся таски с задачей найти уязвимости или миссконфигурации на различных имитациях веб-ресурсов. В простых тасках надо сделать что-то примитивное (например, вставить кавычку) и получить флаг - в сложных же необходимо реализовать атаку на ресурс в несколько этапов. Типовые уязвимости, которые можно встретить в этой категории: CSRF, IDOR, XSS, SQLI, SSRF и другие веб-вулны. А еще можно встретить таски на использование тонкостей веб-технологий, знания которых точно также могут пригодиться. Если вы хотите продвигаться по ветке развития навыков тестирования на проникновение (PenTest) - то стоит решать таски именно этой категории.

Нас предупреждали, что с текущим развитием ИИ нам не грозит восстание роботов. Но кто ж знал, что все начнется с незначительного запроса малоизвестного поискового робота...

`<ip>:<port>`

## Flag

```
ptctf{s1mpl3_but_p0w3rful_w3b_t3ch}
```

## Solve

Простой таск, описание и название которого жирно намекает на функционал /robots.txt - об этой технологии можно [вот тут](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=ru)

В крайнем случае - этот роут должен найтись каким-то легковесным сканером по типу [dirsearch](https://github.com/maurosoria/dirsearch)

Видим в файле "секретную ручку" и переходим по ней - среди нулей и единиц видим флаг и сдаем его.