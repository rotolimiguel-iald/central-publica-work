# -*- coding: utf-8 -*-
"""derivar_encanamento_v400.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v400 a partir dos da v399 (cadeia_de_selo\\v399, a que foi USADA no rito real de 24/10), com o motor derivar_v400_motor:
o mapa 398 -> 399 e 399 -> 400 (a versao anterior da cadeia e a desta) com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v400 faz DIFERENTE da v399.
O que a v400 muda no encanamento, dito uma vez: (a) a base e' a v399 SELADA (nao a v398); (b) NENHUM modulo novo no kernel (STONES = []); a Bancada, que ainda pina a v398, ve o diff v398 -> v400 (DL.STONES_DESDE_B8); (c) o B(n) e' um PASSO SIMPLES v398 -> v400
(sem salto declarado: o esboco R3.5 recusa o elo v399); (d) o recibo pre_selo e' o da cadeia v399 (sobre o um.py v398, que a Bancada ainda pina), reconferido pelo PROPRIO esboco; (e) o alfa vem do programa (SEALED_CODATA_ALPHA).
AUTORAIS (escritos a mao para a v400): delta, registros, montar_runtime, acom_conferencias, gerar_candidato, guardas_estaticas_bancada, comparar, os .pysnip, copiar_base, copiar_k400c.sh.
uso: python -I -B -X utf8 derivar_encanamento_v400.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v400_motor as M  # noqa: E402
from derivar_v400_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v400_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
    exec(open(os.path.join(HERE, _rf), encoding="utf-8").read(), globals())


def main():
    args = sys.argv[1:]
    refazer = "--refazer" in args
    so = None
    if "--so" in args:
        i = args.index("--so"); so = set(a for a in args[i + 1:] if not a.startswith("--"))
    rel = []
    for src, dst, regras, prot_extra, com_bump, autoral in ENTRADAS:
        if so and os.path.basename(dst) not in so and dst not in so:
            continue
        r = M.derivar(src, dst, regras, prot_extra, com_bump, refazer); r["autoral_depois_da_subida"] = autoral; rel.append(r)
        print("%-46s %-12s %s regras=%d" % (dst, r["estado"][:12], r["destino_sha256"][:12], len(regras)))
    if not so:
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v400", "executado": False, "mapa": "398->399, 399->400 com fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
