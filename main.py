import os
import shutil
import re
rootdir = os.path.dirname(os.path.realpath(__file__))
pub_dir = os.path.join(rootdir, 'public')
static_dir = os.path.join(rootdir, 'static')

# def delete_recursively(item):
#     if os.path.isdir(item):
#         contents = os.listdir(item)
#         for i in contents:
#             delete_recursively(i)
#     else:
#         os.remove(item)

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

# def list_files(current_filetree, current_path=""):
#     paths = []
#     for filename in current_filetree:
#         value = current_filetree[filename]
#         full_path = current_path + "/" + filename
#         if value is None:
#             paths.append(full_path)
#         else:
#             paths.extend(list_files(current_filetree[filename], full_path))
#
#     return paths

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

def copy_to_destination(src, dst):
    copy_folders(src, dst)
    copy_files(src,dst)

if __name__ == '__main__':
    clean_destination(pub_dir)
    # shutil.rmtree(pub_dir)
    print("======================================")
    copy_to_destination(static_dir, pub_dir)
    # copy_files(static_dir, pub_dir)
    # copy_folders(static_dir, pub_dir)
