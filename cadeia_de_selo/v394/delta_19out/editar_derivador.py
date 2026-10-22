# -*- coding: utf-8 -*-
"""editar_derivador.py -- DELTA 19/10: edita derivar_instalar_rito_v394.py (backup de bytes ja' feito) para a INTEGRACAO FINAL: o numero de modulos novos deixa de ser digitado (189) e passa a ser LIDO da lista
(kernel_modulos_novos_v394.json / .lista.json, regenerada com a pedra do delta); o sandbox e' C:\\t\\k394d\\final e a arvore C:\\t\\k394d\\arvore; os logs/recibos ficam em kernel_d19; o candidato novo e' DL.CANDIDATO.
Cada troca tem assert de unicidade. NAO toca pos_rito."""
import ast, os, sys
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "derivar_instalar_rito_v394.py")
t = open(P, "rb").read().decode("utf-8")
assert "\r" not in t
n_edits = 0


def sub(old, new, count=1):
    global t, n_edits
    assert t.count(old) == count, ("troca", old[:100], t.count(old), count)
    t = t.replace(old, new); n_edits += 1


# ---- imports, sandbox, pasta dos logs, N lido da lista
sub('HERE = os.path.dirname(os.path.abspath(__file__)); CAD = os.path.dirname(HERE); V3 = os.path.join(CAD, "v393")\n',
    'HERE = os.path.dirname(os.path.abspath(__file__)); CAD = os.path.dirname(HERE); V3 = os.path.join(CAD, "v393"); sys.path.insert(0, HERE)\nimport delta19_v394 as DL  # noqa: E402   (DELTA 19/10: sandbox k394d, logs em kernel_d19, candidato novo, pedra do delta)\n')
sub('SB = os.path.join(C, "t", "k394", "final")\n',
    'SB = DL.SANDBOX\n_NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))\n'
    'assert isinstance(_NJ.get("novos"), list) and DL.STONE_REL in _NJ["novos"] and len(set(_NJ["novos"])) == len(_NJ["novos"]), "kernel_modulos_novos_v394.json tem de trazer a LISTA, com a pedra do delta (preparar_kernel_v394.py)"\n'
    'N_NOVOS = len(_NJ["novos"])   # LIDO da lista dos modulos novos (189 do Codex + a pedra do delta de 19/10): nada digitado\n')
sub('p = os.path.join(HERE, "kernel", "construir_marcas.txt")', 'p = os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")')
sub('"189 modulos a mais que a v393; o timeout do lake build DENTRO do um.py (candidato) tem de caber no tempo medido.")', '"os modulos novos a mais que a v393; o timeout do lake build DENTRO do um.py (candidato) tem de caber no tempo medido.")')
sub('(frio nos 190 modulos novos)', '(frio nos modulos novos)')
# ---- a lista: sandbox x Nos, comparada com a do preparar (sem 189 digitado)
sub('    assert len(novos) == 189 and not removidos, ("o sandbox nao traz exatamente 189 modulos novos e nenhum a menos", len(novos), removidos[:3])\n',
    '    assert not removidos and sorted(novos) == sorted(_NJ["novos"]) and DL.STONE_REL in novos, ("o sandbox (sandbox x Nos) nao traz exatamente os modulos novos da lista (com a pedra do delta) e nenhum a menos", len(novos), len(_NJ["novos"]), removidos[:3])\n')
sub('    assert n_dito in (None, 189), ("kernel_modulos_novos_v394.json diz outro numero", n_dito)\n', '    assert n_dito in (None, len(novos)), ("kernel_modulos_novos_v394.json diz outro numero", n_dito)\n')
sub('"fonte": "diferenca dos .lean de TGLExt/ entre o sandbox C:/t/k394/final e o tgl_kernel do Nos (v393 instalada); so\' leitura"', '"fonte": "diferenca dos .lean de TGLExt/ entre o sandbox " + SB.replace(os.sep, "/") + " e o tgl_kernel do Nos (v393 instalada); so\' leitura"')
# ---- instalar
sub('t = troca(t, "(a v394 traz 3 pedras: o proprio rito as materializa a partir do corpo embutido)", "(a v394 traz 189 modulos novos de kernel: o proprio rito os materializa a partir do corpo embutido)", nome="docstring pedras")',
    't = troca(t, "(a v394 traz 3 pedras: o proprio rito as materializa a partir do corpo embutido)", "(a v394 traz %d modulos novos de kernel: o proprio rito os materializa a partir do corpo embutido)" % N_NOVOS, nome="docstring pedras")\n'
    't = troca(t, \'CAND = os.path.join(HERE, "um_v394_candidato.py")\', \'CAND = os.path.join(HERE, "%s")\' % DL.CANDIDATO, nome="candidato novo")')
sub("(b) NENHUM dos 189 modulos novos da v394 esta la ainda.", "(b) NENHUM dos modulos novos da v394 (os do Codex e a pedra do criterio binario de parada) esta la ainda.")
sub('assert len(NOVOS_V394) == _N_DITO == 189 and len(set(NOVOS_V394)) == 189 and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in NOVOS_V394), ("a lista dos modulos novos nao e\' a de 189 .lean de TGLExt/", len(NOVOS_V394), _N_DITO, _FONTE_NOVOS)',
    'assert len(NOVOS_V394) == _N_DITO and len(set(NOVOS_V394)) == _N_DITO and ESP["kernel"]["modulos_novos"] == _N_DITO and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in NOVOS_V394), ("a lista dos modulos novos nao e\' a do ESPERADOS (.lean de TGLExt/)", len(NOVOS_V394), _N_DITO, _FONTE_NOVOS)')
sub('"algum dos 189 modulos novos (v394) ja esta no kernel do Nos -- nao instalo"', '"algum dos modulos novos (v394) ja esta no kernel do Nos -- nao instalo"')
# ---- rito
sub('"189 modulos novos de kernel (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/*) materializados", nome="pedras no rito")',
    '"%d modulos novos de kernel (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/* e a pedra do criterio binario de parada) materializados" % N_NOVOS, nome="pedras no rito")')
sub('"os registros por spec e os cinco registros novos do core v394 (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394)"',
    '"os registros por spec e os seis registros novos do core v394 (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394, criterio_binario_de_parada_v394)"')
# ---- reverter
sub('"e poe os 189 modulos novos de kernel da v394 em QUARENTENA (nunca apaga; guarda o caminho relativo).", nome="doc quarentena")', '"e poe os %d modulos novos de kernel da v394 em QUARENTENA (nunca apaga; guarda o caminho relativo)." % N_NOVOS, nome="doc quarentena")')
sub("ESPERADOS_v394, a lista dos 189 modulos novos e a ancora do hash da v393 selada", "ESPERADOS_v394, a lista dos modulos novos e a ancora do hash da v393 selada")
sub('assert len(_lista) == len(set(_lista)) == 189 and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in _lista), ("a lista dos modulos novos da v394 nao tem 189 .lean de TGLExt/", len(_lista))',
    'assert len(_lista) == len(set(_lista)) == len(esp["pedras_sha256"]) and set(_lista) == set(esp["pedras_sha256"]) and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in _lista), ("a lista dos modulos novos da v394 difere de ESPERADOS.pedras_sha256", len(_lista))')
# ---- arvore pos-selo e sandbox: k394d e kernel_d19
sub("assert a.count(r'ARV = r\"C:\\t\\k394\\arvore\"') == 1, \"ARV nao ficou em k394\"\n",
    "a = a.replace(r'ARV = r\"C:\\t\\k394\\arvore\"', r'ARV = r\"C:\\t\\k394d\\arvore\"').replace('refaz C:/t/k394/arvore', 'refaz C:/t/k394d/arvore')\n"
    "assert a.count(r'ARV = r\"C:\\t\\k394d\\arvore\"') == 1, \"ARV nao ficou em k394d\"\n"
    "a = troca(a, '\"kernel\", \"KERNEL_RECIBO_v394.json\"', '\"%s\", \"KERNEL_RECIBO_v394.json\"' % DL.KERNEL_DIR, nome=\"recibo na pasta d19\")\n")
sub('L[1] = ("# refaz do ZERO o sandbox B do kernel da v394: copia o kernel que o Nos TEM (a v393 instalada), acrescenta os 189 modulos do Codex (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/*) e GERA a raiz e o Audit")',
    'L[1] = ("# refaz do ZERO o sandbox B do kernel da v394 (C:/t/k394d/final): copia o kernel que o Nos TEM (a v393 instalada), acrescenta os 189 modulos do Codex (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/*) e a pedra do criterio binario de parada e GERA a raiz e o Audit")')
sub('s = troca(s, "preparar_kernel_v394.py final", "preparar_kernel_v394.py gerar", nome="modo gerar")\n',
    's = troca(s, "preparar_kernel_v394.py final", "preparar_kernel_v394.py gerar", nome="modo gerar")\n'
    's = s.replace("/c/t/k394", "/c/t/k394d").replace("C:\\\\t\\\\k394\\\\", "C:\\\\t\\\\k394d\\\\")\n'
    'assert s.count("/c/t/k394d") == 1 and s.count("C:\\\\t\\\\k394d\\\\final") == 1 and s.count("C:\\\\t\\\\k394d\\\\robocopy_final.log") == 1 and "k394\\\\" not in s.replace("k394d\\\\", ""), "os caminhos do sandbox nao ficaram em k394d"\n')
# ---- invariantes
sub('"pilar_anterior_v393_", "APLICADO_AO_CANONICO_%s.json", "CM[\\"base_v393_sha16\\"]", "ESPERADOS_v394.json", "CANDIDATO_v394.json", "um_v394_candidato.py", "kernel_modulos_novos_v394.json",',
    '"pilar_anterior_v393_", "APLICADO_AO_CANONICO_%s.json", "CM[\\"base_v393_sha16\\"]", "ESPERADOS_v394.json", "CANDIDATO_v394.json", DL.CANDIDATO, "kernel_modulos_novos_v394.json",')
sub('"RuleTruthContract", "TheRuleAndTheFigureOfTruth", "TheRuleInTheContinuousMotor", "== 189", "NOVOS_V394", "modulos_novos_v394"],', '"RuleTruthContract", "TheRuleAndTheFigureOfTruth", "TheRuleInTheContinuousMotor", "== _N_DITO", "NOVOS_V394", "modulos_novos_v394"],')
sub('"rodada_v394_stdout.txt", "ESPERADOS_v394.json", "ANCORA", "ESPERADOS_v393.json", "== 189"],', '"rodada_v394_stdout.txt", "ESPERADOS_v394.json", "ANCORA", "ESPERADOS_v393.json", "set(_lista) == set(esp[\\"pedras_sha256\\"])"],')
sub('"refazer_sandbox_v394.sh": ["/c/t/k394", r"C:\\t\\k394\\final", "preparar_kernel_v394.py gerar",', '"refazer_sandbox_v394.sh": ["/c/t/k394d", r"C:\\t\\k394d\\final", "preparar_kernel_v394.py gerar",')
sub('"refazer_arvore_v394_pos_selo.py": ["KERNEL_RECIBO_v394.json", "shutil.rmtree(ARV)",', '"refazer_arvore_v394_pos_selo.py": ["KERNEL_RECIBO_v394.json", r\'ARV = r"C:\\t\\k394d\\arvore"\', "shutil.rmtree(ARV)",')
ast.parse(t)
open(P + ".tmp", "wb").write(t.encode("utf-8")); os.replace(P + ".tmp", P)
print("derivar_instalar_rito_v394.py: %d trocas; ast.parse ok; %d bytes" % (n_edits, len(t.encode("utf-8"))))
