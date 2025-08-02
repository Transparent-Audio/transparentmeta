# Installation

You can install TransparentMeta from PyPI or directly from the source code.

---

## From PyPI
The easiest way to install TransparentMeta is via PyPI. You can use the following command:

```bash
pip install transparentmeta
```

---

## From source code
Or, you can install directly from the repository. This project uses 
[Poetry](https://python-poetry.org/) for dependency management. You’ll need to 
install Poetry first.

To install TransparentMeta from source code run:
```bash
git clone https://github.com/Transparent-Audio/transparentmeta.git
cd transparentmeta
make install
```

To install in development mode, after cloning the repository, run:
```bash
make install_dev
```

`make install` and `make install_dev` wrap relevant Poetry commands. They can 
be found along with other useful commands in the Makefile.

---

## Python version
TransparentMeta supports Python 3.12 and above. Ensure you have a compatible 
version installed.
