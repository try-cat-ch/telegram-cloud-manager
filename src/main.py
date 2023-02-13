import os
import random
import telebot
import requests
import json
from optparse import OptionParser

import integrateYC

parser = OptionParser()
parser.add_option(
    "-d", "--dev", dest="dev_mod", help="Use DEV Telegram Bot", default=False
)
(option, args) = parser.parse_args()

if option.dev_mod:
    bot_token = os.environ.get("BOT_TOKEN_LOCAL")
    iam_access_token = integrateYC.get_iam_local()
else:
    bot_token = os.environ.get("BOT_TOKEN_PROD")
    iam_access_token = integrateYC.get_iam_serverless()


bot = telebot.TeleBot(bot_token)


# --------------------- bot ---------------------
@bot.message_handler(commands=["help"])
def say_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет, я помогу тебе управлять инфраструктурой в YC\n"
        "Исходники здесь [here](https://github.com/try-cat-ch/telegram-cloud-manager",
        parse_mode="markdown",
    )


@bot.message_handler(func=lambda message: True)
def echo(message):
    # auth
    if str(message.from_user.id) != str(os.environ.get("USER_ID_ADMIN")):
        bot.send_message(message.chat.id, "fuck you")
        return

    if message.text.lower() == "/folders":
        folders_info = integrateYC.get_folders(iam_access_token)

        bot.send_message(message.chat.id, str(folders_info))
        return

    if message.text.lower() == "/list":
        instance_info = integrateYC.get_instances_list(iam_access_token)

        bot.send_message(message.chat.id, str(instance_info))
        return

    if "/stop" in message.text.lower():
        arg = message.text.split(maxsplit=1)[1]
        stop_vm_info = integrateYC.stop_vm(iam_access_token, arg)

        bot.send_message(message.chat.id, str(stop_vm_info))
        return

    if "/start" in message.text.lower():
        arg = message.text.split(maxsplit=1)[1]
        start_vm_info = integrateYC.start_vm(iam_access_token, arg)

        bot.send_message(message.chat.id, str(start_vm_info))
        return

    if "/restart" in message.text.lower():
        arg = message.text.split(maxsplit=1)[1]
        restart_vm_info = integrateYC.restart_vm(iam_access_token, arg)

        bot.send_message(message.chat.id, str(restart_vm_info))
        return

    if "/create" in message.text.lower():
        # arg = message.text.split(maxsplit=1)[1]
        create_vm_info = integrateYC.create_vm(access_token=iam_access_token)

        bot.send_message(message.chat.id, str(create_vm_info))
        return

    if "/delete" in message.text.lower():
        arg = message.text.split(maxsplit=1)[1]
        delete_vm_info = integrateYC.delete_vm(iam_access_token, arg)

        bot.send_message(message.chat.id, str(delete_vm_info))
        return

    bot.send_message(message.chat.id, "Seems wrong. Use /help to discover more")


# --------------- local testing ---------------
if __name__ == "__main__":
    bot.infinity_polling()
