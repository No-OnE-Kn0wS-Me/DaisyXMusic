import os
from datetime import datetime
from DaisyXMusic.config import STREAM_URL, CHAT
import ffmpeg
from pyrogram import emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from pytgcalls import GroupCall
import signal
from user import USER
GROUP_CALLS = {}
FFMPEG_PROCESSES = {}
RADIO={6}
class MusicPlayer(object):
    def __init__(self):
        self.group_call = GroupCall(USER, path_to_log_file='')
        self.chat_id = None
        self.msg = {}


    async def start_radio(self):
        if 1 in RADIO:
            return
        group_call = mp.group_call
        if group_call:
            group_call.stop_playout()
            mp.playlist.clear()
        group_call.input_filename = f'radio-{CHAT}.raw'
        process = FFMPEG_PROCESSES.get(CHAT)
        if process:
            process.send_signal(signal.SIGTERM)
        station_stream_url = STREAM_URL
        
        if group_call.is_connected:
            return
        await group_call.start(CHAT)
        try:
            RADIO.remove(0)
        except:
            pass
        try:
            RADIO.add(1)
        except:
            pass
        process = ffmpeg.input(station_stream_url).output(
            group_call.input_filename,
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k'
        ).overwrite_output().run_async()
        FFMPEG_PROCESSES[CHAT] = process


    
    async def stop_radio(self):
        if 0 in RADIO:
            return
        group_call = mp.group_call
        if group_call:
            await group_call.stop()
            try:
                RADIO.remove(1)
            except:
                pass
            try:
                RADIO.add(0)
            except:
                pass
        process = FFMPEG_PROCESSES.get(CHAT)
        if process:
            process.send_signal(signal.SIGTERM)

    async def start_call(self):
        group_call = mp.group_call
        await group_call.start(CHAT)
        
    async def startupradio(self):
        group_call = mp.group_call
        if group_call:
            group_call.stop_playout()
            mp.playlist.clear()
        group_call.input_filename = f'radio-{CHAT}.raw'
        process = FFMPEG_PROCESSES.get(CHAT)
        if process:
            process.send_signal(signal.SIGTERM)
        station_stream_url = STREAM_URL
        await group_call.start(CHAT)
        try:
            RADIO.add(1)
        except:
            pass
        process = ffmpeg.input(station_stream_url).output(
            group_call.input_filename,
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k'
        ).overwrite_output().run_async()
        FFMPEG_PROCESSES[CHAT] = process


mp = MusicPlayer()


# pytgcalls handlers

@mp.group_call.on_network_status_changed
async def network_status_changed_handler(gc: GroupCall, is_connected: bool):
    if is_connected:
        mp.chat_id = int("-100" + str(gc.full_chat.id))
    else:
        mp.chat_id = None

