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
You can also install TransparentMeta directly from the repository. This 
project uses [Poetry](https://python-poetry.org/) for dependency management.
You’ll need to install Poetry first.

To install TransparentMeta from source code run:
```bash
git clone https://github.com/Transparent-Audio/transparentmeta.git
cd transparentmeta
```

Then, activate your Poetry environment:
```bash
poetry env use python3.12  # or any Python >=3.12 you have installed
poetry env activate
```

The last command will print something like:
```
source /path/to/virtualenv/bin/activate
```
Copy and paste that command into your shell to activate the Poetry virtual environment.

This is the workflow for Poetry ≥2.0. If you are using Poetry ≤1.x, run 
`poetry shell` instead — it will activate the
environment in a new subshell automatically.


Now, you can install the project with:
```bash
make install
```

To install in development mode, run:
```bash
make install_dev
```

`make install` and `make install_dev` wrap relevant Poetry commands. They can 
be found along with other useful commands in the Makefile.

---

## Python version
TransparentMeta supports Python 3.12 and above. Ensure you have a compatible 
version installed.
