import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime
import yt_dlp
from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func
import json

# Discord bot to control playing music and sound effects in voice channels


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
    #     info = ydl.extract_info(video_link, download=False)

    # await ctx.send(info.get("title", None))

    try: 
        vc = ctx.message.guild.voice_client
        if vc and vc.channel == ctx.message.author.voice.channel:
            #await ctx.send("Inside Playing")
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=TEMP_PLAY_PATH))
            #await ctx.send(info)
        else:
            await ctx.send("Nope")
    except:
        await ctx.send("Here I go Fucking Up again")


# Play a saved sound via shortcut
@bot.command()
async def nowplay(ctx, shortcut):

    do_i_have_it = None
    with open('saved_sounds.json', 'r') as openfile:
        saves = json.load(openfile)

    for object in saves:
        if object['shortcut'] == shortcut:
            do_i_have_it = object['filepath']

    if do_i_have_it:
        try:
            vc = ctx.message.guild.voice_client
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=do_i_have_it))
        except:
            await ctx.send("If you're seeing this, I'm probably not in a voice channel, try !summon")
    else:
        await ctx.send("No shortcut with the name {}".format(shortcut))


# Privately send a list of all sounds saved
@bot.command()
async def list(ctx):
    user = ctx.message.author

    with open('saved_sounds.json', 'r') as openfile:
        saved = json.load(openfile)

    await user.send("Here are all the saved clips:")

    for item in saved:
        await user.send("{} \t-\t Plays - \t {}".format(item['shortcut'], item['title']))

    await user.send("\n This has been all of the saved clips")


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
async def save(ctx, video_link, shortcut_name, start_time=None, end_time=None):
    # Grab existing file
    try:
        with open("saved_sounds.json", "r") as infile:
            sound_objects : list = json.load(infile)
    except:
        await ctx.send("saved_sounds.json is blank I think")

    for item in sound_objects:
        if item['shortcut'] == shortcut_name:
            await ctx.send("Clip with that name exists already")
            return
        
    output = "/audio_samples/" + shortcut_name
    if start_time and end_time:
        start_time = convert_time(start_time)
        end_time = convert_time(end_time)
        ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': output,
        'download_ranges': download_range_func(None, [(start_time, end_time)]),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }]
        }
    else:
        ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }]
        }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])
        info = ydl.extract_info(video_link, download=False)

    title = info.get("title")

    #sound_objects = []
    filepath = AUDIO_PATH + shortcut_name + ".mp3"
    test_obj = {
        "title" : title,
        "shortcut" : shortcut_name,
        "filepath" : filepath
    }
    
    
    sound_objects.append(test_obj)

    with open("saved_sounds.json", "w") as outfile:
        json.dump(sound_objects, outfile, indent=4, separators=(',',': '))

    await ctx.send("Successfully saved {}".format(shortcut_name))


# Remove a saved sound
@bot.command()
async def delete(ctx, shortcut_name):
    # Grab existing file
    try:
        with open("saved_sounds.json", "r") as infile:
            sound_objects : list = json.load(infile)
    except:
        await ctx.send("saved_sounds.json is blank, I think")

    for item in sound_objects:
        if item['shortcut'] == shortcut_name:
    
            filepath = item['filepath']
            try:
                os.remove(filepath)
                sound_objects.remove(item)
                with open("saved_sounds.json", "w") as outfile:
                    json.dump(sound_objects, outfile, indent=4, separators=(',',': '))
                await ctx.send("Successfully removed {}".format(item['shortcut']))
                return
            except Exception as e:
                print(e)
                await ctx.send("Something went wrong, I couldn't find that file")

    await ctx.send("Couldn't find a saved clip with that name, try !list to see a list of currently saved clips.")


# Test Command to send a user a private message
@bot.command()
async def pmtest(ctx):
    sender = ctx.message.author

    await sender.send("Secret")


def convert_time(time):
    
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":"))))

# Activate bot
bot.run(TOKEN)