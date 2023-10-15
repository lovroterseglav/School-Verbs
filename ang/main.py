import csv
from random import shuffle

import wasabi
from wasabi import diff_strings

RESET_FORMATTING = "\033[0m"
TENSES = ["Infinitive", "Past", "Past Participle"]


def ask(slo: str, d: tuple[str, str, str]):
    f = lambda x: [i.strip() for i in x.split("/")]
    status = []
    print(f"------------------------ {slo} ------------------------")

    for tenese, verb in zip(TENSES, d):
        options = f(verb)
        resp = input().strip()
        if resp == "exit":
            exit(0)
        if resp in options:
            status.append((True, f"{resp} ({'/'.join(options)})"))
            continue
        status.append((False, f"{resp} ({'/'.join(options)})"))

    print()

    for s, r in status:
        if s:
            wasabi.msg.good(r)
        else:
            wasabi.msg.fail(r)

    print()

if __name__ == "__main__":
    with open("ang/verbs.csv") as fr:
        data = [tuple(x) for x in csv.reader(fr) if x]
        data.pop(0)
        shuffle(data)
        # data = set(data)

    di = data.__iter__()
    while True:
        i = next(di, None)
        if not i:
            print("\n\nNew Round\n")
            shuffle(data)
            di = data.__iter__()
            continue
        ask(i[0], (i[1], i[2], i[3]))
#
