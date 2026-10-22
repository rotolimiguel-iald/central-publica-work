# -*- coding: utf-8 -*-
# Auditor REPRO, item (3a): procurar beta (e alpha, thetaM, e derivados) LITERAL nos artefatos dos construtores.
# Varredura propria: tokens numericos (tokenize) + padroes de digitos significativos em qualquer forma
# (0.012031..., 1.2031e-2, 12031300..., 7.2973..., 0.10990..., 1-beta=0.98796..., pureza 0.97622..., 0.15605...).
import io, os, re, sys, json, tokenize, hashlib

W = "C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out\\"
ALVOS = [W + "2_OPTICO\\run_optico.py", W + "2_OPTICO\\conferir_freeze.py", W + "2_OPTICO\\impressao_digital_kernel.py",
         W + "3_KERNEL\\beta_runtime.py", W + "3_KERNEL\\varrer_fonte.py", W + "3_KERNEL\\rodar_lean.py",
         W + "3_KERNEL\\gerar_auditoria.py", W + "3_KERNEL\\analisar_auditoria.py", W + "3_KERNEL\\montar_resultado.py",
         W + "3_KERNEL\\sandbox_toolchain.py", W + "3_KERNEL\\conferir_freeze.py",
         W + "3_KERNEL\\sandbox\\TGLExt\\TheUnitIsTheRank.lean", W + "3_KERNEL\\sandbox\\AuditTheUnitIsTheRank.lean"]
# digitos significativos (sem ponto/expoente) das grandezas que nao podem aparecer literais
ASSINATURAS = {"beta": "1203130040", "beta_curto": "120313", "alpha": "72973525", "thetaM": "1099084307",
               "um_menos_beta": "98796869", "pureza_thM": "976226903", "frob_anticomm": "156051610",
               "sqrt_beta": "1096874", "dois_beta": "240626008", "sqrt_e": "164872127", "e": "271828182"}
out = {}
for p in ALVOS:
    b = open(p, "rb").read()
    t = b.decode("utf-8")
    r = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    # digitos corridos (remove ponto decimal e separadores para pegar qualquer grafia)
    so_dig = re.sub(r"[^0-9]", " ", t)
    hits = {}
    for nome, sig in ASSINATURAS.items():
        # procura a assinatura dentro de qualquer numero literal, ignorando o ponto decimal
        achados = []
        for m in re.finditer(r"\d+(?:[.,_]\d+)*(?:[eE][-+]?\d+)?", t):
            dig = re.sub(r"[^0-9]", "", m.group(0).split("e")[0].split("E")[0])
            dig = dig.lstrip("0")
            if sig in dig:
                linha = t.count("\n", 0, m.start()) + 1
                achados.append([linha, m.group(0)])
        if achados:
            hits[nome] = achados
    r["assinaturas_encontradas"] = hits
    # numeros com 4+ casas decimais ou mantissa longa (python: tokenize; lean: regex)
    longos = []
    if p.endswith(".py"):
        for tok in tokenize.tokenize(io.BytesIO(b).readline):
            if tok.type == tokenize.NUMBER:
                s = tok.string
                mant = re.sub(r"[eE].*", "", s).replace("_", "")
                if len(re.sub(r"[^0-9]", "", mant).lstrip("0")) >= 4 and "." in mant:
                    longos.append([tok.start[0], s])
    else:
        for m in re.finditer(r"(?<![\w.])\d+\.\d{3,}", t):
            longos.append([t.count("\n", 0, m.start()) + 1, m.group(0)])
    r["literais_numericos_longos"] = longos
    out[os.path.relpath(p, W)] = r
# lean: termos proibidos
for p in ALVOS:
    if p.endswith(".lean"):
        t = open(p, encoding="utf-8").read()
        sem_coment = re.sub(r"/-.*?-/", "", t, flags=re.S)
        sem_coment = re.sub(r"--[^\n]*", "", sem_coment)
        proib = {}
        for w in ("sorry", "admit", "axiom", "native_decide", "implemented_by", "extern", "opaque", "unsafe", "partial", "@[csimp]", "debug.skipKernelTC", "Lean.ofReduceBool", "decide := true"):
            n = len(re.findall(r"(?<![\w.])" + re.escape(w) + r"(?![\w])", sem_coment))
            if n:
                proib[w] = n
        out[os.path.relpath(p, W)]["termos_proibidos_fora_de_comentario"] = proib
        out[os.path.relpath(p, W)]["termos_proibidos_inclusive_comentario"] = {w: len(re.findall(r"(?<![\w.])" + re.escape(w) + r"(?![\w])", t)) for w in ("sorry", "admit", "axiom", "native_decide")}
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "A3a_LITERAIS.json")
open(SAIDA, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
