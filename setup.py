from setuptools import setup

setup(
    name="pysloth",
    py_modules=["sloth"],
    license="MIT",
    use_scm_version=True,
    setup_requires=["setuptools_scm", "cffi>=1.0.0"],
    cffi_modules=["sloth_build.py:ffibuilder"],
    install_requires=[
        "cffi>=1.0.0",
        "tqdm>=4.19",
    ],
)
