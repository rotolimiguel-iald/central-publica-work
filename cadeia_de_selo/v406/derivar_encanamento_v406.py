# -*- coding: utf-8 -*-
"""derivar_encanamento_v406.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v406 a partir dos da cadeia v405 FINAL (a que foi USADA no rito real de 01/11 e na custodia de 02/11; origem unica "v405"), com o motor derivar_v406_motor: o mapa das versoes (404 -> 405, 405 -> 406)
com PROTECAO dos nomes nascidos no um.py, mais as regras de contagem exata por arquivo (os lotes derivar_encanamento_v406_regras*.py, subidos mecanicamente dos da v405 por _mk_lotes_v406.py).
ESTADO (02/11/2026, executor mecanico a servico da gerencia c1): so' a SUBIDA MECANICA. O que a v406 muda de verdade (o bundle de ~300 modulos F1Fecho394 no lugar das oito pedras da v405; B14 -> B15; a nova base v405 selada 0030242565cc13f6; as quatro chaves do selo se a gerencia as virar) NAO esta' nas regras:
as regras herdadas casam o texto da v404 e, onde o texto da v405 ja' mudou, o motor ABORTA com a contagem (fail-closed) -- e' a lista do que a gerencia tem de reescrever (ver DERIVACAO_v406_NOTAS.md e DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA.json).
AUTORAIS (a escrever pela gerencia para a v406; ver a receita, secao 5): delta completo (aqui so' o esqueleto de encanamento delta_v406.py), registros, runtime, gerar_candidato, gerar_esperados, comparar, os .pysnip, copiar_pedras, gerar_pino_das_pedras, copiar_insumos, construir_kernel, copiar_logs_do_kernel, textos_v406_novo.pysnip, montar_textos e guarda_ordem_de_chamada.
uso: python -I -B -X utf8 derivar_encanamento_v406.py [--so NOME ...] [--refazer]"""
import json, os, sys, datetime
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v406_motor as M  # noqa: E402
from derivar_v406_motor import entre, sub_n  # noqa: E402,F401
ENTRADAS = []


def entrada(src, dst=None, regras=(), prot_extra=(), com_bump=True, autoral=False, origem="v405"):
    ENTRADAS.append((src, dst or (M.bump(src, prot_extra, origem) if com_bump else src), list(regras), tuple(prot_extra), com_bump, autoral, origem))


LOTES_NAO_CARREGADOS = []
for _rf in sorted(f for f in os.listdir(HERE) if f.startswith("derivar_encanamento_v406_regras") and f.endswith(".py")):   # lotes de regras (exec no escopo deste arquivo)
    _n0 = len(ENTRADAS)
    try:
        exec(open(os.path.join(HERE, _rf), encoding="utf-8").read(), globals())
    except Exception as _e:      # AJUSTE v406 (a v405 deixava o import inteiro cair): um lote cujo PREAMBULO nao carrega (ex.: precisa do delta completo da v406) e' REGISTRADO, suas entradas parciais saem, e os demais lotes seguem. Nenhuma regra e' forcada.
        del ENTRADAS[_n0:]
        import traceback as _tb
        _fr = [x for x in _tb.extract_tb(_e.__traceback__) if x.filename == "<string>"]    # o quadro do codigo do proprio lote (a linha dele que falhou)
        LOTES_NAO_CARREGADOS.append({"lote": _rf, "erro": "%s: %s" % (type(_e).__name__, _e), "linha_do_lote": (_fr[-1].lineno if _fr else None)})
        print("LOTE NAO CARREGADO (fail-closed neste lote; os demais seguem): %s -> %s: %s" % (_rf, type(_e).__name__, str(_e)[:200]))


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
        out = os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v406.json")
        txt = json.dumps({"contrato": "DERIVACAO_ENCANAMENTO_v406", "executado": False, "mapa": "origem v405: 404->405, 405->406; fronteira de digitos e protecao dos nomes nascidos no um.py", "lotes_nao_carregados": LOTES_NAO_CARREGADOS, "arquivos": rel}, ensure_ascii=False, indent=1).encode("utf-8")
        if os.path.exists(out):                                    # backup de BYTES antes de substituir; nunca open(p, "w") direto em arquivo existente
            open(out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(out, "rb").read())
        open(out + ".tmp", "wb").write(txt); os.replace(out + ".tmp", out)


if __name__ == "__main__":
    main()
