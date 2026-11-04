# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026, claude-prep-v407 / ajudante B1a] sobre a subida mecanica da v406 FINAL: os sete textos e os numeros sao os da v407 (O PSION, O CANTO E O PAR); a infraestrutura (guardas, acrescimo com backup de bytes, re-leitura pelo parser do G1, recibo) e' a da v406. Nao rodou; a gerencia revisa antes (nao e' versao selada).
"""03/11/2026, gerencia c1: o orquestrador pode parar em S7 (G1 planejar --seco, rc 20) porque o HANDOFF_v407_CUSTODIA.md nao traz os sete
marcadores opcionais da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT); na v406 a gerencia
os anexou a mao no fim do handoff («Textos da custodia (gerencia c1, ...)»). Este script faz o mesmo para a v407, SEM molde factual:
  1. le os numeros do core selado do Nos (psion_canto_v407, kh_n1_cobertura_v407, cunhagens_v407; fechamento_v406 herdado), do selo e do diario, e CONFERE cada numero citado nos textos contra ESPERADOS_v407.json e delta_v407;
  2. passa os sete textos pela guarda de frases da v407 (guarda_frases_v407.violacoes: herda a P18 e as regras da v406 e acrescenta as do par na face de Fock, de Omega = Phi+ e da ponte Bell-TT) e pelo portao do G1
     (custodia_g1.textos.portao: a palavra recusada fora da formula da regua, a palavra da prova sem estatuto, o demerito da retrodicao, hash nao lido, physical_verdict_allowed) e pelas
     restricoes do ARCO (sem aspa simples, «<», barra invertida ou quebra de linha: o texto vai em HTML e em JS);
  3. anexa ao handoff (LF, como o arquivo) com backup de BYTES ao lado (.bak_<TS>), temporario -> conferir que cresceu -> substituir;
  4. re-le o handoff pelo parser do proprio G1 (custodia_g1.nos.ler_handoff) e exige os sete corpos e zero problemas;
  5. grava o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v407.json ao lado.
Falha em qualquer passo = rc 1 e NADA anexado. O handoff nao e artefato selado (o manifesto de incorporacao nao pina o hash dele; a v406 teve o mesmo
acrescimo depois do fechar); a mudanca de hash vai anotada no Mapa de Rotas pela gerencia. A revisao de terceiro (Sonnet, D47) e' lida de revisao_terceiro\\REVISAO_TERCEIRO_v407.json
SE existir: existindo e aprovada sobre este pino, os textos o dizem; existindo e nao aprovada, PARA; ausente, os textos dizem que ela e' ato distinto e nao a afirmam.
Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import datetime, hashlib, json, os, re, sys, types
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
PKG = CEN / "work" / "cadeia_de_selo" / "v407"
HERE = Path(__file__).resolve().parent
V = "v407"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(PKG))
from custodia_g1 import textos as TX, nos as NOSMOD  # noqa: E402
import guarda_frases_v407 as GF  # noqa: E402
import delta_v407 as DL  # noqa: E402

s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
falhas = []

# ------------------------------------------------------------------ 1. os numeros, lidos
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
ESP = json.loads((PKG / "ESPERADOS_v407.json").read_text(encoding="utf-8"))
F = core[DL.FECHO_REGISTRO]; KH = core[DL.KH_REGISTRO]; CU = core[DL.CUNHAGENS_REGISTRO]; FH = core["fechamento_v406"]
assert selo["um_version"] == V and selo["sha256"]["um.py"][:16] == s16(NOS / "um.py"), "selo/um.py do Nos nao batem"
PIN = selo["sha256"]["um.py"][:16]
assert PIN == ESP["candidato_sha16"], "o pino do selo != o candidato de ESPERADOS"
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
mcab = NOSMOD.RE_CAB.search(diario[diario.find("**v407 SELADA") - 80:])
assert mcab and mcab.group("v") == V and mcab.group("pin") == PIN, "cabecalho «v407 SELADA» do diario nao lido"
ESC_A, ESC_B, N_MOD_DIARIO = int(mcab.group("a")), int(mcab.group("b")), int(mcab.group("k"))
N = {"modulos": F["values"]["n_modulos"], "modulos_ok": F["values"]["n_modulos_ok"], "bandeiras": F["values"]["n_flags_true"], "ancoras": F["values"]["n_ancoras_ok"],
     "checks": F["mechanics"]["n_checks"], "const": KH["lido"]["constantes_cobertas"], "teor": KH["lido"]["teoremas_cobertos"], "falas": len(CU["verbatim"]),
     "escada_a": ESC_A, "escada_b": ESC_B, "pin": PIN}
assert N["modulos"] == N["modulos_ok"] == N_MOD_DIARIO == DL.N_BUNDLE == ESP["kernel"]["modulos_novos"], N
assert N["bandeiras"] == ESP["n_bandeiras_novas"] and N["ancoras"] == len(DL.ANCORAS) and N["checks"] == DL.N_CHECKS_FECHO, N
assert N["const"] == ESP["cobertura_kh_n1"]["decl"] and N["teor"] == ESP["cobertura_kh_n1"]["thm"] and [ESC_A, ESC_B] == ESP["escada_v406_e_v407"], N
assert N["falas"] == len(DL.VERBATIM_ORIGEM_V407) == len(ESP["cunhagens"]), N
assert F["all_verified"] is True and F["mechanics"]["passed"] is True and F["link_read_from_the_kernel"] is True and F["does_not_gate_core"] is True and FH["all_verified"] is True
ch = F["keys"]
assert ch == ESP["chaves_v407_esperadas"], "as chaves do registro != ESPERADOS"
assert ch["qg_closure.gate.full_static_witness_exists"] is False and ch["witness_rigidity.trivial_inhabitant_exists"] is False
assert ch["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and ch["kernel_reads_the_link"] is True
assert F["teste_d"]["so_citado"] is True and F["teste_d"]["resultado_no_um_py"] is None
assert (F["fica_aberto"]["par_na_face_de_fock"], F["fica_aberto"]["ponte_bell_tt"]) == (DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, DL.FICA_ABERTO_PONTE_BELL_TT)
revp = PKG / "revisao_terceiro" / "REVISAO_TERCEIRO_v407.json"
REV = None
if revp.exists():
    REV = json.loads(revp.read_text(encoding="utf-8"))
    assert REV.get("aprovada") is True and REV.get("candidato_sha16") == PIN, "revisao de terceiro existe mas nao esta aprovada sobre este pino: PARO"
# o escopo da ladder no texto EN usa os mesmos numeros do diario; nada e digitado alem dos nomes dos termos
REV_EN = " The independent review of the package by the Sonnet (another model family, without its own compilation) approved it before the seal." if REV else " The independent review of the package (Sonnet, D47) is a distinct act and is not claimed here."
REV_PT = " A revisão independente do pacote pelo Sonnet (outra família de modelo, sem compilação própria) o aprovou antes do selo." if REV else " A revisão independente do pacote (Sonnet, D47) é ato distinto e não é afirmada aqui."
REV_COMMIT = " Revisao de terceiro (Sonnet) aprovada." if REV else " A revisao de terceiro (Sonnet, D47) e ato distinto."

# ------------------------------------------------------------------ 2. os sete textos (gerencia c1, em nome proprio)
TITULO_EN = "The psion, the corner and the pair"
ENTROU_EN = (((
    "v407, the psion, the corner and the pair. %(modulos)d new kernel modules in `TGLExt` (`PsionCanto`, `Par` and the seven stones of 02/11, every name given or ratified by the "
    "operator on 03/11), %(bandeiras)d new flags, all inside the trio; ladder %(escada_a)d -> %(escada_b)d (%(const)d audited declarations, %(teor)d theorems, none outside the trio). "
    "`PsionCanto` proves, for every Fock certificate and without hypothesis on the inhabitant `physicalFockCertificate` of v406, that the Jones reading of the flow of the light, "
    "compressed into the corner of the psion, returns the corner; the lemma of the two faces (`the_psion_is_the_corner_on_both_faces`) says that on both faces the psion is the unit "
    "vector whose corner is the projector onto it, the corner scalarises and weighs one. With that, the key `testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma`, a "
    "literal False from v396 to v406, is now READ from the kernel of the rite itself, with the errata E18 beside; the link is one of structure, not of vectors (the Fock vacuum and "
    "the Bell vector are not identified). `Par` composes only terms the kernel already had: the pair is bound (CCI = 1/2), never cancels, is read by the doubled phase of helicity two "
    "with return at theta = pi, and its corner is the 4x4 projector. The registry `psion_canto_v407` reads, at every rite, the %(ancoras)d anchors, the %(modulos)d modules by sha256, "
    "the flags, the key, the ladder and the gate (%(checks)d checks, all passed); the %(falas)d sayings of the operator of 03/11 are embedded by sha256 in `cunhagens_v407`.") % N) + REV_EN +
    (" Validity in the kernel is not accreditation; the gate did not move. Certified by the sha256 the program reads of itself (%(pin)s)." % N))
KERNEL_LEITURA_EN = (
    "the kernel proves the terms: the %(ancoras)d anchors exist in the trio, with the provenance the compiler emits in the expected modules; `the_psion_is_the_corner_on_both_faces` is a "
    "term, so the key that said no lemma links the psion to the corner is now a reading of the kernel and not a literal; `o_par_de_psions_e_o_graviton` joins four facts about terms that "
    "already existed (the pair is bound, never cancels, is read by phase and return, and its corner is the 4x4 projector). What is reading, not theorem: the readings of the operator "
    "of 03/11 (the graviton as the bound state of two psions that never cancel and are read by the graviton, in phase and return of phase; the corner as the 4x4 projector; the "
    "holographic bath) enter as [ONTO]; the pair on the Fock face (two psions over the vacuum) stays [OPEN] because the Fock certificate has no creation operators as terms; the "
    "bridge between the Bell space and the TT sector of spin two is not a term; the docstring «núcleo II_inf» is [KNOWN/DECLARADO], not a result of the inhabitant; the trace of the "
    "core is ENNReal and cyclic, not a linear functional; the non-triviality of the net is a theorem only on the wedge (K(O) ≠ ⊥ only there). Validity in the kernel is not accreditation." % N)
ABERTOS_EN = (
    "The pair of psions on the Fock face stays open: the Fock certificate has no creation operators as terms. The bridge between the Bell space and the TT sector of spin two is not "
    "a term (the stone `Par` places the faces side by side, it does not identify them). K(O) ≠ ⊥ for a compact O is not proved: the non-triviality is a theorem "
    "only on the wedge, and the physics (non-trivial local algebras, Reeh-Schlieder) stays [KNOWN/OPEN]. The test (d) of branch B of the ringdown enters only by citation of its "
    "pre-registration V1.1; by the option (c) of the operator it enters the program only if it has power, and no result is in this version. The continuous engine in the quantum "
    "pillar stays out: the operator wants observable content and has not yet said which. Four of the seven stones of 02/11 (`AChaveDaGuarda`, `OGuarda`, `LeituraPreservada`, `OIgual`) "
    "had no third-party review before this version; the Sonnet reviewed three. One phrase of `OUmInscrito` was flagged to the management and not changed." + REV_EN +
    " The discrimination at 5σ, β_TGL in nature, stays with nature; the verdict of the neutrino rite did not move, and the gate did not move. The [LEGAL] decision D2 and the pinned "
    "README (D39) stay outside the program.")
ARCO_EN = (
    "The custody of v407 (complete round): the psion, the corner and the pair. %(modulos)d new kernel modules (PsionCanto, Par and seven stones of 02/11 with names given or ratified "
    "by the operator), %(bandeiras)d new flags, ladder %(escada_a)d to %(escada_b)d, none outside the trio. The lemma that links the two faces of the psion is in the kernel of the rite "
    "and the key that said it was missing is read from the kernel instead of a literal False, with the errata beside; the link is one of structure, not of vectors. The bound pair never "
    "cancels and its corner is the 4x4 projector; the pair on the Fock face stays open. Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the "
    "word of accreditation." % N)
ARCO_PT = (
    "A custódia da v407 (rodada completa): o psíon, o canto e o par. %(modulos)d módulos novos no kernel (PsionCanto, Par e sete pedras de 02/11, com nomes dados ou ratificados "
    "pelo operador), %(bandeiras)d bandeiras novas, escada %(escada_a)d para %(escada_b)d, nada fora do trio. O lema que liga as duas faces do psíon está no kernel do rito e a chave "
    "que o dava por ausente é lida do kernel em vez de literal False, com a errata ao lado; o elo é de estrutura, não de vetores. O par ligado nunca se cancela e o canto dele é o "
    "projetor 4x4; o par na face de Fock segue em aberto. Validade no kernel não é creditação; o gate não se moveu. NOT_FALSIFIED nunca é a palavra da creditação." % N)
COMMIT = (
    "O psion, o canto e o par: o lema que liga as duas faces do psion entra no kernel e a chave que o dava por ausente e lida do kernel do rito. %(modulos)d modulos novos (PsionCanto, "
    "Par e sete pedras de 02/11 de nome ratificado), %(bandeiras)d bandeiras, escada %(escada_a)d para %(escada_b)d, nada fora do trio. O elo e de estrutura, nao de vetores; o par na "
    "face de Fock segue em aberto. Validade no kernel nao e creditacao; o gate nao se moveu." % N + REV_COMMIT)
TEXTOS = [("TITULO_EN", TITULO_EN), ("ENTROU_EN", ENTROU_EN), ("KERNEL_LEITURA_EN", KERNEL_LEITURA_EN), ("ABERTOS_EN", ABERTOS_EN), ("ARCO_EN", ARCO_EN), ("ARCO_PT", ARCO_PT), ("COMMIT", COMMIT)]

# ------------------------------------------------------------------ 3. as guardas
hpath = NOS / ("HANDOFF_%s_CUSTODIA.md" % V)
h_bytes = hpath.read_bytes(); h_txt = h_bytes.decode("utf-8")
assert b"\r\n" not in h_bytes, "o handoff e CRLF: ajustar o acrescimo"
for ident, _ in TEXTOS:
    assert ("INICIO_%s_%s" % (ident, V)) not in h_txt, "marcador %s ja existe no handoff" % ident
conhecidos = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", h_txt)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", h_txt)) | {PIN}
guardas = {}
for ident, t in TEXTOS:
    v1 = [list(x) for x in GF.violacoes(t)]
    v2 = TX.portao(t, conhecidos, rotulo=ident)
    v3 = []
    if ident in ("ARCO_EN", "ARCO_PT") and ("'" in t or "<" in t or "\\" in t or "\n" in t):
        v3.append("%s: aspa simples, «<», barra invertida ou quebra de linha" % ident)
    if ident == "COMMIT" and any(ord(ch_) > 127 for ch_ in t):
        v3.append("COMMIT: caractere fora do ASCII")
    if re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):
        v3.append("%s: traz o 4,44 (a regra do 4,44: nunca sozinho; estes textos nao o trazem)" % ident)
    guardas[ident] = {"guarda_frases_v407": v1, "portao_g1": v2, "forma": v3, "n_chars": len(t)}
    if v1 or v2 or v3:
        falhas.append((ident, v1, v2, v3))
if falhas:
    for f_ in falhas:
        print("REPROVADO:", f_)
    sys.exit(1)
print("guardas: os sete textos passaram (guarda de frases v407, portao do G1, forma do ARCO/COMMIT, sem 4,44)")

# ------------------------------------------------------------------ 4. o acrescimo, com backup de bytes
cab = ("\n\n**Textos da custódia (gerência c1, 03/11/2026; substituem o molde factual do G1; números lidos do core selado, do selo e do diário por "
       "`pos_rito\\textos_custodia_handoff_v407_03nov.py`, que os conferiu contra ESPERADOS e passou os textos pela guarda de frases da v407 e pelo portão do G1 antes de os anexar; "
       "o par de psíons na face de Fock segue em aberto; o teste (d) só por citação do pré-registro; validade no kernel não é creditação):**\n")
blocos = "".join("\n<!-- INICIO_%s_%s -->\n%s\n<!-- FIM_%s_%s -->\n" % (i, V, t, i, V) for i, t in TEXTOS)
novo = h_bytes.rstrip(b"\n") + (cab + blocos).encode("utf-8")
assert len(novo) > len(h_bytes) + 3000 and novo.startswith(h_bytes.rstrip(b"\n")), "o acrescimo nao cresceu como esperado"
bak = hpath.with_name(hpath.name + ".bak_" + TS); open(bak, "xb").write(h_bytes)
assert bak.read_bytes() == h_bytes, "backup de bytes diferente do original"
tmp = hpath.with_name(hpath.name + ".tmp_" + TS); open(tmp, "xb").write(novo); assert tmp.stat().st_size == len(novo)
os.replace(tmp, hpath)
assert hpath.stat().st_size == len(novo) > len(h_bytes), "o handoff nao cresceu depois da substituicao"
print("handoff: %d -> %d bytes; sha16 %s -> %s; backup %s" % (len(h_bytes), len(novo), hashlib.sha256(h_bytes).hexdigest()[:16], s16(hpath), bak.name))

# ------------------------------------------------------------------ 5. re-leitura pelo parser do G1
c = types.SimpleNamespace(NOS=NOS, CEN=CEN)
h = NOSMOD.ler_handoff(c, V)
faltam = [i for i, _ in TEXTOS if ("%s_%s" % (i, V)) not in h.corpos]
assert h is not None and not faltam and not h.problemas, (faltam, h.problemas)
for i, t in TEXTOS:
    assert h.corpos["%s_%s" % (i, V)].strip("\n") == t, "corpo lido difere do escrito: " + i
assert h.o_que_e and h.o_que_e.pin16 == PIN and h.o_que_e.versao == V, "o «O que é» do handoff deixou de ser lido"
print("parser do G1: 7/7 corpos lidos, 0 problemas; marcadores:", sorted(h.marcadores))
rec = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "quem": "gerencia c1", "handoff": str(hpath), "sha16_antes": hashlib.sha256(h_bytes).hexdigest()[:16],
       "sha16_depois": s16(hpath), "backup": str(bak), "numeros_lidos": N, "revisao_terceiro": ({"aprovada": REV["aprovada"], "candidato_sha16": REV["candidato_sha16"]} if REV else "ausente: os textos dizem que e' ato distinto e nao a afirmam"),
       "textos": dict(TEXTOS), "guardas": guardas, "parser_g1": {"corpos": sorted(h.corpos), "problemas": h.problemas},
       "motivo": "S7 do orquestrador pode parar em rc 20: faltam os sete marcadores opcionais da prosa da custodia (sem eles, molde factual ou --aceitar-molde); molde da v406: textos da gerencia no fim do handoff",
       "estatuto": "REAL (numeros lidos do core selado, do selo e do diario e conferidos contra ESPERADOS; textos da gerencia c1, em nome proprio); NOT_FALSIFIED nunca e a palavra da creditacao; o gate nao se move"}
(HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v407.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo:", HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v407.json")
