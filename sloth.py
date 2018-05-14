from binascii import a2b_hex, b2a_hex
from threading import Thread, Lock
import tqdm
from _sloth import ffi, lib

PROGRESS = True
progressbar = None

@ffi.def_extern()
def update_progress(delta_iterations):
    if progressbar is not None:
        progressbar.update(delta_iterations)

class Sloth(object):
    """
    Object wrapper for the sloth c library.

    :param data: String or bytes of input data
        will be converted to bytes if sting
    :param bits: Number of bits to use for prime numbers in sloth
        Must be a multiple of 512
    :param iterations: Number of square root permutations in sloth
        Most significant parameter in delay function
    :param final_hash: Sloth output hash as bytes
        Can be used for verification
    :param witness: Sloth output witness as bytes
        Can be used for verification
    """

    def __init__(self, data=None, bits=2048, iterations=50000,
                 final_hash=None, witness=None):
        assert isinstance(bits, int)
        assert (bits % 512) == 0
        assert isinstance(iterations, int)
        self._data = None
        if data is not None:
            self.data = data
        self.bits = bits
        self.iterations = iterations
        self.final_hash = final_hash
        self.witness = witness
        self.valid = None
        self._thread = None
        self._lock = Lock()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, bytes):
            self._data = value
            return
        elif not isinstance(value, str):
            value = str(value)
        self._data = value.encode('utf8')

    def compute(self):
        def compute_task():
            out = ffi.new('char[256]')
            witness = ffi.new('char[{}]'.format(int(self.bits/2)))

            lib.sloth(
                witness,
                out,
                self.data,
                self.bits,
                self.iterations
            )
            with self._lock:
                raw_witness = ffi.string(ffi.cast("char*", witness))
                self.witness = a2b_hex(raw_witness if len(raw_witness) % 2 == 0 else b'0' + raw_witness)
                self.final_hash = a2b_hex(ffi.string(out))
        self._run(task=compute_task)

    def verify(self):
        def verify_task():
            verification = lib.sloth_verification(b2a_hex(self.witness), b2a_hex(self.final_hash), self.data, self.bits, self.iterations)
            with self._lock:
                self.valid = verification == 1
        self._run(task=verify_task)

    def _run(self, task):
        global progressbar
        self.wait()
        if PROGRESS:
            progressbar = tqdm.tqdm(total=self.iterations)
        def wrapped_task():
            task()
            if PROGRESS:
                progressbar.close()
        self._thread = Thread(target=wrapped_task, daemon=True)
        self._thread.start()

    def wait(self, timeout=None):
        if self._thread is not None:
            self._thread.join(timeout=timeout)


if __name__ == "__main__":
    sloth_art = """
      `""==,,__
        `"==..__"=..__ _    _..-==""_
             .-,`"=/ /\ \""/_)==""``
            ( (    | | | \/ |
             \ '.  |  \;  \ /
              |  \ |   |   ||
         ,-._.'  |_|   |   ||
        .\_/\     -'   ;   Y
       |  `  |        /    |-.
       '. __/_    _.-'     /'
              `'-.._____.-'
"""
    print(sloth_art)
    import time
    from datetime import timedelta
    s = Sloth(sloth_art, iterations=500)
    print("Bits: {}\tIterations: {}".format(s.bits, s.iterations))
    t = time.time()
    print("{:=^50}".format(" COMPUTE "))
    s.compute()
    s.wait()
    print("Witness:", s.witness)
    print("Output data:", s.final_hash)
    print("Time:", timedelta(seconds=time.time()-t))
    print("{:=^50}".format(" VERIFY "))
    t = time.time()
    s.verify()
    s.wait()
    print("Verify:", "VALID" if s.valid else "INVALID", "sloth")
    print("Time:", timedelta(seconds=time.time()-t))

