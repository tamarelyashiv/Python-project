import random
from flask import Flask, jsonify, request, make_response, redirect, url_for
import json
from flask_cors import CORS, cross_origin
from functools import wraps

app = Flask(__name__)
CORS(app, supports_credentials=True)


def check_cookie(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_name')
        if user_id:
            return func(*args, **kwargs)
        else:
            print("העוגיה פגה עליך להתחבר שוב בשביל להמשיך לשחק")
            return redirect(url_for('login'))

    return wrapper


def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
        # שגיאות
    except FileNotFoundError:
        return []


# שומר את הנתונים בקובץ
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)


# אני רציתי לראות הדפסה בשבילי
def print_users_to_console():
    users = load_users()
    print(users)


users = load_users()


@app.route('/register', methods=["POST"])
@cross_origin(supports_credentials=True)
def register():
    req = request.json
    if users:
        for user in users:
            if user['Password'] == req['password']:
                return jsonify("הסיסמה כבר בשימוש"), 400
            if user['IdNumber'] == req.get('id_number'):
                return jsonify("מספר המזהה כבר בשימוש"), 400
    Users = {
        'username': req['username'],
        'Password': req['password'],
        'IdNumber': req.get('id_number'),
        'wins': 0,
        'games_played ': 0,
        'words_used': []
    }
    users.append(Users)
    save_users(users)
    response = make_response(jsonify(f"שלום {req['username'], req['id_number']}מספר מזהה"))
    response.set_cookie('user_name', req['username'], max_age=600, httponly=True, secure=False)
    return response, 200


@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    req = request.json
    if 'username' not in req or 'password' not in req:
        return jsonify("חסר שם משתמש או סיסמה"), 400
    for user in users:
        if user['username'] == req['username'] and user['Password'] == req['password']:
            response = make_response(jsonify(f"שלום {req['username']}"))
            response.set_cookie('user_name', req['username'], max_age=600, httponly=True, secure=False)
            return response
    return jsonify("המשתמש לא נמצא, עליך להרשם"), 401


# שמירת המילים של המשחק:
def saveWords(words_list):
    with open("t.txt", "w") as file:
        for word in words_list:
            file.write(word + "\n")


def loadWords():
    with open("t.txt", "r") as file:
        return [line.strip() for line in file.readlines()]


words_list = ["מצוין", "יפה", "מה נשמע"]
saveWords(words_list)


@app.route('/getWords', methods=["GET"])
def getWord():
    index = int(request.args.get('index', 0))
    words_list = loadWords()
    circular_index = index % len(words_list)

    return words_list[circular_index], 200


@app.route('/print_users', methods=["GET"])
def print_users():
    users = load_users()
    return jsonify(users), 200


@app.route('/check_cookie', methods=["GET"])
def check_cookie():
    username = request.cookies.get('user_name')
    if username:
        return jsonify({"active": True}), 200
    else:
        return jsonify({"active": False}), 200


@app.route('/updateWin', methods=["POST"])
@cross_origin(supports_credentials=True)
def update_win():
    username = request.cookies.get('user_name')
    if not username:
        return jsonify("לא מחובר"), 401
    for user in users:
        if user['username'] == username:
            if 'wins' not in user:
                user['wins'] = 0
            user['wins'] += 1
            save_users(users)
            return jsonify(f"{username} ניצחת!"), 200
    return jsonify("המשתמש לא נמצא"), 404


@app.route('/addPlay', methods=["POST"])
@cross_origin(supports_credentials=True)
def play():
    username = request.cookies.get('user_name')
    if not username:
        return jsonify("לא מחובר"), 401
    for user in users:
        if user['username'] == username:
            if 'games_played' not in user:
                user['games_played'] = 0
            user['games_played'] += 1
            save_users(users)
            return jsonify(f" הוספת המשחק"), 200
    return jsonify("המשתמש לא נמצא"), 404


@app.route('/updateUsedWord', methods=["POST"])
@cross_origin(supports_credentials=True)
def update_used_word():
    username = request.cookies.get('user_name')
    if not username:
        return jsonify("לא מחובר"), 401
    req = request.json
    word = req.get('word')
    for user in users:
        if user['username'] == username:
            if 'words_used' not in user:
                user['words_used'] = []
                # אם עדיין אין כזאת מילה אצל המשתמש
            if word not in user['words_used']:
                user['words_used'].append(word)
            print(word)
            save_users(users)
            return jsonify(f"{username} הוסיף את המילה: {word}"), 200
    return jsonify("המשתמש לא נמצא"), 404


@app.route('/getHistory', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_history():
    username = request.cookies.get('user_name')
    if not username:
        return jsonify({"error": "לא מחובר"}), 401
    history = get_user_history(username)
    if history is None:
        return jsonify({"error": "No history found"}), 404

    return jsonify(history), 200


def get_user_history(user_name):
    users = load_users()
    for user in users:
        if user.get('username') == user_name:
            return {
                'username': user['username'],
                'wins': user.get('wins', 0),
                'games_played': user.get('games_played', 0),
                'words_used': list(user.get('words_used', []))
            }


if __name__ == '__main__':
    print_users_to_console()
    app.run(debug=True)
