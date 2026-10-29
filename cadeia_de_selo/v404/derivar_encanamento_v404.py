# -*- coding: utf-8 -*-
"""derivar_encanamento_v404.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v404 a partir dos da cadeia v403 FINAL (a que foi USADA no rito real de 28/10; origem unica "v403"), com o motor derivar_v404_motor: o mapa das versoes (402 -> 403, 403 -> 404)
com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v404 faz DIFERENTE da origem.
O que a v404 muda no encanamento, dito uma vez: (a) a base e' a v403 SELADA (um.py 2ffe9edc7d7545bd) e a Bancada JA pina a v403 (B12): o B(n) e' um PASSO SIMPLES v403 -> v404; (b) DOIS modulos novos no kernel (ProjecaoTransversalDaMeiaNat, de nome PROVISORIO da gerencia, e Jo8v32, nome do operador),
logo os scripts do kernel e as listas de modulos sao de N = 2 pedras (o delta traz STONES com duas); (c) TRES registros com FUNCAO (projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404) lidos no main (os dois de pedra logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, depois dos insumos que ela le -- licao da 1a tentativa do rito, 28/10), mais os specs cunhagens_v404 e kh_n1_cobertura_v404;
(d) os registros da v403 (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403) passam a ser RECRIADOS e comparados com os da v403 selada, como foram os da v402 na v403; (e) as LICOES da v403 ficam (guardas ESTATICAS da Bancada, convencao do cabecalho do diario,
o recibo de parada da Bancada sem o nome do script do servico, alfa nunca como beta/raiz de e, a parafrase da gerencia nunca entre aspas); (f) NOVO: a errata ao lado de neutrino_mass.angle_status (o antigo fica no registro) e a errata ao lado da cobranca F2b (o V1 segue congelado por hash).
AUTORAIS (escritos a mao para a v404): delta, registros, runtime, gerar_candidato, gerar_esperados, comparar, os .pysnip, copiar_pedras, gerar_pino_das_pedras, copiar_logs_do_kernel, pos_rito/textos_v404_novo.pysnip e montar_textos.
uso: python -I -B -X utf8 derivar_encanamento_v404.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v404_motor as M  # noqa: E402
from derivar_v404_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v403"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v404_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
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
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v404", "executado": False, "mapa": "origem v403: 402->403, 403->404; fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
