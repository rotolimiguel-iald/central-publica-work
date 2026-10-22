# -*- coding: utf-8 -*-
"""SO PARA O ENSAIO (Nos SINTETICO): confere os TEXTOS que a cadeia gravou nas COPIAS das superficies (v385_selo\\ensaio_superficies) contra a leitura
(leitura_v385.ler): (1) os numeros, hashes e vereditos de V estao no diario, no desenho e no Atlas; (2) cada palavra do operador (lida do transcrito) esta
no diario VERBATIM; (3) nenhuma palavra proibida (a MESMA guarda do rito) nos blocos novos; (4) fora do ramo 9, nenhuma frase de SUCESSO do pilar;
(5) a frase da reprodutibilidade e' a da classe lida (bit a bit / arredondamento / diferente). Grava ensaio_saidas\\conferir_textos_v385.json."""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
import leitura_v385 as L, textos_v385 as T
AMB = A.ambiente()
assert AMB['sint'], 'so com o Nos SINTETICO'
ENS = os.path.join(HERE, 'ensaio_superficies')
V, P = L.ler()
assert not P, P
X = T._x(V)
txt = {f: open(os.path.join(ENS, f), encoding='utf-8').read() for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'TGL_ATLAS.md', 'MEMORY.md')}
# so os BLOCOS NOVOS (o que vem depois do cabecalho da v385 em cada arquivo)
novo = {}
for f, t in txt.items():
    k = t.find('v385 SELADA')
    novo[f] = t[k:] if k >= 0 else ''
R = {'variante_repro': V['rp_classe'], 'classe_do_pilar': V['qp_classe']}
DEVEM = {'s16': V['s16'], 'ax_v': V['ax_v'], 'rp_v': V['rp_v'], 'qp_v': V['qp_v'], 'ax_nome': V['ax_nome'], 'ax_pedra16': V['ax_pedra16'], 'esc': V['esc'], 'teor': V['teor'],
         'qg': V['qg'], 'rp_prev16': V['rp_prev16'], 'conf16': V['conf16']}
R['no_diario'] = {k: (v in novo['MEMORIA_DA_LINHAGEM.md']) for k, v in DEVEM.items()}
R['no_atlas'] = {k: (v in novo['TGL_ATLAS.md']) for k, v in DEVEM.items()}
R['no_desenho'] = {k: (v in novo['DESENHO_DO_FECHAMENTO_QG.md']) for k, v in (('s16', V['s16']), ('ax_nome', V['ax_nome']), ('qp_v', V['qp_v']), ('qg', V['qg']))}
R['palavras_do_operador_verbatim_no_diario'] = {n: (o['texto'] in novo['MEMORIA_DA_LINHAGEM.md']) for n, o in (V.get('op') or {}).items()}
R['palavras_lidas'] = sorted((V.get('op') or {}).keys())
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY')
R['palavra_proibida'] = {f: bool(GUARDA.search(t) or ('TGL_PRO' + 'VED') in t) for f, t in novo.items()}
R['frases_de_sucesso_fora_do_ramo9'] = ({f: [s for s in T.FRASES_DE_SUCESSO if s in t] for f, t in novo.items()} if V['qp_classe'] != 'RAMO_9' else 'ramo 9: nao se aplica')
_esp = {'BIT_A_BIT': 'iguais bit a bit', 'ARREDONDAMENTO': 'iguais a menos de arredondamento', 'DIFERENTE': 'DIFERENTES em'}.get(V['rp_classe'], 'não houve comparação')
R['frase_da_reprodutibilidade'] = {'esperada': _esp, 'no_diario': _esp in novo['MEMORIA_DA_LINHAGEM.md']}
R['ok'] = (all(R['no_diario'].values()) and all(R['no_atlas'].values()) and all(R['no_desenho'].values()) and len(R['palavras_lidas']) == len(L.VERBATINS)
           and all(R['palavras_do_operador_verbatim_no_diario'].values()) and not any(R['palavra_proibida'].values())
           and (R['frases_de_sucesso_fora_do_ramo9'] == 'ramo 9: nao se aplica' or not any(R['frases_de_sucesso_fora_do_ramo9'].values()))
           and R['frase_da_reprodutibilidade']['no_diario'])
out = A.pode_escrever(os.path.join(AMB['saidas'], 'conferir_textos_v385.json'), AMB)
open(out, 'w', encoding='utf-8').write(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps(R, ensure_ascii=False)[:1500])
print('TEXTOS:', 'OK' if R['ok'] else 'FALHOU')
sys.exit(0 if R['ok'] else 1)
