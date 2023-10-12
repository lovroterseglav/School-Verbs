import base64
import csv
import difflib
import logging
import os
import random

import pydub.playback
import vlc

import requests
from pydub import AudioSegment
import wasabi
from wasabi import color

RESET_FORMATTING = "\033[0m"
os.environ['VLC_VERBOSE'] = '-1'


def fetch_audio_from_url(url):
    try:
        # Define custom headers to mimic the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'TE': 'trailers',
            'Cookie': 'your-cookie-data-here',  # Include your specific cookies
        }

        # Send an HTTP GET request to the URL with custom headers
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Check the content type to ensure it's audio/mpeg or the appropriate format
            if "audio/mpeg" in response.headers.get("Content-Type"):
                # Return the audio data
                return response.content

            else:
                print("The response content is not audio/mpeg.")
        else:
            print("Failed to retrieve the audio file. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))


def play_word(word: str):
    b64 = base64.b64encode(word.encode("utf-8")).decode("utf-8")
    url = f"https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/voiceName=Klaus22k?inputText={b64}"
    p = vlc.MediaPlayer(url)
    p.audio_set_volume(70)
    p.play()


def diff_strings(original, needed):
    output = []
    matcher = difflib.SequenceMatcher(None, original, needed)
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == "equal":
            output.append(original[a0:a1])
        elif opcode == "insert":
            output.append(color(needed[b0:b1], fg=16, bg="green"))
        elif opcode == "delete":
            output.append(color(original[a0:a1], fg=16, bg="red"))
        elif opcode == "replace":
            output.append(color(needed[b0:b1], fg=16, bg="green"))
            output.append(color(original[a0:a1], fg=16, bg="red"))
    return "".join(output)


def verb_ask(data: list[str], prefix):
    bad = []
    for p, v in zip(prefix, data):
        p = p.split("-")[0]
        v: str
        p: str
        if p == "SLO":
            print(f"------------------------ {v.capitalize()} ------------------------\n")
            continue
        print(p, end=" ")
        resp = input().strip()
        if resp == "exit":
            exit(0)
        play_word(v)
        if resp == v:
            wasabi.msg.good(f"{p} {v}")
            print()
            continue
        diff = diff_strings(resp, v)
        print((wasabi.color("✘ ", fg="red") + RESET_FORMATTING + diff.strip() + f" ({p} {v})").replace("\n", "") + "\n")
        bad.append(f"{diff} ({p} {v})")
    print(",\n".join(bad))


def verbs():
    with open("verbs.csv") as fr:
        verbs = list(csv.reader(fr))
        prefix = verbs.pop(0)
    l = None
    while True:
        ver = verbs[random.randint(0, len(verbs) - 1)]
        if ver == l:
            continue
        l = ver
        verb_ask(ver, prefix)


def word_ask(si_word, de_word):
    print(f"------------------------ {si_word} ------------------------\n")
    resp = input().strip()
    if resp == "exit":
        exit(0)
    play_word(de_word)
    if resp == de_word:
        wasabi.msg.good(f"{de_word} {si_word}")
        print()
        return
    diff = diff_strings(resp, de_word)
    print((wasabi.color("✘ ", fg="red") + RESET_FORMATTING + diff.strip() + f" ({de_word})").replace("\n", "") + "\n")


def words(file):
    with open(file) as fr:
        data = list(csv.reader(fr))

    l = None
    while True:
        w = data[random.randint(0, len(data) - 1)]
        if w == l:
            continue
        l = w
        word_ask(w[1], w[0])

# words("words.csv")
# words("numbers.csv")
verbs()