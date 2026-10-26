# -*- coding: utf-8 -*-
"""Reparo do preparo central-publica-work depois da queda de energia de 25/10/2026 (a mescla incremental foi cortada entre o índice e a
cópia): a conferência independente achou 10.339 entradas do INDICE_PUBLICO.json sem o arquivo no preparo. Para cada uma: se a origem
(Central de Patentes\\work\\<rel>) existe e o seu sha256 é o do índice, copia; senão, a entrada SAI do índice (a próxima rodada incremental
a reavalia pela esteira). Backup de bytes do índice; nada é apagado do disco; lista local do que saiu."""
import hashlib, json, os, shutil, time
from pathlib import Path

D = Path(r"C:\IALD\Central_publica\central-publica-work")
SRC = Path(r"C:\IALD\Central de Patentes\work")
W = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")
IP = D / "INDICE_PUBLICO.json"
raw = IP.read_bytes()
idx = json.loads(raw)


def longo(base, rel):
    return "\\\\?\\" + str((base / rel).resolve())


copiados, sairam, presentes = [], [], 0
novos = []
for a in idx["arquivos"]:
    rel = a["caminho"]
    if os.path.exists(longo(D, rel)):
        presentes += 1; novos.append(a); continue
    s = longo(SRC, rel)
    if os.path.exists(s):
        b = open(s, "rb").read()
        if hashlib.sha256(b).hexdigest() == a["sha256"] and len(b) == a["bytes"]:
            os.makedirs(os.path.dirname(longo(D, rel)), exist_ok=True)
            with open(longo(D, rel), "wb") as f:
                f.write(b)
            copiados.append(rel); novos.append(a); continue
    sairam.append(rel)
(W / ("bak_preparo_work_25out")).mkdir(exist_ok=True)
(W / "bak_preparo_work_25out" / ("INDICE_PUBLICO.json.bak_" + TS)).write_bytes(raw)
idx["arquivos"] = novos
idx["n_arquivos"] = len(novos)
idx.setdefault("atualizacoes", []).append({"em": time.strftime("%Y-%m-%d %H:%M:%S"), "motivo": "reparo depois da queda de energia de 25/10/2026 (índice sem arquivo)",
                                            "copiados_da_origem": len(copiados), "retirados_do_indice": len(sairam)})
t = IP.with_name(IP.name + ".tmp"); t.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8"); os.replace(t, IP)
(W / ("reparo_indice_sem_arquivo_%s.json" % TS)).write_text(json.dumps({"copiados": copiados, "retirados": sairam}, ensure_ascii=False, indent=0), encoding="utf-8")
print("presentes %d | copiados da origem (sha256 igual) %d | retirados do índice %d | índice agora %d" % (presentes, len(copiados), len(sairam), len(novos)))
