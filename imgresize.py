# -*- coding: utf-8 -*-
"""
A simple helper script for reducing images for publishing.

References
----------
- https://stackoverflow.com/questions/10607468
- https://stackoverflow.com/questions/76616042
"""
from pathlib import Path
from PIL import Image


def workflow(dname, fname, scale=6):
    """ Workflow for reducing image sizes. """
    wd = Path(f"content/media/{dname}")
    fpath = wd / fname
    npath = wd / f"{fpath.stem}-by-{scale}.jpg"

    if npath.exists():
        print(f"Already generated {npath}")
        return

    img = Image.open(fpath)
    size = (img.size[0]//scale, img.size[1]//scale)
    
    tmp = img.resize(size, Image.LANCZOS)
    tmp.save(npath, optimize=True, quality=95)


if __name__ == "__main__":
    dname = "2024-05-20-VTT-Monts-du-Lyonnais"
    workflow(dname, "IMG_20240520_100458_721.jpg", scale=6)
    workflow(dname, "IMG_20240520_110519_776.jpg", scale=6)
