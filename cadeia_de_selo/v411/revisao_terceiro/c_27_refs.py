import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
P = V.replace("\\", "/")
fontes = ["pos_rito/chain_pos_rito_v411.sh", "rito_v411.sh", "orquestrador/pos_treino_v411.py", "pos_rito/superficies_v411.py", "pos_rito/fechar_v411.py",
          "pos_rito/textos_custodia_handoff_v411.py", "pos_rito/registrar_mapa_v411.py", "pos_rito/leitura_v411.py", "instalar_v411.py", "reverter_v411.py",
          "pos_rito/gerar_x_custodia_v411.py", "pos_rito/fila_memoria_v411.py", "pos_rito/b3_recibo_v411.py", "pos_rito/blocos_custodia_v411.py", "conferir_rito_v411.py",
          "cadeia_v411.sh", "fim_de_cadeia_v411.sh", "p00_precondicoes_v411.py", "gerar_relatorio_v411.py"]
pat = re.compile(r"\b([A-Za-z0-9_./-]*[A-Za-z0-9_]+_v411[A-Za-z0-9_]*\.(?:py|json|sh|md|txt|pysnip|semente))\b")
def existe(n):
    return any(os.path.exists(P + "/" + d + n) for d in ("", "pos_rito/", "bancada_B3_servico/", "kernel/", "bateria_pre_selo/", "orquestrador/"))
saidas = re.compile(r"(rito_horarios|rito_servidor|rito_v411_sinal|rodada_v411_stdout|APLICADO_AO_CANONICO|RECIBO_|conferencia_rito_v411|registro_mapa_v411|ORDEM_HANDOFF|HANDOFF_v411|handoff-v411|leitura_v411_out|CUSTODIA_v411|_out_v411|tentativa|ESTADO|REGISTRADO|v411_selada|PINOS_BATERIA|BATERIA_VINCULO|PINO_UM_PY|quarentena|pilar_anterior|derivacao_out|arvore_dry|cadeia_v411_out|refazer_out|CONFERENCIA_|RESULTADO_|DERIVACAO|PRECONDICOES|PREPARACAO|VARREDURA|RELATORIO|PLANO_|purga_v411\.json|LOGS_COPIADOS|ensaio_a_seco_v411\.json|COMPARACAO|CANDIDATO_v411|FLAGS_v411|KH_N1|GUARDA_|TESTE_|PROVA_PRODUCAO|PINO_RECIBO|SIMULACAO|EXAME_PONTOS|FORMAL_MAP|MANIFESTO|ESPERADOS|VERBATIM|TOPO_RATIFICADO|PINOS_BN|ACORDO|DESENHO|PEDIDOS|pronto|PRONTO|REVISAO_TERCEIRO|SESSION_REFERENCE|registro_mapa)")
tot = {}
for f in fontes:
    t = rd(P + "/" + f)
    for ln, l in enumerate(t.split("\n"), 1):
        if l.lstrip().startswith("#"):
            continue
        for m in pat.finditer(l):
            n = m.group(1)
            base = os.path.basename(n)
            if saidas.search(base):
                continue
            if not existe(base) and not os.path.exists(P + "/" + n):
                tot.setdefault(base, []).append("%s:%d" % (os.path.basename(f), ln))
for k, v in sorted(tot.items()):
    print(k, "<-", v[:5])
print("fim; referencias nao achadas:", len(tot))
