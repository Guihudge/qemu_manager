def choose_list(list, string, default=1):
    for index in range(len(list)):
        print(index+1, ": ", list[index])

    out = input(string)
    if out == "":
        return list[default-1]

    return list[int(out)-1]


def choose_number(string):
    return input(string)


def check_yn(awnser, info=None):
    if info != None:
        print(info)

    rep = input(awnser)

    if rep == "y" or rep == "Y":
        return True
    else:
        return False
