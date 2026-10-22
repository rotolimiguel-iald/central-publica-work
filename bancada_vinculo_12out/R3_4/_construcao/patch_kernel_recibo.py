# -*- coding: utf-8 -*-
"""patch de construcao (R3.4): verificar_kernel_recibo -- contrato KERNEL_RECIBO_R3_4 (modulos_de_auditoria) em ../sincronizar_bancada.py."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "sincronizar_bancada.py"
t = P.read_text(encoding="utf-8")


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:100])
    t = t.replace(old, new)


# 1) o contrato: R3_4, com a R3_2 ainda admitida
sub('''    if k.get("contrato") != KERNEL_CONTRATO:
        return falha("contrato=%r (exigido %s)" % (k.get("contrato"), KERNEL_CONTRATO))
''', '''    if k.get("contrato") not in KERNEL_CONTRATOS_ADMITIDOS:
        return falha("contrato=%r (exigido %s; a %s segue admitida)" % (k.get("contrato"), KERNEL_CONTRATO, KERNEL_CONTRATO_R3_2))
''')

# 2) modulos_de_auditoria: lista explicita, so no contrato R3_4, todos entre as pedras do recibo
sub('''    # R31-6 (R3.2): a decisao X19 do CRITERIOS pinado cruzada com as pedras do recibo: "sim" <=> a pedra LightNetStandardWedgeDataBGL.lean
''', '''    # R3.4 (M): os modulos de auditoria (so run_cmd/#print/import) sao listados pelo recibo, no contrato R3_4, e tem de ser pedras do recibo
    aud = k.get("modulos_de_auditoria")
    aud_set, auditorias = set(), {}
    if aud is not None:
        if k["contrato"] != KERNEL_CONTRATO:
            return falha("modulos_de_auditoria so existe no contrato %s (o recibo e %s) (R3.4)" % (KERNEL_CONTRATO, k["contrato"]))
        if not lista_de_texto(aud) or len(set(aud)) != len(aud):
            return falha("MODULOS_DE_AUDITORIA_INVALIDOS: modulos_de_auditoria exige lista nao vazia de caminhos de pedras, sem repeticao (R3.4)")
        fora_das_pedras = sorted(set(aud) - vistos)
        if fora_das_pedras:
            return falha("MODULO_DE_AUDITORIA_FORA_DAS_PEDRAS: %s nao e pedra do recibo (R3.4)" % fora_das_pedras[:3])
        aud_set = set(aud)
    # R31-6 (R3.2): a decisao X19 do CRITERIOS pinado cruzada com as pedras do recibo: "sim" <=> a pedra LightNetStandardWedgeDataBGL.lean
''')

# 3) a N1k: o modulo de auditoria dispensa as declaracoes, mas a fonte e conferida por script
sub('''    for p in pedras:
        dl = p.get("declaracoes")
        if not lista_de_texto(dl) or len(set(dl)) != len(dl):
''', '''    for p in pedras:
        dl = p.get("declaracoes")
        if p["path"] in aud_set:
            # R3.4 (M): o modulo de auditoria nao tem declaracoes (se as tivesse, seria pedra comum: ambiguidade recusada); a fonte so tem comandos de auditoria
            if dl not in (None, []):
                return falha("MODULO_DE_AUDITORIA_COM_DECLARACOES: %s esta em modulos_de_auditoria e traz declaracoes %s; um modulo de auditoria nao declara nada (R3.4)" % (p["path"], dl))
            av = auditar_fonte_de_auditoria(fontes[p["path"]])
            if not av["ok"]:
                return falha("MODULO_DE_AUDITORIA_FORA_DA_LISTA_DE_COMANDOS: %s: %s (R3.4)" % (p["path"], av["motivo"]))
            auditorias[p["path"]] = av["contagem"]
            continue
        if not lista_de_texto(dl) or len(set(dl)) != len(dl):
''')

# 4) o pino e a mensagem
sub('''    pino.update(contrato=KERNEL_CONTRATO, logs=dict(''', '''    pino.update(contrato=k["contrato"], logs=dict(''')
sub('''                n_pedras=len(pedras), n_declaracoes_das_pedras=n_decl, pedras_cobrem_o_diff_formal=True,
''', '''                n_pedras=len(pedras), n_declaracoes_das_pedras=n_decl, pedras_cobrem_o_diff_formal=True,
                modulos_de_auditoria=dict(lista=sorted(aud_set), n=len(aud_set), fontes_conferidas_por_script=True, contagem_de_comandos=auditorias,
                                          limite="o corpo do run_cmd e codigo executado na compilacao: o script confere comandos de topo e uma lista fechada de palavras; nao prova a inocuidade semantica do corpo"),
''')
sub('''        pino["sha256"][:16], KERNEL_CONTRATO, versao, len(pedras), n_decl,''', '''        pino["sha256"][:16], k["contrato"], versao, len(pedras), n_decl,''')
sub('''%d pedras (%d declaracoes no axiom_report, no log e na fonte) + raiz + Audit''', '''%d pedras (%d declaracoes no axiom_report, no log e na fonte; %d modulo(s) de auditoria sem declaracoes, fonte conferida por script) + raiz + Audit''')
sub('''len(pedras), n_decl, str(kinfo.get("sha256"))[:16], len(nomes_print),''', '''len(pedras) - len(aud_set), n_decl, len(aud_set), str(kinfo.get("sha256"))[:16], len(nomes_print),''')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
