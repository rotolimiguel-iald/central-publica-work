# -*- coding: utf-8 -*-
"""gerar_candidato_v400.py -- gera o um.py CANDIDATO v400 a partir da v399 SELADA (base_v399; o Nos e' so' conferido, NUNCA escrito). PREPARACAO de 24/10/2026 (gerencia c1). Molde: gerar_candidato_v399.py.
A v400 e' uma VERSAO DE CORRECAO, sem gordura: nenhum modulo de kernel, nenhum registro novo, nenhuma inscricao nova. O kernel embutido, as bandeiras, a escada, o ledger, os contratos e todos os registros ficam como na v399 (byte a byte).
Os 5 patches (todos de TEXTO; cada um com contagem exata; o gerador ABORTA se algum nao casar):
 W01_versao      UM_VERSION = "v400";
 W02_runtime_v400  a SECAO do selo pela propria tecnologia (runtime_v399.py, embutido uma vez) -> runtime_v400.py: o alfa NAO e' redeclarado (le SEALED_CODATA_ALPHA) e a checagem do beta do registro confronta com core["beta"] (montar_runtime_v400.py);
 W04_artigo_PT / W05_artigo_EN  a ERRATA AO LADO da secao da v399 (antes da secao da v398): o alfa redeclarado, a recusa da Bancada, a correcao; o QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo;
 W09_md          a linha da errata no .md canonico (depois da linha da v399).
Conferencias antes de gravar: a base e' a v399 selada (sha16 da ordem == selo == arquivo); texto novo passa pela guarda P18 e pela guarda da palavra recusada; sem caractere de controle; CRLF integro; ast.parse do candidato;
e as quatro regexes da guarda ALPHA_LINHA_UNICA / UM_VERSION_LINHA_NAO_UNICA da Bancada (lidas do PROPRIO esboco R3.5 pinado) dao 1/0/1/0 no candidato (e davam 2/0/1/0 na base: o defeito).
uso: python -I -B -X utf8 gerar_candidato_v400.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
import acom_conferencias_v400 as AC  # noqa: E402
import guarda_p18_v400 as GP  # noqa: E402
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
BASE = os.path.join(HERE, DL.BASE_DIR)
raw = open(os.path.join(BASE, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "a base nao e' o um.py que o selo v399 pina"
SHA0 = sha16(raw); assert SHA0 == DL.BASE_SHA16_DA_ORDEM, (SHA0, DL.BASE_SHA16_DA_ORDEM)
nos_um = os.path.join(DL.NOS, "um.py")
if os.path.exists(nos_um) and sha16(open(nos_um, "rb").read()) == SHA0:
    assert open(nos_um, "rb").read() == raw, "o Nos (ainda v399) difere da base copiada"
T0 = raw.decode("utf-8")
LF_SOLTOS0 = len(re.findall(r"(?<!\r)\n", T0))   # os LF soltos (468 na v399) sao de textos Lean embutidos; o candidato nao pode criar nem perder nenhum
assert "\r\n" in T0
EDITS = []   # (a, b, novo, id, grupo, o_que)


def edit(a, b, novo, pid, grupo, o_que):
    EDITS.append((a, b, novo, pid, grupo, o_que))


def replace_unique(old, new, pid, grupo, o_que, n=1):
    assert T0.count(old) == n, (pid, T0.count(old), n)
    i = T0.index(old); edit(i, i + len(old), new, pid, grupo, o_que)


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def _controles(obj, onde):
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\r\n\t"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))


# ---------------- W01: a versao ----------------
m = re.search(r'^UM_VERSION = "v399"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v400"   # v400 (24/10/2026): a CONSTANTE UNICA de versao -- a CORRECAO da v399: a secao do selo ACOM deixa de redeclarar alfa (a Bancada recusou a v399 por ALPHA_LINHA_NAO_UNICA) e le o do programa; '
           'a checagem do beta do registro do selo deixa de ser tautologica; nenhum modulo, registro ou inscricao novo; v399 em 24/10 (o testemunho de dois: o selo pela propria tecnologia)')
_controles(LINHA_V, "UM_VERSION")
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v400'.")

# ---------------- W02: a secao do selo ACOM ----------------
RT9 = open(DL.RUNTIME_V399, "rb").read().decode("utf-8"); RT0 = open(DL.RUNTIME_V400, "rb").read().decode("utf-8")
rm = json.load(open(os.path.join(HERE, "RUNTIME_MONTAGEM_v400.json"), encoding="utf-8"))
assert sha256(RT0.encode("utf-8")) == rm["runtime"]["sha256"], "runtime_v400.py em disco nao e' o que RUNTIME_MONTAGEM_v400.json registra: rode montar_runtime_v400.py"
assert rm["entrada"]["sha256"] == sha256(RT9.encode("utf-8")) and all(v["ok"] for v in rm["conferencias"].values()), "a montagem do runtime tem conferencia reprovada"
assert "\r" not in RT0 and "\r" not in RT9
replace_unique(crlf(RT9), crlf(RT0), "W02_runtime_v400", "G_RUNTIME", "a secao do selo pela propria tecnologia: o alfa nao e' redeclarado (le SEALED_CODATA_ALPHA); a checagem do beta confronta com core[\"beta\"]; o bloco do operador nao muda.")
_controles(RT0, "runtime_v400.py")

# ---------------- W04/W05: a errata ao lado no artigo ----------------
PT0 = open(os.path.join(HERE, "artigo_pt_v400.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v400.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
PT1_FIRST = open(os.path.join(DL.V398, "artigo_pt_v398.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V398, "artigo_en_v398.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: errata ao lado da secao v399 (antes da v398).")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: erratum beside the v399 section (before v398).")

# ---------------- W09: a linha da errata no .md ----------------
A_M = re.search(r'^    md\.append\("> \*\*O testemunho de dois: o selo pela própria tecnologia \(v399, 24/10/2026\):\*\*[^\r\n]*\r\n', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*O testemunho de dois', T0, re.M)) == 1, "a linha da v399 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **Errata ao lado (v400, 24/10/2026):** a v399 trazia o literal de α redeclarado numa linha não indentada da seção do selo ACOM (a adaptação da gerência, antes do bloco do operador); a Bancada Um recusou a sincronização '
            '(`ALPHA_LINHA_NAO_UNICA`) e a recusa fechou como devia (fail-closed): a v399 fica selada como está. A v400 corrige: a seção passa a ler o α do próprio programa (`SEALED_CODATA_ALPHA`), o programa tem uma só declaração de α e nenhum literal de β; '
            'o bloco do operador (hash `%s`) não muda, nem o perfil, nem os controles negativos, nem o sidecar; a checagem «β do runtime» do registro do selo passa a confrontar com o β do core do rito a 1e-9 (antes era tautológica). '
            'Nenhuma pedra, nenhum registro novo, nenhuma inscrição nova; o quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n"'
            ' % ((((core.get("selo_pela_propria_tecnologia_v399") or {}).get("values") or {}).get("bloco_embutido_sha256") or "n/d")[:16],))')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.end(), A_M.end(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha da errata (v400), depois da linha da v399.")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
out, cur, rep = [], 0, []
for a, b, novo, pid, grupo, o_que in EDITS:
    out.append(T0[cur:a]); out.append(novo); cur = b
    rep.append({"id": pid, "grupo": grupo, "o_que_muda": o_que, "bytes_removidos": len(T0[a:b].encode("utf-8")), "bytes_inseridos": len(novo.encode("utf-8"))})
out.append(T0[cur:])
T1 = "".join(out)
assert len(re.findall(r"(?<!\r)\n", T1)) == LF_SOLTOS0, "o candidato criou ou perdeu um LF solto (CRLF)"
assert len(EDITS) == 5 and [e[3] for e in sorted(EDITS, key=lambda e: e[3])] == ["W01_versao", "W02_runtime_v400", "W04_artigo_PT", "W05_artigo_EN", "W09_md"], [e[3] for e in EDITS]
tree1 = ast.parse(T1)
# a guarda ALPHA_LINHA_UNICA e as demais regexes da Bancada, DO PROPRIO esboco pinado: base (o defeito) e candidato (a correcao)
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T1)
assert g0 == {"alfa_col0": 2, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("a base nao tem o defeito medido (2 linhas)", g0)
assert g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("o candidato NAO passa a guarda ALPHA_LINHA_UNICA", g1)
a1_ = RX["RE_ALPHA"].search(T1); v1_ = RX["RE_VERSAO"].search(T1)
assert a1_ and v1_ and v1_.group(1) == "v400" and float(a1_.group(1)) == 7.2973525693e-3, (a1_ and a1_.group(0), v1_ and v1_.group(0))
# v400_pins.py: o BLOCO que a v399 inseriu (o runtime + as fontes pinadas, as quatro inscricoes e os specs), como esta no candidato (com a secao v400), do inicio do runtime ate a linha do bloco da v398; LF.
# E' o que a conferencia das citacoes e os pinos leem (nada do candidato e' digitado em outro arquivo).
_i_rt = T1.index(crlf(RT0)); _j_v398 = T1.index("# ====================== v398 (23/10/2026) -- O SONICO E A AFINACAO DAS CORDAS", _i_rt)
_j_line = T1.rfind("\n", 0, _j_v398) + 1
PINS = T1[_i_rt:_j_line].replace("\r\n", "\n")
_tp = ast.parse(PINS)
_nomes_pins = {t_.id for n_ in _tp.body if isinstance(n_, ast.Assign) for t_ in n_.targets if isinstance(t_, ast.Name)}
assert {"_V399_VERBATINS2", "_V399_SPECS", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256", "ACOM_PROVENIENCIA"} <= _nomes_pins, "o bloco extraido do candidato nao traz os pinos esperados"
assert PINS.startswith(RT0.rstrip("\n")), "o bloco extraido nao comeca pelo runtime v400"
cand_p = os.path.join(HERE, DL.CANDIDATO)
open(os.path.join(HERE, "v400_pins.py"), "w", encoding="utf-8", newline="\n").write(PINS)
data = T1.encode("utf-8")
open(cand_p + ".tmp", "wb").write(data); assert os.path.getsize(cand_p + ".tmp") == len(data); os.replace(cand_p + ".tmp", cand_p)
info = {"candidato": DL.CANDIDATO, "sha16": sha16(data), "sha256": sha256(data), "bytes": len(data), "base_v399_sha16": SHA0, "base_v399_bytes": len(raw), "delta_bytes": len(data) - len(raw),
        "patches": rep, "n_patches": len(rep),
        "kernel": {"modulos_novos": 0, "nota": "o kernel embutido, as bandeiras, a escada, o ledger e os contratos ficam como na v399 (byte a byte); a Bancada, que pina a v398, ve o diff v398 -> v400 (a pedra Testemunho), lido de DL.STONES_DESDE_B8"},
        "escada": (lambda e_: [e_[1], e_[1]])(json.load(open(os.path.join(DL.V399, "CANDIDATO_v399.json"), encoding="utf-8"))["escada"]),   # a v400 NAO muda o kernel: a escada de ANTES e' a de DEPOIS da v399 (lida do CANDIDATO_v399.json)
        "guarda_alpha_unica_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v399": g0, "candidato_v400": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T1[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
        "runtime": {"sha256": rm["runtime"]["sha256"], "bytes": rm["runtime"]["bytes"], "bloco_embutido_sha256": rm["bloco_embutido_sha256"]},
        "artigo": {"pt_snippet_sha16": sha16(PT0.encode("utf-8")), "en_snippet_sha16": sha16(EN0.encode("utf-8")), "md_linha_sha16": sha16(MD_LINHA.encode("utf-8"))},
        "pins_do_candidato": {"arquivo": "v400_pins.py", "sha16": sha16(PINS.encode("utf-8")), "bytes": len(PINS.encode("utf-8")), "nomes": sorted(_nomes_pins)[:40]},
        "ast_nos_de_nivel_de_modulo": len(tree1.body)}
# as chaves que os consumidores da v399 (ESPERADOS, conferidor, estado, pos-rito) leem do CANDIDATO_*.json, com a semantica da v400: o que NAO muda vem do CANDIDATO_v399.json (lido, nao digitado)
CM9 = json.load(open(os.path.join(DL.V399, "CANDIDATO_v399.json"), encoding="utf-8"))
assert CM9["sha16"] == SHA0, "o CANDIDATO_v399.json nao e' o da base"
k9 = CM9["kernel"]
info["n_bandeiras"] = 0
info["kernel"] = {"modulos_novos": 0, "pedras": {}, "raiz_sha16": k9["raiz_sha16"], "audit_sha16": k9["audit_sha16"], "raiz_v399_sha16": k9["raiz_sha16"], "audit_v399_sha16": k9["audit_sha16"], "raiz_v398_sha16": k9["raiz_v398_sha16"], "audit_v398_sha16": k9["audit_v398_sha16"],
                  "pedras_desde_a_bancada": k9["pedras"], "sandbox": DL.SANDBOX, "nota": "a v400 nao acrescenta modulo; pedras_desde_a_bancada = o diff v398 -> v400 que o recibo do kernel do B(n) lista"}
for k_ in ("cunhagens", "formal_files_n", "verbatins_embutidos", "registros", "n_axiomas_da_composicao", "pformat_idempotente_v398_specs"):
    info[k_] = CM9[k_]
info["h8"] = dict(CM9["h8"], pino_antigo_v399_entradas=CM9["h8"]["entradas"], nota="o kernel e a arvore do Nos sao os da v399: o pino h8 e' o mesmo (1429 entradas = 1428 embutidas + o residual _check_damming.lean)")
info["politica_de_bandeiras"] = dict(CM9["politica_de_bandeiras"], nota="nenhuma bandeira NOVA na v400; estas sao as da v399 (novas para a Bancada, que pina a v398)")
info["acom"] = dict(CM9["acom"], runtime_sha256=rm["runtime"]["sha256"], bloco_embutido_sha256=rm["bloco_embutido_sha256"], conferencias_do_runtime={k: v["ok"] for k, v in rm["conferencias"].items()},
                    edicoes_de_texto_declaradas=rm["edicoes_declaradas"], correcao_v400="alfa nao redeclarado (le SEALED_CODATA_ALPHA); beta do registro confrontado com core[beta] a 1e-9; o bloco do operador nao mudou")
info["ponto_de_chamada"] = dict(CM9["ponto_de_chamada"], nota_v400="nenhum ponto de chamada novo: a v400 so' corrige o corpo de registro_core_v399 e de selo_acom_v399")
json.dump(info, open(os.path.join(HERE, "CANDIDATO_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("candidato", DL.CANDIDATO, info["sha16"], info["bytes"], "B (+%d)" % info["delta_bytes"], "| patches:", [p["id"] for p in rep])
print("guarda ALPHA_LINHA_UNICA (esboco R3.5): base v399 =", g0, "-> candidato v400 =", g1)
