# -*- coding: utf-8 -*-
"""patch_controles_r3_2.py -- deriva controles_negativos_r3_2.py da copia de controles_negativos_r3_1.py: (1) todo subprocesso do esboco com
-I -B -X utf8 (R31-1); (2) --selo-anterior/--kernel-manifesto-anterior injetados com --recibo-pre-selo (R31-3), registrados; (3) os
controles cujo formato muda pela R3.2 (A9, N5, R31_A4), com motivo; (4) o bloco R32_ (bloco_r3_2.py.txt) antes do run 2; (5) o fecho
compara com os 337 da R3.1. Cada ancora e conferida (count == 1)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
P = AQUI.parent / "controles_negativos_r3_2.py"
t = P.read_text(encoding="utf-8")
BLOCO = (AQUI / "bloco_r3_2.py.txt").read_text(encoding="utf-8")


def troca(x, y, n=1):
    global t
    assert t.count(x) == n, (t.count(x), x[:120])
    t = t.replace(x, y)


# (0) cabecalho
troca('"""controles_negativos_r3_1.py (R3.1, 13/10/2026) -- ',
      '"""controles_negativos_r3_2.py (R3.2, 13/10/2026) -- os 337 controles da R3.1 (nomes mantidos; os que mudaram de formato listados com motivo em\n'
      'CONTROLES_NEGATIVOS_R3_2.json) e os NOVOS da R3.2 (prefixo R32_), o caso EXATO do auditor e uma variante para cada achado da reauditoria\n'
      'a721b706 (R31-1 a R31-6) e para o item 3 da 12-ter do plano. Todo subprocesso do esboco roda com -I -B -X utf8 (R31-1), e ESTE script tambem\n'
      'tem de rodar assim (as chamadas em processo de main() conferem o interpretador corrente). Com --recibo-pre-selo, todo comando recebe\n'
      '--selo-anterior/--kernel-manifesto-anterior (a custodia v391 do sandbox, fx/custodia_v391), porque o B(n) R3.2 exige o pino externo (R31-3).\n'
      'uso: python -I -B -X utf8 controles_negativos_r3_2.py <raiz curta C:/t/vb*>\n'
      'Da R3.1: controles_negativos_r3_1.py (R3.1, 13/10/2026) -- ')
troca('import contextlib, copy, datetime, hashlib, importlib.util, io, json, os, shutil, subprocess, time, zipfile\nfrom pathlib import Path\n',
      'import contextlib, copy, datetime, hashlib, importlib.util, io, json, os, shutil, subprocess, time, zipfile\nfrom pathlib import Path\n'
      'assert sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.utf8_mode, "R3.2 (R31-1): rode com python -I -B -X utf8"\n')
troca('SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_1.json").read_text(encoding="utf-8"))',
      'SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_2.json").read_text(encoding="utf-8"))\n'
      'R31 = AQUI.parent / "R3_1"\n'
      '# R31-3 (R3.2): a custodia v391 do sandbox (o selo e o manifesto do kernel da versao anterior), gravada pelo montar_sandbox antes do "selo"\n'
      'SELO_ANT = FX / "custodia_v391" / "um_absoluto_selo.json"\n'
      'KMAN_ANT = FX / "custodia_v391" / "tgl_kernel_proof_manifest.json"\n'
      'assert sha(SELO_ANT) == SBM["nos"]["selo"]["sha256"] and sha(KMAN_ANT) == SBM["nos"]["kernel_manifest"]["sha256"], "custodia v391 do sandbox"\n'
      'SEM_SELO_ANT = set()      # controles que testam a AUSENCIA do selo anterior (sem injecao)\n'
      'INJETADOS_SELO = []       # controles cujo comando ganhou --selo-anterior/--kernel-manifesto-anterior (mudanca de formato registrada)')
# sha() e usado na linha acima: a definicao vem antes? (sha_b/sha sao definidas depois de SBM na R3.1) -- mover a definicao para antes
i_sha = t.index("def sha_b(b):")
j_sha = t.index("def sha_teste(t):")
defs = t[i_sha:j_sha]
t = t[:i_sha] + t[j_sha:]
k = t.index("SBM = json.loads(")
t = t[:k] + defs + t[k:]
# (1) -I em todo subprocesso do esboco
troca('def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-B", "-X", "utf8"), sync=None,',
      'def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-I", "-B", "-X", "utf8"), sync=None,')
# (2) a injecao do selo anterior junto com a dos criterios
troca('''def com_criterios(nome, args, sem_criterios=False):
    a = [str(x) for x in args]
    if not sem_criterios and "--kernel-recibo" in a and "--criterios" not in a and "--criterios-sha256" not in a:
        v_ = a[a.index("--versao") + 1] if "--versao" in a and a.index("--versao") + 1 < len(a) else "v392"
        v_ = v_ if (v_.startswith("v") and v_[1:].isdigit()) else "v392"
        p_, s_ = crit_para(v_)
        INJETADOS.append(nome)
        return a + ["--criterios", str(p_), "--criterios-sha256", s_]
    return a''',
      '''def com_criterios(nome, args, sem_criterios=False):
    a = [str(x) for x in args]
    if not sem_criterios and "--kernel-recibo" in a and "--criterios" not in a and "--criterios-sha256" not in a:
        v_ = a[a.index("--versao") + 1] if "--versao" in a and a.index("--versao") + 1 < len(a) else "v392"
        v_ = v_ if (v_.startswith("v") and v_[1:].isdigit()) else "v392"
        p_, s_ = crit_para(v_)
        INJETADOS.append(nome)
        a = a + ["--criterios", str(p_), "--criterios-sha256", s_]
    # R31-3 (R3.2): com --recibo-pre-selo, o pino externo do kernel anterior (a custodia v391 do sandbox), salvo nos controles da ausencia
    if "--recibo-pre-selo" in a and "--selo-anterior" not in a and "--kernel-manifesto-anterior" not in a and nome not in SEM_SELO_ANT:
        INJETADOS_SELO.append(nome)
        a = a + ["--selo-anterior", str(SELO_ANT), "--kernel-manifesto-anterior", str(KMAN_ANT)]
    return a''')
# (2b) as chamadas unitarias de conferir_recibo_pre_selo (antes do bloco R32, que chama MOD direto quando quer a ausencia)
n_unit = t.count("MOD.conferir_recibo_pre_selo(")
t = t.replace("MOD.conferir_recibo_pre_selo(", "_conferir_pre(")
troca('''spec.loader.exec_module(MOD)
''', '''spec.loader.exec_module(MOD)


def _conferir_pre(*a_):
    """R31-3 (R3.2): conferir_recibo_pre_selo com o pino externo (a custodia v391 do sandbox)."""
    return MOD.conferir_recibo_pre_selo(*a_, selo_anterior=SELO_ANT, kernel_manifesto_anterior=KMAN_ANT)
''')
# (3) os controles cujo formato muda
troca('''run("A9_sem_B_nenhum_pycache", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, flags=("-X", "utf8"),
    extra_ok=lambda j, r: not tem_pycache(B1) and recibo_de(j)["python_dont_write_bytecode"] is True,''',
      '''run("A9_sem_B_nenhum_pycache", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B1, flags=("-I", "-X", "utf8"),
    extra_ok=lambda j, r: not tem_pycache(B1) and j.get("recibo") is None and "-B" in str(j.get("recusa")),''')
troca('''    nota="o ataque B3 da auditoria R1: na R1 nascia bancada/__pycache__/canonical.*.pyc; desde a R2 sys.dont_write_bytecode=True no topo")''',
      '''    nota="o ataque B3 da auditoria R1: na R1 nascia bancada/__pycache__/canonical.*.pyc; desde a R2 sys.dont_write_bytecode=True no topo. R3.2 (R31-1): sem -B o "
         "esboco recusa antes de qualquer import (INTERPRETADOR_NAO_ISOLADO) e nenhum __pycache__ nasce")
run("R32_A9_com_I_e_B_nenhum_pycache", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1,
    extra_ok=lambda j, r: not tem_pycache(B1) and recibo_de(j)["python_dont_write_bytecode"] is True and recibo_de(j)["python_isolado"]["dont_write_bytecode_flag"] is True,
    nota="R3.2: com -I -B -X utf8 (a chamada exigida) o canonical.py instalado e importado e nenhum __pycache__ nasce")''')
troca('''"--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-E", "-B", "-X", "utf8"),
    env_extra=dict(PYTHONPATH=str(FX / "n5pp")),''',
      '''"--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-I", "-B", "-X", "utf8"),
    env_extra=dict(PYTHONPATH=str(FX / "n5pp")),''')
troca('''run("N5_PYTHONPATH_sem_E_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_amb, "--bateria-sha256", bt_amb_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 2,
    "AMBIENTE_PYTHON_INJETAVEL", bancada=B2, env_extra=dict(PYTHONPATH=str(FX / "n5vazio")), extra_ok=lambda j, r: j.get("recibo") is None,''',
      '''run("N5_PYTHONPATH_sem_E_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_amb, "--bateria-sha256", bt_amb_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 2,
    "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-B", "-X", "utf8"), env_extra=dict(PYTHONPATH=str(FX / "n5vazio")), extra_ok=lambda j, r: j.get("recibo") is None,''')
troca('''run("R31_A4_appdata_de_ataque_esboco_com_s", _ARGS_A4, 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-s", "-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: _a4_ok("R31_A4_appdata_de_ataque_esboco_com_s", j, True),''',
      '''run("R31_A4_appdata_de_ataque_esboco_com_s", _ARGS_A4, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-s", "-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: (lambda m_: j.get("recibo") is None and not m_)(MARCAS_A4.setdefault("R31_A4_appdata_de_ataque_esboco_com_s", _marcas_e_limpa())),''')
troca('''run("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", _ARGS_A4, 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: _a4_ok("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", j, False),''',
      '''run("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", _ARGS_A4, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: (lambda m_: j.get("recibo") is None and len(m_) >= 1 and all("sincronizar_bancada.py" in v_ for v_ in m_.values()))(
        MARCAS_A4.setdefault("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", _marcas_e_limpa())),''')
i_a4 = t.index('_lanc_dir = FX / "a4_lancador_adulterado"')
t = t[:i_a4] + '''run("R32_A4_appdata_de_ataque_esboco_com_I", _ARGS_A4, 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-I", "-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: _a4_ok("R32_A4_appdata_de_ataque_esboco_com_I", j, True),
    nota="A4/R31-1 (R3.2): o mesmo APPDATA de ataque, com o esboco chamado como exigido (-I -B -X utf8): nenhuma marca de .pth nem de usercustomize em processo "
         "nenhum; os testes com -E -P -s pelo lancador; numpy segue importavel no filho e no neto")
''' + t[i_a4:]
# (4) o bloco R32 antes do run 2
anc = "# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado\n"
troca(anc, BLOCO + "\n" + anc)
# (4b) depois do 2bis: o manifesto B3 registra o manifesto do kernel anterior e o 2bis cruzou por ele
troca('''b2s = RAIZ / "b2s"
copiar_sem_juncao(B2, b2s)''', '''checar("R32_R31_3_manifesto_B3_registra_o_kernel_anterior",
       lambda: json.loads((B2 / "canonical_contracts.json").read_bytes())["sincronizacao"]["anterior"]["kernel_manifesto_sha256"] == sha(KMAN_ANT),
       nota="R31-3: o bloco sincronizacao.anterior do manifesto B3 (gravado pelo run 2) traz o manifesto do kernel v391 que o selo anterior pina")
checar("R32_R31_3_RUN_2bis_cruzou_pelo_registro_do_manifesto",
       lambda: (lambda rec: rec["recibo_pre_selo"]["kernel_cruzado_com_o_selo_anterior"]["registrado_no_manifesto_da_bancada"] == sha(KMAN_ANT)
                and rec["recibo_pre_selo"]["kernel_manifesto_anterior_sha256"] == sha(KMAN_ANT))(
           json.loads(sorted((S / "RUN_2bis_idempotente").glob("RECIBO_SINCRONIZACAO_*.json"))[-1].read_bytes())),
       nota="R31-3: na re-execucao (ja sincronizada), o pino do selo anterior confere tambem com o que o manifesto B3 registrou")
b2s = RAIZ / "b2s"
copiar_sem_juncao(B2, b2s)''')
# (5) o fecho: a comparacao com a R3.1 e o arquivo de saida
troca('''R3_RES = json.loads((R3 / "CONTROLES_NEGATIVOS_R3.json").read_bytes())''',
      '''R31_RES = json.loads((R31 / "CONTROLES_NEGATIVOS_R3_1.json").read_bytes())
R31_NOMES = [c["controle"] for c in R31_RES["controles"]]
faltam_r31 = sorted(set(R31_NOMES) - set(nomes))
NOVOS_R32 = [x for x in nomes if x not in set(R31_NOMES)]
MUDARAM_R32 = {}
for x in sorted(set(INJETADOS_SELO)):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append("R31-3: o comando ganhou --selo-anterior/--kernel-manifesto-anterior (a custodia v391 do sandbox), porque o B(n) R3.2 cruza o "
                                             "recibo pre-selo com o pino externo do kernel anterior; o resto do comando e a recusa esperada nao mudaram")
for x, motivo in (("A9_sem_B_nenhum_pycache", "R31-1: sem -B o esboco R3.2 recusa (INTERPRETADOR_NAO_ISOLADO) antes de qualquer import; o controle (agora -I -X utf8, sem -B) "
                                              "confere que nada e gravado e nenhum __pycache__ nasce; a forma valida ficou em R32_A9_com_I_e_B_nenhum_pycache"),
                  ("N5_PYTHONPATH_injetado_nao_chega_ao_teste", "R31-1: o esboco chamado com -I (que inclui -E) em vez de -E"),
                  ("N5_PYTHONPATH_sem_E_recusado", "R31-1: sem -I a recusa e a do topo, INTERPRETADOR_NAO_ISOLADO, antes da guarda AMBIENTE_PYTHON_INJETAVEL (que segue no "
                                                   "codigo como defesa em profundidade, inalcancavel por subprocesso sob -I)"),
                  ("R31_A4_appdata_de_ataque_esboco_com_s", "R31-1: com -s (sem -I) o esboco R3.2 recusa (INTERPRETADOR_NAO_ISOLADO); nenhuma marca; a forma valida e "
                                                            "R32_A4_appdata_de_ataque_esboco_com_I"),
                  ("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", "R31-1: sem -I o esboco recusa; o .pth/usercustomize do APPDATA herdado ainda roda no "
                                                                                 "processo do esboco ANTES da 1a linha (residuo da chamada errada), e nada e gravado")):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append(motivo)
for x in ("R31_N2c_selo_e_kernel_de_outro_rito", "R31_N2c_so_o_selo_trocado", "R31_N2c_kernel_que_o_selo_dele_nao_pina", "R31_N2c_recibo_sem_selo",
          "R31_N2c_contraprova_recibo_1b_aceito"):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append("R31-3: a chamada unitaria de conferir_recibo_pre_selo passa o selo e o manifesto do kernel anteriores (custodia do sandbox)")
GERAIS_R32 = ["R31-1: todo subprocesso do esboco roda com -I -B -X utf8 (na R3.1, -B -X utf8); este script roda com -I -B -X utf8",
              "R31-4/12-ter: a fixture do recibo do kernel passou ao contrato KERNEL_RECIBO_R3_2 (+ varredura_tokens) e o build log sintetico traz as linhas "
              "de job do lake; os recibos invalidos sao derivados da fixture nova; o codigo de recusa esperado nao mudou",
              "R31-3: a arvore sintetica ganhou TGLExt/O16/SinteticoO16.lean (fora do manifesto) e o sandbox ganhou fx/custodia_v391/"]
R3_RES = json.loads((R3 / "CONTROLES_NEGATIVOS_R3.json").read_bytes())''')
troca('''out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.1 (13/10/2026)", raiz=str(RAIZ), script_sha256=sha(SYNC), bateria_sha256=BAT_SHA,''',
      '''out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.2 (13/10/2026)", raiz=str(RAIZ), script_sha256=sha(SYNC), bateria_sha256=BAT_SHA,
           interpretador_deste_script=dict(isolated=bool(sys.flags.isolated), dont_write_bytecode=bool(sys.flags.dont_write_bytecode), utf8_mode=bool(sys.flags.utf8_mode)),
           n_da_R3_1=len(R31_NOMES), da_R3_1_presentes=len(R31_NOMES) - len(faltam_r31), da_R3_1_ausentes=faltam_r31, n_novos_R3_2=len(NOVOS_R32), novos_R3_2=NOVOS_R32,
           controles_da_R3_1_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R32.items())],
           n_controles_da_R3_1_que_mudaram_de_formato=len(MUDARAM_R32), mudancas_gerais_R3_2=GERAIS_R32,
           custodia_v391_do_sandbox=dict(selo=_pinar(SELO_ANT), kernel_manifest=_pinar(KMAN_ANT)),''')
troca('''controles=RES, veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if n_pass == len(RES) and not faltam_r3 and not juncoes_restantes else "ALGUM_CONTROLE_NAO_RECUSOU"),''',
      '''controles=RES, veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if n_pass == len(RES) and not faltam_r3 and not faltam_r31 and not juncoes_restantes
                                    else "ALGUM_CONTROLE_NAO_RECUSOU"),''')
troca('''(AQUI / "CONTROLES_NEGATIVOS_R3_1.json").write_bytes(texto.encode("utf-8"))
print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R3 presentes %d/%d" % (out["da_R3_presentes"], len(R3_NOMES)), "%.0f s" % out["segundos"])''',
      '''(AQUI / "CONTROLES_NEGATIVOS_R3_2.json").write_bytes(texto.encode("utf-8"))
print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R3.1 presentes %d/%d" % (out["da_R3_1_presentes"], len(R31_NOMES)), "R3 presentes %d/%d" % (out["da_R3_presentes"], len(R3_NOMES)),
      "novos R3.2 %d" % len(NOVOS_R32), "%.0f s" % out["segundos"])''')
P.write_bytes(t.encode("utf-8"))
print("controles_negativos_r3_2.py: ok; chamadas unitarias de conferir_recibo_pre_selo trocadas:", n_unit)
