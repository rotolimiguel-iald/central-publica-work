# -*- coding: utf-8 -*-
"""02/11/2026: revisão Sonnet das três pedras candidatas recebida e conferida; reparos de docstring aplicados; ERRATA AO LADO da
frase da gerência «o espectro pontual da luz é o Um e só ele; o resto é contínuo» (o termo prova o único vetor FIXO). Registro:
Mapa, memória, Atlas, plano. Backup de bytes."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
REV = AQUI / "revisoes/REVISAO_PEDRAS_CANDIDATAS_02nov_SONNET.md"
PLANO = AQUI / "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md"
A = Path(r"C:\t\crivo02nov\KEhATangenteCandidata.lean"); B = Path(r"C:\t\ponte02nov\APonteDoAtritoCandidata.lean"); C = Path(r"C:\t\ponte02nov\OUmInscritoCandidata.lean")
frev, fa, fb, fc = s16(REV), s16(A), s16(B), s16(C)
print("revisao", frev, "A", fa, "B", fb, "C", fc)

def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if b"\r\n" in b: add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS); open(bk, "xb").write(b); assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4; os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)

reg = [
 {"tipo": "ANOTACAO", "rota_id": "conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov", "dominio": "CONCEITUAL",
  "titulo": "ERRATA da gerência (02/11, após revisão Sonnet): o termo prova o ÚNICO VETOR FIXO da luz; «único autovetor» e «o espectro pontual é o Um e só ele; o resto é contínuo» afirmaram demais",
  "resultado": "Revisão sha16 %s (171 linhas; 7 reparos; nenhuma pedra reprovada). Conferido no kernel: gamma_no_fixed conclui ψ ∈ reta do vácuo para ψ FIXO (autovalor 1 do grupo); autovetor com fase (Γ(B0 s)ψ = c(s)ψ) em setores n ≥ 1 não é excluído por termo; «o resto é contínuo» é [KNOWN/OPEN como termo]. Mesmo fato no certificado: light_modular_fixed_iff_vacuum (QGReaderUVLock.lean:149), condicional a C; a candidata vale no Fock concreto sem hipótese. Docstrings da candidata C reparadas (sha16 %s); recompilação em curso." % (frev, fc),
  "estatuto": "REAL (revisão conferida)", "artefatos": [str(REV), str(C)]},
 {"tipo": "ANOTACAO", "rota_id": "kernel.k_e_a_tangente_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Revisão Sonnet (02/11): nenhum teorema errado; reparos de docstring aplicados (θ = π/4 é teorema em toda transição, logo K = 1 sempre; o ½ segue escrito; genK/«posto» homônimos ditos)",
  "resultado": "Revisão sha16 %s. Conferido: theta_eq_pi_div_four é teorema derivado do campo autoconjugado (PonteDaMassa.lean:147); no_posto_o_acorde_e_a_projecao repete massa_derivada_eq_projecao (l.181); o_angulo_e_lido_do_absoluto é coincidência de valor, não ponte (l.245-246, 275-276). Candidata A reparada (sha16 %s); recompilação em curso." % (frev, fa),
  "estatuto": "REAL", "artefatos": [str(REV), str(A)]},
 {"tipo": "ANOTACAO", "rota_id": "kernel.a_ponte_do_atrito_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Revisão Sonnet (02/11): reparos de docstring aplicados (a ponte e o balanço são triviais por definição, ditos; «Clausius» é forma por definição; κ/2π é «normalização herdada (sem Unruh/KMS)» no kernel; limite genérico em q; g e κ livres)",
  "resultado": "Revisão sha16 %s. Conferido: BoostHeatConstruction.lean:16 chama κ/2π «normalizacao herdada (sem Unruh/KMS)»; the_charge_is_continuous_both_sides é TRIVIAL POR DEFINIÇÃO no kernel. Candidata B reparada (sha16 %s); recompilação em curso. Nenhuma prova mudou." % (frev, fb),
  "estatuto": "REAL", "artefatos": [str(REV), str(B)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_rev_pedras_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-90:].replace("\n", " ")); assert q.returncode == 0

ERR = f"""

## ERRATA AO LADO, 3ª (02/11/2026, noite; gerência c1 em nome próprio; achado da revisão Sonnet das pedras, sha16 `{frev}`)

Na 1ª errata escrevi «o espectro pontual da luz é o Um e só ele; o resto é contínuo». Afirmei demais. O termo (`gamma_no_fixed`, e a candidata `o_um_e_o_unico_fixo_da_luz`) prova que o Um é o único vetor FIXO da luz (autovalor 1 do grupo Γ(B0 s)); autovetor com fase em setores de n ≥ 1 partículas não foi excluído por termo, e «o resto é contínuo» é [KNOWN/OPEN como termo]. No certificado o mesmo fato é `light_modular_fixed_iff_vacuum` (QGReaderUVLock.lean:149), condicional a C. A pista para 1.7 não muda (o P_F parte da inscrição). Reparos de docstring nas três candidatas aplicados (A `{fa}`, B `{fb}`, C `{fc}`); nenhuma prova mudou; recompilação em curso.
"""
append_bytes(PLANO, ERR)
append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

**02/11, noite — revisão Sonnet das três pedras (sha16 `{frev}`): nenhuma reprovada; 7 reparos de docstring aplicados (A `{fa}`, B `{fb}`, C `{fc}`; recompilação em curso).** ERRATA minha: «o espectro pontual da luz é o Um e só ele; o resto é contínuo» afirmou demais; o termo prova o único vetor FIXO; autovetor com fase não é excluído por termo. **How to apply:** dizer «o único vetor fixo da luz é o Um inscrito»; em toda `TransicaoParaAMassa` θ = π/4 é teorema (K = 1 sempre); κ/2π é «normalização herdada (sem Unruh/KMS)» no kernel; «Clausius» nas pedras é forma por definição.
""")
append_bytes(M / "a-identidade-tem-nome-13out.md", f"""

**Ao lado (02/11, noite, gerência c1):** «o único autovetor» acima lê-se «o único vetor FIXO» (`gamma_no_fixed`); autovetor com fase não é excluído por termo (revisão Sonnet sha16 `{frev}`).
""")
append_bytes(CEN / "memory/TGL_ATLAS.md", f"""
### 02/11/2026 — AO LADO (gerência c1, em nome próprio): «o único autovetor da luz» lê-se «o único vetor FIXO» <!-- errata_vetor_fixo_da_luz_02nov -->

Revisão Sonnet das pedras candidatas (sha16 `{frev}`): `gamma_no_fixed` conclui para vetores FIXOS (autovalor 1 do grupo); autovetor com fase em setores n ≥ 1 não é excluído por termo; «o espectro pontual é o Um e só ele; o resto é contínuo» (registro de 02/11) é [KNOWN/OPEN como termo]. No certificado: `light_modular_fixed_iff_vacuum`. Docstrings das três candidatas do dia reparadas; nenhuma prova mudou.
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
