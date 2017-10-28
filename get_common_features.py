import sys
import numpy as np
from statsmodels import robust

male = 100
data = sys.stdin.readlines()
dataset = {}
for line in data:
	row = line.strip().split(",")
	dataset.setdefault(row[-1], []).append(row[:-1])

mad_median = {}

for person, features in dataset.items():
	npa = np.asarray(features, dtype=np.float32)
	mad_values = robust.scale.mad(npa.transpose(), axis=1)	
	median_values = np.median(npa,axis=0)
	mad_median.setdefault(person, []).append(median_values.tolist())
	mad_median.setdefault(person, []).append(mad_values.tolist())

percentage_deviation = {}
for person, mad_median_values in mad_median.items():
	for x in range(0, len(mad_median_values[0])):
		percentage_deviation.setdefault(person, []).append((mad_median_values[1][x]/mad_median_values[0][x])*100)

print(percentage_deviation)