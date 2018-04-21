#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
from os import makedirs, path
import shutil
import threading

import gyazo
from jinja2 import Environment, FileSystemLoader
from progress.bar import Bar


def backup(args):
    # Destination directory check and create
    try:
        dest_dir = create_dest_dir(args.directory)
        create_dest_dir(dest_dir + 'images/')
        create_dest_dir(dest_dir + 'thumbnails/')
    except IOError:
        return 1

    api = gyazo.Api(access_token=args.access_token)
    new_images = download_image_list(api)
    old_images = load_old_image_list(dest_dir)
    images = merge_image_lists(new_images, old_images)
    download_images(images, dest_dir, num_threads=args.num_threads)
    save_image_list(images, dest_dir)
    export_html(images, dest_dir)

    return 0


def merge_image_lists(images_1, images_2):
    index = {}
    for image in images_1:
        index[image.created_at] = image

    for image in images_2:
        if image.created_at in index:
            index[image.created_at] |= image
        else:
            index[image.created_at] = image

    images = index.values()
    return gyazo.image.ImageList(images=sorted(images,
                                               key=lambda i: i.created_at,
                                               reverse=True),
                                 total_count=len(images))


def create_dest_dir(directory):
    if path.exists(directory):
        if path.isfile(directory):
            raise IOError("File already exists: " + directory)
    else:
        makedirs(directory)
    if directory[-1] != '/':
        directory += '/'
    return directory


def download_image_list(api):
    images = gyazo.ImageList(total_count=0)
    bar = Bar('List  ')
    i = 1
    while 1:
        _images = api.get_image_list(page=i, per_page=100)
        images += _images
        bar.max = _images.num_pages
        bar.next()
        if not _images.has_next_page():
            break
        i += 1
    bar.finish()
    return images


def load_old_image_list(dest_dir):
    image_file = path.join(dest_dir, 'images.json')
    if path.exists(image_file) and path.isfile(image_file):
        with open(image_file) as f:
            images = json.load(f)
        return gyazo.ImageList.from_list(images)
    return gyazo.ImageList()


def save_image_list(images, dest_dir):
    image_file = path.join(dest_dir, 'images.json')
    if path.exists(image_file) and path.isdir(image_file):
        raise IOError("Directory already exists: " + image_file)
    with open(image_file, 'w') as f:
        f.write(images.to_json(indent=2))


def download_images(images, dest_dir, num_threads=1):
    bar = Bar('Images', max=len(images))
    bar_lock = threading.Lock()

    def bar_next(_):
        with bar_lock:
            bar.next()

    def download_image_and_thumbnail(img):
        if img.thumb_filename is not None:
            thumb_file = dest_dir + 'thumbnails/' + img.thumb_filename
            if not path.exists(thumb_file):
                with open(thumb_file, 'wb') as f:
                    f.write(img.download_thumb())
        if img.filename is not None:
            image_file = dest_dir + 'images/' + img.filename
            if not path.exists(image_file):
                with open(image_file, 'wb') as f:
                        f.write(img.download())

    executor = ThreadPoolExecutor(max_workers=num_threads)
    for image in images:
        future = executor.submit(download_image_and_thumbnail, image)
        future.add_done_callback(bar_next)

    # Wait until done
    executor.shutdown(wait=True)
    bar.finish()


def export_html(images, dest_dir):
    root_dir = path.abspath(path.dirname(__file__))
    theme_dir = path.join(root_dir, 'themes/default/')
    template_env = Environment(
        loader=FileSystemLoader(theme_dir, encoding='utf-8'))
    template = template_env.get_template('index.html')
    html = template.render(images=images, now=datetime.now())

    with open(dest_dir + 'index.html', 'w') as f:
        f.write(html)

    shutil.copy(path.join(theme_dir, 'index.css'),
                path.join(dest_dir, 'index.css'))
