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

def clean_destination(dest_path, current_path=""):
    if os.path.isdir(dest_path):
        contents = os.listdir(dest_path)
        for item in contents:
            item_path = os.path.join(dest_path, item) 
            if os.path.isdir(item_path):
                clean_destination(item_path, item)
            else:
                print(item_path)
        print(dest_path)
    else:
        p = os.path.join(dest_path, current_path)
        print(p)

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
            if os.path.isdir(item_path):
                copy_files(item_path, dst, item)
            else:
                print(f"Copying {item_path} to {dst_path}")
        print(f"Creating {src} in {dst}")
    else:
        s = os.path.join(src, current_path)
        d = os.path.join(src, current_path)
        print(f"Copying {s} to {d}")


def copy_folders(src, dst, current_path=""):
    if os.path.isdir(src):
        folder_name = os.path.basename(os.path.normpath(src))
        # dest_path = os.path.join(dst,current_path)
        # dest_path = os.path.join(dest_path, folder_name)
        # print(dest_path)
        contents = os.listdir(src)
        for item in contents:
            item_path = os.path.join(src, item) 
            dst_path = os.path.join(dst, item)
            res = re.search('static', str(src))
            folder_name = os.path.basename(os.path.normpath(src))
            spath = item_path[res.end():].strip('/')
            dest_path = os.path.join(dst, spath)
            # if os.path.isdir(dest_path):
            if os.path.isdir(item_path):
                # copy_files(item_path, dst, item)
                print(dest_path)
                copy_folders(item_path, dst_path, spath)

def copy_to_destination(src, dst):
    copy_folders(src, dst)
    # copy_files(src,dst)

if __name__ == '__main__':
    # print(pub_dir)
    # clean_destination(pub_dir)
    print("======================================")
    # copy_files(static_dir, pub_dir)
    copy_folders(static_dir, pub_dir)
