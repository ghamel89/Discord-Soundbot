import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import youtube_dl
import json
from audio_file import AudioFile

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
intents = discord.Intents.default()
intents.message_content = True
# Necessary else keyword error
bot = commands.Bot(command_prefix='!', intents=intents)
vc = None


# Ready function, runs when bot is activated
# Possibly put soundboard loader in here
@bot.event
async def on_ready():
    print(f"SoundBot is now Active")
    pass

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    print(f"Can read test message")

@bot.command()
async def summon(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        await ctx.send("Working with a {} now".format(vc.channel))

@bot.command()
async def banish(ctx):
    vc = ctx.message.guild.voice_client
    if vc:
        # vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="E:/Users/ghame/Desktop/Code/audio_samples/Windows_Shutdown.mp3"))
        await vc.disconnect()
    else:
        await ctx.send("SoundBot is not connected to a voice channel")

@bot.command()
async def give_me_info(ctx):
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if vc is None:
        await ctx.send("SoundBot is not in a voice channel")
    else:
        await ctx.send("SoundBot is in {}".format(vc.channel))


@bot.command()
async def play(ctx):
    vc = ctx.message.guild.voice_client
    if vc != None:
        
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="E:/Users/ghame/Desktop/Code/audio_samples/Windows_Shutdown.mp3"))

    else:
        await ctx.send("{} is not in a voice channel".format(ctx.author.name))

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
    await ctx.send(saves)


# Activate bot
bot.run(TOKEN)