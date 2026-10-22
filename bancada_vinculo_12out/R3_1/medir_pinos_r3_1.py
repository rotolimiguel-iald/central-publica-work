# -*- coding: utf-8 -*-
"""medir_pinos_r3_1.py (R3.1, 13/10/2026) -- mede POR SCRIPT o sha256 de tudo o que a R3.1 cita (nunca de memoria) e grava R3_1/PINOS_R3_1.json.
So le fora de R3_1. Confere as fontes pinadas na bateria contra o disco e os pinos da base R3 citados na ordem. uso: medir_pinos_r3_1.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
V = AQUI.parent
R3 = V / "R3"
R2 = V / "R2"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
AUD = Path("C:/IALD/PROGRAMA_IALD/auditorias/F0.6")
ENTRADAS = [
    ("R3.1: o esboco", AQUI / "sincronizar_bancada.py"),
    ("R3.1: o montador do sandbox", AQUI / "montar_sandbox.py"),
    ("R3.1: os controles negativos", AQUI / "controles_negativos_r3_1.py"),
    ("R3.1: este medidor", AQUI / "medir_pinos_r3_1.py"),
    ("R3.1: o resultado dos controles", AQUI / "CONTROLES_NEGATIVOS_R3_1.json"),
    ("R3.1: o contrato do recibo do kernel", AQUI / "CONTRATO_KERNEL_RECIBO_R3_1.md"),
    ("R3.1: o modelo dos criterios (A3)", AQUI / "CRITERIOS_V392.json"),
    ("R3.1: as remissoes ao lado", AQUI / "REMISSOES_PLANO_R3_1.md"),
    ("R3.1: o diff R3 -> R3.1 (os .py)", AQUI / "DIFF_R3_R3_1.patch"),
    ("R3.1: a verificacao do diff", AQUI / "VERIFICACAO_DIFF_R3_1.json"),
    ("R3.1: o resultado", AQUI / "RESULTADO_R3_1.md"),
    ("R3.1: rodada 1 dos controles (registro; 336/337 por defeito do controle)", AQUI / "CONTROLES_NEGATIVOS_R3_1_rodada1_336de337.json"),
    ("R3.1: rodada 2 dos controles (registro; 336/337 por defeito do controle)", AQUI / "CONTROLES_NEGATIVOS_R3_1_rodada2_336de337.json"),
    ("R3.1: construcao, gerador do diff", AQUI / "_construcao" / "gerar_diff_r3_1.py"),
    ("R3.1: construcao, limpeza do sandbox", AQUI / "_construcao" / "limpar_sandbox.py"),
    ("R3.1: construcao, stdout da rodada 1", AQUI / "_construcao" / "controles_stdout_rodada1.txt"),
    ("R3.1: construcao, stdout da rodada 2", AQUI / "_construcao" / "controles_stdout_rodada2.txt"),
    ("R3.1: a referencia da memoria ACOM", AQUI / "_memoria" / "REFERENCIA_R3_1.json"),
    ("R3.1: construcao, patch do esboco", AQUI / "_construcao" / "patch_sync_r3_1.py"),
    ("R3.1: construcao, patch do montador", AQUI / "_construcao" / "patch_montar_r3_1.py"),
    ("R3.1: construcao, patch dos controles", AQUI / "_construcao" / "patch_controles_r3_1.py"),
    ("R3.1: construcao, bloco do kernel", AQUI / "_construcao" / "bloco_kernel_r3_1.py.txt"),
    ("R3.1: construcao, bloco do ambiente", AQUI / "_construcao" / "bloco_ambiente_r3_1.py.txt"),
    ("R3.1: construcao, bloco A4", AQUI / "_construcao" / "bloco_a4_r3_1.py.txt"),
    ("R3.1: construcao, bloco do decoy", AQUI / "_construcao" / "bloco_decoy_r3_1.py.txt"),
    ("R3.1: construcao, bloco pos-run 2", AQUI / "_construcao" / "bloco_pos_run2_r3_1.py.txt"),
    ("R3.1: construcao, bloco do fecho", AQUI / "_construcao" / "bloco_fecho_r3_1.py.txt"),
    ("R3.1: a inscricao da tarefa (memoria ACOM)", AQUI / "_memoria" / "ORIGEM_R3_1.md"),
    ("R3 (base, registro): o esboco", R3 / "sincronizar_bancada.py"),
    ("R3 (base, registro): o montador", R3 / "montar_sandbox.py"),
    ("R3 (base, registro): os controles", R3 / "controles_negativos_r3.py"),
    ("R3 (base, registro): o resultado dos controles", R3 / "CONTROLES_NEGATIVOS_R3.json"),
    ("R3 (base, registro): o contrato do recibo do kernel", R3 / "CONTRATO_KERNEL_RECIBO.md"),
    ("R3 (base, registro): as remissoes", R3 / "REMISSOES_PLANO_R3.md"),
    ("R3 (base, registro): os pinos", R3 / "PINOS_R3.json"),
    ("R2: a bateria (vigente, inalterada)", R2 / "BATERIA_VINCULO.json"),
    ("R2: o gerador de canais (inalterado)", R2 / "gerar_canais_mcp.py"),
    ("a reauditoria curta da R3 (resumo)", AUD / "AUDITORIA_F0_6_C1_a61fad96.md"),
    ("a reauditoria curta da R3 (relatorio)", AUD / "art_a61fad96" / "AUDITORIA_VINCULO_R3_C1.md"),
    ("a reauditoria curta da R3 (os ataques)", AUD / "art_a61fad96" / "ATAQUES_R3_AUDITOR.json"),
    ("a reauditoria curta da R3 (o script dos ataques)", AUD / "art_a61fad96" / "ataques_r3.py"),
    ("o plano da v392", Path("C:/IALD/PROGRAMA_IALD/exame_12out/J_SINTESE/PLANO_V392.md")),
    ("a amostra REAL do aviso de sorry (Nos, so lido)", NOS / "bancada_corpus" / "ChainSiteOperators.20260905_150729.falha_lean.log"),
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
            ENTRADAS.append(("R3.1: evidencia do sandbox (copia; o sandbox foi apagado)", p))
BASE_ESPERADA = {"sincronizar_bancada.py": "8894b74cb1e6d5a0", "montar_sandbox.py": "518cd2af4f67093b", "controles_negativos_r3.py": "9815086af0547a7f"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.1 (13/10/2026)", entradas=[], fontes_da_bateria=[],
           base_R3_conferida={n: dict(esperado16=e, disco=sha(R3 / n), confere=sha(R3 / n).startswith(e)) for n, e in BASE_ESPERADA.items()})
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
out["ausentes"] = [e["path"] for e in out["entradas"] if e.get("ausente")]
out["n_fontes_da_bateria"] = len(out["fontes_da_bateria"])
out["n_fontes_que_conferem"] = sum(1 for e in out["fontes_da_bateria"] if e["confere"])
out["nota"] = "sha256 lidos por script em %s; o livro de eventos e vivo; nada aqui move o gate" % out["quando"]
dados = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
destino = AQUI / "PINOS_R3_1.json"
tmp = destino.with_name(destino.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(destino)
print(json.dumps({k: out[k] for k in ("n_entradas", "n_ausentes", "ausentes", "n_fontes_da_bateria", "n_fontes_que_conferem")}),
      json.dumps({k: v["confere"] for k, v in out["base_R3_conferida"].items()}))
