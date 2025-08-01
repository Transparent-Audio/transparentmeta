# TransparentMeta – Demonstration Scripts

This folder contains four demonstration scripts to help you get started 
with the TransparentMeta SDK. 

⚠️These are not entry‑point scripts. They are code examples showcasing the 
library’s main functionality. You can copy and reuse this code in your 
application when integrating TransparentMeta. 

These examples will help you onboard quickly by walking through the 
workflow for logging, key generation, metadata writing, and verification.

---

## ✅ Installation

Before running any example, install the project dependencies from the root of 
the repository using one of the following commands:

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

## 🧪 Test the full workflow

You can run the scripts in any order, but we recommend following this sequence 
as it reflects typical usage:

1. Generate keys  
2. Write metadata  
3. Read and verify metadata  

---

## 🚀 Demonstration Scripts

### `configure_logging.py`

Demonstrates how to set up logging for TransparentMeta.

---

### `generate_key_pair.py`

Shows how to generate and save an Ed25519 private/public key pair for 
cryptographic signing.

---

### `write_metadata.py`

Demonstrates embedding transparency metadata into an audio file.

---

### `read_metadata.py`

Shows how to read and verifying metadata from an audio file.

---

