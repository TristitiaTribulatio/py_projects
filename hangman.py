import random
words = ['python', 'java', 'kotlin', 'javascript']
rand_word_hidden, rand_word, check, set_letters, letter = [], "", 8, set(), ""


def set_word():
    global rand_word, rand_word_hidden
    rand_word = random.choice(words)
    rand_word_hidden = ["-"] * len(rand_word)


def main():
    global rand_word, rand_word_hidden, check, letter
    print("H A N G M A N")
    menu_choice = menu()
    if menu_choice == "play":
        set_word()
        add_space()
        while True:

            if check_status():
                return False

            verification()

            if letter in rand_word:
                if letter in set_letters:
                    print("You've already guessed this letter")
                    add_space()
                    continue
                for i in range(len(rand_word)):
                    if rand_word[i] == letter:
                        rand_word_hidden[i] = letter
                        set_letters.add(letter)
                        if check_status():
                            return False
            elif letter not in rand_word:
                if letter in set_letters:
                    print("You've already guessed this letter")
                    add_space()
                    continue
                print("That letter doesn't appear in the word")
                set_letters.add(letter)
                check -= 1

            add_space()
    elif menu_choice == "exit":
        return True


def add_space():
    global check
    if check != 0:
        print()


def verification():
    global letter, rand_word_hidden
    while True:
        print("".join(rand_word_hidden))
        letter = input("Input a letter: ")

        if len(letter) != 1:
            print("You should input a single letter")
            add_space()
            continue
        elif letter.lower() != letter or letter not in "abcdefghijklmnopqrstuvwxyz":
            print("Please enter a lowercase English letter")
            add_space()
            continue

        return False


def check_status():
    if "-" not in rand_word_hidden:
        print("You guessed the word!")
        print("You survived!")
        return True
    elif check == 0:
        print("You lost!")
        return True
    return False


def menu():
    while True:
        choice = input('Type "play" to play the game, "exit" to quit:')
        if choice == "play" or choice == "exit":
            break
    return choice


main()
