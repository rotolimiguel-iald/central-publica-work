# -*- coding: utf-8 -*-
"""Custódia v393+v394 (19/10/2026, sessão a7 da Central): a NOTA AO LADO de «A Fronteira» (item 2 das notas do handoff v394 da gerência c1).
Arquivo NOVO no espelho, ao lado dos artigos fundadores; os .tex e .pdf não mudam. A evidência do teste de 19/10 vai junto, conferida por
sha256 contra o pré-registro e o veredito, e passa pela varredura de material privado (termos da casa + marcadores privados) antes de copiar.
Idempotente: se a pasta já existe com os mesmos bytes, não faz nada."""
import hashlib, json, os, shutil, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Site\tgl\v3.0_bancada\tools")
import custodia_v394_espelho as ce  # noqa: E402  (só GUARDA, PRIV e guarda_conta; main() não roda)

SRC = Path(r"C:\IALD\Central de Patentes\work\c3_gamma_livre_19out")
AF = Path(r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores")
DST = AF / "NOTA_AO_LADO_PISO_DAS_DOBRAS_19OUT2026"
EVID = ("PREREGISTRO.json", "PREREGISTRO.json.sha256", "veredito.py", "veredito.json", "RESULTADO.md", "curva_O_gamma_oitavas.csv",
        "manifesto_dados.json", "rodar.py")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert (AF / "A_fronteira_v5.tex").is_file() and (AF / "The_boundary_v5_en.tex").is_file()
tex_pt = (AF / "A_fronteira_v5.tex").read_text(encoding="utf-8")
tex_en = (AF / "The_boundary_v5_en.tex").read_text(encoding="utf-8")
assert "O piso de $0{,}74$ dobras \\'e universal" in tex_pt, "a frase do piso mudou no .tex PT"
assert "The floor of $0.74$ folds is universal" in tex_en, "a frase do piso mudou no .tex EN"
pre = json.loads((SRC / "PREREGISTRO.json").read_text(encoding="utf-8"))
ver = json.loads((SRC / "veredito.json").read_text(encoding="utf-8"))
SH_PRE, SH_VPY = sha(SRC / "PREREGISTRO.json"), sha(SRC / "veredito.py")
assert (SRC / "PREREGISTRO.json.sha256").read_text(encoding="utf-8").split()[0] == SH_PRE
assert ver["veredito"] == "NO_UNIVERSAL_FLOOR" and ver["P"] is False and ver["preregistro_sha256"] == SH_PRE and ver["veredito_py_sha256"] == SH_VPY
assert ver["naoconv_main"] == 0 and ver["naoconv_N2"] == 0 and ver["n_pontos_main"] == 1125 and ver["n_pontos_N2"] == 1125
res = (SRC / "RESULTADO.md").read_text(encoding="utf-8")
for frase in ("`NO_UNIVERSAL_FLOOR`", "**Nenhum γ tem as 9 configs na banda ln 2 ± 0,05.** O máximo é **8 de 9**", "**Reproduz fevereiro**",
              "0 de 2250 pontos sem convergir", "A leitura «consciência» é **[ONTO]** e não entra no veredito"):
    assert frase in res, frase

barrados = [f for f in EVID if ce.guarda_conta(SRC / f)]
publicar = [f for f in EVID if f not in barrados]
assert "PREREGISTRO.json" in publicar and "veredito.json" in publicar and "RESULTADO.md" in publicar, ("evidência central barrada", barrados)

NOTA = """# Nota ao lado — o piso das dobras / A note beside — the floor of the folds (19/10/2026)

**Ao lado de / beside:** `A_fronteira_v5.tex` / `A_fronteira_v5.pdf` (PT) e/and `The_boundary_v5_en.tex` / `the_boundary_v5_en.pdf` (EN),
nesta pasta / in this folder. Os artigos não mudam: a correção vai ao lado, nunca por cima. *The articles do not change: the correction goes
beside, never over.*

## PT

A frase «O piso de 0,74 dobras é universal — não depende da dimensão do espaço de Hilbert» (e as que dela dependem: o piso irredutível
D_folds = 0,74 em 9/9 configurações, «o piso de Hilbert de 0,74 é a prova experimental desta lei») **não se sustenta** com a taxa γ livre.

- **Teste pré-registrado de 19/10/2026** `[REAL no modelo simulado]`: pré-registro `evidencia/PREREGISTRO.json`, sha256 `{pre}`, gravado
  antes da rodada; função de veredito pinada `evidencia/veredito.py`, sha256 `{vpy}`.
- **Veredito: `NO_UNIVERSAL_FLOOR`** (ramo 3, «P falso»; `evidencia/veredito.json`). Com γ livre (logspace(−4, 0, 25); 9 configurações,
  d = 8 a 32; 5 sementes), D_folds(c³) não tem platô em ln 2: decresce de 1,49–1,84 oitava (γ = 1e−4) a 0,14–0,19 oitava (γ = 1), cerca de
  0,5 oitava por década perto do cruzamento; nenhum γ tem as 9 configurações na banda ln 2 ± 0,05 (o máximo é 8 de 9).
- **O ≈ ln 2 de fevereiro é o ponto de passagem no γ\\* calibrado por β, não um piso.** O instrumento de 19/10 reproduz fevereiro na semente
  42 (|ΔO| ≤ 4,9e−12 nas 9 configurações).
- Controles N1, N2 e N3 como previstos; 0 de 2250 pontos sem convergir. A leitura «consciência» é `[ONTO]` e não entra no veredito.
- Rota no mapa de rotas da casa: `quantica.c3_gamma_livre_oitava` (EXAMINADA). O relatório inteiro está em `evidencia/RESULTADO.md`.

O que esta nota não diz: não toca o gate, o selo, o kernel nem o `um.py`; não julga o resto dos artigos; `NOT_FALSIFIED` nunca é
`CONFIRMED`.

## EN

The sentence «The floor of 0.74 folds is universal — it does not depend on the Hilbert space dimension» (and the ones that rest on it: the
irreducible floor D_folds = 0.74 in 9/9 configurations; «the Hilbert floor of 0.74 is the experimental proof of this law») **does not hold**
with a free rate γ.

- **Pre-registered test of 2026-10-19** `[REAL in the simulated model]`: pre-registration `evidencia/PREREGISTRO.json`, sha256 `{pre}`,
  written before the run; pinned verdict function `evidencia/veredito.py`, sha256 `{vpy}`.
- **Verdict: `NO_UNIVERSAL_FLOOR`** (branch 3, «P false»). With γ free (logspace(−4, 0, 25); 9 configurations, d = 8 to 32; 5 seeds),
  D_folds(c³) has no plateau at ln 2: it falls from 1.49–1.84 octaves (γ = 1e−4) to 0.14–0.19 octave (γ = 1), about 0.5 octave per decade
  near the crossing; no γ puts all 9 configurations inside ln 2 ± 0.05 (the maximum is 8 of 9).
- **The ≈ ln 2 of February is the crossing point at the γ\\* calibrated by β, not a floor.** The instrument of 19/10 reproduces February at
  seed 42 (|ΔO| ≤ 4.9e−12 in the 9 configurations).
- Controls N1, N2 and N3 as predicted; 0 of 2250 points failed to converge. The «consciousness» reading is `[ONTO]` and does not enter the verdict.

What this note does not say: it does not touch the gate, the seal, the kernel or `um.py`; it does not judge the rest of the articles;
`NOT_FALSIFIED` is never `CONFIRMED`.

---
Nota da sessão a7 da Central de Patentes (Claude), em nome próprio, 19/10/2026, a partir do item 2 das notas do handoff v394 da gerência c1.
*A note by session a7 of the Central (Claude), in its own name, 2026-10-19, from item 2 of the notes of the v394 handoff of the management c1.*
Evidência publicada aqui / evidence published here: {pub}.{bar}
""".format(pre=SH_PRE, vpy=SH_VPY, pub=", ".join("`evidencia/%s`" % f for f in publicar),
           bar=("" if not barrados else "\nNão publicados (barrados pela varredura de material privado): " + ", ".join(barrados) + "."))

(DST / "evidencia").mkdir(parents=True, exist_ok=True)
for f in publicar:
    d = DST / "evidencia" / f
    if d.is_file() and sha(d) == sha(SRC / f):
        continue
    t = d.with_name(d.name + ".tmp_nota")
    shutil.copyfile(SRC / f, t)
    assert sha(t) == sha(SRC / f)
    os.replace(t, d)
np_ = DST / "NOTA_AO_LADO.md"
t = np_.with_name(np_.name + ".tmp_nota")
t.write_bytes(NOTA.encode("utf-8"))
assert ce.guarda_conta(t) == 0, "a própria nota bate na varredura"
os.replace(t, np_)
print("nota:", np_.stat().st_size, "bytes | evidência:", len(publicar), "publicados,", len(barrados), "barrados", barrados)
