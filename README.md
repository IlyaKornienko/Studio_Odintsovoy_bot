Создал Telegram бота для Instagram страницы [Studio_Odintsovoy](https://www.youtube.com/watch?v=Kh16iosOTIQ).

В учебных целях взял пример создания бота [Урок 11](https://mastergroosha.github.io/telegram-tutorial/docs/lesson_11/). 

Бот представляет собой небольшой опросник для оценки качестава обслживания, узнать как покупатели предпочитают забирать заказ (доставка или самовывоз).

Используется библиотеки telebot, config, dbworker.

Бот запускается в Docker.

Прокинул volume для сохранения базы данных.

```
docker run -d --name so_bot /home/_путь к базе данных_/database.vdb:/home/database.vdb
```
