from os import urandom
from functools import wraps
import time
import sloth

TIME_LOG = 'time.log'

BITS = (512, 512 * 2, 512 * 3, 512 * 4, 512 * 5, 512 * 6, 512 * 7, 512 * 8)
base_iteration = 500
ITERATIONS = [base_iteration * i * 4 for i in range(1, 21)]
LOOPS = 5

def timed_task(s, task):
    t_0 = time.time()
    getattr(s, task)()
    s.wait()
    return time.time() - t_0

def sloth_timing(bits, iterations, loops):
    sum_comp = 0
    sum_veri = 0
    for i in range(loops):
        print("Loop", i + 1, "of", loops)
        s = sloth.Sloth(data=urandom(64),
                        bits=bits,
                        iterations=iterations)

        sum_comp += timed_task(s, 'compute')
        assert s.final_hash is not None
        sum_veri = timed_task(s, 'verify')
        if not s.valid:
            print("NOT VALID", "\n{}\n{}".format(s.final_hash, s.witness))
            print("USED INPUT ->", s.data)
    print("Avg. time:\n\tcomputation -> {}\n\tverification -> {}".format(
        sum_comp/loops, sum_veri/loops))
    if TIME_LOG:
        with open(TIME_LOG, 'a+') as logf:
            print(",{},{}".format(sum_comp/loops, sum_veri/loops), file=logf)


def sloth_timing_configurations(log_file):
    global TIME_LOG
    TIME_LOG = log_file
    if TIME_LOG:
        with open(TIME_LOG, 'w') as logf:
            print("BITS,ITERATIONS,COMPUTATION,VERIFICATION", file=logf)
    for b in BITS:
        for i in ITERATIONS:
            print(b, i)
            if TIME_LOG:
                with open(TIME_LOG, 'a+') as logf:
                    print(str(b) + "," + str(i), end='', file=logf)
            sloth_timing(b, i, LOOPS)


if __name__ == "__main__":
    import sys
    sloth_timing_configurations(sys.argv[1] if len(sys.argv) > 1 else None)

