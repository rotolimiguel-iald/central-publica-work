# -*- coding: utf-8 -*-
"""derivar_encanamento_v402.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v402 a partir dos da cadeia v401 FINAL (a que foi USADA no rito real de 25/10; origem unica "v401"), com o motor derivar_v402_motor: o mapa das versoes (400 -> 401, 401 -> 402)
com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo. Cada regra explica o que a v402 faz DIFERENTE da origem.
O que a v402 muda no encanamento, dito uma vez: (a) a base e' a v401 SELADA (um.py 1925cb691e933ae8) e a Bancada JA pina a v401 (B10): o B(n) e' um PASSO SIMPLES v401 -> v402 (grava B11); (b) TRES modulos novos no kernel (PonteDaEscalaDual do Codex, QuedaSemGeometria, EsperancaCondicional), logo os scripts do kernel
e as listas de modulos sao de N pedras (o delta traz STONES com tres); (c) TRES registros com FUNCAO (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402) lidos no main logo depois da falsidade_da_inercia_v401, mais os specs cunhagens_v402 e kh_n1_cobertura_v402; (d) os registros da v401
(falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) passam a ser RECRIADOS e comparados com os da v401 selada, como foram os da v399 na v401; (e) as LICOES da v401 ficam (guardas ESTATICAS da Bancada sobre o candidato, comparacao dos vizinhos por string inteira, a troca dita explicada chave por chave);
(f) NOVO no pos-rito: a FILA DA MEMORIA (memoria.py pinar) depois do passo das superficies.
AUTORAIS (escritos a mao para a v402): delta, registros, runtime, gerar_candidato, comparar, os .pysnip, copiar_base, copiar_k402c.sh, copiar_pedras, gerar_estado, gerar_registro_mapa_prep, textos e registrar_mapa do pos-rito.
uso: python -I -B -X utf8 derivar_encanamento_v402.py [--so NOME ...] [--refazer]"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v402_motor as M  # noqa: E402
from derivar_v402_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v401"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v402_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
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
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v402", "executado": False, "mapa": "origem v401: 400->401, 401->402; fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
