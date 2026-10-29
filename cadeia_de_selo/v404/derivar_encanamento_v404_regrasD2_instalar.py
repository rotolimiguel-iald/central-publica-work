# -*- coding: utf-8 -*-
# regras (lote D2) de derivar_encanamento_v404.py: instalar, reverter, rito e a conferencia do instalar. ORIGEM v403. Mapa: 402 -> 403, 403 -> 404.
import re as _re_d2

# os tempos MEDIDOS da construcao do sandbox k404c (kernel/construir_marcas.txt: epoch_inicio, epoch_build_fim, epoch_audit_fim), lidos aqui na hora da derivacao (nada digitado)
_mk = {k_: int(v_) for k_, v_ in _re_d2.findall(r"^(epoch_[a-z_]+)=(\d+)$", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), _re_d2.M)}
_T_BUILD, _T_AUDIT = _mk["epoch_build_fim"] - _mk["epoch_inicio"], _mk["epoch_audit_fim"] - _mk["epoch_build_fim"]
_T_PASS = _T_BUILD + _T_AUDIT
_T_MIN = round(3 * _T_PASS / 60.0, 2)

entrada("instalar_v403.py", autoral=True, regras=[
    ("(a v404 traz TRES modulos novos de kernel, Caminho, Vida e VerdadeAdendo [os nomes do operador, 27/10/2026];", "(a v404 traz DOIS modulos novos de kernel, ProjecaoTransversalDaMeiaNat [nome PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro] e Jo8v32 [o nome do operador, 28/10/2026];", 1),
    ("escrito em 27/10/2026, NAO executado na preparacao). Molde: instalar_v403.py.", "escrito em 28/10/2026, NAO executado na preparacao). Molde: instalar_v403.py.", 1),
    ('_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")',
     '_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo")', 1),
    ("(b) os tres modulos novos da v404 (Caminho, Vida, VerdadeAdendo) NAO estao la ainda.", "(b) os dois modulos novos da v404 (ProjecaoTransversalDaMeiaNat, Jo8v32) NAO estao la ainda.", 1),
    ("QuedaSemGeometria e EsperancaCondicional) JA estao no kernel do Nos (a base instalada e' a v403 selada);", "QuedaSemGeometria, EsperancaCondicional, Caminho, Vida e VerdadeAdendo) JA estao no kernel do Nos (a base instalada e' a v403 selada);", 1),
])
entrada("reverter_v403.py", autoral=True, regras=[
    ("escrito em 27/10/2026, NAO executado na preparacao).", "escrito em 28/10/2026, NAO executado na preparacao).", 1),
])
entrada("rito_v403.sh", autoral=True, regras=[
    ("# O RITO v404 (ato da gerencia c1, preparado em 27/10/2026): roda o um.py v404 instalado no Nos -- 3 modulos novos de kernel (TGLExt/Caminho, TGLExt/Vida e TGLExt/VerdadeAdendo: os nomes do operador, 27/10/2026; o numero e' lido de kernel_modulos_novos_v404.json)",
     "# O RITO v404 (ato da gerencia c1, preparado em 28/10/2026): roda o um.py v404 instalado no Nos -- 2 modulos novos de kernel (TGLExt/ProjecaoTransversalDaMeiaNat, nome PROVISORIO da gerencia, e TGLExt/Jo8v32, o nome do operador, 28/10/2026; o numero e' lido de kernel_modulos_novos_v404.json)", 1),
    ("# construidos pelo proprio um.py, os QUATRO registros com FUNCAO caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 (chamados no main logo depois da esperanca condicional da v403; o ultimo e' a F8.1: as tres bandeiras literais do gate passam a calculadas e a letra do veredito nao muda), os registros por spec novos do core v404 (cunhagens_v403, com as duas falas de 27/10,",
     "# construidos pelo proprio um.py, os TRES registros com FUNCAO projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 (a projecao e o jo8v32 chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B e o livro da v383 ja' estao no core -- licao da 1a tentativa, 28/10; a errata de F2b e' AO LADO: o V1 segue congelado por hash; o gate e a funcao do neutrino nao mudam), os registros por spec novos do core v404 (cunhagens_v404, com as nove falas de 28/10,", 1),
    ("no sandbox k404c, 1 lake build INCREMENTAL (a v403 selada, com as tres pedras da v403, ja' esta compilada em .lake/build; as tres pedras novas, Caminho, Vida e VerdadeAdendo, compilam agora; muda a raiz TGLExt; o Audit nao muda) = 371 s e 1 Audit = 228 s",
     "no sandbox k404c, 1 lake build INCREMENTAL (a v403 selada, com as tres pedras da v403, ja' esta compilada em .lake/build; as duas pedras novas, ProjecaoTransversalDaMeiaNat e Jo8v32, compilam agora; muda a raiz TGLExt; o Audit nao muda) = %d s e 1 Audit = %d s" % (_T_BUILD, _T_AUDIT), 1),
])
entrada("conferir_instalar_rito_v403.py", autoral=True, regras=[
    ("(a LISTA, de tres elementos)", "(a LISTA, de dois elementos)", 1),
    ("(aceita a lista de tres elementos;", "(aceita a lista de dois elementos;", 1),
    ('"TGLExt/Caminho", "TGLExt/Vida", "TGLExt/VerdadeAdendo"],', '"TGLExt/ProjecaoTransversalDaMeiaNat", "TGLExt/Jo8v32"],', 1),
    ('"instalar: o trecho da lista de modulos novos RECUSOU com N=3: %s"', '"instalar: o trecho da lista de modulos novos RECUSOU com N=2: %s"', 1),
    ('{"passa_com_N_igual_a_tres": n_passa == 3,', '{"passa_com_N_igual_a_dois": n_passa == 2,', 1),
    ("if ESP and n_passa != 3:\n    falhas.append(\"instalar: o trecho da lista nao passou com N = 3 (%r)\" % (n_passa,))", "if ESP and n_passa != 2:\n    falhas.append(\"instalar: o trecho da lista nao passou com N = 2 (%r)\" % (n_passa,))", 1),
])
