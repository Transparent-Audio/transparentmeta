## FAQs

### When should I write metadata to the audio files I generate?
You should write metadata using TransparentMeta after you generate the 
audio content but just before you distribute it. This ensures that the 
metadata is included in the audio files and can be verified by platforms, regulators, or end-users.

---

### How is TransparentMeta different from C2PA?
TransparentMeta is specifically designed for audio content. It is 
minimalist, focusing  only on the essential features needed to comply with 
AI transparency  legislation. Its metadata is extremely lightweight, unlike 
C2PA, which is designed for full provenance. TransparentMeta is also much easier to integrate and use.

--- 


### What audio formats does TransparentMeta support?
TransparentMeta currently supports adding metadata to WAV and MP3 files. 
Support for additional formats (such as FLAC or AIFF) may be added in future 
releases.

--- 


### Is TransparentMeta compliant with the EU AI Act and other regulations?
TransparentMeta is designed to help gen AI audio companies comply with 
transparency and labeling requirements in the EU AI Act, as well as similar 
emerging regulations. At Transparent Audio, we work closely with legal 
experts and the European Commission to ensure that our tools meet the 
latest compliance standards.

--- 


### Can TransparentMeta metadata be removed or tampered with?
While TransparentMeta embeds metadata directly in the audio file, any 
metadata can potentially be stripped or altered by third-party tools. 
However, through cryptographic signing, TransparentMeta provides a way to 
verify the
integrity of the metadata. If the metadata is tampered with, the signature 
will not match, indicating that the file has been altered. For maximum security and compliance,
we recommend combining metadata with audio watermarks, and 
deep-fake detection. At Transparent Audio, we are busy developing
all these layers of transparency and verification for AI-generated audio 
content to ensure the highest level of trust and compliance.

--- 


### Does TransparentMeta work with both music and speech audio?
Yes, TransparentMeta can be used to tag and verify both AI-generated music and speech audio files.

--- 


### Is TransparentMeta open source?
Yes, TransparentMeta is fully open source under the GPLv3 license. 
Feature requests are welcome via our [Discord server](https://discord.gg/pE9yRt7b9N). We're also planning to open contributions from the community in the future.

--- 


### Can I use TransparentMeta in a commercial product?
Yes. As long as you comply with the terms of the GPLv3 license, you are 
free to use TransparentMeta in commercial projects.

--- 


### How does TransparentMeta handle cryptographic signing?
TransparentMeta provides support for cryptographically signing metadata, 
making it possible to verify the authenticity of the label and the source.

--- 


### Does using TransparentMeta affect audio quality?
No. TransparentMeta embeds metadata in a way that does not alter or degrade the audio content.

--- 


### Can TransparentMeta be integrated into automated pipelines?
Yes, TransparentMeta is designed to be easily scriptable and can be 
integrated into any audio generation, processing, or distribution pipeline.

--- 


### How does TransparentMeta validate that a file is AI-generated?
TransparentMeta does not detect whether content is AI-generated. It 
provides the mechanism for labeling and verifying audio as such, based on your workflow and regulatory needs.

--- 


### What happens if a platform does not recognize TransparentMeta metadata?
If a downstream platform or tool does not read TransparentMeta metadata, 
the audio will still play as normal, but the transparency information will not be visible to users on that platform.

--- 


### Who is responsible for labeling audio content with TransparentMeta?
As per the EU AI Act and similar regulations, it is the responsibility of the generative AI provider to label their AI-generated audio content.

--- 

### Is TransparentMeta available in multiple programming languages?
No. TransparentMeta is currently only available as a Python library.





