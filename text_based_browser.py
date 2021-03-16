import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


def main():
    folder, stack = sys.argv[-1], deque()
    if not os.access(f"{folder}", os.F_OK):
        os.mkdir(folder)
    while True:
        url = input()
        if url == "back":
            if len(stack) <= 1:
                continue
            else:
                with open(f"{folder}/{stack.popleft()}") as file:
                    print(file.read())
                continue
        elif url == "exit":
            break
        elif "." not in url:
            print("Incorrect URL")
            continue
        else:
            stack.append(url)
            if "https://" in url:
                request = requests.get(url).content
            else:
                request = requests.get(f"https://{url}").content
            soup = BeautifulSoup(request, "html.parser")
            with open(f"{folder}/{url}", "a") as file:
                for x in soup.find("body").find_all_next():
                    if x.name == "a":
                        file.write(Fore.BLUE + x.get_text())
                        continue
                    file.write(x.get_text())
            if os.access(f"{folder}/{url}", os.F_OK):
                with open(f"{folder}/{url}") as file:
                    print(file.read())


if __name__ == "__main__":
    main()
