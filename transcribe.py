#!/usr/bin/env python3
"""Write /workspace/clips/<slug>-N.txt transcripts for segment mp3s that lack one."""
import glob, os, re, whisper
fs=[f for f in sorted(glob.glob('/workspace/clips/*-[123].mp3')) if not os.path.exists(f[:-4]+'.txt')]
if fs:
    m=whisper.load_model('base.en')
    for f in fs:
        t=m.transcribe(f,language='en',fp16=False)['text'].strip()
        open(f[:-4]+'.txt','w').write(t); print(os.path.basename(f),'|',t)
