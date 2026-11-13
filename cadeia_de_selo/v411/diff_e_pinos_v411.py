# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] ESCRITO a partir do molde v410/diff_e_pinos_v410.py para uma versao SEM modulo novo: o diff do kernel tem de sair VAZIO (nada novo, nada removido, nada mudado); os pinos herdados vem de v410\PINOS_BN_v410.json (recalculados do arquivo); os pinos NOVOS sao os do teste H0DN x BG1 aberto (as copias duraveis dos 18 insumos e dos 7 citados), as falas congeladas e as fontes autorais do registro
"""diff_e_pinos_v411.py -- (1) DIFF_KERNEL_v411.txt: arquivos novos, removidos e mudados do kernel embutido do candidato contra o da v410 (a v411 NAO tem modulo novo: as tres listas tem de sair VAZIAS; senao PARA); (1b) DIFF_v410_v411.diff:
`diff -u` do um.py da v410 selada (base_v410) contra o candidato (o registro da subida; texto, nao e' prova de nada); (2) PINOS_BN_v411.json: os sha256 que o elo B(n) pede (esboco R3.5, gerador e driver da bateria, base R2, CRITERIOS,
recibo do kernel, recibo pre_selo, selo e manifesto do kernel da v410 SELADA) e os pinos NOVOS da v411 (as copias duraveis dos 18 insumos embutidos e dos 7 citados do H0DN x BG1, conferidas contra o sha256 do delta; a lista
congelada das falas; as fontes autorais do registro e do quadro; FLAGS e KH_N1), LIDOS dos arquivos por script (path e sha256 recalculados aqui; nada digitado). O que so' passa a existir depois de outro passo (o recibo pre_selo,
o CRITERIOS da v411, o ESPERADOS) sai `NAO_PREPARADO` e entra em `pendentes`: pendente, nao erro. Com V411_ENSAIO_TOPO_PROPOSTO=1 o candidato e' o ARTEFATO DE ENSAIO do topo proposto (NAO e' candidato) e as tres saidas vao para a
pasta de ensaio (fora de work\\). Nao ha salto de versoes (a Bancada pina a v410 e o Nos e' a v410). uso: python -I -B -X utf8 diff_e_pinos_v411.py   (roda DEPOIS de gerar_esperados_v411.py)"""
import ast, difflib, hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v411 as DL  # noqa: E402
CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR)
assert sha(open(DL.CANDIDATO_ARQ, "rb").read())[:16] == CM["sha16"], "o manifesto nao e' do arquivo"
E0, _, _, h0 = carregar(os.path.join(BASE, "um.py")); E1, _, _, h1 = carregar(DL.CANDIDATO_ARQ)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v410 (%s) -> v411 (%s)%s" % (h0, h1, " [ENSAIO do topo proposto: NAO e' candidato]" if DL.ENSAIO_TOPO_PROPOSTO else ""), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)] + ["  ~ " + k for k in mudados]
out += ["", "a v411 NAO tem modulo novo: o kernel embutido e' o da v410 byte a byte (%d arquivos)" % len(E1)]
open(DL.saida("DIFF_KERNEL_v411.txt") + ".tmp", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n"); os.replace(DL.saida("DIFF_KERNEL_v411.txt") + ".tmp", DL.saida("DIFF_KERNEL_v411.txt"))
print("\n".join(out[:1]), "| novos", len(novos), "removidos", len(removidos), "mudados", len(mudados))
assert not novos and not removidos and not mudados and CM["kernel"]["modulos_novos"] == 0 and len(E1) == len(E0) == CM["formal_files_n"], ("o kernel embutido da v411 tem de ser o da v410 byte a byte", novos, removidos, mudados)
# (1b) o diff do um.py inteiro: diff -u do sistema (difflib seria quadratico em 46 MB); a base e' a copia de bytes do Nos v410 selado
_dif = shutil.which("diff"); _ddp = DL.saida("DIFF_v410_v411.diff"); _ddm = {"ferramenta": _dif}
if _dif:
    _r = subprocess.run([_dif, "-u", "--label", "um.py v410 %s" % h0, "--label", "um.py v411 %s" % h1, os.path.join(BASE, "um.py"), DL.CANDIDATO_ARQ], capture_output=True)
    assert _r.returncode in (0, 1), ("diff -u falhou", _r.returncode, _r.stderr[:300])
    open(_ddp + ".tmp", "wb").write(_r.stdout); os.replace(_ddp + ".tmp", _ddp); _ddm.update({"rc": _r.returncode, "bytes": len(_r.stdout), "sha256": sha(_r.stdout)})
else:
    _ddm.update({"estado": "NAO_GERADO: diff -u nao esta no PATH"})
print("DIFF_v410_v411.diff:", {k_: (v_[:16] if isinstance(v_, str) and len(v_) == 64 else v_) for k_, v_ in _ddm.items()})
V = os.path.join(HERE, "vinculo")
f = lambda p, **kw: dict({"path": p, "sha256": sha(open(p, "rb").read()), "bytes": os.path.getsize(p)}, **kw) if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
_pino_pr = DL.saida("PINO_RECIBO_PRE_SELO_v411.json"); pendentes = []
if os.path.exists(_pino_pr):
    pr = json.load(open(_pino_pr, encoding="utf-8"))
    assert sha(open(pr["path"], "rb").read()) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
    rp = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"], "pino_do_pino": f(_pino_pr),
          "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"], "sem_salto": True}
else:   # o B(n) pre-selo ainda nao rodou (bateria_pre_selo\rodar_bn_pre_selo_v411.sh): PENDENTE, nao erro
    pr = None; rp = {"path": _pino_pr, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "PINO_RECIBO_PRE_SELO_v411.json ainda nao existe: o B(n) pre-selo da v411 nao rodou"}; pendentes.append("recibo_pre_selo")
P10 = json.load(open(os.path.join(DL.V410, "PINOS_BN_v410.json"), encoding="utf-8"))   # a fusao R3.4/R3.5: o esboco, o gerador e o driver da bateria, a base R2 (so' leitura; o sha e' RECALCULADO do arquivo)


def do_v410(k):
    d = P10[k]; assert os.path.exists(d["path"]) and sha(open(d["path"], "rb").read()) == d["sha256"], ("o pino herdado da v410 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v410.json[%s] (recalculado do arquivo)" % k)


kr = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v411.json"), encoding="utf-8"))
assert kr["versao"] == DL.UM_VERSION and kr["pedras"] == [] and kr["rc"] == 0, "o recibo do kernel da v411 (nenhuma pedra nova)"
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v411.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v411.json"), contrato=kr["contrato"], n_pedras=len(kr["pedras"]), n_modulos=len(kr["pedras"]), modulos_de_auditoria=kr.get("modulos_de_auditoria", [])),
      "candidato": f(DL.CANDIDATO_ARQ, papel=DL.ROTULO_DO_ARTEFATO), "esperados": f(DL.saida("ESPERADOS_v411.json")), "pins_do_candidato": f(DL.PINS_ARQ),
      "esboco_R3_5": do_v410("esboco_R3_5"), "gerador_bateria": do_v410("gerador_bateria"), "driver_t12_t14": do_v410("driver_t12_t14"), "bateria_base_R2": do_v410("bateria_base_R2"),
      "bateria_do_pre_selo": (f(pr["bateria"]["path"], versao="v410", nota="a bateria do ensaio pre_selo (a da v410 gerada e pinada na cadeia anterior); a do POS_SELO da v411 e' GERADA pelo chain depois do selo") if pr else {"path": None, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "depende do recibo pre_selo"}),
      "recibo_pre_selo": rp,
      "selo_anterior_v410": f(os.path.join(BASE, "um_absoluto_selo.json"), nota="o selo da v410 (custodia, o FIM da cadeia anterior): --selo-anterior"),
      "kernel_manifesto_anterior_v410": f(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), nota="o manifesto do kernel da v410 (custodia): --kernel-manifesto-anterior"),
      "nota": "[REAL] lido dos arquivos por script (diff_e_pinos_v411.py): path e sha256 RECALCULADOS; sem salto de versoes (a Bancada de producao pina a v410 = o Nos de antes da instalacao), logo sem pino de cadeia de selos nem 3o argumento do b3_recibo; "
              "o esboco R3.5 e a bateria/driver sao os da cadeia anterior (R3_5), reaproveitados; o passo da Bancada na v411 e' o simples v410 -> v411 (o B(n) seguinte e' %s, lido de delta_v411.B_N_SEGUINTE; a Bancada pina %s); nenhum modulo novo no kernel (o recibo do kernel nao lista pedra)." % (DL.B_N_SEGUINTE, DL.BANCADA_PINA_HOJE["deployment_id"]),
      **DL.MARCA_ENSAIO}
if pr is None:
    pendentes.append("bateria_do_pre_selo")
if pn["esperados"].get("sha256") is None:
    pendentes.append("esperados")
    print("AVISO: ESPERADOS_v411.json ainda NAO existe (gerar_esperados_v411.py nao rodou): o pino dele sai NAO_PREPARADO e entra em `pendentes`")
if pn["criterios"].get("sha256") is None:   # (v411) o CRITERIOS da v411 nao e' escrito pelo pos_build_kernel_v411.py: PENDENTE dito (o que o consome e' o B(n) e o pos-rito)
    pendentes.append("criterios")
    print("AVISO: vinculo\\CRITERIOS_v411.json NAO existe (na v410 era escrito pelo pos_build_kernel; o da v411 nao o escreve): o pino sai NAO_PREPARADO e entra em `pendentes`")
# ---- [v411] os pinos NOVOS, lidos dos arquivos (path e sha256 RECALCULADOS) e conferidos contra o delta (o sha256 da tabela do DESENHO): as COPIAS duraveis em insumos\ (nada da pasta do Kimi)
_INS = os.path.join(HERE, "insumos")
for i_ in DL.INSUMOS_V411:
    pn["h0dn_insumo_" + i_["nome"]] = f(os.path.join(_INS, "h0dn_" + i_["nome"]), sha256_do_delta=i_["sha256"], papel=i_["papel"], reuso_v410=i_["reuso_v410"], nota="copia duravel do insumo EMBUTIDO (origem work\\%s)" % i_["rel"])
for c_ in DL.CITADOS_V411:
    pn["h0dn_citado_" + c_["nome"]] = f(os.path.join(_INS, "citado_" + c_["nome"]), sha256_do_delta=c_["sha256"], nota="copia duravel do CITADO por sha256, NAO embutido (origem %s)" % c_["rel"])
pn["verbatim_congelado"] = f(os.path.join(HERE, "VERBATIM_CONGELADO_v411.json"), n=DL.N_FALAS_V411, nota="a lista congelada das falas de 11 e 12/11 (so' citadas no programa, D181: o texto fica na casa)")
pn["manifesto_insumos"] = f(os.path.join(HERE, "MANIFESTO_INSUMOS_v411.json"), nota="as copias duraveis (insumos\\) == as origens, por sha256")
pn["kernel_flags"] = f(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v411.json"), n_flags=CM["n_bandeiras"])
pn["kernel_kh_n1"] = f(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO))
for _nome in ("registros_h0dn_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "registros_v411.py", "guarda_frases_v411.py", "delta_v411.py"):
    pn["fonte_" + _nome[:-len(".py")]] = f(os.path.join(HERE, _nome), nota="fonte autoral do construtor: o contrato, o texto, o quadro e os specs do registro sao DERIVADOS dela no gerador")
assert all(pn["h0dn_insumo_" + i_["nome"]].get("sha256") == i_["sha256"] for i_ in DL.INSUMOS_V411), "uma copia duravel de insumo do H0DN != o sha256 do DESENHO"
assert all(pn["h0dn_citado_" + c_["nome"]].get("sha256") == c_["sha256"] for c_ in DL.CITADOS_V411), "uma copia duravel de citado do H0DN != o sha256 do DESENHO"
assert all(i_["sha256"] == CM["h0dn"]["insumos"][i_["nome"]]["sha256"] for i_ in DL.INSUMOS_V411), "o candidato nao embute os insumos com o sha256 do DESENHO"
assert not any("kimi" in str((v_ or {}).get("path") or "").lower().split(os.sep) for v_ in pn.values() if isinstance(v_, dict)), "veto: nenhum pino da pasta do Kimi"
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None and k not in pendentes]
assert not bad, ("pino sem arquivo", bad)
pn["pendentes"] = pendentes
_pp = DL.saida("PINOS_BN_v411.json")
open(_pp + ".tmp", "w", encoding="utf-8").write(json.dumps(pn, ensure_ascii=False, indent=1)); os.replace(_pp + ".tmp", _pp)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v and not k.startswith(("h0dn_insumo_", "h0dn_citado_"))}); print("insumos/citados do H0DN pinados:", sum(1 for k in pn if k.startswith(("h0dn_insumo_", "h0dn_citado_"))), "| pendentes:", pendentes or "nenhum")
