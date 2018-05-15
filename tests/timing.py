from functools import wraps
import time
import sloth

TIME_LOG = 'time.log'

INPUT = b'/\x97s\xb8i\xd1\xa5\x84\xcf\x16\x7f\xcc\xc0\xae\xbb\x05!\xf1\x19\x17P\x82\x05\xef\xfcu\x87\x1c"\x10\xaa\xddD\x01\xf4\xcd\xbe\xcf\x87\x05A#\xf6\xaa\xd0Y\xe3\\\xf7\xa8\x08p\x8f\xd8\xfdEi\xdc\xda\xa1l1\x1cE'

BITS = (512, 512 * 2, 512 * 3, 512 * 4, 512 * 5, 512 * 6, 512 * 7, 512 * 8)
ITERATIONS = (500, 5000, 10000, 25000, 50000, 75000)

def timed_task(s, task):
    t_0 = time.time()
    getattr(s, task)()
    s.wait()
    t = time.time() - t_0
    print(t)
    if TIME_LOG:
        with open(TIME_LOG, 'a+') as logf:
            print("," + str(t), end='', file=logf)


def sloth_timing(bits, iterations):
    s = sloth.Sloth(data=INPUT,
                    bits=bits,
                    iterations=iterations)

    timed_task(s, 'compute')
    assert s.final_hash is not None
    timed_task(s, 'verify')
    assert s.valid, "{}\n{}".format(s.final_hash, s.witness)


def sloth_timing_configurations(log_file):
    global TIME_LOG
    TIME_LOG = log_file
    if TIME_LOG:
        with open(TIME_LOG, 'w') as logf:
            print("BITS,ITERATIONS,COMPUTATION,VERIFICATION", end='', file=logf)
    for b in BITS:
        for i in ITERATIONS:
            print(b, i)
            if TIME_LOG:
                with open(TIME_LOG, 'a+') as logf:
                    print("\n" + str(b) + "," + str(i), end='', file=logf)
            sloth_timing(b, i)


if __name__ == "__main__":
    import sys
    sloth_timing_configurations(sys.argv[1] if len(sys.argv) > 1 else None)

