from nltk.tokenize import WhitespaceTokenizer
from nltk import bigrams, trigrams
from collections import defaultdict, Counter
from random import choices, randint


def main():
    user_value = input()
    file = open(f"{user_value}", "r", encoding="utf-8")
    # chain_model(file)
    # generate_random_text(file)
    # generate_full_sentences_bigrams(file)
    generate_full_sentences_trigram(file)


def generate_full_sentences_trigram(file):
    corpus, res_list, count = list(trigrams(WhitespaceTokenizer().tokenize(file.read()))), list(), 0
    while True:
        while True:
            random_value = choices(corpus)
            value = f"{random_value[0][0]} {random_value[0][1]}"
            if value[0].isupper() and (value.split())[0][-1] not in [".", "!", "?"]:
                break
        while True:
            corpus_dict = defaultdict(int)
            if res_list == []:
                res_list.append(value)
            else:
                res_list.append((value.split())[1])
            for x in corpus:
                if f"{x[0]} {x[1]}" == value:
                    corpus_dict[x[2]] += 1
            if len(res_list) >= 5:
                if (value.split())[0][-1] in [".", "!", "?"]:
                    res_list.pop()
                    break
            random_value = choices(Counter(corpus_dict).most_common())
            value = f"{(value.split())[1]} {random_value[0][0]}"
        for x in res_list:
            print(x, end=" ")
        print()
        res_list = list()
        count += 1
        if count == 10:
            break


def generate_full_sentences_bigrams(file):
    corpus, res_list, count = list(bigrams(WhitespaceTokenizer().tokenize(file.read()))), list(), 0
    while True:
        while True:
            value = (choices(corpus))[0][randint(0, 1)]
            if value[0].isupper() and value[-1] not in [".", "!", "?"]:
                break
        while True:
            corpus_dict = defaultdict(int)
            res_list.append(value)
            for x in corpus:
                if x[0] == value:
                    corpus_dict[x[1]] += 1
            if len(res_list) >= 5:
                if value[-1] in [".", "!", "?"]:
                    break
            value = (choices(Counter(corpus_dict).most_common()))[0][0]
        for x in res_list:
            print(x, end=" ")
        print()
        res_list = list()
        count += 1
        if count == 10:
            break


def generate_random_text(file):
    corpus, res_list, check = list(bigrams(WhitespaceTokenizer().tokenize(file.read()))), list(), 0
    value = (choices(corpus))[0][randint(0, 1)]
    while True:
        corpus_dict = defaultdict(int)
        res_list.append(value)
        for x in corpus:
            if x[0] == value:
                corpus_dict[x[1]] += 1
        value = (choices(Counter(corpus_dict).most_common()))[0][0]
        if len(res_list) == 10:
            for x in res_list:
                print(x, end=" ")
            res_list = list()
            print()
        if check == 100:
            break
        check += 1


def chain_model(file):
    corpus = list(bigrams(WhitespaceTokenizer().tokenize(file.read())))
    corpus_dict = defaultdict(int)
    while True:
        try:
            corpus_dict = defaultdict(int)
            value = input()
            if value == "exit":
                break
            print(f"Head: {value}")
            for x in corpus:
                if x[0] == value:
                    corpus_dict[x[1]] += 1
            for tail, count in Counter(corpus_dict).most_common():
                if count > 1:
                    print(f"Tail: {tail} Count: {count}")
        except KeyError:
            print('Key Error. The requested word is not in the model. Please input another word.\n')


if __name__ == "__main__":
    main()