# Cryptographic signature 

To ensure the security and integrity of transparency metadata embedded in 
audio files, TransparentMeta implements cryptographic signatures. While it 
is impossible  to completely prevent metadata modification, cryptographic 
signatures  allow the detection of any unauthorized changes, providing 
tamper-evidence and trustworthiness.

---

## What is a cryptographic signature?

A cryptographic signature is a mathematical technique that binds data (in 
this case, metadata) to a unique digital signature created using a private 
key. Anyone with the corresponding public key can verify that:

- The data has not been altered since it was signed.
- The data was indeed signed by the holder of the private key.

This mechanism works similarly to a handwritten signature but provides 
strong guarantees backed by cryptography.

---

## Ed25519 digital signature algorithm

TransparentMeta uses the **Ed25519** digital signature algorithm, a modern, 
high-performance, and secure elliptic-curve signature scheme known for:

- Strong security guarantees against forgery.
- Fast signing and verification operations.
- Compact signature size (64 bytes), which is well suited for embedding in metadata.

TransparentMeta uses the [cryptography](https://cryptography.io/en/latest/) 
library to implement Ed25519 signatures.

You can learn more about Ed25519 [here]](https://ed25519.cr.yp.to/papers.html).

---

## How signatures work in TransparentMeta

### Signing at write time
When metadata is written into an audio file, TransparentMeta generates a  
digital signature of the metadata using the Ed25519 private key.

This signature, along with the metadata itself, is stored in two separate  
custom ID3v2 tags inside the audio file:
  - `transparency`: contains the serialized metadata.
  - `signature`: contains the digital signature corresponding to the metadata.

### Verifying at read time

1. Upon reading, TransparentMeta retrieves both the metadata and the signature 
from their respective ID3v2 tags.

2. Using the associated public key, TransparentMeta verifies the digital 
signature against the metadata.

3. If **any part of the metadata or signature has been altered**, the 
verification fails, signaling tampering or corruption.

4. If verification succeeds, it guarantees that the metadata is authentic and 
has not been modified since signing. 

This process ensures the integrity and authenticity of transparency 
metadata throughout the lifecycle of the audio file.

By implementing cryptographic signatures in this way, TransparentMeta 
provides a robust foundation for trustworthy AI-generated audio transparency compliance.


















