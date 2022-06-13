from os.path import exists
from turtle_fis import FIS

if __name__ == '__main__':
    if not exists("surface_out1.csv"):
        FIS("surface_out1.csv", 1)
    if not exists("surface_out2.csv"):
        FIS("surface_out2.csv", 2) 