import xml.etree.ElementTree as ET
import re
import csv
import sys
import os
import tkinter as tk
from tkinter import filedialog as fd

def read_xrdml(file):
    """
    Takes a file path to an xrdml-file as argument and returns a dict with 
    2-theta as keys and intensity counts as values
    """
    if not os.path.splitext(file)[1] == '.xrdml':
        raise TypeError('The file is not an xrdml file.')
    f = ET.parse(file)
    root = f.getroot()

    # Check for namespace
    namespace_check = re.match(r'\{.*\}', root.tag)
    namespace = '' if namespace_check is None else namespace_check.group(0)
    
    # Get the scan section
    scan = root.find(f'.//{namespace}scan')
    # Extract the data
    intensities = scan.find(f'.//{namespace}intensities').text.split()
    
    # 2Theta data
    axis = scan.find(f'.//{namespace}positions[@axis="2Theta"]')
    
    startPosition = float(axis.find(f'.//{namespace}startPosition').text)
    endPosition = float(axis.find(f'.//{namespace}endPosition').text)
    step = (endPosition - startPosition) / (len(intensities) - 1)

    tt = [startPosition + n*step for n in range(len(intensities))]

    return {'2-Theta': tt, 'Intensities': intensities}

def xrdml2csv(f):
    if not os.path.exists(f):
        raise FileNotFoundError
    
    xrdml = read_xrdml(f)
    tt = xrdml['2-Theta']
    intensities = xrdml['Intensities']
    
    fname = os.path.splitext(f)[0]

    with open(f'{fname}.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=';', lineterminator='\n')
        csv_writer.writerow(['2-Theta', 'Intensities'])
        for i, _ in enumerate(tt):
            csv_writer.writerow([tt[i], intensities[i]])
    return
        


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Select a file to convert...')
        tk_root = tk.Tk()
        tk_root.withdraw()

        file = fd.askopenfilename()
        path = os.path.split(file)[0]
        os.chdir(path)
    else:
        file = sys.argv[1]
    print(f'Converting "{file}" to csv...')
    xrdml2csv(file)
    input('Done! Press any key to exit...')