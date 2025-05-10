from users import Users
from requests import Session
import random

logo = r"""      	    _    _
           | |  | |
           | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
           |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
           | |  | | (_| | | | | (_| | | | | | | (_| | | | |
           |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                __/ |
                               |___/
"""
print(logo)
session = Session()
basic_url = " http://127.0.0.1:5000"


def register():
    username = input('הכנס שם: ')
    while True:
        password = input('הכנס סיסמא: ')
        if len(password) > 3 and len(password) < 2:
            print("הסיסמא לא תכיל יותר מ-3 תווים. נסה שוב.")
            continue
        break

    id_number = random.randint(100, 999)

    message = Users(username, password, id_number)
    response = session.post(f"{basic_url}/register", json=message.to_dict())

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


def login():
    username = input("הכנס שם:")
    password = input("הכנס סיסמא:")
    response = session.post(f"{basic_url}/login",
                            json={"username": username, "password": password})
    if response.status_code == 200:
        print(response.json())
    else:
        print("אינך מחובר,עליך להרשם")
        register()

        # print(f"Error: {response.status_code}")
def play():
    login()
    # משחק כל עוד הוא מחובר
    while True:
        number = int(input("הכנס מספר: "))
        response = session.get(f"{basic_url}/getWords?number={number}")
        if response.status_code == 200:
            word = response.text.strip()
            # שומר את האותיות שנחשו
            list_guess = []
            # מספר הנסויים
            count = 7
            # שם קו תחתי במקום האות ואיפה שיש רווח שם רווח
            lenWord = ['_' if letter != ' ' else ' ' for letter in word]
            user_response = session.post(f"{basic_url}/updateUsedWord", json={"word": word})
            if user_response.status_code != 200:
                print("שגיאה ", user_response.status_code)
                return
            with open('איש תלוי.txt', 'r') as file:
                read = file.read()
                # שלבים
                stages = [part.strip() for part in read.split('\n\n') if part.strip()]
            # while כל עוד יש לו נסיונות או שעדיין לא סיים את המילה
            while count > 0 and '_' in lenWord:
                check_cookie = session.get(f"{basic_url}/check_cookie")
                if check_cookie.status_code != 200 or not check_cookie.json().get("active"):
                    print("עליך להתחבר מחדש כדי לשחק.")
                    while True:
                        login1 = input("האם אתה רוצה להתחבר מחדש? (כן/לא): ").strip()
                        if login1 == 'כן':
                            login()
                            if response.status_code == 200:
                                word = response.text.strip()
                                break  # חוזר להתחלת הלולאה
                            else:
                                print("שגיאה", response.status_code)
                                return
                        elif login1 == 'לא':
                            return
                        else:
                            print("תשובה לא תקפה, יש להקליד 'כן' או 'לא'.")
                            continue
                print("המילה: " + ' '.join(lenWord))
                print(f"כמות הנסויים שנותרו: {count}")
                guess = input("נחשי את המילה: ").strip()
                # יש להכניס אות אחת ורק אות ולא תו אחר
                if len(guess) != 1 or not guess.isalpha():
                    print("הבחירה לא תקפה. אנא הכנס אות אחת בלבד.")
                    continue

                if guess in list_guess:
                    print("כבר ניחשת את האות הזו.")
                    continue

                list_guess.append(guess)

                if guess in word:
                    print('מצוין')
                    lenWord = [guess if letter == guess else lenWord[i] for i, letter in enumerate(word)]
                else:
                    count -= 1
                    if count > 0 and count <= 7:
                        print(stages[7 - count])

            if count == 0:
                print('הפסדת במשחק זה')
                res = session.post(f"{basic_url}/addPlay")
                if res.status_code == 200:
                    print(res.json())
                else:
                    print("לא הצלחנו להוסיף משחק זה:", res.status_code, res.text)
            else:
                print('ניחשת את המילה: ' + ''.join(lenWord))
                response = session.post(f"{basic_url}/updateWin")
                res = session.post(f"{basic_url}/addPlay")
                if response.status_code == 200:
                    print(response.json())
                if res.status_code == 200:
                    print(res.json())
            while True:
                choice = input("מה אתה רוצה לעשות? (1 - לשחק שוב, 2 - לראות היסטוריה, 3 - להתנתק): ")

                if choice == '1':
                    check_cookie = session.get(f"{basic_url}/check_cookie")
                    if check_cookie.status_code == 200 and check_cookie.json().get("active"):
                        break
                    else:
                        print("עליך להתחבר מחדש כדי לשחק.")
                        login()

                elif choice == '2':
                    check_cookie = session.get(f"{basic_url}/check_cookie")
                    if check_cookie.status_code == 200 and check_cookie.json().get("active"):
                        username = check_cookie.json().get("username")
                        history_response = session.get(f"{basic_url}/getHistory?user_name={username}")
                        if history_response.status_code == 200:
                            history = history_response.json()
                            print("היסטוריית המשחקים שלך:", history)
                        else:
                            print("איננו יכולים להציג את ההיסטוריה", history_response.status_code)
                    else:
                        print("עליך להתחבר מחדש כדי לראות את ההיסטוריה.")
                        login()

                elif choice == '3':
                    print("מתנתק...")
                    return

                else:
                    print("בחירה לא תקפה, נסה שוב.")
        else:
            print("Error fetching words", response.status_code)


def main():
    play()


if __name__ == "__main__":
    main()
