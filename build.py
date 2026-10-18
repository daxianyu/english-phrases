#!/usr/bin/env python3
"""Regenerate data.json from phrases.json and copy media from /workspace/clips.
Usage: python3 build.py   (add new entries to phrases.json first; slug = clip file base name)
Optional per-phrase fields: video, audio (explicit media paths), link (source URL)."""
import json, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); CLIPS="/workspace/clips"; MEDIA=os.path.join(HERE,"media")
os.makedirs(MEDIA,exist_ok=True)
def find(slug,exts):
    for e in exts:
        p=os.path.join(CLIPS,slug+e)
        if os.path.isfile(p): return p
def copy(p):
    dst=os.path.join(MEDIA,os.path.basename(p))
    if not os.path.exists(dst) or os.path.getsize(dst)!=os.path.getsize(p): shutil.copy2(p,dst)
    return "media/"+os.path.basename(p)
def source_link(slug):
    j=os.path.join(CLIPS,slug+".json")
    if not os.path.isfile(j): return None,None
    d=json.load(open(j))
    if d.get("url"): return d["url"],d.get("title")
    if d.get("fallback_teaching_url"): return d["fallback_teaching_url"],d.get("fallback_title")
    for s in d.get("sources",[]):
        if s.get("source_url"): return s["source_url"],s.get("title")
    return None,None
out=[]
for p in json.load(open(os.path.join(HERE,"phrases.json"))):
    s=p["slug"]; e=dict(p)
    v=p.get("video") or find(s,[".mp4"]); a=p.get("audio") or find(s,[".mp3",".m4a"])
    segs=[find(f"{s}-{i}",[".mp3",".m4a"]) for i in (1,2,3)]; segs=[x for x in segs if x]
    e["audios"]=[copy(x) for x in segs]
    if segs: v=None; a=None
    e["video"]=copy(v) if v else None
    e["audio"]=copy(a) if (a and not v) else None
    if not p.get("link"):
        e["link"],e["link_title"]=source_link(s)
    out.append(e)
json.dump(out,open(os.path.join(HERE,"data.json"),"w"),ensure_ascii=False,indent=1)
print(f"{len(out)} phrases; video {sum(1 for x in out if x['video'])}; audio {sum(1 for x in out if x['audio'])}")
