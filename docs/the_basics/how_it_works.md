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

--- 

## Use case

The typical use case for TransparentMeta involves a generative audio AI 
company that wants to label its AI-generated audio content with metadata that 
flag it as AI-generated. This is crucial for compliance with AI 
transparency legislation, such as the EU AI Act and the California AI Transparency Act. 

The worklow usually looks like this:

1. The company generates audio content using its AI models.
2. Just before distributing the audio, it uses TransparentMeta to embed 
   cryptographically signed metadata into the audio files.
3. The audio is stored and distributed through various channels.
4. When the audio is accessed, platforms or end-users can use TransparentMeta 
   to read and verify the metadata, confirming the audio's AI-generated 
   nature and its origin.
