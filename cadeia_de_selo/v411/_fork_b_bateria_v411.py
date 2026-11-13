# -*- coding: utf-8 -*-
"""_fork_b_bateria_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) adapta de verdade os sete scripts de bateria_pre_selo\\ a v411. O B(n) pre-selo da v411 e' o passo simples B20 (a producao pina a v410,
o Nos e' a v410 hoje): esboco e bateria pinados na v410 (lidos dos pinos); o controle «selo anterior errado» usa o selo da versao ANTES da anterior, a v409, guardada em v410\\base_v409 (a subida mecanica deixara
v410\\base_v408, que nao existe); no modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1) TODAS as saidas da bateria (ensaio_1, etapa1_stdout, conferencia, prova_producao, limpeza, os outs) vao para
<pasta de ensaio>\\bateria_pre_selo e o PINO/PROVA para a pasta de ensaio (fora de work); no real, ficam onde ficavam. Nada e' executado. uso: python -B -X utf8 _fork_b_bateria_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

FUNC = ('\n\ndef _saida_pre_selo():\n'
        '    """(v411) onde a bateria grava: no ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v411) a pasta de ensaio, fora de work; no real, esta pasta e v411\\\\ (como na v410)."""\n'
        '    import importlib.util as _u\n'
        '    _s = _u.spec_from_file_location("delta_v411_pre_selo", os.path.join(V, "delta_v411.py")); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)\n'
        '    return (os.path.join(_m.SAIDA, "bateria_pre_selo") if _m.ENSAIO_TOPO_PROPOSTO else HERE), _m.SAIDA, _m\n\n\n'
        'OUTB, OUTV, _DLM = _saida_pre_selo()\nos.makedirs(OUTB, exist_ok=True)\n')

# ---- conferir_recibo_pre_selo
R = "bateria_pre_selo/conferir_recibo_pre_selo_v411.py"
_h10 = L.linha(R, "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410]")
_nh = L.linha(R, "# (nota herdada da adaptacao da v408")
_nh2 = L.linha(R, "# (a subida mecanica deixara `base_v407`")
L.aplicar(R, [
    (_h10 + "\n", ""),
    (_nh, "# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida de versao a versao) molde v410/bateria_pre_selo/conferir_recibo_pre_selo_v410.py (rotulos subidos por _bump_copia_v411.py; diff em bump/). "
          "Adaptado (v411, 12/11/2026, fork B): o controle negativo «selo anterior errado» usa o selo da versao ANTES da anterior: na v411 e' a v409, guardada em v410\\base_v409"),
    (_nh2, "# (a subida mecanica deixara `v410\\base_v408`, que nao existe); o controle chama-se selo_anterior_e_o_da_v409_nao_o_pinado. O resto nao depende de bundle nem de contagem de modulos (tudo e' LIDO do recibo, dos pinos e da producao)."),
    ('V14 = os.path.join(os.path.dirname(V), "v410")\n', 'V14 = os.path.join(os.path.dirname(V), "v410")\n' + FUNC.strip("\n") + "\n"),
    ('ENS = os.path.join(HERE, "ensaio_1")', 'ENS = os.path.join(OUTB, "ensaio_1")'),
    ('out_txt = open(os.path.join(HERE, "etapa1_stdout.txt"), encoding="utf-8")', 'out_txt = open(os.path.join(OUTB, "etapa1_stdout.txt"), encoding="utf-8")'),
    ('SELO_V408 = os.path.join(V14, "base_v408", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v408, guardada em v410\\base_v408): o controle negativo "selo anterior errado"\n'
     'KM_V408 = os.path.join(V14, "base_v408", "tgl_kernel_proof_manifest.json")\n'
     'assert os.path.isfile(SELO_V408) and os.path.isfile(KM_V408), "a base v408 (o selo da versao antes da anterior) nao esta em v410\\\\base_v408"\n',
     'SELO_V409 = os.path.join(V14, "base_v409", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v409, guardada em v410\\base_v409): o controle negativo "selo anterior errado"\n'
     'KM_V409 = os.path.join(V14, "base_v409", "tgl_kernel_proof_manifest.json")\n'
     'assert os.path.isfile(SELO_V409) and os.path.isfile(KM_V409), "a base v409 (o selo da versao antes da anterior) nao esta em v410\\\\base_v409"\n'),
    ('ok, rec_t, _ = conferir(RP, RSHA, SELO_V408, KM_V408)\ncontrole("selo_anterior_e_o_da_v408_nao_o_pinado"', 'ok, rec_t, _ = conferir(RP, RSHA, SELO_V409, KM_V409)\ncontrole("selo_anterior_e_o_da_v409_nao_o_pinado"'),
    ('dest = os.path.join(HERE, "conferencia_pelo_esboco_v411.json")', 'dest = os.path.join(OUTB, "conferencia_pelo_esboco_v411.json")'),
], "o controle «selo anterior errado» com a v409 (v410\\base_v409; a subida deixara v410\\base_v408, que nao existe); o anterior = v411\\base_v410; esboco e bateria lidos dos pinos da v410; as entradas e a saida em OUTB (no ensaio do topo proposto, a pasta de ensaio)")

# ---- gerar_pino_recibo_pre_selo
G = "bateria_pre_selo/gerar_pino_recibo_pre_selo_v411.py"
L.aplicar(G, [
    ('DEST_PROVA = os.path.join(HERE, "prova_producao")', FUNC.strip("\n").replace("\n\n\nOUTB", "\n\n\nOUTB") + '\nDEST_PROVA = os.path.join(OUTB, "prova_producao")'),
    ('rps = glob.glob(os.path.join(HERE, "ensaio_1", "RECIBO_SINCRONIZACAO_v410_*.json"))', 'rps = glob.glob(os.path.join(OUTB, "ensaio_1", "RECIBO_SINCRONIZACAO_v410_*.json"))'),
    ('STDOUT = os.path.join(HERE, "etapa1_stdout.txt")', 'STDOUT = os.path.join(OUTB, "etapa1_stdout.txt")'),
    ('conf_p = os.path.join(HERE, "conferencia_pelo_esboco_v411.json")', 'conf_p = os.path.join(OUTB, "conferencia_pelo_esboco_v411.json")'),
    ('t12 = lj(os.path.join(HERE, "ensaio_1", "recibos", "T12_T13_T14_ATRATOR.json"))', 't12 = lj(os.path.join(OUTB, "ensaio_1", "recibos", "T12_T13_T14_ATRATOR.json"))'),
    ('d_prova = gravar_novo(os.path.join(V, "PROVA_PRODUCAO_INTACTA_v411_pre_selo.json"), prova)\nd_pino = gravar_novo(os.path.join(V, "PINO_RECIBO_PRE_SELO_v411.json"), pino)',
     'if _DLM.ENSAIO_TOPO_PROPOSTO:   # (v411) o ensaio do topo proposto: marcado, na pasta de ensaio (nunca na pasta da cadeia)\n    prova.update(_DLM.MARCA_ENSAIO); pino.update(_DLM.MARCA_ENSAIO)\n'
     'd_prova = gravar_novo(os.path.join(OUTV, "PROVA_PRODUCAO_INTACTA_v411_pre_selo.json"), prova)\nd_pino = gravar_novo(os.path.join(OUTV, "PINO_RECIBO_PRE_SELO_v411.json"), pino)'),
], "le tudo do recibo do ensaio, do stdout, dos pinos da v410 e das fotografias (nada de bundle); as entradas em OUTB e os dois JSON em OUTV (no real: bateria_pre_selo\\ e v411\\, como na v410; no ensaio do topo proposto: a pasta de ensaio, com a marca do ensaio)")

# ---- limpar_sandbox_vb22
S = "bateria_pre_selo/limpar_sandbox_vb22.py"
L.aplicar(S, [
    ('HERE = os.path.dirname(os.path.abspath(__file__))\n', 'HERE = os.path.dirname(os.path.abspath(__file__))\nV = os.path.dirname(HERE)\n' + FUNC.strip("\n") + '\n'),
    ('dest = os.path.join(HERE, "LIMPEZA_SANDBOX_vb22.json")', 'dest = os.path.join(OUTB, "LIMPEZA_SANDBOX_vb22.json")'),
    ('"nota": "as fotografias e as listas que valem como prova estao copiadas em v411\\\\bateria_pre_selo\\\\prova_producao\\\\ (gerar_pino_recibo_pre_selo_v411.py); o resto do sandbox era descartavel"}',
     '"nota": "as fotografias e as listas que valem como prova estao copiadas em %s (gerar_pino_recibo_pre_selo_v411.py); o resto do sandbox era descartavel" % os.path.join(OUTB, "prova_producao"), **_DLM.MARCA_ENSAIO}'),
], "apaga so' C:\\t\\vb22 depois de provar que nao ha juncao nem link (nao depende de versao); o recibo da limpeza em OUTB (no ensaio do topo proposto, a pasta de ensaio)")

# ---- snap_producao: o corpo nao depende de versao (o destino vem do argumento)
L.aplicar("bateria_pre_selo/snap_producao_v411.py", [], "conferido: so' le a Bancada de producao e o Nos e fotografa; o destino vem do argumento (o sandbox curto C:\\t\\vb22\\snap); nao depende de versao nem do modo de ensaio")

# ---- derivar_pre_selo: segue recusando; o texto da base do controle corrigido
D = "bateria_pre_selo/derivar_pre_selo_v411.py"
L.aplicar(D, [
    ('(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v411, a v408, guardada em v410\\\\base_v408).',
     '(o controle negativo "selo anterior errado" usa o selo da versao ANTES da anterior: para a v411, a v409, guardada em v410\\\\base_v409).'),
    ('um mapa herdado deixaria `base_v406` onde a v411 precisa de `base_v408`', 'um mapa herdado deixaria a base errada onde a v411 precisa de `v410\\\\base_v409`'),
], "o derivador segue RECUSANDO de proposito (os cinco scripts da v411 nasceram da subida e foram adaptados a mao pelo fork B do construtor da v411); so' o texto da base do controle mudou (v410\\base_v409)")

# ---- rodar_ensaio_1_pre_selo: a saida do ensaio (--saida) e o stdout em OUTB
SH_OUTB = ('# (v411) onde a bateria grava: no ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v411) a pasta de ensaio, fora de work; no real, esta pasta (como na v410)\n'
           'OUTB_W=$($PY -c "import importlib.util as u,os,sys; s=u.spec_from_file_location(\'d\',sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m); print(os.path.join(m.SAIDA,\'bateria_pre_selo\') if m.ENSAIO_TOPO_PROPOSTO else sys.argv[2])" "$(cygpath -w "$V/delta_v411.py")" "$(cygpath -w "$V/bateria_pre_selo")" | tr -d \'\\r\')\n'
           '[ -n "$OUTB_W" ] || { echo "a pasta de saida da bateria nao foi lida do delta_v411"; exit 9; }\n'
           'OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"\n')
E1 = "bateria_pre_selo/rodar_ensaio_1_pre_selo_v411.sh"
L.aplicar(E1, [
    ("SAIDA='C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v411\\bateria_pre_selo\\ensaio_1'\nOUT=\"$V/bateria_pre_selo/etapa1_stdout.txt\"\ncd \"$V\" || exit 9\n",
     "cd \"$V\" || exit 9\n" + SH_OUTB + "SAIDA=\"$OUTB_W\\\\ensaio_1\"\nOUT=\"$OUTB/etapa1_stdout.txt\"\n"),
], "o ensaio pre_selo contra o Nos v410 (canonico hoje), esboco e bateria pinados na v410 (lidos dos pinos); --versao v410; a saida (--saida) e o stdout em OUTB, lido do delta (no ensaio do topo proposto, a pasta de ensaio)")

# ---- rodar_bn_pre_selo: as saidas em OUTB; os passos 8 e 9 (diff_e_pinos e p00) leem o modo pelo ambiente
BN = "bateria_pre_selo/rodar_bn_pre_selo_v411.sh"
L.aplicar(BN, [
    ("cd \"$B\"\nfor f in rodar_ensaio_1_pre_selo_v411.sh", "cd \"$B\"\n" + SH_OUTB.replace("\"$V/bateria_pre_selo\"", "\"$B\"") + "echo \"saidas da bateria em $OUTB_W\"\nfor f in rodar_ensaio_1_pre_selo_v411.sh"),
    ("tail -3 etapa1_stdout.txt\ngrep -q \"ETAPA1_RC=0\" etapa1_stdout.txt ||", "tail -3 \"$OUTB/etapa1_stdout.txt\"\ngrep -q \"ETAPA1_RC=0\" \"$OUTB/etapa1_stdout.txt\" ||"),
    ("$PY conferir_recibo_pre_selo_v411.py > conferencia_out_v411.txt 2>&1 || RC_CONFERENCIA=$?; tail -4 conferencia_out_v411.txt;",
     "$PY conferir_recibo_pre_selo_v411.py > \"$OUTB/conferencia_out_v411.txt\" 2>&1 || RC_CONFERENCIA=$?; tail -4 \"$OUTB/conferencia_out_v411.txt\";"),
    ("$PY gerar_pino_recibo_pre_selo_v411.py \"$SNAP\" > pino_out_v411.txt 2>&1 || RC_PINO=$?; tail -4 pino_out_v411.txt;",
     "$PY gerar_pino_recibo_pre_selo_v411.py \"$SNAP\" > \"$OUTB/pino_out_v411.txt\" 2>&1 || RC_PINO=$?; tail -4 \"$OUTB/pino_out_v411.txt\";"),
    ("$PY diff_e_pinos_v411.py > \"$B/diff_e_pinos_out_v411.txt\" 2>&1 || RC_DIFF_PINOS=$?; tail -2 \"$B/diff_e_pinos_out_v411.txt\";",
     "$PY diff_e_pinos_v411.py > \"$OUTB/diff_e_pinos_out_v411.txt\" 2>&1 || RC_DIFF_PINOS=$?; tail -2 \"$OUTB/diff_e_pinos_out_v411.txt\";"),
    ("$PY p00_precondicoes_v411.py > \"$B/p00_out_v411.txt\" 2>&1 || RC_P00=$?; tail -16 \"$B/p00_out_v411.txt\";",
     "$PY p00_precondicoes_v411.py > \"$OUTB/p00_out_v411.txt\" 2>&1 || RC_P00=$?; tail -16 \"$OUTB/p00_out_v411.txt\";"),
], "a ordem dos passos da v410; o B(n) pre-selo da v411 e' o passo simples B20 (a producao pina a v410); os passos 8 e 9 chamam diff_e_pinos_v411 e p00_precondicoes_v411 (que leem o modo pelo ambiente); as saidas em OUTB, lido do delta (no ensaio do topo proposto, a pasta de ensaio)")
