# -*- coding: utf-8 -*-
"""gerar_derivacao_pos_rito_v401.py -- REGISTRA a derivacao do pos_rito da v401: roda o MOTOR (derivar_v401_motor) sobre as entradas de pos_rito/ dos lotes F, G, H e I (SEM --refazer: um derivado que ja existe e e' IGUAL ao que as regras produzem sai 'igual'; que difere sai
'EXISTE_E_DIFERE__nao_sobrescrevi' e e' dito) e escreve pos_rito/DERIVACAO_v401.json com o sha256 de entrada e de saida de cada arquivo, as regras de contagem exata e o que foi ESCRITO A MAO (textos_v401.py e registrar_mapa_v401.py: conteudo novo da v401).
NUNCA executa o derivado; so' ast.parse (feito pelo motor). Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v401.py"""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_encanamento_v401 as D  # noqa: E402  (executa os lotes de regras no escopo dele; nao roda o main)
import derivar_v401_motor as M  # noqa: E402

rel = []
for src, dst, regras, prot_extra, com_bump, autoral, origem in D.ENTRADAS:
    if not dst.startswith("pos_rito/"):
        continue
    r = M.derivar(src, dst, regras, prot_extra, com_bump, False, origem=origem)
    r["autoral_depois_da_subida"] = autoral; r["n_regras"] = len(regras)
    rel.append(r)
    print("%-46s %-34s %s regras=%d" % (dst, r["estado"], r["destino_sha256"][:12], len(regras)))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
a_mao = {n: {"sha256": sha(os.path.join(HERE, n)), "nota": nota} for n, nota in (
    ("textos_v401.py", "ESCRITO A MAO (conteudo novo da v401: a falsidade (simulacro) da inercia); a semente mecanica veio de textos_v399.py subido pelo motor e foi reescrita"),
    ("registrar_mapa_v401.py", "ESCRITO A MAO (1 rota nova e 8 anotacoes); a semente mecanica veio de registrar_mapa_v399.py"))}
out = {"contrato": "DERIVACAO_POS_RITO_v401", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False, "origem": "pos_rito da v399 (a cadeia de conteudo que rodou em 24/10), mapa 398 -> 400 e 399 -> 401, com as licoes da v400 (lotes G e H)",
       "lotes": ["derivar_encanamento_v401_regrasF.py", "derivar_encanamento_v401_regrasG.py", "derivar_encanamento_v401_regrasH.py", "derivar_encanamento_v401_regrasI.py"], "arquivos": rel, "escritos_a_mao": a_mao}
dst = os.path.join(HERE, "DERIVACAO_v401.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v401.json gravado (%d derivados, %d escritos a mao)" % (len(rel), len(a_mao)))
bad = [r["destino"] for r in rel if r["estado"] not in ("igual", "gravado")]
sys.exit(1 if bad else 0)
