# -*- coding: utf-8 -*-
"""derivar_encanamento_v405.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v405 a partir dos da cadeia v404 FINAL (a que foi USADA no rito real de 28/10 e na custodia de 29/10; origem unica "v404"), com o motor derivar_v405_motor: o mapa das versoes (403 -> 404, 404 -> 405)
com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v405 faz DIFERENTE da origem.
O que a v405 muda no encanamento, dito uma vez: (a) a base e' a v404 SELADA (um.py 3820476c83267f61) e a Bancada JA pina a v404 (B13, B13-v404-20261028-R1): o B(n) e' um PASSO SIMPLES v404 -> v405 (grava B14); (b) OITO modulos novos no kernel (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal,
LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion -- os NOMES do operador), logo os scripts do kernel e as listas de modulos sao de N = 8 pedras (o delta traz STONES com oito); (c) OITO registros com FUNCAO (um por pedra), lidos no main logo DEPOIS dos tres registros da v404 (projecao transversal, jo8v32 e a errata de F2b: a licao 1 da v404 -- as chaves do core
que eles leem ja' atribuidas), mais os specs cunhagens_v405, nomes_e_hipoteses_descarregadas_v405 e kh_n1_cobertura_v405; (d) os registros da v404 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404, cunhagens_v404, kh_n1_cobertura_v404) passam a ser RECRIADOS e comparados com os da v404 selada, como foram os da v403 na v404;
(e) as LICOES da v404 ficam (a guarda de ordem de chamada no ensaio; o reverter nao restaura o manifesto do kernel [a gerencia o faz da base]; o recibo de parada da Bancada com o PID lido da porta; os rotulos 10a/10b/10c da cadeia); (f) NOVO: a errata E10 ao lado de neutrino_mass.angle_status (o antigo e a E7 ficam) e a secao «A identidade» do artigo (o ensaio do operador verbatim, r2).
AUTORAIS (escritos a mao para a v405): delta, registros, runtime, gerar_candidato, gerar_esperados, comparar, os .pysnip, copiar_base, copiar_pedras, gerar_pino_das_pedras, copiar_insumos, copiar_k405c.sh, preparar_kernel, construir_kernel, copiar_logs_do_kernel, pos_rito/textos_v405_novo.pysnip e montar_textos.
uso: python -I -B -X utf8 derivar_encanamento_v405.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v405_motor as M  # noqa: E402
from derivar_v405_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v404"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v405_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
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
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v405", "executado": False, "mapa": "origem v404: 403->404, 404->405; fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
