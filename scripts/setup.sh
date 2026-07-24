#!/bin/bash

apt update
apt install python3 python3-venv
cd /darcy/

python3 -m venv .venv
source .venv/bin/activate

pip install -U discord.py python-dotenv discord-py-interactions