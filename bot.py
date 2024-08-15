from rubpy import Client
from rubpy.types import Updates
from requests import get
import aiohttp
import info  # محل ذخیره اطلاعات    #Information storage location
import codecs
import json
import guids as g
import links


# --------------------------------------
# Author: Taha Samani
# --------------------------------------
# تابع ایسینک برای ارسال ریکوست
# async function to send request
async def get_response(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


# --------------------------------------
links = links.links  # links
# --------------------------------------
guids = g.guid  # guids groups
# --------------------------------------
# گرفتن و ذخیره گوید گروه ها
# get and save guids
name = "taha"
with Client(name=name, display_welcome=False) as tss:
    for link in links:
        info_link = tss.join_group(link=link)
        if info_link["is_valid"] == True:
            guid = info_link["group"]["group_guid"]
            if guid not in guids:
                guids.append(guid)
                with codecs.open("guids.py", "w", encoding="utf-8") as file:
                    file.write(f"guid = {guids}")
                    file.close()
                tss.send_message(
                    guid,
                    f"ادمین کنید من را در گروه \nadmin me in  group\n{info_link["group"]["group_title"]}",
                )
                print("guids append.")
client = Client(
    name=name
)  # برای این حالت دستور بالا کامنت شود    #Comment the command above for this mode


@client.on_message_updates()
async def main(update: Updates):
    # تعیین متغییر ها
    # Define variables
    ob_g = update.object_guid
    if ob_g in guids:
        print(update)
        if update.is_text:
            text = update.text
        else:
            text = ""
        au_g = update.author_guid
        msg_id = update.message_id
        type_update = update["message"]["type"]
        group_info = await client.get_group_info(ob_g)
        group_title = group_info["group"]["group_title"]
        if update.reply_message_id:
            r_msg_id = update.reply_message_id
        else:
            r_msg_id = None
        if r_msg_id != None:
            msg_by_id = await client.get_messages_by_id(ob_g, [r_msg_id])
            msg = msg_by_id["messages"][0]
            if "text" in msg:
                text_msg = msg["text"]
                au_g_msg = msg["author_object_guid"]
            else:
                text_msg = None
                au_g_msg = None

        # --------------------------------------
        # تابع برای ذخیره و دریافت اطلاعات فایل
        # Function to save and receive file information
        async def load_data():
            try:
                with codecs.open(f"data{ob_g}.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    file.close()
            except FileNotFoundError:
                data = {
                    "lang": "fa",
                    "loocks": {
                        "Gif": False,
                        "Image": False,
                        "Video": False,
                        "Voice": False,
                        "Sticker": False,
                        "Text": False,
                        "forwarded_from": True,
                        "rubino_story_data": True,
                        "file_inline": False,
                        "id": False,
                        "link": True,
                    },
                    "voice": {"mod": "off"},
                    "max_warnings": 4,
                    "dict": {},
                }
            return data

        async def save_data(name_data: str, data_key: str, data_value: str):
            data = await load_data()
            if name_data in data:
                data_x = data[name_data]
            else:
                data_x = {}
            if data_key != None:
                data_x[data_key] = data_value
            else:
                data_x = {}
            data[name_data] = data_x
            with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as file_:
                json.dump(data, file_, indent=2, ensure_ascii=False)
                file_.close()

        data = await load_data()
        # --------------------------------------
        # تعیین اینکه نویسنده پیام ادمین هست یا خیر
        # Determining whether the author of the message is an admin or not
        is_admin = await update.is_admin(ob_g, au_g)
        # --------------------------------------
        #  دریافت و ذخیره متغییر فایل info
        # Get and save the info file variable
        loocks = info.loocks
        if data["lang"] == "fa":
            list_command = info.list_command
            doc_user = info.doc_user
            doc1 = info.doc1
            doc2 = info.doc2
        else:
            list_command = info.list_command_en
            doc_user = info.doc_user_en
            doc1 = info.doc1_en
            doc2 = info.doc2_en
        # شرط تغییر زبان
        # Language change condition
        if text.startswith(list_command[44]):
            text = text[len(list_command[44]) :]
            if text in ["fa", "en"]:
                data["lang"] = text
                with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.close()
                    if data["lang"] == "fa":
                        list_command = info.list_command
                    else:
                        list_command = info.list_command_en
                await client.action_on_message_reaction(ob_g, msg_id, 2)
                a = await client.send_message(ob_g, list_command[45], msg_id)
                await client.set_pin_message(
                    ob_g, a["message_update"]["message_id"], "Pin"
                )
            else:
                await client.action_on_message_reaction(ob_g, msg_id, 3)

        # --------------------------------------
        # تابع برای پاسخ ربات به کلمات و جملات دیشنری که بستگی به مود دارد
        # The function for the robot's response to the words and sentences of the dict that depends on the mode
        async def send_text_to_voice(txt: str):
            mod = data["voice"]["mod"]
            if mod != "off":
                if mod == "man":
                    url = (
                        f"https://api-free.ir/api/voice.php?text={txt}&mod=FaridNeural"
                    )
                    response = await get_response(url)
                    print(response)
                    response = get(response["result"])
                    with open("bot.ogg", "wb") as f:
                        f.write(response.content)
                    await client.send_voice(ob_g, "bot.ogg", txt, msg_id)
                else:
                    url = (
                        f"https://api-free.ir/api/voice.php?text={txt}&mod=DilaraNeural"
                    )
                    response = await get_response(url)
                    response = get(response["result"])
                    with open("bot.ogg", "wb") as f:
                        f.write(response.content)
                    await client.send_voice(ob_g, "bot.ogg", txt, msg_id)
            else:
                await client.send_message(ob_g, txt, msg_id)

        # --------------------------------------
        # تابع برای ارسال اطلاعات ممبر
        # Function to send member information
        async def send_info_user(ob_user: str):
            user_info = await client.get_user_info(ob_user)
            user_guid = user_info["user"]["user_guid"]
            user_name = user_info["user"]["first_name"]
            if "last_name" in user_info["user"]:
                user_last_name = user_info["user"]["last_name"]
            else:
                user_last_name = list_command[0]
            if "username" in user_info["user"]:
                user_id = user_info["user"]["username"]
            else:
                user_id = list_command[0]
            if "bio" in user_info["user"]:
                bio_user = user_info["user"]["bio"]
            else:
                bio_user = list_command[0]
            if ob_user in data:
                if "info" in data[ob_user]:
                    your_info = data[ob_user]["info"]
            else:
                your_info = list_command[0]
            information_user = f"{list_command[1]} : {your_info}\n\n{list_command[2]} : 👇\n{user_name} \n\n{list_command[3]} : 👇\n{user_last_name}\n\n{list_command[4]} :👇\n@{user_id}\n\n{list_command[5]} : 👇\n{bio_user}"
            try:
                profile_user = await client.download_profile_picture(ob_user)
                with open("profile.png", "+wb") as fi:
                    fi.write(profile_user)
                await client.send_photo(
                    ob_g, "profile.png", information_user, msg_id, is_spoil=True
                )
            except:
                await client.send_message(ob_g, information_user, msg_id)

        # --------------------------------------
        # ارسال راهنما ها
        # Send guides
        if text == list_command[42]:
            await client.send_message(ob_g, doc_user, msg_id)
        if text == list_command[43]:
            await client.send_message(ob_g, doc1, msg_id)
            await client.send_message(ob_g, doc2, msg_id)
        # --------------------------------------
        # پاسخ به رویداد ها
        # Respond to events
        if type_update == "Event":
            evant_data = update["message"]["event_data"]
            user = evant_data["performer_object"]["object_guid"]
            info_event_user = await client.get_user_info(user)
            name_user_event = info_event_user["user"]["first_name"]
            if evant_data["type"] == "PinnedMessageUpdated":
                is_pin_msg = True
                await client.send_message(
                    ob_g, f"{list_command[6]} {name_user_event}", msg_id
                )
            else:
                is_pin_msg = False
            if evant_data["type"] == "LeaveGroup":
                is_level_group = True
                await client.send_message(
                    ob_g, f"{name_user_event} {list_command[7]}", msg_id
                )
            else:
                is_level_group = False
            if evant_data["type"] == "JoinedGroupByLink":
                join_by_link = True
                await client.send_message(
                    ob_g,
                    f"{list_command[8]} {name_user_event} {list_command[9]} {group_title}",
                    msg_id,
                )
            else:
                join_by_link = False
        # --------------------------------------
        # ارسال لینک گروه
        # Send group link
        if text == list_command[13]:
            link_group = await client.get_group_link(ob_g)
            await client.send_message(ob_g, link_group["join_link"], msg_id)
        # --------------------------------------
        # ارسال اطلاعات نویسنده پیام
        # Send message author information
        if text == list_command[14]:
            await send_info_user(au_g)
        # --------------------------------------
        # ارسال اطلاعات نویسنده پیام ریپلای شده
        # Send the information of the author of the replied message
        if text == list_command[15]:
            await send_info_user(au_g_msg)
        # --------------------------------------
        # ثبت بیو
        # Bio registration
        if text == list_command[19]:
            await save_data(au_g, "info", text_msg)
        # --------------------------------------
        # حذف بیو
        # Remove bio
        if text == list_command[20]:
            await save_data(au_g, "info", list_command[0])

        # --------------------------------------
        # تابع چک کردن تعداد اخطار و بن و حذف پیام ممنوعه
        # The function of checking the number of warnings and ban and deleting prohibited messages
        async def check_warnings(name_warinng: str):
            await client.delete_messages(ob_g, [msg_id])
            user_info = await client.get_user_info(au_g)
            user_name = user_info["user"]["first_name"]
            if au_g in data:
                if "warnings" in data[au_g]:
                    user_warnings = data[au_g]["warnings"]
                    user_warnings = user_warnings + 1
                    await save_data(au_g, "warnings", user_warnings)
                    await client.send_message(
                        ob_g,
                        f"{user_name}\n{list_command[29]}{name_warinng}\n{list_command[30]}{user_warnings}",
                    )
                    if user_warnings == data["max_warnings"]:
                        await client.send_message(
                            ob_g, f"{user_name}\n{list_command[31]}"
                        )
                        await client.ban_group_member(ob_g, au_g)
                        await save_data(au_g, "warnings", 0)
                else:

                    await save_data(au_g, "warnings", 1)
                    await client.send_message(
                        ob_g,
                        f"{user_name}\n{list_command[29]}{name_warinng}\n{list_command[30]} 1",
                    )
            else:
                await save_data(au_g, "warnings", 1)
                await client.send_message(
                    ob_g,
                    f"{user_name}\n{list_command[29]}{name_warinng}\n{list_command[30]} 1",
                )

        # --------------------------------------
        # ارسال ضعیت قفل ها
        # Send locks status
        if text == list_command[26]:
            statuse = f'{list_command[27]}{data["max_warnings"]}\n'
            for k, v in data["loocks"].items():
                if v == True:
                    v = "🔒✅"
                else:
                    v = "🔓❎"
                statuse = statuse + f"{k} »» {v}\n\n"
            await client.send_message(ob_g, statuse, msg_id)
        # --------------------------------------
        # تیپ پیامی که قفله اینجا پاک میشه
        # The message type that is locked will be deleted here
        if is_admin == False:
            for i in range(len(loocks)):
                loock = loocks[i]
                if data["loocks"][loock] == True:
                    if update["message"]["type"] == loock:
                        await client.delete_messages(ob_g, [msg_id])
                    if update["message"]["type"] == "FileInline":
                        if update["message"]["file_inline"]["type"] == loock:
                            await client.delete_messages(ob_g, [msg_id])
                    if loock in update["message"]:
                        await client.delete_messages(ob_g, [msg_id])
                    if loock == "forwarded_from":
                        if "forwarded_from" in update["message"]:
                            await check_warnings(list_command[32])
                    if loock == "rubino_story_data":
                        if "rubino_story_data" in update["message"]:
                            await check_warnings(list_command[33])
                    if loock == "id":
                        if "@" in text:
                            await check_warnings(list_command[34])
                    if loock == "link":
                        if "http" in text:
                            await check_warnings(list_command[35])
        # --------------------------------------
        # دستورات ادمین
        # Admin commands
        if is_admin == True:
            # ایجاد کلمه و جمله در دیکشنری ربات
            # Creating words and sentences in the robot dictionary
            if list_command[36] and list_command[37] in text:
                try:
                    start_key = text.index(list_command[36]) + len(list_command[36])
                    end_key = text.index(list_command[37])
                    start_value = text.index(list_command[37]) + len(list_command[37])
                    key_dict = text[start_key:end_key].strip()
                    value_dict = text[start_value:].strip()
                    await save_data("dict", key_dict, value_dict)
                    await client.action_on_message_reaction(ob_g, msg_id, 2)
                except:
                    await client.action_on_message_reaction(ob_g, msg_id, 3)
            # --------------------------------------
            # حذف جمله یا کلمه از دیکشنری ربات
            # Deleting a sentence or word from the robot's dictionary
            if text.startswith(list_command[38]):
                key_del = text[len(list_command[38]) :].strip()
                if key_del in data["dict"]:
                    del data["dict"][key_del]
                    with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        f.close()
                    await client.action_on_message_reaction(ob_g, msg_id, 2)
                else:
                    await client.action_on_message_reaction(ob_g, msg_id, 3)
            # --------------------------------------
            # تغییر مود ویس
            # Change the voice mode
            if text.startswith(list_command[41]):
                len_mod = len(list_command[41])
                mod = text[len_mod:]
                if mod in ["off", "man", "woman"]:
                    await save_data("voice", "mod", mod)
                    await client.action_on_message_reaction(ob_g, msg_id, 2)
                else:
                    await client.action_on_message_reaction(ob_g, msg_id, 3)
            # --------------------------------------
            # تعیین حداکثر اخطارها
            # Set the maximum number of warnings
            if text.startswith(list_command[28]):
                text = text[len(list_command[28]) :].strip()
                data["max_warnings"] = int(text)
                with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.close()
            # --------------------------------------
            # بازکردن قفل تیپ پیامی
            # Unlocking the message type
            if text.startswith(list_command[25]):
                w = len(list_command[25])
                text = text[w:]
                if text in loocks:
                    data["loocks"][text] = False
                    with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        f.close()
                    await client.action_on_message_reaction(ob_g, msg_id, 2)
                else:
                    await client.action_on_message_reaction(ob_g, msg_id, 3)
            # --------------------------------------
            # قفل کردن تیپ پیام
            # Lock the message type
            if text.startswith(list_command[24]):
                w = len(list_command[24])
                text = text[w:]
                if text in loocks:
                    data["loocks"][text] = True
                    with codecs.open(f"data{ob_g}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        f.close()
                    await client.action_on_message_reaction(ob_g, msg_id, 2)
                else:
                    await client.action_on_message_reaction(ob_g, msg_id, 3)
            # --------------------------------------
            # بن ممبر از گروه
            # Ban member of the group
            if text == list_command[16]:
                if is_admin == True:
                    if await update.is_admin(ob_g, au_g_msg):
                        await client.send_message(ob_g, list_command[17], msg_id)
                    else:
                        await client.ban_group_member(ob_g, au_g_msg)
                else:
                    await update.reply(list_command[18])
            # --------------------------------------
            # حذف گروهی پیام ها
            # Group deletion of messages
            if text.startswith(list_command[21]):
                text = text[-1]
                try:
                    for i in range(0, int(text)):
                        msg_for_del = await client.get_messages_interval(ob_g, msg_id)
                        del_list_ids = []
                        for x in range(0, len(msg_for_del["messages"])):
                            del_list_ids.append(
                                msg_for_del["messages"][x]["message_id"]
                            )
                        await client.delete_messages(ob_g, del_list_ids)
                    await client.send_message(
                        ob_g, f"{list_command[22]} : {25*int(text)}", msg_id
                    )
                except:
                    await client.send_message(ob_g, list_command[23])
            # --------------------------------------
            # تنظیم پروفایل گروه
            #  Set group profile
            if text == list_command[10]:
                photo_avatar = await client.download(msg["file_inline"])
                with open("taha.png", "+wb") as file_me:
                    file_me.write(photo_avatar)
                await client.upload_avatar(ob_g, "taha.png")
                await client.action_on_message_reaction(ob_g, msg_id, 2)
            # --------------------------------------
            # حذف پروفایل گروه
            # Delete the group profile
            if text == list_command[11]:
                avatar = await client.get_avatars(ob_g)
                avatar_id = avatar["avatars"][0]["avatar_id"]
                await client.delete_avatar(ob_g, avatar_id)
                await client.action_on_message_reaction(ob_g, msg_id, 2)
            # --------------------------------------
            # بیو گروه را تغییر دادن
            # Change group bio
            if text == list_command[12]:
                await client.edit_group_info(group_guid=ob_g, description=text_msg)
                await client.action_on_message_reaction(ob_g, msg_id, 2)
        # --------------------------------------
        # چک کردن اینکه ایا پیام ارسال شده در دیکشنری است یا نه اگر بود جواب مناسب بده
        # Checking whether the sent message is in the dictionary or not, if it is, give an appropriate answer
        if text in data["dict"]:
            await send_text_to_voice(data["dict"][text])
        # ارسال دیکشنری
        # Send dictionary
        if text == list_command[39]:
            data_bot = ""
            for k, v in data["dict"].items():
                data_bot = data_bot + k + " »»» " + v + "\n"
            with codecs.open("data.html", "w", encoding="utf-8") as file_bot:
                file_bot.write(
                    f'<!DOCTYPE html><html dir="rtl" lang="fa"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document bot</title></head><body style="background-color: rgb(0, 84, 87);"><divs style="display: flex;margin: 50px auto;width: 80vw;font-size: 12px;background-color:#ffffff1d;backdrop-filter: blur(8px);border: 1px solid rgba(145, 145, 145, 0);box-shadow: 0px 0px 30px rgba(227,228,237,0.37);border-radius: 20px;padding: 10px;"><pre style="text-wrap: wrap;text-align: justify;">{data_bot}</pre></div></body></html>'
                )
                file_bot.close()
            await client.send_document(
                ob_g, "data.html", caption=list_command[40], reply_to_message_id=msg_id
            )


client.run()
# --------------------------------------
# --------------------------------------
