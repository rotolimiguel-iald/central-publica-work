# -*- coding: utf-8 -*-
"""gerar_bateria.py -- escreve BATERIA_VINCULO.json: a bateria T01-T17 da frente H_BANCADA (BATERIA_FINAL_PROPOSTA_H12.json), na forma que
o sincronizar_bancada.py consome: copias byte a byte dos testes do tunel para a raiz da sincronizacao e, por teste, as FONTES PINADAS por
sha256 (calculado aqui, nunca digitado), o comando com marcadores, a verificacao e as fases. Esboco de 12/10/2026."""
import hashlib, json, datetime, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
O19 = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
H = Path(r"C:\IALD\PROGRAMA_IALD\exame_12out\H_BANCADA")
PY = "{py}"


def pin(p):
    b = Path(p).read_bytes()
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


def copia(de, para):
    b = Path(de).read_bytes()
    return dict(de=str(de), para=para, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


copias = [
    copia(O19 / "F0.3.B2/tests_core/test_core_synthetic.py", "tests_core/test_core_synthetic.py"),
    copia(O19 / "F0.3.B2/tests_core/run_core_suite.py", "tests_core/run_core_suite.py"),
    copia(O19 / "F0.3.B2/tests_core/test_deploy_transaction_fixture.py", "tests_core/test_deploy_transaction_fixture.py"),
    copia(O19 / "F0.3.B2/deploy_candidate.py", "deploy_candidate.py"),
    copia(O19 / "F0.3.B2/tests_channels/test_channels_r1.py", "tests_channels/test_channels_r1.py"),
    copia(O19 / "F0.3.B2/tests_channels/review_motor/test_material_r1.py", "tests_channels/review_motor/test_material_r1.py"),
    copia(O19 / "F0.3.B2/tests_channels/review_motor/fix_pantheon_rounding_r1.py", "tests_channels/review_motor/fix_pantheon_rounding_r1.py"),
    copia(O19 / "F0.3.B2/tests_motor/test_motor_synthetic.py", "tests_motor/test_motor_synthetic.py"),
    copia(O19 / "F8.2.NU3/tests/test_neutrino_candidate_r3.py", "nu3/test_neutrino_candidate_r3.py"),
    copia(O19 / "F8.2.NU3/tests/test_beta_scale_domain_r1.py", "nu3/test_beta_scale_domain_r1.py"),
]
B = []


def t(i, nome, fontes, comando, verificacao, fases=("pre_selo", "pos_selo"), obrigatorio_em=("ensaio", "aplicar"), cwd="{raiz}", timeout_s=900,
      estatuto_12out="", origem_h12=""):
    B.append(dict(id=i, teste=nome, fontes=[pin(f) for f in fontes], comando=comando, cwd=cwd, verificacao=verificacao, fases=list(fases),
                  obrigatorio_em=list(obrigatorio_em), timeout_s=timeout_s, estatuto_12out=estatuto_12out, origem_h12=origem_h12))


t("T01_IDENTIDADE", "pinos do contrato canonico da copia (um.py, selo, codigo, fontes) + beta em runtime bit a bit",
  [AQUI / "bateria/t01_identidade.py"],
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t01_identidade.py", "{candidate}", "{nos}", "{versao}", "{recibos}/T01_IDENTIDADE.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T01_IDENTIDADE.json", campos={"veredito": "PASSA"}),
  estatuto_12out="REAL: PASSA em 12/10 (H_BANCADA T01)", origem_h12="scripts/fidelidade.py b630f12a6a4b6d13")
t("T02_CANAIS", "canais N_eff/F7.2: extracao Tabela 5, recusas numericas, mutacao de bytes, alias, realocacao (13)",
  [O19 / "F0.3.B2/tests_channels/test_channels_r1.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/tests_channels/test_channels_r1.py", "--run", "{rotulo}"],
  dict(tipo="stdout_regex", regex=r"Ran 13 tests[\s\S]*\nOK"), timeout_s=1200,
  estatuto_12out="REAL: PASSA 13/13 em 12/10", origem_h12="F0.3.B2/tests_channels/test_channels_r1.py f03560385acf3e59")
t("T03_CORE", "identidade por operacao, guardas HTTP, quiescencia, formato GW (31)",
  [O19 / "F0.3.B2/tests_core/test_core_synthetic.py", O19 / "F0.3.B2/tests_core/run_core_suite.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/tests_core/run_core_suite.py", "{rotulo}"],
  dict(tipo="stdout_regex", regex=r"Ran 31 tests[\s\S]*\nOK"),
  estatuto_12out="REAL: PASSA 31/31 em 12/10", origem_h12="F0.3.B2/tests_core 1cf44f8ea3f316b5 / d9c5326bddc2173c")
t("T04_MOTOR", "motor sintetico: modos, conjuntos sobrepostos, Sidak nao global, posterior nao e p-valor (17)",
  [O19 / "F0.3.B2/tests_motor/test_motor_synthetic.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/tests_motor/test_motor_synthetic.py"],
  dict(tipo="stdout_regex", regex=r"Ran 17 tests[\s\S]*\nOK"),
  estatuto_12out="REAL: PASSA 17/17 em 12/10", origem_h12="F0.3.B2/tests_motor/test_motor_synthetic.py 987db4e8203f3762")
t("T05_MATERIAL", "regressoes materiais: dupla contagem, M perfilado, origem DR1 DECLARADO (8)",
  [O19 / "F0.3.B2/tests_channels/review_motor/test_material_r1.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/tests_channels/review_motor/test_material_r1.py"],
  dict(tipo="stdout_regex", regex=r"Ran 8 tests[\s\S]*\nOK"),
  estatuto_12out="REAL: PASSA 8/8 em 12/10", origem_h12="review_motor/test_material_r1.py 6de260053fa6df6b")
t("T06_PANTHEON_FORMATO", "5 testes de arredondamento da covariancia (classe extraida por AST, sem o passo de reescrita)",
  [O19 / "F0.3.B2/tests_channels/review_motor/fix_pantheon_rounding_r1.py", AQUI / "bateria/t06_pantheon_rounding.py"],
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t06_pantheon_rounding.py", "{candidate}", "{raiz}/tests_channels/review_motor/fix_pantheon_rounding_r1.py", "{recibos}/T06_PANTHEON_FORMATO.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T06_PANTHEON_FORMATO.json", campos={"veredito": "PASSA", "tests": 5}),
  estatuto_12out="REAL: PASSA 5/5 em 12/10", origem_h12="scripts/pantheon_rounding_tests.py c59688c9cfb359cc")
t("T07_NU3_CONTRATO", "contrato de neutrino: GKLS, RK4, semigrupo, positividade, traco, recusas (72)",
  [O19 / "F8.2.NU3/tests/test_neutrino_candidate_r3.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/nu3/test_neutrino_candidate_r3.py", "{candidate}/bancada/neutrino_contract.py", "{recibos}/T07_NU3_CONTRATO.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T07_NU3_CONTRATO.json", campos={"fail": 0, "pass": 72}), timeout_s=1800,
  estatuto_12out="REAL: PASSA 72/72 em 12/10", origem_h12="F8.2.NU3/tests/test_neutrino_candidate_r3.py f5fab3dba4524138")
t("T08_ESCALA_BETA_CHI", "beta(chi): positividade ou recusa visivel (4)",
  [O19 / "F8.2.NU3/tests/test_beta_scale_domain_r1.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/nu3/test_beta_scale_domain_r1.py", "{candidate}/bancada/neutrino_contract.py", "{recibos}/T08_ESCALA_BETA_CHI.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T08_ESCALA_BETA_CHI.json", campos={"fail": 0}),
  estatuto_12out="REAL: PASSA 4/4 em 12/10", origem_h12="F8.2.NU3/tests/test_beta_scale_domain_r1.py b2c8703de4e00e60")
t("T09_NU4_REPLAY", "16 chamadas sinteticas do piloto NU4 refeitas offline com a identidade canonica da copia (result bit a bit)",
  [AQUI / "bateria/t09_nu4_replay.py", O19 / "F8.2.NU4/PREREGISTRO_R1.json", O19 / "F8.2.NU4/RESULTADOS_R1.json"] + sorted((O19 / "F8.2.NU4").glob("CALL_*.json")),
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t09_nu4_replay.py", "{candidate}", "{tunel}/F8.2.NU4", "{recibos}/T09_NU4_REPLAY.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T09_NU4_REPLAY.json", campos={"veredito": "PASSA", "n_identical": 16}),
  estatuto_12out="REAL: PASSA 16/16 em 12/10", origem_h12="scripts/reproduzir_nu4.py 63a6b0b9e489eb8f")
t("T10_T11_CANAIS", "T10 canal F7.2 B2 (SEM_LIMITE_TGL, tau_star nulo, mapeamento OPEN, alias, guarda de palavra) + T11 N_eff (duas linhas Yp sem escolha; controle anti-dupla-contagem CPU)",
  [AQUI / "bateria/t10_t11_canais.py"],
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t10_t11_canais.py", "{candidate}", "{recibos}/T10_T11_CANAIS.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T10_T11_CANAIS.json", campos={"veredito": "PASSA", "T10": "PASSA", "T11": "PASSA"}), timeout_s=1800,
  estatuto_12out="REAL: PASSA em 12/10 (T10 e T11)", origem_h12="scripts/canais_f72_neff.py 3e05dbe9907ca17b")
t("T12_T13_T14_ATRATOR", "replay dos runners congelados do F1.ATRATOR (otico R3; ADENDO1 A5/A6; controle afim) contra os resultados arquivados",
  [AQUI / "bateria/t12_t14_atrator.py", O19 / "F1.ATRATOR/PREREGISTRO_R1.json", O19 / "F1.ATRATOR/numerical/run_optical_r3.py", O19 / "F1.ATRATOR/numerical/RUN_MANIFEST_R3.json",
   O19 / "F1.ATRATOR/numerical/RESULTADOS_NUMERICOS_R3.json", O19 / "F1.ATRATOR/ADENDO1/PREREGISTRO_ADENDO1_R1.json", O19 / "F1.ATRATOR/ADENDO1/numerical/run_adendo1_r1.py",
   O19 / "F1.ATRATOR/ADENDO1/numerical/RUN_MANIFEST_R1.json", O19 / "F1.ATRATOR/ADENDO1/numerical/RESULTADOS_ADENDO1_R1.json", O19 / "F1.ATRATOR/review/verify_affine_control_r1.py",
   O19 / "F1.ATRATOR/review/ADENDO_CONTROLE_AFIM_R1.json"],
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t12_t14_atrator.py", "{tunel}/F1.ATRATOR", "{raiz}/atrator/F1.ATRATOR", "{recibos}/T12_T13_T14_ATRATOR.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T12_T13_T14_ATRATOR.json", campos={"veredito": "PASSA"}), fases=("pre_selo",), timeout_s=1800,
  estatuto_12out="REAL: identicos ao arquivo em 12/10; os pre-registros pinam o um.py vigente -> SO antes do selo",
  origem_h12="scripts/replicar_atrator.py 638945e33ff67f4e")
t("T15_SONDAS", "sondas em RAM: versao seguinte sob o manifesto vigente (recusa); segunda linha de alpha; manifesto tipo B(n+1) com o mesmo beta",
  [AQUI / "bateria/t15_sondas.py"],
  [PY, "-B", "-X", "utf8", "{vinculo}/bateria/t15_sondas.py", "{candidate}", "{versao}", "{recibos}/T15_SONDAS.json"],
  dict(tipo="json_igual", arquivo="{recibos}/T15_SONDAS.json", campos={"veredito": "PASSA"}),
  estatuto_12out="REAL: PASSA em 12/10 (v392 sob B2 RECUSADO PIN_CHANGED)", origem_h12="scripts/sonda_v392.py 806dd9c80c34876b")
t("T16_DEPLOY_FIXTURE", "transacao de implantacao com falha injetada e rollback (2), em raiz curta",
  [O19 / "F0.3.B2/tests_core/test_deploy_transaction_fixture.py", O19 / "F0.3.B2/deploy_candidate.py"],
  [PY, "-B", "-X", "utf8", "{raiz}/tests_core/test_deploy_transaction_fixture.py"],
  dict(tipo="stdout_regex", regex=r"\"success\": true"),
  estatuto_12out="DECLARADO em 12/10 (WinError 206 no sandbox longo); PASSOU 2/2 no tunel em 09/10", origem_h12="F0.3.B2/tests_core/test_deploy_transaction_fixture.py 90a6ae57c317e3f3")
t("T17_LEAN_KERNEL", "o kernel da versao selada: lido do recibo do build da etapa 2 da cadeia (rc 0, zero sorry, log por hash); nunca recompilado aqui",
  [], ["(sem comando)"], dict(tipo="kernel_recibo"), fases=("pos_selo",), obrigatorio_em=("aplicar",),
  estatuto_12out="DERIVED em 12/10: as 4 pedras do atrator compiladas pela auditoria c1 de 10/10; a compilacao conjunta e da frente formal",
  origem_h12="H_BANCADA T17 (fp_antes.txt 4bc2c028f2892d37)")
out = dict(versao_bateria="VINCULO-12out-R1", quando=datetime.datetime.now().isoformat(timespec="seconds"),
           origem="BATERIA_FINAL_PROPOSTA_H12.json (exame_12out/H_BANCADA/registros) -- " + pin(H / "registros/BATERIA_FINAL_PROPOSTA_H12.json")["sha256"],
           marcadores="{py} {vinculo} {raiz} {candidate} {nos} {versao} {recibos} {tunel} {saida} {rotulo} {kernel_recibo}",
           copias=copias, testes=B, regra="um teste PASSA/FALHA/NAO_EXECUTADO; qualquer FALHA = bateria reprovada = nada se grava na Bancada",
           escopo="sintetica; nenhum dado observado aberto para veredito; nenhuma leitura fisica; gate NONE")
p = AQUI / "BATERIA_VINCULO.json"
if p.exists() and "--sobrescrever" not in sys.argv:
    raise SystemExit("ja existe: " + str(p) + " (use --sobrescrever)")
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("BATERIA_VINCULO.json:", hashlib.sha256(p.read_bytes()).hexdigest(), "testes:", len(B), "copias:", len(copias))
