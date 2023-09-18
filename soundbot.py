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
#intents.message_content = True
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
    pass

@bot.command(name='hello')
async def hello_test(ctx):
    await ctx.send("Hello!")

@bot.event
async def on_message(message):
    print(message.author, ": ", message)




# Activate bot
bot.run(TOKEN)