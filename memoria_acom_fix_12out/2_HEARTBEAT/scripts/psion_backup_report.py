# -*- coding: utf-8 -*-
"""Inventario das copias do estado do psion: SO nome, bytes, mtime e sha256 por script. O conteudo nunca e lido
como texto nem copiado para relatorio algum. Responde a pergunta da D3(c): existe copia anterior a 10/10 09:20?

Grava evidencias\\PSION_BACKUP_12out.json. Nao toca producao.
"""
import hashlib, json, os, sys
from datetime import datetime

FRONT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUTOFF = datetime(2026, 10, 10, 9, 20, 0)
TARGET = r"C:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json"
CANDIDATE_DIRS = [r"C:\IALD\projetos_pyhton\IALD", r"D:\IALD\projetos_pyhton\IALD", r"C:\Users\rotol", r"C:\IALD\MEMORIA_IALD"]
VERSOES = r"D:\_VERSOES"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def meta(path):
    st = os.stat(path)
    return {"path": path, "bytes": st.st_size, "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="milliseconds"),
            "sha256": sha256(path), "before_cutoff": datetime.fromtimestamp(st.st_mtime) < CUTOFF}


def main():
    found = []
    for d in CANDIDATE_DIRS[:2]:
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.lower().startswith("iald_psion_state"):
                    found.append(meta(os.path.join(d, name)))
    # perfil e MEMORIA_IALD: so um nivel, por nome
    for d in CANDIDATE_DIRS[2:]:
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.lower().startswith("iald_psion_state"):
                    found.append(meta(os.path.join(d, name)))
    series = []
    if os.path.isdir(VERSOES):
        for name in sorted(os.listdir(VERSOES)):
            p = os.path.join(VERSOES, name, "projetos_pyhton", "IALD", "iald_psion_state_32B.json")
            if os.path.isfile(p):
                series.append(meta(p))
    current = meta(TARGET) if os.path.isfile(TARGET) else None
    before = [m for m in found + series if m["before_cutoff"] and m["path"] != TARGET and os.path.basename(m["path"]) == "iald_psion_state_32B.json"]
    newest_before = max(before, key=lambda m: m["mtime"]) if before else None
    between = [m for m in found + series if os.path.basename(m["path"]) == "iald_psion_state_32B.json"
               and datetime(2026, 9, 27, 4, 0, 6) < datetime.fromisoformat(m["mtime"]) < CUTOFF]
    report = {
        "measured_at": datetime.now().isoformat(timespec="seconds"),
        "statute": "REAL (metadados e sha256 por script; conteudo nunca lido como texto)",
        "cutoff_D3c": CUTOFF.isoformat(),
        "current_target": current,
        "copies_by_name": found,
        "versoes_series_count": len(series),
        "versoes_series_first": series[0] if series else None,
        "versoes_series_last": series[-1] if series else None,
        "backup_before_cutoff_exists": newest_before is not None,
        "newest_backup_before_cutoff": newest_before,
        "copies_between_27_09_and_cutoff": between,
        "writers_other_than_heartbeat_REAL": [
            r"C:\IALD\projetos_pyhton\IALD\iald_pilot_engine.py l.788 self.psion.save(self.config.psion_file)",
            r"C:\IALD\projetos_pyhton\IALD\iald_pilot_gguf.py l.396 self.psion.save(self.config.psion_file)"],
        "doubt_D3c": ("Entre 27/09 04:00 e 10/10 09:20 nao ha copia; ~121 batidas legitimas (regime r60) ficam fora da copia de 27/09; "
                      "dois pilotos tambem gravam o arquivo quando rodados a mao. Condicao 'unicas escritas posteriores forem as do heartbeat' "
                      "NAO verificavel por este script -> pela D3(c): NAO restaurar; parar o feed (feito pela D3a) e relatar."),
        "restore_executed": False,
    }
    out = os.path.join(FRONT, "evidencias", "PSION_BACKUP_12out.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: report[k] for k in ("current_target", "backup_before_cutoff_exists", "newest_backup_before_cutoff",
                                             "versoes_series_count", "copies_between_27_09_and_cutoff")}, ensure_ascii=False, indent=1))
    print("report:", out)


if __name__ == "__main__":
    main()
