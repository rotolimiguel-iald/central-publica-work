"""Create and restore the sample using the same adapter shipped in the test edition."""
from pathlib import Path
import argparse, hashlib, json, sys, tempfile
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("downloads",type=Path)
parser.add_argument("--codec",type=Path,required=True)
args=parser.parse_args()
sys.path[:0]=[str(HERE/"app"),str(args.codec)]
import archive_safe
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
args.downloads.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);source=root/"Primeira luz";source.mkdir()
    (source/"inscrição.txt").write_bytes(b"1\r\n")
    (source/"Sinais").mkdir()
    (source/"Sinais"/"luz.txt").write_bytes("Haja luz.\r\nLet there be light.\r\nليكن نور.\r\n".encode("utf-8"))
    original={p.relative_to(source).as_posix():digest(p) for p in source.rglob("*") if p.is_file()}
    (source/"CONFERENCIA.txt").write_bytes(("\r\n".join(val+"  "+key for key,val in original.items())+"\r\n").encode())
    archive=root/"Primeira-luz.acom"
    pack=archive_safe.pack_paths([source],archive)
    target=root/"restaurado"
    receive=archive_safe.extract_archive(archive,target)
    files=[p for p in target.rglob("*") if p.is_file()]
    if sorted(digest(p) for p in files)!=sorted(digest(p) for p in source.rglob("*") if p.is_file()):
        raise ValueError("Restauração divergente")
    final=args.downloads/archive.name
    if final.exists() and digest(final)!=digest(archive):raise FileExistsError(str(final))
    if not final.exists():final.write_bytes(archive.read_bytes())
    print(json.dumps(dict(sample=final.name,sha256=digest(archive),pack=pack,extract=receive,files=original),ensure_ascii=False))

