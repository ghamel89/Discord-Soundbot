# Discord-Soundbot

## Discord bot to control playing music and sound effects in voice channels


## <b>   Features </b>
 Usage: '! [command]' to bring into voice channel and to remove
 Commands to grab audio from youtube videos -> need feature to trim audio
 Call to list all saved clips and use reactions on that post to use functions

 ### <b> Current Commands </b>
 - <i> !summon </i> : Will summon SoundBot into current channel
 - <i> !banish </i> : Will disconnect Soundbot from current channel (user must be in same channel to work properly)
 - <i> !play [video_link]</i> : Downloads and begins playback of youtube video link
 - <i> !nowplay [shortcut_name] </i> : Plays the selected clip, if one matching the shortcut exists
 - <i> !pause </i> : Pauses audio playback
 - <i> !resume </i> : Resumes paused playback
 - <i> !stop </i> : Halts and closes out of audio playback
 - <i> !save [video_link], [shortcut_name], [start_time] (optional), [end_time] (optional) </i> : Saves a new object in the 'saved_sounds.json' file to be pulled later
 - <i> !delete [shortcut_name] </i> : Deletes a saved clip
 - <i> !list </i> : Read all saved objects and privately message them to sender

## <b>   Stretch Goals </b>
 - If possible, use reactions to control 'play' 'pause' 'stop' and volume adjustments
 - See if possible to have a command to drop it into a voice channel without being present, for trolling / spamming
 - Switch whole bot to using newer 'interactions' library, or implementing the library in general

