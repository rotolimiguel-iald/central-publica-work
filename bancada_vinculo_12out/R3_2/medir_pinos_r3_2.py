# -*- coding: utf-8 -*-
"""medir_pinos_r3_2.py (R3.2, 13/10/2026) -- mede POR SCRIPT o sha256 de tudo o que a R3.2 cita (nunca de memoria) e grava R3_2/PINOS_R3_2.json.
So le fora de R3_2. Confere as fontes pinadas na bateria contra o disco e os pinos da base R3.1 citados na ordem.
uso: python -I -B -X utf8 medir_pinos_r3_2.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
V = AQUI.parent
R31 = V / "R3_1"
R2 = V / "R2"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
AUD = Path("C:/IALD/PROGRAMA_IALD/auditorias/F0.6")
CUST390 = Path("C:/IALD/Artigo/the_boundary_BACKUPS/um_v390_0f5154bcc2f931cb")
ENTRADAS = [
    ("R3.2: o esboco", AQUI / "sincronizar_bancada.py"),
    ("R3.2: o montador do sandbox", AQUI / "montar_sandbox.py"),
    ("R3.2: os controles negativos", AQUI / "controles_negativos_r3_2.py"),
    ("R3.2: este medidor", AQUI / "medir_pinos_r3_2.py"),
    ("R3.2: o resultado dos controles", AQUI / "CONTROLES_NEGATIVOS_R3_2.json"),
    ("R3.2: o contrato do recibo do kernel", AQUI / "CONTRATO_KERNEL_RECIBO_R3_2.md"),
    ("R3.2: o modelo dos criterios (inalterado desde a R3.1)", AQUI / "CRITERIOS_V392.json"),
    ("R3.2: as remissoes ao lado", AQUI / "REMISSOES_PLANO_R3_2.md"),
    ("R3.2: o diff R3.1 -> R3.2 (os .py)", AQUI / "DIFF_R3_1_R3_2.patch"),
    ("R3.2: a verificacao do diff (core.autocrlf=false)", AQUI / "VERIFICACAO_DIFF_R3_2.json"),
    ("R3.2: o resultado", AQUI / "RESULTADO_R3_2.md"),
    ("R3.2: construcao, patch do montador", AQUI / "_construcao" / "patch_montar_r3_2.py"),
    ("R3.2: construcao, patch dos controles", AQUI / "_construcao" / "patch_controles_r3_2.py"),
    ("R3.2: construcao, bloco R32 dos controles", AQUI / "_construcao" / "bloco_r3_2.py.txt"),
    ("R3.2: construcao, gerador do diff", AQUI / "_construcao" / "gerar_diff_r3_2.py"),
    ("R3.2: construcao, limpeza do sandbox", AQUI / "_construcao" / "limpar_sandbox.py"),
    ("R3.2: construcao, stdout da rodada 1 dos controles", AQUI / "_construcao" / "controles_stdout_rodada1.txt"),
    ("R3.2: construcao, stdout da rodada 2 dos controles (a vigente)", AQUI / "_construcao" / "controles_stdout_rodada2.txt"),
    ("R3.2: rodada 1 dos controles (registro; 397/398: o N5 achou a regressao do -I no sombreaveis)", AQUI / "CONTROLES_NEGATIVOS_R3_2_rodada1_397de398.json"),
    ("R3.2: o registro do mapa (nao registrado; ato da gerencia)", AQUI / "registro_mapa_F0.6_R3_2.json"),
    ("R3.1 (base, registro): o esboco", R31 / "sincronizar_bancada.py"),
    ("R3.1 (base, registro): o montador", R31 / "montar_sandbox.py"),
    ("R3.1 (base, registro): os controles", R31 / "controles_negativos_r3_1.py"),
    ("R3.1 (base, registro): o resultado dos controles", R31 / "CONTROLES_NEGATIVOS_R3_1.json"),
    ("R3.1 (base, registro): o contrato do recibo do kernel", R31 / "CONTRATO_KERNEL_RECIBO_R3_1.md"),
    ("R3.1 (base, registro): as remissoes", R31 / "REMISSOES_PLANO_R3_1.md"),
    ("R3.1 (base, registro): os pinos", R31 / "PINOS_R3_1.json"),
    ("R2: a bateria (vigente, inalterada)", R2 / "BATERIA_VINCULO.json"),
    ("R2: o gerador de canais (inalterado)", R2 / "gerar_canais_mcp.py"),
    ("a reauditoria curta da R3.1 (resumo)", AUD / "AUDITORIA_F0_6_C1_a721b706.md"),
    ("a reauditoria curta da R3.1 (relatorio)", AUD / "art_a721b706" / "AUDITORIA_VINCULO_R3_1_C1.md"),
    ("a reauditoria curta da R3.1 (os ataques)", AUD / "art_a721b706" / "ATAQUES_R3_1_AUDITOR.json"),
    ("a reauditoria curta da R3.1 (o script dos ataques)", AUD / "art_a721b706" / "ataques_r3_1.py"),
    ("a reauditoria curta da R3.1 (as flags do esboco)", AUD / "art_a721b706" / "A4_FLAGS_DO_ESBOCO.json"),
    ("o plano da v392 (com a 12-ter)", Path("C:/IALD/PROGRAMA_IALD/exame_12out/J_SINTESE/PLANO_V392.md")),
    ("a amostra REAL do aviso de sorry (Nos/bancada_corpus, so lido)", NOS / "bancada_corpus" / "ChainSiteOperators.20260905_150729.falha_lean.log"),
    ("custodia v390 (so lida): o build log real", CUST390 / "rodadas" / "tgl_kernel_build_capture.txt"),
    ("custodia v390 (so lida): o log do Audit real", CUST390 / "rodadas" / "tgl_kernel_audit_capture.txt"),
    ("custodia v390 (so lida): o Audit.lean real", CUST390 / "Lean" / "tgl_kernel" / "TGL" / "Audit.lean"),
    ("custodia v390 (so lida): o selo (modelo do --selo-anterior)", CUST390 / "um_absoluto_selo.json"),
    ("custodia v390 (so lida): o manifesto do kernel (modelo do --kernel-manifesto-anterior)", CUST390 / "Lean" / "tgl_kernel_proof_manifest.json"),
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
            ENTRADAS.append(("R3.2: evidencia do sandbox (copia; o sandbox foi apagado)", p))
BASE_ESPERADA = {"sincronizar_bancada.py": "a85be74ffd7a1dee", "montar_sandbox.py": "15c699b5a4fcc83d", "controles_negativos_r3_1.py": "a7614fe341b1461a",
                 "CONTROLES_NEGATIVOS_R3_1.json": "6e27894064399966"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.2 (13/10/2026)", entradas=[], fontes_da_bateria=[],
           base_R3_1_conferida={n: dict(esperado16=e, disco=sha(R31 / n), confere=sha(R31 / n).startswith(e)) for n, e in BASE_ESPERADA.items()})
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
plano = Path("C:/IALD/PROGRAMA_IALD/exame_12out/J_SINTESE/PLANO_V392.md")
out["plano"] = dict(path=str(plano), sha256=sha(plano), linhas=len(plano.read_bytes().splitlines()), tem_12_ter="## 12-ter." in plano.read_text(encoding="utf-8"))
out["n_entradas"] = len(out["entradas"])
out["n_ausentes"] = sum(1 for e in out["entradas"] if e.get("ausente"))
out["ausentes"] = [e["path"] for e in out["entradas"] if e.get("ausente")]
out["n_fontes_da_bateria"] = len(out["fontes_da_bateria"])
out["n_fontes_que_conferem"] = sum(1 for e in out["fontes_da_bateria"] if e["confere"])
out["nota"] = "sha256 lidos por script em %s; o livro de eventos e vivo; nada aqui move o gate" % out["quando"]
dados = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
destino = AQUI / "PINOS_R3_2.json"
tmp = destino.with_name(destino.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(destino)
print(json.dumps({k: out[k] for k in ("n_entradas", "n_ausentes", "ausentes", "n_fontes_da_bateria", "n_fontes_que_conferem")}),
      json.dumps({k: v["confere"] for k, v in out["base_R3_1_conferida"].items()}), json.dumps(out["plano"]))
