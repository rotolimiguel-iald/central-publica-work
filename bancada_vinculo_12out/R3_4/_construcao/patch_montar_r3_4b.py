# -*- coding: utf-8 -*-
"""patch de construcao (R3.4, parte b): ../montar_sandbox.py ganha (1) a camada sintetica v393 (nos_v393s/, a arvore do kernel, o recibo do kernel no contrato KERNEL_RECIBO_R3_4 com um
modulo de auditoria, os CRITERIOS) e (2) uma pasta cadeia_de_selo de ENSAIO (fx/cadeia_de_selo: base_vJ + registros do instalador + backups de bytes) para o gerador da cadeia de selos e
os controles do salto."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "montar_sandbox.py"
t = P.read_text(encoding="utf-8")


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:110])
    t = t.replace(old, new)


EXTRA = r'''# ================================================================ R3.4: a camada sintetica v393 e a cadeia de selos de ensaio
# nos_v393s/ = o Nos sintetico SEGUINTE ao v392 sintetico: UM_VERSION v393 (mesmo comprimento), a arvore do kernel ganha a pedra C (um teorema) e um MODULO DE AUDITORIA
# (so import + run_cmd, sem declaracoes); o recibo do kernel sintetico (contrato KERNEL_RECIBO_R3_4) lista o modulo em modulos_de_auditoria.
V3 = "v393"
KS3 = RAIZ / "fx" / "kernel_src_v393s"
arv3 = dict(arvore)
arv3["TGLExt/PedraSinteticaC.lean"] = "-- SINTETICO (sandbox R3.4): pedra C\nnamespace TGLExt.PedraSinteticaC\ntheorem tres : 3 = 3 := rfl\nend TGLExt.PedraSinteticaC\n"
AUDITORIA_C = """-- SINTETICO (sandbox R3.4): modulo de auditoria: so import, open e run_cmd; nenhuma declaracao
import TGLExt.PedraSinteticaC
import Lean

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut n := 0
  for (c, _) in env.constants.toList do
    if let some i := env.getModuleIdxFor? c then
      let m := env.header.moduleNames[i]!
      if (`TGLExt.PedraSinteticaC).isPrefixOf m then
        n := n + 1
  if n == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDIT_COUNT " ++ toString n)
"""
arv3["TGLExt/AuditoriaSinteticaC.lean"] = AUDITORIA_C
arv3["TGLExt.lean"] = arvore["TGLExt.lean"] + "import TGLExt.PedraSinteticaC\nimport TGLExt.AuditoriaSinteticaC\n"
arv3["TGL/Audit.lean"] = arvore["TGL/Audit.lean"] + "#print axioms TGLExt.PedraSinteticaC.tres\n"
ks3_sha = {}
for rel, txt in arv3.items():
    b = txt.encode("utf-8")
    gravar_novo(KS3 / rel, b)
    ks3_sha[rel] = sha(b)
for rel, txt in ARVORE_EXTRA.items():
    gravar_novo(KS3 / rel, txt.encode("utf-8"))
N_LEAN3 = sum(1 for q in KS3.rglob("*.lean"))
N_LEAN3_O16 = sum(1 for q in (KS3 / "TGLExt" / "O16").rglob("*.lean"))
rec["fx"]["kernel_src_v393s"] = dict(dir=str(KS3), sha256=ks3_sha, arquivos_lean=N_LEAN3, arquivos_lean_em_TGLExt_O16=N_LEAN3_O16)
ff_v392s = dict(kman["formal_files_sha256"])
kman3 = json.loads(json.dumps(kman))
for rel, h in ks3_sha.items():
    kman3["formal_files_sha256"][rel] = h
kman3["axiom_report"]["TGLExt.PedraSinteticaC.tres"] = []
kman3["SINTETICO_SANDBOX"] = "NAO E O MANIFESTO DO RITO: fixture do ensaio do vinculo (R3.4, 19/10/2026); deriva do manifesto sintetico v392 acrescentando a pedra C e o modulo de auditoria C"
kman3_b = json.dumps(kman3, ensure_ascii=False, indent=1).encode("utf-8")
txt3 = um_sin.decode("utf-8-sig")
mv3 = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt3, re.M)
assert mv3 and mv3.group(1) == VERSAO_SINTETICA, mv3
velha3 = mv3.group(0).encode("utf-8")
nova3 = velha3.replace(VERSAO_SINTETICA.encode("utf-8"), V3.encode("utf-8"), 1)
assert um_sin.count(velha3) == 1
um3 = um_sin.replace(velha3, nova3, 1)
assert len(um3) == len(um_sin) and um3 != um_sin
selo3 = dict(selo_sin)
selo3["um_version"] = V3
selo3["sha256"] = dict(selo_sin["sha256"])
selo3["sha256"]["um.py"] = sha(um3)
selo3["sha256"]["tgl_kernel_proof_manifest.json"] = sha(kman3_b)
selo3["SINTETICO_SANDBOX"] = "NAO E UM SELO DO RITO: fixture do ensaio do vinculo (R3.4, 19/10/2026); deriva do selo sintetico v392 trocando um_version, sha256[um.py] e sha256[tgl_kernel_proof_manifest.json]; vive so em %s" % RAIZ
selo3_b = json.dumps(selo3, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_v393s"] = dict(um_py=gravar_novo(RAIZ / "nos_v393s" / "um.py", um3), selo=gravar_novo(RAIZ / "nos_v393s" / "um_absoluto_selo.json", selo3_b),
                        core=gravar_novo(RAIZ / "nos_v393s" / "um_absoluto.json", core), kernel_manifest=gravar_novo(RAIZ / "nos_v393s" / "tgl_kernel_proof_manifest.json", kman3_b), versao=V3)
gravar_novo(RAIZ / "nos_v393s" / "LEIA-ME_SINTETICO.txt", ("Fixture sintetica (R3.4, 19/10/2026): o Nos sintetico v392 com UM_VERSION trocada para %s; selo e manifesto do kernel derivados; core copiado. "
                                                          "NAO e versao selada. So para ensaiar o salto da Bancada no sandbox.\n" % V3).encode("utf-8"))
log_b3 = ("build_full.log SINTETICO (fixture R3.4 19/10/2026): nenhum kernel foi construido aqui; as linhas imitam o formato do lake 4.31\n"
          "✔ [1/6] Built TGLExt.PedraSinteticaA (1s)\n"
          "✔ [2/6] Built TGLExt.PedraSinteticaB (1s)\n"
          "✔ [3/6] Built TGLExt.PedraSinteticaC (1s)\n"
          "✔ [4/6] Built TGLExt.AuditoriaSinteticaC (1s)\n"
          "✔ [5/6] Built TGLExt (1s)\n"
          "✔ [6/6] Built TGL.Audit (1s)\n"
          "Build completed successfully (6 jobs).\n").encode("utf-8")
log_a3 = ("audit.log SINTETICO (fixture R3.4 19/10/2026)\n"
          "'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
          "'TGLExt.PedraSinteticaB.dois' does not depend on any axioms\n"
          "'TGLExt.PedraSinteticaC.tres' does not depend on any axioms\n").encode("utf-8")
rec["fx"]["log_build_v393s"] = gravar_novo(KL / "build_full_SINTETICO_v393s.log", log_b3)
rec["fx"]["log_audit_v393s"] = gravar_novo(KL / "audit_SINTETICO_v393s.log", log_a3)
k3 = dict(contrato="KERNEL_RECIBO_R3_4", versao=V3, quando_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), rc=0, sorry=0, erros=0,
          build_full_log=dict(path=str(KL / "build_full_SINTETICO_v393s.log"), sha256=sha(log_b3)),
          audit_log=dict(path=str(KL / "audit_SINTETICO_v393s.log"), sha256=sha(log_a3)),
          toolchain=dict(lean_version=list(kman["lean_version"]), lake_version=list(kman["lake_version"])),
          arvore=str(KS3),
          raiz=dict(path="TGLExt.lean", sha256_antes=ks_sha["TGLExt.lean"], sha256_depois=ks3_sha["TGLExt.lean"]),
          audit=dict(path="TGL/Audit.lean", sha256_antes=ks_sha["TGL/Audit.lean"], sha256_depois=ks3_sha["TGL/Audit.lean"]),
          pedras=[dict(path="TGLExt/AuditoriaSinteticaC.lean", sha256=ks3_sha["TGLExt/AuditoriaSinteticaC.lean"]),
                  dict(path="TGLExt/PedraSinteticaC.lean", sha256=ks3_sha["TGLExt/PedraSinteticaC.lean"], declaracoes=["TGLExt.PedraSinteticaC.tres"])],
          modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean"],
          axiomas=["propext", "Classical.choice", "Quot.sound"],
          criterios=dict(j1_declaracoes=dict(medido=1), j1_teoremas=dict(medido=1), j1_fora_do_trio=dict(medido=0), audit_entradas_antigas_identicas=dict(medido=0),
                         tokens_proibidos=dict(medido=0), r1_ausente=dict(medido=True), declaracoes_novas_no_trio=dict(medido=True)),
          varredura_tokens=dict(recursiva=True, arquivos_lean=N_LEAN3, arquivos_lean_em_TGLExt_O16=N_LEAN3_O16),
          formal_files_antes=dict(ff_v392s),
          nos_kernel_impressao=dict(definicao="sha256 do JSON canonico (chaves ordenadas, sem espacos, UTF-8) de formal_files_sha256 do Nos", antes=impressao_formal(ff_v392s), depois=impressao_formal(ff_v392s)),
          nota="FIXTURE SINTETICA do recibo do build do kernel da camada v393 sintetica, contrato KERNEL_RECIBO_R3_4: uma pedra com declaracao (C) e um modulo de auditoria sem declaracoes (listado)")
rec["fx"]["KERNEL_RECIBO_v393s_SINTETICO_VALIDO.json"] = gravar_novo(RAIZ / "fx" / "KERNEL_RECIBO_v393s_SINTETICO_VALIDO.json", json.dumps(k3, ensure_ascii=False, indent=1).encode("utf-8"))
crit3 = dict(contrato=CRITERIOS_CONTRATO, versao=V3, preenchido=True, x19="nao",
             esperados=dict(j1_declaracoes=1, j1_teoremas=1, j1_fora_do_trio=0, audit_entradas_antigas_identicas=0, tokens_proibidos=0, r1_ausente=True, declaracoes_novas_no_trio=True),
             SINTETICO_SANDBOX="NAO SAO OS CRITERIOS DA v393: fixture do ensaio (R3.4) para a camada sintetica v393")
rec["fx"]["CRITERIOS_v393_SINTETICO.json"] = gravar_novo(RAIZ / "fx" / "CRITERIOS_v393_SINTETICO.json", json.dumps(crit3, ensure_ascii=False, indent=1).encode("utf-8"))
# a pasta cadeia_de_selo de ENSAIO: <cadeia>/v(J+1)/base_vJ/ (copias de bytes de J), <cadeia>/v(J+1)/APLICADO_AO_CANONICO_<ts>.json (o registro do instalador que trocou J por J+1; o
# diretorio v392 tem tambem uma TENTATIVA REVERTIDA, que o gerador tem de ignorar) e _nos/ (os backups de bytes .bak_<ts>, que na vida real ficam no proprio Nos)
CS = RAIZ / "fx" / "cadeia_de_selo"
camadas = {"v391": (um, selo_raw, core, kman_raw), "v392": (um_sin, selo_b, core, kman_sin), "v393": (um3, selo3_b, core, kman3_b)}
rec["fx"]["cadeia_de_selo"] = dict(dir=str(CS), camadas={})
for v, (u_, s_, c_, k_) in camadas.items():
    proxima = "v%d" % (int(v[1:]) + 1)
    d_ = CS / proxima / ("base_" + v)
    rec["fx"]["cadeia_de_selo"]["camadas"][v] = dict(um_py=gravar_novo(d_ / "um.py", u_), selo=gravar_novo(d_ / "um_absoluto_selo.json", s_), core=gravar_novo(d_ / "um_absoluto.json", c_),
                                                     kernel_manifesto=gravar_novo(d_ / "tgl_kernel_proof_manifest.json", k_))
for (v_ant, v_novo, ts) in (("v391", "v392", "20261001_100000"), ("v392", "v393", "20261002_100000")):
    u_, s_, c_, k_ = camadas[v_ant]
    un = camadas[v_novo][0]
    bu = gravar_novo(CS / "_nos" / ("um.py.bak_" + ts), u_)
    bs = gravar_novo(CS / "_nos" / ("um_absoluto_selo.json.bak_" + ts), s_)
    reg = dict(ts=ts, backups={"um.py": dict(backup=bu["path"], bytes=bu["bytes"], sha16=bu["sha256"][:16]),
                               "um_absoluto_selo.json": dict(backup=bs["path"], bytes=bs["bytes"], sha16=bs["sha256"][:16])},
               um_py_novo=dict(bytes=len(un), sha16=sha(un)[:16], origem="SINTETICO (sandbox R3.4)"))
    gravar_novo(CS / v_novo / ("APLICADO_AO_CANONICO_" + ts + ".json"), json.dumps(reg, ensure_ascii=False, indent=1).encode("utf-8"))
reg_rev = dict(ts="20261001_090000", backups={"um.py": dict(backup=str(CS / "_nos" / "um.py.bak_20261001_100000"), bytes=len(um), sha16=sha(um)[:16])},
               um_py_novo=dict(bytes=1, sha16="0" * 16, origem="SINTETICO: tentativa revertida (o gerador a ignora)"))
gravar_novo(CS / "v392" / "APLICADO_AO_CANONICO_20261001_090000.json", json.dumps(reg_rev, ensure_ascii=False, indent=1).encode("utf-8"))

'''
sub('# fx/eventos_sandbox.jsonl = copia do livro real (so lido) + elos ENCADEADOS de ensaio', EXTRA + '# fx/eventos_sandbox.jsonl = copia do livro real (so lido) + elos ENCADEADOS de ensaio')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
