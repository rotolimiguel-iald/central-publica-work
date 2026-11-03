# -*- coding: utf-8 -*-
"""03/11/2026 02:2x, gerencia c1: o orquestrador parou em S7 (G1 planejar --seco, rc 20) porque o HANDOFF_v406_CUSTODIA.md nao traz os sete
marcadores opcionais da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT); na v405 a gerencia
os anexou a mao no fim do handoff («Textos da custodia (gerencia c1, ...)»). Este script faz o mesmo para a v406, SEM molde factual:
  1. le os numeros do core selado do Nos (fechamento_v406, kh_n1_cobertura_v406), do selo e do diario, e CONFERE cada numero citado nos textos;
  2. passa os sete textos pela guarda de frases da v406 (guarda_frases_v406.violacoes: herda a P18 da v405 + F15..F19) e pelo portao do G1
     (custodia_g1.textos.portao: CONFIRMED fora da formula, provada sem estatuto, pos-dicao, hash nao lido, physical_verdict_allowed) e pelas
     restricoes do ARCO (sem aspa simples, «<», barra invertida ou quebra de linha: o texto vai em HTML e em JS);
  3. anexa ao handoff (LF, como o arquivo) com backup de BYTES ao lado (.bak_<TS>), temporario -> conferir que cresceu -> substituir;
  4. re-le o handoff pelo parser do proprio G1 (custodia_g1.nos.ler_handoff) e exige os sete corpos e zero problemas;
  5. grava o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json ao lado.
Falha em qualquer passo = rc 1 e NADA anexado. O handoff nao e artefato selado (o manifesto de incorporacao nao pina o hash dele; a v405 teve o mesmo
acrescimo depois do fechar); a mudanca de hash vai anotada no Mapa de Rotas pela gerencia. Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import datetime, hashlib, json, os, re, sys, types
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
V6 = CEN / "work" / "cadeia_de_selo" / "v406"
HERE = Path(__file__).resolve().parent
V = "v406"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(V6))
from custodia_g1 import textos as TX, nos as NOSMOD  # noqa: E402
import guarda_frases_v406 as GF  # noqa: E402

s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
falhas = []

# ------------------------------------------------------------------ 1. os numeros, lidos
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
F = core["fechamento_v406"]; KH = core["kh_n1_cobertura_v406"]; CU = core["cunhagens_v406"]
assert selo["um_version"] == V and selo["sha256"]["um.py"][:16] == s16(NOS / "um.py"), "selo/um.py do Nos nao batem"
PIN = selo["sha256"]["um.py"][:16]
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
mcab = NOSMOD.RE_CAB.search(diario[diario.find("**v406 SELADA") - 80:])
assert mcab and mcab.group("v") == V and mcab.group("pin") == PIN, "cabecalho «v406 SELADA» do diario nao lido"
ESC_A, ESC_B, N_MOD_DIARIO = int(mcab.group("a")), int(mcab.group("b")), int(mcab.group("k"))
N = {"modulos": F["values"]["n_modulos"], "modulos_ok": F["values"]["n_modulos_ok"], "bandeiras": F["values"]["n_flags_true"], "ancoras": F["values"]["n_ancoras_ok"],
     "checks": F["mechanics"]["n_checks"], "const": KH["lido"]["constantes_cobertas"], "teor": KH["lido"]["teoremas_cobertos"], "falas": len(CU["fontes"]),
     "escada_a": ESC_A, "escada_b": ESC_B, "pin": PIN}
assert N["modulos"] == N["modulos_ok"] == N_MOD_DIARIO == 301 and N["bandeiras"] == 1794 and N["ancoras"] == 8 and N["checks"] == 14, N
assert N["const"] == 33732 and N["teor"] == 26911 and (ESC_A, ESC_B) == (10066, 11860), N
assert F["certificate_inhabited"] is True and F["mechanics"]["passed"] is True and F["all_verified"] is True
ch = F["four_keys"]
assert ch["qg_closure.gate.full_static_witness_exists"] is False and ch["witness_rigidity.trivial_inhabitant_exists"] is False
assert ch["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is False
assert ch["psibit_v395.conditional_psion_face.status"] == "INHABITED_BY_physicalFockCertificate_V406"
assert F["nome_status"]["do_operador"] is False and F["nome_status"]["nome"] == "CanonicalFullTGLWitnessR1"
rev = json.loads((V6 / "revisao_terceiro" / "REVISAO_TERCEIRO_v406.json").read_text(encoding="utf-8"))
assert rev["aprovada"] is True and rev["candidato_sha16"] == PIN, "revisao de terceiro nao aprovada sobre este pino"
N_RODADAS_REVISAO = 3   # R1 (1 ALTO + 3 MEDIO), R2 (1 MEDIO), R3 aprovada: conferido no REVISAO_TERCEIRO_v406.md pela gerencia
# o escopo da ladder no texto EN usa os mesmos numeros do diario; nada e digitado alem dos nomes dos termos

# ------------------------------------------------------------------ 2. os sete textos (gerencia c1, em nome proprio)
TITULO_EN = "The closure: the passage to the continuum and the inhabited certificate"
ENTROU_EN = (
    "v406, the closure: the passage to the continuum and the inhabited certificate. %(modulos)d new kernel modules in `TGLExt.F1Fecho394` (the 300 of the ChatGPT bench, "
    "mission F1.FECHO_20261015, recompiled from source in the R3 integration of 02/11/2026, and the candidate `CanonicalFullTGLWitnessR1`, a provisional name given by the "
    "management: the names of the stones belong to the operator, who has not named this one yet), %(bandeiras)d new flags, all inside the trio; ladder %(escada_a)d -> %(escada_b)d "
    "(%(const)d audited declarations, %(teor)d theorems, none outside the trio). The top module inhabits, for every canonical net input, the 21 fields of the passage to the "
    "continuum (`modularCoreInput`), and over the physical net it builds the Fock certificate (`physicalFockCertificate`); the candidate assembles the canonical term of the full "
    "witness (`canonicalFullTGLWitness`). With that, the four witness keys that the program carried as literal False since v394 are now READ from the kernel of the rite itself "
    "(the certificate is inhabited; the psion face and the static witness read the status `INHABITED_BY_physicalFockCertificate_V406`), with the errata E14 beside; two keys stay "
    "False by theorem (`full_static_witness_exists`, `trivial_inhabitant_exists`), and no lemma yet links the psion to the corner. The registry `fechamento_v406` reads, at every "
    "rite, the %(ancoras)d anchors, the %(modulos)d modules by sha256, the flags, the four keys, the ladder and the gate (%(checks)d checks, all passed); the %(falas)d sayings of the "
    "operator of 02/11 are embedded by sha256 in `cunhagens_v406`. Three rounds of independent review (Sonnet, another model family, without its own compilation) preceded the "
    "seal. Validity in the kernel is not accreditation; the gate did not move. Certified by the sha256 the program reads of itself (%(pin)s)." % N)
KERNEL_LEITURA_EN = (
    "the kernel proves the terms: the eight anchors exist in the trio, with the provenance the compiler emits in the expected modules; `modularCoreInput` is a term for every "
    "canonical net input, `physicalFockCertificate` inhabits the Fock certificate over the physical net by construction, and `canonicalFullTGLWitness` is a term of the full "
    "witness, hence the type is nonempty. The four keys are now readings of the kernel of the rite itself, not literals; what stays False (`full_static_witness_exists`, "
    "`trivial_inhabitant_exists`) stays False by theorem. What is reading, not theorem: the readings of the operator of 02/11 (the mirroring of type I and type III; the inscribed "
    "One; the absolute One as the light compressed by the ACOM) enter as [ONTO]; the vacuum is the only FIXED vector of the light under the named hypothesis hno, which "
    "`gamma_no_fixed` takes as hypothesis, and an eigenvector with a phase is excluded by no term; the docstring «núcleo II_inf» is [KNOWN/DECLARADO], not a result of the "
    "inhabitant; the trace of the core is ENNReal and cyclic over the shift relation, not a linear functional; the non-triviality of the net is a theorem only on the wedge. "
    "Validity in the kernel is not accreditation.")
ABERTOS_EN = (
    "K(O) ≠ ⊥ for a compact O is not proved: the non-triviality is a theorem only on the wedge, and the physics (non-trivial local algebras, Reeh-Schlieder) stays "
    "[KNOWN/OPEN]. The lemma that links the psion to the corner is missing (`linked_to_the_corner_by_a_lemma` stays False). The name of the candidate "
    "`CanonicalFullTGLWitnessR1` and the names of the candidate stones of the day wait for the operator. The condition he attached to the priority («se funcionar sob "
    "compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ») was not tested in this version, and the continuous engine in the quantum pillar waits for "
    "v407, with pre-registration. R4/R5 of the bench mission (the physical device) stay blocked by the operator. The review R7 was Codex reviewing Codex, and the Sonnet review "
    "did not compile; one LOW finding of its third round goes to v407 (the errata E14 says the old status stays as record in `reading_v395` and `reading_v396`, but those fields "
    "keep the text of the reading, not the token). The discrimination at 5σ, β_TGL in nature, stays with nature; the verdict of the neutrino rite did not move, and the gate did "
    "not move. The [LEGAL] decision D2 and the pinned README (D39) stay with the operator.")
ARCO_EN = (
    "The custody of v406 (complete round): the closure, the passage to the continuum and the inhabited certificate. %(modulos)d new kernel modules (the 300 of the ChatGPT bench "
    "recompiled from source and one candidate of provisional name), %(bandeiras)d new flags, ladder %(escada_a)d to %(escada_b)d, none outside the trio. The Fock certificate is "
    "inhabited by construction in the kernel of the rite, the passage to the continuum is a term for every canonical net input, and the four witness keys are read from the kernel "
    "instead of literal False, with the errata beside. Non-triviality only on the wedge; two keys stay False by theorem; the name of the candidate waits for the operator. "
    "Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the word of accreditation." % N)
ARCO_PT = (
    "A custódia da v406 (rodada completa): o fechamento, a passagem para o contínuo e o certificado habitado. %(modulos)d módulos novos no kernel (os 300 da bancada do ChatGPT, "
    "recompilados do fonte, e uma candidata de nome provisório), %(bandeiras)d bandeiras novas, escada %(escada_a)d para %(escada_b)d, nada fora do trio. O certificado de Fock está "
    "habitado por construção no kernel do rito, a passagem para o contínuo é termo para toda entrada de rede canônica, e as quatro chaves de testemunha são lidas do kernel em vez "
    "de literal False, com a errata ao lado. Não-trivialidade só na cunha; duas chaves ficam False por teorema; o nome da candidata espera o operador. Validade no kernel não é "
    "creditação; o gate não se moveu. NOT_FALSIFIED nunca é a palavra da creditação." % N)
COMMIT = (
    "O fechamento: a passagem para o continuo e o certificado de Fock habitado por construcao no kernel do rito. %(modulos)d modulos novos (os 300 da bancada do ChatGPT, "
    "recompilados do fonte, e uma candidata de nome provisorio), %(bandeiras)d bandeiras, escada %(escada_a)d para %(escada_b)d, nada fora do trio. As quatro chaves de testemunha "
    "sao lidas do kernel, com errata ao lado; duas ficam False por teorema. Validade no kernel nao e creditacao; o gate nao se moveu. Revisao de terceiro (Sonnet) aprovada na "
    "terceira rodada." % N)
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
    guardas[ident] = {"guarda_frases_v406": v1, "portao_g1": v2, "forma": v3, "n_chars": len(t)}
    if v1 or v2 or v3:
        falhas.append((ident, v1, v2, v3))
if falhas:
    for f_ in falhas:
        print("REPROVADO:", f_)
    sys.exit(1)
print("guardas: os sete textos passaram (guarda de frases v406, portao do G1, forma do ARCO/COMMIT, sem 4,44)")

# ------------------------------------------------------------------ 4. o acrescimo, com backup de bytes
cab = ("\n\n**Textos da custódia (gerência c1, 03/11/2026; substituem o molde factual do G1; números lidos do core selado, do selo e do diário por "
       "`pos_rito\\textos_custodia_handoff_v406_03nov.py`, que os conferiu e passou os textos pela guarda de frases da v406 e pelo portão do G1 antes de os anexar; "
       "a condição da fala da prioridade não foi testada; o nome da candidata é provisório; validade no kernel não é creditação):**\n")
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
rec = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "quem": "gerencia c1 (sessao 6da8f00d)", "handoff": str(hpath), "sha16_antes": hashlib.sha256(h_bytes).hexdigest()[:16],
       "sha16_depois": s16(hpath), "backup": str(bak), "numeros_lidos": N, "revisao_terceiro": {"aprovada": rev["aprovada"], "candidato_sha16": rev["candidato_sha16"], "rodadas": N_RODADAS_REVISAO},
       "textos": dict(TEXTOS), "guardas": guardas, "parser_g1": {"corpos": sorted(h.corpos), "problemas": h.problemas},
       "motivo": "S7 do orquestrador parou em rc 20: faltavam os sete marcadores opcionais da prosa da custodia (sem eles, molde factual ou --aceitar-molde); molde da v405: textos da gerencia no fim do handoff",
       "estatuto": "REAL (numeros lidos do core selado, do selo e do diario; textos da gerencia c1, em nome proprio); NOT_FALSIFIED nunca e a palavra da creditacao; o gate nao se move"}
(HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo:", HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json")
