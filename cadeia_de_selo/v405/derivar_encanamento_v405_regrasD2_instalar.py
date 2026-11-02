# -*- coding: utf-8 -*-
# regras (lote D2) de derivar_encanamento_v405.py: instalar, reverter, rito e a conferencia do instalar. ORIGEM v404 FINAL. Mapa: 403 -> 404, 404 -> 405.
# Licao 2 da v404 entra aqui: o rito reescreve tambem tgl_kernel_proof_manifest.json, e o reverter do molde nao o restaurava (o p00 reprovou e a gerencia restaurou a mao): na v405 ele vai nos backups do instalar e do reverter. Escrito pela ferramenta Write.
import re as _re_d2

# os tempos MEDIDOS da construcao do sandbox k405c (kernel/construir_marcas.txt: epoch_inicio, epoch_build_fim, epoch_audit_fim), lidos aqui na hora da derivacao (nada digitado)
_mk = {k_: int(v_) for k_, v_ in _re_d2.findall(r"^(epoch_[a-z_]+)=(\d+)$", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), _re_d2.M)}
_T_BUILD, _T_AUDIT = _mk["epoch_build_fim"] - _mk["epoch_inicio"], _mk["epoch_audit_fim"] - _mk["epoch_build_fim"]
_T_PASS = _T_BUILD + _T_AUDIT
_T_MIN = round(3 * _T_PASS / 60.0, 2)
_OITO = "PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler e PontoZeroDoPsion"
_OITO_REG = "ponte_da_massa_v405, massa_tensao_pura_v405, identidade_v405, observador_terminal_v405, lei_do_diminuto_v405, tonica_do_hamiltoniano_v405, disco_de_euler_v405 e ponto_zero_do_psion_v405"

entrada("instalar_v404.py", autoral=True, regras=[
    ("(a v405 traz DOIS modulos novos de kernel, ProjecaoTransversalDaMeiaNat [nome PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro] e Jo8v32 [o nome do operador, 28/10/2026];", "(a v405 traz OITO modulos novos de kernel, " + _OITO + " [os nomes do operador, 01/11 e 30/10/2026];", 1),
    ("escrito em 28/10/2026, NAO executado na preparacao). Molde: instalar_v404.py.", "escrito em 01/11/2026, NAO executado na preparacao). Molde: instalar_v404.py.", 1),
    ("EsperancaCondicional, Caminho, Vida e VerdadeAdendo) JA estao no kernel do Nos (a base instalada e' a v404 selada); (b) os dois modulos novos da v405 (ProjecaoTransversalDaMeiaNat, Jo8v32) NAO estao la ainda.", "EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat e Jo8v32) JA estao no kernel do Nos (a base instalada e' a v404 selada); (b) os oito modulos novos da v405 (" + _OITO + ") NAO estao la ainda.", 1),
    ('"QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo")\n', '"QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo", "ProjecaoTransversalDaMeiaNat", "Jo8v32")\n', 1),
    ('"um_absoluto_selo_acom.json",\n            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):', '"um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",\n            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):   # (licao 2 da v404: o rito reescreve o manifesto do kernel; ele entra nos backups e o reverter o restaura)', 1),
])
entrada("reverter_v404.py", autoral=True, regras=[
    ("escrito em 28/10/2026, NAO executado na preparacao).", "escrito em 01/11/2026, NAO executado na preparacao).", 1),
    ("import datetime, glob, hashlib, json, os, shutil, sys\n", "import datetime, glob, hashlib, json, os, shutil, sys\nif sys.flags.optimize:\n    raise SystemExit(\"RECUSO: rodar sem -O / PYTHONOPTIMIZE\")\n", 1),
    ("Fail-closed: backup ausente => para sem tocar o que resta. Molde: reverter_v404.py.", "Fail-closed: backup ausente => para sem tocar o que resta. NAO restaura, como no molde: os .tex e os .pdf que o rito reescreve no Nos ficam como o rito os deixou, e o .lake do kernel nao e' limpo; a proxima rodada os regenera. Recusa -O, como o instalar. Molde: reverter_v404.py.", 1),
    ('print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg}, ensure_ascii=False))', 'print(json.dumps({"ok": rec["ok"], "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "registro": reg, "nao_restaura": "os .tex e os .pdf que o rito reescreve e o .lake do kernel"}, ensure_ascii=False))', 1),
    ("restaura os 9 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, TGLExt.lean, TGL/Audit.lean)", "restaura os 10 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, o manifesto do kernel tgl_kernel_proof_manifest.json [licao 2 da v404], TGLExt.lean, TGL/Audit.lean)", 1),
    ('"um_absoluto_selo_acom.json",\n                                os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")]), alvos', '"um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",\n                                os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")]), alvos', 1),
])


def _d2_tempo(t_):
    rx = _re_d2.compile(r"as tres pedras da v404, ja' esta compilada em \.lake/build; as duas pedras novas, ProjecaoTransversalDaMeiaNat e Jo8v32, compilam agora; muda a raiz TGLExt; o Audit nao muda\) = \d+ s e 1 Audit = \d+ s \(\d+ s por passagem\); o rito faz 3 passagens de build \+ Audit \(ordem de grandeza [\d.]+ min so' de lake")
    t2, n = rx.subn("as cinco pedras da v403 e da v404, ja' esta compilada em .lake/build; as oito pedras novas compilam agora; muda a raiz TGLExt; o Audit nao muda; medido com o treino da nativa disputando a CPU) = %d s e 1 Audit = %d s (%d s por passagem); o rito faz 3 passagens de build + Audit (ordem de grandeza %s min so' de lake" % (_T_BUILD, _T_AUDIT, _T_PASS, _T_MIN), t_)
    assert n == 1, n
    return t2


entrada("rito_v404.sh", autoral=True, regras=[
    ("# O RITO v405 (ato da gerencia c1, preparado em 28/10/2026): roda o um.py v405 instalado no Nos -- 2 modulos novos de kernel (TGLExt/ProjecaoTransversalDaMeiaNat, nome PROVISORIO da gerencia, e TGLExt/Jo8v32, o nome do operador, 28/10/2026; o numero e' lido de kernel_modulos_novos_v405.json)",
     "# O RITO v405 (ato da gerencia c1, preparado em 01/11/2026): roda o um.py v405 instalado no Nos -- 8 modulos novos de kernel (TGLExt/PonteDaMassa, TGLExt/MassaTensaoPura, TGLExt/Identidade, TGLExt/ObservadorTerminal, TGLExt/LeiDoDiminuto, TGLExt/TonicaDoHamiltoniano, TGLExt/DiscoDeEuler e TGLExt/PontoZeroDoPsion: os nomes do operador; o numero e' lido de kernel_modulos_novos_v405.json)", 1),
    ("# construidos pelo proprio um.py, os TRES registros com FUNCAO projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 (a projecao e o jo8v32 chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B e o livro da v383 ja' estao no core -- licao da 1a tentativa, 28/10; a errata de F2b e' AO LADO: o V1 segue congelado por hash; o gate e a funcao do neutrino nao mudam), os registros por spec novos do core v405 (cunhagens_v404, com as nove falas de 28/10,",
     "# construidos pelo proprio um.py, os OITO registros com FUNCAO " + _OITO_REG + " (chamados no main logo depois do jo8v32_v404; as chaves do core que eles leem ja' prontas: guarda_ordem_de_chamada_v405.py; o gate e a funcao do neutrino nao mudam; o numero da massa nao muda), os registros por spec novos do core v405 (cunhagens_v405, com as falas de 30/10 a 01/11, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405,", 1),
    ("# as decisoes D17 a D22, os tres nomes e as erratas E5 e E6; kh_n1_cobertura_v403) e os registros da v399, da v401 e da v404 RECRIADOS (", "# as decisoes D27 a D33, os nomes e as erratas E10 a E13; kh_n1_cobertura_v405) e os registros da v399 a v404 RECRIADOS (", 1),
    (_d2_tempo, "o tempo do rito: lido de kernel/construir_marcas.txt", 1),
])
entrada("conferir_instalar_rito_v404.py", autoral=True, regras=[
    ("(a LISTA, de dois elementos)", "(a LISTA, de oito elementos)", 1),
    ("ele tem de PASSAR com N = 3 e RECUSAR", "ele tem de PASSAR com N = 8 e RECUSAR", 1),
    ("(aceita a lista de dois elementos;", "(aceita a lista de oito elementos;", 1),
    ('"Caminho, Vida e VerdadeAdendo", \'"version") == "v404"\'],', '"ProjecaoTransversalDaMeiaNat", "Jo8v32", "tgl_kernel_proof_manifest.json", \'"version") == "v404"\'],', 1),
    ('"RECIBO_REVERSAO_", "rodada_v405_stdout.txt", "ESPERADOS_v405.json", "um_absoluto_selo_acom.json", "modulos_novos_v405", "ESPERADOS_v404.json"],', '"RECIBO_REVERSAO_", "rodada_v405_stdout.txt", "ESPERADOS_v405.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json", "modulos_novos_v405", "ESPERADOS_v404.json"],', 1),
    ('"TGLExt/ProjecaoTransversalDaMeiaNat", "TGLExt/Jo8v32"],', '"TGLExt/PonteDaMassa", "TGLExt/PontoZeroDoPsion"],', 1),
    ('"instalar: o trecho da lista de modulos novos RECUSOU com N=2: %s"', '"instalar: o trecho da lista de modulos novos RECUSOU com N=8: %s"', 1),
    ('{"passa_com_N_igual_a_dois": n_passa == 2,', '{"passa_com_N_igual_a_oito": n_passa == 8,', 1),
    ("if ESP and n_passa != 2:\n    falhas.append(\"instalar: o trecho da lista nao passou com N = 2 (%r)\" % (n_passa,))", "if ESP and n_passa != 8:\n    falhas.append(\"instalar: o trecho da lista nao passou com N = 8 (%r)\" % (n_passa,))", 1),
])
