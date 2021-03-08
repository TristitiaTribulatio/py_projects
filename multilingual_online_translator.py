import requests
import sys
from bs4 import BeautifulSoup


def translate():
    url, languages = "", {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                          8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}
    first_lang, second_lang, word = "", "", ""
    try:
        if len(sys.argv) == 1:
            print("Hello, you're welcome to the translator. Translator supports:")
            for key, value in languages.items():
                print(f"{key}. {value}")
            first_lang = int(input("Type the number of your language: "))
            second_lang = int(input("Type the number of a language you want to translate to or '0' to translate to all languages: "))
            word = input("Type the word you want to translate: ")
        elif len(sys.argv) > 1:
            first_lang = sys.argv[-3]
            second_lang = sys.argv[-2]
            word = sys.argv[-1]
            for key, value in languages.items():
                if value.lower() == first_lang.lower():
                    first_lang = key
                    break
            for key, value in languages.items():
                if value.lower() == second_lang.lower():
                    second_lang = key
                    break
            if isinstance(second_lang, str) and second_lang == "all":
                second_lang = 0
        if second_lang == 0:
            for key, value in languages.items():
                if value == languages[first_lang]:
                    continue
                url = f"https://context.reverso.net/translation/{languages[first_lang].lower()}-{value.lower()}/{word}"
                response_translator(languages, url, key, word)
        else:
            url = f"https://context.reverso.net/translation/{languages[first_lang].lower()}-{languages[second_lang].lower()}/{word}"
            response_translator(languages, url, second_lang, word)
    except KeyError:
        print(f"Sorry, the program doesn't support {second_lang}")


def response_translator(languages, url, second_lang, word):
    try:
        request = requests.get(url, headers={'User-Agent': 'Mozilla / 5.0'})
        if request.status_code == 200:
            translate_page = BeautifulSoup(request.content, "html.parser")
            words = translate_page.find("div", {"id": "translations-content"}).find_all("a", {"class": "translation"})
            words_text = [y.get_text().strip() for y in words]
            examples = translate_page.find("section", {"id": "examples-content"}).find_all("div", {"class": "ltr"})
            examples_text = [x.get_text().strip() for x in examples]
            # print_translation(languages, words_text, examples_text, second_lang)
            save_and_read_translation(languages, words_text, examples_text, second_lang, word)
        elif request.status_code == 404:
            raise IndexError
    except requests.ConnectionError:
        print("Something wrong with your internet connection")
    except IndexError:
        print(f"Sorry, unable to find {word}")


def print_translation(languages, words_text, examples_text, second_lang):
    print(f"\n{languages[second_lang]} translations:")
    for i in range(len(words_text)):
        print(words_text[i])
    print(f"\n{languages[second_lang]} Examples:")
    for j in range(len(examples_text)):
        if j % 2 == 0:
            print(f"{examples_text[j]}")
        elif j % 2 == 1:
            print(f"{examples_text[j]}\n")


def save_and_read_translation(languages, words_text, examples_text, second_lang, word):
    save_file = open(f"{word}.txt", "a", encoding="utf-8")
    save_file.write(f"""
{languages[second_lang]} translations:
{words_text[0]}

{languages[second_lang]} Examples:
{examples_text[0]}
{examples_text[1]}  
    """)
    save_file.close()

    read_file = open(f"{word}.txt", "r", encoding="utf-8")
    print(read_file.read())
    read_file.close()


if __name__ == "__main__":
    translate()
