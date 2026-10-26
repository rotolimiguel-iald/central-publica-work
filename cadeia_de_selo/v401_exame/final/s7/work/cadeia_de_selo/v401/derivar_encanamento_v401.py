# -*- coding: utf-8 -*-
"""derivar_encanamento_v401.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v401 a partir dos das cadeias v400 (a que foi USADA no rito real de 24/10; origem "v400") e v399 (a cadeia de CONTEUDO, com modulo novo de
kernel; origem "v399"), com o motor derivar_v401_motor: o mapa das versoes com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v401 faz DIFERENTE da origem.
O que a v401 muda no encanamento, dito uma vez: (a) a base e' a v400 SELADA e a Bancada JA pina a v400 (nao ha base_v398); (b) UM modulo novo no kernel (a pedra FalsidadeDaInercia), logo os scripts do kernel e as listas de modulos sao os da cadeia de CONTEUDO (v399);
(c) o B(n) e' um PASSO SIMPLES v400 -> v401 e o recibo pre_selo e' GERADO e PINADO antes da instalacao (como na v399); (d) as LICOES da v400 ficam: as guardas ESTATICAS da Bancada sobre o candidato (no ensaio, no conferidor C15/C16 e na leitura), a comparacao dos
vizinhos por string inteira, a troca dita explicada chave por chave, o motor que nao sobe etiquetas de stdout.
AUTORAIS (escritos a mao para a v401): delta, registros, runtime, gerar_candidato, comparar, os .pysnip, copiar_base, copiar_k401c.sh.
uso: python -I -B -X utf8 derivar_encanamento_v401.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v401_motor as M  # noqa: E402
from derivar_v401_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v400"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v401_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
    exec(open(os.path.join(HERE, _rf), encoding="utf-8").read(), globals())


def main():
    args = sys.argv[1:]
    refazer = "--refazer" in args
    so = None
    if "--so" in args:
        i = args.index("--so"); so = set(a for a in args[i + 1:] if not a.startswith("--"))
    rel = []
    for src, dst, regras, prot_extra, com_bump, autoral, origem in ENTRADAS:
        if so and os.path.basename(dst) not in so and dst not in so:
            continue
        r = M.derivar(src, dst, regras, prot_extra, com_bump, refazer, origem=origem); r["autoral_depois_da_subida"] = autoral; rel.append(r)
        print("%-46s %-12s %s regras=%d (origem %s)" % (dst, r["estado"][:12], r["destino_sha256"][:12], len(regras), origem))
    if not so:
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v401", "executado": False, "mapa": "origem v400: 399->400, 400->401; origem v399: 398->400, 399->401; fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
