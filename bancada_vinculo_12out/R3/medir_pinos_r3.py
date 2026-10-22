# -*- coding: utf-8 -*-
"""medir_pinos_r3.py (R3, 13/10/2026) -- mede POR SCRIPT o sha256 de tudo o que a R3 cita (nunca de memoria) e grava R3/PINOS_R3.json.
So le fora de R3. Confere as fontes pinadas na bateria contra o disco. uso: medir_pinos_r3.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
V = AQUI.parent
R2 = V / "R2"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
ENTRADAS = [
    ("R3: o esboco", AQUI / "sincronizar_bancada.py"),
    ("R3: o montador do sandbox", AQUI / "montar_sandbox.py"),
    ("R3: os controles negativos", AQUI / "controles_negativos_r3.py"),
    ("R3: este medidor", AQUI / "medir_pinos_r3.py"),
    ("R3: o gerador do resultado", AQUI / "gerar_resultado_r3.py"),
    ("R3: o resultado dos controles", AQUI / "CONTROLES_NEGATIVOS_R3.json"),
    ("R3: o contrato do recibo do kernel", AQUI / "CONTRATO_KERNEL_RECIBO.md"),
    ("R3: as remissoes do plano", AQUI / "REMISSOES_PLANO_R3.md"),
    ("R3: o diff R2 -> R3 (todos os .py)", AQUI / "DIFF_R2_R3.patch"),
    ("R3: o diff R1 -> R2 do montar_sandbox.py (a omissao da R2)", AQUI / "DIFF_R1_R2_montar_sandbox.patch"),
    ("R2: o esboco (registro)", R2 / "sincronizar_bancada.py"),
    ("R2: o montador (registro)", R2 / "montar_sandbox.py"),
    ("R2: os controles (registro)", R2 / "controles_negativos_r2.py"),
    ("R2: a bateria (vigente na R3, inalterada)", R2 / "BATERIA_VINCULO.json"),
    ("R2: o gerador de canais (inalterado na R3)", R2 / "gerar_canais_mcp.py"),
    ("R2: o gerador da bateria (inalterado na R3)", R2 / "gerar_bateria.py"),
    ("R2: o resultado dos controles", R2 / "CONTROLES_NEGATIVOS_R2.json"),
    ("R2: as remissoes (substituidas)", R2 / "REMISSOES_PLANO.md"),
    ("R2: o resultado", R2 / "RESULTADO_R2.md"),
    ("R1: o montador original", R2 / "originais_R1" / "montar_sandbox.py"),
    ("o desenho", V / "VINCULO_BANCADA_UMPY.md"),
    ("a declaracao de canais de exemplo (A13)", V / "sandbox" / "CANAIS_v391_exemplo.json"),
    ("a re-auditoria da R2 (resumo)", Path("C:/IALD/PROGRAMA_IALD/auditorias/F0.6/AUDITORIA_F0_6_C1_a645d974.md")),
    ("a re-auditoria da R2 (relatorio)", Path("C:/IALD/PROGRAMA_IALD/auditorias/F0.6/art_a645d974/AUDITORIA_VINCULO_R2_C1.md")),
    ("o plano da v392", Path("C:/IALD/PROGRAMA_IALD/exame_12out/J_SINTESE/PLANO_V392.md")),
    ("o molde da cadeia pos-rito", Path("C:/IALD/Central de Patentes/work/v391_selo/chain_pos_rito_v391.sh")),
    ("a producao: o manifesto vigente (so lido)", Path("C:/IALD/Bancada_Um/canonical_contracts.json")),
    ("a producao: o canonical.py instalado (so lido)", Path("C:/IALD/Bancada_Um/bancada/canonical.py")),
    ("o Nos: um.py v391 (so lido)", NOS / "um.py"),
    ("o Nos: o selo v391 (so lido)", NOS / "um_absoluto_selo.json"),
    ("o Nos: o core (so lido)", NOS / "um_absoluto.json"),
    ("o Nos: o manifesto do kernel pinado pelo selo (so lido)", NOS / "tgl_kernel_proof_manifest.json"),
    ("o livro de eventos (VIVO: cresce com outras sessoes; so lido)", Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")),
]
ev = AQUI / "evidencias_sandbox"
if ev.is_dir():
    for p in sorted(ev.rglob("*")):
        if p.is_file():
            ENTRADAS.append(("R3: evidencia do sandbox (copia; o sandbox foi apagado)", p))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3 (13/10/2026)", entradas=[], fontes_da_bateria=[])
for papel, p in ENTRADAS:
    p = Path(p)
    if p.is_file():
        out["entradas"].append(dict(papel=papel, path=str(p), bytes=p.stat().st_size, sha256=sha(p)))
    else:
        out["entradas"].append(dict(papel=papel, path=str(p), ausente=True))
bat = json.loads((R2 / "BATERIA_VINCULO.json").read_bytes())
for t in bat["testes"]:
    for f in t.get("fontes", []):
        p = Path(f["path"])
        s = sha(p) if p.is_file() else None
        out["fontes_da_bateria"].append(dict(teste=t["id"], path=str(p), sha256_pinado=f["sha256"], sha256_disco=s, confere=(s == f["sha256"])))
for c in bat.get("copias", []):
    p = Path(c["de"])
    s = sha(p) if p.is_file() else None
    out["fontes_da_bateria"].append(dict(teste="copias", path=str(p), sha256_pinado=c["sha256"], sha256_disco=s, confere=(s == c["sha256"])))
out["n_entradas"] = len(out["entradas"])
out["n_ausentes"] = sum(1 for e in out["entradas"] if e.get("ausente"))
out["n_fontes_da_bateria"] = len(out["fontes_da_bateria"])
out["n_fontes_que_conferem"] = sum(1 for e in out["fontes_da_bateria"] if e["confere"])
out["nota"] = "sha256 lidos por script em %s; o livro de eventos e vivo; nada aqui move o gate" % out["quando"]
(AQUI / "PINOS_R3.json").write_bytes(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({k: out[k] for k in ("n_entradas", "n_ausentes", "n_fontes_da_bateria", "n_fontes_que_conferem")}))
