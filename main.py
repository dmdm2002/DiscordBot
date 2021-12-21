"# -*- coding:utf-8 -*-"
import urllib.request
from bs4 import BeautifulSoup
import discord, asyncio, os
from discord.ext import commands
from GetMusic_Item import get_item
import youtube_dl

token = ''
# client = discord.Client()
game = discord.Game("Primary Bot")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)

baseURL = 'https://www.youtube.com/results?search_query='
url_list = []


async def song_start(voice, url):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # 파일로 다운로드 하지 않고 재생
        URL = info['formats'][0]['url']

    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


@bot.command()
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention}님 안녕하세요')


@bot.command()
async def play(ctx, *, txt):
    name_df, urls = get_item(txt)
    channel = ctx.author.voice.channel

    if bot.voice_clients == []:
        await channel.connect()
        # await ctx.send("connected to the voice channel, " + str(bot.voice_clients[0].channel))
    voice = bot.voice_clients[0]

    await song_start(voice, urls[0])


@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("already paused")


@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("already playing")


@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()

    else:
        await ctx.send("not playing")

bot.run(token)
