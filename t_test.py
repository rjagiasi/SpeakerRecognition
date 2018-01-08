# Gives Student's T Test among itself and other users
# python feature_extract.py | python median_deviation.py
# This file is useless!

import sys
import numpy as np
from scipy.stats import ttest_ind, ttest_ind_from_stats
from scipy.special import stdtr
import json

# no_of_samples = 40
no_of_features = 20
# no_of_files_for_each_person = 2

data = sys.stdin.readlines()
dataset = {}
for line in data:
	row = line.strip().split(",")
	dataset.setdefault(row[-1], []).append(row[:-1])
# print(dataset)
t_test_result = {}
for x in range(0, no_of_features):
	for person, mfcc in dataset.items():
		row = {}
		mfccnpa = np.asarray(mfcc, dtype=np.float32)
		for person2, mfcc2 in dataset.items():
			mfcc2npa = np.asarray(mfcc2, dtype=np.float32)
			t, p = ttest_ind(mfccnpa.transpose()[x], mfcc2npa.transpose()[x], equal_var=False)
			row.setdefault(person2, []).append(t)
			row.setdefault(person2, []).append(p)
		t_test_result.setdefault(person, []).append(row)
		
# print(t_test_result)
json_eq = json.dumps({'t_test_result': t_test_result })
parsed = json.loads(json_eq)
print(json.dumps(parsed, indent=2, sort_keys=True))