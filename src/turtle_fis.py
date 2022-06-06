import numpy as np
import csv

class FIS():
    def __init__(self):
        pass

    def fis(self, x, y):
        pass

    def makeCSV(self):
        size = len(self.x),len(self.y)
        mat_z = np.zeros(size)
        for j in range(len(y)):
            for i in range(len(x)):
                z = self.fis(x[i],y[j])
                mat_z[i,j] = z
                
        with open("surface.csv", "w") as f:
            wr = csv.writer(f)
            wr.writerows(mat_z)