import os

runs = os.listdir('runs')

results = []
results2 = {}

for run in runs:
    if len(os.listdir(f"runs/{run}")) == 0:
        continue
    result = open(f"runs/{run}/result.txt", 'r').readlines()
    results.append(float(result[1].replace('\n', '')))
    results2[run] = float(result[1].replace('\n', ''))


results.sort()
print(results)
print(results2)