import random
from os import system
import os.path as path

def readFromFile():
    try:
        path_to_script = path.dirname(path.abspath(__file__))
        new_path = path.join(path_to_script, "countries_and_capitals.txt")
        with open(new_path, 'r', encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print("Cannot Find a file with countries and capitals")
        return None


def chooseCity():
    l = readFromFile()
    if l == None:
        l = ["Warsaw | Poland", "Berlin | Germany", "London | England"]
    record = random.choice(l)

    country, capital = record.split("|")
    capital, country = capital.strip().upper(), country.strip()
    return (capital, country)


def tip(lives, country):
    if lives == 1:
        print(f"Psst, It's the capital city of {country}.")


def blankSpots(capital):
    b_spots = []
    for letter in capital:
        if letter == ' ':
            b_spots.append(' ')
        else:
            b_spots.append('_')
    return b_spots


def getUserInput():
    decision = input("Enter 'w' if you want to enter a whole word." +
                     "Enter 'l' if you want to enter one letter: ")
    return decision.upper()


def checkWord(capital, guessed_letters):
    user_capital = input('Enter name of the capital: ')
    if user_capital.upper() == capital:
        print("Im here!!!!!")
        guessed_letters[:] = list(capital)
        return 0
    else:
        return -2


def checkLetter(capital, guessed_letters, in_word, not_in_word):
    user_letter = input(
        'Enter one letter which is in the name of the capital: ').upper()
    letter_list = []
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
    print(f"You have {lives} lives left")
    return lives


def main():
    play = True
    while play:
        not_in_word = []
        in_word = set()
        lives = 5
        capital, country = chooseCity()
        print(capital)
        guessed_letters = blankSpots(capital)
        print()
        while True:
            if lives == 0:
                print("You lose!")
                break
            if getUserInput() == "W":
                result = checkWord(capital, guessed_letters)
            else:
                result = checkLetter(
                    capital, guessed_letters, in_word, not_in_word)
            print(guessed_letters)
            # print(result)
            print(in_word, not_in_word)
            if not '_' in guessed_letters:
                print("You win")
                break
            lives = lives_left(lives, result)
            tip(lives, country)
        again = input("Do you want to play again? (Enter yes or no): ")
        if again.lower() == "no":
            play = False
        elif again.lower() == "yes":
            play = True

    print("end")


if __name__ == "__main__":
    main()
