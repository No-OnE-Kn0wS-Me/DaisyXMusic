from pyrogram import Client, filters
from pyrogram.types import Message
from vc import mp, RADIO
from DaisyXMusic.config import ADMINS, STREAM_URL

@Client.on_message(filters.command("radio") & filters.user(ADMINS))
async def radio(client, message: Message):
    if 1 in RADIO:
        await message.reply_text("Kindly stop existing Radio Stream /stopradio")
        return
    await mp.start_radio()
    await message.reply_text(f"Started Radio: <code>{STREAM_URL}</code>")

@Client.on_message(filters.command('stopradio') & filters.user(ADMINS))
async def stop(_, message: Message):
    if 0 in RADIO:
        await message.reply_text("Kindly start Radio First /radio")
        return
    await mp.stop_radio()
    await message.reply_text("Radio stream ended.")
