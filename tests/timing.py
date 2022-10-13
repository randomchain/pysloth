import time
from math import log2
from os import urandom

import click
import numpy as np

import sloth

TIME_LOG = "time.log"
LOOPS = 0
VERIFICATION_LOOPS = 5


def lvl(n, start, stop, remove=True):
    step_size = (stop - start) / (2**n)
    if step_size < 1:
        return np.array([])
    l = np.arange(0, stop - start + 1, step_size)
    l = l + start
    if remove and n > 0:
        l = np.setxor1d(l, lvl(n - 1, start, stop, remove=False))
    return l


def iterations(start, stop):
    for i in range(0, int(log2(stop - start)) + 1):
        for v in lvl(i, start, stop):
            yield int(v)


def timed_task(s, task):
    t_0 = time.perf_counter()
    getattr(s, task)()
    s.wait()
    return time.perf_counter() - t_0


def sloth_timing(bits, iterations):
    sum_comp = 0
    sum_veri = 0
    for i in range(LOOPS):
        print("Loop", i + 1, "of", LOOPS)
        s = sloth.Sloth(data=urandom(64), bits=bits, iterations=iterations)

        sum_comp += timed_task(s, "compute")
        assert s.final_hash is not None
        for _ in range(VERIFICATION_LOOPS):
            sum_veri += timed_task(s, "verify")
        if not s.valid:
            print("NOT VALID", "\n{}\n{}".format(s.final_hash, s.witness))
            print("USED INPUT ->", s.data)
    avg_comp = sum_comp / LOOPS
    avg_veri = sum_veri / (LOOPS + VERIFICATION_LOOPS)
    print(
        "Avg. time:\n\tcomputation -> {}\n\tverification -> {}".format(
            avg_comp, avg_veri
        )
    )
    if TIME_LOG:
        with open(TIME_LOG, "a+") as logf:
            print(",{},{}".format(avg_comp, avg_veri), file=logf)


def sloth_timing_configurations(start, stop, bits, log_file):
    global TIME_LOG
    TIME_LOG = log_file
    if TIME_LOG:
        with open(TIME_LOG, "w") as logf:
            print("BITS,ITERATIONS,COMPUTATION,VERIFICATION", file=logf)
    for i in iterations(start, stop):
        i = i * 10
        for b in bits:
            print(b, i)
            if TIME_LOG:
                with open(TIME_LOG, "a+") as logf:
                    print(str(b) + "," + str(i), end="", file=logf)
            sloth_timing(b, i)


@click.command()
@click.option("-i", type=int)
@click.option("-b", type=int, multiple=True)
@click.option("-l", type=int, default=5)
@click.option("-o", default="sloth.csv")
def main(i, b, l, o):
    global LOOPS
    LOOPS = l
    sloth_timing_configurations(0, 2**i, b, o)


if __name__ == "__main__":
    main()
