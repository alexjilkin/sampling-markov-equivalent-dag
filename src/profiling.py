import numpy as np

records = {}

def record(name: str, time: float):
    if (name not in records.keys()):
        records[name] = []
        
    records[name].append(time)

def print_profiling():
    for (name, record) in records.items():
        record = np.array(record)
        print(f'{name}: {record.sum():3f}, mean={record.mean():.5f}, max={record.max():.3f}')
