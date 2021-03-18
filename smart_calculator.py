from collections import deque
from re import findall, sub
from string import punctuation


def main():
    dict_vars = dict()
    while True:
        nums = input()
        if "=" in nums:
            nums = list(map(lambda x: x.strip(), nums.split("=")))
            try:
                if len(nums) >= 3:
                    print("Invalid assignment")
                elif not nums[0].isalpha():
                    print("Invalid identifier")
                elif not nums[1].isdigit() and not nums[1].isalpha():
                    print("Invalid assignment")
                elif nums[1].isalpha():
                    dict_vars[nums[0]] = dict_vars[nums[1]]
                elif nums[1].isdigit():
                    dict_vars[nums[0]] = nums[1]
            except KeyError:
                print("Unknown variable")
        elif "=" not in nums:
            if len(nums) >= 1 and nums[0] == "/":
                if not commands(nums):
                    return True
            else:
                expressions(nums, dict_vars)


def commands(nums):
    if nums == "/exit":
        print("Bye!")
        return False
    elif nums == "/help":
        print("The program calculates the sum of numbers")
    else:
        print("Unknown command")
    return True


def expressions(nums, dict_vars):
    deq, res_list = deque(), list()
    if len(nums) == 0:
        return True
    if infix_to_postfix(nums, dict_vars, deq, res_list):
        if len(deq) >= 1:
            print("Invalid expression")
            return False
        postfix_to_result(dict_vars, deq, res_list)


def infix_to_postfix(nums, dict_vars, deq, res_list):
    high, low = list(["*", "/"]), list(["+", "-"])
    nums = findall('[()]|[*/+-]+|[0-9]+|[a-zA-Z]+', sub('[+]+', "+", nums))
    if nums[0] == "-":
        nums[0] += nums[1]
        del nums[1]
    if len(nums) == 1:
        if nums[0].isalpha():
            try:
                print(dict_vars[nums[0]])
            except KeyError:
                print("Unknown variable")
        elif nums[0].isdigit():
            print(nums[0])
        return False
    for x in range(1, len(nums)):
        if "-" in nums[x]:
            if len(nums[x]) % 2 == 0:
                nums[x] = "+"
            elif len(nums[x]) % 2 == 1:
                nums[x] = "-"
        elif "*" in nums[x] or "/" in nums[x]:
            if len(nums[x]) >= 2:
                print("Invalid expression")
                return False
    try:
        for x in nums:
            if x not in punctuation:
                res_list.append(x)
            elif len(deq) == 0 or deq[-1] == "(":
                deq.append(x)
            elif deq[-1] in low and x in high:
                deq.append(x)
            elif (deq[-1] in high and (x in high or x in low)) or (deq[-1] in low and x in low):
                while True:
                    res_list.append(deq.pop())
                    if len(deq) == 0 or (deq[-1] is low and x in high) or deq[-1] == "(":
                        deq.append(x)
                        break
            elif x == "(":
                deq.append(x)
            elif x == ")":
                while True:
                    res_list.append(deq.pop())
                    if deq[-1] == "(":
                        deq.pop()
                        break
        for y in range(len(deq)):
            if deq[-1] in high or deq[-1] in low:
                res_list.append(deq.pop())
        return True
    except IndexError:
        print("Invalid expression")


def postfix_to_result(dict_vars, deq, res_list):
    for z in res_list:
        if z.isdigit() or z.isalpha():
            deq.append(z)
        elif z in ["*", "/", "+", "-"]:
            num1, num2 = str(deq.pop()), str(deq.pop())
            if num1.isalpha() and num2.isalpha():
                num1, num2 = dict_vars[num1], dict_vars[num2]
            elif num1.isalpha():
                num1 = dict_vars[num1]
            elif num2.isalpha():
                num2 = dict_vars[num2]

            if z == "/":
                deq.append(int(eval(f'{num2}{z}{num1}')))
            elif z in ["*", "+", "-"]:
                deq.append(eval(f'{num2}{z}{num1}'))
    print(deq.pop())


if __name__ == "__main__":
    main()
