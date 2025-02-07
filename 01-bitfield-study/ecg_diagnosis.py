"""
    This script interacts with a server to send ECG file data,  
    run it through a prediction model, and retrieve whether  
    the ECG contains any detected diseases.  

    Usage:
        python ecg_diagnosis.py --file path/to/file --model model_name --freq 1000
"""

"""
    The only other interesting library here is getpass,  
    which masks user password input for security.
"""
import os
import json
import requests
import argparse
import getpass
import numpy as np 

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True)
parser.add_argument("--model", required=True)
parser.add_argument("--freq", type=int, default=1000)
parser.add_argument("--output")
args = parser.parse_args()

if not os.path.exists(args.file):
    print(f"can't open file {args.file}")
    exit()

username = input("Username: ")
password = getpass.getpass("Password: ")

r = requests.post("https://private-api/login", json={"username": username, "password": password})

if r.status_code == 200:
    access_token = r.json()["access_token"]
else:
    print(r.text)
    exit()

csv_data = np.loadtxt(args.file, delimiter=',', dtype=str).tolist()
csv_data.pop(0)

for i, value in enumerate(csv_data):
    csv_data[i] = csv_data[i][1]

content = {"data": '\n'.join(csv_data),
           "model": args.model,
           "freq": args.freq}

bitfield = ""

post_r = requests.post("https://private-api/label", headers={"Authorization": "Bearer " + access_token}, data=content, stream=True)
for chunk in post_r.iter_content(chunk_size=1024):
    if chunk:
        print(str(chunk, encoding="utf-8"), end="")
        bitfield += str(chunk, encoding="utf-8")

d = {"filename": args.file,
     "bitfield": bitfield,
     "model": args.model,
     "freq": args.freq}

x = json.dumps(d)

with open(args.output, 'a') as file:
    file.write(x)