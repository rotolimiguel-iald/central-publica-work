"""Offline v408 staging. No production queue client or activation entry point."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

WORK = Path(__file__).resolve().parent
SUPPORT = WORK.parent / "scientific_memory_sync_20261013"
MEMBER = "codex-f03-v408-staging"
UNIT = "F0.3.MEMORIA_CIENTIFICA_SYNC"
STAGE = WORK / "staging"
RELEASES = STAGE / "releases"
POINTER_COPY = STAGE / "BASELINE_POINTER.json"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SUPPORT))


def inside(path, root):
    return Path(path).resolve().is_relative_to(root)


def guard(event, args):
    # Installed before importing the helper. Reads of queue DBs below are opaque
    # file digests only. SQLite is confined to the staging tree.
    if event in {"subprocess.Popen", "os.system", "os.startfile", "socket.connect",
                 "socket.bind", "socket.getaddrinfo"}:
        raise PermissionError(event)
    if event == "exec" and Path(args[0].co_filename).name.casefold() == "um.py":
        raise PermissionError("Scientific execution refused")
    if event == "sqlite3.connect":
        location = str(args[0])
        db = Path.from_uri(location.split("?")[0]) if location.startswith("file:") else Path(location)
        if not inside(db, STAGE):
            raise PermissionError("Database outside staging")
    paths = []
    if event == "open" and not isinstance(args[0], int):
        if args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            paths = [args[0]]
    elif event in {"os.mkdir", "os.remove", "os.rmdir", "os.chmod", "os.utime"}:
        paths = [args[0]]
    elif event in {"os.rename", "os.link", "os.symlink"}:
        paths = args[:2]
    for path in paths:
        if not inside(path, WORK):
            raise PermissionError("Write outside staging workspace")


sys.addaudithook(guard)
import scientific_memory_sync as helper

cm = helper.cm
production = helper.ScientificMemorySync(work=WORK, member=MEMBER, unit=UNIT)


def pin(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def create(path, value):
    helper.save_json(path, value, expected_old=None)


def inventory():
    state = cm.ACTIVE.parent.parent
    requests = state / "session_requests"
    queue_files = list(requests.glob("*.json"))
    for name in ("tasks.sqlite3", "iald_orchestrator.sqlite3"):
        for suffix in ("", "-wal", "-journal"):
            path = state / (name + suffix)
            if path.is_file():
                queue_files.append(path)
    return {
        "canonical_files": {str(f.relative_to(cm.ACTIVE.parent)): pin(f)
                            for f in sorted(cm.ACTIVE.parent.rglob("*")) if f.is_file()},
        "queue_storage_bytes": {str(f.relative_to(state)): pin(f) for f in sorted(queue_files)},
    }


def staged_api():
    # The injected module redirects the writable release root. The only default
    # load verifies the actual baseline via the installed, read-only loader.
    def load(directory=None, *, refresh=False):
        if directory is None:
            if POINTER_COPY.read_bytes() != cm.ACTIVE.read_bytes():
                raise ValueError("Production baseline advanced")
        elif not inside(directory, RELEASES):
            raise ValueError("Verification target escaped staging")
        return cm.load(directory, refresh=False)

    return SimpleNamespace(
        RELEASES=RELEASES, ACTIVE=POINTER_COPY, CATALOG=cm.CATALOG,
        __file__=cm.__file__, SNAPSHOT_NAMES=cm.SNAPSHOT_NAMES, SNAPSHOT_MODE=cm.SNAPSHOT_MODE,
        build=cm.build, chunks=cm.chunks, digest=cm.digest, prepare=cm.prepare, load=load,
    )


def run(operation):
    baseline = WORK / "BASELINE_PRODUCTION.json"
    seal = production.check()
    if seal["sealed_version"] != "v408" or seal["active"]["release"] != "v407":
        raise ValueError("Expected sealed v408 over active v407")
    epoch = seal["sealed_epoch"]
    if any(cm.RELEASES.glob("v408_*")):
        raise ValueError("Existing production preparation: reconcile before continuing")
    sync = helper.ScientificMemorySync(module=staged_api(), work=WORK, member=MEMBER, unit=UNIT)
    if operation == "prepare":
        claim = helper.require_claim(UNIT, MEMBER)
        if baseline.exists() or RELEASES.exists():
            raise ValueError("Existing build evidence: inspect instead of rebuilding")
        create(baseline, {"check": seal, "claim": claim, "inventory": inventory()})
        raw = cm.ACTIVE.read_bytes()
        if cm.digest(raw) != seal["active_pin"]["sha256"]:
            raise ValueError("Baseline changed during inventory")
        helper.replace_bytes(POINTER_COPY, raw, expected_old=None)
        result = sync.prepare()
        if result["generation"] != seal["sealed_generation"]:
            raise ValueError("Prepared generation differs from initial measurement")
        print(result["status"], result["epoch"], result["documents"], result["chunks"])
        return

    before = read(baseline)
    if before["check"] != seal or pin(POINTER_COPY) != seal["active_pin"]["sha256"]:
        raise ValueError("Production baseline or source generation differs")
    result = sync.verify(epoch)
    manifest = read(RELEASES / epoch / "manifest.json")
    if result["status"] != "PASS" or result["generation"] != seal["sealed_generation"]:
        raise ValueError("Unverified staging generation")
    for mode, receipt in result["retrieval"].items():
        if receipt["retrieval_scope"] != "SELECTED_PASSAGES_ONLY" or receipt["memory_mode"] != mode:
            raise ValueError("No passages or incorrect mode")
    after = inventory()
    if before["inventory"] != after:
        raise ValueError("Production files changed; reconcile the difference before delivery")
    if operation == "verify":
        create(WORK / "VERIFY_STAGING.json", result)
        create(WORK / "PRESERVATION.json", {
            "baseline_sha256": pin(baseline), "compared_at": helper.utc_now(),
            "all_production_hashes_equal": True, "canonical_files": len(after["canonical_files"]),
            "previous_releases": len(list(cm.RELEASES.iterdir())),
            "queue_storage_files": len(after["queue_storage_bytes"]),
            "scope": "Hash dos bytes de releases, ponteiro, recibos ativos de pedidos e bancos da fila, sem conexão aos bancos.",
            "active_production": seal["active"], "active_production_sha256": pin(cm.ACTIVE),
        })
    print(result["status"], result["generation"], result["chunks"], manifest["index_sha256"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "verify", "inspect"))
    run(parser.parse_args().operation)
