import json
import os
import csv
import sys

DEST = 'prod'

def main():
    with open(sys.argv[1]) as f:
        lines = list(csv.reader(f))
        for line in lines[1:]:
            meta = {
                'codigo': line[1],
                'nombre': line[2],
                'precio': line[5],
                'fila': 0,
                'columna': 0
            }
            categoria = line[3]

            cat_dir = os.path.join(DEST, categoria)
            if not os.path.exists(cat_dir):
                os.mkdir(cat_dir)

            prod_dir = os.path.join(cat_dir, line[1])
            if not os.path.exists(prod_dir):
                os.mkdir(prod_dir)
            with open(os.path.join(prod_dir, 'meta.txt'), 'w') as f:
                f.write(json.dumps(meta, indent=4))
                f.flush()
if __name__ == '__main__':
    main()
                




            
