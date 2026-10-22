# -*- coding: utf-8 -*-
"""patch de construcao (R3.4): main() -- flags --cadeia-de-selos[-sha256], pinos_da_versao da bateria, salto, marcadores do um.py. Aplica-se uma vez sobre
../sincronizar_bancada.py (cada trecho tem de existir exatamente uma vez)."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "sincronizar_bancada.py"
t = P.read_text(encoding="utf-8")


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:110])
    t = t.replace(old, new)


# (a) os argumentos
sub('''    ap.add_argument("--forcar-regeracao", action="store_true", help="regenera mesmo se a Bancada ja pina a versao alvo")
''', '''    ap.add_argument("--cadeia-de-selos", default=None, help="R3.4 (S): a CADEIA_DE_SELOS (contrato CADEIA_DE_SELOS_R3_4) entre a versao que a Bancada pina e a do Nos; obrigatoria em "
                                                          "--fase pre_selo quando a Bancada pina uma versao anterior a do Nos (salto); em pos_selo, junto do recibo pre-selo de um salto")
    ap.add_argument("--cadeia-de-selos-sha256", default=None, help="R3.4 (S): sha256 esperado da cadeia de selos (lido de vNNN_pins); obrigatorio com --cadeia-de-selos")
    ap.add_argument("--forcar-regeracao", action="store_true", help="regenera mesmo se a Bancada ja pina a versao alvo")
''')

# (b) os pinos da versao da bateria, conferidos contra o Nos que o esboco leu
sub('''        nos_info = ler_nos(nos_dir, a.versao)
        recibo["nos"] = {k: v for k, v in nos_info.items() if not k.startswith("_")}
''', '''        nos_info = ler_nos(nos_dir, a.versao)
        recibo["nos"] = {k: v for k, v in nos_info.items() if not k.startswith("_")}
        # R3.4 (P): a bateria por versao -- pinos_da_versao e testes pina_o_um_py conferidos contra o Nos lido agora (pino velho = recusa antes de qualquer gravacao)
        recibo["bateria"]["pinos_da_versao"] = conferir_pinos_da_versao(bateria, nos_info, a.versao)
''')

# (c) o salto: a cadeia de selos (pre_selo: Bancada atrasada; pos_selo: junto do recibo pre-selo de um salto)
sub('''        if a.recibo_pre_selo:                             # A6, N2
            recibo["recibo_pre_selo"] = conferir_recibo_pre_selo(a.recibo_pre_selo, anterior, bancada, ja_sincronizada, a.recibo_pre_selo_sha256,
                                                                 a.selo_anterior, a.kernel_manifesto_anterior)
''', '''        # R3.4 (S): o salto. Em pre_selo, se a Bancada pina uma versao anterior a do Nos, a cadeia de selos e OBRIGATORIA e e conferida por hash (inicio = a Bancada,
        # fim = o Nos lido agora); em pos_selo ela acompanha o recibo pre-selo de um salto (conferir_recibo_pre_selo). Cadeia sem salto e recusada (flag sem efeito).
        if a.cadeia_de_selos_sha256 and not a.cadeia_de_selos:
            raise Recusa("CADEIA_DE_SELOS_AUSENTE: --cadeia-de-selos-sha256 sem --cadeia-de-selos")
        cadeia, salto = None, None
        if a.cadeia_de_selos:
            cadeia = carregar_cadeia_de_selos(a.cadeia_de_selos, a.cadeia_de_selos_sha256)
            recibo["cadeia_de_selos"] = cadeia_para_recibo(cadeia)
        atrasada = a.fase == "pre_selo" and not ja_sincronizada and anterior["version"] != a.versao
        if atrasada:
            if versao_numero(anterior["version"]) > versao_numero(a.versao):
                raise Recusa("BANCADA_A_FRENTE_DO_NOS: a Bancada pina %s e o Nos tem %s; um salto so vai para a frente (R3.4)" % (anterior["version"], a.versao))
            if cadeia is None:
                raise Recusa("BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS: a Bancada pina %s e o Nos tem %s; o ensaio pre_selo de uma Bancada atrasada exige --cadeia-de-selos e "
                             "--cadeia-de-selos-sha256 (a cadeia de selos de %s a %s verificada por hash) (R3.4)" % (anterior["version"], a.versao, anterior["version"], a.versao))
            conferir_cadeia_com_a_bancada(cadeia, anterior)
            conferir_cadeia_com_o_fim(cadeia, a.versao, nos_info["um_py"]["sha256"], nos_info["selo"]["sha256"], (nos_info.get("kernel") or {}).get("sha256"), "o Nos lido agora")
            salto = montar_salto(cadeia, anterior)
            recibo["salto"] = salto
        elif cadeia is not None and not (a.fase == "pos_selo" and a.recibo_pre_selo):
            raise Recusa("CADEIA_DE_SELOS_SEM_SALTO: --cadeia-de-selos so serve a uma Bancada atrasada (pre_selo) ou ao recibo pre-selo de um salto (pos_selo) (R3.4)")
        if a.recibo_pre_selo:                             # A6, N2
            recibo["recibo_pre_selo"] = conferir_recibo_pre_selo(a.recibo_pre_selo, anterior, bancada, ja_sincronizada, a.recibo_pre_selo_sha256,
                                                                 a.selo_anterior, a.kernel_manifesto_anterior, cadeia)
            salto = recibo["recibo_pre_selo"].get("salto")
            if salto is not None:
                recibo["salto"] = salto
                if salto["proxima_a_selar"] != a.versao:
                    raise Recusa("SALTO_VERSAO_NAO_CONSECUTIVA: o recibo pre-selo e de um salto que termina em %s e a versao a sincronizar e %s (a seguinte seria %s) (R3.4)"
                                 % (salto["ate"]["versao"], a.versao, salto["proxima_a_selar"]))
''')

# (d) regenerar com o salto; veredito do salto
sub('''            novo, md, rotulo, n = regenerar(bancada, anterior, nos_info, a.versao, (evento or {}).get("evento"), script_sha, bateria_sha, a.modo,
                                            a.forcar_regeracao, stamp, recibo.get("recibo_pre_selo"), a.reparo_de_pino)
''', '''            novo, md, rotulo, n = regenerar(bancada, anterior, nos_info, a.versao, (evento or {}).get("evento"), script_sha, bateria_sha, a.modo,
                                            a.forcar_regeracao, stamp, recibo.get("recibo_pre_selo"), a.reparo_de_pino, salto)
''')
sub('''            veredito_base = "REPINADA_B%d" % n
''', '''            veredito_base = "REPINADA_B%d" % n
            if salto is not None:       # R3.4 (S): o veredito diz o salto (de onde a Bancada sai e a versao a que chega)
                veredito_base += "__SALTO_%s_%s" % (salto["de"]["versao"], a.versao)
''')

# (e) os marcadores do um.py medido, para os testes que o pinam
sub('''                       kernel_recibo=a.kernel_recibo or "", kernel_recibo_sha256=(str(a.kernel_recibo_sha256).lower() if a.kernel_recibo_sha256 else ""))
''', '''                       kernel_recibo=a.kernel_recibo or "", kernel_recibo_sha256=(str(a.kernel_recibo_sha256).lower() if a.kernel_recibo_sha256 else ""),
                       um_py_path=nos_info["um_py"]["path"], um_py_sha256=nos_info["um_py"]["sha256"], um_py_bytes=nos_info["um_py"]["bytes"], selo_sha256=nos_info["selo"]["sha256"])
''')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
