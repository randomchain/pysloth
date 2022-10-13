import sloth


class ValidSloth:
    INPUT = b"testy"

    BITS = 1024
    ITERATIONS = 100

    WITNESS = b"wO\x05:\xa4\xe9\x83\xe1f\x8a\xeb\x7f\xdf\xf5::\x12\x17\xad\x03(|,\xb4\xf2C3\xdcH\xfb\xd6<\xf24\x9f=\x84\xbcS+\xec\xd1\xa5{vE\x9c\xd8\x98Y\x8c\xfc}\x1f\x8a3\xd7\x84\x98;\x03e\xe6\xac\x1f\x0c\x08uR.\xa0\xf6\":d\xfa\xd6;Q\x1dd\xda\x8a\x9e\xb1\x91\x88\x84x\x1b0\xd3;\xdf\x81\xed\xf1\x97\x10\xd8\xcc\x17/o\xe5\xec\xc6\xe0z\xed\xf2!f` u\xd8dC'\xb8\xf4\x03\xfd\x1d\xf3z\xc4"
    OUTPUT = b"\x9c\tt\xdc5\xcd\x88\xbd&\xdf\xd5\x16\x85\xc6\xa3\xbak\xce\x01\x08RA\xd3f\xbc\x81\x8d\x94\x18*\xac\x13\x106Q\xc4\xdcf7$\x839<\xb0+w\xfa\xe8\xa2^\xedknl\x91\x04\x95\xa79\xa4B\xb2\xa0\xad"


class InvalidInput(ValidSloth):
    INPUT = b"testie"


class InvalidOutput(ValidSloth):
    OUTPUT = b"meme"


class InvalidWitness(ValidSloth):
    WITNESS = b"wO\x05:\xa5\xe4\x83\xe1f\x8a\xeb\x7f\xdf\xf5::\x12\x17\xad\x03(|,\xb4\xf2C3\xdcH\xfb\xd6<\xf24\x9f=\x84\xbcS+\xec\xd1\xa5{vE\x9c\xd8\x98Y\x8c\xfc}\x1f\x8a3\xd7\x84\x98;\x03e\xe6\xac\x1f\x0c\x08uR.\xa0\xf6\":d\xfa\xd6;Q\x1dd\xda\x8a\x9e\xb1\x91\x88\x84x\x1b0\xd3;\xdf\x81\xed\xf1\x97\x10\xd8\xcc\x17/o\xe5\xec\xc6\xe0z\xed\xf2!f` u\xd8dC'\xb8\xf4\x03\xfd\x1d\xf3z\xc4"


# TEST CASES
def test_sloth_empty_init():
    s = sloth.Sloth()
    assert s.data is None
    assert s.bits == 2048
    assert s.iterations == 50000
    assert s.final_hash is None
    assert s.witness is None


def test_sloth_init():
    s = sloth.Sloth(
        data=ValidSloth.INPUT,
        final_hash=ValidSloth.OUTPUT,
        witness=ValidSloth.WITNESS,
        bits=ValidSloth.BITS,
        iterations=ValidSloth.ITERATIONS,
    )
    assert s.data == ValidSloth.INPUT
    assert s.bits == ValidSloth.BITS
    assert s.iterations == ValidSloth.ITERATIONS
    assert s.final_hash == ValidSloth.OUTPUT
    assert s.witness == ValidSloth.WITNESS


def test_sloth_predef_compute():
    s = sloth.Sloth(
        data=ValidSloth.INPUT, bits=ValidSloth.BITS, iterations=ValidSloth.ITERATIONS
    )
    s.compute()
    s.wait()
    assert s.final_hash == ValidSloth.OUTPUT
    assert s.witness == ValidSloth.WITNESS


def test_sloth_compute():
    s = sloth.Sloth(
        data=ValidSloth.INPUT, bits=ValidSloth.BITS, iterations=ValidSloth.ITERATIONS
    )
    s.compute()
    s.wait()
    assert s.final_hash
    assert s.witness


def test_sloth_predef_verify():
    s = sloth.Sloth(
        data=ValidSloth.INPUT,
        final_hash=ValidSloth.OUTPUT,
        witness=ValidSloth.WITNESS,
        bits=ValidSloth.BITS,
        iterations=ValidSloth.ITERATIONS,
    )
    s.verify()
    s.wait()
    assert s.valid


def test_sloth_compute_verify():
    s = sloth.Sloth(
        data=ValidSloth.INPUT, bits=ValidSloth.BITS, iterations=ValidSloth.ITERATIONS
    )
    s.compute()
    s.wait()
    s.verify()
    s.wait()
    assert s.valid


def test_sloth_verify_bad_finalhash():
    s = sloth.Sloth(
        data=InvalidOutput.INPUT,
        final_hash=InvalidOutput.OUTPUT,
        witness=InvalidOutput.WITNESS,
        bits=InvalidOutput.BITS,
        iterations=InvalidOutput.ITERATIONS,
    )
    s.verify()
    s.wait()
    assert not s.valid


def test_sloth_verify_bad_witness():
    s = sloth.Sloth(
        data=InvalidWitness.INPUT,
        final_hash=InvalidWitness.OUTPUT,
        witness=InvalidWitness.WITNESS,
        bits=InvalidWitness.BITS,
        iterations=InvalidWitness.ITERATIONS,
    )
    s.verify()
    s.wait()
    assert not s.valid


def test_sloth_bits_time():
    import time

    s = sloth.Sloth(data=b"test", bits=512, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_512bits = time.time() - start_t

    s = sloth.Sloth(data=b"test", bits=1024, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_1024bits = time.time() - start_t

    s = sloth.Sloth(data=b"test", bits=2048, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_2048bits = time.time() - start_t

    assert (
        t_512bits < t_1024bits < t_2048bits
    ), "Increase in bits does not increase time!"


def test_sloth_iteration_time():
    import time

    s = sloth.Sloth(data=b"test", bits=1024, iterations=1000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_1000iter = time.time() - start_t

    s = sloth.Sloth(data=b"test", bits=1024, iterations=2000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_2000iter = time.time() - start_t

    s = sloth.Sloth(data=b"test", bits=1024, iterations=5000)
    start_t = time.time()
    s.compute()
    s.wait()
    t_5000iter = time.time() - start_t

    assert (
        t_1000iter < t_2000iter < t_5000iter
    ), "Increase in bits does not increase time!"
