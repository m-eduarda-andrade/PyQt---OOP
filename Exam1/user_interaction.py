# define vocals

CONSTANTS = {
    "up_low": ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U", "ä", "Ä", "ö", "Ö", "ü", "Ü"],
    "low": ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
}


def create_new_dict(case):
    dic = dict()

    if case:
        dic = {i: 0 for i in CONSTANTS["up_low"]}
    else:
        dic = {i: 0 for i in CONSTANTS["low"]}

    return dic


def count_vocals(text, case=True):
    if case:
        dic = create_new_dict(case)
        for i in text:
            if i in dic.keys():
                dic[i] += 1
            else:
                continue
    else:
        dic = create_new_dict(case)
        text = text.lower()

        for i in text:
            if i in dic.keys():
                dic[i] += 1
            else:
                continue

    return dic


def print_result(text, counter):
    print("Text:\n", text)

    print("Counter:")
    for k, v in counter.items():
        print(k, ":", v)


def main():
    my_text = input("\nWrite your text: (0 to exit)\n")

    while my_text != "0":

        case = input("\nCase sensitive ([Y]/N): (Case sensitive True is default)\n")
        if case.lower() == "n":
            case = False
        else:
            case = True

        counter = count_vocals(my_text, case)

        print_result(my_text, counter)

        my_text = input("\nWrite your text: (0 to exit)\n")


main()
