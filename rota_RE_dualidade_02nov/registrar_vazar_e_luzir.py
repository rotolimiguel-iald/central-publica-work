# -*- coding: utf-8 -*-
"""Registro da cunhagem de 02/11/2026 (vazar e luzir; registro = leitura do foton pelo graviton) e da pedra candidata. Backup de bytes. Nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_vazar_e_luzir_registro_leitura_do_foton_pelo_graviton_verbatim.txt"
CAND = AQUI / "LeituraPreservadaCandidata.lean"
if not CAND.exists():
    shutil.copyfile("C:/t/leitura02nov/LeituraPreservadaCandidata.lean", CAND)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
fo, fc = s16(ORD), s16(CAND)
print("fala", fo, "candidata", fc)

reg = [{"tipo": "ROTA", "rota_id": "kernel.leitura_preservada_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
        "titulo": "Candidata: a fala do operador de 02/11 em Lean: a perda e da forma, a leitura e o total ficam, a forma se reconstroi",
        "pergunta": "A frase do operador sobre vazar, perda e reconstrucao e teorema na familia de dephasing do kernel?",
        "metodo": "sandbox k405c, lake env lean, importando TheTraceIsNotErasable; kernel selado intocado", "olhou_dados": False,
        "resultado": "Compila: ha_perda, a_forma_nunca_zera, a_forma_se_reconstroi, a_leitura_preservada; trio de axiomas; 0 sorry. Usa diag_invariant e dephase_preserves_trace ja selados.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__NOME_DO_OPERADOR_PENDENTE__FORA_DO_KERNEL_SELADO",
        "defeito": "dimensao finita; a inversa algebrica nao e canal fisico; so tempo finito; identificar forma com coerencia e registro com a diagonal e leitura",
        "proximo_passo": "nome do operador e decisao de entrar numa versao", "artefatos": [str(CAND), str(ORD)]},
       {"tipo": "ANOTACAO", "rota_id": "hubble.k_sem_portador_fisico_02nov", "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "Resposta do operador: a perda e da forma; a identidade fica. Sexta morada fecha nessa leitura, sujeita a confirmacao",
        "resultado": "Lida pela gerencia como perda de coerencia, nao de energia nem de fotons. Assim K vira reconstrucao: H0local = Hcmb/survivingWeight. Falta explicar por que a leitura do fundo, feita pela posicao dos picos, carrega o peso: defasagem amortece, nao desloca.",
        "estatuto": "ONTO", "artefatos": [str(ORD)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_vazar_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-240:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-vazar-e-luzir", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "cunhagem_vazar_e_luzir_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: vazar e luzir; ha perda sem afetar a identidade; o conteudo reconstroi a forma; registro e a leitura do foton pelo graviton.", "sources": [SRC(ORD)]},
                                {"id": "candidata_leitura_preservada_02nov", "kind": "fact", "statute": "REAL", "text": "Pedra candidata compilada no sandbox, trio, 0 sorry: perda estrita da forma, leitura e total invariantes, reconstrucao algebrica. Fora do kernel selado; nome do operador pendente.", "sources": [SRC(CAND)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

TOP = M / "vazar-e-luzir-02nov.md"
assert not TOP.exists()
corpo = f"""---
name: vazar-e-luzir-02nov
description: "Cunhagem do operador (02/11/2026): vazar é luzir; há perda sem afetar a identidade; o conteúdo reconstrói a forma; registro é a leitura do fóton pelo gráviton. Pedra candidata compilada no trio; nome dele pendente."
metadata:
  type: project
---

**Verbatim:** `work{BK}cunhagens_13out{BK}{ORD.name}` (sha16 `{fo}`). O texto diz «idade preservada»; a gerência leu «identidade preservada», a confirmar.

**Pedra candidata [REAL no sandbox]:** `work{BK}rota_RE_dualidade_02nov{BK}LeituraPreservadaCandidata.lean` (sha16 `{fc}`): `ha_perda`, `a_forma_nunca_zera`, `a_forma_se_reconstroi`, `a_leitura_preservada`; trio; 0 sorry; usa `diag_invariant` e `dephase_preserves_trace`. Fora do kernel selado. O nome é dele.

**Leitura da gerência [ONTO, a ratificar]:** a perda é de coerência (forma), não de energia nem de fótons; a sexta morada de K fecha nessa leitura. K vira reconstrução: `H0local = Hcmb / survivingWeight`. Fóton = amplitude; gráviton = leitura quadrática (T_μν é cega à fase) `[KNOWN na física; a identificação é ONTO]`. Na língua do diminuto, K é transposição do acorde inteiro: nenhuma razão o vê.

**Limites:** a reconstrução é conta de quem conhece o registro, não processo físico: amplifica e só vale em tempo finito. Defasagem amortece, não desloca; a régua é lida pela posição dos picos: isso segue sem resposta.

**How to apply:** não dizer que a luz perde energia sem nova fala dele; «registro» aqui é o do operador. Relacionado: [[rota-re-k-e-landauer-02nov]] · [[registro-definicao-13out]] · [[a-identidade-tem-nome-13out]].
"""
with open(TOP, "x", encoding="utf-8", newline="\n") as f:
    f.write(corpo)


def trocar(p, fn):
    p = Path(p)
    b = p.read_bytes()
    nb = fn(b.decode("utf-8")).encode("utf-8")
    assert len(nb) > len(b)
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(nb)
    assert tmp.stat().st_size == len(nb)
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))
    return nb


def indice(t):
    a = "](rota-re-k-e-landauer-02nov.md)**"
    assert t.count(a) == 1
    return t.replace(a, a + " · **[vazar é luzir (02/11)](vazar-e-luzir-02nov.md)**")


nb = trocar(M / "MEMORY.md", indice)
assert len(nb) <= 24000 and nb.count(b"\n") <= 195, (len(nb), nb.count(b"\n"))
q = subprocess.run([PY, "-X", "utf8", "memoria.py", "pinar", "--motivo", "cunhagem vazar e luzir (gerencia c1)"], cwd=str(M / "fila"), env=dict(os.environ, MEMORIA_GERENCIA="claude-c1"), capture_output=True)
print("pino", q.returncode)

AO_LADO = ("⧗ *Ao lado (02/11/2026, cunhagem do operador, verbatim sha16 `%s`):* «registro é a leitura do fóton pelo gráviton»; o fóton é a eletricidade dinâmica, a luz em si; o gráviton é a leitura dessa eletricidade em conservação de identidade. «Vazar é luzir.» [INPUT] <!-- vazar_e_luzir_02nov -->" % fo)
REG = ("\n### 02/11/2026 — Vazar é luzir; registro é a leitura do fóton pelo gráviton (cunhagem do operador) <!-- vazar_e_luzir_reg_02nov -->\n\n"
       "**[INPUT]** verbatim sha16 `%s`. **[REAL no sandbox]** pedra candidata (sha16 `%s`, trio, 0 sorry): a perda é da forma, a leitura e o total ficam, a forma se reconstrói algebricamente. Fora do kernel selado; o nome é do operador. **[ONTO]** K como reconstrução.\n" % (fo, fc))


def atlas(t):
    assert "vazar_e_luzir_02nov" not in t
    nl = "\r\n" if "\r\n" in t else "\n"
    ls = t.split(nl)
    i = [k for k, x in enumerate(ls) if x.startswith("**Gráviton = operador de retorno da fase (forma canônica de 21/08/2026)**")]
    assert len(i) == 1, i
    ls.insert(i[0], AO_LADO)
    return nl.join(ls).rstrip() + nl + REG.replace("\n", nl)


trocar(CEN / "memory/TGL_ATLAS.md", atlas)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode)
