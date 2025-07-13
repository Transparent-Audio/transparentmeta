# TransparentMeta

[**TransparentMeta**](https://github.com/Transparent-Audio/transparentmeta) is an open-source Python library developed by 
[Transparent Audio](https://www.transparentaudio.ai/) for adding, verifying, and reading metadata labels in audio files to ensure compliance with AI transparency laws such as the **EU AI Act** and the **California AI Transparency Act**. It supports cryptographic signing, robust file validation, and a modular SDK to help generative AI companies label AI-generated audio content effectively.

## 🚀 Features

- Add cryptographically signed transparency metadata to MP3 and WAV files  
- Read and verify metadata to detect AI-generated audio  
- Key pair generation and signature verification built-in  
- Simple Python SDK for easy integration
- 100% tested with extensive unit and integration coverage  

## 🔧 Use Cases

- Speech synthesis and voice cloning labeling output with transparency metadata  
- Generative AI music and sound effects tagging output with metadata and attribution  
- Compliance with EU AI Act & California AI Transparency Act  
- Building trusted pipelines with verifiable audio provenance  

## 📦 Installation

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple transparentmeta```
```
Note: This allows installation of dependencies from the official PyPI while 
fetching the TransparentMeta package from Test PyPI. Once launched, 
TransparentMeta will be available for installation from the official PyPI 
repository.

Or, install directly from the repository:
```bash
git clone https://github.com/your-org/transparentmeta.git
cd transparentmeta
make install
```

To install in development mode, after cloning the repository, run:
```bash
make install_dev
```

## 📚 Getting Started 
- Check the `/examples` folder for quick usage examples. Start by reading the 
[README.md file](examples/README.md) inside the folder.
- For a more thorough introduction to TransparentMeta watch the video 
  tutorials on [YouTube](https://www.youtube.com/@transparentaudio).

## 📖 Documentation 
Full documentation on [Read the Docs](https://transparentmeta.readthedocs.io/en/stable/)

## 📂 Project Structure 
- `transparentmeta/` - Main library code
- `examples/` - Example scripts and usage
- `tests/` - Unit and integration tests
- `docs/` - Sphinx documentation
- `Makefile` - Useful commands for development

## 🧩 Dependencies 
TransparentMeta relies on the following core libraries:
- [mutagen](https://mutagen.readthedocs.io/en/latest/) – for reading and writing audio metadata (MP3, WAV, etc.)
- [cryptography](https://cryptography.io/en/latest/) – for generating and verifying digital signatures 

You can find all dependencies in `pyproject.toml`.

## ✅ Running tests and quality checks 
To run tests, linting, and type checks, use:
```bash
make checklist
```

## Python version 
TransparentMeta supports Python 3.12 and above. Ensure you have a compatible 
version installed.

## 📝 License 
This project is licensed under GPL-3.0. See the [LICENSE](LICENSE) file for details.

## 📬 Contact 
If you have any questions, issues, or feature requests, please write to 
Transparent Audio's founder Valerio Velardo at valerio@transparentaudio.ai.

