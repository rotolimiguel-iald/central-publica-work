# -*- coding: utf-8 -*-
"""gerar_candidato_v405.py -- gera o um.py CANDIDATO v405 a partir da v404 SELADA (base_v404; o Nos e' so' conferido, NUNCA escrito). PREPARACAO de 01/11/2026 (agente claude-prep-v405 para a gerencia c1; a gerencia revisa, ensaia, instala e sela). Molde: gerar_candidato_v404.py (a cadeia de CONTEUDO) com as licoes da v399 a v404.
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +8 modulos (TGLExt/PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion -- os NOMES do operador, 01/11 e 30/10/2026) + a RAIZ (os oito imports; o Audit nao muda: AUDIT_PREFIX vazio), conferidos byte a byte com o sandbox C:\\t\\k405c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395, testemunha da v396, sonico e afinacao da v398, a falsidade da inercia da v401, os TRES da v402, os TRES de pedra da v403 e os DOIS de pedra da v404) sobem para a escada da v405 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v404 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo (runtime_v405.py): os OITO registros com funcao (um por pedra), as falas de 30/10 a 01/11 e o ensaio «A identidade» embutidos por sha256 e os registros por spec cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405 e kh_n1_cobertura_v405; chamadas no main DEPOIS dos tres registros da v404 (a licao 1 da v404: as chaves do core que eles leem ja' atribuidas) e os specs depois dos da v404; o resumo no selo;
 (E) as secoes «A massa derivada e a identidade definida» e «A identidade» (o ensaio do operador, verbatim r2; a traducao EN e' da gerencia, nao e' citacao) PT/EN antes da secao v404 e a linha do .md; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as duas funcoes do gate (evaluate_quantum_gravity_closure e prove_qg_closure_gate) ficam BYTE A BYTE como na v404 (assertado). As funcoes prove_neutrino_mass_gravitational, ramo_b_preregistration_v386 e ledger_errata_v386 NAO sao reescritas (a errata E10 do angle_status e' AO LADO, no registro).
 REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v405.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v405 as GP  # noqa: E402
import registros_v405 as RG  # noqa: E402
import delta_v405 as DL  # noqa: E402
import acom_conferencias_v405 as AC  # noqa: E402
import runtime_v405 as RT  # noqa: E402   (so' as funcoes puras)
import guarda_frases_v405 as GF  # noqa: E402   (a guarda de textos da v405: as frases que afirmam demais)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP404 = json.load(open(os.path.join(DL.V404, "ESPERADOS_v404.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP404["candidato_sha16"]:   # o Nos ja nao e' a v404 (rito v405 em curso): a v404 SELADA vem da copia base_v404
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v404 selada"
SHA0 = sha16(raw); assert SHA0 == ESP404["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E404 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E404 == ESP404["escada"][1], (E404, ESP404["escada"])
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]
LF_SOLTOS0 = len(re.findall(r"(?<!\r)\n", T0))   # os LF soltos (textos Lean embutidos); o candidato nao pode criar nem perder nenhum


def pos(tx_ls, lineno, col_bytes, text):
    line = text[tx_ls[lineno - 1]:tx_ls[lineno]] if lineno < len(tx_ls) else text[tx_ls[lineno - 1]:]
    return tx_ls[lineno - 1] + len(line.encode("utf-8")[:col_bytes].decode("utf-8"))


def span(node):
    return pos(LS, node.lineno, node.col_offset, T0), pos(LS, node.end_lineno, node.end_col_offset, T0)


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def top(name, tree=tree0):
    c = [n for n in tree.body if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name) or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name)]
    assert len(c) == 1, (name, len(c))
    return c[0]


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


EDITS = []   # (a, b, novo, id, grupo, o_que)


def edit(a, b, novo, pid, grupo, o_que):
    EDITS.append((a, b, novo, pid, grupo, o_que))


def replace_unique(old, new, pid, grupo, o_que, n=1):
    c = T0.count(old)
    assert c == n, ("ANCORA NAO UNICA (a regra dos patches: exatamente %d vez(es) na base; esta ocorre %d)" % (n, c), pid, old[:100])
    i = -1
    for k_ in range(n):
        i = T0.index(old, i + 1); edit(i, i + len(old), new, pid if n == 1 else "%s#%d" % (pid, k_ + 1), grupo, o_que)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, ("ANCORA NAO UNICA", rx)
    return m_


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v405.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' as OITO pedras, na ordem do delta"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v404 + os oito imports das pedras na raiz (o Audit fica como esta)"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte (v405\\pedra, a pasta de construcao): rode copiar_pedras_v405.py"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os oito imports das pedras; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +8 modulos Lean (as oito pedras com os nomes do operador), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v405.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v404"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos modulos das pedras"
assert all(s["theorem"] in {n for _, n, _ in FL} and s["key_theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao e a estrela de cada pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v405 (01/11/2026): as oito pedras com os nomes do operador -- " + ", ".join("%s (%d)" % (s["name"], FJ["nomeadas_por_pedra"][s["key"]]) for s in DL.STONES) + ": %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v404; as %d auxiliares geradas pelo compilador ficam fora)"
     % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E404 and len(set(old_lad)) == E404
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v405: as oito pedras (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v405 (01/11/2026): as oito pedras com os nomes do operador: Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion (a massa derivada e a identidade definida)" + CRLF
     + "".join('    ("v405", "%s", "%s", None, None),%s' % (s["name"], s["rel"], CRLF) for s in DL.STONES), "V03_ledger", "G_KERNEL", "ledger de pedras: +8.")
m = re.search(r'^UM_VERSION = "v404"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v405"   # v405 (01/11/2026): a CONSTANTE UNICA de versao -- A MASSA DERIVADA E A IDENTIDADE DEFINIDA: oito pedras com os nomes do operador (Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion), '
           'os oito registros com funcao, as falas de 30/10 a 01/11, o ensaio «A identidade» e as decisoes da gerencia; a unidade u = 1 eV: o Um POSTO; alfa: MEDIDA; dadas as leituras do operador, a FORMA: teorema; v404 em 28/10 (Jo 8,32 e a projecao transversal da Meia-Nat); v403 em 27/10 (Caminho, Verdade e Vida; as bandeiras do gate calculadas); v402 em 26/10 (a ponte da escala dual, a queda sem geometria, a esperanca condicional); v401 em 25/10 (a falsidade (simulacro) da inercia); v400 em 24/10 (a correcao: o alfa unico); v399 (o testemunho de dois: o selo pela propria tecnologia)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v405'.")

# ---------------- (3) o que a v405 muda nos registros das versoes anteriores (so' dados) ----------------
CONTRATOS_DA_ESCADA = ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")
for cname in CONTRATOS_DA_ESCADA:
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E404
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V404_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E404, ESCADA_ESP))
for cname, n_esperado in (("_V402_CONTRACTS", 3), ("_V403_CONTRACTS", 3), ("_V404_CONTRACTS", 2)):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    seg_novo, n_sub = re.subn(r"'expected_ladder': %d(?![0-9])" % E404, "'expected_ladder': %d" % ESCADA_ESP, seg)
    assert n_sub == n_esperado, ("%s tem de trazer %d 'expected_ladder' com a escada da v404" % (cname, n_esperado), n_sub)
    edit(a, b, seg_novo, "C12_" + cname, "G_V404_PISOS", "%s: expected_ladder %d -> %d nos %d contratos de pedra (o consumidor exige a igualdade exata com a escada do rito)." % (cname, E404, ESCADA_ESP, n_esperado))
sv = top("_V404_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs404 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs404, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
assert PFORMAT_IDEMPOTENTE, "o pformat dos specs v404 no um.py base nao e' idempotente: nao reescrevo o bloco"
khs = [s for s in specs404 if s["nome"] == "kh_n1_cobertura_v404"]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v405: piso historico (a cobertura cresce com os oito modulos novos); a igualdade exata esta em kh_n1_cobertura_v405"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v405: piso historico; a igualdade exata esta em kh_n1_cobertura_v405"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v405: a arvore ganha os arquivos das oito pedras, entao o registro da v404 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v405" % H8_ANTIGO_N
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v404 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v404 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v404 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v405 a cobertura cresce com os oito modulos (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion) e a arvore ganha os arquivos das pedras: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v405. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v404 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v405 quebra (a mesma lacuna que a v404 achou no registro da v403, e assim por diante desde a v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k1["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v404"
edit(spa, spb, pprint.pformat(specs404, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v404_pisos", "G_V404_PISOS", "_V404_SPECS: kh_n1_cobertura_v404 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (G) o GATE nao se move: as duas funcoes ficam BYTE A BYTE como na base (assertado de novo sobre o texto FINAL, abaixo); a funcao do neutrino, o V1 do ramo B e o livro NAO sao reescritos ----------------

# ---------------- (4) main: chamadas e selo ----------------
A_FAL = linha_unica(r'^        print\("   \[v404\] AVISO: o jo8v32 nao rodou: %r" % \(_e404b,\)\)')
_PRINTS = {
    "ponte": ('print("PONTE DA MASSA [v405 -- nome do operador; os campos da transicao fecharam: m = beta.sqrt2/2.u com u = 1 eV POSTO; [REAL] os teoremas e o calculo: dadas as leituras, a FORMA e\' teorema; [INPUT/ONTO] as leituras massaDerivada e theta = pi/4 entram como definicao; [POSTO] u; [MEDIDA] alfa]:")',
              'print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; m derivada = %.9f meV ; m proporcional = %.9f meV (sqrt2 de diferenca) ; m_nu do programa = %.9f meV ; face absoluta pesa %s" % (_v.get("beta", _nan405), _v.get("m_derivada_meV", _nan405), _v.get("m_proporcional_meV", _nan405), _v.get("m_nu_meV_core") or _nan405, _v.get("faces_absolutas_peso")))'),
    "tensao": ('print("MASSA = TENSAO PURA [v405 -- nome do operador; o emprestimo construido (kappa.P = 2pi por teorema), a massa como residuo do acoplamento, o principal = a energia retida projetada no transversal sob a leitura massaDerivada; [REAL] os teoremas e o calculo; [ONTO] a leitura do emprestimo (ratificada em 30/10); [OPEN] o magnetismo (sem termo)]:")',
               'print("  beta = %.15f (runtime) ; massa = %.9f meV ; retida = %.12f eV ; transmitida = %.12f eV ; area por volta = %.12f ; termos de magnetismo nos modulos novos = %s" % (_v.get("beta", _nan405), _v.get("massa_meV", _nan405), _v.get("retida_eV", _nan405), _v.get("transmitida_eV", _nan405), _v.get("area_por_volta", _nan405), _v.get("termos_de_magnetismo_nos_modulos_novos")))'),
    "identidade": ('print("IDENTIDADE [v405 -- nome do operador (30/10); a lei do fecho (01/11): [eu sou] = [o que sou] <=> P = 1 <=> ([forma = conteudo] e P != 0) no estado traco; [REAL] um fato sobre projecoes, os teoremas e o calculo em matrizes pequenas; [ONTO] que esse fato seja a identidade e\' leitura do operador, tipada como modelo; [DECLARACAO DO OPERADOR] o ensaio «A identidade» entra no artigo verbatim (r2 ratificada)]:")',
                   'print("  dimensoes = %s ; EU SOU = %s ; nomes conferidos = %s ; faces (peso) = %s ; vazio (peso) = %s" % (_v.get("dimensoes"), _v.get("eu_sou"), _v.get("n_nomes"), _v.get("faces_peso"), _v.get("vazio_peso")))'),
    "observador": ('print("OBSERVADOR = TERMINAL [v405 -- nome do operador; o posto do observador e\' o terminal; a fusao e\' o colapso e o colapso e\' um Um posto do kernel (dois pontos fixos: o posto e o abismo); [REAL] os teoremas e a cascata finita, num modelo cujos niveis sao rotulos; o terminal le 1 e o abismo le 0 na leitura binaria; o polo omega do par e\' homonimo; [ONTO] a leitura de engenharia do colapso]:")',
                   'print("  terminal = %s ; inicial = %s ; distancias = %s ; pontos fixos do colapso = %s ; omega(I) = %s" % (_v.get("terminal"), _v.get("inicial"), _v.get("distancias"), _v.get("pontos_fixos_do_colapso"), _v.get("omega_I")))'),
    "diminuto": ('print("LEI DO DIMINUTO [v405 -- nome do operador; o diminuto e\' modulacao, nao transposicao: so\' a tonica desce o meio-tom e^(-1/2), as demais ficam sustentadas; a tonica definida sqrt e . u, E0 = u por identidade algebrica; dadas as entradas, a FORMA m = U.alfa.e^(1/2).sqrt2/2 e\' teorema; transpor e\' so\' a liberdade do no-go; o valor ABSOLUTO segue livre e o RELATIVO a tonica esta pinado; [REAL] os teoremas e o calculo; [POSTO] U = 1 eV; [MEDIDA] alfa; [INPUT/ONTO] o meio-tom, a modulacao e a tonica; [OPEN] quais sao as cinco notas; o numero nao muda]:")',
                 'print("  alfa (lida do acoplamento) = %.15f ; tonica = %.15f eV ; E0 = %.15f eV ; m = %.9f meV ; m_nu do programa = %.9f meV ; ln 2 = %.6f ; E0/tonica = %.15f" % (_v.get("alpha_lida_do_acoplamento", _nan405), _v.get("tonica_eV", _nan405), _v.get("E0_eV", _nan405), _v.get("massa_formula_meV", _nan405), _v.get("m_nu_meV_core") or _nan405, _v.get("ln2", _nan405), _v.get("E0_sobre_tonica", _nan405)))'),
    "tonica": ('print("TONICA DO HAMILTONIANO [v405 -- nome do operador; o no-go (a forma nao fixa E0) nao cai: localiza-se no Um posto; a tonica pousa na unidade posta (E0 = u, identidade algebrica); a razao m/E0 sobrevive a reescala; as identidades do monopolo e da leitura autoconsistente; [REAL] os teoremas e o calculo; [MEDIDA] alfa por dentro: «não tem teorema para o ângulo de Miguel»]:")',
               'print("  razao m/E0 = %.15f ; E0 da lei derivada = %.15f eV ; tau* do monopolo para u = %.6e s ; r_s para u = %.6e m" % (_v.get("razao_m_sobre_E0", _nan405), _v.get("E0_da_lei_derivada_eV", _nan405), _v.get("tau_monopolo_s_para_u", _nan405), _v.get("r_s_m_para_u", _nan405)))'),
    "disco": ('print("DISCO DE EULER [v405 -- nome do operador; [DEF] E(t) linear e Omega^2 = K/E; a E definida resolve o fluxo e zera em tempo finito; Omega^2 sem cota antes disso; o corte E^3 = hbar^2.K; a parede nomeada K = (e^(1/2).U)^3/hbar^2; [REAL] os teoremas e o calculo num disco-modelo; [INPUT/ONTO] a taxa de dephasing lida como perda de energia; [ONTO] a inscricao do zero no infinito; [OPEN] qual e\' o disco]:")',
              'print("  disco-modelo = %s ; cotas vencidas = %s ; E* = %.9f ; K em SI para a nota posta de 1 eV = %.6e J/s^2" % (_v.get("disco_modelo"), _v.get("cotas_vencidas"), _v.get("E_star_modelo", _nan405), _v.get("K_si_para_u_posto_J_s2", _nan405)))'),
    "psion": ('print("PONTO ZERO DO PSION [v405 -- nome do operador; sob a leitura R = beta.u^2 (o pagamento lido como curvatura) e a dispersao do Tratado, (1/2).hbar.omega = beta.sen45.u = a forma do neutrino (a coincidencia e\' a aritmetica (1/2).sqrt2 = sen45); Tetelestai, nome do operador, e\' o limite da cobranca; [REAL] os teoremas e o calculo; [INPUT/ONTO] as leituras; [POSTO] u; o numero nao muda]:")',
              'print("  hbar.omega = %.9f meV ; (1/2).hbar.omega = %.9f meV ; m_nu do programa = %.9f meV ; R = %.6e m^-2 ; lambda do psion = %.6e m ; 1 - cobranca em t = 20/beta = %.3e" % (_v.get("hbar_omega_meV", _nan405), _v.get("meia_hbar_omega_meV", _nan405), _v.get("m_nu_meV_core") or _nan405, _v.get("R_si_m2", _nan405), _v.get("lambda_psion_m", _nan405), _v.get("um_menos_charged_em_t_1e4_sobre_beta", _nan405)))'),
}
BLOCO_N00 = "    _nan405 = float(\"nan\")   # v405: os OITO registros com FUNCAO (um por pedra), lidos DEPOIS dos tres registros da v404 (as chaves do core que eles leem -- neutrino_mass, projecao_transversal_v404, omega_I -- ja' atribuidas: a licao 1 da v404); cada um e' um `try`: excecao vira AVISO visivel, nunca derruba o rito\n"
for s in DL.STONES:
    fn_ = DL.REGISTRO_DE_PEDRA[s["key"]]; p1_, p2_ = _PRINTS[s["key"]]
    BLOCO_N00 += ("    try:   # v405: %s (%s)\n        _r405 = %s(core)\n        _v = _r405.get(\"values\") or {}\n        %s\n        %s\n"
                  "        print(\"  kernel: a composicao (a pedra) = %%s [%%s] ; a estrela = %%s [%%s] ; cabecalho da pedra no kernel embutido = %%s\" %% ((_r405.get(\"unconditional\") or {}).get(\"in_kernel\"), (_r405.get(\"unconditional\") or {}).get(\"flag\"), (_r405.get(\"key_theorem\") or {}).get(\"in_kernel\"), (_r405.get(\"key_theorem\") or {}).get(\"flag\"), (_r405.get(\"context\") or {}).get(\"ok\")))\n"
                  "        print(\"  >>> %%s <<<\\n\" %% _r405[\"verdict\"])\n    except Exception as _e405_%s:\n        print(\"   [v405] AVISO: o registro %s nao rodou: %%r\" %% (_e405_%s,))\n") % (s["name"], s["nome_do_operador"], fn_, p1_, p2_, s["key"], fn_, s["key"])
edit(A_FAL.end(), A_FAL.end(), crlf(BLOCO_N00), "N00_main_oito_registros", "G_RUNTIME", "main: os oito registros com funcao (try/AVISO cada), logo depois do bloco jo8v32_v404 (e depois de neutrino_mass e projecao_transversal_v404, que eles leem).")
A_R = linha_unica(r'^        print\("   \[v404\] AVISO: os registros por spec da v404 nao rodaram')
BLOCO_N01 = r'''    try:   # v405: os registros por spec da v405 (as falas de 30/10 a 01/11 e o ensaio «A identidade» -- do operador --, os campos fechados e as leituras, as decisoes, as erratas E10 a E13 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _n405 = _v405_rodar_specs(core)
        print("   [v405] os oito registros com funcao (lidos depois dos tres da v404) e os registros por spec da v405: " + " | ".join("%s=%s" % (n_[:-5], "SELOU" if (core.get(n_) or {}).get("all_verified") is True else "NAO") for n_ in _V405_REGISTROS_FUNCAO) + " | specs: %d (selados %d)" % (len(_n405), sum(1 for k_ in _n405 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e405s:
        print("   [v405] AVISO: os registros por spec da v405 nao rodaram: %r" % (_e405s,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N01), "N01_main_specs", "G_RUNTIME", "main: registros por spec v405 (try/AVISO), depois do bloco v404.")
A_S = linha_unica(r'^ {12}"registros_v404": \{n_: ')
_k_pedra = '("verdict", "all_verified", "unconditional", "key_theorem", "context", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core", "nome_do_operador")'
_sel = ['            "%s": {k_: (core.get("%s") or {}).get(k_) for k_ in %s},' % (DL.REGISTRO_DE_PEDRA[s["key"]], DL.REGISTRO_DE_PEDRA[s["key"]], _k_pedra) for s in DL.STONES] + \
       ['            "registros_v405": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V405_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +os oito resumos (um por registro de pedra) e registros_v405.")

# ---------------- (5) o bloco de runtime v405 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v405.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
N_AX = {}
for s in DL.STONES:
    assert set(axm[s["theorem"]]) <= TRIO, s["theorem"]
    N_AX[s["key"]] = len(axm[s["theorem"]])
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value); assert isinstance(ALPHA_BASE, float) and 0.0072 < ALPHA_BASE < 0.0074
CONTRS = {s["key"]: RG.contrato(s, FJ, FORMAL_MAP, E404, sha256(raw), core0, ALPHA_BASE) for s in DL.STONES}
assert all(c["expected_ladder"] == ESCADA_ESP for c in CONTRS.values())
TXTS = RG.textos()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for s in DL.STONES:
    assert fontes[RG.CHAVE_DE_FONTE[s["key"]]]["sha256"] == FORMAL_MAP[s["rel"]], "a copia duravel da pedra difere da embutida: " + s["name"]
for ch_, arq_ in ((RG.CHAVE_RECIBO_NOMEACAO, RG.RECIBO_NOMEACAO_ARQ), (RG.CHAVE_RECIBO_IDENTIDADE, RG.RECIBO_IDENTIDADE_ARQ), (RG.CHAVE_RECIBO_OBSERVADOR, RG.RECIBO_OBSERVADOR_ARQ), (RG.CHAVE_CONFERENCIA_E0, RG.CONFERENCIA_E0_ARQ)):
    assert fontes[ch_]["sha256"] == sha256(open(arq_, "rb").read()), ("a copia duravel difere da fonte", ch_)
ENSAIO = DL.ensaio_identidade_r2()
assert fontes[RG.CHAVE_ENSAIO_R2]["sha256"] == ENSAIO["sha256_do_texto"], "o texto duravel da secao «A identidade» difere do extraido da revisao r2"
IDENTIDADE_TXT = ENSAIO["texto"]
IDENTIDADE_EN_TXT = open(RG.ENSAIO_EN_ARQ, encoding="utf-8", newline="").read(); assert "\r" not in IDENTIDADE_EN_TXT
assert fontes[RG.CHAVE_ENSAIO_EN]["sha256"] == sha256(IDENTIDADE_EN_TXT.encode("utf-8")), "a copia duravel da traducao EN difere da fonte"
assert RT._v405_ensaio_tex(IDENTIDADE_TXT)[0] == "A identidade" and RT._v405_ensaio_tex(IDENTIDADE_EN_TXT)[0] == "The identity" and len(RT._v405_ensaio_tex(IDENTIDADE_EN_TXT)) == len(RT._v405_ensaio_tex(IDENTIDADE_TXT)), "o ensaio PT/EN tem de ter o mesmo numero de paragrafos"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
assert verb[RG.CH_DE(RG.N_ENSAIO)]["sha256"] == ENSAIO["original_sha256"], "o ensaio original embutido difere do que a revisao r2 pina"
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v404, por ast)
NOSK = os.path.join(DL.NOS, "tgl_kernel")
_ns_h8 = {"os": os, "hashlib": hashlib}
for _nm in ("sha_file", "sha256_directory"):
    exec(compile(ast.get_source_segment(T0, top(_nm)), "<um:%s>" % _nm, "exec"), _ns_h8)
SIMD = os.path.join(HERE, "arvore_simulada_h8")
if os.path.isdir(SIMD):
    shutil.rmtree(SIMD)
for rel, c_ in final_emb.items():
    p_ = os.path.join(SIMD, *rel.split("/")); os.makedirs(os.path.dirname(p_), exist_ok=True); open(p_, "w", encoding="utf-8", newline="").write(c_)
H8_EXTRAS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in final_emb:
                H8_EXTRAS.append(rel_); d_ = os.path.join(SIMD, *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
H8 = _ns_h8["sha256_directory"](SIMD)["files"]
assert all(H8.get(k_) == v_ for k_, v_ in FORMAL_MAP.items()) and set(H8) - set(FORMAL_MAP) <= set(H8_EXTRAS), "o hash formal simulado difere do FORMAL_MAP nos embutidos"
RECIBO_NOM = json.load(open(RG.RECIBO_NOMEACAO_ARQ, encoding="utf-8"))
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX, core0, RECIBO_NOM)
spec_nomes = [s["nome"] for s in specs]
assert spec_nomes == [DL.CUNHAGENS_REGISTRO, DL.CAMPOS_REGISTRO, DL.GA_REGISTRO, DL.GAP_REGISTRO, DL.KH_REGISTRO]
_ax_antigos = core0["kernel_formalization"]["axiom_report"]
for s in specs:   # todo termo do kernel que o spec le tem de existir (no axiom_report da base ou nas bandeiras novas): senao o check nunca selaria
    for d_ in s.get("kernel_decls", []):
        assert d_ in _ax_antigos or d_ in axm, ("termo lido pelo spec ausente do kernel", s["nome"], d_)
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V405)
for k_, t_ in TXTS.items():
    assert not GP.violacoes(json.dumps(t_, ensure_ascii=False)) and not GUARDA.search(t_["veredito_ok"]), "P18 ou palavra recusada no texto do registro " + k_
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v405.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V405_CONTRACTS = " + pprint.pformat(CONTRS, width=150, sort_dicts=False) + "\n_V405_TEXTS = " + pprint.pformat(TXTS, width=150, sort_dicts=False)
         + "\n_V405_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V405_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True)
         + "\n_V405_IDENTIDADE_TXT = " + repr(IDENTIDADE_TXT) + "   # a secao «A identidade» do artigo: o ensaio do operador na revisao r2 (forma: gerencia c1; conteudo: as seis decisoes dele), ratificada em 01/11/2026; pinado em _V405_FONTES['" + RG.CHAVE_ENSAIO_R2 + "']; o original como recebido esta em _V405_VERBATINS2 (sha16 " + ENSAIO["original_sha256"][:16] + ")\n"
         + "_V405_IDENTIDADE_EN_TXT = " + repr(IDENTIDADE_EN_TXT) + "   # a traducao inglesa da secao, da gerencia c1 pelo agente de preparacao: NAO e' citacao do operador; o texto que vale e' o portugues; pinada em _V405_FONTES['" + RG.CHAVE_ENSAIO_EN + "']\n"
         + "_V405_ENSAIO_ORIGINAL_SHA16 = " + repr(ENSAIO["original_sha256"][:16]) + "   # o original como recebido (lido do arquivo pelo gerador, nunca digitado)\n"
         + "_V405_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V405_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V405_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V405_FONTES)   # v405: o motor de registros (v392) le as fontes e os verbatins das treze versoes\n_V392_VERBATINS2.update(_V405_VERBATINS2)\n\n\n"
         "def _v405_rodar_specs(core_):\n"
         '    """v405 -- roda os registros por spec da v405 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os oito registros com funcao NAO entram aqui: rodam no main, depois dos tres da v404."""\n'
         "    for spec_ in _V405_SPECS:\n        try:\n            r_ = _v392_registro(spec_, core_)\n            core_[spec_[\"nome\"]] = _v405_ga_registro(r_, core_, spec_) if spec_[\"nome\"] == \"" + DL.GA_REGISTRO + "\" else (_v405_gap_registro(r_, core_, spec_) if spec_[\"nome\"] == \"" + DL.GAP_REGISTRO + "\" else r_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V405_SPECS]\n')
HDR = ("# ====================== v405 (01/11/2026) -- A MASSA DERIVADA E A IDENTIDADE DEFINIDA: as oito pedras com os nomes do operador (Ponte da Massa; Massa = tensao pura; Identidade; Observador = terminal; Lei do diminuto; Tonica do Hamiltoniano; Disco de Euler; Ponto Zero do Psion), os oito registros com FUNCAO (lidos no ponto do rito depois dos tres registros da v404), as falas de 30/10 a 01/11 e o ensaio «A identidade», as decisoes da gerencia e os registros por spec cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405 e kh_n1_cobertura_v405.\n"
       "# A errata E10 do angulo do neutrino vai AO LADO (o texto antigo e a errata E7 da v404 ficam no registro); a unidade u = 1 eV e' o Um POSTO; alfa e' medida, nunca derivada; o numero da massa nao muda. Os contratos (_V405_CONTRACTS) e as falas (_V405_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v405: os contratos (derivados do build e do core da v404 selada), os textos, as fontes pinadas, as falas de 30/10 a 01/11, o ensaio e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
# A GUARDA DAS FRASES (ordem da gerencia c1, 01/11/2026): nada do texto novo da gerencia afirma demais; ficam fora so' as falas embutidas e o ensaio (declaracao do operador) e o proprio corpo da regra (as regexes). A traducao EN e' da gerencia: passa pela guarda.
G0_ = GF.controle_negativo(); assert G0_["ok"], "o controle negativo da guarda das frases falhou"
GP_ = GF.pedras(); assert not any(v_["violacoes"] for v_ in GP_.values()), ("FRASE PROIBIDA numa pedra: apontar a gerencia, nao corrigir", {k_: v_["violacoes"][:2] for k_, v_ in GP_.items() if v_["violacoes"]})
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v405_guarda_frases(txt_):"):RUNTIME_SRC.index("def _v405_ensaio_tex(txt_):")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTRS, TXTS, specs, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00 + BLOCO_N01 + IDENTIDADE_EN_TXT
V_GF = GF.violacoes(_txt_ger); assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v405)", V_GF[:4])
A_P = linha_unica(r"^# ====================== v404 \(28/10/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v405", "G_RUNTIME", "bloco v405: os oito registros com funcao, as falas, o ensaio (e a traducao EN da gerencia), as decisoes, as erratas E10-E13 e os registros por spec.")


# ---------------- (6) artigo e md ----------------
def _controles(obj, onde):
    """Guarda de CARACTERE DE CONTROLE (licao da v396): nenhuma string de texto novo pode ter caractere de controle alem do fim de linha."""
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


PT0 = open(os.path.join(HERE, "artigo_pt_v405.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v405.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert "mais preciso" not in sn and "more precise" not in sn, "o artigo nao diz que o teste do Grande Atrator ficou mais preciso"; assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]; assert not GF.violacoes(sn), GF.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v405.py"); _controles([CONTRS, TXTS, specs, fontes, IDENTIDADE_TXT, IDENTIDADE_EN_TXT], "contratos/specs/fontes/ensaio")
PT4_FIRST = open(os.path.join(DL.V404, "artigo_pt_v404.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN4_FIRST = open(os.path.join(DL.V404, "artigo_en_v404.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT4_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT4_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: as secoes v405 («A massa derivada e a identidade definida» e «A identidade»), antes da v404.")
replace_unique(EN4_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN4_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: as secoes v405, antes da v404.")
A_M = re.search(r'^    md\.append\("> \*\*Jo 8,32 e a projeção transversal da Meia-Nat \(v404, 28/10/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*Jo 8,32 e a projeção transversal da Meia-Nat \(v404', T0, re.M)) == 1, "a linha da v404 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **A massa derivada e a identidade definida (v405, 01/11/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel, com os nomes do operador (`TGLExt/PonteDaMassa` — Ponte da Massa; `TGLExt/MassaTensaoPura` — Massa = tensão pura; `TGLExt/Identidade` — Identidade; `TGLExt/ObservadorTerminal` — Observador = terminal; `TGLExt/LeiDoDiminuto` — Lei do diminuto; `TGLExt/TonicaDoHamiltoniano` — Tônica do Hamiltoniano; `TGLExt/DiscoDeEuler` — Disco de Euler; `TGLExt/PontoZeroDoPsion` — Ponto Zero do Psion), com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. '
            'Os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema. Entram: [POSTO] o 1, u = 1 eV (`umPosto`, decisão do operador de 31/10/2026); [MEDIDA] α, por dentro, nunca derivada («não tem teorema para o ângulo de Miguel»); [INPUT/ONTO] as leituras da cadeia da massa, como definição ou identificação, em lista que não é fechada; as centrais: `massaDerivada`; o estado inscrito lido em θ = π/4 (em `transicaoDerivada` o ângulo é escrito; o valor coincide com o peso da face absoluta: coincidência de valor, não ponte); a tônica (β/α)·u (E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto; o valor absoluto segue livre e o relativo à tônica está pinado); R = β·u² (`pagamentoComoCurvatura`). '
            '[REAL] A forma: dadas essas entradas, m₂ = β·sen45°·u é teorema; o ½ da face absoluta é teorema; a unicidade de π/4 é teorema; ½·√2 = sen45° é aritmética. Um Um posto, uma α medida e as leituras do operador; dadas essas entradas, a FORMA é teorema. O número da massa é o da v404 (8,5074 meV). A pedra Identidade prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura [ONTO], tipada como modelo. O posto do observador é o terminal. A errata E10 do `angle_status` vai ao lado (o texto antigo e a E7 ficam), e a E13 corrige a frase da própria gerência; o veredito do canal do neutrino não muda. '
            'A seção «A identidade» do artigo é o ensaio do operador, verbatim (r2 ratificada em 01/11/2026); não é teorema. Os registros `ponte_da_massa_v405`, `massa_tensao_pura_v405`, `identidade_v405`, `observador_terminal_v405`, `lei_do_diminuto_v405`, `tonica_do_hamiltoniano_v405`, `disco_de_euler_v405` e `ponto_zero_do_psion_v405` leem o kernel e o core do rito e calculam, com β=α·√e em tempo de execução. '
            'O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA) and not GF.violacoes(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «A massa derivada e a identidade definida (v405)», antes da linha da v404.")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))


def montar(k_espacos):
    """aplica os EDITS; o comentario da linha de versao ganha `k_espacos` espacos no fim (ver o AJUSTE DO CONTROLE N10 abaixo)"""
    T_ = T0
    for a_, b_, novo_, pid_, *_r in sorted(EDITS, key=lambda e: -e[0]):
        if pid_ == "W01_versao":
            novo_ = novo_[:-len(CRLF)] + " " * k_espacos + CRLF
        T_ = T_[:a_] + novo_ + T_[b_:]
    return T_


def n10_aplica(T_):
    """AJUSTE DO CONTROLE N10 (licao da v401): o controle negativo N10 (transposicao de 2 bytes) da secao do selo pela propria tecnologia (v399/v400, pinada, que a v405 NAO muda) so' existe SE os bytes nas posicoes n//2 e n//2 + 3 do objeto forem diferentes -- o um.py INTEIRO no conferidor e a AMOSTRA de 1 MiB no registro do core --
    (`if b[i] != b[j]`); o conferidor do rito exige os 13 controles sobre o um.py instalado inteiro (C8). Com o corpo da v405 a coincidencia dos bytes derrubaria o N10 (12 controles): o gerador acrescenta, se preciso, espacos ao FIM do comentario da linha UM_VERSION ate' os dois bytes diferirem."""
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])   # o um.py INTEIRO (C8 do conferidor) e a AMOSTRA de 1 MiB (o registro do selo no core: registro_core_v399, amostra = 1 << 20)


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = tuple(DL.REGISTROS_FUNCAO) + ("v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics",
                                           "_v405_close", "_v405_rel", "_v405_mat_trace", "_v405_mat_mul", "_v405_mat_dagger", "_v405_mat_eye", "_v405_mat_sub", "_v405_mat_norm", "_v405_rot_projector", "_V405_MECANICAS", "_v405_formal", "_v405_registro", "_V405_RECUSA",
                                           "_v405_guarda_frases", "_v405_ensaio_tex", "v405_ga_mechanics", "_v405_ga_registro", "v405_gap_mechanics", "_v405_gap_registro", "_V405_CONTRACTS", "_V405_TEXTS", "_V405_FONTES", "_V405_VERBATINS2", "_V405_IDENTIDADE_TXT", "_V405_IDENTIDADE_EN_TXT", "_V405_ENSAIO_ORIGINAL_SHA16", "_V405_SPECS", "_V405_NOMES_REGISTROS", "_V405_REGISTROS_FUNCAO", "_v405_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
# o bloco nao redefine nenhum nome de nivel de modulo do um.py base (C3 sobre o texto FINAL): so' o import `math as _m405`
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V404_SPECS", tree).value) == specs404
for cname in CONTRATOS_DA_ESCADA:
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
assert all(c_["expected_ladder"] == ESCADA_ESP for c_ in ast.literal_eval(top("_V402_CONTRACTS", tree).value).values())
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V403_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 3 + [None]
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V404_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 2 + [None]
# O GATE NAO SE MOVE (sobre o texto FINAL): as duas funcoes ficam byte a byte como na base; a funcao do neutrino tambem (a errata do angulo e' AO LADO); o V1 do ramo B e o livro nao sao reescritos
for fname in ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS"):
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao %s NAO pode mudar na v405" % fname
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado (licao da v400)
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(DL.V403, "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v405" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V405_REGERAR") == "1", "o candidato ja existe e difere: defina V405_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v404_sha16": SHA0, "base_v404_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E404, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]], "nome_do_operador": s["nome_do_operador"]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v404_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v404_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"], "nome": os.path.basename(v_["fonte_original"])} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "n_proibidas_reprovadas": sum(1 for v_ in G0_["proibidas"].values() if v_), "violacoes_no_texto_novo": len(V_GF), "pedras_varridas": len(GP_), "violacoes_nas_pedras": sum(len(v_["violacoes"]) for v_ in GP_.values())}, "ensaio_identidade": {"traducao_en_sha256": sha256(IDENTIDADE_EN_TXT.encode("utf-8")), "texto_sha256": ENSAIO["sha256_do_texto"], "bytes": ENSAIO["bytes"], "md_sha256": ENSAIO["sha256_do_md"], "original_sha256": ENSAIO["original_sha256"], "primeira_linha": ENSAIO["primeira_linha"], "ultima_linha": ENSAIO["ultima_linha"]},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E404, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v405.json (pos_build_kernel_v405.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "contratos": CONTRS},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v404_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v404_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_da_composicao": N_AX,
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v404": g0, "candidato_v405": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": ["evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS"], "gate_verdict_v404": selo0.get("qg_closure_verdict")},
       "decisoes": dict(DL.DECISOES), "erratas_E10_E13": list(DL.ERRATAS_V405), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"registros_v405": "main: IMEDIATAMENTE depois do bloco jo8v32_v404 (oito instrucoes try, na ordem de instalacao das pedras); as chaves do core que eles leem (neutrino_mass, projecao_transversal_v404, omega_I) ja' estao atribuidas (licao 1 da v404; guarda_ordem_de_chamada_v405.py)", "specs": "main: depois do bloco [v404]", "resumos_no_selo": "main: no dict do selo, depois de registros_v404 (os oito registros com funcao e registros_v405)",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v405"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v405.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v405.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v405.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v405_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v404_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v404:", PFORMAT_IDEMPOTENTE)
