from _sloth import ffi, lib

class Sloth(object):

    """Docstring for Sloth. """

    def __init__(self, data=None, bits=2048, iterations=50000):
        """TODO: to be defined1. """
        assert isinstance(bits, int)
        assert isinstance(iterations, int)
        self._data = None
        self.data = data
        self.bits = bits
        self.iterations = iterations
        self.witness = None
        self.final_hash = None

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
        out = ffi.new('char[512]')
        witness = ffi.new('char[{}]'.format(int(self.bits/4)))

        lib.sloth(witness, out, self.data, self.bits, self.iterations)
        self.witness = ffi.string(witness)
        self.final_hash = ffi.string(out)

    def verify(self):
        return lib.sloth_verification(self.witness, self.final_hash, self.data, self.bits, self.iterations) == 1


if __name__ == "__main__":
    import time
    t = time.time()
    s = Sloth("testy mctest string", iterations=50000)
    s.compute()
    print("witness:", s.witness)
    print("output hash:", s.final_hash)
    print("Time:", time.time()-t)
    t = time.time()
    print("VALID" if s.verify() else "INVALID")
    print("Time:", time.time()-t)

