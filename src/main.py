import os
from os.path import isdir
import shutil
import re

from textnode import markdown_to_html

rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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
    pat = '^# (.+)'
    matches = re.match(pat, md_file) 
    title = matches.group(1)
    return title

def copy_to_destination(src, dst):
    copy_folders(src, dst)
    copy_files(src,dst)

def generate_page(from_path, template_path, dest_path):
    if os.path.isdir(from_path):
        return
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        md_file = f.read()
    with open(template_path, 'r') as f:
        html_template = f.read()
    title = extract_title(md_file)
    print(title)
    html = markdown_to_html(md_file)
    final_html = html_template.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html)
    filename = 'index.html'
    page_filepath = os.path.join(dest_path, filename)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    with open(page_filepath, 'w') as f:
        f.write(final_html)
    print(f"Succesfully generated {filename} at {page_filepath}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    for item in content:
        item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        if os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_item_path)
        generate_page(item_path, template_path, dest_dir_path)

        
def main():
    clean_destination(pub_dir)
    print("======================================")
    copy_to_destination(static_dir, pub_dir)
    index_md_path = os.path.join(rootdir, 'content/index.md')
    content_path = os.path.join(rootdir, 'content')
    template_path = os.path.join(rootdir, 'template.html')
    # generate_page(index_md_path, template_path, pub_dir)
    generate_pages_recursive(content_path, template_path, static_dir)



if __name__ == '__main__':
    main()
