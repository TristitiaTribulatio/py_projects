import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cur = connection.cursor()
card_number, pin, log_check = [], 0, 0


def main():
    global log_check
    while True:
        if log_check == 0:
            if not main_menu():
                break
        elif log_check == 1:
            if not log_menu():
                break


def create_account():
    global card_number, pin
    card_number = list("400000{0}".format(random.randint(100000000, 999999999)))
    luhn_algorithm(card_number, "create")
    pin = random.randint(1000, 9999)
    cur.execute("INSERT INTO card (number, pin) VALUES ({0}, {1})".format(card_number, pin))
    connection.commit()
    print("\nYour card has been created\nYour card number:\n{0}\nYour card PIN:\n{1}\n".format(card_number, pin))


def log():
    global card_number, pin, log_check
    print("\nEnter your card number:")
    check_card = int(input())
    print("Enter your PIN:")
    check_pin = int(input())
    cur.execute("SELECT number FROM card WHERE number = {0};".format(check_card))
    if bool(cur.fetchone()):
        cur.execute("SELECT number, pin FROM card WHERE number = {0};".format(check_card))
        card_db, pin_db = cur.fetchone()
        if check_card == int(card_db) and check_pin == int(pin_db):
            print("\nYou have successfully logged in!\n")
            log_check, card_number, pin = 1, card_db, pin_db
        else:
            print("\nWrong card number or PIN!\n")
    else:
        print("\nWrong card number or PIN!\n")


def main_menu():
    print("1. Create an account\n2. Log into account\n0. Exit")
    number = int(input())
    if number == 1:
        create_account()
    elif number == 2:
        log()
    elif number == 0:
        print("\nBye!")
        return False
    return True


def log_menu():
    global log_check
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    number = int(input())
    if number == 1:
        balance()
    elif number == 2:
        add_income()
    elif number == 3:
        do_transfer()
    elif number == 4:
        close_account()
    elif number == 5:
        print("\nYou have successfully logged out!\n")
        log_check = 0
    elif number == 0:
        print("\nBye!")
        return False
    return True


def luhn_algorithm(card_n, act):
    global card_number
    checksum, sum_v, card_str, card_copy = 0, 0, "", list(card_n)
    if act == "transfer":
        card_copy.pop()
    card_copy = [int(card_copy[x]) for x in range(len(card_copy))]
    card_copy = [card_copy[x] * 2 if x % 2 == 0 else card_copy[x] for x in range(len(card_copy))]
    card_copy = [card_copy[x] - 9 if card_copy[x] > 9 else card_copy[x] for x in range(len(card_copy))]
    for x in range(len(card_copy)):
        sum_v += card_copy[x]
    while True:
        if sum_v % 10 == 0:
            break
        else:
            sum_v += 1
            checksum += 1
    if act == "create":
        card_number.append(checksum)
        card_number = [str(card_number[x]) for x in range(len(card_number))]
        for x in range(len(card_number)):
            card_str += card_number[x]
        card_number = int(card_str)
        return True
    elif act == "transfer":
        if checksum == int(card_n[-1]):
            return True
        else:
            return False


def balance():
    cur.execute("SELECT balance FROM card WHERE number = {0};".format(card_number))
    print("\nBalance: {0}\n".format((cur.fetchone())[0]))


def add_income():
    print("\nEnter income:")
    income = int(input())
    cur.execute("UPDATE card SET balance = balance + {0} WHERE number = {1};".format(income, card_number))
    connection.commit()
    print("Income was added!\n")


def do_transfer():
    print("\nTransfer\nEnter card number:")
    card_n = int(input())
    cur.execute("SELECT number FROM card WHERE number = {0};".format(card_n))
    if card_n == card_number:
        print("You can't transfer money to the same account!\n")
        return True
    elif not luhn_algorithm(list(str(card_n)), "transfer"):
        print("Probably you made a mistake in the card number. Please try again!\n")
        return True
    elif not bool(cur.fetchone()):
        print("Such a card does not exist.\n")
        return True
    print("Enter how much money you want to transfer:")
    money = int(input())
    cur.execute("SELECT balance FROM card WHERE number = {0};".format(card_number))
    if (cur.fetchone())[0] < money:
        print("Not enough money!\n")
        return True
    cur.execute("UPDATE card SET balance = balance + {0} WHERE number = {1};".format(money, card_n))
    connection.commit()
    cur.execute("UPDATE card SET balance = balance - {0} WHERE number = {1};".format(money, card_number))
    connection.commit()
    print("Success!\n")


def close_account():
    global log_check, card_number
    print("\nThe account has been closed!\n")
    cur.execute("DELETE FROM card WHERE number = {0};".format(card_number))
    connection.commit()
    log_check, card_number = 0, []


main()
