from random import randint


class Friends:
    def __init__(self):
        self.friends, self.count = {}, 0
        self.count = int(input("Enter the number of friends joining (including you):\n"))
        if self.count > 0:
            self.enter_friends()
            self.enter_total_bill()
            self.show_friends()
        else:
            print("No one is joining for the party")

    def enter_friends(self):
        print("\nEnter the name of every friend (including you), each on a new line:")
        for _ in range(self.count):
            self.friends[input()] = 0

    def show_friends(self):
        if self.friends:
            print(self.friends)

    def enter_total_bill(self):
        print("\nEnter the total bill value:")
        total_bill = int(input())
        the_lucky_one = self.is_lucky()
        if not the_lucky_one:
            average_bill = round(total_bill / len(self.friends), 2)
            for key, value in self.friends.items():
                self.friends.update({key: value+average_bill})
        elif the_lucky_one:
            average_bill = round(total_bill / (len(self.friends)-1), 2)
            for key, value in self.friends.items():
                self.friends.update({key: value+average_bill})
            self.friends[the_lucky_one] = 0

    def is_lucky(self):
        choice = input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:')
        if choice == "Yes":
            the_lucky_one = list(self.friends.keys())[randint(0, len(self.friends.keys()) - 1)]
            print(f"\n{the_lucky_one} is the lucky one!\n")
            return the_lucky_one
        elif choice == "No":
            print("\nNo one is going to be lucky\n")
            return False


if __name__ == "__main__":
    Friends()