# -*- coding: utf-8 -*-
"""Registro de 02/11/2026: ratificacao do operador (perda = coerencia; sexta morada fechada), K como o operador '=' e a candidata. Backup de bytes. Nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_K_faz_a_funcao_do_graviton_operador_igual_que_criva_verbatim.txt"
CAND = AQUI / "OIgualCandidata.lean"
SAI = AQUI / "OIgualCandidata_saida.txt"
for a, b in (("C:/t/igual02nov/OIgualCandidata.lean", CAND), ("C:/t/igual02nov/saida2.txt", SAI)):
    if not b.exists():
        shutil.copyfile(a, b)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
fo, fc = s16(ORD), s16(CAND)
print("fala", fo, "candidata", fc)
NOTA = AQUI / "DERIVACAO_RE_02nov.md"

reg = [{"tipo": "ROTA", "rota_id": "kernel.k_operador_igual_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
        "titulo": "Candidata: K como o operador '=': tres leis, holonomia trivial, crivo com testemunha unica; omega(I)=1 proibe K global",
        "pergunta": "K faz a funcao do graviton, o operador '=' que criva?",
        "metodo": "sandbox k405c, lake env lean, importando Cocycle, TheFlowLawContrast e LeiDoDiminuto; kernel selado intocado", "olhou_dados": False,
        "resultado": "12 teoremas no trio, 0 sorry, 1 aviso cosmetico de linter. K_refl, K_symm, K_trans, K_triangle, leitura_norm, leitura_chain, a_face_em_menos_i, K_e_a_lei, o_crivo_tem_testemunha_unica, cociclo_de_um_escalar, escalar_entre_normalizados_e_um, o_fundo_e_a_media.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__K_SO_ENTRE_SETOR_E_TODO__K_RENORMALIZA_NAO_DESLOCA__LEITURA_GRAVITON_ONTO__NOME_DO_OPERADOR_PENDENTE",
        "defeito": "as tres leis valem para qualquer razao f(b)/f(a): barra baixa; a taxa zero do que vazou e leitura; a ponte com o cociclo vale entre pesos, nao entre estados normalizados; nao resolve a regua; K de Hubble, K modular e K_beta sao homonimos",
        "proximo_passo": "leitura do operador sobre o setor de 7,7%; nome; decisao de versao", "refs": ["hubble.k_sem_portador_fisico_02nov"], "artefatos": [str(CAND), str(SAI), str(ORD)]},
       {"tipo": "ANOTACAO", "rota_id": "hubble.k_sem_portador_fisico_02nov", "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "Ratificado pelo operador: a perda e de coerencia; a sexta morada fecha. As seis moradas caem como portador; K passa a relacao entre setor e todo",
        "resultado": "Fala sha16 %s, 'E isso mesmo'. K nao desloca os picos: renormaliza pelo peso sobrevivente. Falta dizer o que e o setor de 7,7%% e por que a leitura pela regua e a media." % fo,
        "estatuto": "INPUT", "artefatos": [str(ORD), str(CAND)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_igual_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-240:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-operador-igual", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "k_operador_igual_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: ratificou perda = coerencia; K faz a funcao do graviton, o operador '=' que criva.", "sources": [SRC(ORD)]},
                                {"id": "candidata_o_igual_02nov", "kind": "fact", "statute": "REAL", "text": "Candidata no sandbox: 12 teoremas, trio, 0 sorry. omega(I)=1 proibe K como fator global entre estados normalizados; K e razao entre setor e todo; fundo = media, local = condicionada. Fora do kernel selado.", "sources": [SRC(CAND)]},
                                {"id": "residuo_setor_7p7_02nov", "kind": "pending", "statute": "OPEN", "text": "Leitura do operador: o que e o setor vazado de 7,7%, e por que a leitura pela regua e a media?", "sources": [SRC(CAND)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

TOP = M / "vazar-e-luzir-02nov.md"
b = TOP.read_bytes()
add = f"""

## 02/11/2026 — ratificação e K como o operador «=»

**Verbatim:** `work{BK}cunhagens_13out{BK}{ORD.name}` (sha16 `{fo}`): «É isso mesmo, mas agora o K me pareceu fazer a função do próprio gráviton (que antes eu disse ser o operador "=", aquele que criva)». Ratifica: perda = coerência; a sexta morada fecha.

**Candidata [REAL no sandbox]:** `work{BK}rota_RE_dualidade_02nov{BK}OIgualCandidata.lean` (sha16 `{fc}`), 12 teoremas, trio, 0 sorry, fora do kernel selado, nome dele. O que pesa: a fórmula de K só tem E(z), sem luz; holonomia trivial (a objeção de Einstein a Weyl não o atinge); crivo com testemunha única; **`escalar_entre_normalizados_e_um`: ω(I) = 1 proíbe K como fator global**, logo K é razão entre setor e todo; **`o_fundo_e_a_media`: K não desloca, renormaliza**.

**Limites:** as três leis são barra baixa (toda razão as obedece); a taxa zero do que vazou é leitura; a ponte com o cociclo vale entre pesos, não entre estados normalizados; a régua segue sem derivação; K de Hubble, K modular e K_β são homônimos. **Resíduo com ele:** o que é o setor de 7,7%.
"""
add = add.replace("\n", "\r\n") if b"\r\n" in b else add
bak = TOP.with_name(TOP.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(b)
tmp = TOP.with_name(TOP.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(b + add.encode("utf-8"))
assert tmp.stat().st_size > len(b)
os.replace(tmp, TOP)
print("topico", len(b), "->", TOP.stat().st_size)

n = NOTA.read_bytes()
ad = f"""

## Ao lado (02/11/2026, gerência c1)

O operador ratificou que a perda é de coerência (fala sha16 `{fo}`): a sexta morada fecha, e as seis caem como portador físico. K passa a relação: `escalar_entre_normalizados_e_um` mostra que ω(I) = 1 proíbe K como fator global, e `o_fundo_e_a_media` lê o fundo como média e o local como média condicionada. K não desloca os picos: renormaliza. Falta dizer o que é o setor de 7,7% e por que a leitura pela régua é a média. Candidata: `OIgualCandidata.lean` (sha16 `{fc}`).
"""
bak = NOTA.with_name(NOTA.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(n)
tmp = NOTA.with_name(NOTA.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(n + ad.encode("utf-8"))
os.replace(tmp, NOTA)

REG = ("\n### 02/11/2026 — K como o operador «=» (fala do operador, candidata da gerência) <!-- k_operador_igual_02nov -->\n\n"
       "**[INPUT]** verbatim sha16 `%s`: K faz a função do gráviton, o operador «=» que criva; ratifica perda = coerência. **[REAL no sandbox]** candidata sha16 `%s`, 12 teoremas, trio, 0 sorry, fora do kernel selado: três leis do «=» (barra baixa), holonomia trivial, crivo com testemunha única, ω(I) = 1 proíbe K global. **[ONTO]** K renormaliza pelo peso sobrevivente: o fundo é a média; o local, a condicionada. **[OPEN]** o setor de 7,7%%; a régua.\n" % (fo, fc))
A = CEN / "memory/TGL_ATLAS.md"
ba = A.read_bytes()
nl = "\r\n" if b"\r\n" in ba else "\n"
bak = A.with_name(A.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(ba)
assert bak.read_bytes() == ba
tmp = A.with_name(A.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(ba.rstrip() + (nl + REG.replace("\n", nl)).encode("utf-8"))
assert tmp.stat().st_size > len(ba)
os.replace(tmp, A)
print("atlas", len(ba), "->", A.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:80])
