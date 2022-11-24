import json
import math
from time import sleep

from pyrogram import Client, filters

import config

app = Client("my_account", config.API_ID, config.API_HASH)

data = {}
with open("database.json", "r") as read_file:
    data = json.load(read_file)


async def get_massage_from_date(date, chat_id):
    async for message in app.get_chat_history(chat_id):
        if message.date == date:
            return message


@app.on_message(filters.command("start", prefixes="!") & filters.me)
def start(client, message):
    if message.text == "!start" or message.text == "!start ":
        message.edit("Must be longer than two arguments")
    else:
        argsString = message.text.split("!start ", maxsplit=1)[1]
        args = argsString.split(" ")
        if args[0] in config.START_ARGS["recording"]["usage"]:
            message.edit("chat recording started")
            if len(args) == 1:
                temp_user = "553147242"
                title = message.chat.title
                if title is None:
                    title = message.chat.username
                mirror = app.create_group("mirror " + title, [app.get_me().id, temp_user])

                app.ban_chat_member(mirror.id, temp_user)

                data['recorded'][str(message.chat.id)] = mirror.id
                with open("database.json", "w") as write_file:
                    json.dump(data, write_file)
            elif len(args) == 2:
                if args[1] == "me":
                    data['recorded'][message.chat.id] = "me"
                    with open("database.json", "w") as write_file:
                        json.dump(data, write_file)
                    app.restart()
                else:
                    try:
                        data['recorded'][message.chat.id] = int(args[1])
                        with open("database.json", "w") as write_file:
                            json.dump(data, write_file)
                        app.restart()
                    except ValueError:
                        message.edit("argument 2 must be id of chat")
        elif args[0] in config.START_ARGS["dice"]["usage"]:
            app.send_dice(message.chat.id)
        else:
            message.edit("command undefined")

    sleep(1)
    message.delete()


@app.on_message(filters.command("stop", prefixes="!") & filters.me)
def stop(client, message):
    if message.text == "!stop" or message.text == "!stop ":
        message.edit("Must be longer than two arguments")
    else:
        argsString = message.text.split("!stop ", maxsplit=1)[1]
        args = argsString.split(" ")
        if args[0] in config.STOP_ARGS["recording"]["usage"]:
            message.edit("chat recording stoped")
            try:
                data['recorded'].pop(str(message.chat.id))
                with open("database.json", "w") as write_file:
                    json.dump(data, write_file)
            except Exception:
                print(str(Exception))
                message.edit("Some errors, try later")

        else:
            message.edit("command undefined")

    sleep(1)
    message.delete()


@app.on_message(filters.command("get", prefixes="!") & filters.me)
def get(client, message):
    message_text = ""

    if (message.text == "!get" or message.text == "!get "):
        message_text = "Must be longer than two arguments"
    else:
        argsString = message.text.split("!get ", maxsplit=1)[1]
        args = argsString.split(" ")

        if len(args) > 0:

            if args[0] in config.GET_ARGS["info"]["usage"]:
                if len(args) > 1:
                    if args[1] in config.GET_ARGS["chat"]["usage"]:  
                        id = message.chat.id
                        if len(args) > 2:
                            id = int(args[2])
                        
                        chat = app.get_chat(id)
                        message_text = "------------------------------\n"
                        message_text += f"id - <a href='tg://user?id={id}>{id}</a>\n"
                        if str(chat.type) == "ChatType.PRIVATE":
                            message_text += "Type - private\n"
                            message_text += f"Username - {chat.username}\n"
                            if chat.first_name != None:
                                message_text += f"First name - {chat.first_name}\n"
                            if chat.last_name != None:
                                message_text += f"Last name - {chat.last_name}\n"
                        if str(chat.type) == "ChatType.GROUP":
                            message_text += f"Title - {chat.title}\n"
                            message_text += f"Members count - {chat.members_count}\n"
                            message_text += f"Can you send a messages - {chat.permissions.can_send_messages}\n"
                            message_text += f"Are you a creator of chat - {chat.is_creator}\n"
                            message_text += f"Can you edit info - {chat.permissions.can_change_info}\n"
                        
                        message_text += "------------------------------"
                    else:
                        message_text = "Invalid argument"
                else:
                    message_text = "Must be longer than two arguments"
            elif args[0] in config.GET_ARGS["database"]["usage"]:
                with open("database.json", "r") as read_file:
                    database = json.load(read_file)
                    message_text += "------------------------------\n"
                    message_text += "Recorded chats:\n"
                    if database["recorded"] == {}:
                        message_text += "No recorded chats\n"
                    else:
                        for recorded_chat in database["recorded"].keys():
                            id1 = int(recorded_chat)
                            id2 = int(database['recorded'][recorded_chat])
                            
                            message_text += f"Chat: <a href='tg://user?id={str(id1)}'>{id1}</a>. Mirror: <a href='tg://user?id={str(id2)}'>{id2}</a>.\n"
                    message_text += "------------------------------"
            elif args[0] in config.GET_ARGS["pow"]["usage"]:
                if len(args) > 1:
                    s = 2
                    if len(args) > 2:
                        s = int(args[2])

                    a = int(args[1])

                    message_text = str(pow(a, s))
                else:
                    message_text = "Invalid argument"
            elif args[0] in config.GET_ARGS["sqrt"]["usage"]:
                s = 2
                if len(args) > 2:
                    s = int(args[2])

                a = int(args[1])

                message_text = str(math.pow(a, 1 / s))
            elif args[0] in config.GET_ARGS["cos"]["usage"]:
                a = int(args[1])
                message_text = str(round(math.cos(math.radians(a)), 3))
            elif args[0] in config.GET_ARGS["sin"]["usage"]:
                a = int(args[1])
                message_text = str(round(math.sin(math.radians(a)), 3))
            elif args[0] in config.GET_ARGS["tg"]["usage"]:
                a = int(args[1])
                message_text = str(round(math.tan(math.radians(a)), 3))
            else:
                message_text = "Invalid argument"
        else:
            message_text = "Must be longer than two arguments"

    app.send_message("me", message_text, parse_mode=app.parse_mode.HTML)
    message.edit(message_text, parse_mode=app.parse_mode.HTML)
    sleep(1)
    message.delete()


@app.on_message(filters.command("help", prefixes="!") & filters.me)
def help(client, message):
    help_message = "------------------------------\n"
    if message.text == "!help" or message.text == "!help ":
        help_message += "<b>AllCommands:</b>\n"
        for i in config.ALL_COMMANDS.keys():
            help_message += f"!{i} - <i>{config.ALL_COMMANDS[i]['description']}</i>\n"
        help_message += "------------------------------"
    else:
        argsString = message.text.split("!help ", maxsplit=1)[1]
        args = argsString.split(" ")

        if args[0] in config.ALL_COMMANDS.keys():
            help_message += f"<b>Command: <i>!{args[0]}</i></b>\n"
            help_message += f"Description: <i>{config.ALL_COMMANDS[args[0]]['description']}</i>\n"

            if config.ALL_COMMANDS[args[0]]["args"] != {}:
                help_message += f"<b>Arguments:</b>\n"
                command_arguments = config.ALL_COMMANDS[args[0]]["args"]
                for argument_name in command_arguments.keys():
                    help_message += f"{argument_name} - <i>{command_arguments[argument_name]}</i>\n"

            help_message += "------------------------------"
        else:
            help_message = "Command not found"

    # message.edit(help_message, parse_mode=app.parse_mode.HTML)
    app.send_message("me", help_message, parse_mode=app.parse_mode.HTML)
    # sleep(1)
    message.delete()


@app.on_message()
def retraslate(client, message):
    chatId = str(message.chat.id)
    if chatId in data['recorded'].keys():
        if config.PRINT_RETRANSLATED_MESSAGES:
            print(f"From @{message.from_user.username}: {message.text}")

        if data['recorded'][chatId] == "me":
            app.forward_messages("me", int(chatId), message.id)
        else:
            app.forward_messages(int(data['recorded'][chatId]), int(chatId), message.id)


@app.on_edited_message()
async def retraslate_edited(client, message):
    chatId = str(message.chat.id)
    if chatId in data['recorded'].keys():
        if config.PRINT_RETRANSLATED_MESSAGES:
            print(f"@{message.from_user.username} edited message sended {message.date} to {message.text}")
        sleep(2)
        edited_message = await get_massage_from_date(message.date, data['recorded'][chatId])
        await app.send_message(data['recorded'][chatId], f"edited to: {message.text}",
                               reply_to_message_id=edited_message.id)


if __name__ == "__main__":
    print("Starting...")
    app.run()
