# -*- coding: utf-8 -*-
"""_desfazer_pedras_r2_v408.py -- (claude-construtor-v408-r2, a servico da gerencia c1, 05/11/2026) a MUDANCA DE INSUMO da gerencia de 05/11 ~01h25
(a revisao de terceiro R1 nao aprovou; MEDIO 1, opcao B: o PIgualNP R3 define em Lean Problema, ClasseP, ClasseNP e prova p_igual_np_nas_classes_do_dicionario, 18 ancoras;
as outras tres pedras so' perderam CANDIDATA no cabecalho; sha256 em insumos\\RECIBO_PEDRAS_v408_NOMES.json de 05/11 01:25) chegou DEPOIS de o preparar_bundle_v408 ter gravado
as versoes de 04/11 noite no sandbox C:\\t\\k408c\\final e de o kernel ter sido construido com elas. COPIA do _desfazer_pedras_r1_v408.py (o mecanismo usado em 04/11 noite),
so' com os rotulos r1 -> r2; DESFAZ com BACKUP DE BYTES de tudo o que toca (nada e' apagado sem copia conferida por sha256): (1) TGLExt/<Nome>.lean das 4 pedras sai do sandbox
(para C:\\t\\k408c\\superado_r2_<TS>\\TGLExt\\), com os artefatos do build; (2) a raiz TGLExt.lean do sandbox NAO muda (CONFERIDO); (3) em v408\\: pedra\\<Nome>.lean e
pedra\\origem\\<Nome>.lean vao para pedra\\superado_r2_<TS>\\; kernel_modulos_novos_v408.json e BUNDLE_v408.json ganham .bak_<TS>_r1 (sufixo herdado) e saem; os arquivos de kernel\\
vao para kernel\\superado_r2_<TS>\\. Grava RECIBO_DESFAZER_PEDRAS_R2_v408_<TS>.json. Nunca toca o Nos (so' le a raiz). Uso: python -I -B -X utf8 _desfazer_pedras_r2_v408.py"""
import datetime, hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
K8 = os.path.join("C:" + os.sep, "t", "k408c", "final")
SUP = os.path.join("C:" + os.sep, "t", "k408c", "superado_r2_" + TS)
NOS_RAIZ = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "tgl_kernel", "TGLExt.lean")
NOMES = ["TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rec = {"quando": TS, "quem": "claude-construtor-v408-r2 (a servico da gerencia c1)", "motivo": "as 4 pedras vigentes de insumos\\ (RECIBO_PEDRAS_v408_NOMES.json de 05/11 01:25: PIgualNP R3 e cabecalhos sem CANDIDATA) diferem das gravadas no sandbox e em pedra\\ em 04/11 20:2x",
       "molde": "_desfazer_pedras_r1_v408.py", "movidos": [], "backups": [], "raiz": {}, "conferencia_antes": {}}


def mover(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    assert not os.path.exists(dst), dst
    h = sha(src); shutil.copy2(src, dst); assert sha(dst) == h; os.remove(src)
    rec["movidos"].append({"de": src, "para": dst, "sha256": h})


# (0) conferencia: o sandbox e pedra\ tem as R1 (iguais entre si), e a vigente de insumos\ difere delas
recibo = json.load(open(os.path.join(HERE, "insumos", "RECIBO_PEDRAS_v408_NOMES.json"), encoding="utf-8"))
vig = {os.path.splitext(os.path.basename(p["destino"]))[0]: p["sha256"] for p in recibo["pedras"]}
for n in NOMES:
    sb = os.path.join(K8, "TGLExt", n + ".lean"); pd = os.path.join(HERE, "pedra", n + ".lean")
    assert os.path.exists(sb) and os.path.exists(pd), ("o sandbox ou pedra\\ nao tem o modulo: nada a desfazer?", n)
    assert sha(sb) == sha(pd), ("o sandbox tem um modulo que NAO e' o de pedra\\ (R1): PARAR e avisar a gerencia", n)
    assert sha(os.path.join(HERE, "insumos", n + ".lean")) == vig[n], ("a fonte de insumos\\ nao e' a do recibo", n)
    og = os.path.join(HERE, "pedra", "origem", n + ".lean")
    assert os.path.exists(og) and sha(og) != vig[n], ("a origem gravada ja' e' a vigente: nada a desfazer", n)
    rec["conferencia_antes"][n] = {"sandbox_sha256": sha(sb), "pedra_sha256": sha(pd), "origem_r1_sha256": sha(og), "vigente_sha256": vig[n]}
# (1) os modulos e os artefatos do build deles
for n in NOMES:
    mover(os.path.join(K8, "TGLExt", n + ".lean"), os.path.join(SUP, "TGLExt"))
    for sub in (os.path.join(".lake", "build", "lib", "lean", "TGLExt"), os.path.join(".lake", "build", "ir", "TGLExt")):
        d = os.path.join(K8, sub)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.startswith(n + ".") or f == n:
                    q = os.path.join(d, f)
                    if os.path.isfile(q):
                        mover(q, os.path.join(SUP, sub))
# (2) a raiz: CONFERIDA (Nos + os 4 imports, na ordem do bundle), nao tocada
raiz_nos = open(NOS_RAIZ, "rb").read()
raiz_k8 = open(os.path.join(K8, "TGLExt.lean"), "rb").read()
nl = b"\r\n" if b"\r\n" in raiz_nos else b"\n"
sufixo = nl.join(b"import TGLExt." + n.encode() for n in NOMES) + nl
assert raiz_k8 == raiz_nos + sufixo, "a raiz do sandbox nao e' a do Nos + os 4 imports na ordem do bundle: PARAR"
rec["raiz"] = {"sha256": hashlib.sha256(raiz_k8).hexdigest(), "igual_ao_nos_mais_os_4_imports": True, "tocada": False}
# (3) a pasta v408
for n in NOMES:
    for sub in ("", "origem"):
        q = os.path.join(HERE, "pedra", sub, n + ".lean") if sub else os.path.join(HERE, "pedra", n + ".lean")
        if os.path.exists(q):
            mover(q, os.path.join(HERE, "pedra", "superado_r2_" + TS, sub) if sub else os.path.join(HERE, "pedra", "superado_r2_" + TS))
for nome in ("kernel_modulos_novos_v408.json", "BUNDLE_v408.json"):
    q = os.path.join(HERE, nome)
    if os.path.exists(q):
        b = q + ".bak_%s_r1" % TS; shutil.copy2(q, b); assert sha(b) == sha(q); rec["backups"].append(b); os.remove(q)
kd = os.path.join(HERE, "kernel")
if os.path.isdir(kd):
    dst = os.path.join(kd, "superado_r2_" + TS); os.makedirs(dst)
    for f in sorted(os.listdir(kd)):
        q = os.path.join(kd, f)
        if os.path.isfile(q):
            mover(q, dst)
json.dump(rec, open(os.path.join(HERE, "RECIBO_DESFAZER_PEDRAS_R2_v408_%s.json" % TS), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("desfeito:", len(rec["movidos"]), "arquivos movidos;", len(rec["backups"]), "backups; raiz do sandbox == Nos + 4 imports (nao tocada):", rec["raiz"]["igual_ao_nos_mais_os_4_imports"])
