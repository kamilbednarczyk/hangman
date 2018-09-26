import random
import time
from os import system
import os.path as path

def read_file(f_name):
    try:
        path_to_script = path.dirname(path.abspath(__file__))
        new_path = path.join(path_to_script, f_name)
        with open(new_path, 'r', encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Cannot Find a file - {f.name}")
        return None


def get_cities_from_file():
    cities = read_file("countries_and_capitals.txt")
    if cities == None:
        cities = ["Warsaw | Poland", "Berlin | Germany", "London | England"]
    return cities


def chooseCity():
    cities = get_cities_from_file()
    record = random.choice(cities)
    country, capital = record.split("|")
    capital, country = capital.strip().upper(), country.strip()
    return (capital, country)


def tip(lives, country):
    if lives == 1:
        print(f"Psst, It's the capital city of {country}.")


def print_word_status(word):
    print("Capital: ", end="")
    for place in word:
        print(f"{place}", end=" ")
    print()


def print_wrong_letters(not_in_word):
    print("Wrong letter used: ", end="")
    for letter in not_in_word:
        print(letter, ",", sep="", end=" ")
    print()


def read_hangman_art():
    hangman_list = read_file("ascii_hangman.txt")
    if hangman_list == None:
        hangman_list = ""
    hangman_list = [elem[:-1] for elem in hangman_list]
    return hangman_list


def print_hangman(lives):
    art = read_hangman_art()
    if art:
        print(art[0])
        for i in range(1, len(art)):
            print(art[i][:11], end="")
            if lives < 5:
                print(art[i][11:])
                lives += 1
            else:
                print()


def play_again():
    while True:
        try:
            again = input("Do you want to play again? (Enter yes or no): ")
            if again.lower() == "no":
                return False
            elif again.lower() == "yes":
                return True
            raise ValueError
        except ValueError:
            print("**** You can enter 'yes' or 'no' only. ****")

def blankSpots(capital):
    b_spots = []
    for letter in capital:
        if letter == ' ':
            b_spots.append(' ')
        else:
            b_spots.append('_')
    return b_spots


def getUserInput():
    while True:
        try:
            decision = input("Enter 'w' if you want to enter a whole word." +
                            "Enter 'l' if you want to enter one letter: ")
            decision = decision.upper()
            if decision == 'W' or decision == 'L':
                return decision
            raise ValueError
        except ValueError:
            print("**** You can enter 'w' or 'l' only. ****")


def checkWord(capital, guessed_letters):
    user_capital = input('Enter name of the capital: ')
    if user_capital.upper() == capital:
        underscore_count = guessed_letters.count('_')
        guessed_letters[:] = list(capital)
        return 0, underscore_count
    else:
        return -2, None


def checkLetter(capital, guessed_letters, in_word, not_in_word):
        user_letter = input(
            'Enter one letter which is in the name of the capital: ').upper()
        result = -1
        for i in range(len(capital)):
            if capital[i] == user_letter:
                guessed_letters[i] = user_letter
                result = 0
        if result == 0:
            in_word.add(user_letter)
        else:
            not_in_word.append(user_letter)
        return result


def lives_left(lives, result):
    if result != 0:
        print("Wrong answer! You lose one life")
        lives += result
    else:
        print("Good shot")
    return lives


# add to START and END main()
def stoper():
    return time.time()


# add to highscore list
def endTime():
    clock = time.strftime('%d %b %Y %H:%M:%S')
    return clock


# in main add this function and arg
# trzeba wywolac addToHighScore w main() z argumentami start_time(start) stop_time(stop)
def list_to_add_in_highscore(capital, start, stop, player_name, uncovered_letters):
    end_game_time = endTime()
    line_with_data = [player_name, end_game_time,
                      scoring(start, stop, uncovered_letters), capital]
    split_line = '|'.join([str(elem) for elem in line_with_data])
    make_and_edit_high_score_document(split_line)

    # add to main


def scoring(start, stop, uncovered_letters):
    time_score = 1200 - (10*(stop-start))
    under_cover_position = 100 * uncovered_letters
    score = int(time_score) + under_cover_position
    return score


def make_and_edit_high_score_document(split_line):  # take user score
    with open('high_score.txt', 'a+') as open_file:
        open_file.write(split_line)


def check_position():
    pass


def main():
    play = True
    while play:
        start_time = stoper()
        not_in_word = []
        in_word = set()
        lives = 5
        capital, country = chooseCity()
        guessed_letters = blankSpots(capital)
        while True:
            system("clear")
            print_hangman(lives)
            print(f"You have {lives} lives left")
            tip(lives, country)
            if lives == 0:
                print("You lose!")
                break
            print_word_status(guessed_letters)
            print_wrong_letters(not_in_word)
            if '_' not in guessed_letters:
                print("You win")
                break
            if getUserInput() == "W":
                result, uncovered_letters = checkWord(capital, guessed_letters)
            else:
                result = checkLetter(
                    capital, guessed_letters, in_word, not_in_word)
            lives = lives_left(lives, result)
        stop_time = stoper()
        if lives > 0:
            player_name = input('What is your name?')
            list_to_add_in_highscore(
                capital, start_time, stop_time, player_name, uncovered_letters)
        play = play_again()

    print("end")


if __name__ == "__main__":
    main()
