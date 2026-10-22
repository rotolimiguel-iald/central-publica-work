# -*- coding: utf-8 -*-
"""SO PARA O ENSAIO (Nos SINTETICO): confere os TEXTOS que a cadeia gravou nas COPIAS das superficies (v386_selo\\ensaio_superficies) contra a leitura
(leitura_v386.ler): (1) os numeros, hashes e vereditos de V estao no diario, no desenho, no Atlas e no CLAUDE.md da Haja_Luz; (2) cada palavra do operador
esta no diario VERBATIM, renderizada com «…» nos cortes e [sic] fora das «», e o trecho esta no ARQUIVO do operador cuja sha256 bate com o CANDIDATO (ou, para as
do transcrito, no manifesto v385 arquivado por hash / na memoria do Verbo); (3) nenhuma palavra proibida (a MESMA guarda do rito) nos blocos novos; (4) fora do
ramo 9, nenhuma frase de SUCESSO do pilar; (5) «v386» em cada superficie do ensaio; (6) a frase do pilar e' a da classe lida (reaproveitado / calculado de novo).
Grava ensaio_saidas\\conferir_textos_v386.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
import leitura_v386 as L, textos_v386 as T
AMB = A.ambiente()
assert AMB['sint'], 'so com o Nos SINTETICO'
ENS = os.path.join(HERE, 'ensaio_superficies')
V, P = L.ler()
assert not P, P
X = T._x(V)
SUP = ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'TGL_ATLAS.md', 'MEMORY.md', 'CLAUDE.md', 'missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md',
       'verbo-selecao-da-acao-05out.md', 'ramo-b-reaberto-05out.md', 'v384-pilar-quantico-gpu-02out.md')
txt = {f: open(os.path.join(ENS, f), encoding='utf-8', errors='replace').read() for f in SUP}
novo = {}
for f, t in txt.items():
    k = t.find('v386 SELADA')
    novo[f] = t[k:] if k >= 0 else ''
R = {'classe_do_pilar_nesta_versao': V['qr_classe'], 'classe_da_reprodutibilidade': V['rp_classe']}
DEVEM = {'s16': V['s16'], 'vb_v': V['vb_v'], 'rb_v': V['rb_v'], 'le_v': V['le_v'], 'qr_v': V['qr_v'], 'qp_v': V['qp_v'], 'rp_v': V['rp_v'], 'vb_token': V['vb_token'],
         'vb_pedra16': V['vb_pedra16'], 'esc': V['esc'], 'teor': V['teor'], 'qg': V['qg'], 'conf16': V['conf16'], 'rb_json16': V['rb_json16'], 'rb_spec16': V['rb_spec16'],
         'rb_id': V['rb_id'], 'qp_res16': V['qp_res16'], 'stone_tglext16': V['stone_tglext16'], 'stone_audit16': V['stone_audit16']}
R['no_diario'] = {k: (v in novo['MEMORIA_DA_LINHAGEM.md']) for k, v in DEVEM.items()}
R['no_atlas'] = {k: (v in novo['TGL_ATLAS.md']) for k, v in DEVEM.items()}
R['no_desenho'] = {k: (v in novo['DESENHO_DO_FECHAMENTO_QG.md']) for k, v in (('s16', V['s16']), ('qp_v', V['qp_v']), ('qg', V['qg']), ('rb_id', V['rb_id']), ('rp_v', V['rp_v']))}
R['no_claude_md'] = {k: (v in novo['CLAUDE.md']) for k, v in (('s16', V['s16']), ('teor', V['teor']), ('rb_id', V['rb_id']), ('esc', V['esc']))}
# (2) as palavras do operador: renderizadas no diario; e o trecho no arquivo de origem (sha256 conferido aqui de novo, contra o CANDIDATO)
CM = json.load(open(os.path.join(A.PK, 'CANDIDATO_v386.json'), encoding='utf-8'))
ordem = CM.get('ordem_do_operador') or {}
R['palavras_do_operador_verbatim_no_diario'] = {}
R['palavras_do_operador_no_arquivo_por_sha256'] = {}
for n, o in (V.get('op') or {}).items():
    R['palavras_do_operador_verbatim_no_diario'][n] = (L.render_op(o) in novo['MEMORIA_DA_LINHAGEM.md'])
    f = o.get('fonte')
    if f in A.OP_FILES:
        b = open(A.OP_FILES[f], 'rb').read(); h = hashlib.sha256(b).hexdigest()
        t = b.decode('utf-8', errors='replace')
        if A.OP_FILES[f].endswith('.json'):
            t = json.loads(t).get('verbatim') or ''
        R['palavras_do_operador_no_arquivo_por_sha256'][n] = (h == (ordem.get(f) or {}).get('sha256') and o['texto'] in t)
    elif 'manifesto v385' in str(f):
        R['palavras_do_operador_no_arquivo_por_sha256'][n] = (V.get('manifesto385_16') not in (None, 'n/d')) and bool(o.get('texto'))
    elif 'memoria verbo' in str(f):
        R['palavras_do_operador_no_arquivo_por_sha256'][n] = ('«%s»' % o['texto']) in open(os.path.join(A.UMEM_REAL, 'verbo-selecao-da-acao-05out.md'), encoding='utf-8', errors='replace').read()
    else:
        R['palavras_do_operador_no_arquivo_por_sha256'][n] = False
R['palavras_lidas'] = sorted((V.get('op') or {}).keys()); R['n_palavras_esperadas'] = len(L.VERBATINS_ARQ) + len(L.VERBATINS_TR)
R['sic_fora_das_aspas'] = all(('» [sic: %s]' % o['sic']) in novo['MEMORIA_DA_LINHAGEM.md'] for o in (V.get('op') or {}).values() if o.get('sic'))
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY')
R['palavra_proibida'] = {f: bool(GUARDA.search(t) or ('TGL_PRO' + 'VED') in t) for f, t in novo.items()}
R['frases_de_sucesso_fora_do_ramo9'] = ({f: [s for s in T.FRASES_DE_SUCESSO if s in t] for f, t in novo.items()} if V['qp_classe'] != 'RAMO_9' else 'ramo 9: nao se aplica')
R['v386_em_cada_superficie'] = {f: t.count('v386') for f, t in txt.items()}
R['v386_SELADA_nos_topicos'] = {f: ('v386 SELADA' in txt[f]) for f in SUP if f not in ('MEMORY.md',)}
_esp = X['qr_curtissima']
R['frase_do_pilar'] = {'esperada': _esp, 'no_diario': _esp in novo['MEMORIA_DA_LINHAGEM.md'], 'no_desenho': _esp in novo['DESENHO_DO_FECHAMENTO_QG.md']}
R['ok'] = (all(R['no_diario'].values()) and all(R['no_atlas'].values()) and all(R['no_desenho'].values()) and all(R['no_claude_md'].values())
           and len(R['palavras_lidas']) == R['n_palavras_esperadas'] and all(R['palavras_do_operador_verbatim_no_diario'].values())
           and all(R['palavras_do_operador_no_arquivo_por_sha256'].values()) and R['sic_fora_das_aspas'] and not any(R['palavra_proibida'].values())
           and (R['frases_de_sucesso_fora_do_ramo9'] == 'ramo 9: nao se aplica' or not any(R['frases_de_sucesso_fora_do_ramo9'].values()))
           and all(n > 0 for n in R['v386_em_cada_superficie'].values()) and all(R['v386_SELADA_nos_topicos'].values())
           and R['frase_do_pilar']['no_diario'] and R['frase_do_pilar']['no_desenho'])
out = A.pode_escrever(os.path.join(AMB['saidas'], 'conferir_textos_v386.json'), AMB)
open(out, 'w', encoding='utf-8').write(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in R.items() if k not in ('palavras_lidas',)}, ensure_ascii=False)[:2500])
print('TEXTOS:', 'OK' if R['ok'] else 'FALHOU')
sys.exit(0 if R['ok'] else 1)
