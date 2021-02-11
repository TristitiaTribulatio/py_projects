WATER = 400
MILK = 540
BEANS = 120
CUPS = 9
MONEY = 550

class CoffeeMachine:
    def __init__(self, water=0, milk=0, beans=0, cups=0, money=0):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups
        self.money = money

    def buy(self):
        global WATER, MILK, BEANS, CUPS, MONEY
        WATER -= self.water
        MILK -= self.milk
        BEANS -= self.beans
        CUPS -= self.cups
        MONEY += self.money

    def fill(self):
        global WATER, MILK, BEANS, CUPS
        WATER += self.water
        MILK += self.milk
        BEANS += self.beans
        CUPS += self.cups

    def take(self):
        global MONEY
        MONEY = 0

    def info(self):
        global WATER, MILK, BEANS, CUPS, MONEY
        print("{0} of water".format(WATER))
        print("{0} of milk".format(MILK))
        print("{0} of coffee beans".format(BEANS))
        print("{0} of disposable cups".format(CUPS))
        print("${0} of money".format(MONEY))


def main():
    print("Write action (buy, fill, take, remaining, exit):")
    act = input()
    if act == "fill":
        print("Write how many ml of water do you want to add:")
        water = int(input())
        print("Write how many ml of milk do you want to add:")
        milk = int(input())
        print("Write how many grams of coffee beans do you want to add:")
        beans = int(input())
        print("Write how many disposable cups of coffee do you want to add:")
        cups = int(input())
        CoffeeMachine(water, milk, beans, cups).fill()
        main()
    elif act == "take":
        print("I gave you ${0}".format(MONEY))
        CoffeeMachine().take()
        main()
    elif act == "buy":
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        type = input()
        if type == "1":
            if WATER < 250 or BEANS < 16 or CUPS == 0:
                print("I haven't enough resources")
                main()
            else:
                print("I have enough resources, making you a coffee!")
                CoffeeMachine(250, 0, 16, 1, 4).buy()
                main()
        elif type == "2":
            if WATER < 350 or MILK < 75 or BEANS < 20 or CUPS == 0:
                print("I haven't enough resources")
                main()
            else:
                print("I have enough resources, making you a coffee!")
                CoffeeMachine(350, 75, 20, 1, 7).buy()
                main()
        elif type == "3":
            if WATER < 200 or MILK < 100 or BEANS < 12 or CUPS == 0:
                print("I haven't enough resources")
                main()
            else:
                print("I have enough resources, making you a coffee!")
                CoffeeMachine(200, 100, 12, 1, 6).buy()
                main()
        elif type == "back":
            main()
    elif act == "remaining":
        CoffeeMachine().info()
        main()
    elif act == "exit":
        return True


main()