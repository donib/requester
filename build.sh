#!/bin/bash
pyinstaller --noconfirm --onefile --windowed --icon "./icon.ico" --name "requester_`date +%Y%m%d`" --clean --add-data "./icon.png;."  "./main.py"

#rm -rf build requester*.spec