"""Interoperability and adversarial tests independent of the adapter unit tests."""
from __future__ import annotations
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import struct
import sys
import tempfile

HERE=Path(__file__).resolve().parent
app=Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parent / "app"
original=Path(sys.argv[2]) if len(sys.argv)>2 else Path("C:/IALD/Central de Patentes/patents/BR102025026951-1_ACOM/dispositivo")
sys.path[:0]=[str(app),str(original)]
import archive_safe as safe

out={}
refusals={}
def check(key, outcome): out[key]=bool(outcome)
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def make_manifest(blob, manifest):
    fp=io.BytesIO(blob); off,_=safe.arc._read_footer(fp)
    encoded=json.dumps(manifest,ensure_ascii=False,separators=(",",":")).encode()
    return blob[:off]+encoded+safe.arc.MAGIC_END+struct.pack(">QI",off,len(encoded))
def get_manifest(blob):
    fp=io.BytesIO(blob); off,n=safe.arc._read_footer(fp)
    return json.loads(blob[off:off+n])
with tempfile.TemporaryDirectory(prefix="probe-",dir=HERE) as tmp:
    root=Path(tmp); src=root/"宇宙 – AÇÃO"; src.mkdir()
    (src/"silêncio").mkdir(); (src/"源.txt").write_bytes(("αω\n"*5000).encode())
    # Uses actual canonical streaming route, including size=None in the manifest.
    large=src/"large.bin"; large.write_bytes(bytes(range(256))*(40*1024+3))
    pkg=root/"roundtrip.acom"; dst=root/"restored"
    counts=safe.pack_paths([src],pkg)
    sizes=safe.extract_archive(pkg,dst)
    check("new_writer_reads_big_stream_and_empty_dir",
          (dst/src.name/"silêncio").is_dir() and h(dst/src.name/large.name)==h(large) and h(dst/src.name/"源.txt")==h(src/"源.txt"))
    check("reported_byte_counts_match_disk",sizes["outputBytes"]==sum(p.stat().st_size for p in src.iterdir() if p.is_file())
          and sizes["inputBytes"]==pkg.stat().st_size and counts["outputBytes"]==pkg.stat().st_size)
    original_read=dict(safe.arc.unpack_to_memory(pkg))
    check("canonical_read_of_new_writer",hashlib.sha256(original_read[src.name+"/large.bin"]).hexdigest()==h(large))
    new_data=pkg.read_bytes(); new_manifest=get_manifest(new_data)
    new_manifest["entries"][0]["path"]="new-name.bin"
    new_tampered=root/"new-name-tampered.acom"
    new_tampered.write_bytes(make_manifest(new_data,new_manifest))
    try: safe.extract_archive(new_tampered,root/"tampered-restore"); new_refused=False
    except ValueError as exc: new_refused=True;refusals["new_filename_change"]=str(exc)
    check("new_writer_detects_accidental_filename_change",new_refused and not (root/"tampered-restore").exists())
    raw,_=safe.arc.pack_files([("original₁.txt",b"x"),("second.txt",b"abcd"*4)])
    direct=root/"original-format.acom";direct.write_bytes(raw)
    direct_result=safe.extract_archive(direct,root/"canonical-output")
    check("untouched_canonical_manifest_accepted",direct_result["files"]==2 and (root/"canonical-output"/"original₁.txt").read_bytes()==b"x")
    manifest=get_manifest(raw)
    checks=[
        ("overlapping_off",lambda m: m["entries"][1].update(off=m["entries"][0]["off"])),
        ("declared_input_cap",lambda m: m["entries"][0].update(size=safe.MAX_MEMBER+1)),
        ("header_position",lambda m:m["entries"][0].update(off=0)),
        ("reparse_separator",lambda m:m["entries"][1].update(path=r"\\?\UNC\test\work")),
        ("ads_in_subdirectory",lambda m:m["entries"][1].update(path="nodes/part:data")),
        ("reserved_superscript_device",lambda m:m["entries"][1].update(path="COM¹.txt")),
        ("casefold_type_collision",lambda m:m["entries"][1].update(path="ORIGINAL₁.TXT/inside")),
        ("aliased_dir",lambda m:m["entries"][1].update(path="LONGFO~1/target")),
        ("modified_byte_hash",lambda m:m["entries"][1].update(sha256="f"*64)),
    ]
    for key, mutate in checks:
        copied=json.loads(json.dumps(manifest));mutate(copied)
        altered=root/(key+".acom");altered.write_bytes(make_manifest(raw,copied));target=root/("out-"+key)
        try: safe.extract_archive(altered,target)
        except ValueError as exc:
            refusals[key]=str(exc)
            rejected=True
        else: rejected=False
        check("reject_"+key,rejected and not target.exists() and not list(root.glob(".iald-acom-*")))
    # Hashes carried by canonical v1 cover file content. Record metadata coverage separately.
    modified=json.loads(json.dumps(manifest));modified["entries"][1]["path"]="different.txt"
    modified_path=root/"changed-name.acom";modified_path.write_bytes(make_manifest(raw,modified));renamed=root/"renamed"
    try: safe.extract_archive(modified_path,renamed);metadata_hash="content-only v1" if (renamed/"different.txt").exists() else "unexpected"
    except (ValueError,OSError) as exc: metadata_hash="filename-change-rejected: "+str(exc)
report=dict(checks=out,refusals=refusals,passed=sum(out.values()),total=len(out),adapter_sha256=h(app/"archive_safe.py"),canonical_modules=[{"name":p.name,"sha256":h(p)} for p in (original/"acom_archive.py",original/"acom_codec.py",original/"acom_auto.py")],metadata_probe=metadata_hash)
receipt=HERE/("ARCHIVE_REVIEW_"+report["adapter_sha256"][:12]+".json");receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"passed":report["passed"],"total":len(out),"failed":[k for k,v in out.items() if not v],"metadata_probe":metadata_hash,"receipt":str(receipt)}))
sys.exit(int(not all(out.values())))
