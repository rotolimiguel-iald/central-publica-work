# -*- coding: utf-8 -*-
"""patch_controles_r35.py (R3.5, 19/10/2026) -- converte controles_negativos_r3_4.py (copia de bytes em R3_5/controles_negativos_r3_5.py) para a R3.5: os 547 da R3.4 com os nomes mantidos (a familia b1 e
os controles que liam o Nos REAL migram para o stand-in da custodia v393, porque o Nos real esta no meio do rito da v394) e os NOVOS (R35_M_, R35_V_, R35_P_).
uso: python -I -B -X utf8 patch_controles_r35.py"""
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
P = AQUI / "controles_negativos_r3_5.py"
R34 = AQUI.parent / "R3_4" / "controles_negativos_r3_4.py"
raw = P.read_bytes()
assert raw == R34.read_bytes(), "o script de partida nao e, byte a byte, o da R3.4"
ORIG = AQUI / "_construcao" / "controles_negativos_R3_4_original.py"
if not ORIG.exists():
    with open(ORIG, "xb") as f:
        f.write(raw)
t = raw.decode("utf-8")


def sub(velho, novo, n=1):
    global t
    assert t.count(velho) == n, (velho[:100], t.count(velho), n)
    t = t.replace(velho, novo)


bloco_novos = (AQUI / "_construcao" / "bloco_controles_r35.txt").read_text(encoding="utf-8")

# --- cabecalho, nomes de arquivos, constantes
sub('"""controles_negativos_r3_4.py (R3.4, 19/10/2026) -- ',
    '"""controles_negativos_r3_5.py (R3.5, 19/10/2026) -- os 547 da R3.4 (nomes mantidos; a familia b1 e os controles que liam o Nos REAL migrados para o stand-in da custodia v393 -- o Nos real esta no meio do rito '
    'da v394 --, e os 3 controles da varredura de auditoria que a lista de PERMISSAO estrita muda de forma) e os NOVOS (prefixos R35_M_ evasoes do modulo de auditoria, R35_V_ validade do recibo pre_selo real '
    'da R3.4, R35_P_ a bateria da v394 contra o candidato real). Da R3.4: controles_negativos_r3_4.py (R3.4, 19/10/2026) -- ')
sub('B1, B2, NOS, NOS392, FX, S = RAIZ / "b1", RAIZ / "b2", RAIZ / "nos", RAIZ / "nos_v392", RAIZ / "fx", RAIZ / "s"\n',
    'B1, B2, NOS, NOS392, FX, S = RAIZ / "b1", RAIZ / "b2", RAIZ / "nos", RAIZ / "nos_v392", RAIZ / "fx", RAIZ / "s"\n'
    'NOS_STAND, B1R, B1S394, NOS394S = RAIZ / "nos_real", RAIZ / "b1real", RAIZ / "b1v394s", RAIZ / "nos_v394s"   # R3.5: o stand-in do Nos v393 (custodia), b1real (pina o caminho real), o stand-in do v394\n'
    'R34 = AQUI.parent / "R3_4"\n')
sub('(RAIZ / "SANDBOX_MANIFEST_R3_4.json").read_text(encoding="utf-8")', '(RAIZ / "SANDBOX_MANIFEST_R3_5.json").read_text(encoding="utf-8")')
sub('sandbox_manifest_sha256=sha(RAIZ / "SANDBOX_MANIFEST_R3_4.json")', 'sandbox_manifest_sha256=sha(RAIZ / "SANDBOX_MANIFEST_R3_5.json")')
sub('INJETADOS_SELO = []', 'INJETADOS_SELO = []\nINJETADOS_NOS = []        # R3.5: controles cujo comando ganhou --nos <stand-in v393 da custodia> (antes liam o Nos real por omissao)')

# --- a injecao do --nos (stand-in) em todo run() sem --nos
sub('def com_criterios(nome, args, sem_criterios=False):',
    'def com_nos_stand(nome, args):\n'
    '    """R3.5: o Nos REAL esta no meio do rito da v394 (um.py v394 instalado, selo v393): nao se le. Todo comando do sandbox sem --nos (que lia o Nos real por omissao) le o stand-in v393 (nos_real/, copia de bytes da custodia)."""\n'
    '    a = [str(x) for x in args]\n'
    '    if "--nos" not in a:\n'
    '        INJETADOS_NOS.append(nome)\n'
    '        a = a + ["--nos", str(NOS_STAND)]\n'
    '    return a\n\n\n'
    'def com_criterios(nome, args, sem_criterios=False):')
sub('    args = com_criterios(nome, args, sem_criterios)\n    saida = saida or (S / nome)', '    args = com_nos_stand(nome, com_criterios(nome, args, sem_criterios))\n    saida = saida or (S / nome)')
sub('NOS_LISTA_ANTES = sorted(os.listdir(NOS_REAL))', 'NOS_LISTA_ANTES = sorted(os.listdir(NOS_REAL))\nNOS_UM_SHA_ANTES = sha(NOS_REAL / "um.py")        # R3.5: so para registrar que este script nao mexeu (o rito escreve no Nos, nao este script)')

# --- o stand-in no lugar do Nos real (conteudo)
sub('gerar_bateria_r34("real_" + VR, VR, NOS_REAL, real=True)', 'gerar_bateria_r34("real_" + VR, VR, NOS_STAND, real=True)')
sub('rec["manifesto_anterior"]["pina_o_nos_real"] is True and\n', 'rec["manifesto_anterior"]["pina_o_nos_real"] is False and\n')
sub('_ni_real = MOD.ler_nos(NOS_REAL, VR)', '_ni_real = MOD.ler_nos(NOS_STAND, VR)')
sub('Path(NOS_REAL / f_)', 'Path(NOS_STAND / f_)', n=2)
sub('"--versao", VR, "--nos", str(NOS_REAL), "--driver"', '"--versao", VR, "--nos", str(NOS_STAND), "--driver"')
sub('def driver(nome, src, pino, nos_dir=NOS_REAL, sha_=None, bytes_=None):', 'def driver(nome, src, pino, nos_dir=NOS_STAND, sha_=None, bytes_=None):')
sub('["$.source_pins[9].bytes", "$.source_pins[9].sha256"]', '["$.source_pins[9].bytes", "$.source_pins[9].path", "$.source_pins[9].sha256"]', n=2)

# --- as tres guardas A2 passam a b1real (o manifesto pina o caminho REAL do Nos; --nos = stand-in)
sub('jb1 = juncao(RAIZ / "jb1", B1)', 'jb1 = juncao(RAIZ / "jb1", B1R)')
sub('"\\\\\\\\?\\\\" + str(B1), "--versao", VR,', '"\\\\\\\\?\\\\" + str(B1R), "--versao", VR,')
sub('"--evento", "SANDBOX:B1 prefixo"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1,', '"--evento", "SANDBOX:B1 prefixo"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R,')
sub('"--evento", "SANDBOX:B1 juncao"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)', '"--evento", "SANDBOX:B1 juncao"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R)')
sub('run("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)',
    'run("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", ["--bancada", B1R, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R)')

# --- a varredura de auditoria: tres controles da R3.4 mudam de forma sob a lista de permissao (import fora da lista; nomes de local fora da lista)
sub(r'''_okp("import A.B\nopen Lean in\nrun_cmd do\n  IO.println \"x\"\n#print axioms A.B.c\n-- comentario\n\n")["ok"]''',
    r'''_okp("import TGLExt.B\nopen Lean in\nrun_cmd do\n  IO.println \"x\"\n#print axioms A.B.c\n-- comentario\n\n")["ok"]''')
sub(r'''lambda: _okp("run_cmd do\n  let defaults := 1\n  let instances := 2\n  let theorem_count := 3\n")["ok"],''',
    r'''lambda: (lambda r_: (not r_["ok"]) and "'defaults'" in r_["motivo"])(_okp("run_cmd do\n  let defaults := 1\n  let instances := 2\n  let theorem_count := 3\n")),''')
sub("nota=\"M (unitario): `defaults`, `instances`, `theorem_count` no corpo nao sao as palavras proibidas (a lista olha a palavra inteira)\")",
    "nota=\"M (unitario, R3.5): na R3.4 a lista de PROIBICAO olhava a palavra inteira e aceitava `defaults`, `instances`, `theorem_count`; na lista de PERMISSAO estrita um local fora da lista e recusado (e o motivo nomeia o local)\")")
sub(r'''lambda: _okp("import A\r\nrun_cmd do\r\n\tIO.println \"x\"\r\n")["ok"] and not _okp("import A\r\nrun_cmd do\r\n\ttheorem x : True := trivial\r\n")["ok"],''',
    r'''lambda: _okp("import Lean\r\nrun_cmd do\r\n\tIO.println \"x\"\r\n")["ok"] and not _okp("import Lean\r\nrun_cmd do\r\n\ttheorem x : True := trivial\r\n")["ok"],''')

# --- os controles novos
sub('# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado', bloco_novos + '# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado')

# --- o fecho: o Nos real esta em obra (rito); a R3.4 exigia a lista igual
sub('assert sorted(os.listdir(NOS_REAL)) == NOS_LISTA_ANTES, "a lista do Nos mudou"\n',
    'NOS_LISTA_DEPOIS = sorted(os.listdir(NOS_REAL))\n'
    'NOS_REAL_REGISTRO = dict(itens_antes=len(NOS_LISTA_ANTES), itens_depois=len(NOS_LISTA_DEPOIS), acrescentados=sorted(set(NOS_LISTA_DEPOIS) - set(NOS_LISTA_ANTES)), removidos=sorted(set(NOS_LISTA_ANTES) - set(NOS_LISTA_DEPOIS)),\n'
    '                         um_py_sha256_antes=NOS_UM_SHA_ANTES, um_py_sha256_depois=sha(NOS_REAL / "um.py"),\n'
    '                         nota="R3.5: o Nos real esta no meio do rito da v394 (outro processo escreve nele); este script so o LE (a lista e o sha do um.py) e nunca grava nele: a guarda SAIDA_NO_NOS e os controles A5 o provam; '
    'o stand-in v393 vem da custodia")\n')
sub('nos_real_intocado=True, eventos_jsonl_real_sha256=EV_REAL_SHA_ANTES,', 'nos_real_so_lido=NOS_REAL_REGISTRO, eventos_jsonl_real_sha256=EV_REAL_SHA_ANTES,')

# --- a contabilidade da R3.4 (547) para a R3.5
sub('faltam_r33 = sorted(set(R33_NOMES) - set(nomes))\n',
    'faltam_r33 = sorted(set(R33_NOMES) - set(nomes))\n'
    'R34_RES = json.loads((R34 / "CONTROLES_NEGATIVOS_R3_4.json").read_bytes())\n'
    'R34_NOMES = [c["controle"] for c in R34_RES["controles"]]\n'
    'faltam_r34 = sorted(set(R34_NOMES) - set(nomes))\n'
    'NOVOS_R35 = [x for x in nomes if x not in set(R34_NOMES)]\n')
sub('out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.4 (19/10/2026)",', '''MUDARAM_R35 = {}
for x_ in sorted(set(INJETADOS_NOS)):
    if x_ in R34_NOMES:
        MUDARAM_R35.setdefault(x_, []).append("R3.5: o comando ganhou --nos <stand-in v393 da custodia (nos_real/)>: o Nos REAL esta no meio do rito da v394 (um.py v394 instalado, selo v393) e nao se le; antes o "
                                              "controle lia o Nos real por omissao; a recusa ou o veredito esperado nao mudou")
for x_, motivo_ in (("A2_B1_replay_prefixo_sandbox_aplicar_b1", "R3.5: a Bancada e b1real (o manifesto pina o caminho REAL do Nos; --nos = stand-in): a guarda A2 recusa antes de qualquer conteudo do Nos importar"),
                    ("A2_B1_replay_juncao_sandbox_aplicar_b1", "R3.5: idem (a juncao aponta b1real)"),
                    ("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", "R3.5: idem"),
                    ("RUN_1a_pre_selo_b1_nos_real", "R3.5: contra o stand-in v393 da custodia (nos_real/), nao o Nos real; manifesto_anterior.pina_o_nos_real e false"),
                    ("R34_P_run_1a_T12_repinado_so_o_pino_do_um_py_e_o_resto_identico_ao_arquivado", "R3.5: o pino do um.py do pre-registro agora difere tambem em .path (o stand-in nao esta no caminho real do Nos)"),
                    ("R34_P_driver_sozinho_contraprova_passa_com_o_pino_certo", "R3.5: idem"),
                    ("R34_P_bateria_gerada_para_o_nos_real_pina_a_versao_instalada", "R3.5: o Nos 'real' v393 e o stand-in da custodia (os pinos do stand-in sao os do Nos v393 antes da instalacao da v394)"),
                    ("R34_P_gerador_e_determinista_mesma_entrada_mesma_bateria", "R3.5: idem"),
                    ("R34_S_cadeia_real_confere_com_a_producao_e_o_nos_reais", "R3.5: o fim da cadeia e o stand-in v393 (custodia) no lugar do Nos real, que ja e o v394 em instalacao; a producao e a real (so lida)"),
                    ("R34_S_o_selo_nao_pina_o_selo_anterior_medido", "R3.5: medido no selo v393 da custodia (nos_real/), que e o selo real da v393"),
                    ("R34_M_varredura_aceita_import_open_print_axioms_e_run_cmd", "R3.5: o import da amostra passa a ser TGLExt.B (a lista de permissao so admite Lean/TGLExt/TGL)"),
                    ("R34_M_varredura_palavras_dentro_de_nome_nao_sao_a_palavra", "R3.5: INVERTIDO: na lista de PERMISSAO um local fora da lista e recusado (antes, a lista de proibicao aceitava `defaults`, `instances`, `theorem_count`)"),
                    ("R34_M_varredura_CRLF_e_tab", "R3.5: o import da amostra passa a ser `import Lean`")):
    if x_ in R34_NOMES:
        MUDARAM_R35.setdefault(x_, []).append(motivo_)
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.5 (19/10/2026)",''')
sub('n_da_R3_3=len(R33_NOMES),', 'n_da_R3_4=len(R34_NOMES), da_R3_4_presentes=len(R34_NOMES) - len(faltam_r34), da_R3_4_ausentes=faltam_r34, n_novos_R3_5=len(NOVOS_R35), novos_R3_5=NOVOS_R35,\n'
    '           controles_da_R3_4_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R35.items())], n_controles_da_R3_4_que_mudaram_de_formato=len(MUDARAM_R35),\n'
    '           n_da_R3_3=len(R33_NOMES),')
sub('and not faltam_r33 and not juncoes_restantes', 'and not faltam_r33 and not faltam_r34 and not juncoes_restantes')
sub('(AQUI / "CONTROLES_NEGATIVOS_R3_4.json").write_bytes(texto.encode("utf-8"))', '(AQUI / "CONTROLES_NEGATIVOS_R3_5.json").write_bytes(texto.encode("utf-8"))')
sub('"R3.3 presentes %d/%d" % (out["da_R3_3_presentes"], len(R33_NOMES)), "novos R3.4 %d" % len(NOVOS_R34),',
    '"R3.3 presentes %d/%d" % (out["da_R3_3_presentes"], len(R33_NOMES)), "R3.4 presentes %d/%d" % (out["da_R3_4_presentes"], len(R34_NOMES)), "novos R3.5 %d" % len(NOVOS_R35),')
tmp = P.with_name(P.name + ".tmp_r35")
with open(tmp, "xb") as f:
    f.write(t.encode("utf-8"))
os.replace(tmp, P)
print("ok", len(raw), "->", P.stat().st_size)
