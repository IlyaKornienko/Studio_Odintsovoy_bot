import telebot
from telebot import types

import config
import dbworker

bot = telebot.TeleBot(config.token)

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "Вкажіть, будь ласка, своє ім'я:( Чекаю...)")
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, "Вкажіть свій вік:( Чекаю...)")
    elif state == config.States.S_ENTER_DOST.value:
        bot.send_message(message.chat.id, "Вкажіть, який спосіб доставки ви обрали:( Чекаю...)")
    elif state == config.States.S_ENTER_VOITE.value:
        bot.send_message(message.chat.id, "Вкажіть, наскільки вам сподобалося обслуговування:( Чекаю...)")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Привіт! Як я можу звертатися до тебе?")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Що ж, почнемо по-новому. Як тебе звати?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(message.chat.id, "Чудове ім'я, запам'ятаю! Тепер вкажіть, будь ласка, свій вік.")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    # А вот тут сделаем проверку
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Щось не так, спробуй ще раз!")
        return
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "Якийсь дивний вік. Не вірю! Відповідай чесно.")
        return
    else:
        # Возраст введён корректно, можно идти дальше
        bot.send_message(message.chat.id, "Коли ви замовляли квіти ви обирали 1-самовивіз 2-доставка (вкажи число)?")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_DOST.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DOST.value)
def user_entering_age(message):
    # А вот тут сделаем проверку
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Щось не так, спробуй ще раз!")
        return
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if int(message.text) < 1 or int(message.text) > 2:
        bot.send_message(message.chat.id, "Немає такого варінту. Спробуй ще 1-самовивіз чи 2-доставка")
        return
    else:
        # Возраст введён корректно, можно идти дальше
        bot.send_message(message.chat.id, "Круто! Дякую тобі!"
                                          "Як тобі обслуговування в нашому магазині (від 1 до 5)?")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_VOITE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_VOITE.value)
def user_entering_voite(message):
    # А вот тут сделаем проверку
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Щось не так, спробуй ще раз!!!")
        return
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if int(message.text) < 1 or int(message.text) > 5:
        bot.send_message(message.chat.id, "Поставте будь ласка оцінку від 1 до 5.")
        return
    else:
        bot.send_message(message.chat.id, "Дякуємо тобі за твій відгук. Залиши будьласка відгук на " '[google maps](https://g.page/studio-odintsovoy-flowers?share)', parse_mode='Markdown')
        dbworker.set_state(message.chat.id, config.States.S_START.value)

if __name__ == "__main__":
    bot.infinity_polling()
