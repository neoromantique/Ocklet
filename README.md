Ocklet | Simple flask image gallery
===========

Simple flask image gallery

Features: 

* Lightbox 
* Video support
* Thumbnail generation (Both for photo and video)

Setup
-----

Requirements: ```flask, pillow, ffmpeg```

Set PHOTO_DIR in main.py

Symlink 'images' in static directory to PHOTO_DIR, e.g.
```
ln -s /home/david/Pictures/ images
```

Run
---

```
python3 main.py
```
