# How TransparentMeta works

TransparentMeta is a Python library that integrates seamlessly into your 
application. Once you import TransparentMeta, with just a few lines of code, 
you can add transparency features quickly without disrupting existing development 
workflows.

---

## Writing

When AI-generated audio is produced, you can call a TransparentMeta routine to 
write cryptographically signed metadata directly into your audio files. This 
metadata includes key details such as generation timestamp, model identity, 
and content origin.

---

## Reading

TransparentMeta provides tools to read and verify embedded metadata from audio 
files at any stage of the distribution chain. This functionality allows platforms, 
regulators, or end-users to confirm whether audio content is AI-generated and 
ensures the transparency information remains intact. The verification process 
validates cryptographic signatures to confirm data integrity and detect any 
unauthorized modifications.

Reading is done by calling a simple TransparentMeta routine, making it easy to 
integrate into existing systems.
