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
                 final_hash=None, witness=None, threading=True):
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
        self.threading = threading
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
            out = ffi.new('unsigned char[64]')
            witness = ffi.new('unsigned char[{}]'.format(int(self.bits / 8)))
            witness_size = ffi.new('size_t*')
            lib.sloth(
                witness,
                witness_size,
                out,
                self.data,
                self.bits,
                self.iterations
            )
            witness_size = witness_size[0]
            with self._lock:
                self.witness = bytes(ffi.buffer(witness))
                self.final_hash = bytes(ffi.buffer(out))
        self._run(task=compute_task)

    def verify(self):
        def verify_task():
            verification = lib.sloth_verification(self.witness, self.final_hash, self.data, self.bits, self.iterations)
            with self._lock:
                self.valid = verification == 1
        self._run(task=verify_task)

    def _run(self, task):
        global progressbar
        if self.threading:
            self.wait()
        if PROGRESS:
            progressbar = tqdm.tqdm(total=self.iterations)
        def wrapped_task():
            task()
            if PROGRESS:
                progressbar.close()
        if self.threading:
            self._thread = Thread(target=wrapped_task, daemon=True)
            self._thread.start()
        else:
            wrapped_task()

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
    s = Sloth(sloth_art, bits=1024, iterations=100, threading=False)
    print("Bits: {}\tIterations: {}".format(s.bits, s.iterations))
    t = time.time()
    print("{:=^50}".format(" COMPUTE "))
    s.compute()
    print("Witness:", s.witness)
    print("Output data:", s.final_hash)
    print("Time:", timedelta(seconds=time.time()-t))
    print("{:=^50}".format(" VERIFY "))
    t = time.time()
    s.verify()
    print("Verify:", "VALID" if s.valid else "INVALID", "sloth")
    print("Time:", timedelta(seconds=time.time()-t))

