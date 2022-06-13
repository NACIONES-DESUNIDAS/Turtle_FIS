import numpy as np
import csv
import skfuzzy as sk
from matplotlib import pyplot as plt

class FIS():
    def __init__(self, file_path, out_number):
        self.file_path = file_path
        self.out_number = out_number
        self.setInputIntervals()
        self.makeCSV()

    def setInputIntervals(self):
        self.in1_u = np.arange(-180, 180, 1)
        self.in1_1 = sk.gbellmf(self.in1_u, 45, 2, -180)
        self.in1_2 = sk.gbellmf(self.in1_u, 45, 2, -90)
        self.in1_3 = sk.gbellmf(self.in1_u, 45, 2, 0)
        self.in1_4 = sk.gbellmf(self.in1_u, 45, 2, 90)
        self.in1_5 = sk.gbellmf(self.in1_u, 45, 2, 180)
        self.in1_l = [self.in1_1, self.in1_2,self.in1_3,self.in1_4,self.in1_5]
        self.in2_u = np.arange(0.0, 16.0, 0.1)
        self.in2_1 = sk.gbellmf(self.in2_u, 2, 2, 0.0)
        self.in2_2 = sk.gbellmf(self.in2_u, 2, 2, 4.0)
        self.in2_3 = sk.gbellmf(self.in2_u, 2, 2, 8.0)
        self.in2_4 = sk.gbellmf(self.in2_u, 2, 2, 12.0)
        self.in2_5 = sk.gbellmf(self.in2_u, 2, 2, 16.0)
        self.in2_l = [self.in2_1, self.in2_2,self.in2_3,self.in2_4,self.in2_5]
        if self.out_number == 1:
            self.out_u = np.arange(0, 4, 0.1)
            self.out_1 = sk.trimf(self.out_u, [0, 0, 1.0])
            self.out_2 = sk.trimf(self.out_u, [0, 1.0, 2.0])
            self.out_3 = sk.trimf(self.out_u, [1.0, 2.0, 3.0])
            self.out_4 = sk.trimf(self.out_u, [2.0, 3.0, 4.0])
            self.out_5 = sk.trimf(self.out_u, [3.0, 4.0, 4.0])
        elif self.out_number == 2:
            self.out_u = np.arange(-2, 2, 0.1)
            self.out_1 = sk.trimf(self.out_u, [-2.0, -2.0, -1.0])
            self.out_2 = sk.trimf(self.out_u, [-2.0, -1.0, 0])
            self.out_3 = sk.trimf(self.out_u, [-1.0, 0, 1.0])
            self.out_4 = sk.trimf(self.out_u, [0, 1.0, 2.0])
            self.out_5 = sk.trimf(self.out_u, [1.0, 2.0, 2.0])

    def minimums(self, x, y):
        size = 5, 5
        self.rule_mins = np.zeros(size)
        for i in range(5):
            for j in range(5):
                self.rule_mins[i][j] = min(self.in1_l[i][x], self.in2_l[j][y])

    def maximums(self):
        if self.out_number == 1:
            self.out_m1 = max(self.rule_mins[0][0], self.rule_mins[0][1], self.rule_mins[0][2], self.rule_mins[0][3], self.rule_mins[0][4], self.rule_mins[1][0], self.rule_mins[2][0], self.rule_mins[3][0], self.rule_mins[4][0], self.rule_mins[4][1], self.rule_mins[4][2], self.rule_mins[4][3], self.rule_mins[4][4])
            self.out_m2 = max(self.rule_mins[1][1], self.rule_mins[1][2], self.rule_mins[3][1], self.rule_mins[3][2])
            self.out_m3 = max(self.rule_mins[1][3], self.rule_mins[1][4], self.rule_mins[3][3], self.rule_mins[3][4])
            self.out_m4 = max(self.rule_mins[2][1], self.rule_mins[2][2])
            self.out_m5 = max(self.rule_mins[2][3], self.rule_mins[2][4])
        elif self.out_number == 2:
            self.out_m1 = max(self.rule_mins[3][0], self.rule_mins[3][1], self.rule_mins[4][0], self.rule_mins[4][1], self.rule_mins[4][2])
            self.out_m2 = max(self.rule_mins[3][2], self.rule_mins[3][3], self.rule_mins[3][4], self.rule_mins[4][3], self.rule_mins[4][4])
            self.out_m3 = max(self.rule_mins[2][0], self.rule_mins[2][1], self.rule_mins[2][2], self.rule_mins[2][3], self.rule_mins[2][4])
            self.out_m4 = max(self.rule_mins[0][3], self.rule_mins[0][4], self.rule_mins[1][2], self.rule_mins[1][3], self.rule_mins[1][4])
            self.out_m5 = max(self.rule_mins[0][0], self.rule_mins[0][1], self.rule_mins[0][2], self.rule_mins[1][0], self.rule_mins[1][1])

    def copyOutputs(self):
        self.out_1_c = self.out_1.copy()
        self.out_2_c = self.out_2.copy()
        self.out_3_c = self.out_3.copy()
        self.out_4_c = self.out_4.copy()
        self.out_5_c = self.out_5.copy()
        self.out_1_c[self.out_1_c > self.out_m1] = self.out_m1
        self.out_2_c[self.out_2_c > self.out_m2] = self.out_m2
        self.out_3_c[self.out_3_c > self.out_m3] = self.out_m3
        self.out_4_c[self.out_4_c > self.out_m4] = self.out_m4
        self.out_5_c[self.out_5_c > self.out_m5] = self.out_m5
    
    def maxValue(self, i):
        value = max(self.out_1_c[i], self.out_2_c[i], self.out_3_c[i], self.out_4_c[i], self.out_5_c[i])
        return value

    def fis(self, x, y):
        self.minimums(x, y)
        self.maximums()
        self.copyOutputs()
        arr = list()        
        mu1 = 0.0
        mu2 = 0.0
        for i in range(0, len(self.out_u)):
            arr.append(self.maxValue(i))
        for i in range(0, len(arr)):
            mu1 += arr[i] * (i)
            mu2 += arr[i]
        z = (mu1 / mu2) / 40.0
        return z

    def makeCSV(self):
        count = 1
        size = len(self.in1_u),len(self.in2_u)
        mat_z = np.zeros(size)
        for j in range(len(self.in2_u)):
            for i in range(len(self.in1_u)):
                z = self.fis(i, j)
                mat_z[i][j] = z
                print(count)
                count += 1
        with open(self.file_path, "w") as f:
            wr = csv.writer(f)
            wr.writerows(mat_z)

        self.in1_u = np.reshape(self.in1_u, (len(self.in1_u), 1))
        self.in2_u = np.reshape(self.in2_u, (1, len(self.in2_u)))

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_surface(self.in1_u, self.in2_u, mat_z, cmap= 'hot')
        plt.show()