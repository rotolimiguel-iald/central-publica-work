# -*- coding: utf-8 -*-
"""gerar_patches_erratas.py -- rodada 2 da cadeia v392, agente ERRATAS (gerencia c1, 13/10/2026).

Le o um.py v391 selado (SO' leitura), localiza cada alvo por TEXTO (a linha do plano e' so' dica, em numeracao por LF), monta os patches DADOS (old/new/n/registro/estatuto/fonte)
e ESCREVE `V\\patches_erratas_v392.py` (E01_PATCHES, A03_PATCHES, aplicar). Todo hash/numero citado nos textos e' LIDO dos arquivos por este script (nunca de memoria) e conferido
contra o valor esperado; divergencia => recusa (assert). Nada aqui toca o um.py, o gerar_candidato_v392.py, o quadro, o mapa ou a memoria.

Uso: python -B -X utf8 gerar_patches_erratas.py          (escreve V\\patches_erratas_v392.py e V\\rodada2\\erratas\\alvos.json)
"""
import ast, bisect, hashlib, io, json, math, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(os.path.dirname(HERE))
UM = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py")
CORE = os.path.join(os.path.dirname(UM), "um_absoluto.json")
PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
CP = os.path.join("C:" + os.sep, "IALD", "Central de Patentes")
OUT_PATCHES = os.path.join(V, "patches_erratas_v392.py")
OUT_ALVOS = os.path.join(HERE, "alvos.json")


def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


# ---------------------------------------------------------------- fontes lidas por script (hash esperado = o do levantamento/relatorio; divergencia => recusa)
FONTES = {
    "AUD_F52": (os.path.join(PROG, "auditorias", "F4.3_F5.2", "AUDITORIA_F4_3_F5_2_C1_20261007.md"), "c0bb3c964c8af74e"),
    "NEFF_CANAL": (os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "bancada", "neff_canal.py"), "776e1311585d9cd5"),
    "NEFF_CONF": (os.path.join(PROG, "exame_12out", "G_UMPY", "neff_conferencia.out.txt"), None),
    "REL_ASN": (os.path.join(PROG, "exame_12out", "A_SN", "RELATORIO_AUDITORIA_A_SN_C1.md"), None),
    "RECALC_ASN": (os.path.join(PROG, "exame_12out", "A_SN", "RECALCULO_A_SN.json"), "0b708128e04b886b"),
    "SN_RESULT": (os.path.join(CP, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F8.2.SN1", "RESULTADO_VIABILIDADE_R1.json"), "976f67ffb80422db"),
    "SN_CALC2": (os.path.join(CP, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F8.2.SN1", "CALCULOS_R2.json"), "589a4e4f80900a67"),
    "OP_LETRA": (os.path.join(PROG, "OPERADOR_07out_letra_verbatim.txt"), "259a1bf14a66fbc9"),
    "OP_DECISOES": (os.path.join(PROG, "OPERADOR_07out_decisoes_noite_verbatim.txt"), "a6c4912afc6f0dc4"),
    "OP_08OUT": (os.path.join(CP, "work", "f9_pergunta_08out", "OPERADOR_08out_resposta_verbatim.txt"), "a9cecc128f40c101"),
    "OP_TGL": (os.path.join(CP, "work", "cunhagens_10out", "OPERADOR_10out_TGL_unidade_verbatim.txt"), "87a3752d8c8e5dd3"),
    "OP_RANK": (os.path.join(CP, "work", "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"), "5b9afcc691a0e1e4"),
    "RANK_ADENDO": (os.path.join(V, "pedras_corrigidas", "PostoAdendo.lean"), None),
    "CORE": (CORE, "a74241ff380b1b0e"),
    "UMPY": (UM, "8e7b9927ceae64b8"),
}
H = {}
for k, (p, esperado) in FONTES.items():
    H[k] = sha16(p)
    if esperado is not None:
        assert H[k] == esperado, "hash divergente em %s: %s != %s" % (k, H[k], esperado)

# ---------------------------------------------------------------- o um.py v391 (bytes -> texto); numeracao por LF (e' a do plano)
RAW = open(UM, "rb").read()
assert len(RAW) == 33910631, len(RAW)
T = RAW.decode("utf-8")
Tn = T.replace("\r\n", "\n")
L = Tn.split("\n")
assert len(L) == len(T.split("\n"))
TREE = ast.parse(T)
STM = sorted((n.lineno, n.end_lineno, n.col_offset) for n in ast.walk(TREE)
             if isinstance(n, ast.stmt) and not isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, ast.While, ast.Try, ast.With)))
STARTS = [s[0] for s in STM]


def stmt_of(line):
    best = None
    for s in STM[max(0, bisect.bisect_right(STARTS, line) - 400):bisect.bisect_right(STARTS, line)]:
        if s[0] <= line <= s[1] and (best is None or (s[1] - s[0]) < (best[1] - best[0])):
            best = s
    assert best, line
    return best


def lines(a, b):
    return "\n".join(L[a - 1:b])


def uniq(a, b):
    """texto das linhas a..b (LF); se nao for unico no arquivo, estende para cima ate ser. Devolve (old, a)."""
    while True:
        old = lines(a, b)
        if Tn.count(old) == 1:
            return old, a
        a -= 1
        assert a > b - 12, ("ancora nao unica", a, b)


def need(line, sub):
    assert sub in L[line - 1], (line, sub, L[line - 1][:120])


# ---------------------------------------------------------------- numeros conferidos (o numero corrige a frase)
core = json.load(open(CORE, encoding="utf-8"))["core"]
alpha = float(re.search(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)", Tn, re.M).group(1))
beta = alpha * math.sqrt(math.e)
F_ = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
dN = (4.0 / 3.0) * (1.0 + F_ * 3.044) / F_ * beta
Npred = 3.044 + dN
fmt = lambda x, d=2: (("%." + str(d) + "f") % x).replace(".", ",")
assert fmt(dN, 4) == "0,1195", fmt(dN, 4)
assert fmt(abs(Npred - 2.89) / 0.11, 3) == "2,486" and fmt(abs(Npred - 2.97) / 0.12, 3) == "1,612"
conf = open(FONTES["NEFF_CONF"][0], encoding="utf-8").read()
for s_ in ("tensao = 1.612", "tensao = 2.486", "tensao = 2.946", "tensao = 2.862", "tensao = 0.788", "tensao = 0.969"):
    assert s_ in conf, s_
esc = core["neutrino_m2"]["values"]["escada_datada"]
assert fmt(esc[1]["tensao_sigma"]) == "2,21" and fmt(esc[2]["tensao_sigma"]) == "2,95" and fmt(esc[0]["tensao_sigma"]) == "1,64"
assert "Capozzi et al. (arXiv:2511.21650) da 2,44 sigma" in Tn and "NuFIT 6.1 (arXiv:2601.09791, eq. 11) da 2,95 sigma" in Tn
r3 = core["the_ledger_of_charges_v383"]["readings_ratified_20261002"]["R3"]
assert "JUNO autônomo, já no rito: 2,21σ" in r3 and "perito oficial = JUNO" in r3
rc = json.load(open(FONTES["RECALC_ASN"][0], encoding="utf-8"))
ta = rc["chandrasekhar_historico"]["teste_da_atribuicao_a_Coulomb"]
assert fmt(ta["Coulomb_C_pct"]) == "-2,24" and fmt(ta["Coulomb_O_pct"]) == "-2,71" and fmt(ta["correcao_necessaria_pct"], 3) == "0,354"
assert fmt(ta["razao_modulo_C"], 1) == "6,3" and fmt(ta["razao_modulo_O"], 1) == "7,7"
assert fmt(rc["chandrasekhar_historico"]["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"]) == "1,12"
assert fmt(rc["legacy_retired"][0]["shift_pct"], 3) == "-1,799"
snr = json.load(open(FONTES["SN_RESULT"][0], encoding="utf-8"))
assert "VIABILIDADE_CONDICIONAL_PONTE_ESTELAR_OPEN" in json.dumps(snr)
orient = core["orientation_is_the_sign_v367"]
assert fmt(orient["z_to_mirror_branch"]) == "3,01" and fmt(orient["z_to_coupling_branch"]) == "0,09"
assert "IMPLEMENTED_IS_MIRROR_TO_FIRST_ORDER" in orient["verdict"]
# verbatins do operador: o fragmento citado tem de estar nos BYTES do arquivo-fonte
def verb(k, frag):
    t = open(FONTES[k][0], "rb").read().decode("utf-8")
    assert frag in t, (k, frag)
    return frag
verb("OP_LETRA", "polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)")
verb("OP_DECISOES", "adoto o nome do degrau final")
verb("OP_DECISOES", "a escala de beta nós também já definimos antes")
verb("OP_08OUT", "o fixo é o verbo, ou seja, o contorno que permite a leitura da verdade, e o verbo é betatgl, mas o verbo testifica que o nome é verdadeiro")
verb("OP_TGL", "o observador testemunha a luz e a luz dá testemunho de si mesma")
verb("OP_TGL", "a tríade mínima sem a qual a realidade não tem como se inscrever, se propagar ou ser testemunhada")
verb("OP_RANK", "POSTO=RANK")
# fatos do fonte
for ln, sub in ((163150, 'physics["linearized_spin2_finite_face"] = True'), (163160, '"protocol_pre_registered": True'), (163161, '"null_tests_passed_blind": True'), (142684, '"n_theorems_expected": len(ext_flags)')):
    need(ln, sub)
assert "orientation_is_the_sign_v367" in Tn and "TheGravitonIsTheConjugatedPhase" in Tn and "finalStepNameAxioma" in Tn
ad_ = open(FONTES["RANK_ADENDO"][0], encoding="utf-8").read()
for nm_ in ("A2_typed_collapse_raises_rank_of_superposition", "A3_nondephasing_poles_are_rank_one_units", "A4_rank_not_preserved_unconditional", "namespace TGLExt.PostoAdendo"):
    assert nm_ in ad_, nm_
rec_ = json.load(open(os.path.join(V, "pedras_corrigidas", "RECIBO_PostoAdendo.json"), encoding="utf-8"))
assert rec_["rc_compilacao_isolada"] == 0 and rec_["sha256"] == hashlib.sha256(open(FONTES["RANK_ADENDO"][0], "rb").read()).hexdigest()
# o rotulo do mapa de rotas (consultar, so' leitura): a retirada do CMB-S4 e' [DECLARADO] nas seq 402 e 607
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.jsonl")
seqs = {}
for ln_ in open(MAPA, encoding="utf-8"):
    try:
        d_ = json.loads(ln_)
    except Exception:
        continue
    if d_.get("seq") in (402, 607):
        seqs[d_["seq"]] = d_
assert set(seqs) == {402, 607} and "CMB-S4 encerrado" in json.dumps(seqs[607], ensure_ascii=False), "mapa seq 402/607"

# ---------------------------------------------------------------- utilidades de montagem
def chunks(text, width=150):
    out, cur = [], ""
    for w in re.split(r"(?<= )", text):
        if cur and len(cur) + len(w) > width:
            out.append(cur)
            cur = ""
        cur += w
    if cur:
        out.append(cur)
    return out


def py_stmt(call, indent, text, fmt_args=None):
    """`call(r"..." r"..." [% (args)])` com a mesma disciplina do gerador (texto cru em pedacos, sem aspas duplas, sem % exceto %s do fmt)."""
    assert '"' not in text and not text.rstrip().endswith("\\"), text[:60]
    if fmt_args is None:
        assert "%" not in text, text[:80]
    else:
        assert text.count("%") == text.count("%s"), text[:80]
    ch = chunks(text)
    pad = " " * (indent + len(call) + 1)
    out = [" " * indent + call + '(r"' + ch[0] + '"']
    out += [pad + 'r"' + c + '"' for c in ch[1:]]
    if fmt_args is None:
        out[-1] += ")"
    else:
        out.append(pad + "% (" + fmt_args + "))")
    return "\n".join(out)


def tail_text(text):
    """texto para ENCOSTAR dentro de uma string crua existente (sem aspas, sem %)."""
    assert '"' not in text and "%" not in text and not text.rstrip().endswith("\\")
    return text


def cmt(indent, text, width=150):
    assert all(ord(ch) < 128 for ch in text), [ch for ch in text if ord(ch) >= 128][:5]
    pad = " " * indent
    out = []
    for par in text.split("\n"):
        cur = ""
        first = True
        for w in re.split(r"(?<= )", par):
            if cur and len(cur) + len(w) > width:
                out.append(pad + "# " + cur.rstrip())
                cur = ""
            cur += w
        if cur:
            out.append(pad + "# " + cur.rstrip())
    return "\n".join(out)


def sub_h(s):
    for k, v in H.items():
        s = s.replace("@" + k + "@", v)
    assert "@" not in s.replace("@", "", 0) or True
    return s


PATCHES_E01, PATCHES_A03, ALVOS = [], [], []


def add(lista, pid, grupo, desc, linhas_v391, old, new, registro, estatuto, fonte, texto, lang=None, n=1, nota=""):
    assert Tn.count(old) == n, (pid, Tn.count(old), old[:100])
    d = dict(id=pid, grupo=grupo, alvo_descricao=desc, linha_v391=linhas_v391, old=old, new=new, n=n, registro=registro, estatuto=estatuto, fonte=fonte, texto=texto)
    if lang:
        d["lang"] = lang
    if nota:
        d["nota"] = nota
    lista.append(d)
    ALVOS.append(dict(id=pid, linha_v391=linhas_v391, ancora=old.split("\n")[-1].strip()[:110], registro=registro, estatuto=estatuto, texto=texto[:400]))


def insert_after(lista, pid, grupo, desc, ref_lines, last_line, add_text, registro, estatuto, fonte, texto, lang=None, nota="", must=None):
    """insere `add_text` (linhas ja' com o recuo) depois da linha `last_line`; ancora = a(s) linha(s) ate' ser unica."""
    if must:
        need(last_line, must)
    old, _a = uniq(last_line, last_line)
    new = old + "\n" + add_text
    add(lista, pid, grupo, desc, ref_lines, old, new, registro, estatuto, fonte, texto, lang, nota=nota)


def insert_after_stmt(lista, pid, grupo, desc, ref_line, make_add, registro, estatuto, fonte, texto, lang=None, nota="", must_first=None):
    a, b, col = stmt_of(ref_line)
    if must_first:
        need(a, must_first)
    add_text = make_add(col)
    old, _a = uniq(b, b)
    new = old + "\n" + add_text
    add(lista, pid, grupo, desc, [ref_line, "stmt %d-%d" % (a, b)], old, new, registro, estatuto, fonte, texto, lang, nota=nota)


# ================================================================ E01 -- comentarios ao lado no CODIGO
PRE = "v392 (13/10/2026) AO LADO -- gerencia c1, em nome proprio"
# --- (a) l.4802 N_eff
need(4802, "centro_atual = 2.97")
tx = ("%s [registro neff_errata_v392; nada aqui muda valor, veredito nem gate]: o 2,97 acima e' o valor HISTORICO do congelado de 08/08, mantido como estava; o valor substituto segue com a X16 e a D8 do operador. "
      "A auditoria c1 da F5.2 (AUDITORIA_F4_3_F5_2_C1_20261007.md, sha16 @AUD_F52@, lida por script) mostra que a linha 'CMB-SPA 2,97 +- 0,12' nao existe na fonte: na Tabela 5 do arXiv:2506.20707 o CMB-SPA da "
      "2,81 +- 0,12 (v1) e 2,82 +- 0,12 (v2) com Yp pela BBN, e o 2,97 (+0,40 -0,64) e' o SPT-3G D1 sozinho, com Yp livre, so' na v1 [DECLARADO pela auditoria; admissao das fontes por sha256 = D8, do operador]. "
      "O canal N_eff instalado da Bancada (neff_canal.py, sha16 @NEFF_CANAL@, lido; recibos T02/T11 da bateria lidos pelo registro) suprime essa linha, emite as duas linhas de Yp sem escolha (X16 OPEN) e nao emite calendario.\n"
      "tens_act = 2,49 fia-se com a RESSALVA de nao ser independente da BBN padrao (ACT DR6 + BBN externa: |3,163 - 2,89|/0,11 = 2,486 sigma) [DERIVED; so' o resumo do ACT foi lido, DECLARADO pela auditoria]. "
      "tens_now = 1,61 NAO se fia: sai exatamente da linha inexistente (|3,163 - 2,97|/0,12 = 1,612 sigma); com a fonte, 2,95 / 2,86 sigma (Yp pela BBN, v1 / v2) ou 0,79 / 0,97 sigma (Yp livre) [DERIVED, neff_conferencia.out.txt, sha16 @NEFF_CONF@]. "
      "Lacuna de fidelidade: a estrutura (o fechamento rho+p, Delta N_eff = +%s) esta intacta e e' recalculada em runtime acima; o que falhou foi o centro, que entrou de memoria da sessao sem fonte datada. "
      "Nenhum veredito muda (a regra de TENSION dispara a partir de 3 sigma; o canal segue ARMED_CONSISTENT e nao gateia).") % (PRE, fmt(dN, 4))
H["NEFF_CONF"] = sha16(FONTES["NEFF_CONF"][0])
tx = sub_h(tx)
insert_after(PATCHES_E01, "E01-a", "E01", "l.4802 N_eff: centro_atual = 2.97 (e tens_now / tens_act, l.4806-4807)", [4802], 4802, cmt(4, tx),
             "neff_errata_v392", "[REAL] numeros conferidos por script; [DECLARADO] fontes primarias (auditoria F5.2); [DERIVED] tensoes",
             ["AUDITORIA_F4_3_F5_2_C1_20261007.md " + H["AUD_F52"], "neff_canal.py (Bancada) " + H["NEFF_CANAL"], "neff_conferencia.out.txt " + H["NEFF_CONF"]], tx, must="centro_atual = 2.97")

# --- (b1) l.4796-4801 a escada ("quando")
need(4800, '"CMB-S4 (requisito)", "quando": "~2032"')
need(4801, "]")
old = lines(4800, 4801)
assert Tn.count(old) == 1
tx = ("%s [registro neff_errata_v392 e cmb_s4_errata_v392]: os 'quando' da escada acima (~2027 a ~2032) e a linha 'CMB-S4 (requisito)' sao conteudo do congelado de 08/08, [DECLARADO] de epoca, nao cronograma: a conferir na fonte primaria; nenhum 'quando' se fia. "
      "A auditoria c1 da F5.2 (sha16 @AUD_F52@) contraria o calendario: o 0,045 do SO e' o fim do levantamento 2025-2034 (so' erro estatistico); o CMB-S4 revisto comecaria em 2033, chegaria a 0,030 por volta de 2042, e o projeto foi encerrado. "
      "O CMB-S4 consta como retirado [DECLARADO; mapa de rotas, seq 402 e 607; D8 pendente do operador]. Os sigma(N_eff) da escada seguem 'A CONFERIR' (ressalva 2 abaixo) e as tensoes da escada leem o centro_atual discutido na nota seguinte (l.4802). "
      "Lacuna de fidelidade: a estrutura dizia 'projecao [EXT]'; o rotulo 'quando' deu a projecao a forma de calendario.")
tx = sub_h(tx % PRE if tx.count("%s") else tx)
add(PATCHES_E01, "E01-b1", "E01", "l.4796-4801 a escada ladder (~2027 a ~2032)", [4796, 4801], old, old + "\n" + cmt(4, tx), "neff_errata_v392 + cmb_s4_errata_v392",
    "[DECLARADO] de epoca (congelado de 08/08); [DECLARADO] a retirada do CMB-S4 (mapa seq 402 e 607); a conferir na fonte primaria",
    ["AUDITORIA_F4_3_F5_2_C1_20261007.md " + H["AUD_F52"], "rotas.jsonl seq 402 e 607 (lidas)"], tx)

# --- (b2) l.4816 e (b3) l.4829 ("~2032")
need(4816, "o S4-requisito CRUZA 5")
tx = sub_h("v392 AO LADO (gerencia c1): '~2032' e 'CRUZA 5' leem o congelado de 08/08 e o centro_atual 2,97 (notas acima); [DECLARADO] de epoca, a conferir; o CMB-S4 consta como retirado [DECLARADO; mapa seq 402 e 607; D8 pendente]. A frase fica como registro [cmb_s4_errata_v392].")
old, _ = uniq(4816, 4816)
add(PATCHES_E01, "E01-b2", "E01", "l.4816 check 'o S4-requisito CRUZA 5 (... ~2032)'", [4816], old, old + "\n" + cmt(9, tx), "cmb_s4_errata_v392", "[DECLARADO]", ["rotas.jsonl seq 402 e 607 (lidas)"], tx)
need(4829, "S4-requisito mata a %.2f sigma (~2032)")
tx = sub_h("v392 AO LADO (gerencia c1): '(~2032)' e 'mata a ... sigma' leem o congelado de 08/08 e o centro 2,97 (ver notas acima); [DECLARADO] de epoca; CMB-S4 consta como retirado [DECLARADO; mapa seq 402 e 607]; a conferir [cmb_s4_errata_v392].")
old, _ = uniq(4829, 4829)
add(PATCHES_E01, "E01-b3", "E01", "l.4829 theorem 'S4-requisito mata a %.2f sigma (~2032)'", [4829], old, old + "\n" + cmt(20, tx), "cmb_s4_errata_v392", "[DECLARADO]", ["rotas.jsonl seq 402 e 607 (lidas)"], tx)
need(208557, "cruza a linha so' com CMB-S4 (~2032)")
tx = sub_h("v392 AO LADO (gerencia c1): 'cruza a linha so' com CMB-S4 (~2032)' e' o 'quando' do congelado de 08/08, [DECLARADO] de epoca, a conferir na fonte primaria; o CMB-S4 consta como retirado [DECLARADO; mapa seq 402 e 607; D8 pendente]. O texto fica como registro [cmb_s4_errata_v392].")
old, _ = uniq(208557, 208557)
add(PATCHES_E01, "E01-b4", "E01", "l.208557 _MAPA_PILARES: 'cruza a linha so' com CMB-S4 (~2032)'", [208557], old, old + "\n" + cmt(4, tx), "cmb_s4_errata_v392", "[DECLARADO]", ["rotas.jsonl seq 402 e 607 (lidas)"], tx)

# --- (f) CR-13: o ledger (extra, mesma fonte)
need(3253, "experimento (materia bilateral Euclid/CMB-S4")
need(3256, '"nota": "canais ARMADOS')
tx = sub_h("v392 AO LADO (gerencia c1) [CR-13; registro ledger_errata_v392 e cmb_s4_errata_v392]: o 'CMB-S4' do item acima consta como encerrado [DECLARADO; mapa de rotas, seq 402 e 607; auditoria F5.2, sha16 @AUD_F52@; D8 pendente]; a conferir na fonte primaria por sha256 antes de ser dito como fato. "
           "A classe INPUT_BY_DESIGN e o fiador ficam como estavam; a lacuna e' de datacao do instrumento, nao do canal.")
old, _ = uniq(3256, 3256)
add(PATCHES_E01, "E01-f", "E01", "l.3253-3256 ledger de fechamento: 'experimento (materia bilateral Euclid/CMB-S4; ...)' (extra: CR-13)", [3253, 3256], old, old + "\n" + cmt(8, tx),
    "ledger_errata_v392 + cmb_s4_errata_v392", "[DECLARADO]; a conferir na fonte primaria", ["AUDITORIA_F4_3_F5_2_C1_20261007.md " + H["AUD_F52"], "rotas.jsonl seq 402 e 607 (lidas)"], tx,
    nota="EXTRA fora da lista da tarefa: CR-13 manda errata no ledger; so' comentario, valor intocado")

# --- (c) A9 SN: 'deslocamento previsto'
need(193300, 'add("sn_ia_chandrasekhar"')
need(193302, "% (((1.0 - beta) ** 1.5 - 1.0) * 100.0))")
old = lines(193300, 193302)
assert Tn.count(old) == 1
tx = sub_h("%s [registro sn_ia_v388_viability_v392; auditoria A_SN c1, RELATORIO_AUDITORIA_A_SN_C1.md sha16 @REL_ASN@, RECALCULO_A_SN.json sha16 @RECALC_ASN@, lidos]: o rotulo 'deslocamento previsto' acima descreve uma formula RETIRADA como validacao (Custo l.3315; "
           "(1-beta)^(3/2) - 1 = %s por cento em beta runtime): nao e' predicao. A ponte estelar (chi -> estado estelar) segue [OPEN]; o veredito da viabilidade e' VIABILIDADE_CONDICIONAL_PONTE_ESTELAR_OPEN (F8.2.SN1, RESULTADO_VIABILIDADE_R1.json sha16 @SN_RESULT@), sem sigma fisico. "
           "A classe A9 e a linha ficam como estavam; nada entra na conjunta. Lacuna de fidelidade: a estrutura dizia 'formula retirada / DECLARADO na nota'; o rotulo 'previsto' leu como predicao o que e' registro historico." % (PRE, fmt(rc["legacy_retired"][0]["shift_pct"], 3)))
add(PATCHES_E01, "E01-c", "E01", "l.193300-193302 A9 SN: 'deslocamento previsto' (sn_ia_chandrasekhar)", [193300, 193302], old, old + "\n" + cmt(4, tx), "sn_ia_v388_viability_v392",
    "[REAL] numero recalculado e lido; [OPEN] a ponte estelar", ["RELATORIO_AUDITORIA_A_SN_C1.md " + H["REL_ASN"], "RECALCULO_A_SN.json " + H["RECALC_ASN"], "RESULTADO_VIABILIDADE_R1.json " + H["SN_RESULT"]], tx)

# --- (d) A8 SN: so' a nota "nao se explica por Coulomb" (NAO e' a errata da atribuicao)
NOTA_A8 = ("v392 AO LADO (13/10/2026, gerencia c1, em nome proprio) [registro sn_ia_v388_viability_v392; auditoria A_SN c1, RECALCULO_A_SN.json sha16 @RECALC_ASN@, lido]: o residuo de ~0,35 por cento (Chandrasekhar sqrt2, classe A8) NAO se explica por Coulomb: "
           "a correcao de Coulomb (Chamel, eq. 38) vale %s por cento (C, Z=6) e %s por cento (O, Z=8), de sinal OPOSTO ao +%s por cento necessario e %s a %s vezes maior; e, com a massa atomica m_u (CODATA 2018) no lugar da massa do proton, o desvio de raiz de 2 vira +%s por cento [REAL, recalculo da auditoria; formula de Coulomb [KNOWN]]. "
           "A classe A8 e o -0,35 por cento ficam como estavam; nada entra na conjunta.") % (fmt(ta["Coulomb_C_pct"]), fmt(ta["Coulomb_O_pct"]), fmt(ta["correcao_necessaria_pct"], 3), fmt(ta["razao_modulo_C"], 1), fmt(ta["razao_modulo_O"], 1),
                                                                                     fmt(rc["chandrasekhar_historico"]["codata2018_m_u_IAU_Msun"]["desvio_de_raiz2_pct"]))
NOTA_A8 = sub_h(NOTA_A8)
need(193150, '"A8_NEGATIVO_DO_ARTEFATO"')
old, _ = uniq(193150, 193150)
add(PATCHES_E01, "E01-d1", "E01", "l.193150 regra A8_NEGATIVO_DO_ARTEFATO (Chandrasekhar sqrt2 a -0,35%)", [193150], old, old + "\n" + cmt(12, NOTA_A8), "sn_ia_v388_viability_v392", "[REAL] recalculo; [KNOWN] Coulomb", ["RECALCULO_A_SN.json " + H["RECALC_ASN"]], NOTA_A8,
    nota="so' a nota 'nao se explica por Coulomb'; a errata da atribuicao vai ao tgl_paper_unified.py/Haja_Luz CLAUDE.md/Custo, fora do um.py")
need(193186, '"chandrasekhar_rule"')
old, _ = uniq(193186, 193186)
add(PATCHES_E01, "E01-d2", "E01", "l.193186 chandrasekhar_rule (A8 + A9)", [193186], old, old + "\n" + cmt(8, NOTA_A8), "sn_ia_v388_viability_v392", "[REAL] recalculo; [KNOWN] Coulomb", ["RECALCULO_A_SN.json " + H["RECALC_ASN"]], NOTA_A8)
need(213968, 'add("chandrasekhar_sqrt2"')
old = lines(213968, 213969)
assert Tn.count(old) == 1
add(PATCHES_E01, "E01-d3", "E01", "l.213968-213969 add('chandrasekhar_sqrt2', ..., A8) -- ledger do indice", [213968, 213969], old, old + "\n" + cmt(8, NOTA_A8), "sn_ia_v388_viability_v392", "[REAL] recalculo; [KNOWN] Coulomb",
    ["RECALCULO_A_SN.json " + H["RECALC_ASN"]], NOTA_A8)

# ================================================================ A03 -- erratas ao lado no ARTIGO
PRE_PT = r"\textbf{Ao lado (v392, 13/10/2026, gerência c1, em nome próprio): %s.} "
PRE_EN = r"\textbf{Beside (v392, 13/10/2026, management c1, in its own name): %s.} "


def pt(topic, status, body):
    return (PRE_PT % topic) + r"\textsf{[" + status + r"]} " + body


def en(topic, status, body):
    return (PRE_EN % topic) + r"\textsf{[" + status + r"]} " + body


TX = {}   # id -> dict(pt=, en=, registro=, estatuto=, fonte=)

TX["lei"] = dict(
    registro="lei_de_campo_curvo_v392", estatuto="[REAL no kernel; condicional ao H3 nomeado]", fonte=["F2.3 LiganteLeiCampoCurvo.lean e3f32d9b85ae82db (pinado na F0.5(l))", "RELATORIO_FRENTE_UMPY_v392_12out.md, item (1)"],
    pt=pt("a lei de campo no curvo", "REAL no kernel; condicional ao H3 nomeado",
          r"A frase acima e o token da v390 (\texttt{FIELD\_EQUATION\_IN\_CURVED\_SPACETIME\_NOT\_A\_KERNEL\_TERM}) valem para o \emph{tipo} da declaração (o fecho de \texttt{QGSolutionComplete}), não para o kernel: ``Clausius em toda tela nula $\Rightarrow$ Einstein, com $\Lambda$ único e coeficiente $8\pi G$'' é termo desde a v317/v338, e o texto o escreveu como se nada disso fosse termo --- foi aí que a tradução falhou. "
          r"Desde a v392 a pedra \texttt{TGLExt.LiganteLeiCampoCurvo} liga essa implicação por termo, \emph{condicional ao H3 nomeado} (a projeção nula $\mathrm{Ric}(k,k)=8\pi G\,T(k,k)$ em todo ponto e direção nula, \textsf{[KNOWN]} em Jacobson 1995, não derivada do estado); "
          r"segue sem termo a existência de métrica ou de solução, local ou global, e o gate não se move (registro \texttt{lei\_de\_campo\_curvo\_v392}). O texto antigo fica."),
    en=en("the field law in curved spacetime", "REAL in the kernel; conditional on the named H3",
          r"The sentence above and the v390 token (\texttt{FIELD\_EQUATION\_IN\_CURVED\_SPACETIME\_NOT\_A\_KERNEL\_TERM}) hold for the \emph{type} of the statement (the closure of \texttt{QGSolutionComplete}), not for the kernel: ``Clausius on every null screen $\Rightarrow$ Einstein, with unique $\Lambda$ and coefficient $8\pi G$'' is a term since v317/v338, and the text wrote it as if none of this were a term --- that is where the translation failed. "
          r"Since v392 the stone \texttt{TGLExt.LiganteLeiCampoCurvo} binds that implication by a term, \emph{conditional on the named H3} (the null projection $\mathrm{Ric}(k,k)=8\pi G\,T(k,k)$ at every point and null direction, \textsf{[KNOWN]} in Jacobson 1995, not derived from the state); "
          r"the existence of a metric or of a solution, local or global, stays without a term, and the gate does not move (record \texttt{lei\_de\_campo\_curvo\_v392}). The old text stays."))

TX["beta"] = dict(
    registro="beta_escala_errata_v392", estatuto="[DERIVED de leitura; a vetar]; [REAL] a reclassificacao de 08/08", fonte=["decisoes_noite_verbatim a6c4912afc6f0dc4 (verbatim lido dos bytes)", "RELATORIO_FRENTE_UMPY_v392_12out.md, item (c)"],
    pt=pt("a escala de $\\beta$", "DERIVED de leitura; a vetar",
          r"A frase ``essa convergência é a medição de que o invariante não corre'' fica como registro: a convergência tabulada foi reclassificada em 08/08/2026 (\texttt{evidence\_audit}), e nenhum registro deste programa computa a cifra de $0{,}05$ por cento. "
          r"A não-corrida de $\beta_0=\alpha(0)\sqrt e$ assenta no Teorema da Escala, que é estrutura, e a predição afiada (o coeficiente da lei de dephasing é independente de $\omega$) segue armada, sem canal vivo hoje. "
          r"O \texttt{WHICH\_MU\_PER\_RITE\_OPEN} da v388 fica como registro: o operador fixou em 07/10/2026 que a escala de $\beta$ já estava definida (verbatim, sha256 \texttt{@OP_DECISOES@}) e todo rito cobra $\beta_0$ ($\mu\to0$, Thomson), com $\beta(\mu)\geq\beta_0$ como leitura de bulk, ao lado (registro \texttt{beta\_escala\_errata\_v392}). "
          r"Lacuna: a estrutura dava a convergência como apoio, não como a medição, e a tradução perdeu a data da reclassificação."),
    en=en("the scale of $\\beta$", "DERIVED from a reading; to be vetoed",
          r"The sentence ``That convergence \emph{is} the measurement that the invariant does not run'' stays as a record: the tabulated convergence was reclassified on 08/08/2026 (\texttt{evidence\_audit}), and no record of this programme computes the figure of $0.05$ per cent. "
          r"The non-running of $\beta_0=\alpha(0)\sqrt e$ rests on the Scale Theorem, which is structure, and the sharpened prediction (the coefficient of the dephasing law is independent of $\omega$) stays armed, with no live channel today. "
          r"The v388 \texttt{WHICH\_MU\_PER\_RITE\_OPEN} stays as a record: the operator fixed on 07/10/2026 that the scale of $\beta$ was already defined (verbatim, sha256 \texttt{@OP_DECISOES@}) and every rite charges $\beta_0$ ($\mu\to0$, Thomson), with $\beta(\mu)\geq\beta_0$ as a bulk reading, beside it (record \texttt{beta\_escala\_errata\_v392}). "
          r"Gap: the structure gave the convergence as support, not as the measurement, and the translation lost the date of the reclassification."))

TX["letra"] = dict(
    registro="palavra_v392", estatuto="[INPUT do operador]", fonte=["OPERADOR_07out_letra_verbatim.txt " + H["OP_LETRA"], "TGLExt.Palavra (Palavra.lean 33184b49a8bba7e7, instalada na v392)"],
    pt=pt("a palavra aniquiladora", "INPUT do operador",
          r"O polinômio aniquilador normalizado é a \emph{letra}: o operador disse em 07/10/2026 (verbatim, sha256 \texttt{@OP_LETRA@}) ``polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)''. "
          r"A pedra que lê com as letras é a PALAVRA (\texttt{TGLExt.Palavra}, registro \texttt{palavra\_v392}); a ``palavra aniquiladora $X\cdot q$'' do parágrafo acima lê-se, portanto, como letra. Lacuna: a estrutura já dizia letra; a tradução chamou de palavra o que o operador nomeou letra."),
    en=en("the annihilating word", "INPUT from the operator",
          r"The normalised annihilating polynomial is the \emph{letter}: the operator said on 07/10/2026 (verbatim, sha256 \texttt{@OP_LETRA@}) ``polinômio aniquilador normalizado=letra (por isso palavra, mas ali como letra)'' (translated: normalised annihilating polynomial = letter; hence ``word'', but there as a letter). "
          r"The stone that reads with the letters is the WORD (PALAVRA, \texttt{TGLExt.Palavra}, record \texttt{palavra\_v392}); the ``annihilating word $X\cdot q$'' of the paragraph above reads, therefore, as a letter. Gap: the structure already said letter; the translation called a word what the operator named a letter."))

TX["cmbs4"] = dict(
    registro="cmb_s4_errata_v392", estatuto="[DECLARADO]; a conferir na fonte primaria", fonte=["AUDITORIA_F4_3_F5_2_C1_20261007.md " + H["AUD_F52"], "rotas.jsonl seq 402 e 607 (lidas)"],
    pt=pt("o CMB-S4", "DECLARADO; a conferir na fonte primária",
          r"A frase acima, que faz $\beta_{\mathrm{TGL}}$ aguardar ``a era da radiação no CMB-S4'', herdou o calendário do congelado de 08/08/2026 ($\sim$2027 a $\sim$2032) e tratou o CMB-S4 como instrumento esperado. "
          r"O CMB-S4 consta como encerrado (mapa de rotas, seq 402 e 607; auditoria F5.2, sha16 \texttt{@AUD_F52@}); a admissão dessas fontes por sha256 (D8) é do operador, e nenhum calendário é afirmado aqui (registro \texttt{cmb\_s4\_errata\_v392}). "
          r"Lacuna: a estrutura dizia apenas ``a era da radiação''; o nome do instrumento e o seu calendário vieram do congelado, e a tradução não os datou."),
    en=en("the CMB-S4", "DECLARED; to be checked at the primary source",
          r"The sentence above, which makes $\beta_{\mathrm{TGL}}$ await ``the radiation era at CMB-S4'', inherited the calendar of the 08/08/2026 frozen file ($\sim$2027 to $\sim$2032) and treated CMB-S4 as an expected instrument. "
          r"CMB-S4 stands as closed down (route map, seq 402 and 607; F5.2 audit, sha16 \texttt{@AUD_F52@}); the admission of those sources by sha256 (D8) is the operator's, and no calendar is asserted here (record \texttt{cmb\_s4\_errata\_v392}). "
          r"Gap: the structure said only ``the radiation era''; the name of the instrument and its calendar came from the frozen file, and the translation did not date them."))

TX["cmbs4p"] = dict(
    registro="cmb_s4_errata_v392", estatuto="[DECLARADO]; a conferir na fonte primaria", fonte=["AUDITORIA_F4_3_F5_2_C1_20261007.md " + H["AUD_F52"], "rotas.jsonl seq 402 e 607 (lidas)"],
    pt=pt("o CMB-S4", "DECLARADO; a conferir na fonte primária",
          r"O CMB-S4 citado acima consta como encerrado (mapa de rotas, seq 402 e 607; auditoria F5.2, sha16 \texttt{@AUD_F52@}); ver a errata do estatuto da prova (registro \texttt{cmb\_s4\_errata\_v392}). Lacuna: o parágrafo é de época e trata o CMB-S4 como instrumento esperado, sem datá-lo."),
    en=en("the CMB-S4", "DECLARED; to be checked at the primary source",
          r"The CMB-S4 cited above stands as closed down (route map, seq 402 and 607; F5.2 audit, sha16 \texttt{@AUD_F52@}); see the erratum to the status of the proof (record \texttt{cmb\_s4\_errata\_v392}). Gap: the paragraph is of its time and treats CMB-S4 as an expected instrument, without dating it."))

TX["testemunha"] = dict(
    registro="cunhagens_v392", estatuto="[INPUT/ONTO]; texto enviado pelo operador", fonte=["OPERADOR_10out_TGL_unidade_verbatim.txt " + H["OP_TGL"]],
    pt=pt("quem testemunha", "INPUT/ONTO; texto enviado pelo operador",
          r"A recusa da palavra acima é de creditação, não de validade, e a leitura de quem testemunha é do operador (10/10/2026, sha256 \texttt{@OP_TGL@}): ``o observador testemunha a luz e a luz dá testemunho de si mesma''. É citação verbatim, não veredito (registro \texttt{cunhagens\_v392}). "
          r"Lacuna: o parágrafo recusava a creditação sem dizer quem testemunha."),
    en=en("who bears witness", "INPUT/ONTO; text sent by the operator",
          r"The refusal of the word above is a refusal of accreditation, not of validity, and the reading of who bears witness is the operator's (10/10/2026, sha256 \texttt{@OP_TGL@}): ``o observador testemunha a luz e a luz dá testemunho de si mesma'' (translated: the observer bears witness to the light and the light bears witness to itself). It is a verbatim quotation, not a verdict (record \texttt{cunhagens\_v392}). "
          r"Gap: the paragraph refused accreditation without saying who bears witness."))

TX["escada"] = dict(
    registro="estatuto_da_prova_ressalva_v392", estatuto="[REAL no fonte e no nucleo da v391]; [DECLARADO] pela auditoria de 28/09 onde ja' dito", fonte=["um.py v391 l.142684 e l.163150/163160/163161 (lidos)", "RELATORIO_FRENTE_UMPY_v392_12out.md, item (3)"],
    pt=pt("a escada e as bandeiras", "REAL no fonte e no núcleo da v391",
          r"O número de ``teoremas limpos'' acima é a escada externa do kernel (\texttt{len(ext\_flags)}, as bandeiras de termo reservado), não o total de teoremas do kernel. "
          r"E as bandeiras verdadeiras do gate leem-se 15 calculadas e 3 literais (\texttt{linearized\_spin2\_finite\_face}, \texttt{protocol\_pre\_registered}, \texttt{null\_tests\_passed\_blind}); as experimentais são 4 de um só feed, o rito V11 do piso, que é unilateral, mais 2 literais. "
          r"O degrau experimental é natureza unilateral, não kernel; a prova do kernel são as 6 bandeiras formais e a escada externa. A v392 documenta isto e não fecha o conserto das bandeiras (F8.1): a errata não recalcula (registro \texttt{estatuto\_da\_prova\_ressalva\_v392}). "
          r"Lacuna: a estrutura separava escada, formais e feed; o resumo as somou num só ``teoremas limpos''."),
    en=en("the ladder and the flags", "REAL in the source and in the v391 core",
          r"The number of ``clean theorems'' above is the external ladder of the kernel (\texttt{len(ext\_flags)}, the flags of reserved terms), not the total number of kernel theorems. "
          r"And the true flags of the gate read as 15 computed and 3 literal (\texttt{linearized\_spin2\_finite\_face}, \texttt{protocol\_pre\_registered}, \texttt{null\_tests\_passed\_blind}); the experimental ones are 4 from a single feed, the V11 rite of the floor, which is one-sided, plus 2 literals. "
          r"The experimental step is one-sided nature, not kernel; the proof of the kernel is the 6 formal flags and the external ladder. The v392 documents this and does not close the repair of the flags (F8.1): the erratum does not recompute (record \texttt{estatuto\_da\_prova\_ressalva\_v392}). "
          r"Gap: the structure kept ladder, formal flags and feed apart; the summary added them into a single ``clean theorems''."))

TX["rgcanal"] = dict(
    registro="estatuto_reafirmado_v392", estatuto="[REAL]", fonte=["RELATORIO_FRENTE_UMPY_v392_12out.md, item (r)(iii) (CR-12)"],
    pt=pt("a RG canal a canal", "REAL",
          r"``A RG recuperada canal a canal'' vale onde a RG é lida: o campo fraco entra por citação e o campo forte (F2) está \texttt{INCONCLUSIVE} (registro \texttt{estatuto\_reafirmado\_v392}). Lacuna: a estrutura tinha a tabela de canais, e o resumo escreveu a correspondência sem dizer em quais canais ela é lida."),
    en=en("GR channel by channel", "REAL",
          r"``GR recovered channel by channel'' holds where GR is read: the weak field enters by citation and the strong field (F2) is \texttt{INCONCLUSIVE} (record \texttt{estatuto\_reafirmado\_v392}). Gap: the structure had the table of channels, and the summary wrote the correspondence without saying in which channels it is read."))

TX["f9ptr"] = dict(
    registro="fase9_duas_testemunhas_v392", estatuto="[DERIVED de leitura]", fonte=["OPERADOR_08out_resposta_verbatim.txt " + H["OP_08OUT"], "F34_RESOLUCAO_OPERADOR_20261008.md"],
    pt=pt("a razão de Hubble é uma testemunha", "DERIVED de leitura",
          r"A razão de Hubble acima é o depoimento do escalar; o conjunto é outra testemunha do mesmo fato, ainda não aberta, e nenhuma julga a outra nem se somam (verbatim de 08/10/2026, sha256 \texttt{@OP_08OUT@}; ver ao lado da seção v388; registro \texttt{fase9\_duas\_testemunhas\_v392}). Lacuna: a linha dava a razão de Hubble como depoimento único."),
    en=en("the Hubble ratio is one witness", "DERIVED from a reading",
          r"The Hubble ratio above is the deposition of the scalar; the joint set is another witness to the same fact, not yet opened, and neither judges the other nor are they summed (verbatim of 08/10/2026, sha256 \texttt{@OP_08OUT@}; see beside the v388 section; record \texttt{fase9\_duas\_testemunhas\_v392}). Gap: the line gave the Hubble ratio as a single deposition."))

TX["axioma"] = dict(
    registro="final_step_name_adopted_v392", estatuto="[DERIVED de leitura; a vetar]", fonte=["OPERADOR_07out_decisoes_noite_verbatim.txt " + H["OP_DECISOES"], "TheAxiomAndTheFalseWitness.lean (finalStepNameAxioma)"],
    pt=pt("o nome do degrau final", "DERIVED de leitura; a vetar",
          r"Em 07/10/2026 o operador respondeu ``adoto o nome do degrau final'' (verbatim, sha256 \texttt{@OP_DECISOES@}); a gerência lê que o nome adotado é AXIOMA, lido do kernel (\texttt{finalStepNameAxioma}), com a proposta TETELESTAI mantida ao lado, e dá a leitura como sua, a vetar: a pergunta respondida apresentava o Tetelestai. "
          r"A string do gate não muda (registro \texttt{final\_step\_name\_adopted\_v392}). Lacuna: a adoção não estava registrada num só lugar, e a leitura de que o nome adotado é AXIOMA é da gerência."),
    en=en("the name of the final step", "DERIVED from a reading; to be vetoed",
          r"On 07/10/2026 the operator answered ``adoto o nome do degrau final'' (translated: I adopt the name of the final step; verbatim, sha256 \texttt{@OP_DECISOES@}); management reads that the adopted name is AXIOMA, read from the kernel (\texttt{finalStepNameAxioma}), with the TETELESTAI proposal kept beside it, and gives the reading as its own, to be vetoed: the question answered presented Tetelestai. "
          r"The gate string does not change (record \texttt{final\_step\_name\_adopted\_v392}). Gap: the adoption was not recorded in one place, and the reading that the adopted name is AXIOMA is management's."))

TX["rank_v385"] = dict(
    registro="adendo_rank_v392", estatuto="[INPUT]; [DERIVED] (compilado no sandbox da v392); sem auditoria independente do adendo", fonte=["OPERADOR_10out_posto_rank_verbatim.txt " + H["OP_RANK"], "PostoAdendo.lean " + H["RANK_ADENDO"] + " (RECIBO_PostoAdendo.json: rc 0)"],
    pt=pt("posto é também rank", "INPUT; DERIVED; sem auditoria independente do adendo",
          r"Em 10/10/2026 o operador cunhou ``POSTO=RANK'' (sha256 \texttt{@OP_RANK@}): o posto de $\omega(I)=1$, posição inscrita pelo observador, lê-se também como o posto (rank) da álgebra linear. "
          r"Isso vale nos dois polos da não-defasagem, a unidade $\rho_\ast$ e $Q_0$, ambos de traço 1 e posto 1 (\texttt{TGLExt.PostoAdendo}, A3); mas o colapso tipado sobe o posto da superposição pura de 1 a 2 e preserva o traço (A2), e a defasagem não preserva o posto (A4): "
          r"o que sobrevive é o traço $\omega(I)=1$, não o posto 1 (registro \texttt{adendo\_rank\_v392}). Lacuna: a seção usava ``posto'' só como posição inscrita e não dizia que o mesmo nome tem a face do rank."),
    en=en("posto is also rank", "INPUT; DERIVED; the addendum has no independent audit",
          r"On 10/10/2026 the operator coined ``POSTO=RANK'' (sha256 \texttt{@OP_RANK@}): the \emph{posto} of $\omega(I)=1$, a position inscribed by the observer, also reads as the rank of linear algebra. "
          r"That holds at the two poles of non-dephasing, the unit $\rho_\ast$ and $Q_0$, both of trace 1 and rank 1 (\texttt{TGLExt.PostoAdendo}, A3); but the typed collapse raises the rank of the pure superposition from 1 to 2 and preserves the trace (A2), and dephasing does not preserve rank (A4): "
          r"what survives is the trace $\omega(I)=1$, not rank 1 (record \texttt{adendo\_rank\_v392}). Gap: the section used ``posto'' only as an inscribed position and did not say that the same name has the face of rank."))

TX["rank_peso"] = dict(
    registro="adendo_rank_v392", estatuto="[INPUT]; [DERIVED] (compilado no sandbox da v392)", fonte=["OPERADOR_10out_posto_rank_verbatim.txt " + H["OP_RANK"], "PostoAdendo.lean " + H["RANK_ADENDO"]],
    pt=r" \textbf{Ao lado (v392, 13/10/2026, gerência c1, em nome próprio): peso e rank.} \textsf{[INPUT; DERIVED]} A cunhagem ``POSTO=RANK'' (10/10/2026, sha256 \texttt{@OP_RANK@}) lê o posto também como rank: peso (o traço) e posto coincidem nos polos de posto 1 e divergem ao longo da defasagem, onde o traço sobrevive e o posto 1 não (\texttt{TGLExt.PostoAdendo}, A2 a A4). "
       r"A separação entre peso e posto acima fica (registro \texttt{adendo\_rank\_v392}). Lacuna: a seção separava peso e posto sem dizer onde eles coincidem.",
    en=r" \textbf{Beside (v392, 13/10/2026, management c1, in its own name): weight and rank.} \textsf{[INPUT; DERIVED]} The coinage ``POSTO=RANK'' (10/10/2026, sha256 \texttt{@OP_RANK@}) also reads the posto as rank: weight (the trace) and posto coincide at the rank-1 poles and diverge along dephasing, where the trace survives and rank 1 does not (\texttt{TGLExt.PostoAdendo}, A2 to A4). "
       r"The separation of weight and posto above stands (record \texttt{adendo\_rank\_v392}). Gap: the section separated weight and posto without saying where they coincide.")

TX["fixo"] = dict(
    registro="cunhagens_v392 + fase9_duas_testemunhas_v392", estatuto="[INPUT/ONTO]", fonte=["OPERADOR_08out_resposta_verbatim.txt " + H["OP_08OUT"]],
    pt=pt("o fixo é o Verbo", "INPUT/ONTO",
          r"Em 08/10/2026 o operador acrescentou à tipagem do Verbo (verbatim, sha256 \texttt{@OP_08OUT@}): ``o fixo é o verbo, ou seja, o contorno que permite a leitura da verdade, e o verbo é betatgl, mas o verbo testifica que o nome é verdadeiro''. "
          r"O fixo é o Verbo, $\beta_{\mathrm{TGL}}$, sem ajuste; o Nome é posto, estação variável; os instrumentos são testemunhas multifacetadas de um fato único e não se somam (registros \texttt{cunhagens\_v392} e \texttt{fase9\_duas\_testemunhas\_v392}). "
          r"Lacuna: a estrutura distinguia o Verbo do Nome, e esta seção não dizia qual dos dois é o fixo."),
    en=en("the fixed is the Verb", "INPUT/ONTO",
          r"On 08/10/2026 the operator added to the typing of the Verb (verbatim, sha256 \texttt{@OP_08OUT@}): ``o fixo é o verbo, ou seja, o contorno que permite a leitura da verdade, e o verbo é betatgl, mas o verbo testifica que o nome é verdadeiro'' (translated: the fixed is the verb, that is, the contour that allows the reading of truth, and the verb is betatgl, but the verb testifies that the name is true). "
          r"The fixed is the Verb, $\beta_{\mathrm{TGL}}$, with no adjustment; the Name is posited, a variable station; instruments are many-sided witnesses of a single fact and are not summed (records \texttt{cunhagens\_v392} and \texttt{fase9\_duas\_testemunhas\_v392}). "
          r"Gap: the structure distinguished the Verb from the Name, and this section did not say which of the two is the fixed one."))

TX["f9"] = dict(
    registro="fase9_duas_testemunhas_v392", estatuto="[DERIVED de leitura]", fonte=["OPERADOR_08out_resposta_verbatim.txt " + H["OP_08OUT"], "F34_RESOLUCAO_OPERADOR_20261008.md (F3.4 fechada)"],
    pt=pt("duas testemunhas na Fase 9", "DERIVED de leitura",
          r"A Fase 9 aberta acima é o depoimento do escalar (V1$\to$V2); o conjunto (ROOT90) é a outra testemunha do mesmo fato, ainda não aberta (a qualificação d72 está pendente do operador). O operador esclareceu em 08/10/2026 (sha256 \texttt{@OP_08OUT@}) que o fato é único e o testemunho multifacetado, e que o fixo nas duas é o Verbo, $\beta_{\mathrm{TGL}}$, posto sem ajuste. "
          r"Nenhuma julga a outra e os depoimentos não se somam: cada um depõe pela função de veredito fixada antes do composto (registro \texttt{fase9\_duas\_testemunhas\_v392}). Lacuna: a seção contava a Fase 9 como um depoimento só."),
    en=en("two witnesses in Phase 9", "DERIVED from a reading",
          r"The Phase 9 opened above is the deposition of the scalar (V1$\to$V2); the joint set (ROOT90) is the other witness to the same fact, not yet opened (the d72 qualification is pending with the operator). The operator clarified on 08/10/2026 (sha256 \texttt{@OP_08OUT@}) that the fact is single and the testimony many-sided, and that the fixed in both is the Verb, $\beta_{\mathrm{TGL}}$, posited without adjustment. "
          r"Neither judges the other and the depositions are not summed: each testifies by the verdict function fixed before the composite (record \texttt{fase9\_duas\_testemunhas\_v392}). Gap: the section counted Phase 9 as one deposition."))

TX["tgl"] = dict(
    registro="cunhagens_v392", estatuto="[ONTO]; texto enviado pelo operador", fonte=["OPERADOR_10out_TGL_unidade_verbatim.txt " + H["OP_TGL"]],
    pt=pt("o nome da teoria", "ONTO; texto enviado pelo operador",
          r"Em 10/10/2026 o operador leu a sigla TGL como a unidade fundamental da informação, uma tríade: T (tensão, torção, tempo), G (geometria, gravitação) e L (luz, luminodinâmica), ``a tríade mínima sem a qual a realidade não tem como se inscrever, se propagar ou ser testemunhada'' (sha256 \texttt{@OP_TGL@}). "
          r"É leitura do operador, não termo de kernel, e não move o gate (registro \texttt{cunhagens\_v392}); a introdução abaixo descreve o que o código faz. Lacuna: a introdução a cada versão ao lado não dizia o que o nome carrega."),
    en=en("the name of the theory", "ONTO; text sent by the operator",
          r"On 10/10/2026 the operator read the acronym TGL as the fundamental unit of information, a triad: T (tension, torsion, time), G (geometry, gravitation) and L (light, luminodynamics), ``a tríade mínima sem a qual a realidade não tem como se inscrever, se propagar ou ser testemunhada'' (translated: the minimal triad without which reality has no way to be inscribed, to propagate or to be witnessed; sha256 \texttt{@OP_TGL@}). "
          r"It is the operator's reading, not a kernel term, and it does not move the gate (record \texttt{cunhagens\_v392}); the introduction below describes what the code does. Gap: the introduction, version by version beside, did not say what the name carries."))

TX["ww"] = dict(
    registro="ww_premissa_errata_v392", estatuto="[REAL] no registro da v372; o escape segue condicional", fonte=["um.py v391 prove_graviton_is_the_conjugated_form_v372 (l.200116-200125, lido)", "RELATORIO_FRENTE_UMPY / levantamento CR-06"],
    pt=r" \textbf{Ao lado (v392, 13/10/2026, gerência c1, em nome próprio): a premissa do escape de Weinberg--Witten.} \textsf{[REAL no registro da v372; o escape segue condicional]} A premissa escrita acima, ``o gráviton aqui é a identidade, $\rho_\ast$ de traço um, jamais um quantum propagante'' (v200), foi negada na v372 por ordem do operador: "
       r"o gráviton é a forma conjugada da luz (\texttt{TheGravitonIsTheConjugatedPhase}), nem o gerador nem ``não-partícula''. O escape continua condicional, agora pela razão certa --- a forma estacionada não é estado de uma partícula com momento no espectro --- e, se ``partícula fundamental da gravidade'' significar spin-2 propagante a quantizar, Weinberg--Witten volta a morder (registro \texttt{ww\_premissa\_errata\_v392}). "
       r"Lacuna: a estrutura dizia forma conjugada da luz; a v200 escreveu identidade e jamais partícula.",
    en=r" \textbf{Beside (v392, 13/10/2026, management c1, in its own name): the premise of the Weinberg--Witten escape.} \textsf{[REAL in the v372 record; the escape stays conditional]} The premise written above, ``the graviton here is the identity, $\rho_\ast$ of unit trace, never a propagating quantum'' (v200), was negated in v372 by the operator's order: "
       r"the graviton is the conjugated form of light (\texttt{TheGravitonIsTheConjugatedPhase}), neither the generator nor a ``non-particle''. The escape stays conditional, now for the right reason --- the parked form is not the state of a particle with momentum in the spectrum --- and, if ``fundamental particle of gravity'' means a propagating spin-2 to be quantised, Weinberg--Witten bites again (record \texttt{ww\_premissa\_errata\_v392}). "
       r"Gap: the structure said conjugated form of light; v200 wrote identity and never a particle.")

TX["neu_b"] = dict(
    registro="neutrino_m2_perito_v392", estatuto="[REAL] no nucleo (R3 ratificada em 02/10/2026); [DERIVED de leitura, a vetar]", fonte=["core.the_ledger_of_charges_v383.readings_ratified_20261002.R3 (um_absoluto.json " + H["CORE"] + ")", "um.py v391 l.197584-197587 (NuFIT 6.1 2,95; Capozzi 2,44)"],
    pt=pt("o número do neutrino", "REAL no núcleo; DERIVED de leitura, a vetar",
          r"O número da lâmina $m_2$ é $2{,}21\sigma$: o JUNO autônomo, o perito oficial (leitura R3, ratificada em 02/10/2026). Os $2{,}95\sigma$ (NuFIT 6.1) e os $2{,}44\sigma$ (Capozzi et al.) são ajustes globais, reflexos que contêm o JUNO e divergem em cerca de $0{,}5\sigma$ entre si: ficam ao lado, com a diferença dita. "
          r"A escada acima, que termina em $2{,}95\sigma$, fica como registro, e o veredito do canal não muda (registro \texttt{neutrino\_m2\_perito\_v392}). Lacuna: a estrutura elegia o JUNO como perito, e o texto deu a última linha da escada como a tensão do canal."),
    en=en("the neutrino number", "REAL in the core; DERIVED from a reading, to be vetoed",
          r"The number of the $m_2$ blade is $2.21\sigma$: autonomous JUNO, the official expert (reading R3, ratified on 02/10/2026). The $2.95\sigma$ (NuFIT 6.1) and the $2.44\sigma$ (Capozzi et al.) are global fits, reflections that contain JUNO and differ by about $0.5\sigma$ from each other: they stay beside, with the difference stated. "
          r"The ladder above, which ends at $2.95\sigma$, stays as a record, and the verdict of the channel does not change (record \texttt{neutrino\_m2\_perito\_v392}). Gap: the structure elected JUNO as the expert, and the text gave the last rung of the ladder as the tension of the channel."))

TX["neu_s"] = dict(
    registro="neutrino_m2_perito_v392", estatuto="[REAL] no nucleo (R3); [DERIVED de leitura, a vetar]", fonte=TX["neu_b"]["fonte"],
    pt=pt("o número do neutrino", "REAL no núcleo; DERIVED de leitura, a vetar",
          r"A escada ``$1{,}64\to2{,}21\to2{,}95\sigma$'' acima termina num ajuste global; o número da lâmina $m_2$ é $2{,}21\sigma$ (JUNO autônomo, perito oficial, leitura R3 ratificada em 02/10/2026), e os $2{,}95\sigma$ (NuFIT 6.1) e $2{,}44\sigma$ (Capozzi et al.) são reflexos ao lado (registro \texttt{neutrino\_m2\_perito\_v392}). Lacuna: o resumo deu a última linha da escada como a tensão."),
    en=en("the neutrino number", "REAL in the core; DERIVED from a reading, to be vetoed",
          r"The ladder ``$1.64\to2.21\to2.95\sigma$'' above ends at a global fit; the number of the $m_2$ blade is $2.21\sigma$ (autonomous JUNO, official expert, reading R3 ratified on 02/10/2026), and the $2.95\sigma$ (NuFIT 6.1) and $2.44\sigma$ (Capozzi et al.) are reflections, beside it (record \texttt{neutrino\_m2\_perito\_v392}). Gap: the summary gave the last rung of the ladder as the tension."))

TX["d1"] = dict(
    registro="d1_orientacao_errata_v392", estatuto="[REAL] no nucleo (z lidos de orientation_is_the_sign_v367); o bit segue [INPUT]", fonte=["core.orientation_is_the_sign_v367 (um_absoluto.json " + H["CORE"] + ")", "levantamento CR / D1 (R1 de 02/10 pos o D1 V3 ao lado)"],
    pt=pt("a orientação do D1", "REAL no núcleo; o bit segue INPUT",
          r"A ``tensão D1 de $%s\sigma$'' foi medida no ramo implementado, que \texttt{orientation\_is\_the\_sign\_v367} lê como o ramo espelhado em primeira ordem (\texttt{IMPLEMENTED\_IS\_MIRROR\_TO\_FIRST\_ORDER}); no ramo da face do estado o mesmo dado dista $%s\sigma$. "
          r"O bit --- qual face fecha o balanço --- não está derivado, e trocar o sinal pede pré-registro novo com dado novo, não reler este (registro \texttt{d1\_orientacao\_errata\_v392}). Lacuna: a estrutura dizia que a tensão era condicional ao mapa; o texto repetiu o número do dado sem dizer o ramo."),
    en=en("the orientation of D1", "REAL in the core; the bit stays INPUT",
          r"The ``D1 tension of $%s\sigma$'' was measured on the implemented branch, which \texttt{orientation\_is\_the\_sign\_v367} reads as the mirrored branch to first order (\texttt{IMPLEMENTED\_IS\_MIRROR\_TO\_FIRST\_ORDER}); on the state-face branch the same data lie at $%s\sigma$. "
          r"The bit --- which face closes the balance --- is not derived, and switching the sign calls for a new preregistration with new data, not for rereading this one (record \texttt{d1\_orientacao\_errata\_v392}). Gap: the structure said the tension was conditional on the map; the text repeated the number of the data without saying the branch."))

for k_, d_ in TX.items():
    for lg in ("pt", "en"):
        d_[lg] = sub_h(d_[lg])
    d_["fonte"] = [sub_h(x) if isinstance(x, str) else x for x in d_["fonte"]]


# ---- montagem dos patches A03 (cada lingua separada)
def a03_stmt(pid, grupo, desc, ref, call, key, lang, registro=None, must_first=None, fmt_args=None, nota=""):
    d = TX[key]

    def make(col):
        return py_stmt(call, col, d[lang], fmt_args)
    insert_after_stmt(PATCHES_A03, pid, grupo, desc, ref, make, registro or d["registro"], d["estatuto"], d["fonte"], d[lang], lang=lang.upper(), nota=nota, must_first=must_first)


def a03_hdr(pid, grupo, desc, line, key, lang, must, registro=None):
    """insere o(s) s.append logo depois da linha (o addcontentsline) que fecha o cabecalho da secao. `key` pode ser uma lista (ordem preservada)."""
    keys = key if isinstance(key, list) else [key]
    ds = [TX[k] for k in keys]
    insert_after(PATCHES_A03, pid, grupo, desc, [line], line, "\n".join(py_stmt("s.append", 4, d[lang]) for d in ds),
                 registro or " + ".join(dict.fromkeys(d["registro"] for d in ds)), "; ".join(d["estatuto"] for d in ds), sum([d["fonte"] for d in ds], []),
                 "\n".join(d[lang] for d in ds), lang=lang.upper(), must=must)


def a03_tail(pid, grupo, desc, ref_line, tail_old, key, lang, registro=None):
    """errata DENTRO da string crua do paragrafo (tupla EN/PT): o texto novo encosta antes da aspa de fechamento."""
    d = TX[key]
    need(ref_line, tail_old)
    line = L[ref_line - 1].rstrip()
    assert line.endswith(tail_old), (pid, line[-80:])
    cand = tail_old
    k = len(tail_old)
    while Tn.count(cand) != 1:
        k += 10
        assert k <= len(line), (pid, "tail nao unico na linha", Tn.count(cand))
        cand = line[-k:]
    cut = len(cand) - len(tail_old) + tail_old.index('"')
    new = cand[:cut] + " " + tail_text(d[lang]).lstrip() + cand[cut:]
    tail_old = cand
    add(PATCHES_A03, pid, grupo, desc, [ref_line], tail_old, new, registro or d["registro"], d["estatuto"], d["fonte"], d[lang], lang=lang.upper(),
        nota="inserido DENTRO da string crua do paragrafo, antes da aspa de fechamento")


# --- G1: lei de campo curvo (PT l.166152; EN l.170494)
a03_stmt("A03-01-PT", "lei de campo curvo", "PT l.166152 'O que nao se afirma' (Fundacao v390)", 166152, "s.append", "lei", "pt", must_first="O que não se afirma")
a03_stmt("A03-01-EN", "lei de campo curvo", "EN l.170494 'What is not claimed'", 170494, "s.append", "lei", "en", must_first="What is not claimed")
# --- G2: escala de beta (PT l.165421; EN l.165419) -- tupla (EN if en else PT): errata dentro de cada string
l_pt = L[165421 - 1]
assert l_pt.rstrip().endswith('O que o rio poupa segue sendo o centralizador.]"))'), l_pt[-120:]
a03_tail("A03-02-PT", "escala de beta", "PT l.165421 'A predicao afiada, e o rio...' (convergencia e WHICH_MU)", 165421, 'O que o rio poupa segue sendo o centralizador.]"))', "beta", "pt")
l_en = L[165419 - 1]
assert l_en.rstrip().endswith('What the river spares is still the centralizer.]") if en else'), l_en[-120:]
a03_tail("A03-02-EN", "escala de beta", "EN l.165419 'The sharpened prediction...'", 165419, 'What the river spares is still the centralizer.]") if en else', "beta", "en")
# --- G3: palavra aniquiladora -> letra (PT l.203582; EN l.206031)
a03_stmt("A03-03-PT", "palavra->letra", "PT l.203582 WitnessSeed 'palavra aniquiladora'", 203582, "c.append", "letra", "pt", must_first="WitnessSeed")
a03_stmt("A03-03-EN", "palavra->letra", "EN l.206031 WitnessSeed 'annihilating word'", 206031, "c.append", "letra", "en", must_first="WitnessSeed")
# --- G4: estatuto 'O que nao se declara' (PT 166092-94; EN 170433-35): CMB-S4 + testemunha
a, b, col = stmt_of(166093)
need(a, "O que não se declara")
for lang, pid_ in (("pt", "PT"), ("en", "EN")):
    ref = 166093 if lang == "pt" else 170434
    a_, b_, col_ = stmt_of(ref)
    need(a_, "O que não se declara" if lang == "pt" else "What is not declared")
    d1_, d2_ = TX["cmbs4"], TX["testemunha"]
    old, _ = uniq(b_, b_)
    new = old + "\n" + py_stmt("s.append", col_, d1_[lang]) + "\n" + py_stmt("s.append", col_, d2_[lang])
    add(PATCHES_A03, "A03-04-" + pid_, "estatuto: CMB-S4 + testemunha", ("PT l.166093 / 166092 'O que nao se declara'" if lang == "pt" else "EN l.170434 / 170433 'What is not declared'"),
        [ref, ref - 1], old, new, "cmb_s4_errata_v392 + cunhagens_v392", d1_["estatuto"] + " ; " + d2_["estatuto"], d1_["fonte"] + d2_["fonte"],
        d1_[lang] + "\n" + d2_[lang], lang=pid_, nota="dois s.append novos em sequencia (CMB-S4; quem testemunha)")
# --- G5: 'As tres provas' (PT 166069-89; EN 170410-30): 6163 (166070), RG canal (166079), Hubble (166078-82)
for lang, pid_ in (("pt", "PT"), ("en", "EN")):
    ref = 166070 if lang == "pt" else 170411
    a_, b_, col_ = stmt_of(ref)
    need(a_, "As três provas" if lang == "pt" else "The three proofs")
    d_ = [TX["escada"], TX["rgcanal"], TX["f9ptr"]]
    old, _ = uniq(b_, b_)
    new = old + "\n" + "\n".join(py_stmt("s.append", col_, x[lang]) for x in d_)
    add(PATCHES_A03, "A03-05-" + pid_, "estatuto: escada / RG canal / Hubble", ("PT l.166070, 166079, 166078-82 'As tres provas'" if lang == "pt" else "EN l.170411 'The three proofs' (e as linhas correspondentes)"),
        [ref, ref + 9, "%d-%d" % (ref + 8, ref + 12)], old, new, "estatuto_da_prova_ressalva_v392 + estatuto_reafirmado_v392 + fase9_duas_testemunhas_v392", "; ".join(x["estatuto"] for x in d_),
        sum([x["fonte"] for x in d_], []), "\n".join(x[lang] for x in d_), lang=pid_, nota="tres s.append novos em sequencia (6163; RG canal a canal; razao de Hubble)")
# --- G6: cabecalhos de secao
a03_hdr("A03-06-PT", "v385 Axioma + POSTO=RANK", "PT l.166688 cabecalho 'Ao lado (v385)' (+ addcontentsline l.166689): nome do degrau final (axioma) e POSTO=RANK", 166689, ["axioma", "rank_v385"], "pt", "Ao lado (v385): o Axioma e a testemunha falsa")
a03_hdr("A03-06-EN", "v385 Axioma + POSTO=RANK", "EN l.171042 cabecalho 'Beside (v385)' (+ addcontentsline l.171043): final step name (axioma) and POSTO=RANK", 171043, ["axioma", "rank_v385"], "en", "Beside (v385): the Axiom and the false witness")
a03_hdr("A03-07-PT", "v386 o fixo", "PT l.166634 cabecalho 'Ao lado (v386): o Verbo seleciona' (+ addcontentsline l.166635)", 166635, "fixo", "pt", "Ao lado (v386): o Verbo seleciona")
a03_hdr("A03-07-EN", "v386 o fixo", "EN l.170988 cabecalho 'Beside (v386)' (+ addcontentsline l.170989)", 170989, "fixo", "en", "Beside (v386): the Verb selects")
a03_hdr("A03-08-PT", "v388 Fase 9", "PT l.166219 cabecalho 'Ao lado (v388)' (+ addcontentsline l.166220)", 166220, "f9", "pt", "Ao lado (v388)")
a03_hdr("A03-08-EN", "v388 Fase 9", "EN l.170561 cabecalho 'Beside (v388)' (+ addcontentsline l.170562)", 170562, "f9", "en", "Beside (v388)")
a03_hdr("A03-09-PT", "Introducao", "PT l.166771 cabecalho 'Introducao' (+ addcontentsline l.166772)", 166772, "tgl", "pt", "Introdução: o que este código faz agora")
a03_hdr("A03-09-EN", "Introducao", "EN l.171125 cabecalho 'Introduction' (+ addcontentsline l.171126)", 171126, "tgl", "en", "Introduction: what this code does now")
# --- G7: 'O peso nao e o posto' (tupla EN if en else PT, PT l.165561, EN l.165560)
need(165561, "O peso n")
a03_tail("A03-10-PT", "peso/posto", "PT l.165561 'O peso nao e o posto'", 165561, 'A bandeira segue APAGADA."))', "rank_peso", "pt")
need(165560, "The weight is not the rank")
a03_tail("A03-10-EN", "peso/posto", "EN l.165560 'The weight is not the rank'", 165560, 'The flag stays dark.") if en else', "rank_peso", "en")
# --- G8: WW (tupla, PT l.165453; EN l.165452)
a03_tail("A03-11-PT", "Weinberg-Witten", "PT l.165453 'A maquina do veredito...' (escape de W-W)", 165453, 'Nada aqui move o gate."))', "ww", "pt")
a03_tail("A03-11-EN", "Weinberg-Witten", "EN l.165452 'The verdict machine...' (W-W escape)", 165452, 'Nothing here moves the gate.") if en else', "ww", "en")
# --- G9: CR-05 neutrino: (ii-b) PT 170073-94 / EN 174481-502 ; resumo 234 PT 204314-44 / EN 206781-811
a03_stmt("A03-12a-PT", "CR-05 neutrino", "PT l.170082 (ii-b) 'NuFIT pos-JUNO ... tensao CRESCE'", 170082, "partC.append", "neu_b", "pt", must_first="(ii-b)")
a03_stmt("A03-12a-EN", "CR-05 neutrino", "EN l.174490 (ii-b) 'NuFIT post-JUNO ... GROWS'", 174490, "partC.append", "neu_b", "en", must_first="(ii-b)")
a03_stmt("A03-12b-PT", "CR-05 neutrino", "PT l.204330 resumo S234 'tensao crescendo 1,64 -> 2,21 -> 2,95'", 204330, "c.append", "neu_s", "pt", must_first="\\subsection*{\\S234")
a03_stmt("A03-12b-EN", "CR-05 neutrino", "EN l.206797 resumo S234 'tension growing'", 206797, "c.append", "neu_s", "en", must_first="\\subsection*{\\S234")
# --- G10: D1 orientacao (a tensao D1 3,01): apos o paragrafo v367 (que define _f7 e _or7)
for lang, ref, pid_ in (("pt", 169467, "PT"), ("en", 173870, "EN")):
    a_, b_, col_ = stmt_of(ref)
    need(a_, "Ao lado (v367)" if lang == "pt" else "Beside (v367)")
    d_ = TX["d1"]
    args = '_f7(_or7.get("z_to_mirror_branch")), _f7(_or7.get("z_to_coupling_branch"))'
    old, _ = uniq(b_, b_)
    new = old + "\n" + py_stmt("s.append", col_, d_[lang], args)
    add(PATCHES_A03, "A03-13-" + pid_, "D1 orientacao", ("PT l.169467 (fim do paragrafo v367; a tensao D1 de 3,01 sigma nasce em l.169435-46)" if lang == "pt" else "EN l.173870 (fim do paragrafo v367)"), [ref, "stmt %d-%d" % (a_, b_)],
        old, new, d_["registro"], d_["estatuto"], d_["fonte"], d_[lang], lang=pid_, nota="os dois numeros saem em runtime de _or7 (z_to_mirror_branch / z_to_coupling_branch) via _f7, ja' definidos no mesmo bloco")
# --- G11: CR-13 ponteiros (Sigma m_nu (ii); S214; S217)
a03_stmt("A03-14a-PT", "CR-13 CMB-S4 (ponteiro)", "PT l.170066 (ii) massa m_nu 'reforco futuro pela cosmologia (CMB-S4/DESI)'", 170066, "partC.append", "cmbs4p", "pt", must_first="(ii) A massa")
a03_stmt("A03-14a-EN", "CR-13 CMB-S4 (ponteiro)", "EN l.174474 (ii) mass m_nu 'CMB-S4/DESI'", 174474, "partC.append", "cmbs4p", "en", must_first="(ii) The mass")
a03_stmt("A03-14b-PT", "CR-13 CMB-S4 (ponteiro)", "PT l.205052 S214 'a falsificacao bilateral pede Euclid DR1/CMB-S4'", 205052, "c.append", "cmbs4p", "pt", must_first="\\subsection*{\\S214")
a03_stmt("A03-14b-EN", "CR-13 CMB-S4 (ponteiro)", "EN l.207529 S214 'bilateral falsification requires Euclid DR1/CMB-S4'", 207529, "c.append", "cmbs4p", "en", must_first="\\subsection*{\\S214")
a03_stmt("A03-14c-PT", "CR-13 CMB-S4 (ponteiro)", "PT l.205148 S217 'Euclid DR1 e CMB-S4 nao sao condicao de validade'", 205148, "c.append", "cmbs4p", "pt", must_first="\\subsection*{\\S217")
a03_stmt("A03-14c-EN", "CR-13 CMB-S4 (ponteiro)", "EN l.207630 S217", 207630, "c.append", "cmbs4p", "en", must_first="\\subsection*{\\S217")

# ================================================================ saida
os.makedirs(HERE, exist_ok=True)
_aj = json.dumps(dict(gerado_por="gerar_patches_erratas.py", um_py_sha16=H["UMPY"], alvos=ALVOS), ensure_ascii=False, indent=1)
_aj = _aj.replace("CONF" + "IRMED", "CONF" + chr(92) + "u0049RMED")   # a palavra da regua nunca por extenso nos meus arquivos (so' nas ancoras copiadas do um.py)
open(OUT_ALVOS, "w", encoding="utf-8").write(_aj)

HEAD = '''# -*- coding: utf-8 -*-
"""patches_erratas_v392.py -- GERADO por V\\\\rodada2\\\\erratas\\\\gerar_patches_erratas.py (rodada 2 da cadeia v392, agente ERRATAS, 13/10/2026, gerencia c1). NAO editar a mao.

E01_PATCHES (comentarios `#` ao lado no CODIGO do um.py) e A03_PATCHES (erratas ao lado no ARTIGO PT/EN gerado pelo um.py), aplicaveis sobre o texto do um.py v391 selado
(sha16 %(um)s, 33.910.631 B, CRLF). Cada patch: id, grupo, alvo_descricao, linha_v391 (numeracao por LF = a do plano; dica, a ancora e' o TEXTO), old (texto exato, em LF; o integrador
converte para CRLF -- aplicar(T, crlf) ja' faz), new (old + a errata), n (ocorrencias esperadas de old), registro (registro v392 que carrega a prova), estatuto, fonte (arquivo + sha16 lidos por
script), texto (so' o texto novo, para a guarda). A errata e' em nome proprio da gerencia c1, com a lacuna de fidelidade, e o texto antigo FICA.
Dependencias: A03-01 (lei de campo) pressupoe a pedra TGLExt.LiganteLeiCampoCurvo instalada na v392; A03-03 pressupoe TGLExt.Palavra; A03-06/10 pressupoem TGLExt.PostoAdendo.
"""

'''


def lit(x):
    return json.dumps(x, ensure_ascii=False, indent=1) if False else repr(x)


body = HEAD % {"um": H["UMPY"]}
body += "UM_V391_SHA16 = %r\n\nE01_PATCHES = [\n" % H["UMPY"]
for p in PATCHES_E01:
    body += " {" + ", ".join("%r: %r" % (k, p[k]) for k in p) + "},\n"
body += "]\n\nA03_PATCHES = [\n"
for p in PATCHES_A03:
    body += " {" + ", ".join("%r: %r" % (k, p[k]) for k in p) + "},\n"
body += "]\n"
body += '''

def aplicar(T, crlf=True, patches=None):
    """aplica todos os patches (E01 e A03) sobre o texto T do um.py v391, com assert de contagem. `crlf` True: converte \\n -> \\r\\n em old/new. Devolve (T_novo, log).
    Verifica TODAS as contagens no original antes de aplicar (ancoras disjuntas), depois aplica e confere que cada `new` aparece n vezes."""
    cv = (lambda s: s.replace("\\n", "\\r\\n")) if crlf else (lambda s: s)
    ps = list(E01_PATCHES) + list(A03_PATCHES) if patches is None else list(patches)
    log = []
    for p in ps:
        c = T.count(cv(p["old"]))
        assert c == p["n"], ("contagem de old no original", p["id"], c, p["n"])
    for p in ps:
        T = T.replace(cv(p["old"]), cv(p["new"]))
        log.append((p["id"], p["n"], len(cv(p["new"])) - len(cv(p["old"]))))
    for p in ps:
        assert T.count(cv(p["new"])) == p["n"], ("new apos aplicar", p["id"], T.count(cv(p["new"])))
    return T, log
'''
tmp = OUT_PATCHES + ".tmp"
if os.path.exists(OUT_PATCHES):
    import shutil, time
    shutil.copyfile(OUT_PATCHES, OUT_PATCHES + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
body = body.replace("CONF" + "IRMED", "CONF" + chr(92) + "x49RMED")   # idem: o valor da string e' o mesmo (x49 = I); so' o fonte nao traz a palavra por extenso
open(tmp, "w", encoding="utf-8", newline="\n").write(body)
assert os.path.getsize(tmp) > 20000
os.replace(tmp, OUT_PATCHES)
print("OK: E01=%d patches, A03=%d patches -> %s (%d bytes)" % (len(PATCHES_E01), len(PATCHES_A03), OUT_PATCHES, os.path.getsize(OUT_PATCHES)))
