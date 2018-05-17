import numpy as np
from math import sqrt, log2, ceil

def lvl(n, start, stop, remove=True):
    step_size = (stop - start) / (2**n)
    if step_size < 1:
        return np.array([]) 
    l = np.arange(0, stop - start + 1, step_size)
    l = l + start
    if remove and n > 0:
        l = np.setxor1d(l, lvl(n-1, start, stop, remove=False))
    return l

def refinement(start, stop):
    for i in range(0, int(log2(stop - start)) + 1):
        for v in lvl(i, start, stop):
            yield int(v)

import time

found = list()
stop = 2**16
for x in refinement(0, stop):
    print(x)
    time.sleep(1)
    assert x not in found, f"{x} collission found after {len(found)} numbers"
    assert x <= stop, "TOO LARGE " + str(x)
    found.append(x)

print(f"{len(found)} values")