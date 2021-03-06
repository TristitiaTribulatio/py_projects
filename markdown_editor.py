formatters, res = list(["plain", "bold", "italic", "inline-code",
                        "link", "header", "line-break",
                        "ordered-list", "unordered-list"]), list()


def only_text(index):
    text = input("- Text: ")
    if index == 0:
        return f"{text}"
    elif index == 1:
        return f"**{text}**"
    elif index == 2:
        return f"*{text}*"
    elif index == 3:
        return f"`{text}`"


def lvl_text():
    while True:
        lvl = int(input("- Level: "))
        if lvl in [1, 2, 3, 4, 5, 6]:
            break
        print("The level should be within the range of 1 to 6")
    text = input("- Text: ")
    return f"{'#'*lvl} {text}\n"


def url_label():
    label, url = input("- Label: "), input("- URL: ")
    return f"[{label}]({url})"


def line_break():
    return "\n"


def lists(index):
    while True:
        rows = int(input("- Number of rows: "))
        if rows > 0:
            break
        print("The number of rows should be greater than zero")
    list_rows = list()
    for x in range(0, rows):
        list_rows.append(input(f"- Row #{x + 1}: "))
    if index == 7:
        return list(map(lambda y: f"{list_rows.index(y) + 1}. {y}", list_rows))
    elif index == 8:
        return list(map(lambda y: f"* {y}", list_rows))


def main():
    while True:
        choice = input("- Choose a formatter: ")
        if choice == "!help":
            print("Available formatters: plain bold italic link inline-code header"
                  " ordered-list unordered-list line-break\nSpecial commands: !help !done")
        elif choice in formatters[:4]:
            res.append(only_text(formatters.index(choice)))
        elif choice in formatters[5]:
            res.append(lvl_text())
        elif choice in formatters[4]:
            res.append(url_label())
        elif choice in formatters[6]:
            res.append(line_break())
        elif choice in formatters[7:]:
            res.append(lists(formatters.index(choice)))
        elif choice == "!done":
            file = open("output.md", "w")
            for i in res:
                if type(i) is list:
                    for j in i:
                        file.write(f"{j}\n")
                else:
                    file.write(i)
            file.close()
            break
        elif choice not in formatters:
            print("Unknown formatter or command. Please try again")
        for i in res:
            if type(i) is list:
                for j in i:
                    print(j, sep="")
            else:
                print(i, sep="", end="")
        print()


if __name__ == "__main__":
    main()