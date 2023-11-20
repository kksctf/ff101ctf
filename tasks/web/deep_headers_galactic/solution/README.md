# Deep Headers Galactic
Author: `@greg0r0`

## Desc
В давней давней истории был один разведчик...

`<ip>:<port>`

## Flag

```
ptctf{just_s0m3_h34d3r_m3ss}
```

## Solve
```
curl --header 'Date: Tue, 24 Jan 1999' --header 'Accept-Language: cs-cs' --header 'User-Agent: Lynx/2.8.9' --header 'Accept: image/png' http://<ip>:<port>
```
Классический таск на подбор хедеров. [Вот еще пример такого таска](https://ctftime.org/writeup/26905). Довольно частый типаж, главное понять смысл очередного всплывающего сообщения.