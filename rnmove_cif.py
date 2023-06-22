import os
import re
import sys
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename as openfn
from tkinter.filedialog import askdirectory as askdir
DATA_LABELS = ["_chemical_formula_structural",
               "_chemical_name_systematic",
               "_chemical_formula_sum"]

CIF_PATH = r"F:\OneDrive - Stockholm University\Documents\.PhD\Quasicrystals\CIF Files"

def get_formula(cif_file: str):
    # Parse file
    fname = os.path.basename(cif_file)
    with open(cif_file, 'r') as f:
        for line in f.readlines():
            for label in DATA_LABELS:
                if label in line:
                    p = re.compile("(?<=\w ).+(?=\n?)")
                    m = p.search(line)
                    new_name = m.group(0)
                    break
    
    return f'{new_name} {fname}'

def copy_with_new_name(cif_file, new_path):
    new_fname = get_formula(cif_file)
    new_file = os.path.join(new_path, new_fname)
    if os.path.exists(new_file):
        overwrite_flag = input(f"File {new_file} exists.\nWould you like to overwrite? (Y/N): ")
        while True:
            if overwrite_flag.lower() in ('y', 'ye', 'yes', 'yup', 'do it', 'confirm', 'go for it'):
                shutil.copy2(cif_file, new_file)
                break
            elif overwrite_flag.lower() in ('n', 'no', 'nope', 'don\'t', 'stop', 'abort', 'negative'):
                break
            else: print("I don't understand what you want me to do.")
    else:
        shutil.copy2(cif_file, new_file)

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    try:
        src = sys.argv[1]
    except IndexError:
        print("Please specify CIF-file to move")
        src = openfn(defaultextension='cif')
    try:
        dst = sys.argv[2]
    except IndexError:
        print(f"Please specify the destination of {src}") 
        dst = askdir(initialdir='%USERPROFILE%')

    copy_with_new_name(src, dst)
    exit() 