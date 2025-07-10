# TransparentMeta – Example Scripts

This folder contains four minimal scripts to help you get started with the
[TransparentMeta](https://transparentaudio.ai) SDK. These examples will onboard
you quickly by walking through the full process of logging, key generation,
metadata writing, and verification. You can use them as a reference for 
integrating TransparentMeta into your own applications.

👉 **Study and run the scripts in order for best results.**

---

## ✅ Installation

Before running the examples, install the project dependencies from the root
of the repo.

Use one of the following:

```bash
make install        # for runtime-only dependencies
make install_dev    # for full development setup
```

---

## 📁 Move into the `examples/` folder

Before running any script, navigate into the `examples/` directory:

```bash
cd examples
```

---

## 🚀 Script Overview (in order)

### 1. `configure_logging.py`

Set up logging for TransparentMeta.

- Enables SDK logging (default: `INFO`, optionally `DEBUG`).
- Use the TransparentMeta custom logger **only** if your app doesn’t 
  already configure logging.
- If you have your logger, logs will bubble up through Python's logging system.

Run:

```bash
python examples/configure_logging.py
```

---

### 2. `generate_key_pair.py`

Generate a new Ed25519 private/public key pair.

- Saves `private_key.pem` and `public_key.pem` in the current directory.
- Used to sign (private key) and verify (public key) audio metadata.

Run:

```bash
python examples/generate_key_pair.py
```

---

### 3. `write_metadata.py`

Embed signed transparency metadata into an audio file.

- Uses `private_key.pem` to sign metadata.
- Writes metadata and signature into an MP3 or WAV file.
- Edit the `metadata` dictionary in the script to customize.

Run:

```bash
python examples/write_metadata.py
```

---

### 4. `read_metadata.py`

Read and verify metadata from an audio file.

- Uses `public_key.pem` to verify the embedded signature.
- Prints decoded metadata and verification result.

Run:

```bash
python examples/read_metadata.py
```

---

## 🧪 Test the full flow

Use a single MP3 or WAV file to test the full workflow:

1. Generate keys  
2. Write metadata  
3. Read and verify metadata  

You’ll confirm that signing and verification work end to end.

---

## 📁 File paths

The scripts use hardcoded file paths like:

```python
audio_path = Path("/home/valerio/Music/22.mp3")
```

Be sure to update those paths to match your local test files.