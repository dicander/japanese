import unicodedata
import random


distractors = []


def init():
    global distractors
    with open("distractors.txt", "r") as file:
        for row in file:
            distractors.append(set(row.split()))


def quiz(v, d):
    random.shuffle(v)
    fails = []
    correct = 0
    incorrect = 0
    for i, x in enumerate(v):
        preview = " ".join(v[i+1:min(i+4, len(v))])
        guess = input(x+" ("+preview+") : ").lower()
        if guess == d[x]:
            correct += 1
            print("Yes.")
        else:
            incorrect +=1
            print("No.")
            print(x, "means", d[x].lower())
            fails.append(x)
            for y in d.keys():
                if d[y] == guess:
                    print(y, "means", d[y]+".")
    print("correct", correct)
    print("incorrect", incorrect)
    return fails


def kanadict(start, end):
    d = dict()
    for x in range(start, end):
        kana = chr(x)
        row = unicodedata.name(kana)
        if "SMALL" not in row:
            latinization = row.split()[-1]
            d[kana] = latinization.lower()
    v = list(d.keys())
    return v, d


def reversequiz(v, d):
    correct = 0
    incorrect = 0
    distractors = []
    fails = []
    reversedict = {val: k for k, val in d.items()}
    random.shuffle(v)
    for kana in v:
        similar = set()
        for cluster in distractors:
            if kana in cluster:
                similar |= cluster
        for latinization in d.values():
            if latinization[0] == d[kana][0] or\
               (len(latinization) == 2 and \
               len(d[kana]) == 2 and \
               latinization[1] == d[kana][1]) or \
               (len(latinization) == 1 and \
                len(latinization)==1):
                   similar.add(reversedict[latinization])
        print("Find", unicodedata.name(kana))
        while len(similar)>5:
            victim = random.choice(list(similar))
            if victim != kana:
                similar.remove(victim)
        similar = list(similar)
        random.shuffle(similar)
        for index, value in enumerate(similar):
            print(str(index+1) + ": " + value, end = "  ")
            if index>0 and index%5 == 0:
                print()
        print()
        candidate = input(">")
        if candidate.isdigit() and 0 < int(candidate) <= len(similar):
            i = int(candidate)-1
            if similar[i] == kana:
                print("Yes.")
                correct += 1
            else:
                print("No.", similar[i], "means", unicodedata.name(similar[i]))
                print("The right kana was", kana)
                incorrect += 1
                fails.append(kana)
        else:
            print("Not an integer")
            incorrect += 1
            fails.append(kana)
    print("Correct:", correct)
    print("Incorrect:", incorrect)
    return fails


def main():
    init
    hiragana = kanadict(0x3041, 0x3097)
    katakana = kanadict(0x30a1, 0x30fb)
    for f in reversequiz, quiz:
        for v, d in [hiragana, katakana]:
            turn = 0
            while v:
                turn += 1
                v = f(v, d)
                if turn == 1 and v == []:
                    print("Perfect!")
                print("End of turn", turn)


main()
