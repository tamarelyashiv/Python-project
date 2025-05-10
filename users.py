
class Users:
    def __init__(self, username, password, id_number):
        self.username = username
        self.id_number = id_number
        self.password = password
        self.words_used = []
        self.games_played = 0
        self.wins = 0

    def add_game(self):
        self.games_played += 1

    def add_word(self, word):
        self.words_used.add(word)
        print(word)

    def add_win(self):
        self.wins += 1

    def to_dict(self):
        return {
            "username": self.username,
            "id_number": self.id_number,
            "password": self.password,
            "games_played": self.games_played,
            "words_used": list(self.words_used),
            "wins": self.wins
        }
