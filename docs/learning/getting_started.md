# Getting started

This quickstart guide shows how to generate a private Ed25519 key on the 
fly and use it to write cryptographically signed transparency metadata into 
an audio file using TransparentMeta.

This minimal example requires no pre-existing keys and demonstrates the core functionality to embed compliant metadata.

---

## Generate key and write metadata

```python
import logging
from datetime import datetime, timezone

from transparentmeta.crypto.key_management import generate_key_pair
from transparentmeta.sdk import build_transparent_metadata_writer
from transparentmeta.entity.metadata import AIUsageLevel
from transparentmeta.logger_config import configure_logging

# Configure logging at debug level for following all the steps
configure_logging(level=logging.DEBUG)

# Path to the target audio file to write metadata into
audio_file_path = "path/to/your/audio.mp3"

# Define metadata to embed
metadata = {
    "company": "Transparent Audio",
    "model": "v2.1",
    "created_at": datetime.now(timezone.utc),
    "ai_usage_level": AIUsageLevel.AI_ASSISTED,
    "content_id": "12345",
    "user_id": "user_67890",
    "private_key_id": "generated_key_1",
    "additional_info": {
        "attribution": {
            "lyrics": "John Doe",
            "composer": "Jane Smith",
            "singer": "HAL 9000",
        }
    },
}

# Generate a new Ed25519 private/public key pair on the fly
private_key, public_key = generate_key_pair()

# Build a metadata writer instance with the generated private key necessary for signing
transparent_metadata_writer = build_transparent_metadata_writer(private_key)

# Write the metadata and signature into the audio file
transparent_metadata_writer.write(audio_file_path, metadata)
```