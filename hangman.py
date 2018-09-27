import random
import time
from os import system
import os.path as path
from tabulate import tabulate


class Colors():
    reset = "\033[0m"
    green = "\033[38;2;0;255;0m"
    br_red = "\033[1;31m"
    blink_br_red = "\033[1;5;31m"
    sbrown = "\033[38;2;139;69;19m"
    nwhite = "\033[38;2;255;222;173m"
    col = "\033[38;2;139;69;19m"


def read_file(f_name):
    try:
        path_to_script = path.dirname(path.abspath(__file__))
        new_path = path.join(path_to_script, f_name)
        with open(new_path, 'r', encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Cannot Find a file - {f_name}")
        return None


def get_cities_from_file():
    cities = read_file("countries_and_capitals.txt")
    if cities == None:
        cities = ["Warsaw | Poland", "Berlin | Germany", "London | England"]
    return cities


def choose_city():
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
    print(f"{Colors.col}Wrong letter used: ", end="")
    for letter in not_in_word:
        print(letter, ",", sep="", end=" ")
    print(Colors.reset)


def read_hangman_art():
    hangman_list = read_file("ascii_hangman.txt")
    if hangman_list is None:
        hangman_list = ""
    hangman_list = [elem[:-1] for elem in hangman_list]
    return hangman_list


def print_hangman(lives):
    art = read_hangman_art()
    if art:
        print(f"{Colors.sbrown}{art[0]}")
        for i in range(1, len(art)):
            print(art[i][:11], end="")
            if lives < 5:
                print(f"{Colors.nwhite}{art[i][11:]}{Colors.sbrown}")
                lives += 1
            else:
                print()
        print(f"{Colors.reset}")


def print_lives(lives):
    if lives != 1:
        print(f"Lives left: {Colors.br_red}{lives}{Colors.reset}")
    else:
        print(f"Lives left: {Colors.blink_br_red}{lives}{Colors.reset}")


def check_win(guessed_letters):
    if '_' not in guessed_letters:
        print("CONGRATULATIONS! YOU WIN!")
        return True
    return False


def check_lose(lives, capital, country):
    if lives == 0:
        print(f"\n{Colors.br_red}YOU LOSE! WE ARE ALL DOOMED!{Colors.reset}\n")
        print(
            f"The right answer was {Colors.green}{capital}{Colors.reset}. The capital of {country}.")
        return True
    return False


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


def blank_spots(capital):
    b_spots = []
    for letter in capital:
        if letter == ' ':
            b_spots.append(' ')
        else:
            b_spots.append('_')
    return b_spots


def get_user_input():
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


def check_word(capital, guessed_letters):
    user_capital = input('Enter name of the capital: ')
    if user_capital.upper() == capital:
        underscore_count = guessed_letters.count('_')
        guessed_letters[:] = list(capital)
        return 0, underscore_count
    else:
        return -2, None


def check_letter(capital, guessed_letters, in_word, not_in_word):
    while True:
        try:
            user_letter = input(
                'Enter one letter which is in the name of the capital: ').upper()
            if len(user_letter) > 1 or user_letter.isalpha() == False:
                raise ValueError
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
        except ValueError:
            print("**** You can enter only letter. ****")


def lives_left(lives, result):
    if result != 0:
        if abs(result) == 1:
            print(f"{Colors.br_red}Wrong answer! You lose one life.{Colors.reset}")
        elif abs(result) == 2:
            print(f"{Colors.br_red}Wrong answer! You lose two lives.{Colors.reset}")
        time.sleep(2)
        lives += result
        if lives < 0:
            lives = 0
    else:
        print(f"{Colors.green}Good shot!{Colors.reset}")
        time.sleep(2)
    return lives


# add to START and END main()
def stoper():
    return time.time()


# add to highscore list
def end_time():
    clock = time.strftime('%d %b %Y %H:%M:%S')
    return clock


def list_to_add_in_highscore(capital, start, stop, player_name, uncovered_letters):
    end_game_time = end_time()
    line_with_data = [player_name, end_game_time,
                      scoring(start, stop, uncovered_letters), capital]
    split_line = '|'.join([str(elem) for elem in line_with_data])
    print(split_line)
    make_and_edit_high_score_document(split_line)


def scoring(start, stop, uncovered_letters):
    play_time = stop - start
    if play_time < 120:
        time_score = 1200 - (10*(play_time))
    else:
        time_score = 0
    under_cover_position = 100 * uncovered_letters
    score = int(time_score) + under_cover_position
    return score


def make_and_edit_high_score_document(split_line):
    with open('high_score.txt', 'a+') as open_file:
        open_file.write(split_line + '\n')


def show_high_score_top10():
    lines = []
    with open('high_score.txt', "r") as r:
        lines = r.readlines()

    delet_sign = [item.split('|')for item in lines]

    for l in delet_sign:
        l[2] = int(l[2])

    sorted_by_punctation = sorted(
        delet_sign, key=lambda tup: tup[2], reverse=True)

    sorted_and_numerate_list = []
    num = 0
    for lp, data in enumerate(sorted_by_punctation):
        if num < 10:
            data.insert(0, lp+1)
            sorted_and_numerate_list.append(data)
            num += 1

    print(tabulate(sorted_and_numerate_list, headers=[
          'Place', 'Name', 'Time', 'Score', 'Capital'], tablefmt='fancy_grid'))
    print('\n')

    back_to_menu()


def about():
    text = read_file('about.txt')
    print(''.join(text))
    print('\n\n')
    back_to_menu()


def show_banner():
    banner = read_file("banner_hangman.txt")
    if banner == None:
        banner = ""
    print("\033[6;31m"+''.join(banner)+"\033[0m")


def menu():
    while True:
        try:
            system('clear')
            show_banner()
            print(f'Choose option:\n'+'1. Start Game\n' +
                  '2. High Score\n'+'3. About\n'+'4. Exit\n')
            choice = input('Your choice: ')
            if choice == '1':
                break
            elif choice == '2':
                system('clear')
                show_high_score_top10()
            elif choice == '3':
                system('clear')
                about()
            elif choice == '4':
                exit_game()
            else:
                raise ValueError
        except ValueError:
            pass


def back_to_menu():
    word_to_exit = 'EXIT'
    while True:
        try:
            decision = input(
                f"Enter '{word_to_exit}' if you want back to menu: ")
            decision = decision.upper()
            if decision == 'EXIT' or decision == 'X':
                break
            raise ValueError
        except ValueError:
            print(f"**** You can enter '{word_to_exit}' only. ****")


def final_informations(in_word, not_in_word, start_time, stop_time):
    tries = len(in_word) + len(not_in_word)
    play_time = int(stop_time - start_time)
    print(
        f"You guessed the capital after {tries} letters. It took you {play_time} seconds")


def exit_game():
    system('clear')
    show_banner()
    print('\n\nThanks for buy our game $$$$. GANG!!')
    time.sleep(2)
    exit(1)


def main():
    play = True
    while play:
        menu()
        not_in_word = []
        in_word = set()
        lives = 5
        capital, country = choose_city()
        guessed_letters = blank_spots(capital)
        start_time = stoper()
        while True:
            system("clear")
            print_hangman(lives)
            print_lives(lives)
            tip(lives, country)
            if check_lose(lives, capital, country):
                break
            print_word_status(guessed_letters)
            print_wrong_letters(not_in_word)
            if check_win(guessed_letters):
                break
            if get_user_input() == "W":
                result, uncovered_letters = check_word(
                    capital, guessed_letters)
            else:
                result = check_letter(
                    capital, guessed_letters, in_word, not_in_word)
            lives = lives_left(lives, result)
        stop_time = stoper()
        if lives > 0:
            final_informations(in_word, not_in_word, start_time, stop_time)
            player_name = input('What is your name? ')
            list_to_add_in_highscore(
                capital, start_time, stop_time, player_name, uncovered_letters)
        play = play_again()


if __name__ == "__main__":
    main()
