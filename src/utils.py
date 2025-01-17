import const
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import os
import shutil

from datetime import datetime

def crawl_textures(root_dir):
    textures = []
    # Telusuri citra di dalam root_dir dan subdirektorinya
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.tga'):
                name = os.path.splitext(filename)[0]
                textures.append(os.path.join(dirpath, filename))
    return textures

def backup_textures(textures, backup_dir, stripped_dir):
    # Buat direktori backup jika belum ada
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Untuk setiap citra, salin ke direktori backup
    for texture in textures:
        # Strip Direktori Asal
        stripped_texture = os.path.relpath(texture, stripped_dir)
        backup_path = os.path.join(backup_dir, stripped_texture)

        # Buat direktori jika belum ada
        if not os.path.exists(os.path.dirname(backup_path)):
            os.makedirs(os.path.dirname(backup_path))

        shutil.copy(texture, backup_path)

def select_file(title):
    print(title)
    path = input("Enter the path of the image: ")
    return path

def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = const.MAX_DIM / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]

    return img

def tensor_to_pil_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

def imshow(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)

    plt.imshow(image)
    if title:
        plt.title(title)

def save_pil_image(image, filepath):
    # Overwrite image if exists
    image.save(filepath)

def log(message):
    date_format = '%Y-%m-%d %H:%M:%S'
    print(f'[{datetime.now().strftime(date_format)}] {message}')