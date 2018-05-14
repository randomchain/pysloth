import sloth


class ValidSloth:
    INPUT = b'/\x97s\xb8i\xd1\xa5\x84\xcf\x16\x7f\xcc\xc0\xae\xbb\x05!\xf1\x19\x17P\x82\x05\xef\xfcu\x87\x1c"\x10\xaa\xddD\x01\xf4\xcd\xbe\xcf\x87\x05A#\xf6\xaa\xd0Y\xe3\\\xf7\xa8\x08p\x8f\xd8\xfdEi\xdc\xda\xa1l1\x1cE'

    BITS = 2048
    ITERATIONS = 5000

    OUTPUT = b'\x06\x97\x17!\x91w\xa1f\xa1?\x8f\xee\xe3h\xd1>\x1f\x8b\x91Z\xfd\\\xb6t\xc4\xfa\x07\xa1\xca\xae\x190\x9cx\x12\xfd\x84\xd9\x1e\xdd2\x01\xf9\xb6\x0e\xb9\x1a\xba\xd9\t_U\x89@]\xf0\xa43C\x08i\x1bd\xc9'
    WITNESS = b'5+\xa7m\xeb7\xdb\xf5(\xfb\x92\\d\xd3\xc0V(\x9c\xb1\xb0y\x96>\xf3 \xf5b|\x02\x8d\xbf\x8a\xc9\x1f\xff\xa1g\x88\xe7\x1d\x89\x91\x0c\xfbW\x07n:\x8f\xb7\x11\n\xa8\xc8\xc9\xe5\x9d\xa1\xc5\xb4aH\xd2KJ~A\x8e(\x05\xdc\x9bs`\xa1\xd8\xe9\x0c\xe9\x04\xee\xd7\xa5k\xc2\xde\x8e\xe1\x1d,\xcb\x1e\xd2P\x92XS\x01x\xc9K4\x8bI\xe1qhbR\x97T/S\xeexCYM\x8b\xd2\r\x1a,\xd8\xe1B{d\x8c\t?\xef\xd7{\x98.\xbc|c\x02S\x00\x1b\xb7\x0e\xa8Q\x1bj\x12\x14\xd1l\x0e\xedM\xca\xc0\x15\xcd\xcd\xcf\x94L\x80x\xcf/\xae\x02A\x0c\xa8\xf7u\x1d\x0cDD\x92\xf6\x811W\xbd5#\xc2\xe6\x7fH\xcb\xc1k\xe3\xbd\x84\x8f\xda\xb0\xbf\xbbv\x8e\xf4\x16\xfcM\x9e\x16^\xd7\xb3\xa7#G\xce\x7f\xef \x99\x0e\x87:\xd4v\xc0<\x90\xac(\xdc*\xb81_\xc5\x93\xe4\xb7\xbc\x11\x98\xd6L\xeb\x85\x08\x86\xec\x1e\x14\xe6M\xa7\x1d'


class InvalidInput(ValidSloth):
    INPUT = b'/\x99s\xb8i\xd1\xa5\x84\xcf\x16\x7f\xcc\xc0\xae\xbb\x05!\xf1\x19\x17P\x82\x05\xef\xfcu\x87\x1c"\x10\xaa\xddD\x01\xf4\xcd\xbe\xcf\x87\x05A#\xf6\xaa\xd0Y\xe3\\\xf7\xa8\x08p\x8f\xd8\xfdEi\xdc\xda\xa1l1\x1cE'


class InvalidOutput(ValidSloth):
    OUTPUT = b'meme'


class InvalidWitness(ValidSloth):
    WITNESS = b'5+\xa7m\xec7\xdb\xf5(\xfb\x92\\d\xd3\xc0V(\x9c\xb1\xb0y\x96>\xf3 \xf5b|\x02\x8d\xbf\x8a\xc9\x1f\xff\xa1g\x88\xe7\x1d\x89\x91\x0c\xfbW\x07n:\x8f\xb7\x11\n\xa8\xc8\xc9\xe5\x9d\xa1\xc5\xb4aH\xd2KJ~A\x8e(\x05\xdc\x9bs`\xa1\xd8\xe9\x0c\xe9\x04\xee\xd7\xa5k\xc2\xde\x8e\xe1\x1d,\xcb\x1e\xd2P\x92XS\x01x\xc9K4\x8bI\xe1qhbR\x97T/S\xeexCYM\x8b\xd2\r\x1a,\xd8\xe1B{d\x8c\t?\xef\xd7{\x98.\xbc|c\x02S\x00\x1b\xb7\x0e\xa8Q\x1bj\x12\x14\xd1l\x0e\xedM\xca\xc0\x15\xcd\xcd\xcf\x94L\x80x\xcf/\xae\x02A\x0c\xa8\xf7u\x1d\x0cDD\x92\xf6\x811W\xbd5#\xc2\xe6\x7fH\xcb\xc1k\xe3\xbd\x84\x8f\xda\xb0\xbf\xbbv\x8e\xf4\x16\xfcM\x9e\x16^\xd7\xb3\xa7#G\xce\x7f\xef \x99\x0e\x87:\xd4v\xc0<\x90\xac(\xdc*\xb81_\xc5\x93\xe4\xb7\xbc\x11\x98\xd6L\xeb\x85\x08\x86\xec\x1e\x14\xe6M\xa7\x1d'


# TEST CASES
def test_sloth_empty_init():
    s = sloth.Sloth()
    assert s.data is None
    assert s.bits == 2048
    assert s.iterations == 50000
    assert s.final_hash is None
    assert s.witness is None

def test_sloth_init():
    s = sloth.Sloth(data=ValidSloth.INPUT,
                    final_hash=ValidSloth.OUTPUT,
                    witness=ValidSloth.WITNESS,
                    bits=ValidSloth.BITS,
                    iterations=ValidSloth.ITERATIONS)
    assert s.data == ValidSloth.INPUT
    assert s.bits == ValidSloth.BITS
    assert s.iterations == ValidSloth.ITERATIONS
    assert s.final_hash == ValidSloth.OUTPUT
    assert s.witness == ValidSloth.WITNESS

def test_sloth_compute():
    s = sloth.Sloth(data=ValidSloth.INPUT,
                    bits=ValidSloth.BITS,
                    iterations=ValidSloth.ITERATIONS)
    s.compute()
    s.wait()
    assert s.final_hash == ValidSloth.OUTPUT
    assert s.witness == ValidSloth.WITNESS

def test_sloth_verify():
    s = sloth.Sloth(data=ValidSloth.INPUT,
                    final_hash=ValidSloth.OUTPUT,
                    witness=ValidSloth.WITNESS,
                    bits=ValidSloth.BITS,
                    iterations=ValidSloth.ITERATIONS)
    s.verify()
    s.wait()
    assert s.valid

def test_sloth_verify_bad_finalhash():
    s = sloth.Sloth(data=InvalidOutput.INPUT,
                    final_hash=InvalidOutput.OUTPUT,
                    witness=InvalidOutput.WITNESS,
                    bits=InvalidOutput.BITS,
                    iterations=InvalidOutput.ITERATIONS)
    print(s.final_hash)
    print(s.valid)
    s.verify()
    s.wait()
    assert not s.valid

def test_sloth_verify_bad_witness():
    s = sloth.Sloth(data=InvalidWitness.INPUT,
                    final_hash=InvalidWitness.OUTPUT,
                    witness=InvalidWitness.WITNESS,
                    bits=InvalidWitness.BITS,
                    iterations=InvalidWitness.ITERATIONS)
    s.verify()
    s.wait()
    assert not s.valid

def test_sloth_bits_time():
    import time
    s = sloth.Sloth(data=b'test', bits=512, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_512bits = time.time() - start_t

    s = sloth.Sloth(data=b'test', bits=1024, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_1024bits = time.time() - start_t

    s = sloth.Sloth(data=b'test', bits=2048, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_2048bits = time.time() - start_t

    assert t_512bits < t_1024bits < t_2048bits, "Increase in bits does not increase time!"

def test_sloth_iteration_time():
    import time
    s = sloth.Sloth(data=b'test', bits=1024, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_1000iter = time.time() - start_t

    s = sloth.Sloth(data=b'test', bits=1024, iterations=2000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_2000iter = time.time() - start_t

    s = sloth.Sloth(data=b'test', bits=1024, iterations=5000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_5000iter = time.time() - start_t

    assert t_1000iter < t_2000iter < t_5000iter, "Increase in bits does not increase time!"

