#!/bin/bash
pyinstaller --noconfirm --onefile --windowed --icon "./icon.ico" --name "requester" --clean --add-data "./icon.png;."  "./main.py"