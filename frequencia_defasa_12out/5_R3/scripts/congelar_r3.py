# -*- coding: utf-8 -*-
r"""RODADA 3 — congela por hash (sha256 lido dos bytes) o ADENDO do pre-registro aditivo e os artefatos da rodada 3 que ja
existem no momento do congelamento. Grava 5_R3\FREEZE_R3.json (recusa sobrescrever). Nao escreve fora de 5_R3."""
import hashlib, json, os, datetime

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)
ITENS = [
    "ADENDO_PREREGISTRO_ADITIVO_R3.md", "ADENDO_PREREGISTRO_ADITIVO_R3.json",
    "sandbox/TGLExt/TheUnitIsTheRank.lean", "olean/TheUnitIsTheRank.olean",
    "sandbox/AuditTheUnitIsTheRank.lean", "sandbox/TiposTheUnitIsTheRank.lean", "sandbox/ValoresTheUnitIsTheRank.lean",
    "sandbox_r2/TGLExt/TheUnitIsTheRank.lean", "sandbox_r2/TiposTheUnitIsTheRank.lean", "sandbox_r2/ValoresTheUnitIsTheRank.lean",
    "MONTAGEM_PEDRA_R3.json", "DECLARACOES_R3.json", "TIPOS_R2_VS_R3.json", "TABELA_R2_R3.md", "DIFF_r2_r3.txt",
    "IMPRESSAO_DIGITAL_KERNEL_ANTES.json",
    "logs/repro_r2_pedra_RECIBO.json", "logs/repro_r2_pedra_SAIDA.txt", "logs/r3_pedra_RECIBO.json", "logs/r3_pedra_SAIDA.txt",
    "logs/auditoria_r3_RECIBO.json", "logs/auditoria_r3_SAIDA.txt", "logs/tipos_r2_RECIBO.json", "logs/tipos_r2_SAIDA.txt",
    "logs/tipos_r3_RECIBO.json", "logs/tipos_r3_SAIDA.txt", "logs/valores_r2_RECIBO.json", "logs/valores_r2_SAIDA.txt",
    "logs/valores_r3_RECIBO.json", "logs/valores_r3_SAIDA.txt",
    "scripts/montar_pedra_r3.py", "scripts/gerar_auditoria_r3.py", "scripts/gerar_valores_r3.py", "scripts/comparar_r2_r3.py",
    "scripts/rodar_lean.py", "scripts/sandbox_toolchain.py", "scripts/impressao_digital_kernel.py", "scripts/auto_auditoria_r3.py",
    "scripts/congelar_r3.py",
]
FORA = [  # pinos de fora de 5_R3, so lidos
    os.path.join(UNID, "1_PREREGISTRO", "FREEZE.json"), os.path.join(UNID, "1_PREREGISTRO", "PREREGISTRO.json"),
    os.path.join(UNID, "3_KERNEL", "rodada2", "sandbox", "TGLExt", "TheUnitIsTheRank.lean"),
    os.path.join(UNID, "3_KERNEL", "rodada2", "olean", "TheUnitIsTheRank.olean"),
    os.path.join(UNID, "4_RELATORIO", "RELATORIO_FINAL.md"),
    os.path.join(UNID, "4_RELATORIO", "auditorias_copia", "POSTO_AUD_ESTATUTO", "r2", "sandbox", "AuditorEstatutoR2.lean"),
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


dst = os.path.join(R3, "FREEZE_R3.json")
if os.path.exists(dst):
    raise SystemExit("FALHA VISIVEL: FREEZE_R3.json ja existe (nao sobrescrevo)")
out = {"documento": "FREEZE da RODADA 3 — ADENDO (pre-registro aditivo) e artefatos da rodada 3, congelados por hash",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "adendo": {}, "artefatos_5_R3": {}, "pinos_externos_so_lidos": {}}
for rel in ITENS:
    p = os.path.join(R3, rel.replace("/", os.sep))
    if not os.path.exists(p):
        raise SystemExit("FALHA VISIVEL: ausente: " + p)
    d = {"bytes": os.path.getsize(p), "sha256": sha(p)}
    (out["adendo"] if rel.startswith("ADENDO") else out["artefatos_5_R3"])[rel] = d
for p in FORA:
    out["pinos_externos_so_lidos"][p] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
tmp = dst + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
os.replace(tmp, dst)
print(json.dumps({"adendo": out["adendo"], "quando_utc": out["quando_utc"],
                  "pedra_r3": out["artefatos_5_R3"]["sandbox/TGLExt/TheUnitIsTheRank.lean"],
                  "olean_r3": out["artefatos_5_R3"]["olean/TheUnitIsTheRank.olean"]}, ensure_ascii=False, indent=1))
