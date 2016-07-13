# ./prod
#      ./categoria_1
#           ./producto1 
#           ./producto2
#           ./producto3
#      ./categoria_2
#           ./producto4 
#           ./producto5
#           ./producto6

import sys
import json
import jinja2
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import os
import shutil

IGNORE = (
    './.git',
    './deploy'
)

DEST = './deploy'
PROD_DIR = './prod'
PROD_DETAIL_PAGE = './product_detail_template.html'
PROD_LIST_PAGE = './product_list_template.html'
env = Environment()
env.loader = FileSystemLoader('.')


class ProductPage(object):

    def __init__(self, meta, directory, cat, descripcion):
        self.meta = meta
        self.directory = directory
        self.cat = cat 
        self.descripcion = descripcion


def get_product_by_cat(category):
    for x in os.listdir(os.path.join(PROD_DIR, category)):
        prod_dir = os.path.join(PROD_DIR, category, x)
        with open(os.path.join(prod_dir, 'descripcion.txt')) as fdesc:
            desc = fdesc.read()
        with open(os.path.join(prod_dir, 'meta.txt')) as fmeta:
            meta = json.loads(fmeta.read())
        yield ProductPage(meta=meta, cat=category, directory=prod_dir, descripcion=desc)


def generate_prod_list_page(cat, prod):
    temp = env.get_template(PROD_LIST_PAGE)
    with open(os.path.join(DEST, cat + '.html'), 'w') as f:
        f.write(temp.render(prod=prod, cat=cat))
        f.flush()


def generate_prod_page(prod):
    temp = env.get_template(PROD_DETAIL_PAGE)
    with open(os.path.join(DEST, prod.meta['codigo'] + '.html'), 'w') as f:
        f.write(temp.render(prod=prod))


def main():
    for cat in os.listdir(PROD_DIR):
        prod = list(get_product_by_cat(cat))
        generate_prod_list_page(cat, prod)
        print 'generado categoria', cat
        for p in prod:
            generate_prod_page(p)
            print 'generado producto', p
        print 'copiando imagenes...'
        shutil.rmtree(os.path.join(DEST, PROD_DIR))
        shutil.copytree(PROD_DIR, os.path.join(DEST, PROD_DIR))


if __name__ == '__main__':
    main()
