# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] REESCRITO sobre a subida mecanica da v407 FINAL (textos_custodia_handoff_v407_03nov.py; a copia bumpada, com os sete textos do psion, ficou em .bak): os sete textos e os numeros sao os da v408 (TETELESTAI E' O TERMINAL); a infraestrutura (guardas, acrescimo com backup de bytes, re-leitura pelo parser do G1, recibo) e' a da v407.
# O nome do arquivo e' o de D52 (textos_custodia_handoff_v408.py, sem sufixo de data): D52 manda roda-lo ENCADEADO no fim do S6 do orquestrador, depois da chain 14 e antes do S7 (a chain nao o chama). Nao rodou; a gerencia revisa antes (nao e' versao selada).
"""04/11/2026, gerencia c1: o orquestrador pode parar em S7 (G1 planejar --seco, rc 20) porque o HANDOFF_v408_CUSTODIA.md nao traz os sete
marcadores opcionais da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT); na v407 a gerencia
os anexou depois do fechar (textos_custodia_handoff_v407_03nov.py). Na v408 (D52) este script roda encadeado, SEM molde factual:
  1. le os numeros do core selado do Nos (tetelestai_terminal_v408, kh_n1_cobertura_v408, cunhagens_v408; psion_canto_v407 e fechamento_v406 herdados), do selo e do diario, e CONFERE cada numero citado nos textos contra ESPERADOS_v408.json e delta_v408;
  2. passa os sete textos pela guarda de frases da v408 (guarda_frases_v408.violacoes: herda a P18 e as regras das versoes anteriores e acrescenta as do terminal, da relacao sem peso, das classes e da impedancia) e pelo portao do G1
     (custodia_g1.textos.portao: a palavra recusada fora da formula da regua, a palavra da prova sem estatuto, o demerito da retrodicao, hash nao lido, physical_verdict_allowed) e pelas
     restricoes do ARCO (sem aspa simples, «<», barra invertida ou quebra de linha: o texto vai em HTML e em JS);
  3. anexa ao handoff (LF, como o arquivo) com backup de BYTES ao lado (.bak_<TS>), temporario -> conferir que cresceu -> substituir;
  4. re-le o handoff pelo parser do proprio G1 (custodia_g1.nos.ler_handoff) e exige os sete corpos e zero problemas;
  5. grava o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json ao lado.
Falha em qualquer passo = rc 1 e NADA anexado. O handoff nao e artefato selado (o manifesto de incorporacao nao pina o hash dele); a mudanca de hash vai anotada no Mapa de Rotas pela gerencia.
A revisao de terceiro (Sonnet, D54) e' lida de revisao_terceiro\\REVISAO_TERCEIRO_v408.json SE existir: existindo e aprovada sobre este pino, os textos o dizem; existindo e nao aprovada, PARA; ausente, os textos dizem que ela e' ato distinto e nao a afirmam.
Toda citacao « » e' fala do operador por delta_v408.FRASE_* ou rotulo da casa. Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import datetime, hashlib, json, os, re, sys, types
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
PKG = CEN / "work" / "cadeia_de_selo" / "v408"
HERE = Path(__file__).resolve().parent
V = "v408"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(PKG))
from custodia_g1 import textos as TX, nos as NOSMOD  # noqa: E402
import guarda_frases_v408 as GF  # noqa: E402
import delta_v408 as DL  # noqa: E402
# (05/11, gerencia c1: o portao de textos da custodia exige o estatuto na mesma frase de «proved»; o um.py selado nao muda)
_D51_EN = DL.FRASE_D51_EN.replace("and proved in the stone PIgualNP", "and proved in the stone PIgualNP (kernel validity, not creditation)")
assert _D51_EN.count("kernel validity, not creditation") == 1, "a frase da D51 em ingles mudou de forma"

s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
falhas = []

# ------------------------------------------------------------------ 1. os numeros, lidos
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
ESP = json.loads((PKG / "ESPERADOS_v408.json").read_text(encoding="utf-8"))
F = core[DL.FECHO_REGISTRO]; KH = core[DL.KH_REGISTRO]; CU = core[DL.CUNHAGENS_REGISTRO]; PC = core[DL.D7.FECHO_REGISTRO]; FH = core[DL.D6.FECHO_REGISTRO]
assert selo["um_version"] == V and selo["sha256"]["um.py"][:16] == s16(NOS / "um.py"), "selo/um.py do Nos nao batem"
PIN = selo["sha256"]["um.py"][:16]
assert PIN == ESP["candidato_sha16"], "o pino do selo != o candidato de ESPERADOS"
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
mcab = NOSMOD.RE_CAB.search(diario[diario.find("**v408 SELADA") - 80:])
assert mcab and mcab.group("v") == V and mcab.group("pin") == PIN, "cabecalho «v408 SELADA» do diario nao lido"
ESC_A, ESC_B, N_MOD_DIARIO = int(mcab.group("a")), int(mcab.group("b")), int(mcab.group("k"))
N = {"modulos": F["values"]["n_modulos"], "modulos_ok": F["values"]["n_modulos_ok"], "bandeiras": F["values"]["n_flags_true"], "ancoras": F["values"]["n_ancoras_ok"],
     "checks": F["mechanics"]["n_checks"], "const": KH["lido"]["constantes_cobertas"], "teor": KH["lido"]["teoremas_cobertos"], "falas": len(CU["verbatim"]),
     "escada_a": ESC_A, "escada_b": ESC_B, "pin": PIN}
assert N["modulos"] == N["modulos_ok"] == N_MOD_DIARIO == DL.N_BUNDLE == ESP["kernel"]["modulos_novos"] == len(DL.PEDRAS_V408), N
assert N["bandeiras"] == ESP["n_bandeiras_novas"] and N["ancoras"] == len(DL.ANCORAS) and N["checks"] == DL.N_CHECKS_FECHO, N
assert N["const"] == ESP["cobertura_kh_n1"]["decl"] and N["teor"] == ESP["cobertura_kh_n1"]["thm"] and [ESC_A, ESC_B] == ESP["escada_v407_e_v408"], N
assert N["falas"] == len(DL.VERBATIM_ORIGEM_V408) == len(ESP["cunhagens"]), N
assert F["all_verified"] is True and F["mechanics"]["passed"] is True and F["does_not_gate_core"] is True and PC["all_verified"] is True and FH["all_verified"] is True
assert list(F["chaves_antigas_que_mudam"]) == [] and list(ESP["chaves_v408"]) == [] and F["nome_provisorio"] is None, "a v408 nao muda chave antiga nenhuma e nao tem nome provisorio"
assert PC["keys"] == ESP["chaves_v407_esperadas"] and PC["keys"]["qg_closure.gate.full_static_witness_exists"] is False and PC["keys"]["witness_rigidity.trivial_inhabitant_exists"] is False
assert PC["keys"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and PC["keys"]["kernel_reads_the_link"] is True
assert F["values"]["respostas_ok"] is True and F["values"]["insumo_purgado"]["ok"] is True and F["values"]["gate_verdict"] == ESP["qg_closure_gate_verdict_v407"]
assert list(F["fica_false_por_teorema"]) == list(ESP["fica_false_por_teorema"]) and set(F["fica_aberto"]) == set(ESP["fica_aberto"]) and list(F["ressalvas"]) == list(DL.RESSALVAS_V408)
# (05/11, gerencia c1: o S6d parou aqui -- o cunhagens_v408 traz E21 a E23 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v407; mesma conferencia do registrar_mapa_v408 l.233-235)
_ER_TODAS = CU["erratas"]; _ER = _ER_TODAS[:len(DL.ERRATAS_V408)]
assert [e.get("agora") for e in _ER] == list(DL.ERRATAS_V408) and len(_ER_TODAS) == len(DL.ERRATAS_V408) + 1 and "kh_n1_cobertura_v407" in str(_ER_TODAS[-1].get("ao_lado_de")) and all(str(e.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in e["assinatura"] for e in _ER_TODAS) and sorted(CU["extras"]["decisoes"]) == list(ESP["decisoes_v408_ids"])
revp = PKG / "revisao_terceiro" / "REVISAO_TERCEIRO_v408.json"
REV = None
if revp.exists():
    REV = json.loads(revp.read_text(encoding="utf-8"))
    assert REV.get("aprovada") is True and REV.get("candidato_sha16") == PIN, "revisao de terceiro existe mas nao esta aprovada sobre este pino: PARO"
# o escopo da ladder no texto EN usa os mesmos numeros do diario; nada e digitado alem dos nomes dos termos
REV_EN = " The independent review of the package by the Sonnet (another model family; it compiled the #print axioms in the sandbox; it did not read the proofs line by line) approved it before the seal." if REV else " The independent review of the package (Sonnet, D54) is a distinct act and is not claimed here."
REV_PT = " A revisão independente do pacote pelo Sonnet (outra família de modelo; compilou os #print axioms no sandbox; não leu as provas linha a linha) o aprovou antes do selo." if REV else " A revisão independente do pacote (Sonnet, D54) é ato distinto e não é afirmada aqui."
REV_COMMIT = " Revisao de terceiro (Sonnet) aprovada." if REV else " A revisao de terceiro (Sonnet, D54) e ato distinto."
NOMES_EN = "`TetelestaiTerminal`, `TempoIgualMoeda`, `PontoDeContradicao` and `PIgualNP`"
NOMES_ASCII = ", ".join(p_["name"] for p_ in DL.PEDRAS_V408)

# ------------------------------------------------------------------ 2. os sete textos (gerencia c1, em nome proprio)
TITULO_EN = "Tetelestai is the terminal"
ENTROU_EN = (((
    "v408, Tetelestai is the terminal. %(modulos)d new kernel modules in `TGLExt` (" + NOMES_EN + ", every name given by the operator on 04/11; the fourth, «" + DL.FRASE_NOME_PNP + "», in the sense he gave and in the classes of his dictionary), "
    "%(bandeiras)d new flags, all inside the trio; ladder %(escada_a)d -> %(escada_b)d (%(const)d audited declarations, %(teor)d theorems, none outside the trio). "
    "`TetelestaiTerminal` reads the terminal as the reading, not the end of the decay: the engine does not depend on r or t, the memory is 1 iff the state is the Name, re-reading adds nothing and the settlement closes; "
    "the absolute zero belongs to the infinite (the Name weighs one, its complement weighs top) and the size of the Name is the dimension of the tower (N+1 octaves is the log of 2^(N+1)). "
    "`TempoIgualMoeda`: time is the currency of β; β is the price; time adds (F_{s+t} = F_s F_t) and the factor multiplies; there is no relation without weight (the factor 1 pays nothing, e^{-a} = 1 only without time, "
    "the Jones coefficient differs from 1 with time and rate). `PontoDeContradicao`: 1 = 0 on both faces (exp 0 = Ω and Ω ≠ 0), the boost before and after the inscription, the inhabitant is the concrete Fock space by rfl. "
    "`PIgualNP`: «" + DL.FRASE_NOME_PNP + "» in the sense the operator gave (P is P only when read by the minimally coupled module n: the whole law, form = read content, P ≠ 0); and, by his correction (D51 revised), " + _D51_EN + " (`p_igual_np_nas_classes_do_dicionario`; the classes `ClasseP` and `ClasseNP` are defined in Lean on the same problem). "
    "The registry `tetelestai_terminal_v408` reads, at every rite, the %(ancoras)d anchors, the %(modulos)d modules by sha256, the flags, the frozen gate verdict and the purged input (%(checks)d checks, all passed); "
    "no old key changes; the %(falas)d sayings of the operator of 04/11 are embedded by sha256 in `cunhagens_v408`.") % N) + REV_EN +
    (" Validity in the kernel is not accreditation; the gate did not move. Certified by the sha256 the program reads of itself (%(pin)s)." % N))
KERNEL_LEITURA_EN = (
    ("the kernel proves the terms: the %(ancoras)d anchors exist in the trio, with the provenance the compiler emits in the expected modules; `tetelestai` (the terminal is the reading: the engine returns the post for every r and t), "
     "`o_tempo_e_a_moeda` (the payment is price times time: the Jones contraction and the dephasing are the flow of the axiom to the payments r s and β t), `o_ponto_de_contradicao` (1 = 0 read on the two faces, with the concrete Fock inhabitant by rfl), "
     "`p_igual_np` (P is P only when read by the minimally coupled module n) and `p_igual_np_nas_classes_do_dicionario` (the classes `ClasseP` and `ClasseNP`, defined in Lean on the same problem T, are the same set: the solution of every problem is reached by a real polynomial word q in T with q(0) ≠ 0 and degree of q below dim End H, `palavra_com_grau`; and the reading of the solution of T at every unit state is 1 iff T ψ = 0, `leitura_um_sse_solucao`) are terms; `as_classes_do_dicionario` keeps the finite face. "
     "By the operator's rule (prove or prune, D49) no identification of his stays parked: what has a mirror is proved under his name (kernel validity, not creditation), and what has none was pruned: the word «impedância» (no term; the content keeps his name «" + DL.FRASE_INCLINACAO_NOME + "», mirrored as a_inclinacao_modular). "
     + _D51_EN + " (D51 revised). The lock (1 − P) and the modular Hamiltonian (K = −log Δ) are distinct objects that share Ω as zero mode; their identification stays pruned. "
     "β enters only by name (TGLCoupling.beta in the kernel; α of CODATA 2018 times √e at runtime), never as a literal. Validity in the kernel is not accreditation.") % N)
ABERTOS_EN = (
    "The pair of psions on the Fock face stays open as a LINK to be made, not as an absence of terms (errata E21): the abstract certificate has no creation operators as terms, but the concrete Fock space "
    "(the inhabitant of the physical certificate, by rfl) has them. The bridge between the Bell space and the TT sector of spin two is not a term. K(O) ≠ ⊥ for a compact O is not a theorem beyond the wedge. "
    "The translation of the classes of the operator's dictionary to the classes of Turing machines stays open (D51 revised): " + _D51_EN + "; the linear time in the floors is an identity of a flow for the Name of the tower. "
    "The word «impedância» is pruned as a term (D50). Two phrases of the management were corrected by E22 (one gave the TGL as having no terminal; the other, in the R1 of the stone, read the remainder without trace as a relation without payment): "
    "both were wrong by the theorems of the house and were pruned. The input from the archive enters only by its purged copy (E23); the full text stays outside the mirror by the order of the operator and is cited only by sha16. "
    "No test with nature: no new datum, no rite of nature changed; the discrimination at 5σ, β_TGL in nature, stays with nature; the gate did not move." + REV_EN +
    " The [LEGAL] decision D2 and the pinned README (D39) stay outside the program.")
ARCO_EN = (
    "The custody of v408 (complete round): Tetelestai is the terminal. %(modulos)d new kernel modules (" + NOMES_ASCII + ", with the names the operator gave), %(bandeiras)d new flags, ladder %(escada_a)d to %(escada_b)d, "
    "none outside the trio. The terminal is the reading, not the end of the decay; there is no relation without weight; time is the currency of beta; the point of contradiction reads 1 = 0 on both faces; "
    "P = nP is a theorem in the computation classes of the operator’s dictionary, defined in Lean (ClasseP, ClasseNP) and proved in the stone PIgualNP (kernel validity, not creditation) (p_igual_np_nas_classes_do_dicionario); the translation to the classes of Turing machines (bits = log2 n) is [OPEN], not a refusal. No old key changes. Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the word of accreditation.") % N
ARCO_PT = (
    "A custódia da v408 (rodada completa): Tetelestai é o terminal. %(modulos)d módulos novos no kernel (" + NOMES_ASCII + ", com os nomes que o operador deu), %(bandeiras)d bandeiras novas, escada %(escada_a)d para %(escada_b)d, "
    "nada fora do trio. O terminal é a leitura, não o fim do decaimento; não há relação sem peso; o tempo é a moeda de β; o ponto de contradição lê 1 = 0 nas duas faces; "
    "P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); a tradução às classes das máquinas de Turing (bits = log2 n) é [OPEN], não recusa. Nenhuma chave antiga muda. Validade no kernel não é creditação; o gate não se moveu. NOT_FALSIFIED nunca é a palavra da creditação.") % N
COMMIT = (
    "Tetelestai e o terminal: o terminal e a leitura, nao o fim do decaimento; nao ha relacao sem peso; o tempo e a moeda de beta. %(modulos)d modulos novos (" + NOMES_ASCII + ", nomes do operador), %(bandeiras)d bandeiras, "
    "escada %(escada_a)d para %(escada_b)d, nada fora do trio. P = nP e teorema nas classes de computacao do dicionario do operador, definidas em Lean (ClasseP, ClasseNP) e provadas em p_igual_np_nas_classes_do_dicionario; a traducao as classes das maquinas de Turing (bits = log2 n) e [OPEN], nao recusa; nenhuma chave antiga muda. Validade no kernel nao e creditacao; o gate nao se moveu.") % N + REV_COMMIT
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
    guardas[ident] = {"guarda_frases_v408": v1, "portao_g1": v2, "forma": v3, "n_chars": len(t)}
    if v1 or v2 or v3:
        falhas.append((ident, v1, v2, v3))
if falhas:
    for f_ in falhas:
        print("REPROVADO:", f_)
    sys.exit(1)
print("guardas: os sete textos passaram (guarda de frases v408, portao do G1, forma do ARCO/COMMIT, sem 4,44)")

# ------------------------------------------------------------------ 4. o acrescimo, com backup de bytes
cab = ("\n\n**Textos da custódia (gerência c1, 04/11/2026; substituem o molde factual do G1; números lidos do core selado, do selo e do diário por "
       "`pos_rito\\textos_custodia_handoff_v408.py`, que os conferiu contra ESPERADOS e passou os textos pela guarda de frases da v408 e pelo portão do G1 antes de os anexar (D52: encadeado no fim do S6); "
       "o par de psíons na face de Fock segue em aberto como ligação (E21); nenhuma chave antiga muda; validade no kernel não é creditação):**\n")
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
       "motivo": "S7 do orquestrador pode parar em rc 20: faltam os sete marcadores opcionais da prosa da custodia (sem eles, molde factual ou --aceitar-molde); D52: os textos entram encadeados no fim do S6",
       "estatuto": "REAL (numeros lidos do core selado, do selo e do diario e conferidos contra ESPERADOS; textos da gerencia c1, em nome proprio); NOT_FALSIFIED nunca e a palavra da creditacao; o gate nao se move"}
(HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo:", HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json")
