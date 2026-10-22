# -*- coding: utf-8 -*-
"""harness_fechar_sandbox_v396.py -- roda fechar_v396.py e registrar_mapa_v396.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v396\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v396.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, o handoff) e o main do registrar_mapa. Derivado do harness_fechar_sandbox_v395.py (que rodou na v395).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v396 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v395, insumos, o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + nos\\ (o Nos EMULADO montado de dry_v396, como no harness dos textos) + memory\\
(a memoria vazia). As copias dos scripts (leitura, textos, fechar) trocam SO' as duas constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox; o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais
e' so' essas linhas).
O que ele prova: fechar_v396.py sai com rc 0 e grava o handoff (guarda P18 limpa), o handoff do Nos, os dois diffs, o manifesto e o arquivo; RECUSA (rc 2) sem o recibo do religamento e com um recibo do B(n) que declara salto; registrar_mapa_v396.py (main) monta o JSON
com 3 registros e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v395, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -I -B -X utf8 harness_fechar_sandbox_v396.py [--manter]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita)"""
import hashlib, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); DRY = os.path.join(PKG, "dry_v396")
OUT = os.path.join(HERE, "harness_saida_v396"); SB = os.path.join(OUT, "fechar_sandbox")
sys.path.insert(0, PKG)
from guarda_p18_v396 import violacoes  # noqa: E402
MANTER = "--manter" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
rdj = lambda p: json.load(open(p, encoding="utf-8"))
R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}}


def falha(m):
    R["problemas"].append(m); print("  PROBLEMA:", m)


def recusa(m):
    print("RECUSO:", m); sys.exit(4)


ESP = rdj(os.path.join(PKG, "ESPERADOS_v396.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v396.json"))
cand16 = fsha(os.path.join(PKG, "um_v396_candidato.py"))[:16]
if not (ESP["candidato_sha16"] == CM["sha16"] == cand16 == fsha(os.path.join(DRY, "um.py"))[:16]):
    recusa("o candidato nao e' um so' (ESPERADOS, CANDIDATO, arquivo e dry_v396/um.py divergem)")
for n in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v396_pt.txt", "dry_v396_en.txt", "dry_v396_pt.toc", "dry_v396_en.toc", "tgl_kernel"):
    if not os.path.exists(os.path.join(DRY, n)):
        recusa("dry_v396 incompleto (falta %s)" % n)
os.makedirs(OUT, exist_ok=True); shutil.rmtree(SB, ignore_errors=True)
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v396"); POS = os.path.join(PKS, "pos_rito"); NOSS = os.path.join(SB, "nos"); UMS = os.path.join(SB, "memory"); TOOLS = os.path.join(SB, "work", "cadeia_de_selo")
for d in (POS, os.path.join(PKS, "base_v395"), os.path.join(PKS, "kernel"), os.path.join(POS, "conferidor"), os.path.join(PKS, "bancada_B3"), os.path.join(PKS, "bancada_B3_servico"), NOSS):
    os.makedirs(d, exist_ok=True)
# ---- o pacote do sandbox
for n in ("guarda_p18_v396.py", "ESPERADOS_v396.json", "CANDIDATO_v396.json", "PINOS_BN_v396.json", "kernel_modulos_novos_v396.json", "delta_v396.py", "conferir_rito_v396.py"):
    shutil.copyfile(os.path.join(PKG, n), os.path.join(PKS, n))
for kn_ in ("KERNEL_RECIBO_v396.json", "FLAGS_v396.json"):
    shutil.copyfile(os.path.join(PKG, "kernel", kn_), os.path.join(PKS, "kernel", kn_))
shutil.copyfile(os.path.join(PKG, "base_v395", "um.py"), os.path.join(PKS, "base_v395", "um.py")); shutil.copyfile(os.path.join(PKG, "base_v395", "um_absoluto.json"), os.path.join(PKS, "base_v395", "um_absoluto.json"))
shutil.copyfile(os.path.join(PKG, "base_v395", "um_absoluto_selo.json"), os.path.join(PKS, "base_v395", "um_absoluto_selo.json"))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"), os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"))
open(os.path.join(PKS, "rito_horarios_v396.txt"), "w", encoding="utf-8").write("00:00:00\n00:45:00\n")          # EMULADO (sandbox)
# ---- as copias dos scripts, trocando SO' os caminhos do Nos e da memoria
NOS_RX = 'NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")'
UMEM_RX = 'UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")'
TROCAS = {"leitura_v396.py": [(NOS_RX, 'NOS = %r' % NOSS)], "textos_v396.py": [(NOS_RX, 'NOS = %r' % NOSS)], "fechar_v396.py": [(UMEM_RX, 'UMEM = %r' % UMS)], "registrar_mapa_v396.py": []}
DIF = {}
for n, trs in TROCAS.items():
    t = open(os.path.join(HERE, n), encoding="utf-8").read(); t0 = t
    for a, b in trs:
        if t.count(a) != 1:
            recusa("a linha de caminho nao e' unica em %s: %r (%d)" % (n, a[:60], t.count(a)))
        t = t.replace(a, b)
    open(os.path.join(POS, n), "w", encoding="utf-8", newline="\n").write(t)
    s0_ = set(t0.splitlines()); DIF[n] = [l for l in t.splitlines() if l not in s0_]
# ---- o Nos emulado (dry_v396 + o selo completado como em teste_conferidor_positivo_v396.py)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"), ("dry_v396_pt.txt", "um_absoluto_pt.txt"),
                 ("dry_v396_en.txt", "um_absoluto_en.txt"), ("dry_v396_pt.toc", "um_absoluto_pt.toc"), ("dry_v396_en.toc", "um_absoluto_en.toc"), ("dry_v396_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v396_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSS, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSS, "tgl_kernel"))
s0 = rdj(os.path.join(PKS, "base_v395", "um_absoluto_selo.json")); s = dict(s0); s.update(rdj(os.path.join(DRY, "selo_ensaio.json"))); s["sha256"] = dict(s0.get("sha256") or {}); s["sha256"]["um.py"] = fsha(os.path.join(NOSS, "um.py"))
open(os.path.join(NOSS, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, default=str))
N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v396"])
open(os.path.join(NOSS, "rodada_v396_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join([
    "[v396] EMULADO PELO SANDBOX", "   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], n_spec, n_spec),
    "teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", "RITO_RC=0", ""]))
bu = os.path.join(PKS, "base_v395", "um.py")
ap = {"ts": time.strftime("%Y%m%d_%H%M%S"), "backups": {"um.py": {"backup": bu, "bytes": os.path.getsize(bu), "sha16": fsha(bu)[:16]}}, "um_py_novo": {"bytes": os.path.getsize(os.path.join(NOSS, "um.py")), "sha16": ESP["candidato_sha16"]}}
open(os.path.join(PKS, "APLICADO_AO_CANONICO_%s.json" % ap["ts"]), "w", encoding="utf-8").write(json.dumps(ap, indent=1))
# ---- o conferidor REAL (copia) contra o Nos emulado: a conferencia que a leitura le
env = dict(os.environ); env["V396_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"
cfd = os.path.join(SB, "conferidor_tmp"); os.makedirs(cfd)
for n in ("conferir_rito_v396.py", "delta_v396.py", "ESPERADOS_v396.json"):
    shutil.copyfile(os.path.join(PKS, n), os.path.join(cfd, n))
pc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", "conferir_rito_v396.py"], cwd=cfd, env=env, capture_output=True, text=True, encoding="utf-8")
if pc.returncode != 0 or not os.path.exists(os.path.join(cfd, "conferencia_rito_v396.json")):
    falha("o conferidor nao deu TUDO BATE contra o Nos emulado do sandbox: %s" % pc.stdout[-300:])
else:
    shutil.copyfile(os.path.join(cfd, "conferencia_rito_v396.json"), os.path.join(POS, "conferidor", "conferencia_rito_v396.json"))
# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v395)
PKG_ANT = os.path.join(os.path.dirname(PKG), "v395")
import glob
base_apl = rdj(glob.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v395_*.json"))[0])
pinos = rdj(os.path.join(PKG, "PINOS_BN_v396.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1


def recibo_apl(com_salto=False):
    r = json.loads(json.dumps(base_apl)); r["versao_alvo"] = "v396"; r["fase"] = "pos_selo"; r["modo"] = "aplicar"; r.pop("salto", None); r.pop("cadeia_de_selos", None)
    r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v396-20261022-R1" % n_ger
    r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}; r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v396"}
    r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
    r["veredito"] = "REPINADA_B%d__%sAPLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (n_ger, "SALTO_v395_v396__" if com_salto else "")
    r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v396", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
    if com_salto:
        r["salto"] = {"declarado": True}
    r["_sintetico"] = "SINTETICO (sandbox do fechar): NAO e' um recibo do esboco"
    return r


def escreve(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))


RAPL = recibo_apl(); man_novo = RAPL["manifesto_novo"]["sha256"]
pth_apl = os.path.join(PKS, "bancada_B3", "RECIBO_SINCRONIZACAO_v396_SINTETICO.json"); escreve(pth_apl, RAPL)
agora = time.strftime("%Y-%m-%dT%H:%M:%S")
open(os.path.join(PKS, "bancada_B3_servico", "RECIBO_PARADA_v396.json"), "w", encoding="utf-8").write(json.dumps({"passo": "10-bis-a", "pid": 11111, "porta": 18777, "porta_fechada": True, "hora": agora, "_sintetico": "sandbox"}))
pth_rel = os.path.join(PKS, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v396.json")
open(pth_rel, "w", encoding="utf-8").write(json.dumps({"passo": "10-ter", "versao_servida": "v396", "manifesto_sha256": man_novo, "pid": 22222, "hora": agora, "_sintetico": "sandbox"}))


def roda(script, nome):
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, script)], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    open(os.path.join(SB, nome + "_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return p.returncode, p.stdout, p.stderr


# ---- 1. controles negativos do fechar: sem o religamento e com recibo que declara salto => RECUSA (rc 2), nada de handoff
NEG = []
os.rename(pth_rel, pth_rel + ".fora")
rc, so, se = roda("fechar_v396.py", "fechar_sem_religamento"); NEG.append({"controle": "sem o recibo do religamento", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v396-custodia.md"))})
os.rename(pth_rel + ".fora", pth_rel)
escreve(pth_apl, recibo_apl(com_salto=True))
rc, so, se = roda("fechar_v396.py", "fechar_com_salto"); NEG.append({"controle": "recibo do B(n) com salto declarado", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v396-custodia.md"))})
escreve(pth_apl, RAPL)
for n in NEG:
    print("  controle negativo do fechar: %-40s %s" % (n["controle"], "RECUSOU como esperado" if (n["recusou"] and not n["handoff_escrito"]) else "NAO RECUSOU"))
    if not (n["recusou"] and not n["handoff_escrito"]):
        falha("fechar_v396.py nao recusou como esperado: %s" % n)
R["etapas"]["fechar_negativos"] = NEG
# ---- 2. o fechar (positivo)
t0 = time.time(); rc, so, se = roda("fechar_v396.py", "fechar"); dt = time.time() - t0
ok_f = (rc == 0 and "FECHADO v396:" in so)
chk = {}
for rel in (os.path.join(UMS, "handoff-v396-custodia.md"), os.path.join(NOSS, "HANDOFF_v396_CUSTODIA.md"), os.path.join(PKS, "DIFF_v395_v396.diff"), os.path.join(PKS, "DIFF_KERNEL_v396.txt"), os.path.join(PKS, "MANIFESTO_ARQUIVO_v396.json"),
            os.path.join(POS, "v396_incorporacao_manifesto.json"), os.path.join(TOOLS, "v396_incorporacao_manifesto.json"), os.path.join(TOOLS, "v396_kernel", "pedras", "TGLExt_TestemunhaEstatica.lean"), os.path.join(TOOLS, "v396_selo", "chain_pos_rito_v396.sh") if os.path.exists(os.path.join(POS, "chain_pos_rito_v396.sh")) else os.path.join(TOOLS, "v396_selo", "fechar_v396.py")):
    chk[os.path.relpath(rel, SB)] = os.path.exists(rel) and os.path.getsize(rel) > 0
ho = open(os.path.join(UMS, "handoff-v396-custodia.md"), encoding="utf-8").read() if os.path.exists(os.path.join(UMS, "handoff-v396-custodia.md")) else ""
vio = violacoes(ho)
dk = open(os.path.join(PKS, "DIFF_KERNEL_v396.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v396.txt")) else ""
man = rdj(os.path.join(POS, "v396_incorporacao_manifesto.json")) if os.path.exists(os.path.join(POS, "v396_incorporacao_manifesto.json")) else {}
R["etapas"]["fechar"] = {"rc": rc, "segundos": round(dt, 1), "ok": ok_f, "arquivos": chk, "handoff_bytes": len(ho.encode("utf-8")), "handoff_guarda_p18": [list(x) for x in vio][:3], "diff_kernel_novos": ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk),
                         "manifesto_chaves": sorted(man.keys())[:30], "ultima_linha": so.strip().splitlines()[-1][:200] if so.strip() else se[-300:]}
print("  fechar em sandbox: rc %s (%.0f s); arquivos %s; handoff %d B; guarda P18 %s; diff do kernel traz o modulo novo: %s" % (rc, dt, "todos presentes" if all(chk.values()) else [k for k, v in chk.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], "novos (1)" in dk))
if not ok_f:
    falha("fechar_v396.py (sandbox) saiu com rc %s: %s" % (rc, (so + se)[-400:]))
if not all(chk.values()):
    falha("fechar_v396.py (sandbox) nao gravou: %s" % [k for k, v in chk.items() if not v])
if vio:
    falha("handoff com violacao da guarda P18: %s" % vio[:2])
if not ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk):
    falha("DIFF_KERNEL_v396.txt nao traz o modulo novo")
for k_ in ("registros_v396", "base_v395", "b3", "diffs", "insumos_sha16", "conferidor"):
    if k_ not in man:
        falha("o manifesto de incorporacao nao traz a chave %s" % k_)
# ---- 3. o registrar_mapa (main)
rc, so, se = roda("registrar_mapa_v396.py", "registrar_mapa")
pj = os.path.join(POS, "registro_mapa_v396.json"); reg = rdj(pj) if os.path.exists(pj) else []
ok_m = (rc == 0 and len(reg) == 3 and "registro MONTADO (NAO registrado)" in so and "COMANDO (ato da gerencia)" in so)
R["etapas"]["registrar_mapa"] = {"rc": rc, "ok": ok_m, "n_registros": len(reg), "rotas": [x.get("rota_id") for x in reg], "comando": [l for l in so.splitlines() if l.startswith("COMANDO")][:1], "artefatos_da_rota": [os.path.basename(a) for a in (reg[0].get("artefatos") or [])] if reg else []}
print("  registrar_mapa (main) em sandbox: rc %s; %d registro(s); %s" % (rc, len(reg), "ok" if ok_m else "FALHOU"))
if not ok_m:
    falha("registrar_mapa_v396.py (main, sandbox) falhou: rc %s: %s" % (rc, (so + se)[-400:]))
# ---- 4. as copias dos scripts diferem dos originais so' nas linhas de caminho
R["etapas"]["copias_dos_scripts"] = {n: [l[:140] for l in v] for n, v in DIF.items()}
if any(len(v) != 1 for n, v in DIF.items() if n != "registrar_mapa_v396.py") or DIF["registrar_mapa_v396.py"]:
    falha("as copias dos scripts diferem dos originais em mais de uma linha de caminho: %s" % {n: len(v) for n, v in DIF.items()})
# ---- limpeza
LIMP = None
if not MANTER:
    LIMP = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(SB) for f_ in fs_)
    keep = os.path.join(OUT, "fechar_sandbox_resultado"); shutil.rmtree(keep, ignore_errors=True); os.makedirs(keep)
    for nome in ("fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "registrar_mapa_out.txt"):
        if os.path.exists(os.path.join(SB, nome)):
            shutil.copyfile(os.path.join(SB, nome), os.path.join(keep, nome))
    for src, dst in ((os.path.join(UMS, "handoff-v396-custodia.md"), "handoff-v396-custodia.md"), (os.path.join(POS, "registro_mapa_v396.json"), "registro_mapa_v396_SANDBOX.json"), (os.path.join(POS, "v396_incorporacao_manifesto.json"), "v396_incorporacao_manifesto_SANDBOX.json"),
                     (os.path.join(PKS, "DIFF_KERNEL_v396.txt"), "DIFF_KERNEL_v396_SANDBOX.txt")):
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(keep, dst))
    shutil.rmtree(SB, ignore_errors=True)
R["etapas"]["limpeza"] = {"sandbox_removido_bytes": LIMP, "guardado_em": os.path.join(OUT, "fechar_sandbox_resultado") if not MANTER else SB}
R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["tudo_passou"] = not R["problemas"]
R["veredito"] = "TUDO PASSOU: o fechar grava o handoff, os diffs, o manifesto e o arquivo e RECUSA sem o religamento e com salto; o registrar_mapa monta o registro" if R["tudo_passou"] else "NAO PASSOU (ver problemas)"
R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados; a prova e' do codigo do fechar e do registrar_mapa, nao de um B(n) real"
saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v396.json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))
print("VEREDITO (fechar em sandbox):", R["veredito"]); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)
