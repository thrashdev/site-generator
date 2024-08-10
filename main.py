import os
import shutil
import re
rootdir = os.path.dirname(os.path.realpath(__file__))
pub_dir = os.path.join(rootdir, 'public')
static_dir = os.path.join(rootdir, 'static')

def clean_destination(dest_path):
    if os.path.isdir(dest_path):
        contents = os.listdir(dest_path)
        for item in contents:
            item_path = os.path.join(dest_path, item) 
            if os.path.isdir(item_path):
                print(f'Removing directory {item_path}')
                shutil.rmtree(item_path)
            else:
                print(f"Removing file {item_path}")
                os.remove(item_path)


def copy_files(src, dst, current_path=""):
    if os.path.isdir(src):
        contents = os.listdir(src)
        for item in contents:
            item_path = os.path.join(src, item) 
            dst_path = os.path.join(dst, item)
            new_path = current_path + f'/{item}'
            if os.path.isdir(item_path):
                copy_files(item_path, dst_path, new_path)
            else:
                print(f"Copying {item_path} to {dst_path}")
                shutil.copy(item_path, dst_path)


def copy_folders(src, dst, current_path=""):
    if os.path.isdir(src):
        contents = os.listdir(src)
        for item in contents:
            item_path = os.path.join(src, item) 
            dst_path = os.path.join(dst, item)
            new_path = current_path + f'/{item}'
            if os.path.isdir(item_path):
                os.mkdir(dst_path)
                print(dst_path)
                copy_folders(item_path, dst_path, new_path)

def extract_title(md_file:str):
    pat = '^# ([a-zA-Z0-9_ ]+)'
    title = re.match(pat, md_file).group(1)
    return title

def copy_to_destination(src, dst):
    copy_folders(src, dst)
    copy_files(src,dst)

def main():
    clean_destination(pub_dir)
    print("======================================")
    copy_to_destination(static_dir, pub_dir)
    with open('content/index.md', 'r') as f:
        md_file = f.read()
    title = extract_title(md_file)
    print(title)

if __name__ == '__main__':
    main()
