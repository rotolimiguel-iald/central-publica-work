# -*- coding: utf-8 -*-
"""gerar_candidato_v386.py -- gera o um.py CANDIDATO v386 a partir da v385 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v385.py.
AS CUNHAGENS E DECISOES DO OPERADOR (05/10/2026; lidas de arquivos por sha256, nunca digitadas): o VERBO (16:53:25 UTC: «Verbo=seleção da ação»; «O Verbo
seleciona: nome, tempo e verdade»), a DECISAO do ramo B (17:11:36 UTC: «eu não havia proibido o ramo B …»; «de resto concordo com tudo») e as RESPOSTAS
(18:29:37 UTC: luz/gravidade indissociaveis; verdade e custo duas faces; o tempo lido duas vezes; a Lagrangiana; «o Nome não é ontologia, o nome é "posto"»;
«o resto vc consegue responder tudo agroa» -- a delegacao: o padrao da gerencia vale e e' dito como «decidido por delegacao»).
(1) KERNEL EMBUTIDO: o da v385 + TGLExt/TheVerbSelectsTheAction.lean (nova) + TGLExt.lean e TGL/Audit.lean (mudam: +1 import; +1 bloco de 110 #print axioms);
    kernel_src = ../v376/kernel_src, compilado e auditado ali (v386/kernel/build_full.log: rc_build 0, rc_audit 0; 10239 declaracoes; 110/110 bandeiras no trio;
    zero sorry -- lidos de kernel/sandbox_raiz_v386.json). Os TGLExt.lean e TGL/Audit.lean embutidos na v385 sao conferidos BYTE A BYTE contra os .bak do
    sandbox antes da troca. O arquivo TGL/AuditVerb_tmp.lean do sandbox (auditoria temporaria da fase A; nao importado por ninguem) NAO entra, e isso fica dito.
(2) PINOS (v386_pins.py, GERADO aqui): as 110 bandeiras (kernel/v386_flags.py + AUDIT_NOMES_v386.json); o token lido da def verbTypingStoneName da pedra; os
    4 arquivos do operador EMBUTIDOS como texto com o sha256 (VERBO txt sha16 5973d79a49995c4c; RESPOSTAS txt b49b0d9e60ee4646; DECISAO json; RESPOSTAS json),
    os carimbos lidos do transcrito (a mensagem cujo texto e' igual ao arquivo); o pre-registro V1 do ramo B (ESPEC_RUNTIME_RAMO_B_v386.json, cada sha256
    reconferido no disco; spec_sha256 recomputado); os numeros do poder (ESPEC) conferidos contra o V1 antes de pinar; a F2b e as erratas de R6/F2 (ESPEC); os
    textos R6 da v383 lidos do core selado; os pinos do pilar da v385 (chave, sha256 do resultado, veredito) lidos do core selado.
(3) PATCHES (count(old) == 1): V01 bandeiras (+110), V02 escada (+110), V03 livro das pedras (+1), V04 kernel, W01 UM_VERSION v386, W02 runtime (pinos +
    logica), W03a/b/c o reaproveitamento do pilar pela chave (_QP_REUSE_V386; a leitura do reuse dita como v386), W04 o registro no main (4 chaves novas,
    depois do registro da v385, que fica INTOCADO), W05/W06 artigo PT/EN («Ao lado (v386)», antes do trecho da v385), W07 selo, W08 a errata ao lado de R6
    no .md canonico. W09 (etiquetas): nao precisou ([POSTO] ja existe). W10 (ORDEM DO OPERADOR, 05/10 tarde): o teste em tempo real na GPU na apresentacao, no
    resumo, nas palavras-chave e no sumario (PT/EN) -- patch_W10_gpu_apresentacao_v386.py, aplicado depois do W08 (14 trocas unicas).
(4) CORRECOES pre-instalacao (05/10, noite; as tres afericoes adversariais): a pedra revisada para VERBATIM (sha256 lido de kernel/PEDRA_v386_pos_build.json, junto
    com o sha256 do build_full.log que a auditou); o RESPOSTAS json com a errata [sic] («tudo agroa») -- o V1 congelado registra o sha256 ANTERIOR, o backup de bytes
    dessa versao tem de existir (errata ao lado, dita nos pinos e no registro); o pino beta_runtime_do_V1 RETIRADO (coberto pelo spec_sha256 + 1e-9 rel + alpha.sqrt(e));
    o_que_conferir dos pinos diz a regra implementada (1e-9 rel) com a errata; a note dos verbatins diz que o VERBO escreve a constante como alpha ao quadrado (citacao, nao valor).
uso: python gerar_candidato_v386.py"""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))        # .../scratchpad/v386/pacote
V6 = os.path.dirname(HERE)                               # .../scratchpad/v386
SP = os.path.dirname(V6)                                 # .../scratchpad
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
KS = os.path.join(SP, "v376", "kernel_src")
V5 = os.path.join(SP, "v385")
K6 = os.path.join(V6, "kernel")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest()
sha16 = lambda b: sha256(b)[:16]
# ---------- a base: a v385 SELADA (o registro da instalacao da v385 e o selo dizem o mesmo) ----------
AP5 = sorted(f for f in os.listdir(V5) if f.startswith("APLICADO_AO_CANONICO_") and f.endswith(".json"))
assert AP5, "o registro da instalacao da v385 nao foi achado"
AP5 = json.load(open(os.path.join(V5, AP5[-1]), encoding="utf-8"))
SHA0 = AP5["um_py_novo"]["sha16"]
CM5 = json.load(open(os.path.join(V5, "CANDIDATO_v385.json"), encoding="utf-8"))
assert CM5["sha16"] == SHA0 == "d406ae5725105145", (CM5["sha16"], SHA0)
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v385 selada (%s)" % SHA0
assert len(raw) == 33386720, len(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v385", selo0.get("um_version")
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v386_runtime.py"), encoding="utf-8").read()
RT5_FIRST = open(os.path.join(V5, "v385_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT5_FIRST = open(os.path.join(V5, "artigo_pt_v385.pysnip"), encoding="utf-8").read().splitlines()[0]
EN5_FIRST = open(os.path.join(V5, "artigo_en_v385.pysnip"), encoding="utf-8").read().splitlines()[0]
KREP = json.load(open(os.path.join(K6, "sandbox_raiz_v386.json"), encoding="utf-8"))
assert KREP["sorry_warnings"] == 0 and KREP["fora_do_trio"] == {} and KREP["bandeiras_ok"] == len(KREP["bandeiras"]) == 110 and all(KREP["bandeiras"].values()), "o kernel do sandbox nao fechou"
assert KREP["n_pedra"] == 93 and KREP["n_fiacao"] == 17 and KREP["n_axiom_report"] == 10239
_log = open(os.path.join(K6, "build_full.log"), encoding="utf-8", errors="replace").read()
assert _log.count("rc_build=0") == 1 and _log.count("rc_audit=0") == 1 and "Built TGLExt.TheVerbSelectsTheAction" in _log

# ---------- (1) o kernel embutido (o molde da v383/v385) ----------
lines = T.splitlines(keepends=True)
i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
assert len(i0) == 1
i0 = i0[0]; j = i0 + 1
while lines[j].rstrip("\r\n") != "}":
    j += 1
off0 = sum(len(l) for l in lines[:i0])
blk = "".join(lines[i0:j + 1])
dnode = ast.parse(blk).body[0].value
blines = blk.splitlines(keepends=True)
bstart = [0]
for l in blines:
    bstart.append(bstart[-1] + len(l))


def charpos(lineno, col_bytes):
    l = blines[lineno - 1]
    return bstart[lineno - 1] + len(l.encode("utf-8")[:col_bytes].decode("utf-8"))


old_d = ast.literal_eval(blk.split("=", 1)[1].strip())
spans = {ast.literal_eval(k): (charpos(v.lineno, v.col_offset), charpos(v.end_lineno, v.end_col_offset)) for k, v in zip(dnode.keys, dnode.values)}
IGNORADOS_DO_SANDBOX = {"TGL/AuditVerb_tmp.lean"}   # auditoria temporaria da fase A (sandbox), nao importada por ninguem: NAO e' kernel
cand = {}
for top in ("TGL", "TGLExt"):
    for root, dirs, files in os.walk(os.path.join(KS, top)):
        for f in files:
            if f.endswith(".lean"):
                p = os.path.join(root, f); rel = os.path.relpath(p, KS).replace("\\", "/")
                if rel in IGNORADOS_DO_SANDBOX:
                    continue
                cand[rel] = open(p, "r", encoding="utf-8", newline="").read()
for f in ("TGL.lean", "TGLExt.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain"):
    if os.path.exists(os.path.join(KS, f)):
        cand[f] = open(os.path.join(KS, f), "r", encoding="utf-8", newline="").read()
for k in old_d:
    if k not in cand and not k.endswith(".lean"):
        cand[k] = old_d[k]
assert [k for k in old_d if k not in cand] == []
for ig in IGNORADOS_DO_SANDBOX:
    assert ig not in old_d
    mod = ig[:-5].replace("/", ".")
    for k, v in cand.items():
        assert ("import " + mod) not in v, (ig, "importado por", k)
changed = sorted(k for k in old_d if cand[k] != old_d[k])
new = sorted(k for k in cand if k not in old_d)
assert set(changed) == {"TGLExt.lean", "TGL/Audit.lean"}, changed
assert new == ["TGLExt/TheVerbSelectsTheAction.lean"], new
for k in new:
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", cand[k], flags=re.S)), k
# os dois arquivos embutidos na v385 sao BYTE A BYTE os .bak do sandbox (o estado que a fase A tocou)
for k, bak in (("TGLExt.lean", "TGLExt.lean.bak_antes_v386_20261005_154417"), ("TGL/Audit.lean", "TGL/Audit.lean.bak_antes_v386_20261005_154417")):
    bb = open(os.path.join(KS, *bak.split("/")), "r", encoding="utf-8", newline="").read()
    assert bb == old_d[k], "o %s embutido na v385 nao e' byte a byte o .bak do sandbox" % k
# a mudanca dos dois arquivos e' SO acrescimo: a raiz ganha o import no fim; a auditoria ganha o bloco v386 no fim
assert cand["TGLExt.lean"] == old_d["TGLExt.lean"].rstrip("\n") + "\nimport TGLExt.TheVerbSelectsTheAction\n"
_bloco = open(os.path.join(K6, "AUDIT_BLOCO_v386.lean"), "r", encoding="utf-8", newline="").read()
assert cand["TGL/Audit.lean"] == old_d["TGL/Audit.lean"].rstrip("\n") + "\n" + _bloco and _bloco.count("#print axioms ") == 110
# a pedra embutida e' EXATAMENTE a que o build/auditoria do sandbox compilou: sha256 LIDO de kernel/PEDRA_v386_pos_build.json (gravado por script DEPOIS do build,
# com o sha256 do build_full.log que a auditou) -- nunca digitado aqui
_PED = json.load(open(os.path.join(K6, "PEDRA_v386_pos_build.json"), encoding="utf-8"))
_pb = cand["TGLExt/TheVerbSelectsTheAction.lean"].encode("utf-8")
assert sha256(_pb) == _PED["sha256"] and len(_pb) == _PED["bytes"], "a pedra do sandbox nao e' a que o build auditou (PEDRA_v386_pos_build.json)"
assert sha256(open(os.path.join(K6, "build_full.log"), "rb").read()) == _PED["build_log_sha256"], "o build_full.log nao e' o que auditou esta pedra"
assert sha256(cand["TGLExt.lean"].encode("utf-8")) == _PED["TGLExt_lean_sha256"] and sha256(cand["TGL/Audit.lean"].encode("utf-8")) == _PED["Audit_lean_sha256"]
nb = blk
for k in sorted(changed, key=lambda k: -spans[k][0]):
    a, b = spans[k]
    nb = nb[:a] + repr(cand[k]) + nb[b:]
fim = nb.rstrip("\r\n")
assert fim.endswith("}")
nb = fim[:-1] + "".join("    %r: %s,%s" % (k, repr(cand[k]), CRLF) for k in new) + "}" + nb[len(fim):]
T = T[:off0] + nb + T[off0 + len(blk):]
assert ast.literal_eval(nb.split("=", 1)[1].strip()) == cand
KERNEL_MANIFEST = {"changed": {k: [sha16(old_d[k].encode()), sha16(cand[k].encode())] for k in changed},
                   "new": {k: sha16(cand[k].encode()) for k in new}, "n_entries": len(cand), "ignorados_do_sandbox": sorted(IGNORADOS_DO_SANDBOX)}

# ---------- (2) os PINOS, lidos dos artefatos ----------
NOMES = json.load(open(os.path.join(K6, "AUDIT_NOMES_v386.json"), encoding="utf-8"))
_fl = open(os.path.join(K6, "v386_flags.py"), encoding="utf-8").read()
_ns = {}
exec(compile("\n".join(l for l in _fl.splitlines() if l.startswith(("_VRB_FLAGS_V386", "_ANG_FLAGS_V386", "]")) or l.startswith("    \"ext_")), "<flags>", "exec"), _ns)
VRB = list(_ns["_VRB_FLAGS_V386"]); ANG = list(_ns["_ANG_FLAGS_V386"])
FLAGS = list(zip(VRB, NOMES["TheVerbSelectsTheAction"])) + list(zip(ANG, NOMES["AngularWiring"]))
assert len(VRB) == len(NOMES["TheVerbSelectsTheAction"]) == 93 and len(ANG) == len(NOMES["AngularWiring"]) == 17 and len(FLAGS) == 110 and len({f for f, _ in FLAGS}) == 110
for f, nm in FLAGS:   # a bandeira e' o nome EXATO da declaracao, posicao a posicao
    pfx = "ext_vrb_" if f.startswith("ext_vrb_") else "ext_ang_"
    assert f.replace(pfx, "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
    assert f not in T, f
    assert KREP["bandeiras"].get(f) is True, f
    assert nm in KREP["axiomas_novas"] and set(KREP["axiomas_novas"][nm]) <= {"propext", "Classical.choice", "Quot.sound"}, nm
    assert ("#print axioms " + nm + "\n") in _bloco, nm
    assert (("theorem " + nm.split(".")[-1]) in cand["TGLExt/TheVerbSelectsTheAction.lean"] or ("def " + nm.split(".")[-1]) in cand["TGLExt/TheVerbSelectsTheAction.lean"]
            or ("inductive " + nm.split(".")[-1]) in cand["TGLExt/TheVerbSelectsTheAction.lean"]) if f.startswith("ext_vrb_") else True, nm
# o token, LIDO da pedra
_mtok = re.search(r'def verbTypingStoneName : String :=\s*"([A-Z0-9_]+)"', cand["TGLExt/TheVerbSelectsTheAction.lean"])
assert _mtok, "verbTypingStoneName nao achado na pedra"
TOKEN = _mtok.group(1)
assert TOKEN.startswith("THE_VERB_SELECTS_THE_ACTION__") and TOKEN.endswith("__GATE_UNTOUCHED") and not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", TOKEN)
# os 4 arquivos do operador, por sha256 (os sha16 da tarefa conferidos) e os carimbos LIDOS do transcrito
ESPEC = json.load(open(os.path.join(V6, "ramo_b", "ESPEC_RUNTIME_RAMO_B_v386.json"), encoding="utf-8"))
_V1J = json.load(open(ESPEC["preregistro_V1"]["arquivos"]["json"]["path"], encoding="utf-8"))
# o RESPOSTAS json recebeu, DEPOIS do congelamento do V1, a errata [sic] na leitura da gerencia ("tudo agora" -> «tudo agroa» [sic], o verbatim do operador): o V1
# registra o sha256 da versao ANTERIOR; o sha256 de agora e' lido do disco, e o backup de BYTES da versao que o V1 registrou tem de existir e bater (errata AO LADO)
_RESP_JSON_SHA_NO_V1 = _V1J["ratificacao"]["sha256_json"]
_files = {"verbo_20261005_1653": (os.path.join(V6, "VERBO_operador_05out.txt"), "5973d79a49995c4c"),
          "ramo_b_decision_20261005_1711": (os.path.join(V6, "ramo_b", "DECISAO_OPERADOR_RAMO_B_05out.json"), ESPEC["livro_de_cobrancas"]["errata_ao_lado_de_R6"]["sha256"][:16]),
          "respostas_20261005_1829": (os.path.join(V6, "RESPOSTAS_operador_05out.txt"), "b49b0d9e60ee4646"),
          "respostas_json_20261005_1829": (os.path.join(V6, "RESPOSTAS_operador_05out.json"), None)}
FILES = {}
for k, (p, s16) in _files.items():
    b = open(p, "rb").read()
    assert s16 is None or sha16(b) == s16, (k, sha16(b), s16)
    FILES[k] = {"path": p.replace("\\", "/"), "sha256": sha256(b), "bytes": len(b), "text": b.decode("utf-8")}
DEC = json.loads(FILES["ramo_b_decision_20261005_1711"]["text"]); RESPJ = json.loads(FILES["respostas_json_20261005_1829"]["text"])
assert RESPJ["verbatim_inteiro"] == FILES["respostas_20261005_1829"]["text"] and RESPJ["sha256_txt"] == FILES["respostas_20261005_1829"]["sha256"]
assert DEC["verbatim"].startswith("eu não havia proibido o ramo B") and RESPJ["trechos"]["delegacao"] == "o resto vc consegue responder tudo agroa"
assert "tudo agora" not in FILES["respostas_json_20261005_1829"]["text"] and "«o resto vc consegue responder tudo agroa» [sic]" in RESPJ["leituras_da_gerencia"]["delegacao"], "a errata [sic] do RESPOSTAS json nao esta aplicada"
_bak_v1 = sorted(f for f in os.listdir(V6) if f.startswith("RESPOSTAS_operador_05out.json.bak_") and sha256(open(os.path.join(V6, f), "rb").read()) == _RESP_JSON_SHA_NO_V1)
assert _bak_v1, "o backup de bytes do RESPOSTAS json com o sha256 que o V1 congelado registrou (%s) nao foi achado" % _RESP_JSON_SHA_NO_V1[:16]
assert FILES["respostas_json_20261005_1829"]["sha256"] != _RESP_JSON_SHA_NO_V1
FILES["respostas_json_20261005_1829"]["errata_ao_lado"] = {"sha256_registrado_no_V1_congelado": _RESP_JSON_SHA_NO_V1, "backup_bytes_dessa_versao": _bak_v1[0],
    "o_que_mudou": "leituras_da_gerencia.delegacao: \"tudo agora\" (leitura da gerencia, nao verbatim) -> «tudo agroa» [sic] (o verbatim do operador: RESPOSTAS txt, ultima linha, 18:29:37 UTC); "
                   "verbatim_inteiro, trechos e sha256_txt intocados; o V1 (congelado por hash) registra o sha256 anterior -- errata AO LADO em ramo_b_preregistration_v386.erratas_ao_lado"}
_TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
_want = {"verbo_20261005_1653": FILES["verbo_20261005_1653"]["text"], "respostas_20261005_1829": FILES["respostas_20261005_1829"]["text"], "ramo_b_decision_20261005_1711": DEC["verbatim"]}
_ts = {}
for _ln in open(_TR, encoding="utf-8", errors="replace"):
    try:
        _d = json.loads(_ln)
    except ValueError:
        continue
    if _d.get("isCompactSummary") or _d.get("isMeta"):
        continue
    if _d.get("type") == "user":
        _c = _d.get("message", {}).get("content"); _tx = [_c] if isinstance(_c, str) else [x.get("text", "") for x in (_c or []) if isinstance(x, dict) and x.get("type") == "text"]
    elif _d.get("type") == "attachment" and (_d.get("attachment") or {}).get("type") == "queued_command":
        _pr = _d["attachment"].get("prompt"); _tx = [_pr] if isinstance(_pr, str) else [x.get("text", "") for x in (_pr or []) if isinstance(x, dict) and x.get("type") == "text"]
    else:
        continue
    for _t in _tx:
        for _k, _w in _want.items():
            if _t and (_t == _w or _t.strip() == _w):
                _ts.setdefault(_k, _d.get("timestamp"))
assert set(_ts) == set(_want), ("mensagem do operador nao achada no transcrito", sorted(set(_want) - set(_ts)))
for k in FILES:
    FILES[k]["quando_utc"] = _ts["respostas_20261005_1829"] if k == "respostas_json_20261005_1829" else _ts[k]
assert FILES["ramo_b_decision_20261005_1711"]["quando_utc"] == DEC["quando"] == ESPEC["livro_de_cobrancas"]["errata_ao_lado_de_R6"]["quando_utc"]
assert FILES["respostas_20261005_1829"]["quando_utc"] == RESPJ["quando"] == _V1J["ratificacao"]["quando_utc"]
OPERATOR_VERBATIM = {"note": "textos EMBUTIDOS dos arquivos extraidos do transcrito (lidos por sha256 pelo gerar_candidato_v386.py; os carimbos lidos do transcrito pela igualdade do texto); a cunhagem e' do operador. "
                             "o VERBO escreve a constante como α²; a régua do signo lê β_TGL = α·√e — citação, não valor",
                     "files": FILES, "delegation": RESPJ["trechos"]["delegacao"]}
# o pre-registro V1 do ramo B: cada sha256/bytes da ESPEC reconferido no disco; spec_sha256 recomputado
PRE = ESPEC["preregistro_V1"]
RB_FILES = {}
for k, f in PRE["arquivos"].items():
    b = open(f["path"], "rb").read()
    assert sha256(b) == f["sha256"] and len(b) == f["bytes"], ("o arquivo do V1 mudou", k)
    RB_FILES[k] = {"path": f["path"], "sha256": f["sha256"], "bytes": f["bytes"]}
_canon = json.dumps(_V1J["spec"], sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
assert sha256(_canon) == _V1J["spec_sha256"] == PRE["spec_sha256"] and _V1J["id"] == PRE["identificador"] == _V1J["spec"]["id"]
_H = json.load(open(RB_FILES["hashes"]["path"], encoding="utf-8"))
for nome, e_ in _H["arquivos"].items():
    b = open(e_["caminho"], "rb").read(); assert sha256(b) == e_["sha256"] and len(b) == e_["bytes"], nome
# o_que_conferir: a ESPEC dizia «|diff| < 1e-15» para o beta -- o numero corrigiu a frase (1e-9 relativo, a regra da casa); nos PINOS entra a regra IMPLEMENTADA com a errata
# dita; a ESPEC em disco fica INTACTA (a errata ao lado: ramo_b/ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json, cujo sha256 e' pinado e que pina o sha256 da ESPEC original)
_OQC = [("spec.beta.valor_runtime == beta do rito (a 1e-9 relativo; a diferenca exata fica dita) -- a ESPEC dizia |diff| < 1e-15 e o numero corrigiu a frase (errata ao lado)" if "1e-15" in x_ else x_)
        for x_ in PRE["o_que_conferir"]]
assert sum("1e-15" in x_ for x_ in PRE["o_que_conferir"]) == 1 and all("errata" in x_ for x_ in _OQC if "1e-15" in x_)
_ERRP = os.path.join(V6, "ramo_b", "ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json")
_ERRATA_ESPEC = json.load(open(_ERRP, encoding="utf-8"))
assert _ERRATA_ESPEC["espec_original"]["sha256"] == sha256(open(os.path.join(V6, "ramo_b", "ESPEC_RUNTIME_RAMO_B_v386.json"), "rb").read()), "a ESPEC mudou depois da errata (ela deve ficar intacta)"
RAMO_B_PREREG = {"identificador": PRE["identificador"], "spec_sha256": PRE["spec_sha256"], "spec_sha256_formula": PRE["spec_sha256_formula"], "pasta": PRE["pasta"],
                 "files": RB_FILES, "ler_por_hash": list(PRE["ler_por_hash"]), "conferir_tambem": list(PRE["conferir_tambem"]), "o_que_conferir": _OQC,
                 "espec_errata_ao_lado": {"arquivo": "ramo_b/ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json", "sha256": sha256(open(_ERRP, "rb").read()), "espec_original_sha256": _ERRATA_ESPEC["espec_original"]["sha256"]}}
RAMO_B_FIELDS = dict(ESPEC["registro_no_core"]["campos_a_transcrever_do_V1_json"])


def _get(o, path):
    for p in path:
        o = o[p] if isinstance(o, dict) else o[int(p)]
    return o


_PINMAP = {"hipotese_k": ["spec", "poder_cego", "hipotese", "k"], "poder_exato_A31": ["spec", "poder_cego", "hipotese", "poder_exato", "A_31_std"],
           "poder_exato_B10": ["spec", "poder_cego", "hipotese", "poder_exato", "B_GWTC3_10"], "poder_exato_C": ["spec", "poder_cego", "hipotese", "poder_exato", "C_GW250114"],
           "poder_x0p273": ["spec", "poder_cego", "hipotese", "poder_exato", "A_31_x0p273_difusao_de_fase"], "delta_pred_A31_exato": ["spec", "poder_cego", "hipotese", "delta_pred_ponderado", "exato"],
           "sigma_comb_A31": ["spec", "poder_cego", "sigma_comb_A31"], "sigma_beta_lido_A31": ["spec", "beta_lido", "sigma_dita_antes_conjunto_A31_hipotese"],
           "sigma_beta_lido_sobre_beta_A31": ["spec", "beta_lido", "sigma_sobre_beta_A31_hipotese"], "conjunto_D_n": ["spec", "conjuntos", "D", "n_elegiveis"],
           "conjunto_D_sem_hold": ["spec", "conjuntos", "D", "n_sem_pendencia_de_qualidade"], "k_em_chi_0": ["spec", "k", "em_chi_0"]}
# o pino beta_runtime_do_V1 (um float de beta nos PINOS, o unico literal de beta em codigo no um.py -- afericao de codigo, 05/10) foi RETIRADO: o spec_sha256 ja cobre
# spec.beta.valor_runtime, e o runtime o compara ao beta do rito (1e-9 relativo) e a alpha.sqrt(e) recomputado -- tres coberturas; nenhum literal de beta nos pinos
_NUMS = ESPEC["registro_no_core"]["numeros_que_o_runtime_transcreve_sem_recalcular"]
assert "beta_runtime_do_V1" in _NUMS and set(_NUMS) - {"beta_runtime_do_V1"} == set(_PINMAP), (sorted(set(_NUMS) ^ set(_PINMAP)))
RAMO_B_PINS = {}
for k, path in _PINMAP.items():
    v = _get(_V1J, path)
    assert v == _NUMS[k], ("o numero da ESPEC nao e' o do V1", k, v, _NUMS[k])
    RAMO_B_PINS[k] = {"path": path, "value": v}
# o beta do V1 veio do literal CODATA (SEALED_CODATA_ALPHA por regex) x sqrt(e); o beta do core vem do motor da identidade (o CODATA so valida): concordam a
# ~5e-13 relativo, NAO a 1e-15 absoluto como a ESPEC supunha -- o numero corrige a frase; a regua da casa para beta e' 1e-9 relativo (o livro v383)
_bv1 = float(_get(_V1J, ["spec", "beta", "valor_runtime"])); _bc = float(core0["beta"])   # lido do V1 (nao pinado): so' para dizer a diferenca aqui
assert _bv1 == _NUMS["beta_runtime_do_V1"] and _bc > 0 and abs(_bv1 / _bc - 1.0) < 1e-9 and RAMO_B_PINS["conjunto_D_n"]["value"] == 14 and len(RAMO_B_PINS) == 12, (_bv1, _bc)
BETA_V1_VS_CORE = {"beta_v1": _bv1, "beta_core_v385": _bc, "abs_diff": _bv1 - _bc, "rel_diff": _bv1 / _bc - 1.0,
                   "rule": "1e-9 relativo (a regra da casa, v383); a ESPEC dizia 1e-15 absoluto e o numero corrigiu a frase (errata ao lado: ramo_b/ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json)",
                   "pino_beta_runtime_do_V1": "RETIRADO dos pinos (coberto pelo spec_sha256 + comparacao 1e-9 rel + alpha.sqrt(e) recomputado no runtime); 12 pinos numericos ficam"}
F2B = dict(ESPEC["livro_de_cobrancas"]["cobranca_nova_F2b"])
_ER = ESPEC["livro_de_cobrancas"]["errata_ao_lado_de_R6"]
assert DEC["verbatim"] in _ER["texto_R6"] and _ER["verbatim_do_operador_17_11_36_utc"] == DEC["verbatim"]
_led0 = core0["the_ledger_of_charges_v383"]
assert _led0["all_verified"] is True and len(_led0["ledger"]) == 11 and "ENCERRADO" in _led0["corrections_beside_20261002"]["R6"]
R6_ERRATA = {"texto_R6": _ER["texto_R6"], "texto_F2": _ER["texto_F2"], "quando_utc": _ER["quando_utc"], "sha256_decisao": _ER["sha256"],
             "R6_v383_corrections_beside": _led0["corrections_beside_20261002"]["R6"], "R6_v383_readings_ratified": _led0["readings_ratified_20261002"]["R6"],
             "delegacao_verbatim": _ER["delegacao_verbatim_18_29_37_utc"], "delegacao_quando_utc": _ER["delegacao_quando_utc"], "delegacao_sha256_txt": _ER["delegacao_sha256_txt"]}
assert R6_ERRATA["sha256_decisao"] == FILES["ramo_b_decision_20261005_1711"]["sha256"] and R6_ERRATA["delegacao_sha256_txt"] == FILES["respostas_20261005_1829"]["sha256"]
_qp0 = core0["quantum_pillar_v384"]; _rp0 = core0["quantum_pillar_reproducibility_v385"]
assert _qp0["mode"] == "COMPUTE" and _qp0["all_verified"] is True and _qp0["result_sha256"] and _rp0["compared"] is True
QP_V385 = {"key": _qp0["key"], "result_sha256": _qp0["result_sha256"], "verdict": _qp0["verdict"], "run_id": _qp0["run_id"], "finished": _qp0.get("finished"),
           "reproducibility_verdict_v385": _rp0["verdict"], "reproducibility_n_fields_v385": _rp0.get("n_fields"), "note": "lidos do core SELADO da v385 (um_absoluto.json do Nos) pelo gerador"}
_cdir = (_qp0.get("reuse") or {}).get("saved_to_cache")
assert _cdir and sha256(open(os.path.join(_cdir, "result.json"), "rb").read()) == QP_V385["result_sha256"], "o cache do pilar nao guarda o resultado da v385 selada"
PINS = ("# ====================== v386 (05/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v386.py), nunca digitados ======================\n"
        "# as 110 bandeiras (93 da pedra TGLExt/TheVerbSelectsTheAction.lean + 17 da fiacao angular, no Audit.lean do kernel); o token lido da def\n"
        "# verbTypingStoneName da pedra; os 4 arquivos do operador EMBUTIDOS como texto com o sha256 e o carimbo (lido do transcrito); o pre-registro V1 do\n"
        "# ramo B (caminhos, sha256, bytes; spec_sha256); os numeros do poder pinados (do V1); a cobranca F2b e as erratas de R6/F2; os textos R6 da v383 e os\n"
        "# pinos do pilar lidos do core SELADO da v385. c = beta_TGL e' [INPUT]; beta nunca literal; o gate nao se move.\n"
        "_VRB_FLAGS_V386 = [\n" + "".join("    %r,\n" % f for f in VRB) + "]\n"
        "_ANG_FLAGS_V386 = [\n" + "".join("    %r,\n" % f for f in ANG) + "]\n"
        "_VERB_TOKEN_V386 = %r\n" % TOKEN
        + "_V386_OPERATOR_VERBATIM = " + pprint.pformat(OPERATOR_VERBATIM, width=150, sort_dicts=False) + "\n"
        + "_V386_RAMO_B_PREREG = " + pprint.pformat(RAMO_B_PREREG, width=150, sort_dicts=False) + "\n"
        + "_V386_RAMO_B_FIELDS = " + pprint.pformat(RAMO_B_FIELDS, width=150, sort_dicts=False) + "\n"
        + "_V386_RAMO_B_PINS = " + pprint.pformat(RAMO_B_PINS, width=150, sort_dicts=False) + "\n"
        + "_V386_F2B = " + pprint.pformat(F2B, width=150, sort_dicts=False) + "\n"
        + "_V386_R6_ERRATA = " + pprint.pformat(R6_ERRATA, width=150, sort_dicts=False) + "\n"
        + "_V386_QP_V385 = " + pprint.pformat(QP_V385, width=150, sort_dicts=False) + "\n")
_pins_ns = {}
exec(compile(PINS, "<pins>", "exec"), _pins_ns)
assert _pins_ns["_V386_OPERATOR_VERBATIM"] == OPERATOR_VERBATIM and _pins_ns["_V386_RAMO_B_PINS"] == RAMO_B_PINS and _pins_ns["_V386_F2B"] == F2B and _pins_ns["_V386_RAMO_B_PREREG"] == RAMO_B_PREREG
assert _pins_ns["_V386_R6_ERRATA"] == R6_ERRATA and _pins_ns["_V386_QP_V385"] == QP_V385 and _pins_ns["_V386_RAMO_B_FIELDS"] == RAMO_B_FIELDS and _pins_ns["_VERB_TOKEN_V386"] == TOKEN
assert _pins_ns["_VRB_FLAGS_V386"] == VRB and _pins_ns["_ANG_FLAGS_V386"] == ANG
_pp = os.path.join(HERE, "v386_pins.py")
open(_pp + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); assert os.path.getsize(_pp + ".tmp") > 20000; os.replace(_pp + ".tmp", _pp)
RT = PINS.rstrip("\n") + "\n\n\n" + RT_LOGIC
ast.parse(RT)
# «alpha ao quadrado» proibido na LOGICA e nos pinos que nao sao citacao; os textos VERBATIM do operador ficam como ele escreveu (citacao, nao signo da casa)
_sem_verbatim = PINS[:PINS.index("_V386_OPERATOR_VERBATIM = ")] + PINS[PINS.index("_V386_RAMO_B_PREREG = "):] + RT_LOGIC
assert not re.search(r"α²|α\^2|alpha\^2|alpha²", _sem_verbatim), "alpha ao quadrado fora de citacao"
# a palavra proibida: na LOGICA e nos pinos que nao sao citacao (os arquivos embutidos do operador/da gerencia sao citacao por hash: la a palavra aparece
# em frases de proibicao -- «vereditos permitidos sem CONFIRMED» -- e a guarda do rito age sobre os VEREDITOS do core, nao sobre os textos embutidos)
assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", _sem_verbatim.replace('"CONF" + "IRMED', "").replace('"TGL_PRO" + "VED"', "").replace('PRO" + "VED_BY', ""))
_hits_verbatim = [(k, m_.group(0)) for k, f_ in FILES.items() for m_ in re.finditer(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", f_["text"])]
print("palavra proibida nos textos embutidos (citacao; frases de proibicao):", _hits_verbatim)

# ---------- (3) os patches ----------
patches = []


def add(pid, grupo, old, new_, selo):
    global T
    assert T.count(old) == 1, (pid, T.count(old))
    T = T.replace(old, new_)
    patches.append({"id": pid, "grupo": grupo, "old": old, "new": new_, "o_que_muda": selo})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(prefixo_regex):
    m = re.search(prefixo_regex + r"[^\r\n]*\r\n", T, re.M)
    assert m and T.count(m.group(0)) == 1, prefixo_regex
    return m.group(0)


A01 = '    "ext_dks_the_iald_selector_separates_the_sectors_kernel_proved": "TGLExt.the_iald_selector_separates_the_sectors",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v386 (05/10/2026; o Verbo seleciona -- o Nome e' o posto; e a fiacao do regime angular na escada): vrb (%d) + ang (%d)" % (len(VRB), len(ANG)) + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d (ext_vrb_ %d, ext_ang_ %d)." % (len(FLAGS), len(VRB), len(ANG)))
A02 = '        "ext_dks_the_iald_selector_separates_the_sectors_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v386: o Verbo seleciona (%d) + a fiacao angular (%d)" % (len(VRB), len(ANG)) + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v385", "TheAxiomAndTheFalseWitness", "TGLExt/TheAxiomAndTheFalseWitness.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v386 (05/10/2026): o Verbo seleciona a acao -- o Nome e' o posto (a projecao de posto 1); select = o Verbo em ato; a leitura e' um peso; a ordem importa; a triade com c = beta_TGL [INPUT]; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis; + a fiacao angular (17) na escada" + CRLF
    + '    ("v386", "TheVerbSelectsTheAction", "TGLExt/TheVerbSelectsTheAction.lean", None, None),' + CRLF, "ledger de pedras: +1 (TheVerbSelectsTheAction).")
patches.append({"id": "V04_kernel", "grupo": "G_PEDRAS", "old": "(_EMBEDDED_KERNEL_FILES: TGLExt.lean e TGL/Audit.lean da v385)", "new": "(+ TGLExt/TheVerbSelectsTheAction.lean; TGLExt.lean e TGL/Audit.lean do sandbox)",
                "o_que_muda": "kernel embutido: +1 pedra (TheVerbSelectsTheAction); TGLExt.lean (+1 import) e TGL/Audit.lean (+110 #print axioms) trocados pelos do sandbox, conferidos byte a byte contra os .bak antes; TGL/AuditVerb_tmp.lean do sandbox NAO entra."})
m = re.search(r'^UM_VERSION = "v385"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v385"') == 1
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v386"   # v386 (05/10/2026): a CONSTANTE UNICA de versao -- o Verbo seleciona (o Nome e\' o posto); o ramo B reaberto por pre-registro (V1 por hash); a errata ao lado de R6; o pilar reaproveitado da v385 pela chave; v385 em 05/10' + CRLF,
    "UM_VERSION = 'v386'.")
assert T.count(RT5_FIRST) == 1
add("W02_runtime", "G_RUNTIME", RT5_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT5_FIRST,
    "runtime v386: os pinos (110 bandeiras; o token lido da pedra; os 4 verbatins por sha256; o V1 do ramo B por hash; as erratas; os pinos do pilar v385) + a logica (the_verb_v386, quantum_pillar_reuse_v386, ramo_b_preregistration_v386, ledger_errata_v386; _QP_REUSE_V386).")
A3a = "        if _RITE_CKPT_ON:" + CRLF + "            cached = _qp_cached_ok(cdir)" + CRLF
add("W03a_pilar_reuse_start", "G_RUNTIME", A3a, "        if _RITE_CKPT_ON or _QP_REUSE_V386:   # v386: o pilar nao e' objeto desta versao -- reaproveita pela chave (sha256 + ambiente + motor) tambem sem TGL_RITE_CHECKPOINT; senao calcula (dito)" + CRLF + "            cached = _qp_cached_ok(cdir)" + CRLF,
    "quantum_pillar_start_v384: o reaproveitamento pela chave tambem sob _QP_REUSE_V386 (a decisao da v386: o pilar nao roda de novo).")
A3b = '                    print("[v384] pilar quantico: REAPROVEITADO da rodada de %s (chave %s) -- a versao FINAL roda sem TGL_RITE_CHECKPOINT" % (cached.get("finished"), key), flush=True)' + CRLF
add("W03b_pilar_reuse_print", "G_RUNTIME", A3b, '                    print(("[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de %s (chave %s) -- o pilar nao e\' objeto desta versao (_QP_REUSE_V386)" if (_QP_REUSE_V386 and not _RITE_CKPT_ON)'
    + ' else "[v384] pilar quantico: REAPROVEITADO da rodada de %s (chave %s) -- a versao FINAL roda sem TGL_RITE_CHECKPOINT") % (cached.get("finished"), key), flush=True)' + CRLF,
    "o anuncio do reaproveitamento diz v386 quando e' pela chave da v386.")
A3c = '                            "reading": "RODADA_INTERMEDIARIA__PILAR_QUANTICO_REAPROVEITADO__A_VERSAO_FINAL_RODA_SEM_A_CHAVE"}' + CRLF
add("W03c_pilar_reuse_reading", "G_RUNTIME", A3c, '                            "reading": ("V386__PILAR_QUANTICO_REAPROVEITADO_DA_RODADA_SELADA_V385_PELA_CHAVE__O_PILAR_NAO_E_OBJETO_DESTA_VERSAO" if (_QP_REUSE_V386 and not _RITE_CKPT_ON)'
    + ' else "RODADA_INTERMEDIARIA__PILAR_QUANTICO_REAPROVEITADO__A_VERSAO_FINAL_RODA_SEM_A_CHAVE")}' + CRLF,
    "quantum_pillar_v384.reuse.reading diz v386 (nao «rodada intermediaria») quando o reuse e' pela chave da v386.")
A05 = linha_unica(r'^    print\("   \[v385\] o Axioma e a testemunha falsa')
reg = ['    try:   # v386: o pilar quantico desta rodada -- reaproveitado da rodada selada v385 pela chave (sha256 conferido) ou calculado de novo (dito); nunca derruba o rito',
       '        core["quantum_pillar_reuse_v386"] = quantum_pillar_reuse_v386(_QP_ST_V384, core["quantum_pillar_v384"])   # v386: o pilar nao e\' objeto desta versao [COMPUTED]',
       '    except Exception as _e386:',
       '        core["quantum_pillar_reuse_v386"] = {"verdict": "TGL_QUANTUM_PILLAR_REUSE_V386__NOT_RECORDED__RUNTIME_ERROR__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}',
       '    print("   [v386] o pilar quantico nesta rodada (reaproveitado da v385 pela chave, ou calculado de novo -- dito): %s" % core["quantum_pillar_reuse_v386"]["verdict"])',
       '    try:   # v386: uma excecao aqui vira o Verbo NAO selado, dito (all_verified False: vai ao balde dos nao selados)',
       '        core["the_verb_v386"] = the_verb_v386(core)   # v386: o Verbo seleciona -- as 93 declaracoes da pedra e os 17 da fiacao angular verificados pelo kernel desta rodada; o token lido do kernel; os verbatins por sha256',
       '    except Exception as _e386:',
       '        core["the_verb_v386"] = {"verdict": "TGL_THE_VERB_V386__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}',
       '    print("   [v386] o Verbo seleciona (o Nome e\' o posto; a leitura e\' um peso; a ordem importa; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis; a fiacao angular na escada): %s" % core["the_verb_v386"]["verdict"])',
       '    try:   # v386: o pre-registro V1 do ramo B lido por hash -- falha de hash e\' AVISO visivel (V1_NOT_READ), nunca ok falso',
       '        core["ramo_b_preregistration_v386"] = ramo_b_preregistration_v386(core)   # v386: OUTRA LEI (tau* = k.G.M_f/c^3), canal F2b; so o conjunto D testa; nada aberto [INPUT por hash]',
       '    except Exception as _e386:',
       '        core["ramo_b_preregistration_v386"] = {"verdict": "TGL_RAMO_B_PREREGISTERED_V386__V1_NOT_READ__RUNTIME_ERROR__AWAITING_PREREGISTRATION__NOTHING_OPENED__GATE_UNTOUCHED", "all_verified": False, "read_ok": False, "error": repr(_e386)[:400], "does_not_gate_core": True}',
       '    print("   [v386] o ramo B do ringdown pre-registrado por hash (outra lei, canal F2b; o conjunto D cego; nada aberto): %s" % core["ramo_b_preregistration_v386"]["verdict"])',
       '    try:   # v386: a errata AO LADO de R6 (ENCERRADO -> REABERTO POR PRE-REGISTRO) e a cobranca F2b; o livro v383 fica intacto',
       '        core["ledger_errata_v386"] = ledger_errata_v386(core, core["ramo_b_preregistration_v386"])   # v386: a errata ao lado, com o verbatim do operador de 17:11:36 UTC por sha256',
       '    except Exception as _e386:',
       '        core["ledger_errata_v386"] = {"verdict": "TGL_LEDGER_ERRATA_V386__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}',
       '    print("   [v386] a errata ao lado de R6 e a cobranca F2b (o livro v383 intacto): %s" % core["ledger_errata_v386"]["verdict"])']
add("W04_registro", "G_RUNTIME", A05, A05 + CRLF.join(reg) + CRLF, "core: +4 chaves v386 (depois do registro da v385, que fica intocado; antes do artigo).")
pt = open(os.path.join(HERE, "artigo_pt_v386.pysnip"), encoding="utf-8").read()
A06 = PT5_FIRST + CRLF
add("W05_artigo_PT", "G_ARTIGO", A06, crlf(pt.rstrip("\n") + "\n") + A06, "artigo PT: «Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro», antes do trecho da v385.")
en = open(os.path.join(HERE, "artigo_en_v386.pysnip"), encoding="utf-8").read()
A07 = EN5_FIRST + CRLF
add("W06_artigo_EN", "G_ARTIGO", A07, crlf(en.rstrip("\n") + "\n") + A07, "artigo EN: «Beside (v386): the Verb selects; branch B reopened by preregistration», before the v385 text.")
for _snip in (pt, en):
    assert not re.search(r"α²|α\^2|alpha\^2|alpha²|\\alpha\^2", _snip) and not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", _snip)
A08 = linha_unica(r'^ {12}"quantum_pillar_reproducibility_v385": \{k_: ')
add("W07_selo", "G_SELO", A08, A08 + "            # v386 (05/10/2026) -- O VERBO SELECIONA; o ramo B reaberto por pre-registro (V1 por hash); a errata ao lado de R6; o pilar reaproveitado da v385: registros proprios AO LADO do gate; nenhum valor do gate muda" + CRLF
    + '            "the_verb_reading_v386": "OPERATOR_COINAGES_2026_10_05__VERB_EQ_SELECTION_OF_THE_ACTION__THE_VERB_SELECTS_NAME_TIME_AND_TRUTH__THE_NAME_IS_THE_POST_NOT_ONTOLOGY_THE_PLACE_WHERE_THE_INSCRIPTION_DWELLS__'
    + 'TRUTH_AND_COST_TWO_FACES_OF_ONE_OBJECT_THE_COST_IS_JUSSIVE_TO_THE_TRUTH__TIME_IS_ONE_FLOW_READ_TWICE_C_CUBED_AS_THE_RETURN_PHASE_SECOND_READING__LIGHT_PRECEDES_GRAVITY_IN_READING_INSEPARABLE__'
    + 'LAGRANGIAN_FULL_AGREEMENT_TYPED_FACE_IS_ONE__ITEMS_6_TO_17_DECIDED_BY_DELEGATION__BRANCH_B_NOT_FORBIDDEN_CRITERIA_WERE_MISSING_REOPENED_BY_PREREGISTRATION_OTHER_LAW_OWN_CHANNEL__'
    + 'TYPED_TheVerbSelectsTheAction_BY_TERM_C_IS_INPUT_NEVER_LITERAL__ANGULAR_WIRING_ON_THE_LADDER__PILLAR_REUSED_FROM_V385_BY_KEY_NOT_THE_OBJECT__THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING__'
    + 'READINGS_ARE_INPUT_ONTO__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF
    + '            "verb_typing_stone_name_v386": (core.get("the_verb_v386") or {}).get("token_from_kernel"),' + CRLF
    + '            "the_verb_v386": {k_: (core.get("the_verb_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "vrb_ok", "vrb_total", "ang_ok", "ang_total", "missing_flags", "token", "token_from_kernel", "token_matches_kernel", "verbatim_hashes_ok", "verbatim_files", "delegation", "stone")},' + CRLF
    + '            "ledger_errata_v386": {k_: (core.get("ledger_errata_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "v383_ledger_intact", "v383_n_charges", "R6_v383_beside_20261002", "corrections_beside_20261005", "operator_decision_20261005", "delegation_20261005", "charge_F2b", "F2_untouched", "R2_untouched")},' + CRLF
    + '            "ramo_b_preregistration_v386": {k_: (core.get("ramo_b_preregistration_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "sha256_expected", "sha256_read", "bytes_read", "hashes_file_ok", "beta", "beta_ok", "pins", "pins_ok", "recompute_ok", "conjunto_D_n", "F2b_status", "F2b_qualifier", "veredito_do_V1", "token_estado", "nothing_opened", "no_central_value_in_spec_or_D", "central_values_transcribed_from_sealed_registry_NOT_BLIND", "erratas_ao_lado", "errors")},' + CRLF
    + '            "quantum_pillar_reuse_v386": {k_: (core.get("quantum_pillar_reuse_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "reused", "mode", "key", "result_sha256", "result_sha256_matches_v385_sealed", "verdict_same_as_v385_sealed", "key_same_as_v385", "custody_chain_ok", "switch_reuse_v386", "rite_checkpoint_switch", "pinned_v385", "reuse_refused_detail")},' + CRLF,
    "selo: +1 leitura, +1 token (lido do kernel) e +4 registros (the_verb_v386, ledger_errata_v386, ramo_b_preregistration_v386, quantum_pillar_reuse_v386), ao lado do gate.")
A09 = linha_unica(r'^    md\.append\("> \*\*Errata ao lado \(v385, 05/10/2026, o operador\):\*\*')
add("W08_md_errata_R6", "G_ARTIGO", A09, A09 + '    md.append("> **Errata ao lado (v386, 05/10/2026, o operador):** no livro de cobranças da v383 (intacto como registro) a leitura R6 dizia «o ramo B segue ENCERRADO»; pela decisão do operador de 05/10/2026 17:11:36 UTC '
    + '(«eu não havia proibido o ramo B, acontece que naquela ocasião ainda não tínhamos todos os críterios para prosseguir …»), o ramo B do ringdown passa a **REABERTO POR PRÉ-REGISTRO** — outra lei (τ★ = k·G·M_f/c³, k = 2π/κ̂(χ_f)), canal próprio F2b (face), '
    + 'V1 lido por hash (`ramo_b_preregistration_v386`), nada aberto, estado AWAITING_DATA; F2 e R2 intocados; a chave de 02/10 não se revoga. O Verbo tipado: o Nome é o **posto** (`the_verb_v386`). O pilar quântico não é objeto da v386: reaproveitado da v385 pela chave (`quantum_pillar_reuse_v386`). O gate não muda.\\n\\n")' + CRLF,
    "md canonico: a errata ao lado de R6 (ENCERRADO -> REABERTO POR PRE-REGISTRO), logo abaixo da errata da v385.")
# W10 -- ORDEM DO OPERADOR (05/10/2026, tarde): o teste em tempo real na GPU na APRESENTACAO, no resumo, nas palavras-chave e no sumario (PT e EN). O modulo
# patch_W10_gpu_apresentacao_v386.py (testado contra o um.py v385: 14 trocas, ast ok) e' aplicado DEPOIS do ultimo patch; respeita o CRLF; cada troca e' unica (assert)
sys.path.insert(0, V6)
import patch_W10_gpu_apresentacao_v386 as _W10   # noqa: E402
_T_antes_W10 = T
T, _rel10 = _W10.aplicar(T)
assert len(_rel10) == 14 and T != _T_antes_W10 and [n_ for n_, _ in _rel10] == [p_[0] for p_ in _W10.PATCHES]
for _nome, _delta in _rel10:
    patches.append({"id": _nome, "grupo": "G_ARTIGO", "old": "(patch_W10_gpu_apresentacao_v386.py)", "new": "(%+d chars)" % _delta,
                    "o_que_muda": "W10 (ordem do operador 05/10): o teste em tempo real na GPU na apresentacao / resumo / palavras-chave / sumario -- %s" % _nome})
_W10_SHA = sha256(open(os.path.join(V6, "patch_W10_gpu_apresentacao_v386.py"), "rb").read())
assert T.count("def the_verb_v386(") == 1 and T.count("def ramo_b_preregistration_v386(") == 1 and T.count("def ledger_errata_v386(") == 1 and T.count("def quantum_pillar_reuse_v386(") == 1
for f, _ in FLAGS:
    assert T.count('"%s"' % f) == 2 and T.count("'%s'" % f) == 1, (f, T.count('"%s"' % f), T.count("'%s'" % f))   # o dicionario e a escada (aspas duplas); os pinos (repr, aspas simples)
assert T.count('_QP_PREV_V385 = quantum_pillar_previous_v385(_QP_ST_V384)') == 1 and T.count('core["the_axiom_v385"] = the_axiom_v385(core)') == 1   # o registro da v385 INTOCADO
b = T.encode("utf-8")
ast.parse(T)
h16 = sha16(b)
out = os.path.join(HERE, "um_v386_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
_C385 = core0["external_ladder"]
_E385 = int(_C385["n_theorems_expected"]); assert int(_C385["n_theorems_clean"]) == _E385 == 6027
man = {"candidato": out, "sha16": h16, "bytes": len(b), "base_v385_sha16": SHA0, "base_v385_bytes": len(raw), "kernel": KERNEL_MANIFEST, "escada": [_E385, _E385 + len(FLAGS)],
       "pedra_sha16": KERNEL_MANIFEST["new"]["TGLExt/TheVerbSelectsTheAction.lean"], "token_lido_da_pedra": TOKEN,
       "ordem_do_operador": {k: {"quando_utc": v["quando_utc"], "sha256": v["sha256"], "bytes": v["bytes"], "arquivo": v["path"], "lido_por": "gerar_candidato_v386.py (texto igual ao da mensagem no transcrito; sha256 do arquivo)"} for k, v in FILES.items()},
       "delegacao": OPERATOR_VERBATIM["delegation"], "pins_module": _pp, "pins_sha16": sha16(PINS.encode("utf-8")),
       "ramo_b_V1": {"identificador": RAMO_B_PREREG["identificador"], "spec_sha256": RAMO_B_PREREG["spec_sha256"], "files": {k: v["sha256"] for k, v in RB_FILES.items()}},
       "pilar_v385_pinado": {k: QP_V385[k] for k in ("key", "result_sha256", "run_id", "reproducibility_verdict_v385")}, "beta_v1_vs_core": BETA_V1_VS_CORE,
       "pedra_pos_build": {k: _PED[k] for k in ("sha256", "bytes", "linhas", "build_log_sha256", "build_inicio", "build_fim", "n_axiom_report", "bandeiras_ok", "sorry")},
       "respostas_json_errata_ao_lado": FILES["respostas_json_20261005_1829"]["errata_ao_lado"], "espec_errata_ao_lado": RAMO_B_PREREG["espec_errata_ao_lado"],
       "W10": {"modulo": "patch_W10_gpu_apresentacao_v386.py", "sha256": _W10_SHA, "trocas": _rel10},
       "patches": [{k: p[k] for k in ("id", "grupo", "o_que_muda")} for p in patches], "flags": [f for f, _ in FLAGS]}
_mp = os.path.join(HERE, "CANDIDATO_v386.json")
open(_mp + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(_mp + ".tmp", _mp)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v385_sha16", "kernel", "escada", "pedra_sha16", "pins_sha16")}, ensure_ascii=False, indent=1))
print("patches:", [p["id"] for p in patches])
