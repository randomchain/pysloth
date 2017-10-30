from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef(
r"""
void sloth(char witness[], char outputBuffer[], char string[], int bits, int iterations);
int sloth_verification(const char witness[], const char final_hash[], const char input_string[], int bits, int iterations);
"""
)

with open('sloth.c', 'r') as c_file:
    c_str = c_file.read()

ffibuilder.set_source("_sloth", c_str, libraries=['m', 'gmp', 'ssl', 'crypto'])#, libraries_dir=['/usr/local/opt/openssl/lib'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, debug=True)
