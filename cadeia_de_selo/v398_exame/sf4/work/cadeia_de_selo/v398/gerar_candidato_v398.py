# -*- coding: utf-8 -*-
"""gerar_candidato_v398.py -- gera o um.py CANDIDATO v398 a partir da v397 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v397.py (e, para a FUNCAO de registro, gerar_candidato_v396.py). PREPARACAO de 23/10/2026 (gerencia c1).
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +2 modulos (TGLExt/Sonico.lean: o nome «sonico» e' do operador; TGLExt/AfinacaoDasCordas.lean: pedra e nome ratificados por ele; ambas aprovadas em revisao independente) + raiz + Audit (os dois imports), conferidos byte a byte com o sandbox C:\\t\\k398c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger (com os 5 nomeados da afinacao que ficam FORA da composicao, listados como tais), UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395 e testemunha da v396) sobem para a escada da v398 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v397 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo: os DOIS registros com funcao `sonico_v398` e `afinacao_das_cordas_v398` (chamados no ponto real do main, na fractalizacao do Um, logo depois da testemunha_estatica_v396), as SEIS inscricoes de 23/10 embutidas por sha256 (cinco falas do operador e a leitura da
     gerencia que ele ratificou, esta rotulada como da gerencia), os registros por spec cunhagens_v398 e kh_n1_cobertura_v398; chamadas no main e no selo;
 (E) a secao «Sonico e a afinacao das cordas» PT/EN antes da secao v397 e a linha do .md. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
uso: python -I -B -X utf8 gerar_candidato_v398.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v398 as GP  # noqa: E402
import registros_v398 as RG  # noqa: E402
import delta_v398 as DL  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP397 = json.load(open(os.path.join(DL.V397, "ESPERADOS_v397.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP397["candidato_sha16"]:   # o Nos ja nao e' a v397 (rito v398 em curso): a v397 SELADA vem da copia base_v397
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v397 selada"
SHA0 = sha16(raw); assert SHA0 == ESP397["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E397 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E397 == ESP397["escada"][1], (E397, ESP397["escada"])
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]


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
    assert T0.count(old) == n, (pid, T0.count(old), n)
    i = T0.index(old); edit(i, i + len(old), new, pid, grupo, o_que)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, rx
    return m_


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v398.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' as duas pedras (Sonico, AfinacaoDasCordas)"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v397 + os imports das duas pedras"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte aprovada (v398\\pedra, work\\...): rode copiar_pedras_v398.py e refazer_sandbox_v398.sh"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ os imports das pedras Sonico e AfinacaoDasCordas; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +2 modulos Lean (TGLExt/Sonico.lean e TGLExt/AfinacaoDasCordas.lean), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v398.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v397"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos dois modulos"
assert all(s["theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao de cada pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v398 (23/10/2026): as pedras Sonico (o nome e' do operador; %d bandeiras) e AfinacaoDasCordas (pedra e nome ratificados por ele; %d bandeiras): %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v397; as %d auxiliares geradas pelo compilador ficam fora)"
     % (FJ["nomeadas_por_pedra"]["sonico"], FJ["nomeadas_por_pedra"]["afinacao"], len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E397 and len(set(old_lad)) == E397
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v398: as pedras Sonico e AfinacaoDasCordas (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
AFI = DL.STONES[1]
aux_curtos = ", ".join(n.split(".")[-1] for n in AFI["auxiliares_fora_da_composicao"])
edit(sbl, sbl, "    # v398 (23/10/2026): a pedra Sonico (o Verbo, seletor de identidade, e' o controle de oitava pinada; o custo e' a reacao ao pino, que e' memoria; o preco de uma oitava pinada e' o bit justo, ln 2; o nome «sonico» e' do operador; a lei de custo e' INPUT e nenhum termo diz que select paga uma oitava)" + CRLF
     + '    ("v398", "%s", "%s", None, None),%s' % (DL.STONES[0]["name"], DL.STONES[0]["rel"], CRLF)
     + "    # v398 (23/10/2026): a pedra AfinacaoDasCordas (fechar ciclicamente o parametro do boost e' o circulo da leitura, kappa.P = 2 pi; a torre de Matsubara n.kappa e' infinita; D = 26 e D = 10 pelo fecho da soma regularizada sob a hipotese NOMEADA MasslessFirstLevel [KNOWN]; geometria [OPEN]; pedra e nome ratificados pelo operador); "
       "os %d nomeados que ficam FORA da composicao (6), auxiliares: %s" % (len(AFI["auxiliares_fora_da_composicao"]), aux_curtos) + CRLF
     + '    ("v398", "%s", "%s", None, None),%s' % (AFI["name"], AFI["rel"], CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +2 (os auxiliares da afinacao fora da composicao listados como tais).")
m = re.search(r'^UM_VERSION = "v397"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v398"   # v398 (23/10/2026): a CONSTANTE UNICA de versao -- o sonico e a afinacao das cordas (as pedras Sonico e AfinacaoDasCordas, os registros sonico_v398 e afinacao_das_cordas_v398 e as seis inscricoes de 23/10); v397 em 23/10 (o Teste da Unica Palavra)' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v398'.")

# ---------------- (3) o que a v398 muda nos registros das versoes anteriores (so' dados) ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E397
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V397_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E397, ESCADA_ESP))
sv = top("_V397_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs397 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs397, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
khs = [s for s in specs397 if s["nome"] == "kh_n1_cobertura_v397"]; assert len(khs) == 1
k7 = khs[0]
H8_ANTIGO_N = None
for c in k7["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v398: piso historico (a cobertura cresce com os modulos Sonico e AfinacaoDasCordas); a igualdade exata esta em kh_n1_cobertura_v398"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v398: piso historico; a igualdade exata esta em kh_n1_cobertura_v398"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v398: a arvore ganha os arquivos das duas pedras, entao o registro da v397 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v398" % H8_ANTIGO_N
k7["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v397 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v397 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v397 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v398 a cobertura cresce com os modulos Sonico e AfinacaoDasCordas e a arvore ganha os arquivos das duas pedras: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v398. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v397 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v398 quebra (a mesma lacuna que a v397 achou no registro da v396)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; conferidas no ensaio a seco]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k7["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v397"
edit(spa, spb, pprint.pformat(specs397, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v397_pisos", "G_V397_PISOS", "_V397_SPECS: kh_n1_cobertura_v397 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas e selo ----------------
A_TES = re.escape('        print("   [v396] AVISO: a testemunha estatica nao rodou: %r" % (_e396,))')
m_tes = re.search("^" + A_TES + r"\r\n", T0, re.M); assert m_tes and T0.count(m_tes.group(0)) == 1, "ancora do bloco testemunha_estatica_v396 (no ponto da fractalizacao do Um) nao achada ou nao unica"
son = ['    try:   # v398: o SONICO (o Verbo pina a oitava; o custo e\' a memoria), no mesmo ponto de chamada das pedras anteriores (psibit, testemunha): o calculo e\' lido contra os termos do kernel do proprio rito; excecao vira AVISO visivel, nunca derruba o rito',
       '        _son398 = sonico_v398(core)',
       '        _sov398 = _son398.get("values") or {}',
       '        _nan398 = float("nan")',
       '        print("SONICO [v398 -- o Verbo pina a oitava e o custo e\' a memoria; [REAL] os termos do kernel e o calculo, [DERIVED] a entropia do colapso em theta_M, [INPUT/ONTO] a definicao do operador e a leitura ratificada; a lei de custo e\' INPUT]:")',
       '        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime; um dado, dois nomes: SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018) ; ln 2 = K.octaveNats 1 = o bit justo = %.12f (residuo vs H2(1/2,1/2) %.1e) ; exp(ln 2) = %.12f (residuo %.1e)" % (_sov398.get("beta", _nan398), _sov398.get("ln2", _nan398), abs(_sov398.get("octave_one_nats", _nan398) - _sov398.get("fair_bit_entropy", _nan398)), _sov398.get("exp_ln2", _nan398), _sov398.get("exp_ln2_residual", _nan398)))',
       '        print("  n oitavas = n bits (residuo %.1e ; aditividade %.1e) ; o pino nao e\' a meia-nat (ln 2 - 1/2 = %.6f) ; o seletor pina: idempotencia %.1e, fixa a acao %.1e, iteracao 10x %.1e" % (_sov398.get("n_octaves_residual", _nan398), _sov398.get("additivity_residual", _nan398), _sov398.get("pin_minus_half_nat", _nan398), _sov398.get("selector_idempotence_residual", _nan398), _sov398.get("selector_fixes_action_residual", _nan398), _sov398.get("selector_iteration_residual", _nan398)))',
       '        print("  [DERIVED] colapso em theta_M = arcsin sqrt(beta) = %.9f rad: H2(cos^2, sin^2) = %.12f nat = %.9f oitava (a fracao do bit; NUMERO DERIVADO, nao esta no kernel; teto ln 2 = %.12f)" % (_sov398.get("theta_M_rad", _nan398), _sov398.get("collapse_entropy_theta_M_nats", _nan398), _sov398.get("collapse_entropy_theta_M_octaves", _nan398), _sov398.get("ln2", _nan398)))',
       '        print("  kernel: composicao INCONDICIONAL = %s [%s] ; a lei de custo e\' INPUT e nenhum termo diz que select paga uma oitava" % ((_son398.get("unconditional") or {}).get("in_kernel"), (_son398.get("unconditional") or {}).get("flag")))',
       '        print("  >>> %s <<<\\n" % _son398["verdict"])',
       '    except Exception as _e398:',
       '        print("   [v398] AVISO: o sonico nao rodou: %r" % (_e398,))',
       '    try:   # v398: a AFINACAO DAS CORDAS, no mesmo ponto, logo depois do sonico: a aritmetica (zeta por Bernoulli, D = 26 e D = 10, d = D - 1, a torre n.kappa e os retornos) lida contra os termos do kernel do proprio rito; excecao vira AVISO visivel, nunca derruba o rito',
       '        _afc398 = afinacao_das_cordas_v398(core)',
       '        _afv398 = _afc398.get("values") or {}',
       '        _nan398a = float("nan")',
       '        print("AFINACAO DAS CORDAS [v398 -- o parametro do boost fecha ciclicamente no circulo da leitura (kappa P = 2 pi); a torre n.kappa e\' infinita; a soma regularizada fecha D = 26 e D = 10 sob a hipotese NOMEADA MasslessFirstLevel [KNOWN]; a geometria e\' [OPEN]; nada deriva cordas do axioma]:")',
       '        print("  zeta(-1) = %s e zeta(-1, 1/2) = %s (de Mathlib; conferidos por Bernoulli em fracoes) ; por direcao: boson %s, fermion NS %s, soma %s" % (_afv398.get("zeta_minus_one"), _afv398.get("hurwitz_zeta_minus_one_half"), _afv398.get("boson_direction"), _afv398.get("ns_fermion_direction"), _afv398.get("ns_direction_sum")))',
       '        print("  D critica: bosonica %s (-(D-2)/24 = -1) e supercorda NS %s (-(D-2)/16 = -1/2) ; com o sinal fermionico trocado daria D = %s ; D = 10 e\' d = %s dimensoes espaciais (o d = 9 da casa e\' [DECLARADO], nao recalculado aqui)" % (_afv398.get("bosonic_critical_dimension"), _afv398.get("superstring_critical_dimension"), _afv398.get("wrong_fermion_sign_dimension"), _afv398.get("house_spatial_dimension")))',
       '        print("  torre n.kappa (kappa de TESTE; o kappa do boost nao esta no core): residuos torre %.1e, razoes %.1e, retorno em t = P %.1e ; periodo infiel (1,1 P) a %.3f do kappa ; par afinado volta (residuo %.1e), par da estacao (1, raiz 2) maximo %.6f < 2" % (_afv398.get("tower_residual", _nan398a), _afv398.get("ratio_residual", _nan398a), _afv398.get("return_residual", _nan398a), _afv398.get("unfaithful_period_min_distance", _nan398a), _afv398.get("tuned_pair_return_residual", _nan398a), _afv398.get("station_pair_max_over_samples", _nan398a)))',
       '        print("  kernel: composicao INCONDICIONAL = %s [%s] ; hipotese MasslessFirstLevel = %s (nomeada, nao provada) ; geometria = %s ; deriva cordas do axioma = %s" % ((_afc398.get("unconditional") or {}).get("in_kernel"), (_afc398.get("unconditional") or {}).get("flag"), (_afc398.get("hypothesis") or {}).get("status"), _afc398.get("geometry"), _afc398.get("derives_strings_from_the_axiom")))',
       '        print("  >>> %s <<<\\n" % _afc398["verdict"])',
       '    except Exception as _e398a:',
       '        print("   [v398] AVISO: a afinacao das cordas nao rodou: %r" % (_e398a,))']
edit(m_tes.end(), m_tes.end(), CRLF.join(son) + CRLF, "N00_main_sonico_afinacao", "G_RUNTIME", "main: sonico_v398(core) e afinacao_das_cordas_v398(core) chamados no ponto da fractalizacao do Um, logo depois do bloco testemunha_estatica_v396, com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v397\] AVISO: os registros por spec da v397 nao rodaram')
reg = ['    try:   # v398: os registros por spec da v398 (as seis inscricoes de 23/10 -- cinco falas do operador e a leitura da gerencia que ele ratificou, esta rotulada como da gerencia --, as pedras Sonico e AfinacaoDasCordas e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito',
       '        _n398 = _v398_rodar_specs(core)',
       '        print("   [v398] o sonico e a afinacao das cordas (lidos na fractalizacao do Um) e as inscricoes de 23/10 (cunhagens_v398): sonico=%s | afinacao=%s | cunhagens=%s | registros por spec: %d (selados %d)" % ((core.get("sonico_v398") or {}).get("verdict"), (core.get("afinacao_das_cordas_v398") or {}).get("verdict"), (core.get("cunhagens_v398") or {}).get("verdict"), len(_n398), sum(1 for k_ in _n398 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e398b:',
       '        print("   [v398] AVISO: os registros por spec da v398 nao rodaram: %r" % (_e398b,))']
edit(A_R.end(), A_R.end(), CRLF.join(reg) + CRLF, "N01_main_specs", "G_RUNTIME", "main: registros por spec v398 (try/AVISO), depois do bloco v397.")
A_S = linha_unica(r'^ {12}"registros_v397": \{n_: ')
_sel = ['            "sonico_v398": {k_: (core.get("sonico_v398") or {}).get(k_) for k_ in ("verdict", "all_verified", "unconditional", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "afinacao_das_cordas_v398": {k_: (core.get("afinacao_das_cordas_v398") or {}).get(k_) for k_ in ("verdict", "all_verified", "unconditional", "exact_ladder", "hypothesis", "geometry", "derives_strings_from_the_axiom", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v398": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V398_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +sonico_v398, afinacao_das_cordas_v398 e registros_v398.")

# ---------------- (5) o bloco de runtime v398 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v398.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
N_AX = {}
for s in DL.STONES:
    assert set(axm[s["theorem"]]) == TRIO, s["theorem"]
    N_AX[s["key"]] = len(axm[s["theorem"]])
CONTR_SON = RG.contrato(FJ, FORMAL_MAP, E397, sha256(raw), DL.STONES[0], RG.USA_SONICO); CONTR_AFI = RG.contrato(FJ, FORMAL_MAP, E397, sha256(raw), DL.STONES[1], RG.USA_AFINACAO)
assert CONTR_SON["expected_ladder"] == CONTR_AFI["expected_ladder"] == ESCADA_ESP
TXT_SON = RG.texto_sonico(); TXT_AFI = RG.texto_afinacao()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["sonico_pedra"]["sha256"] == FORMAL_MAP[DL.STONES[0]["rel"]] and fontes["afinacao_pedra"]["sha256"] == FORMAL_MAP[DL.STONES[1]["rel"]], "a copia duravel de uma pedra difere da embutida"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v397, por ast)
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
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX)
spec_nomes = [s["nome"] for s in specs]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
for nome_, c_, t_, usa in (("sonico", CONTR_SON, TXT_SON, RG.USA_SONICO), ("afinacao", CONTR_AFI, TXT_AFI, RG.USA_AFINACAO)):
    assert not GP.violacoes(json.dumps(t_, ensure_ascii=False)), (nome_, GP.violacoes(json.dumps(t_, ensure_ascii=False))[:3])
    assert not GUARDA.search(t_["veredito_ok"]), nome_
    assert all(ch in verb for ch in usa) and c_["verbatins"] == list(usa), nome_
HDR = ("# ====================== v398 (23/10/2026) -- O SONICO E A AFINACAO DAS CORDAS: as pedras Sonico e AfinacaoDasCordas, os registros com FUNCAO sonico_v398 e afinacao_das_cordas_v398 (lidos na fractalizacao do Um, junto do psibit e da testemunha), as seis inscricoes de 23/10\n"
       "# (cinco falas do operador e a leitura da gerencia que ele ratificou, rotulada como da gerencia) e os registros por spec cunhagens_v398 e kh_n1_cobertura_v398. Os contratos sao DERIVADOS do build do sandbox desta cadeia (gerar_candidato_v398.py), nunca digitados; a fonte autoral das\n"
       "# funcoes e' runtime_pedras_v398.py; as falas entram EMBUTIDAS por sha256. O quadro «O Teste da Unica Palavra» (v397) fica no topo do artigo, intocado. O gate nao se move. ======================\n")
RUNTIME_SRC = open(os.path.join(HERE, "runtime_pedras_v398.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
RCODE = ("_V398_SONICO_CONTRACT = " + pprint.pformat(CONTR_SON, width=150, sort_dicts=False) + "\n_V398_SONICO_TEXT = " + pprint.pformat(TXT_SON, width=150, sort_dicts=False)
         + "\n_V398_AFINACAO_CONTRACT = " + pprint.pformat(CONTR_AFI, width=150, sort_dicts=False) + "\n_V398_AFINACAO_TEXT = " + pprint.pformat(TXT_AFI, width=150, sort_dicts=False) + "\n\n\n"
         "_V398_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V398_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V398_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V398_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V398_FONTES)   # v398: o motor de registros (v392) le as fontes e os verbatins das sete versoes\n_V392_VERBATINS2.update(_V398_VERBATINS2)\n\n\n"
         "def _v398_rodar_specs(core_):\n"
         '    """v398 -- roda os registros por spec da v398 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os registros sonico_v398 e afinacao_das_cordas_v398 NAO entram aqui: rodam no ponto da fractalizacao do Um (main)."""\n'
         "    for spec_ in _V398_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V398_SPECS]\n')
RT = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v398: os contratos (derivados do build), os textos, as fontes pinadas, as seis inscricoes de 23/10 e os registros por spec\n" + RCODE
ast.parse(RT)
_novo_texto = RUNTIME_SRC + json.dumps([CONTR_SON, CONTR_AFI], ensure_ascii=False) + json.dumps([TXT_SON, TXT_AFI], ensure_ascii=False) + json.dumps(specs, ensure_ascii=False)   # as falas do operador (verbatim) ficam fora da guarda: a guarda vale para o texto NOVO
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v397 \(23/10/2026\) -- O TESTE DA UNICA PALAVRA LIDO POR HASH")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v398", "G_RUNTIME", "bloco v398: sonico_v398 e afinacao_das_cordas_v398 (funcoes + contratos derivados do build), as seis inscricoes, registros por spec.")


# ---------------- (6) artigo e md ----------------
def _controles(obj, onde):
    """Guarda de CARACTERE DE CONTROLE (licao da v396: o heredoc do Bash colapsa `\\\\` em `\\` e `\\texttt` virou TAB + `exttt`): nenhuma string de texto novo pode ter caractere de controle alem do fim de linha."""
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


PT0 = open(os.path.join(HERE, "artigo_pt_v398.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v398.pysnip"), encoding="utf-8").read()
# os sha16 das inscricoes citadas no artigo sao LIDOS dos arquivos (registros_v398), nunca digitados nos snippets
SUBST = (("@@S_VERBO@@", RG.S_VERBO), ("@@S_NOME@@", RG.S_NOME), ("@@S_ANTES@@", RG.S_ANTES), ("@@S_CORDAS@@", RG.S_CORDAS), ("@@S_CONCORDO@@", RG.S_CONCORDO), ("@@S_LEITURA@@", RG.S_LEITURA))
for _tag, _s16 in SUBST:
    PT0 = PT0.replace(_tag, _s16); EN0 = EN0.replace(_tag, _s16)
assert "@@" not in PT0 and "@@" not in EN0, "placeholder de sha16 sobrando nos snippets do artigo"
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RUNTIME_SRC, "runtime_pedras_v398.py"); _controles([CONTR_SON, CONTR_AFI, TXT_SON, TXT_AFI, specs, fontes], "contratos/textos/specs/fontes")
PT1_FIRST = open(os.path.join(DL.V397, "artigo_pt_v397.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V397, "artigo_en_v397.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v398, antes da v397.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v398, antes da v397.")
A_M = linha_unica(r'^    md\.append\("> \*\*O Teste da Única Palavra e a pedra Token \(v397, 23/10/2026\):\*\*')
edit(A_M.end(), A_M.end(), '    md.append("> **Sônico e a afinação das cordas (v398, 23/10/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel (`TGLExt/Sonico`, o nome «sônico» é do operador; `TGLExt/AfinacaoDasCordas`, pedra e nome ratificados por ele), com ' + str(len(FL)) + ' bandeiras só de declaração nomeada; os registros com função `sonico_v398` e `afinacao_das_cordas_v398`, lidos na fractalização do Um junto do psibit e da testemunha estática, leem a composição de cada pedra no kernel do próprio rito e conferem o cálculo: ln 2 é o bit da paridade e o preço de uma oitava pinada, e^(ln 2) = 2, a entropia do colapso em θ_M é número derivado (não está no kernel), o parâmetro do boost fecha ciclicamente no círculo da leitura (κP = 2π), a torre n·κ é infinita, ζ(−1) = −1/12 e ζ(−1, ½) = 1/24, D = 26 e D = 10 pelo fecho da soma sob a hipótese nomeada MasslessFirstLevel [KNOWN], d = 9 [DECLARADO]; as ' + str(len(verb)) + ' inscrições de 23/10 embutidas por sha256 (`cunhagens_v398`: cinco falas do operador e o texto da gerência que ele ratificou, rotulado como da gerência) e a cobertura exata do Audit (`kh_n1_cobertura_v398`). Leituras do operador [INPUT/ONTO]: verbo = controle de oitava pinada; o custo é a reação ao pino, e é memória (leitura da gerência, ratificada por ele); antes de espelhada a luz é palavra; as cordas fecham a face por fora e a TGL fecha só a leitura (composição da gerência, ratificada por ele); afinação = comensurabilidade [ONTO]. Nada deriva cordas do axioma; a geometria é [OPEN]; Hagedorn só é mencionado; a lei de custo é [INPUT]; o quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF,
     "W09_md", "G_ARTIGO", "md canonico: a linha «Sonico e a afinacao das cordas (v398)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
tree = ast.parse(T)
for n in ("_v398_h2", "v398_sonico_mechanics", "_v398_bernoulli", "_v398_bernoulli_poly", "v398_afinacao_mechanics", "_v398_beta", "_v398_formal", "_V398_RECUSA", "sonico_v398", "afinacao_das_cordas_v398", "_V398_SONICO_CONTRACT", "_V398_SONICO_TEXT",
          "_V398_AFINACAO_CONTRACT", "_V398_AFINACAO_TEXT", "_V398_FONTES", "_V398_VERBATINS2", "_V398_SPECS", "_V398_NOMES_REGISTROS", "_v398_rodar_specs"):
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V397_SPECS", tree).value) == specs397
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT"):
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V398_REGERAR") == "1", "o candidato ja existe e difere: defina V398_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v397_sha16": SHA0, "escada": [E397, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v397_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v397_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": ["sonico_v398", "afinacao_das_cordas_v398"] + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E397, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v398.json (pos_build_kernel_v398.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "auxiliares_da_afinacao_fora_da_composicao": list(AFI["auxiliares_fora_da_composicao"])},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v397_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v397_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_das_composicoes": N_AX,
       "ponto_de_chamada": {"sonico_v398": "main: na fractalizacao do Um, IMEDIATAMENTE depois do bloco testemunha_estatica_v396 (que vem imediatamente depois do psibit_v395)", "afinacao_das_cordas_v398": "main: IMEDIATAMENTE depois do bloco sonico_v398", "specs": "main: depois do bloco [v397]",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v398.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v398.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v398.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v398_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v397_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v397:", PFORMAT_IDEMPOTENTE)
