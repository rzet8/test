import telebot
import pymysql
from telebot import TeleBot, \
    types

db = pymysql.connect("us-cdbr-east-02.cleardb.com", "b2205ac2fa816b", "0b26771a", "heroku_aab66e56c5d646a")
cursor = db.cursor()

#cursor.execute("CREATE TABLE `heroku_aab66e56c5d646a`.`test2` ( `id` VARCHAR(255) NOT NULL , `ds` VARCHAR(255) NOT NULL , UNIQUE (`id`))")
#db.commit()

cursor.execute("SELECT * FROM `test2`")
print(cursor.fetchall())


bot = TeleBot("1441966878:AAGGP4iVaDl-xmc96ixvBwQpUNHeXPwgW3k")

@bot.message_handler(commands=['start', 'desc', 'info'])
def poll_commands(message: types.Message):
    if message.text == "/start":
        bot.send_message(message.chat.id, "Hello")
        try:
            cursor.execute(f"INSERT INTO `test2`(`id`, `ds`) VALUES ('{message.chat.id}','test')")
            db.commit()
        except:
            pass
    
    elif "/desc" in message.text:
        cursor.execute(f"""UPDATE `test2` SET `ds`= '{message.text.replace("/desc ", "")}' WHERE `id` = '{message.chat.id}'""")
        db.commit()
        bot.send_message(message.chat.id, f"""Description successfully updated to {message.text.replace("/desc ", "")}""")

    elif message.text == "/info":
        cursor.execute(f"SELECT * FROM `test2` WHERE `id` = {message.chat.id}")
        desc = cursor.fetchone()[1]

        bot.send_message(message.chat.id, f"Your description = {desc}")


@bot.message_handler(commands=['desc'])
def poll_desc(message: types.Message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['text'])
def poll_text(message: types.Message):
    bot.send_message(message.chat.id, message.text)

if __name__ == "__main__":
    bot.polling(True)


