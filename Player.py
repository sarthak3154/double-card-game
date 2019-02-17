class Player:
    def __init__(self, play_choice,name):
        self.play_choice = play_choice
        self.name = name

    def get_play_choice(self):
        return self.play_choice

    def get_player_name(self):
        return self.name
