from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

from os import listdir, mkdir, symlink, _exit, environ, walk, path
from os.path import isdir, join, dirname, exists, splitext
from PIL import Image

import os.path
import subprocess
import json
from pathlib import Path

debug = False
proto = 'https'

if (environ.get('ENV') == "development"):
    proto = 'http'
    debug = True

app = Flask(__name__)

app.config.update(dict(
    DEBUG=debug,
    SECRET_KEY='SECRET',
    # PHOTO_DIR needs to be symlinked from 'static/images' to allow files to be
    # served:
    # ln -s /home/david/Pictures/ images
    PHOTO_DIR='/home/david/Pictures',
    FQDN=environ.get('DOMAIN'),
    THUMB_SIZE=(256, 256)
))


@app.route('/restart', defaults={'path': ''})
def restart(path):
    _exit(11)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def photo_dir(path):
    pd = app.config['PHOTO_DIR']
    dir_entries = []
    image_entries = []
    up = None

    if path != '':
        up = dirname(join('/', path))

    nav = join(pd, path)
    if isdir(nav):
        thumb_dir = join(nav, '.thumbnail')
        if not exists(thumb_dir):
            mkdir(thumb_dir)
        list_all = sorted(listdir(nav))

        for list_item in list_all:
            if isdir(join(nav, list_item)) and list_item != '.thumbnail':
                dir_entries.append(list_item)
            elif list_item.endswith('.png') or list_item.endswith('.jpg') or list_item.endswith('.JPG') or list_item.endswith('.jpeg'):
                # Generate missing thumbnails
                thumb = join(thumb_dir, list_item)
                thumbjpg = Path(thumb).stem + '.jpg'
                if not exists(str(Path(thumb).parent) + '/' + thumbjpg):
                    print('Generating thumb', thumb)
                    im = Image.open(join(nav, list_item))
                    if im.mode != "RGB":
                        im = im.convert("RGB")
                    im.thumbnail(app.config['THUMB_SIZE'], Image.ANTIALIAS)
                    im.save(str(Path(thumb).parent) + '/' + thumbjpg, "JPEG")
                image_entries.append([list_item, thumbjpg])

            elif list_item.endswith('.mp4') or list_item.endswith('.webp') or list_item.endswith('.gif'):
                # Generate missing thumbnails 
                thumb = join(thumb_dir, list_item)
                thumbjpg = Path(thumb).stem + '.jpg'
                if not exists(str(Path(thumb).parent) + '/' + thumbjpg):
                    subprocess.call(['ffmpeg', '-i', join(nav, list_item), '-ss', '00:00:00.000',
                                     '-vframes', '1', str(Path(thumb).parent) + '/' + thumbjpg])
                image_entries.append([list_item, thumbjpg])

        return render_template('layout.html', dir_entries=dir_entries, image_entries=image_entries, path=path, up=up, proto=proto, base=app.config['FQDN'])


@app.route('/api/', defaults={'path': ''})
@app.route('/api/<path:path>')
def photo_feed(path):
    base = app.config['PHOTO_DIR']
    up = None
    if path != '':
        up = dirname(join('/', path))

    entries = {"domain": proto + '://' + app.config['FQDN'], "up": up, "dir": [], "img": []}

    dir = join(base + '/' + path)

    for list_item in sorted(listdir(dir)):
        if isdir(join(dir, list_item)) and list_item != '.thumbnail':
            entries['dir'].append(list_item)
        elif list_item.endswith('.png') or list_item.endswith('.jpg') or list_item.endswith('.JPG') or list_item.endswith('.jpeg'):
            entries['img'].append(list_item)
        elif list_item.endswith('.mp4') or list_item.endswith('.webp') or list_item.endswith('.gif'):
            entries['img'].append(list_item)

    return(json.dumps(entries))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
