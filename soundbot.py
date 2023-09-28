import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import yt_dlp
from yt_dlp import YoutubeDL
import json

# Discord bot to control playing music and sound effects in voice channels


                    ### Features ###
# Usage: '! [command]' to bring into voice channel and to remove
# Commands to grab audio from youtube videos -> need feature to trim audio
# Call to list all saved clips and use reactions on that post to use functions

                    ### Stretch Goals ###
# If possible, use reactions to control 'play' 'pause' 'stop' and volume adjustments
# See if possible to have a command to drop it into a voice channel without being present, for trolling / spamming

### Excuse my blatent tutorial code figuring out the start of this


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"
AUDIO_PATH = "E:/Users/ghame/Desktop/Code/audio_samples/"
TEMP_PLAY_PATH = "E:/Users/ghame/Desktop/Code/audio_samples/play.mp3"
intents = discord.Intents.default()
intents.message_content = True
# Necessary else keyword error
#bot = commands.Bot(command_prefix='!', intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)



# Ready function, runs when bot is activated
# Possibly put soundboard loader in here
@bot.event
async def on_ready():
    print(f"SoundBot is now Active")
    pass


# Basic command, will direct user to github repo where if they know how to read
#   they might find the commands
@bot.command()
async def helpme(ctx):
    await ctx.send("Scroll down for the README")
    await ctx.send("https://github.com/ghamel89/Discord-Soundbot")


# Command will play a test sound if bot and message sender are in same channel
@bot.command()
async def test(ctx):
    vc = ctx.message.guild.voice_client
    if vc != None:
        play_this = AUDIO_PATH + "Windows_Shutdown.mp3"
        vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=play_this))

    else:
        await ctx.send("{} is not in a voice channel".format(ctx.author.name))


# Summons bot to channel message sender is currently in
@bot.command()
async def summon(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    elif ctx.message.guild.voice_client:
        # SoundBot is already in a voice channel, this should pop
        vc = ctx.message.guild.voice_client
        await ctx.send("SoundBot is currently in {}".format(vc.channel))

        for entry in ctx.message.author.roles:
            await ctx.send("{} is a {}".format(ctx.message.author.name, entry))
        admin = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)

        if admin in ctx.message.author.roles:
            await full_banish(ctx)
            await summon(ctx)
        else:
            await ctx.send("{} is not important enough to move SoundBot, scrub".format(ctx.message.author.name))
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        await ctx.send("SoundBot is now in {}".format(vc.channel))


async def full_banish(ctx):
    vc = ctx.message.guild.voice_client
    await vc.disconnect()


# Removes bot from voice channel
@bot.command()
async def banish(ctx):
    vc = ctx.message.guild.voice_client
    
    try:
        if vc and vc.channel == ctx.message.author.voice.channel:
            # vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="E:/Users/ghame/Desktop/Code/audio_samples/Windows_Shutdown.mp3"))
            await vc.disconnect()
        elif vc:
            await ctx.send("Must be in the same channel as SoundBot, I can't hear you from that far away")
        else:
            await ctx.send("SoundBot is not connected to a voice channel")
    except:
        await ctx.send("Something went wrong, try being in the same channel")


# Will play from youtube link
@bot.command()
async def play(ctx, video_link):
    ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': '/audio_samples/play',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    try: 
        vc = ctx.message.guild.voice_client
        if vc and vc.channel == ctx.message.author.voice.channel:
            #await ctx.send("Inside Playing")
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=TEMP_PLAY_PATH))
        else:
            await ctx.send("Nope")
    except:
        await ctx.send("Here I go Fucking Up again")


# Testing command to play last downloaded temp file
@bot.command()
async def justplay(ctx):
    vc = ctx.message.guild.voice_client
    vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=TEMP_PLAY_PATH))


#Pauses currently playing audio
@bot.command()
async def pause(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_playing():
        vc.pause()
    elif vc.is_paused():
        await ctx.send("Try 'Resume'?")
    else:
        await ctx.send("Nothing to pause")


# Resumes currently playing audio
@bot.command()
async def resume(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_paused():
        vc.resume()
    elif vc.is_playing():
        await ctx.send("Turn your volume up, it's already playing")
    else:
        await ctx.send("Nothing to play, so sad")


# Stops currently playing audio
@bot.command()
async def stop(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_playing() or vc.is_paused():
        vc.stop()
        await ctx.send("Stopping now")
    else:
        await ctx.send("Nothing playing or paused")


@bot.command()
async def save(ctx, video_link, start_time, end_time, shortcut_name):
    sound_objects = []
    filepath = "audio_samples/" + shortcut_name + ".mp3"
    test_obj = {
        "link" : video_link,
        "start" : start_time,
        "end" : end_time,
        "shortcut" : shortcut_name,
        "filepath" : filepath
    }
    # Grab existing file
    try:
        with open("saved_sounds.json", "r") as infile:
            sound_objects : list = json.load(infile)
    except:
        await ctx.send("saved_sounds.json is blank I think")
    #dump_me = json.dumps(test_obj)
    await ctx.send("Printing json test object")
    await ctx.send(test_obj)

    sound_objects.append(test_obj)

    with open("saved_sounds.json", "w") as outfile:
        json.dump(sound_objects, outfile, indent=4, separators=(',',': '))


@bot.command()
async def load(ctx):
    with open('saved_sounds.json', 'r') as openfile:
        saves = json.load(openfile)

    await ctx.send("Reading test object from json file")
    for object in saves:
        await ctx.send(object['shortcut'])


@bot.command()
async def pmtest(ctx):
    sender = ctx.message.author

    await sender.send("Secret")



# Activate bot
bot.run(TOKEN)