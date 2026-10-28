# -*- coding: utf-8 -*-
"""derivar_encanamento_v403.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v403 a partir dos da cadeia v402 FINAL (a que foi USADA no rito real de 27/10; origem unica "v402"), com o motor derivar_v403_motor: o mapa das versoes (401 -> 402, 402 -> 403)
com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v403 faz DIFERENTE da origem.
O que a v403 muda no encanamento, dito uma vez: (a) a base e' a v402 SELADA (um.py 6a5033dc3f29324c) e a Bancada JA pina a v402: o B(n) e' um PASSO SIMPLES v402 -> v403; (b) TRES modulos novos no kernel (Caminho, Vida, VerdadeAdendo: os nomes do operador, 27/10/2026), logo os scripts do kernel
e as listas de modulos sao de N = 3 pedras (o delta traz STONES com tres); (c) QUATRO registros com FUNCAO (caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, a F8.1) lidos no main logo depois da esperanca_condicional_v402, mais os specs cunhagens_v403 e kh_n1_cobertura_v403;
(d) os registros da v402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402) passam a ser RECRIADOS e comparados com os da v402 selada, como foram os da v401 na v402; (e) as LICOES da v402 ficam (guardas ESTATICAS da Bancada sobre o candidato,
comparacao dos vizinhos por string inteira, a troca dita explicada chave por chave, a FILA DA MEMORIA no pos-rito); (f) NOVO: o gate (qg_closure) e' RECALCULADO pelo ensaio com a prove_qg_closure_gate nova (kwarg blind_null) sobre os dados do core selado, e o conferidor compara o qg_closure sem a lista de checks (que ganha a sonda nova).
AUTORAIS (escritos a mao para a v403): delta, registros, runtime, gerar_candidato, gerar_esperados, comparar, os .pysnip, copiar_pedras, gerar_pino_das_pedras, copiar_logs_do_kernel.
uso: python -I -B -X utf8 derivar_encanamento_v403.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v403_motor as M  # noqa: E402
from derivar_v403_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v402"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v403_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
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
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v403", "executado": False, "mapa": "origem v402: 401->402, 402->403; fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
