# pysloth

Python wrapper around the sloth algorithm by Benjamin Wesolowski in A random zoo: sloth, unicorn, and trx

The python module exposes an api for the sloth c-extension.

## Install

__Note: this module is only tested to work on linux (ubuntu)__

Can be installed with pip or by running `python3 setup.py install`.
The setup process includes compiling the c-extension, which has the following requirements (both installable via apt):
* libgmp-dev
* libssl-dev

## Usage

Usage example:
```
from sloth import Sloth

sloth = Sloth(data=b'testdata', bits=2048, iterations=5000)
sloth.compute()
sloth.wait()

print("sloth computation done")
print("witness", sloth.witness)
print("output", sloth.final_hash)

sloth.verify()
sloth.wait()
print("sloth is", ("valid" if sloth.valid else "invalid"))
```

You can enable/disable a sloth progressbar by setting `PROGRESS` on the sloth module to `true` or `false`.

_If in doubt read the code_
