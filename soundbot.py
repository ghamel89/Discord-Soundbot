import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

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
        await channel.connect()

@bot.command()
async def banish(ctx):
    vc = ctx.message.guild.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("SoundBot is not connected to a voice channel")

    #ctx.voice_client.play(discord.FFmpegPCMAudio("/audio_samples/Windows_Shutdown.mp3"))

# Activate bot
bot.run(TOKEN)