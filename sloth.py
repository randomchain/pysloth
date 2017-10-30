import time
from _sloth import ffi, lib

out = ffi.new('char[512]')
in_str = input('in str>> ').encode('ascii')
bits = int(input('bits >> '))
witness = ffi.new('char[{}]'.format(int(bits/4)))
iterations = int(input('iterations >> '))

s = time.time()
lib.sloth(witness, out, in_str, bits, iterations)
print("Took {:.2f}s".format(time.time() - s))
print("witness", ffi.string(witness))
print("out", ffi.string(out))


s = time.time()
v = lib.sloth_verification(witness, out, in_str, bits, iterations)
print("Took {:.2f}s".format(time.time() - s))
print("VALID" if v else "INVALID!")
