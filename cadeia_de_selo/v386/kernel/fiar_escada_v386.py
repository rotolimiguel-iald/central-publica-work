# -*- coding: utf-8 -*-
"""fiar_escada_v386.py -- a FIACAO da pedra do Verbo (v386) na escada do SANDBOX (scratchpad\v376\kernel_src; NUNCA o canonico do Nos).
Le os nomes das declaracoes DA PEDRA (regex sobre o .lean, na ordem do arquivo), confere por grep a existencia de cada termo da fiacao angular
(lista A3 do critico, os 17 nomes da tarefa), e grava, por tempario -> conferir tamanho -> substituir, com backup de bytes ja feito antes:
  (1) TGLExt.lean: `import TGLExt.TheVerbSelectsTheAction` no fim (padrao do TheAxiomAndTheFalseWitness);
  (2) TGL/Audit.lean: bloco `-- 2026-10-05, v386: O VERBO SELECIONA ...` com #print axioms para TODAS as declaracoes da pedra e para os termos
      ja compilados sem auditoria (fiacao do regime angular/dobras/seletor/terminalidade/Verbo-gesto/tensor);
  (3) AUDIT_NOMES_v386.json (nome qualificado, por modulo, na ordem do bloco) e v386_flags.py (_VRB_FLAGS_V386 / _ANG_FLAGS_V386, no formato que
      gerar_candidato_v385.py / extrair_axiomas_v385.py consomem: a bandeira e' o nome EXATO da declaracao, posicao a posicao;
      def/inductive -> _kernel_checked; theorem -> _kernel_proved).
Recusa (assert) se um nome da fiacao nao existir no sandbox, se uma edicao ja tiver sido aplicada, ou se o arquivo encolher."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(os.path.dirname(HERE))
K = os.path.join(SP, "v376", "kernel_src")
STONE = os.path.join(K, "TGLExt", "TheVerbSelectsTheAction.lean")
ROOT = os.path.join(K, "TGLExt.lean")
AUDIT = os.path.join(K, "TGL", "Audit.lean")
NS = "TGLExt.TheVerbSelectsTheAction"
ANCHOR = "-- 2026-10-05, v386"

# ---------- (0) os nomes da pedra, na ordem do arquivo ----------
src = open(STONE, encoding="utf-8").read()
# fora dos comentarios de bloco /-! ... -/ e /-- ... -/ : removemos antes de procurar as declaracoes
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
decls = []
for m in re.finditer(r"(?m)^(noncomputable def|def|theorem|inductive|abbrev|structure|lemma)\s+([A-Za-z_][\w']*)", code):
    kind, name = m.group(1), m.group(2)
    decls.append((name, "checked" if kind in ("noncomputable def", "def", "inductive", "abbrev", "structure") else "proved"))
assert len(decls) == len({n for n, _ in decls}), "nome repetido na pedra"
assert all(n.isascii() for n, _ in decls), [n for n, _ in decls if not n.isascii()]
print("declaracoes da pedra:", len(decls))

# ---------- (1) a fiacao angular: existencia conferida por grep (os 17 nomes da tarefa) ----------
ANG = [
    ("TGLExt.the_angle_is_the_projection", "TGLExt/TheAngleIsTheProjection.lean"),
    ("TGLExt.the_observer_reads_the_angle", "TGLExt/TheObserverReadsTheAngle.lean"),
    ("TGLExt.observing_adds_nothing", "TGLExt/TheObserverReadsTheAngle.lean"),
    ("TGLExt.spectral_projections_split_the_identity", "TGLExt/TheAngleIsTheProjection.lean"),
    ("TGLExt.the_generator_is_the_difference_of_the_faces", "TGLExt/TheAngleIsTheProjection.lean"),
    ("TGLExt.J_and_K_anticommute", "TGLExt/TheTwoPairings.lean"),
    ("TGLExt.the_two_folds_commute", "TGLExt/TheTwoFolds.lean"),
    ("TGLExt.the_left_fold_closes", "TGLExt/TheTwoFolds.lean"),
    ("TGLExt.the_right_fold_closes", "TGLExt/TheTwoFolds.lean"),
    ("TGLExt.each_fold_is_a_complex_structure", "TGLExt/TheTwoFolds.lean"),
    ("TGLExt.the_selector_can_refuse", "TGLExt/TheSelectorCanRefuse.lean"),
    ("TGLExt.normSq_reflection", "TGLExt/SMatrix.lean"),
    ("TGLExt.the_name_above_every_name", "TGLExt/TheIdentityOfIdentity.lean"),
    ("TGLExt.terminality_forces_minimality", "TGLExt/TheTerminalRankOne.lean"),
    ("TGLExt.firstAtom_is_terminal", "TGLExt/TheTerminalRankOne.lean"),
    ("TGL.VerbInhabitant.verb_semigroup_fixes", "TGL/VerbInhabitant.lean"),
    ("TGLExt.the_tensor_squares_the_phase", "TGLExt/TheLightInterface.lean"),
]
existencia = {}
for q, f in ANG:
    short = q.split(".")[-1]
    ns = q[: -len(short) - 1]
    t = open(os.path.join(K, f), encoding="utf-8").read()
    m = re.search(r"(?m)^theorem\s+%s\b" % re.escape(short), t)
    nsm = re.search(r"(?m)^namespace\s+(\S+)", t)
    existencia[q] = {"arquivo": f, "theorem_na_linha": (t[: m.start()].count("\n") + 1) if m else None,
                     "namespace_do_arquivo": nsm.group(1) if nsm else None, "namespace_confere": bool(nsm and nsm.group(1) == ns)}
    assert m and existencia[q]["namespace_confere"], (q, existencia[q])
au = open(AUDIT, encoding="utf-8").read()
for q, _ in ANG:
    assert re.search(r"(?m)^#print axioms %s$" % re.escape(q), au) is None, "ja auditado: " + q
print("fiacao angular: %d nomes, todos existem e no namespace certo; nenhum ja auditado" % len(ANG))

# ---------- (2) TGLExt.lean: o import no fim ----------
root = open(ROOT, encoding="utf-8").read()
assert "import TGLExt.TheVerbSelectsTheAction" not in root, "o root ja importa a pedra"
assert root.rstrip("\n").endswith("import TGLExt.TheAxiomAndTheFalseWitness"), "o padrao do fim do root mudou"
root2 = root.rstrip("\n") + "\nimport TGLExt.TheVerbSelectsTheAction\n"

# ---------- (3) TGL/Audit.lean: o bloco v386 ----------
assert ANCHOR not in au, "o bloco v386 ja existe no Audit.lean"
assert au.rstrip("\n").endswith("#print axioms TGLExt.the_iald_selector_separates_the_sectors"), "o padrao do fim do Audit.lean mudou"
cab = (ANCHOR + ": O VERBO SELECIONA (o operador, 05/10/2026: «Verbo=seleção da ação»; «O verbo não descreve a ação; ele a escolhe. É um operador de "
       "projeção: 𝒱 = |a⟩⟨a|»; «o nome é \"posto\", é justamente \"o posto\", o local … onde a inscrição pode habitar com objeto distinto definido»; "
       "«são as duas faces do mesmo o objeto, porque o custo é jussivo à verdade»; «o tempo … precisa ser lido duas vezes»; «a luz … precede a gravidade, "
       "mas eles são indissociáveis»; «o resto vc consegue responder tudo agroa»): a pedra do Verbo (o Nome é o posto; select; a leitura é um peso; a "
       "ordem importa; a tríade com c = β_TGL [INPUT]; os postos por eixo; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade "
       "indissociáveis; %d nomes) e a FIAÇÃO dos termos compilados sem auditoria até a v385 (regime angular, as duas dobras, o seletor que recusa, "
       "|𝓡|² = sin²θ, o nome sobre todo nome, a terminalidade, o gesto 𝕍_t, o tensor; %d nomes; lista A3 do crítico, existência conferida por grep)"
       % (len(decls), len(ANG)))
bloco = "\n".join([cab] + ["#print axioms %s.%s" % (NS, n) for n, _ in decls] + ["#print axioms %s" % q for q, _ in ANG])
au2 = au.rstrip("\n") + "\n" + bloco + "\n"

# ---------- (4) os nomes e as bandeiras ----------
NOMES = {"TheVerbSelectsTheAction": ["%s.%s" % (NS, n) for n, _ in decls], "AngularWiring": [q for q, _ in ANG]}
VRB = ["ext_vrb_%s_kernel_%s" % (n, k) for n, k in decls]
ANGF = ["ext_ang_%s_kernel_proved" % q.split(".")[-1] for q, _ in ANG]
assert len(set(VRB + ANGF)) == len(VRB) + len(ANGF)
flags_py = (
    "# ====================== v386 (05/10/2026) -- O VERBO SELECIONA: as bandeiras da pedra (ext_vrb_) e da fiacao angular (ext_ang_) ======================\n"
    "# Geradas por fiar_escada_v386.py a partir dos nomes LIDOS da pedra e do bloco v386 do TGL/Audit.lean (sandbox). A bandeira e' o nome EXATO da\n"
    "# declaracao, posicao a posicao (def/inductive -> _kernel_checked; theorem -> _kernel_proved) -- o formato que gerar_candidato_v385.py e\n"
    "# extrair_axiomas_v385.py consomem. c = beta_TGL e' [INPUT]; beta nunca literal; o gate nao se move.\n"
    "_VRB_FLAGS_V386 = [\n" + "".join('    "%s",\n' % f for f in VRB) + "]\n"
    "_ANG_FLAGS_V386 = [\n" + "".join('    "%s",\n' % f for f in ANGF) + "]\n")

# ---------- (5) gravar: tempario -> conferir tamanho -> substituir ----------
def gravar(p, texto, minimo):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    assert os.path.getsize(tmp) >= minimo, (p, os.path.getsize(tmp), minimo)
    os.replace(tmp, p)

gravar(ROOT, root2, len(root.encode("utf-8")) + 10)
gravar(AUDIT, au2, len(au.encode("utf-8")) + 100)
gravar(os.path.join(HERE, "AUDIT_NOMES_v386.json"), json.dumps(NOMES, ensure_ascii=False, indent=1), 100)
gravar(os.path.join(HERE, "v386_flags.py"), flags_py, 100)
gravar(os.path.join(HERE, "FLAGS_v386.json"), json.dumps(
    {"vrb": [{"flag": f, "nome": "%s.%s" % (NS, n), "tipo": k} for f, (n, k) in zip(VRB, decls)],
     "ang": [{"flag": f, "nome": q, "arquivo": existencia[q]["arquivo"], "linha": existencia[q]["theorem_na_linha"]} for f, (q, _) in zip(ANGF, ANG)],
     "n_vrb": len(VRB), "n_ang": len(ANGF), "n_total": len(VRB) + len(ANGF)}, ensure_ascii=False, indent=1), 100)
print(json.dumps({"pedra_decls": len(decls), "vrb_checked": sum(1 for _, k in decls if k == "checked"), "vrb_proved": sum(1 for _, k in decls if k == "proved"),
                  "ang": len(ANGF), "total_novas": len(VRB) + len(ANGF), "root_linhas": root2.count("\n"), "audit_linhas": au2.count("\n")}, ensure_ascii=False))
