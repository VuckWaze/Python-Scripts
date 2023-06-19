from re import S
import numpy as np
import xrayutilities.io as xu
import pandas as pd
from glob import glob


def convert_all(folder):
    folder = ''
    files = glob(folder+'/**/*.xrdml') 
    for f in files:
        x, y = xu.getxrdml_scan(f)
        try:
            df = pd.DataFrame({'2-Theta': x, 'Intensities': y})
        except ValueError:
            x, y = np.average(x, axis=0), np.average(y, axis=0)
        df.to_csv(f[:-5]+'.xy', header=True, )

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        try:
            convert_all(folder=sys.argv[1])
        except:
            print("Something went wrong...")
    if len(sys.argv) == 1:
        raise Exception('No folder path was input')
    