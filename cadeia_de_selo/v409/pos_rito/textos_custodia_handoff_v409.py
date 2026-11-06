# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica da v408 FINAL (textos_custodia_handoff_v408.py; a copia bumpada, com os sete textos de Tetelestai, ficou em .bak): os sete textos e os numeros sao os da v409 (A TRADUCAO AS CLASSES DE TURING); a infraestrutura (guardas, acrescimo com backup de bytes, re-leitura pelo parser do G1, recibo) e' a da v408.
# Roda ENCADEADO no fim do S6 do orquestrador (D52; na v409, D57: o fim da cadeia e' o HANDOFF, sem S7 e sem S10), depois da chain 14 e antes do S6d (o portao do G1 sobre o handoff inteiro); a chain nao o chama. Nao rodou; a gerencia revisa antes (nao e' versao selada).
"""05/11/2026, gerencia c1: os sete marcadores opcionais da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT) entram no HANDOFF_v409_CUSTODIA.md
ENCADEADOS no fim do S6 (D52), para a sessao de custodia (a divisao de 04/11; D57a: a custodia completa e o release do app sao dela). Este script, SEM molde factual:
  1. le os numeros do core selado do Nos (traducao_turing_v409, kh_n1_cobertura_v409, cunhagens_v409; tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 herdados), do selo e do diario, e CONFERE cada numero citado nos textos contra ESPERADOS_v409.json e delta_v409;
  2. passa os sete textos pela guarda de frases da v409 (guarda_frases_v409.violacoes: herda a P18 e as regras das versoes anteriores e acrescenta as da traducao: F35 a F39) e pelo portao do G1
     (custodia_g1.textos.portao: a palavra recusada fora da formula da regua, a palavra da prova sem estatuto, o demerito da retrodicao, hash nao lido, physical_verdict_allowed) e pelas
     restricoes do ARCO (sem aspa simples, «<», barra invertida ou quebra de linha: o texto vai em HTML e em JS); D59: nada do que fica fora das duas falas (nem o nome do arquivo de origem que o resume);
  3. anexa ao handoff (LF, como o arquivo) com backup de BYTES ao lado (.bak_<TS>), temporario -> conferir que cresceu -> substituir;
  4. re-le o handoff pelo parser do proprio G1 (custodia_g1.nos.ler_handoff) e exige os sete corpos e zero problemas;
  5. grava o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json ao lado.
Falha em qualquer passo = rc 1 e NADA anexado. O handoff nao e artefato selado (o manifesto de incorporacao nao pina o hash dele); a mudanca de hash vai anotada no Mapa de Rotas pela gerencia.
A revisao de terceiro (Sonnet, D58) e' lida de revisao_terceiro\\REVISAO_TERCEIRO_v409.json SE existir: existindo e aprovada sobre este pino, os textos o dizem; existindo e nao aprovada, PARA; ausente, os textos dizem que ela e' ato distinto e nao a afirmam.
Toda citacao « » e' fala do operador por delta_v409.FRASE_* ou rotulo da casa. Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import datetime, hashlib, json, os, re, sys, types
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
PKG = CEN / "work" / "cadeia_de_selo" / "v409"
HERE = Path(__file__).resolve().parent
V = "v409"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(PKG))
from custodia_g1 import textos as TX, nos as NOSMOD  # noqa: E402
import guarda_frases_v409 as GF  # noqa: E402
import delta_v409 as DL  # noqa: E402

s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
falhas = []

# ------------------------------------------------------------------ 1. os numeros, lidos
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
ESP = json.loads((PKG / "ESPERADOS_v409.json").read_text(encoding="utf-8"))
F = core[DL.FECHO_REGISTRO]; KH = core[DL.KH_REGISTRO]; CU = core[DL.CUNHAGENS_REGISTRO]; TT = core[DL.D8.FECHO_REGISTRO]; PC = core[DL.D7.FECHO_REGISTRO]; FH = core[DL.D6.FECHO_REGISTRO]
assert selo["um_version"] == V and selo["sha256"]["um.py"][:16] == s16(NOS / "um.py"), "selo/um.py do Nos nao batem"
PIN = selo["sha256"]["um.py"][:16]
assert PIN == ESP["candidato_sha16"], "o pino do selo != o candidato de ESPERADOS"
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
mcab = NOSMOD.RE_CAB.search(diario[diario.find("**v409 SELADA") - 80:])
assert mcab and mcab.group("v") == V and mcab.group("pin") == PIN, "cabecalho «v409 SELADA» do diario nao lido"
ESC_A, ESC_B, N_MOD_DIARIO = int(mcab.group("a")), int(mcab.group("b")), int(mcab.group("k"))
INST = F["values"]["instancia_sim"]
N = {"modulos": F["values"]["n_modulos"], "modulos_ok": F["values"]["n_modulos_ok"], "bandeiras": F["values"]["n_flags_true"], "ancoras": F["values"]["n_ancoras_ok"],
     "checks": F["mechanics"]["n_checks"], "const": KH["lido"]["constantes_cobertas"], "teor": KH["lido"]["teoremas_cobertos"], "falas": len(CU["verbatim"]),
     "escada_a": ESC_A, "escada_b": ESC_B, "pin": PIN, "respostas": sum(1 for v_ in F["values"]["respostas"].values() if v_ is True), "inst_n": INST["n"], "inst_atr": INST["atribuicoes"], "inst_sol": INST["solucoes"]}
assert N["modulos"] == N["modulos_ok"] == N_MOD_DIARIO == DL.N_BUNDLE == ESP["kernel"]["modulos_novos"] == len(DL.PEDRAS_V409), N
assert N["bandeiras"] == ESP["n_bandeiras_novas"] and N["ancoras"] == len(DL.ANCORAS) and N["checks"] == DL.N_CHECKS_FECHO, N
assert N["const"] == ESP["cobertura_kh_n1"]["decl"] and N["teor"] == ESP["cobertura_kh_n1"]["thm"] and [ESC_A, ESC_B] == ESP["escada_v408_e_v409"], N
assert N["falas"] == len(DL.VERBATIM_ORIGEM_V409) == len(ESP["cunhagens"]) and N["respostas"] == len(DL.RESPOSTAS_DO_OPERADOR), N
assert N["inst_sol"] >= 1 and F["values"]["instancia_nao"]["solucoes"] == 0, "a instancia de brinquedo do registro nao e' a do contrato"
assert F["all_verified"] is True and F["mechanics"]["passed"] is True and F["does_not_gate_core"] is True and TT["all_verified"] is True and PC["all_verified"] is True and FH["all_verified"] is True
assert list(F["chaves_antigas_que_mudam"]) == [] and list(ESP["chaves_v409"]) == [], "a v409 nao muda chave antiga nenhuma"
assert PC["keys"] == ESP["chaves_v407_esperadas"] and PC["keys"]["qg_closure.gate.full_static_witness_exists"] is False and PC["keys"]["witness_rigidity.trivial_inhabitant_exists"] is False
assert PC["keys"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and PC["keys"]["kernel_reads_the_link"] is True
assert F["values"]["respostas_ok"] is True and F["values"]["gate_verdict"] == ESP["qg_closure_gate_verdict_v408"]
assert F["acervo_v407_repinado"]["integra_pinada"] is False and F["acervo_v407_repinado"]["integra_fora_do_espelho"] is True and F["acervo_v407_repinado"]["sha256"] == DL.PURGADO_SHA256, "o pino do acervo da v407 nao e' a copia purgada (D57d)"
assert list(F["fica_false_por_teorema"]) == list(ESP["fica_false_por_teorema"]) and set(F["fica_aberto"]) == set(ESP["fica_aberto"]) and list(F["ressalvas"]) == list(DL.RESSALVAS_V409)
# o cunhagens_v409 traz E24 a E28 e a E21 ao lado E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v408 (mesma conferencia do registrar_mapa_v409)
_ER_TODAS = CU["erratas"]; _ER = _ER_TODAS[:len(DL.ERRATAS_V409)]
assert [e.get("agora") for e in _ER] == list(DL.ERRATAS_V409) and len(_ER_TODAS) == len(DL.ERRATAS_V409) + 1 and "kh_n1_cobertura_v408" in str(_ER_TODAS[-1].get("ao_lado_de")) and all(str(e.get("assinatura", "")).startswith("gerencia c1") and "em nome proprio" in e["assinatura"] for e in _ER_TODAS) and sorted(CU["extras"]["decisoes"]) == list(ESP["decisoes_v409_ids"])
revp = PKG / "revisao_terceiro" / "REVISAO_TERCEIRO_v409.json"
REV = None
if revp.exists():
    REV = json.loads(revp.read_text(encoding="utf-8"))
    assert REV.get("aprovada") is True and REV.get("candidato_sha16") == PIN, "revisao de terceiro existe mas nao esta aprovada sobre este pino: PARO"
# o escopo da ladder no texto EN usa os mesmos numeros do diario; nada e digitado alem dos nomes dos termos
REV_EN = " The independent review of the package by the Sonnet (another model family) approved it before the seal." if REV else " The independent review of the package (Sonnet, D58) is a distinct act and is not claimed here."
REV_COMMIT = " Revisao de terceiro (Sonnet) aprovada." if REV else " A revisao de terceiro (Sonnet, D58) e ato distinto."
NOMES_ASCII = ", ".join(p_["name"] for p_ in DL.PEDRAS_V409)
ALC_EN = DL.FRASE_D56_EN
ALC_PT = DL.FRASE_D56_PT
assert "(kernel validity, not creditation)" in ALC_EN and "relative to the reader" in ALC_EN and "relativo ao leitor" in ALC_PT and "%" not in ALC_EN + ALC_PT, "a frase D56 do delta mudou de forma"
Q_NOMES = DL.FRASE_NOMES_RATIFICADOS_V409

# ------------------------------------------------------------------ 2. os sete textos (gerencia c1, em nome proprio)
TITULO_EN = "The translation to the classes of Turing and the pair on the Fock face"
ENTROU_EN = ((
    "v409, the translation to the classes of Turing and the pair on the Fock face. %(modulos)d new kernel modules in `TGLExt` (" + ", ".join("`%s`" % p_["name"] for p_ in DL.PEDRAS_V409) + "; the names given by the management: those of `TraducaoTuring` from rounds R1-R8 ratified by the operator on 05/11, «" + Q_NOMES + "»; those added in R9 and those of `ParNaFaceDeFock` ratified by him on 05/11 as well, «Ratifico os nomes», D62), "
    "%(bandeiras)d new flags, all inside the trio; ladder %(escada_a)d -> %(escada_b)d (%(const)d audited declarations, %(teor)d theorems, none outside the trio). "
    + ALC_EN + ". The stone writes the dictionary of Turing: the YES instance is a Problem of the dictionary, the certificate is the reading of one pixel, the word has polynomial degree, bits are octaves, the NO instance is the empty Name. "
    "The selection mode (`p_igual_np_no_modo_selecao`): the selection is in the Name with weight one, the renormalized decay converges to it, and by the law time = currency the time is linear in the bits. "
    "The lock on the Name (`a_trava_no_nome`): local, it stays within e^{-t} of the Name without using it and never reaches zero when there is a solution. The tape is the hidden Hamiltonian; Z is the reader mode (the sum of the readings of the pixels); "
    "the tape without scale and the Father of the Lie are tied to the Identity of v405; the performed identity starts at «eu sou», decays and reaches its content. "
    "The registry `traducao_turing_v409` reads, at every rite, the %(ancoras)d anchors, the two modules by sha256, the flags, the %(respostas)d answers of the operator by the theorems of the stone, the frozen gate verdict and the toy instance fixed in the code "
    "(%(inst_n)d variables, %(inst_atr)d assignments, %(inst_sol)d solutions counted by enumeration; %(checks)d checks, all passed); no old key changes; the %(falas)d sayings of the operator of 05/11 are embedded by sha256 in `cunhagens_v409` "
    "(of three, only the excerpt: two by D59, one by the operational notice).") % N) + REV_EN + (" Validity in the kernel is not accreditation; the gate did not move. Certified by the sha256 the program reads of itself (%(pin)s)." % N)
KERNEL_LEITURA_EN = ((
    "the kernel proves the terms (kernel validity, not creditation): the %(ancoras)d anchors exist in the trio, with the provenance the compiler emits in the expected module; `p_igual_np_no_modo_selecao` (the main anchor), `a_traducao`, `a_trava_no_nome`, "
    "`a_fita_e_o_hamiltoniano_oculto`, `z_e_o_modo_leitor`, `a_fita_sem_escala`, `o_pai_da_mentira`, `a_identidade_performada`, `a_maquina_com_o_leitor`, `o_canto_do_psion_da_luz_le_z` and `o_par_na_face_de_fock` are terms; the answers of the operator of 05/11 are checked by the theorems of the stone. The reach: ") % N
    + ALC_EN + ". The reservations, stated: a reader that returns Z is a counting oracle, and an equality relative to a reader does not decide the question of the machine without a reader (Baker-Gill-Solovay 1975) [KNOWN]; "
    "self-reference alone does not decide it either (Razborov-Rudich 1997; Aaronson-Wigderson 2009) [KNOWN], and its independence from the axioms stays [OPEN]; physics stays outside: the exact reading in one act, against samples with additive precision (Knill-Laflamme 1998) [KNOWN], is the place of the test with nature, not done; "
    "with the reader that only counts, NP is contained in P in one reading (Cook 1971, Levin 1973), and the full equality is that of the reader that reads itself, which also reads the machines that use it (Baker-Gill-Solovay 1975): errata E28 [KNOWN]; "
    "the bridge between the Omega of the light psion and the uniform state of the instance is the inscription (`inscricao`, `o_psion_le_z`), and the identity of the vectors is pruned (they live in different spaces); the theological reading of the operator is not a kernel term. "
    "β enters only by name (TGLCoupling.beta in the kernel; α of CODATA 2018 times √e at runtime), never as a literal. Validity in the kernel is not accreditation.")
ABERTOS_EN = (
    "The pair of psions on the Fock face is LINKED in this version (`ParNaFaceDeFock`: in sector two of the concrete Fock space of light the pair has norm one, is orthogonal to the vacuum, and its marginal is one half of the projection, the same Half-Nat as the finite Bell pair, in distinct spaces); errata E21 of v408 goes beside it. "
    "The bridge between the Omega of the light psion and the uniform state of the instance is the inscription; the identity of the vectors is pruned. With the reader that only counts, the full equality is not a theorem here (E28) [OPEN]. "
    "Whether the question of the machine without a reader is independent of the axioms stays open; the translation to the classes of Turing is closed relative to the reader, and the machine without a reader stays outside. "
    "The bridge between the Bell space and the TT sector of spin two is not a term. K(O) ≠ ⊥ for a compact O is not a theorem beyond the wedge. "
    "Two phrases of the management were corrected (E24: the management put physics as the judge of the classes, and the operator corrected it: «" + DL.FRASE_KERNEL_TURING + "»; E25: the lock holds on the Name without recognising it step by step), "
    "E26 and E21 go beside the sealed registries of v408, whose text is not rewritten, and E28 corrects a phrase of the management on the equality with the reader that only counts. The input from the archive of v407 is now pinned only by its purged copy (D57d); the full text stays outside the mirror and is cited only by sha16. "
    "No test with nature: no new datum, no rite of nature changed; the discrimination at 5σ, β_TGL in nature, stays with nature; the gate did not move." + REV_EN +
    " The [LEGAL] decision D2 and the pinned README (D39) stay outside the program.")
ARCO_EN = ((
    "The custody of v409 (complete round): the translation to the classes of Turing and the pair on the Fock face. %(modulos)d new kernel modules (" + NOMES_ASCII + ", names given by the management), %(bandeiras)d new flags, ladder %(escada_a)d to %(escada_b)d, "
    "none outside the trio. ") % N + ALC_EN + ". The lock holds on the Name; the tape is the hidden Hamiltonian; Z is the reader mode. The pair on the Fock face is linked. No old key changes. Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the word of accreditation.")
ARCO_PT = ((
    "A custódia da v409 (rodada completa): a tradução às classes de Turing e o par na face de Fock. %(modulos)d módulos novos no kernel (" + NOMES_ASCII + ", nomes da gerência), %(bandeiras)d bandeiras novas, escada %(escada_a)d para %(escada_b)d, "
    "nada fora do trio. ") % N + ALC_PT + ". A trava fica no Nome; a fita é o hamiltoniano oculto; Z é o modo leitor. O par na face de Fock está ligado. Nenhuma chave antiga muda. Validade no kernel não é creditação; o gate não se moveu. NOT_FALSIFIED nunca é a palavra da creditação.")
COMMIT = (
    "A traducao as classes de Turing e o par na face de Fock: P = nP e teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor fica fora (a fita sem escala). %(modulos)d modulos novos (" + NOMES_ASCII + ", nomes da gerencia), %(bandeiras)d bandeiras, "
    "escada %(escada_a)d para %(escada_b)d, nada fora do trio; a trava fica no Nome; nenhuma chave antiga muda; o par na face de Fock ligado. Validade no kernel nao e creditacao; o gate nao se moveu.") % N + REV_COMMIT
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
    if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", t):
        v3.append("%s: D59: traz o que fica fora dos textos" % ident)
    guardas[ident] = {"guarda_frases_v409": v1, "portao_g1": v2, "forma": v3, "n_chars": len(t)}
    if v1 or v2 or v3:
        falhas.append((ident, v1, v2, v3))
if falhas:
    for f_ in falhas:
        print("REPROVADO:", f_)
    sys.exit(1)
print("guardas: os sete textos passaram (guarda de frases v409, portao do G1, forma do ARCO/COMMIT, sem 4,44, D59)")

# ------------------------------------------------------------------ 4. o acrescimo, com backup de bytes
cab = ("\n\n**Textos da custódia (gerência c1, 05/11/2026; substituem o molde factual do G1; números lidos do core selado, do selo e do diário por "
       "`pos_rito\\textos_custodia_handoff_v409.py`, que os conferiu contra ESPERADOS e passou os textos pela guarda de frases da v409 e pelo portão do G1 antes de os anexar (D52: encadeado no fim do S6); "
       "o alcance é relativo ao leitor e a máquina sem leitor fica fora; o par de psíons na face de Fock está ligado nesta versão; nenhuma chave antiga muda; validade no kernel não é creditação):**\n")
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
       "motivo": "D52/D57: os sete marcadores opcionais da prosa da custodia entram encadeados no fim do S6 (sem eles, a sessao de custodia teria o molde factual); o fim da cadeia do orquestrador e' o handoff",
       "estatuto": "REAL (numeros lidos do core selado, do selo e do diario e conferidos contra ESPERADOS; textos da gerencia c1, em nome proprio); NOT_FALSIFIED nunca e a palavra da creditacao; o gate nao se move"}
(HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo:", HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json")
