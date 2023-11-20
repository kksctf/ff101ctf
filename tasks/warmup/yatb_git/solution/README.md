# Ветка
Author: `@greg0r0`

## Desc
> Формально, под понятием ["Digital **Forensic**"](https://www.interpol.int/en/How-we-work/Innovation/Digital-forensics#:~:text=Digital%20forensics%20is%20a%20branch,crucial%20for%20law%20enforcement%20investigations.) понимают расследование преступлений с использованием компьютерных технологий обработки и хранения информации. Но важно отметить, что в формат CTF очень сложно заснуть полноценное расследование и поэтому в категории Forensic вы найдете задачи на исследование различных артефактов: файлов, логов, сетевого трафика, дампов RAM, файловых систем etc. В целом тут существует множество разнообразных типов заданий, но цель всегда одна - разобраться что перед вами и что с этим не так. Эта категория будет полезна тем, кто хочет работать, собственно, с Digital Forensic: SOC, вирусная аналитика, расследование инцидентов etc.

Иногда новенькие оставляют секреты в проектах. Я не исключение...

[yatb.zip](./yatb.zip)

## Flag

```
ptctf{d0nt_f0rs4k3_s3cr3t_d4t4_1n_g1t}
```

## Solve

В проекте есть директория .git, сам проект есть на github и название таска как бы намекает. 

Смотрим доступные ветки, делаем `git checkout` на ветку `scoreboard-graph` и в `git log` видим следующие логи:

```
commit 215215683301214c4bc13e3f15d089481fac57aa (HEAD -> scoreboard-graph)
Author: undefineduser <undefineduser@internet.com>
Date:   Wed Nov 8 16:29:44 2023 +0300

    Update Secret Environment Key for FF101 AGAIN

commit 9952d244e7a593b4d76b48d67b007fa3caf908f3
Author: undefineduser <undefineduser@internet.com>
Date:   Wed Nov 8 16:28:53 2023 +0300

    Update Secret Environment Key for FF101

```

Cмотрим какие файлы были затронуты при помощи `git show 9952d244e7a593b4d76b48d67b007fa3caf908f3`:

```
@@ -1,6 +1,6 @@
 YATB_DEBUG = False

-YATB_JWT_SECRET_KEY = s3cr3t_keys_that_you_maybe_need_to_change
+YATB_JWT_SECRET_KEY = ptctf{d0nt_f0rs4k3_s3cr3t_d4t4_1n_g1t}
```