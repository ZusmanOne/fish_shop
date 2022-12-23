# Бот для продажи  рыбы в Telegram

Данный бот служит как интернет-магазин, поставляющий рыбу по всей России.

## Как запустить бота
Скачайте код  
```
https://github.com/ZusmanOne/fish_shop.git
```
перейдите в скачанный каталог 
```sh
cd fish_shop
```
[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```



Создайте файл `.env` в корне каталога `fish_shop/`  со следующими настройками:

- `TG_TOKEN` — для этого вам нужно написать [отцу ботов](https://telegram.me/BotFather)
- `TG_ID` — для этого нужно написать [этому боту](https://telegram.me/getmyid_bot)
- `CLIENT_ID`-yiLVdBsYI5uaYNMPPkI7Rf2TXxeRfZAf6tcxdxPfjJ
- `CLIENT_SECRET`O2qmHZ2zM0eR0lqywNeYdCR7STCOMZ7RTNYjRVGyTu


Зарегистрируйтесь на [redislabs](https://redis.com/)

Получите адрес БД вида redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com, его порт вида: 16635 и его пароль.

- `REDIS_HOST` - redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com
- `REDIS_PORT`- 13965
- `REDIS_PASSWORD`- указан в конфигурции вашей базы на [сайте](https://app.redislabs.com/) в разделе Security

## Функционал бота
- Для запуска и перезапуска выполните  команду `/start`
- Откроется меню, которая состоит из товаров магазина и корзины
- Можно выбрать товар, что бы узнать его подробности и заказать
- Так же есть функция оплаты товаров, данная кнопка появится при переходе в корзину
- При нажатии `оплатить` вам предложат оставить свою почту для дальнейшей связи.