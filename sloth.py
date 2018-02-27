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

    def __init__(self, data=None, bits=1024, iterations=50000,
                 final_hash=None, witness=None):
        assert isinstance(bits, int)
        assert (bits % 512) == 0
        assert isinstance(iterations, int)
        self._data = None
        self.data = data
        self.bits = bits
        self.iterations = iterations
        self.final_hash = final_hash
        self.witness = final_hash
        self._compute_thread = None
        self._compute_lock = Lock()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, bytes):
            self._data = value
        elif not isinstance(value, str):
            value = str(value)
        self._data = value.encode('utf8')

    def compute(self):
        global progressbar
        if self._compute_thread is not None:
            return
        def run():
            out = ffi.new('char[512]')
            witness = ffi.new('char[{}]'.format(int(self.bits/4)))

            lib.sloth(witness, out, self.data, self.bits, self.iterations)
            with self._compute_lock:
                self.witness = ffi.string(witness)
                self.final_hash = ffi.string(out)
            if PROGRESS:
                progressbar.close()
            print("sloth computation done")
        if PROGRESS:
            progressbar = tqdm.tqdm(total=self.iterations)
        self._compute_thread = Thread(target=run, daemon=True)
        self._compute_thread.start()

    def wait(self, timeout=None):
        if self._compute_thread is not None:
            self._compute_thread.join(timeout=timeout)

    def verify(self):
        return lib.sloth_verification(self.witness, self.final_hash, self.data, self.bits, self.iterations) == 1


if __name__ == "__main__":
    import time
    t = time.time()
    s = Sloth("testy mctest string", iterations=50000)
    s.compute()
    s._compute_thread.join()
    print("witness:", s.witness)
    print("output hash:", s.final_hash)
    print("Time:", time.time()-t)
    t = time.time()
    print("VALID" if s.verify() else "INVALID")
    print("Time:", time.time()-t)

