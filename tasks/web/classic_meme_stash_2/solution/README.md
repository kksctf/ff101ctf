# Classic Meme Stash 2
Author: `@disasm_me`

## Desc
Я писал jwt-аутентификацию в 3 часа ночи, и она настолько гениальная, что утром я не смог понять свой же код.

От греха подальше отключил вход для пользователя `jwt_is_unbreakable`, мало ли что...

## Flag

```
ptctf{4w3s0m3_jw7_unh4ck1ng}
```

## Solve
```
В первом таске в одной из админской картинок отображен наш jwt - jwt_st0red_in_file

Используя его и код серверной части, можно успешно подписать токен для любого пользователя и обойти функционал бана
```