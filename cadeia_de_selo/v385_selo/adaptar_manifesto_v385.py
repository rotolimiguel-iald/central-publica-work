# -*- coding: utf-8 -*-
"""Adapta o manifesto_v385.py (gerado pelo conversor): os arquivos do pacote v385 e os registros novos (o Axioma, a reprodutibilidade, as palavras do
operador lidas do transcrito). Pares contados; backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "manifesto_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = []
T.append(("""PKF = ('ESPERADOS_v385.json', 'CANDIDATO_v385.json', 'conferir_rito_v385.py', 'v385_runtime.py', 'pilar_quantico_worker.py', 'artigo_pt_v385.pysnip', 'artigo_en_v385.pysnip',
       'gerar_candidato_v385.py', 'gerar_esperados_v385.py', 'instalar_v385.py', 'rito_v385.sh', 'ensaio_a_seco_v385.json', 'disposicoes_afericoes_v385.json', 'AFERIDOR_v385.txt',
       'conferir_congelamento_v384_resultado.json', 'registro_rascunhos_apresentados_v385.json')""",
"""PKF = ('ESPERADOS_v385.json', 'CANDIDATO_v385.json', 'conferir_rito_v385.py', 'v385_runtime.py', 'artigo_pt_v385.pysnip', 'artigo_en_v385.pysnip',
       'gerar_candidato_v385.py', 'gerar_esperados_v385.py', 'instalar_v385.py', 'rito_v385.sh', 'ensaio_a_seco_v385.py', 'ensaio_a_seco_v385.json',
       'disposicoes_afericoes_v385.json', 'AFERIDOR_v385.txt', os.path.join('kernel', 'sandbox_raiz_v385.json'), os.path.join('kernel', 'sandbox_axiom_report_v385.json'),
       os.path.join('kernel', 'AUDIT_NOMES_v385.json'))"""))
T.append(("""     'leitura_do_selo': V['qp_reading'], 'funcoes': ['quantum_pillar_start_v384', 'quantum_pillar_finish_v384', '_qp_summary'],""",
"""     'axioma': {'veredito': V['ax_v'], 'bandeiras': V['ax_ok'], 'declaracoes_no_trio': V['ax_decl'], 'pedra_sha16': V['ax_pedra16'], 'declaracoes_da_pedra': V['ax_n_pedra'],
                'declaracoes_do_darksplit': V['ax_n_dks'], 'nome_do_degrau_final': V['ax_nome'], 'etiqueta_de_omega_I': V['ax_tag'], 'leitura_do_selo': V['ax_reading'],
                'escada': {'v384': V['esc_v384'], 'v385': V['esc']}},
     'reprodutibilidade': {'veredito': V['rp_v'], 'classe': V['rp_classe'], 'campos': V['rp_n_fields'], 'numericos': V['rp_n_num'], 'diferem': V['rp_n_differ'],
                           'max_rel': V['rp_maxrel'], 'mesmo_veredito_do_pilar': V['rp_same_v'], 'anterior_sha16': V['rp_prev16'], 'anterior_run8': V['rp_prev_run8'],
                           'primeiras_diferencas': V['rp_dif_txt'], 'porque_nao': V['rp_why'], 'pilar_v384_veredito': V['qp_v384'], 'pilar_v384_result_sha16': V['qp_res384_16']},
     'palavras_do_operador_05out': V['op'],
     'custodia_no_git': {'v383': V['v383_commit'] or None, 'v384': V['v384_commit'] or None},
     'leitura_do_selo': V['qp_reading'], 'leitura_do_selo_v385': V['ax_reading'],
     'funcoes': ['the_axiom_v385', 'quantum_pillar_previous_v385', 'quantum_pillar_reproducibility_v385', 'quantum_pillar_start_v384', 'quantum_pillar_finish_v384', '_qp_summary'],"""))
T.append(("""     'base_v384': V['base16'],""", """     'base_v384': V['base16'], 'fumaca': V['fumaca_txt'],"""))
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK manifesto_v385.py: %d trocas" % len(T))
