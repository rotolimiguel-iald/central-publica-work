from pathlib import Path

HERE = Path(__file__).resolve().parent
for path in sorted(HERE.glob("*.fits")):
    raw = path.read_bytes()
    print(f"FILE {path.name} bytes={len(raw)}")
    if raw.startswith(b"version"):
        print(raw.decode("utf-8", errors="replace"))
        continue
    for offset in range(0, min(len(raw), 2880 * 4), 2880):
        print(raw[offset:offset + 2880].decode("ascii", errors="replace"))
        if b"END     " in raw[offset:offset + 2880]:
            break
    print("---")
