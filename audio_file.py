class AudioFile():
    name = None
    path = None
    emoji = None

    def __init__(self, shortcut_name, file_path, reaction_emoji):
        self.name = shortcut_name
        self.path = file_path
        self.emoji = reaction_emoji