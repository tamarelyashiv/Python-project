# Hanigman Game
At the beginning of the game, the user must log in or register if not logged in.
The game is activated by a cookie that has expired, then the user must log in again, and when logging in again, he has the option to see his history, play another game, or exit.
The game is played by randomly drawing a word from the server, and the player must guess one letter each turn. He has a choice of 7 attempts.
The following history is saved for each player:
*Number of games played.
*Number of wins.
*List of words guessed.
## Technologies Used

- Python
- Flask
- requests
- JSON

## Usage:
Run the server:
python server.py
Run the client:
python client.py

## API Endpoints:
POST /register: Register a new user.
POST /login: Log in an existing user.
GET /getWords: Retrieve words for the game.
GET /check_cookie: Check if the user is logged in.
POST /updateWin: Update the user's win count.