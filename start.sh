#!/bin/bash
# https://superuser.com/a/1221697

myscript(){
    python3 main.py
}

until myscript; do
    echo "'Main' crashed with exit code $?. Restarting..." >&2
    sleep 1
done

