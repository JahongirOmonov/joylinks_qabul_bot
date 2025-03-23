from datetime import date
from aiogram.fsm.context import FSMContext
from bot.states.main import SmsForAdmin, RegisteredUsersState
from bot.utils.orm import get_user, get_channels
import common.tasks
from aiogram import types, Bot
from common.models import TelegramProfile, BannedUser, RegisteredUsers
from datetime import datetime
from django.utils.timezone import make_aware
from utils.choices import Role
import aiohttp
from src.settings import API_TOKEN
from bot.keyboards.outline import phone_number
import re
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime
import pytz

bot = Bot(token=API_TOKEN)


async def start(message: types.Message, bot: Bot, state: FSMContext):
    user = await get_user(message.chat)
    # current_date = date.today()


    # current_time = datetime.now().strftime("%H:%M:%S")
    text = (f"<b>👋 Assalomu alaykum 😊\n"
            f"📌Ismingizni kiriting✍️ </b>")
    # mention = f"<a href='tg://user?id={user.chat_id}'>{user.first_name}</a>"
    # notification = (f"Diqqat!!!   ID: {user.id}  \n\n"
    #                 f"{mention} ro'yhatdan o'tdi✅ \n\n"
    #                 f"Sana: {current_date}  |  {current_time}")
    # file_id="BAACAgIAAxkBAAOOZ0jMg14gDmGTJE79dN40zes2BNMAAnheAALgIUlKkj-4CcsokSE2BA"
    # caption = "📹Botning barcha imkoniyatlarini bilish uchun videoni ko'ring..."
    await message.answer(text, reply_to_message_id=message.message_id, parse_mode="HTML")
    await state.set_state(RegisteredUsersState.ism_s)
    # await message.answer_video(video=file_id, caption=caption, width=1920, height=1080)
    # admin_users = TelegramProfile.objects.filter(role=Role.ADMIN)
    # for admin in admin_users:
    #     try:
    #         if admin.chat_id:
    #             await bot.send_message(chat_id=admin.chat_id, text=notification, parse_mode="HTML")
    #     except:
    #         pass
    # current_date = date.today()
    # await bot.send_message(7628428313, notification, parse_mode="HTML")

# async def get_video_file_id(message: types.Message, bot: Bot):
#     await message.answer(message.video.file_id)

async def get_ism(message: types.Message, bot: Bot, state: FSMContext):
    ism = message.text
    await state.update_data(ism=ism)
    await message.answer("<b>📌Familiyangizni kiriting📝</b>", parse_mode="HTML")
    await state.set_state(RegisteredUsersState.familiya_s)

async def get_familiya(message: types.Message, state: FSMContext):
    familiya = message.text
    await state.update_data(familiya=familiya)
    await message.answer('📌<b>Ishlaydigan telefon raqamingizni kiriting📞 </b>\n\n'
                         '1️⃣. "📞 Raqamni yuborish" tugmachasini bosing\n'
                         '2️⃣. 📲Yoki o`zingiz raqamni kiriting. Misol uchun: <i>998901234567</i>', reply_markup=phone_number, parse_mode="HTML")
    await state.set_state(RegisteredUsersState.telefon_s)

# async def get_telraqam(message: types.Message, state: FSMContext):
#     if message.contact:
#         telefon = message.contact.phone_number
#         await state.update_data(telefon=telefon)
#         data = await state.get_data()
#         ism = data['ism']
#         familiya = data['familiya']
#         telefon = data['telefon']
#
#         user = RegisteredUsers.objects.filter(
#             chat_id=message.chat.id)
#
#         if not user.exists():
#             prepared_user = RegisteredUsers.objects.create(
#                 ism=ism,
#                 familiya=familiya,
#                 telefon=telefon,
#                 chat_id=message.chat.id,
#                 username=message.chat.username,
#                 first_name=message.chat.first_name,
#                 last_name=message.chat.last_name
#             )
#             text = "Siz ro'yhatdan muvaffaqiyatli o'tdingiz✅"
#             await message.answer(
#                 text,
#                 reply_to_message_id=message.message_id)
#             return prepared_user
#         text = "Siz ro'yhatdan muvaffaqiyatli o'tdingiz✅"
#         await message.answer(
#             text,
#             reply_to_message_id=message.message_id)
#         return user.first()

async def get_telraqam(
        message: types.Message,
        bot: Bot,
        state: FSMContext):
    telefon = None
    tashkent_tz = pytz.timezone(
        'Asia/Tashkent')
    current_time = datetime.now(
        tashkent_tz).strftime(
        "%H:%M:%S")

    if message.contact:  # Foydalanuvchi "📞 Raqamni yuborish" tugmachasini bosgan bo'lsa
        telefon = message.contact.phone_number
    else:  # Foydalanuvchi raqamni qo'lda yozgan bo'lsa
        if re.fullmatch(
                r"^\+?\d{9,15}$",
                message.text):  # Raqamni validatsiya qilish
            telefon = message.text
        else:
            await message.answer(
                "❌ Noto‘g‘ri telefon raqam! Iltimos, raqamni to‘g‘ri formatda kiriting yoki tugmani bosing.")
            return

    await state.update_data(
        telefon=telefon)
    data = await state.get_data()
    ism = data.get(
        'ism')
    familiya = data.get(
        'familiya')
    print("<<<<<<<<<<<")
    user = RegisteredUsers.objects.filter(
        chat_id=message.chat.id)
    current_date = date.today()
    # current_time = datetime.now().strftime(
    #     "%H:%M:%S")
    if not user.exists():
        prepared_user = RegisteredUsers.objects.create(
            ism=ism,
            familiya=familiya,
            telefon=telefon,
            chat_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name
        )
        mention = f"<a href='tg://user?id={message.chat.id}'>{prepared_user.first_name}</a>"
        notification = (f"Diqqat!!!   ID: {prepared_user.id}  \n\n"
                    f"{mention} ro'yhatdan o'tdi✅ \n\n"
                    f"Sana: {current_date}  |  {current_time}")

        await bot.send_message(
            7628428313,
            notification,
            parse_mode="HTML")
        print(notification)
        text = "<b>Siz ro'yhatdan muvaffaqiyatli o'tdingiz✅</b>"
        print(text)
        await message.answer(
            text,
            reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await state.clear()
        return prepared_user
    prepared_user, created = RegisteredUsers.objects.update_or_create(
    chat_id=message.chat.id,  # Unikal identifikator (shart bo'lishi kerak)
    defaults={
        "ism": ism,
        "familiya": familiya,
        "telefon": telefon,
        "username": message.chat.username,
        "first_name": message.chat.first_name,
        "last_name": message.chat.last_name
        }
    )
    mention = f"<a href='tg://user?id={message.chat.id}'>{prepared_user.first_name}</a>"
    notification = (f"Diqqat!!!   ID: {prepared_user.id}  \n\n"
                f"{mention} ma'lumotlarini yangiladi✅ \n\n"
                f"Sana: {current_date}  |  {current_time}")

    await bot.send_message(
        7628428313,
        notification,
        parse_mode="HTML")
    text = "<b>Sizning ma'lumotlaringiz yangilandi✅</b>"
    await message.answer(
        text,
        reply_markup=ReplyKeyboardRemove(),         parse_mode = "HTML")
    await state.clear()
    return user.first()


#/sms(for admin)
async def sms_for_admin(message: types.Message, bot: Bot, state: FSMContext):
    await message.answer("Adminga xabar yuborish uchun matnni kiriting: ")
    await state.set_state(SmsForAdmin.sms)

#/sms(for admin)
async def sms_received(message: types.Message, state: FSMContext, bot: Bot):
    if message.text.startswith("/"):
        await message.answer("Siz hozir statening ichidasiz ")
        return
    await state.update_data(sms=message.text)
    data = await state.get_data()
    user = TelegramProfile.objects.filter(chat_id=message.from_user.id).first()
    admin_users = RegisteredUsers.objects.filter(role=Role.ADMIN)

    # Adminlarga xabar yuborish
    for admin in admin_users:
        try:
            # Har bir admin foydalanuvchining chat_id sini olish va unga xabar yuborish
            if admin.chat_id:
                text = (f"ID: {user.id}\n"
                        f"Nick: <a href='tg://user?id={user.chat_id}'>{user.first_name}</a>\n"
                        f"Username: @{user.username}\n\n"
                        f"===message===\n"
                        f"{data.get('sms')}")
                # Adminga xabar yuborish
                await bot.send_message(chat_id=admin.chat_id, text=text, parse_mode="HTML")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
    await message.answer("Xabar muvaffaqiyatli yuborildi✅. Iltimos, admin javobini kuting...")
    await state.clear()

async def echo_photo(message: types.Message):
    import os
    # Rasmni olish
    file_id = message.photo[-1].file_id  # Eng katta rasmni olish
    file = await bot.get_file(file_id)

    # Faylni serverga saqlash
    file_name = os.path.join('downloads', f"{file.file_id}.jpg")
    os.makedirs('downloads', exist_ok=True)  # downloads papkasini yaratish

    await download_image(file_id, file_name)
    import pytesseract
    from PIL import Image

    # Rasmni yuklash
    image_path = f'{file_name}'
    img = Image.open(image_path)

    # Rasmni matnga o‘girish
    text = pytesseract.image_to_string(img)
    os.remove(image_path)

    #>>>>>>yuqoridagi kodlar rasmdan textni olish uchun ishlatildi⬆️

    file_id = message.photo[-1].file_id
    caption = message.caption or ""
    user = await get_user(message.chat)
    common.tasks.send_echo_photo.delay(file_id=file_id,
                                       caption=caption,
                                       chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       user_id=user.id,
                                       first_name=message.from_user.first_name,
                                       username=message.from_user.username,
                                       text_of_img=text
                                       )

async def download_image(file_id: str, file_name: str):
    file = await bot.get_file(file_id)
    file_path = file.file_path

    url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_name, 'wb') as f:
                f.write(await response.read())
    # print(f"Image saved as {file_name}")



async def echo_video(message: types.Message):
    file_id = message.video.file_id
    caption = message.caption or ""
    user = await get_user(message.chat)
    common.tasks.send_echo_video.delay(file_id=file_id,
                                       caption=caption,
                                       chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       user_id=user.id,
                                       first_name=message.from_user.first_name,
                                       username=message.from_user.username
                                       )



async def echo(message: types.Message):
    user = await get_user(message.chat)
    common.tasks.send_echo_celery.delay(
        chat_id=message.chat.id,
        message_text=message.text,
        user_id=user.id,
        first_name=user.first_name,
        username=user.username,
        message_id=message.message_id
    )


async def sms_for_banned_user(message: types.Message, state: FSMContext, bot: Bot):
    telegram_id = message.from_user.id
    text = message.text[7:].strip()  # "/sms " qismidan keyingi matnni olish

    # Foydalanuvchi ban qilinganmi?
    profile = TelegramProfile.objects.filter(chat_id=telegram_id).first()
    if not profile:
        await message.answer("Sizning profilingiz topilmadi.")
        return


    # Xabarni adminlarga yuborish
    if text:
        user = TelegramProfile.objects.filter(chat_id=telegram_id).first()
        admin_users = TelegramProfile.objects.filter(role__in=[Role.ADMIN, Role.MODERATOR])

        # Adminlarga xabar yuborish
        for admin in admin_users:
            try:
                if admin.chat_id:
                    text_to_send = (
                        "🤕 Ban userdan keldi 🤕\n\n"
                        f"ID: {user.id}\n"
                        f"Nick: {user.first_name}\n"
                        f"Username: @{user.username}\n\n"
                        f"===message===\n"
                        f"{text}"
                    )
                    await bot.send_message(chat_id=admin.chat_id, text=text_to_send)
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
        await message.answer("Xabar muvaffaqiyatli yuborildi✅. Iltimos, admin javobini kuting...")
    else:
        await message.answer("Unday emas! <b><i>/xabar [text kiriting]</i></b>.", parse_mode="HTML")

    # State ni tozalash
    await state.clear()


async def confirm_callback(callback: types.CallbackQuery):
    kanallar = await get_channels()
    azo_bolmaganlar = []
    for kanal in kanallar:
        try:
            member = await bot.get_chat_member(chat_id=kanal.chat_id, user_id=callback.from_user.id)
            if member.status == "left" or member.status == "kicked":
                azo_bolmaganlar.append(kanal.title)
        except Exception as e:
            print(e)
    if azo_bolmaganlar:
        await callback.message.answer(
            "Siz barcha kanallarga a'zo bo'lmagansiz!❌"
        )
        await callback.answer()
        return
    else:
        await callback.message.answer("Siz barcha kanallarga a'zo bo'ldingiz✅")
        await start(callback.message, bot)
    await callback.answer()



