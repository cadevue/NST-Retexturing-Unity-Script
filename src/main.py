from utils import *
from nst import stylize
import argparse

UNITY_PROJ_BASE_DIR = './../..'
BACKUP_DIR = 'backup'

def retexture(texture_paths, style_path):
    log('Retexturing...')

    # Load style image
    log('Loading style image...')
    style_image = load_image(style_path)

    # Stylize masing-masing texture
    for texture_path in texture_paths:
        log(f'Stylizing {os.path.basename(texture_path)}')

        log('Loading texture image...')
        texture = load_image(texture_path)

        log('Stylizing...')
        result = stylize(texture, style_image)

        # Overwrite hasil stylize ke texture path
        log('Saving result...')
        save_pil_image(result, texture_path)

    log('Retexturing complete!')

def revert_textures(backup_dir):
    log('Reverting textures...')

    # Load backup textures
    backup_textures = crawl_textures(backup_dir)

    # Restore backup textures
    for backup_texture in backup_textures:
        stripped_backup_texture = os.path.relpath(backup_texture, backup_dir)
        texture_path = os.path.join(UNITY_PROJ_BASE_DIR, stripped_backup_texture)
        shutil.copy(backup_texture, texture_path)

    log('Reverting complete!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retexture Unity Project')
    parser.add_argument('--revert', action='store_true', help='Revert the project to original textures')

    args = parser.parse_args()

    if args.revert:
        revert_textures(BACKUP_DIR)
    else:
        log('Crawling Texture Paths...')
        texture_paths = crawl_textures(UNITY_PROJ_BASE_DIR)

        log('Backing up textures...')
        backup_textures(texture_paths, BACKUP_DIR, UNITY_PROJ_BASE_DIR)

        log('Selecting Style Image')
        style_path = select_file('Select style image')

        retexture(texture_paths, style_path)