# Discord-Soundbot

## Discord bot to control playing music and sound effects in voice channels


                  <b>   Features </b>
 Usage: '! [command]' to bring into voice channel and to remove
 Commands to grab audio from youtube videos -> need feature to trim audio
 Call to list all saved clips and use reactions on that post to use functions

 # <b> Current Commands </b>
 - <i> !summon </i> : Will summon SoundBot into current channel
 - <i> !banish </i> : Will disconnect Soundbot from current channel (user must be in same channel to work properly)
 - <i> !play </i> : Plays test sound if bot is in server
 - <i> !save [video_link], [start_time], [end_time], [shortcut_name] </i> : Saves a new object in the 'saved_sounds.json' file to be pulled later
 - <i> !load </i> : Read all saved objects and print them in channel

                  <b>   Stretch Goals </b>
 If possible, use reactions to control 'play' 'pause' 'stop' and volume adjustments
 See if possible to have a command to drop it into a voice channel without being present, for trolling / spamming

Excuse my blatent tutorial code figuring out the start of this