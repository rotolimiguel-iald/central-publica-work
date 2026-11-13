# -*- coding: utf-8 -*-
# [AUTORAL v411, 13/11/2026, claude-construtor-r36 (a servico da gerencia c1)] o COMPLEMENTO R3.6 do recibo do kernel da v411: o contrato KERNEL_RECIBO_R3_6 (versao SEM pedra nova) por MEDICAO, sem build e sem Audit
"""complementar_recibo_kernel_v411_r36.py -- parte do kernel\\KERNEL_RECIBO_v411.json (contrato KERNEL_RECIBO_R3_2, gerado por pos_build_kernel_v411.py e complementado por complementar_recibo_kernel_v411.py) e o leva ao
contrato KERNEL_RECIBO_R3_6 (R3_6\\sincronizar_bancada.py): o recibo da versao SEM pedra nova. O ensaio do B(n) da v411 (13/11/2026) parou no T17 porque a R3.5 nao tem caminho para uma versao sem modulo Lean novo
(pedras vazias, sem job do lake da raiz, sem o ANTES do kernel). NADA aqui refaz build nem Audit: so' MEDE e acrescenta/atualiza:
  (1) contrato = KERNEL_RECIBO_R3_6 e versao_sem_pedra_nova = true (pedras segue []);
  (2) formal_files_antes = o formal_files_sha256 do manifesto do kernel da v410 em custodia (base_v410\\tgl_kernel_proof_manifest.json), DEPOIS de conferir o sha256 dele contra o pino
      kernel_manifesto_anterior_v410 de PINOS_BN_v411.json;
  (3) nos_kernel_impressao = {definicao, antes, depois} com antes == depois == impressao_formal(formal_files_antes) (sha256 do JSON canonico: chaves ordenadas, separadores , e :, UTF-8, ensure_ascii=False);
      cruzada com (a) recibo_pre_selo.kernel_anterior.impressao_formal do recibo da falha do ensaio e nos.kernel.impressao_formal do recibo pre-selo pinado e (b) a impressao do formal_files_sha256 do manifesto que o Nos tem hoje (so' leitura);
  (4) toolchain.lake_version = a saida de `lake --version` MEDIDA agora, com cwd no sandbox do build (C:\\t\\k411c\\final, que tem o lean-toolchain); e' o UNICO comando lake;
  (5) arvore = C:/t/k411c/arvore (a arvore so-fontes refeita por refazer_arvore_v411_pos_selo.py: sem .lake, sem juncao) e varredura_tokens RECONTADA nela (mesmo algoritmo de contar_lean_recursivo: sem seguir juncao
      nem link; zero juncao/link) com os tokens proibidos do um.py da v410 selada re-escaneados nela;
  (6) complemento_r36: quem, quando (relogio), de onde veio cada campo; nenhum build nem Audit refeito.
O recibo NAO ganha as chaves proibidas (um_py_sha256, tgl_kernel_proof_manifest_sha256, selo_sha256). Ensaio a seco por padrao; --executar grava (backup de BYTES .bak_<AAAAMMDD_HHMMSS>_r36 ao lado; escrita por temporario +
os.replace; confere depois). Se um cruzamento ou uma medicao falhar, PARA sem gravar. uso: python -B -X utf8 complementar_recibo_kernel_v411_r36.py [--executar]"""
import datetime, hashlib, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import base_um_v410 as B  # noqa: E402
EXECUTAR = "--executar" in sys.argv[1:]
rd = lambda p: open(p, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
impressao_formal = lambda ff: sha(json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))   # a funcao da ferramenta (sincronizar_bancada.py, impressao_formal)
CONTRATO_NOVO = "KERNEL_RECIBO_R3_6"
PROIBIDAS = ("um_py_sha256", "tgl_kernel_proof_manifest_sha256", "selo_sha256")
REC_P = os.path.join(HERE, "kernel", "KERNEL_RECIBO_v411.json")
PINOS_P = os.path.join(HERE, "PINOS_BN_v411.json")
BASE_MAN_P = os.path.join(HERE, "base_v410", "tgl_kernel_proof_manifest.json")
BASE_SELO_P = os.path.join(HERE, "base_v410", "um_absoluto_selo.json")
REC10_P = os.path.join(os.path.dirname(HERE), "v410", "kernel", "KERNEL_RECIBO_v410.json")
FALHA_P = os.path.join(HERE, "bancada_B3_ensaio_20261113_023032", "RECIBO_SINCRONIZACAO_v411_20261113_023032.json")
NOS_MAN_P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel_proof_manifest.json"
SANDBOX = r"C:\t\k411c\final"
ARVORE = r"C:\t\k411c\arvore"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
rec_raw = rd(REC_P); rec = json.loads(rec_raw.decode("utf-8"))
if rec.get("contrato") == CONTRATO_NOVO:
    print(json.dumps({"estado": "JA_COMPLEMENTADO_R3_6", "sha256": sha(rec_raw), "nota": "o recibo ja' e' do contrato %s; nada a fazer" % CONTRATO_NOVO}, ensure_ascii=False)); sys.exit(0)
assert rec.get("contrato") == "KERNEL_RECIBO_R3_2" and rec.get("versao") == "v411" and rec.get("pedras") == [] and rec.get("rc") == 0, ("o recibo de partida nao e' o da v411 sem pedra", rec.get("contrato"))
assert not any(c in rec for c in PROIBIDAS) and "modulos_de_auditoria" not in rec and "formal_files_antes" not in rec and "nos_kernel_impressao" not in rec, "o recibo de partida ja' tem chaves do contrato novo ou proibidas"
cruzamentos = {}

# (2) o manifesto do kernel da v410 em custodia, conferido contra o pino
pinos = json.load(open(PINOS_P, encoding="utf-8")); pm = pinos["kernel_manifesto_anterior_v410"]
base_man_raw = rd(BASE_MAN_P)
assert os.path.normcase(os.path.normpath(pm["path"])) == os.path.normcase(os.path.normpath(BASE_MAN_P)), ("o pino kernel_manifesto_anterior_v410 aponta outro arquivo", pm["path"])
assert sha(base_man_raw) == pm["sha256"], ("o manifesto do kernel da v410 em custodia diverge do pino", sha(base_man_raw), pm["sha256"])
base_man = json.loads(base_man_raw.decode("utf-8")); ff_antes = base_man["formal_files_sha256"]
assert isinstance(ff_antes, dict) and ff_antes and all(isinstance(c, str) and re.fullmatch(r"[0-9a-f]{64}", v or "") for c, v in ff_antes.items()), "formal_files_sha256 do manifesto da v410 mal formado"
imp = impressao_formal(ff_antes)
cruzamentos["manifesto_v410_sha256_igual_ao_pino"] = True
cruzamentos["raiz_antes_igual_ao_manifesto_v410"] = ff_antes.get("TGLExt.lean") == rec["raiz"]["sha256_antes"] == rec["raiz"]["sha256_depois"]
cruzamentos["audit_antes_igual_ao_manifesto_v410"] = ff_antes.get("TGL/Audit.lean") == rec["audit"]["sha256_antes"] == rec["audit"]["sha256_depois"]

# (3) as tres impressoes tem de coincidir: a do manifesto v410, a do recibo pre-selo (falha e pinado) e a do manifesto que o Nos tem hoje
falha = json.load(open(FALHA_P, encoding="utf-8")); ka_falha = (falha.get("recibo_pre_selo") or {}).get("kernel_anterior") or {}
rps_pin = pinos["recibo_pre_selo"]; assert sha(rd(rps_pin["path"])) == rps_pin["sha256"], "o recibo pre-selo pinado mudou desde o pino"
ka_pin = ((json.load(open(rps_pin["path"], encoding="utf-8")).get("nos") or {}).get("kernel")) or {}   # no recibo pre-selo pinado (o do ensaio contra o Nos v410) o kernel esta em nos.kernel; a ferramenta o copia para kernel_anterior no recibo seguinte
nos_man_raw = rd(NOS_MAN_P); nos_man = json.loads(nos_man_raw.decode("utf-8"))
imp_nos = impressao_formal(nos_man["formal_files_sha256"])
cruzamentos["impressao_igual_ao_recibo_pre_selo_da_falha"] = (ka_falha.get("impressao_formal") == imp)
cruzamentos["impressao_igual_ao_recibo_pre_selo_pinado"] = (ka_pin.get("impressao_formal") == imp and ka_pin.get("raiz_sha256") == rec["raiz"]["sha256_antes"] and ka_pin.get("audit_sha256") == rec["audit"]["sha256_antes"])
cruzamentos["impressao_igual_ao_manifesto_do_nos_hoje"] = (imp_nos == imp)
cruzamentos["formal_files_do_nos_hoje_igual_ao_da_v410"] = (nos_man["formal_files_sha256"] == ff_antes)
cruzamentos["raiz_e_audit_iguais_ao_recibo_pre_selo_da_falha"] = (ka_falha.get("raiz_sha256") == rec["raiz"]["sha256_antes"] and ka_falha.get("audit_sha256") == rec["audit"]["sha256_antes"])

# a frase da definicao: a do recibo da v410, com a versao do selo que o Nos tinha na etapa 2 (a v410 aqui; na v410 era a v409)
rec10 = json.load(open(REC10_P, encoding="utf-8")); def10 = rec10["nos_kernel_impressao"]["definicao"]
m_def = re.search(r"selo (v\d+)\)", def10); assert m_def, ("a definicao do recibo da v410 nao traz a versao do selo", def10)
selo_base = json.load(open(BASE_SELO_P, encoding="utf-8")); assert selo_base["um_version"] == "v410" and sha(rd(BASE_MAN_P)) == selo_base["sha256"]["tgl_kernel_proof_manifest.json"], "o selo da base nao pina o manifesto da v410"
definicao = def10.replace("selo " + m_def.group(1) + ")", "selo " + selo_base["um_version"] + ")")
nos_kernel_impressao = {"definicao": definicao, "antes": imp, "depois": imp}
formal_antes = dict(ff_antes)
assert impressao_formal(formal_antes) == imp

# (4) toolchain.lake_version: MEDIDO agora (o unico comando lake), cwd no sandbox do build
assert os.path.isfile(os.path.join(SANDBOX, "lean-toolchain")), "o sandbox do build nao tem lean-toolchain"
lake = shutil.which("lake") or os.path.join(os.environ.get("USERPROFILE", ""), ".elan", "bin", "lake.exe")
assert os.path.isfile(lake) or shutil.which("lake"), ("lake nao encontrado", lake)
rp = subprocess.run([lake, "--version"], cwd=SANDBOX, capture_output=True, timeout=180)
lake_out = rp.stdout.decode("utf-8", "replace").replace("\r\n", "\n"); lake_err = rp.stderr.decode("utf-8", "replace").replace("\r\n", "\n")
assert rp.returncode == 0 and lake_out.strip(), ("lake --version falhou", rp.returncode, lake_out[:200], lake_err[:200])
lake_version = [l_.strip() for l_ in lake_out.split("\n") if l_.strip()]
cruzamentos["lake_version_medido_igual_ao_manifesto_v410"] = (lake_version == base_man.get("lake_version"))
cruzamentos["lake_version_medido_igual_ao_manifesto_do_nos_hoje"] = (lake_version == nos_man.get("lake_version"))
cruzamentos["lean_version_do_recibo_igual_ao_manifesto_do_nos_hoje"] = (rec["toolchain"]["lean_version"] == nos_man.get("lean_version"))

# (5) a arvore so-fontes: a MESMA contagem de contar_lean_recursivo (sem seguir juncao nem link), e os tokens proibidos re-escaneados nela
assert os.path.isdir(ARVORE), "a arvore C:\\t\\k411c\\arvore nao existe (rodar refazer_arvore_v411_pos_selo.py)"
n_lean = n_o16 = 0; links = []; baks = []; hits = []; hits_probe = []
NS = B.carregar(["_lean_strip_comments_and_strings", "_LEAN_FORBIDDEN_TOKENS"]); TOKS = list(NS["_LEAN_FORBIDDEN_TOKENS"]); strip_ = NS["_lean_strip_comments_and_strings"]
pilha = [ARVORE]
while pilha:
    d_ = pilha.pop()
    with os.scandir(d_) as it_:
        for e_ in it_:
            if ".bak" in e_.name:
                baks.append(os.path.relpath(e_.path, ARVORE))
            if e_.is_junction() or e_.is_symlink():
                links.append(os.path.relpath(e_.path, ARVORE))
            elif e_.is_dir(follow_symlinks=False):
                pilha.append(e_.path)
            elif e_.is_file(follow_symlinks=False) and e_.name.lower().endswith(".lean"):
                n_lean += 1; rel_ = os.path.relpath(e_.path, ARVORE).replace(os.sep, "/"); n_o16 += rel_.startswith("TGLExt/O16/")
                code_ = strip_(rd(e_.path).decode("utf-8"))
                for tok_ in TOKS:
                    if re.search(r"\b%s\b" % re.escape(tok_), code_):
                        (hits_probe if os.path.basename(rel_).startswith("Probe") else hits).append("%s:%s" % (rel_, tok_))
vt_old = rec["varredura_tokens"]
cruzamentos["arvore_sem_juncao_nem_link"] = not links
cruzamentos["contagens_iguais_as_do_recibo_de_partida"] = (n_lean == vt_old["arquivos_lean"] and n_o16 == vt_old["arquivos_lean_em_TGLExt_O16"])
cruzamentos["zero_tokens_proibidos_na_arvore"] = not hits
cruzamentos["tokens_proibidos_igual_ao_criterio_medido"] = (len(hits) == rec["criterios"]["tokens_proibidos"]["medido"])
cruzamentos["raiz_e_audit_da_arvore_iguais_ao_recibo"] = (sha(rd(os.path.join(ARVORE, "TGLExt.lean"))) == rec["raiz"]["sha256_depois"] and sha(rd(os.path.join(ARVORE, "TGL", "Audit.lean"))) == rec["audit"]["sha256_depois"])
print(json.dumps({"cruzamentos": cruzamentos, "impressao_formal": imp, "n_arquivos_formais_antes": len(ff_antes), "lake_version": lake_version, "lake_stderr": lake_err.strip()[:200],
                  "varredura": {"arquivos_lean": n_lean, "em_O16": n_o16, "links": links[:5], "hits": hits[:5], "hits_probe": len(hits_probe), "arquivos_com_bak_no_nome": baks[:5]}}, ensure_ascii=False))
assert all(cruzamentos.values()), ("o complemento R3.6 nao fecha: PARO sem gravar", [k_ for k_, v_ in cruzamentos.items() if not v_])

# o recibo novo: a ordem das chaves e' a do recibo de partida, com as chaves novas ao lado das irmas
novo = {}
for k_, v_ in rec.items():
    if k_ == "contrato":
        novo["contrato"] = CONTRATO_NOVO; novo["versao_sem_pedra_nova"] = True
    elif k_ == "toolchain":
        novo["toolchain"] = {"lean_version": v_["lean_version"], "lake_version": lake_version}
    elif k_ == "arvore":
        novo["arvore"] = ARVORE.replace("\\", "/")
    elif k_ == "varredura_tokens":
        novo["varredura_tokens"] = {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16, "raiz_da_varredura": ARVORE.replace("\\", "/"), "sem_lake": True, "hits_em_Probe": len(hits_probe),
                                    "tokens_proibidos_reescaneados_na_arvore": True, "sem_juncao_nem_link": True}
    else:
        novo[k_] = v_
    if k_ == "criterios":
        novo["nos_kernel_impressao"] = nos_kernel_impressao; novo["formal_files_antes"] = formal_antes
fontes = {"manifesto_v410": {"path": BASE_MAN_P, "sha256": sha(base_man_raw)}, "recibo_da_falha": {"path": FALHA_P, "sha256": sha(rd(FALHA_P))}, "recibo_pre_selo_pinado": {"path": rps_pin["path"], "sha256": rps_pin["sha256"]},
          "manifesto_do_nos_hoje_so_leitura": {"path": NOS_MAN_P, "sha256": sha(nos_man_raw)}, "recibo_v410_so_a_frase_da_definicao": {"path": REC10_P, "sha256": sha(rd(REC10_P))}, "selo_da_base_v410": {"path": BASE_SELO_P, "sha256": sha(rd(BASE_SELO_P))}}
novo["complemento_r36"] = {
    "por": "complementar_recibo_kernel_v411_r36.py (claude-construtor-r36, a servico da gerencia c1)", "quando": AGORA,
    "nota": "so' medicao: NENHUM build e NENHUM Audit foram refeitos (o kernel da v411 e' o da v410 byte a byte); o unico comando lake rodado foi `lake --version` com cwd em C:/t/k411c/final",
    "de_onde_veio_cada_campo": {
        "contrato e versao_sem_pedra_nova": "o contrato novo KERNEL_RECIBO_R3_6 (sincronizar_bancada.py da R3_6): o recibo da versao sem pedra nova; pedras segue [] e nao ha modulos_de_auditoria",
        "formal_files_antes": "formal_files_sha256 do manifesto do kernel da v410 em custodia (base_v410), conferido por sha256 contra o pino kernel_manifesto_anterior_v410 de PINOS_BN_v411.json",
        "nos_kernel_impressao": "sha256 do JSON canonico de formal_files_antes (a funcao impressao_formal da ferramenta); antes == depois; cruzada com recibo_pre_selo.kernel_anterior.impressao_formal (falha e pinado) e com o manifesto do Nos hoje",
        "nos_kernel_impressao.definicao": "a frase do recibo da v410 com a versao do selo que o Nos tinha na etapa 2: %s no lugar de %s" % (selo_base["um_version"], m_def.group(1)),
        "toolchain.lake_version": "saida MEDIDA de `lake --version` (cwd C:/t/k411c/final): %s" % json.dumps(lake_version, ensure_ascii=False),
        "arvore e varredura_tokens": "C:/t/k411c/arvore (so-fontes, refeita por refazer_arvore_v411_pos_selo.py): .lean recontados com o algoritmo de contar_lean_recursivo (sem seguir juncao nem link) e tokens proibidos re-escaneados nela",
    },
    "fontes": fontes, "cruzamentos": cruzamentos,
    "limite": "a identidade do kernel com o da v410 e' a identidade dos formal_files_sha256 (arquivo a arquivo) e dos logs/Audit ja' conferidos no recibo de partida; este complemento nao refaz o build"}
assert not any(c in novo for c in PROIBIDAS) and "modulos_de_auditoria" not in novo and novo["pedras"] == [] and novo["rc"] == 0
novo_raw = json.dumps(novo, ensure_ascii=False, indent=1).encode("utf-8")
print(json.dumps({"modo": "EXECUTAR" if EXECUTAR else "ENSAIO_A_SECO", "recibo_atual": {"bytes": len(rec_raw), "sha256": sha(rec_raw)[:16]}, "recibo_novo": {"bytes": len(novo_raw), "sha256": sha(novo_raw)[:16]}}, ensure_ascii=False))
if not EXECUTAR:
    print("ensaio a seco: nada gravado (use --executar)"); sys.exit(0)
bak = REC_P + ".bak_" + TS + "_r36"
assert not os.path.exists(bak), "backup ja' existe"
open(bak, "wb").write(rec_raw); assert rd(bak) == rec_raw, "o backup nao e' copia de bytes do recibo"
open(REC_P + ".tmp", "wb").write(novo_raw); assert os.path.getsize(REC_P + ".tmp") == len(novo_raw)
os.replace(REC_P + ".tmp", REC_P)
depois = rd(REC_P); assert depois == novo_raw and len(depois) > len(rec_raw), "o recibo gravado nao e' o esperado (restaurar do backup %s)" % bak
chk = json.loads(depois.decode("utf-8")); assert chk["contrato"] == CONTRATO_NOVO and chk["versao_sem_pedra_nova"] is True and chk["pedras"] == [] and not any(c in chk for c in PROIBIDAS)
print(json.dumps({"gravado": REC_P, "bytes": len(depois), "sha256": sha(depois), "backup": bak, "backup_sha256": sha(rd(bak))}, ensure_ascii=False))
