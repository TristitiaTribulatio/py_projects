import random
options, score = [], 0

def main():
    global score, options
    name_player()
    init_option()
    while True:
        user_enter = input()
        if user_enter in options:
            unfair_computer(user_enter)
        elif user_enter == "!exit":
            print("Bye!")
            break
        elif user_enter == "!rating":
            print("Your rating: {0}".format(score))
        else:
            print("Invalid input")
    return True


def unfair_computer(user_enter):
    global score, options
    win_list = priority(user_enter)
    rand_choice = random.randint(0, len(options) - 1)
    if user_enter == options[rand_choice]:
        print(f"There is a draw ({user_enter})")
        score += 50
    elif options[rand_choice] not in win_list and user_enter != options[rand_choice]:
        print(f"Well done. The computer chose {options[rand_choice]} and failed")
        score += 100
    elif options[rand_choice] in win_list and user_enter != options[rand_choice]:
        print(f"Sorry, but the computer chose {options[rand_choice]}")


def name_player():
    global score
    name = input("Enter your name: ")
    print("Hello, {0}".format(name))
    names = open("rating.txt", "r")
    for i in names:
        if (i.split())[0] == name:
            score = int((i.split())[1])


def init_option():
    global options
    options = list(input().split(','))
    if options == [""]:
        options = ["rock", "paper", "scissors"]
    print("Okay, let's start")


def priority(user_enter):
    global options
    quan_options = (len(options) - 1) // 2
    win_list = options[options.index(user_enter) + 1 : options.index(user_enter) + quan_options + 1]
    if len(win_list) == quan_options:
        return win_list
    else:
        quan_options -= len(win_list)
        win_list += options[:quan_options]
        return win_list


main()
