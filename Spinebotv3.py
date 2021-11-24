#256064
import discord
from discord import channel
from discord import client

from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

from discord.ext import commands



bot = commands.Bot(command_prefix="s!", help_command=None)

@bot.event
async def on_ready():
    print("logged in as {bot.user}")

@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Spinebot Commands", description="คำสั่งทั้งหมด", color=0x5a49e3)
    emBed.add_field(name="s!help", value="📋║คำสั่งที่สามารถใช้ได้", inline=False)
    emBed.add_field(name="s!hello", value="👋🏻║ทักทาย", inline=False)
    emBed.add_field(name="s!play", value="🧿║เล่นเพลง s!play + url/name", inline=False)
    emBed.add_field(name="s!pause", value="🔈║หยุดเพลงที่เล่น", inline=False)
    emBed.add_field(name="s!resume", value="🔊║เล่นเพลงต่อจากเดิม", inline=False)
    emBed.add_field(name="s!stop", value="🔇║หยุดเพลง", inline=False)
    emBed.add_field(name="s!leave", value="👣║ออกจากห้อง", inline=False)
    emBed.set_thumbnail(url="https://cdn.discordapp.com/attachments/861386789952290826/902391108112363581/Spine-logos.jpeg")
    emBed.set_footer(text="SpineBot", icon_url="https://cdn.discordapp.com/attachments/861386789952290826/902391108112363581/Spine-logos.jpeg")
    await ctx.channel.send(embed=emBed)

@bot.event
async def on_message(message):
    if message.content == "s!hello":
        print(message.channel)
        await message.channel.send("สวัสดี " + str(message.author.name))
    elif message.content == "s!logout":
        await message.channel.send("ลาก่อน")
        await bot.logout()
    await bot.process_commands(message)

@bot.command()
async def play(ctx, *, url):
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':"bestaudio", 'default_search':"ytsearch"}
    vc = ctx.voice_client

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            url2 = info["entries"][0]["formats"][0]['url']
        elif 'formats' in info:
            url2 = info["formats"][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)

@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("บอทไม่ได้เชื่อมต่อในขณะนี้")
        return

    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("บอทกำลังเชื่อมต่อที่ห้อง %s " %voice_client.channel)
        return

    voice_client.stop()

@bot.command()
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("Bot is not connected to vc")
        return

    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("บอทกำลังเชื่อมต่อที่ห้อง %s " %voice_client.channel)
        return

    voice_client.pause()

@bot.command()
async def resume(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("Bot is not connected to vc")
        return

    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("บอทกำลังเชื่อมต่อที่ห้อง %s " %voice_client.channel)
        return

    voice_client.resume()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run('')