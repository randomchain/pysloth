from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef(
r"""
extern "Python" void update_progress(int);

void sloth(unsigned char witness[], size_t* witness_size, unsigned char outputBuffer[], char string[], int bits, int iterations);

int sloth_verification(const unsigned char witness[], size_t witness_size, const unsigned char final_hash[], const char input_string[], int bits, int iterations);
"""
)

with open('sloth.c', 'r') as c_file:
    c_str = c_file.read()

ffibuilder.set_source(
    "_sloth", c_str,
    libraries=['m', 'gmp', 'ssl', 'crypto'],
    include_dirs=[
        '/usr/local/include',
        '/usr/local/opt/openssl/include',
    ],
    library_dirs=[
        '/usr/local/lib',
        '/usr/local/opt/openssl/lib',
    ],
    extra_compile_args=['-std=c99'],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, debug=True)
