# -*- coding: utf-8 -*-
"""Adapta o conteudo da leitura_v385.py (gerada pelo converter_cadeia_v385.py a partir da leitura_v384.py): cada troca e' (antigo, novo) com a contagem
conferida (1 salvo dito); backup de BYTES antes; temporario -> conferir -> substituir; ast.parse do resultado."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "leitura_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = []

# (1) o cabecalho: o que a v385 le a mais
T.append(("""# pilar, e os textos dizem o aceite. Ensaiado classe a classe, de ponta a ponta (variantes_pilar_v385.py -> testar_formatos_v385.py e ensaio_guardas_v385.py).
import os, re, json, glob, hashlib, time, datetime""",
"""# pilar, e os textos dizem o aceite. (Na v384 isso foi ensaiado classe a classe; na v385 o ensaio da cadeia e' o ensaio_v385.py.)
# v385 (05/10/2026): a mais, le (a) O AXIOMA -- o registro the_axiom_v385 do core e do selo, as 28 declaracoes no axiom_report dentro do trio, a pedra no
# kernel do Nos por sha256, o nome do degrau final lido do kernel; nao selar e' PROBLEMA (o kernel nao e' item do pilar); (b) A REPRODUTIBILIDADE -- o
# registro quantum_pillar_reproducibility_v385, conferido contra o resultado pinado da v384 (sha256 e chave); o que ela DEU (bit a bit, arredondamento,
# diferente) e' RESULTADO, nunca problema; nao ter comparado, no ramo 9, e' problema; (c) AS PALAVRAS DO OPERADOR de 05/10, lidas do transcrito por
# script (mensagem achada pelo comeco; trecho por ancoras); (d) a custodia da v383 e da v384 no git (a custodia conjunta das tres e' decisao do operador).
# O kernel CRESCE (escada 5998 -> 6026; as bandeiras True = as da v384 + as 28); o pilar roda de NOVO sob o mesmo V1 (o veredito dele nao esta pinado:
# igual ao da v384 ou nao, e' o que a reprodutibilidade mede).
import os, re, json, glob, hashlib, time, datetime"""))
# (2) os itens do conferidor da v385 que falam SO do pilar (o texto exato dos itens do conferir_rito_v385.py)
T.append(("""PILAR_ITENS = ("o pilar RODOU nesta rodada", "o veredito do pilar e' da arvore congelada", "a cadeia de custodia do pilar confere",
               "o resultado foi GRAVADO no cache", "o selo registra o mesmo veredito e o mesmo sha256 do resultado", "o beta do trabalhador e' o do core",
               "o resultado do pilar esta no Nos e no hash do selo", "o terceiro balde da custodia de sentido existe e esta vazio",
               "details.jsonl e cpuref.json da rodada batem")""",
"""PILAR_ITENS = ("o pilar RODOU de novo nesta rodada", "o pilar rodou com a MESMA chave da v384", "o veredito do pilar e' da arvore congelada",
               "a cadeia de custodia do pilar confere", "o resultado novo foi GRAVADO no cache", "o resultado novo NAO e' o arquivo da v384",
               "o selo registra o mesmo veredito e o mesmo sha256 do resultado do pilar", "o beta do trabalhador e' o do core",
               "o resultado do pilar esta no Nos e no hash do selo", "o terceiro balde da custodia de sentido existe e esta vazio",
               "details.jsonl e cpuref.json da rodada batem", "a reprodutibilidade FOI MEDIDA")
# as classes da reprodutibilidade (lidas do token do veredito do runtime quantum_pillar_reproducibility_v385)
REPRO_TXT = {'BIT_A_BIT': 'iguais bit a bit', 'ARREDONDAMENTO': 'iguais a menos de arredondamento', 'DIFERENTE': 'DIFERENTES (é resultado, e fica dito)',
             'NAO_COMPARADO': 'não comparados nesta rodada', 'SEM_ANTERIOR': 'sem rodada anterior para comparar', 'DESCONHECIDO': 'veredito da reprodutibilidade fora da forma do runtime'}
# as palavras do operador de 05/10 que os textos citam: (nome, o COMECO da mensagem, a ancora do inicio do trecho, a ancora do fim do trecho -- inclusive;
# None = ate o fim da mensagem). Tudo LIDO do transcrito; nada digitado aqui alem das ancoras.
VERBATINS = (('custodia', 'excelente, conseguimos o que queríamos', 'antes de custodiar', 'tudo junto.'),
             ('espelho', 'excelente, conseguimos o que queríamos', 'penso que podemos espelhar', 'indexar a referência'),
             ('nome_axioma', 'excelente, conseguimos o que queríamos', 'Penso que podemos chamar o degrau', '"Axioma"'),
             ('posto', 'no começo da cadeia não é postulado', 'no começo da cadeia', 'python um.py"'),
             ('posicao', 'e posto faz muito mais sentido léxico', 'e posto faz', None),
             ('guarda', 'concordo com tudo, com uma pequena ressalva', 'O "posto" não é a "guarda"', 'cujo posto dá nome'),
             ('axioma', 'sim para tudo, é isso mesmo', 'agora sim alcançamos o fechamento', 'definição física de axioma'),
             ('observador', 'não existe observador não conjugado', 'não existe observador não conjugado', None),
             ('testemunha', 'testemunha falsa é a testemunha estática', 'testemunha falsa', None),
             ('conjugacao', 'isso mesmo, mas eu nunca disse', 'isso mesmo, mas eu nunca disse', None),
             ('prossiga', 'agora sim, concordo com tudo, prossiga', 'agora sim', None))"""))
# (3) as funcoes novas: as palavras do operador e a classe da reprodutibilidade
T.append(("""def sha(p):
    h = hashlib.sha256()""",
"""def _textos_transcrito(d):
    if d.get('type') == 'user':
        c = d.get('message', {}).get('content'); return [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    if d.get('type') == 'attachment' and (d.get('attachment') or {}).get('type') == 'queued_command':
        pr = d['attachment'].get('prompt'); return [pr] if isinstance(pr, str) else [x.get('text', '') for x in (pr or []) if isinstance(x, dict) and x.get('type') == 'text']
    return []


def palavras_do_operador(tr):
    \"\"\"{nome: {'quando': ISO, 'quando_txt': hora local, 'texto': trecho verbatim}} lido do transcrito; e a lista dos que NAO foram achados (vira problema).\"\"\"
    msgs = []
    for line in open(tr, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        for t in _textos_transcrito(d):
            t = (t or '').strip()
            if t and not t.startswith('<'):
                msgs.append((d.get('timestamp') or '', t))
    out, falta = {}, []
    for nome, comeco, a0, a1 in VERBATINS:
        ms = [(ts, t) for ts, t in msgs if t.startswith(comeco)]
        if not ms:
            falta.append('%s: nenhuma mensagem do operador comeca com %r' % (nome, comeco)); continue
        ts, t = ms[-1]
        if len({x[1] for x in ms}) > 1:
            falta.append('%s: mais de uma mensagem DIFERENTE comeca com %r' % (nome, comeco)); continue
        i = t.find(a0)
        j = (t.find(a1, i) + len(a1)) if a1 is not None else len(t)
        if i < 0 or (a1 is not None and t.find(a1, i) < 0):
            falta.append('%s: a ancora nao esta na mensagem (%r / %r)' % (nome, a0, a1)); continue
        out[nome] = {'quando': ts, 'quando_txt': _hora_local(ts), 'texto': t[i:j]}
    return out, falta


def classe_da_reprodutibilidade(v):
    if '__REPRODUCED_BIT_FOR_BIT__' in v:
        return 'BIT_A_BIT'
    if '__REPRODUCED_WITHIN_ROUNDOFF__' in v:
        return 'ARREDONDAMENTO'
    if '__NOT_REPRODUCED__' in v:
        return 'DIFERENTE'
    if '__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__' in v:
        return 'NAO_COMPARADO'
    if '__NO_PREVIOUS_RUN_TO_COMPARE__' in v:
        return 'SEM_ANTERIOR'
    return 'DESCONHECIDO'


def sha(p):
    h = hashlib.sha256()"""))
# (4) o candidato da v385 nao carrega os pinos do V1 (vem da v384, conferidos nos ESPERADOS): as conferencias sao contra ESPERADOS e o V1
T.append(("""    if not (V['pr_json64'] == ESP['prereg_sha256']['json'] == CM['prereg_sha256']['json'] and V['pr_md64'] == ESP['prereg_sha256']['md'] == CM['prereg_sha256']['md']):""",
          """    if not (V['pr_json64'] == ESP['prereg_sha256']['json'] and V['pr_md64'] == ESP['prereg_sha256']['md']):   # v385: o candidato nao carrega os pinos (ESPERADOS os conferiu no modulo)"""))
T.append(("""    if not (V['pr_spec64'] == PJ.get('spec_sha256') == ESP['spec_sha256'] == CM['spec_sha256']):""",
          """    if not (V['pr_spec64'] == PJ.get('spec_sha256') == ESP['spec_sha256']):"""))
T.append(("""    if not (V['pr_worker64'] == ESP['worker_sha256'] == CM['worker_sha256']):""",
          """    if not (V['pr_worker64'] == ESP['worker_sha256']):"""))
T.append(("""    if V['pr_verbatim'] != ((CM.get('ratificacao_do_operador') or {}).get('verbatim')) or RAT.get('spec_sha256_ratificada') != V['pr_spec64']""",
          """    if V['pr_verbatim'] in ('', 'AUSENTE') or RAT.get('spec_sha256_ratificada') != V['pr_spec64']"""))
# (5) a fumaca e a conferencia do congelamento sao da v384 (o trabalhador e o V1 sao os mesmos)
T.append(("""    _fu = sorted(glob.glob(os.path.join(PK, 'fumaca_v384_*', 'result.json')))
    _fuv = str(json.load(open(_fu[-1], encoding='utf-8')).get('verdict')) if _fu else 'AUSENTE'
    V['fumaca_txt'] = ('completou o caminho de código (`%s`; especificação de fumaça, nunca resultado do pilar)' % os.path.basename(os.path.dirname(_fu[-1]))) if '__FIVE_JUMP_GKLS__' in _fuv else ('NÃO completou (%s)' % _fuv[:80])""",
"""    _fu = sorted(glob.glob(os.path.join(A.PK384, 'fumaca_v384_*', 'result.json')))
    _fuv = str(json.load(open(_fu[-1], encoding='utf-8')).get('verdict')) if _fu else 'AUSENTE'
    V['fumaca_txt'] = (('não houve fumaça nova (o trabalhador e a especificação são os da v384); o ensaio a seco usou a fumaça da v384 (`%s`, que completou o caminho de código; '
                        'especificação de fumaça, nunca resultado do pilar)' % os.path.basename(os.path.dirname(_fu[-1]))) if '__FIVE_JUMP_GKLS__' in _fuv else ('a fumaça da v384 NÃO completou (%s)' % _fuv[:80]))"""))
T.append(("""        CC = json.load(open(os.path.join(PK, 'conferir_congelamento_v384_resultado.json'), encoding='utf-8'))['result']""",
          """        CC = json.load(open(os.path.join(A.PK384, 'conferir_congelamento_v384_resultado.json'), encoding='utf-8'))['result']   # o V1 e' o mesmo da v384"""))
# (6) a escada: o kernel CRESCE (28 declaracoes novas)
T.append(("""    elif [int(m.group(1)), int(m.group(2))] != ESP['escada_v384']:
        P.append('a escada do stdout (%s) != a da v384 em ESPERADOS (%s): o kernel devia ser o MESMO' % (V['teor'], ESP['escada_v384']))""",
"""    elif [int(m.group(1)), int(m.group(2))] != [ESP['escada_v385'][1]] * 2:
        P.append('a escada do stdout (%s) != a esperada da v385 (%s/%s)' % (V['teor'], ESP['escada_v385'][1], ESP['escada_v385'][1]))"""))
T.append(("""    if [lad.get('n_theorems_clean'), lad.get('n_theorems_expected')] != ESP['escada_v384']:
        P.append('a escada do core (%s) != a da v384 (%s)' % (V['esc'], ESP['escada_v384']))""",
"""    if [lad.get('n_theorems_clean'), lad.get('n_theorems_expected')] != [ESP['escada_v385'][1]] * 2:
        P.append('a escada do core (%s) != a esperada da v385 (%s/%s)' % (V['esc'], ESP['escada_v385'][1], ESP['escada_v385'][1]))
    V['esc_v384'] = '%s/%s' % tuple(ESP['escada_v384'])"""))
# (7) as bandeiras: as da v384 + exatamente as 28 da v385
T.append(("""    if V['n_flags_true'] != ESP['n_flags_true_v384']:
        P.append('bandeiras True do kernel %d != %d (v384)' % (V['n_flags_true'], ESP['n_flags_true_v384']))
    if {k: kf.get(k) for k in ESP['flags_gpf_gpc_v384']} != ESP['flags_gpf_gpc_v384']:""",
"""    _ft = sorted(k for k, v in kf.items() if v is True)
    if _ft != sorted(set(ESP['flags_true_v384']) | set(ESP['flags_v385'])):
        P.append('as bandeiras True do kernel (%d) != as da v384 (%d) + as 28 da v385' % (V['n_flags_true'], len(ESP['flags_true_v384'])))
    if {k: kf.get(k) for k in ESP['flags_gpf_gpc_gpi_v384']} != ESP['flags_gpf_gpc_gpi_v384']:"""))
# (8) as linhas do stdout: as do pilar continuam [v384] (o codigo do pilar e' o da v384); as da v385 sao [v385]
T.append(("""    V['v385_linhas'] = [l.strip() for l in out.splitlines() if '[v384]' in l and 'em curso' not in l]""",
          """    V['pilar_linhas'] = [l.strip() for l in out.splitlines() if '[v384]' in l and 'em curso' not in l]   # o codigo do pilar e' o da v384: imprime [v384]
    V['v385_linhas'] = [l.strip() for l in out.splitlines() if '[v385]' in l]"""))
T.append(("""    for _l in V['v385_linhas']:
        _m = re.match(""", """    for _l in V['pilar_linhas']:
        _m = re.match("""))
T.append(("""(o trabalhador da GPU foi lancado|REAPROVEITADO)', l) for l in V['v385_linhas'])""",
          """(o trabalhador da GPU foi lancado|REAPROVEITADO)', l) for l in V['pilar_linhas'])"""))
# (9) a custodia da v383 E da v384 no git; e as leituras novas da v385 (o Axioma, a reprodutibilidade, as palavras do operador), antes da data
T.append(("""    V['v384_commit'] = ''
    try:
        import subprocess
        _g = subprocess.run(['git', '-C', os.path.dirname(A.ATLAS_DIR_REAL), 'log', '--oneline', '-400'], capture_output=True, text=True, encoding='utf-8', timeout=60)
        _c = [l for l in _g.stdout.splitlines() if 'custodia(v384)' in l]
        V['v384_commit'] = _c[0][:80] if _c else ''
        V['v384_git_lido'] = _g.returncode == 0""",
"""    V['v384_commit'] = ''; V['v383_commit'] = ''
    try:
        import subprocess
        _g = subprocess.run(['git', '-C', os.path.dirname(A.ATLAS_DIR_REAL), 'log', '--oneline', '-400'], capture_output=True, text=True, encoding='utf-8', timeout=60)
        _c = [l for l in _g.stdout.splitlines() if 'custodia(v384)' in l]
        V['v384_commit'] = _c[0][:80] if _c else ''
        _c3 = [l for l in _g.stdout.splitlines() if 'custodia(v383)' in l]
        V['v383_commit'] = _c3[0][:80] if _c3 else ''
        V['v384_git_lido'] = _g.returncode == 0"""))
T.append(("""    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')""",
"""    # ---- (v385) O AXIOMA: o registro do core e do selo, as 28 declaracoes no axiom_report (trio), a pedra no kernel do Nos, o nome do degrau final
    ax = core.get('the_axiom_v385') or {}; sax = selo.get('the_axiom_v385') or {}
    V['ax_v'] = str(ax.get('verdict') or 'AUSENTE')
    V['ax_ok'] = '%s de %s' % (ax.get('kernel_flags_ok'), ax.get('kernel_flags_total'))
    V['ax_nome'] = str(ax.get('final_step_name_from_kernel') or 'AUSENTE'); V['ax_tag'] = str(ax.get('tag_for_omega_I') or 'AUSENTE')
    if not (ax.get('all_verified') is True and ax.get('kernel_flags_ok') == 28 and ax.get('kernel_flags_total') == 28 and V['ax_v'].startswith('TGL_THE_AXIOM_V385__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED__')):
        P.append('o Axioma nao selou nesta rodada (%s; %s)' % (V['ax_ok'], V['ax_v'][:90]))
    if not (ax.get('final_step_name_matches_kernel') is True and V['ax_nome'] == ESP['final_step_name'] and selo.get('final_step_name_v385') == ESP['final_step_name']):
        P.append('o nome do degrau final lido do kernel / do selo nao e o aprovado pelo operador (ESPERADOS)')
    if sax.get('verdict') != ax.get('verdict'):
        P.append('o registro do Axioma no selo != o do core')
    if GUARDA.search(V['ax_v']) or 'TGL_PRO' + 'VED' in V['ax_v']:
        P.append('o veredito do Axioma traz palavra proibida')
    V['ax_reading'] = str(selo.get('the_axiom_reading_v385') or 'AUSENTE')
    if V['ax_reading'] == 'AUSENTE' or GUARDA.search(V['ax_reading']) or 'TGL_PRO' + 'VED' in V['ax_reading']:
        P.append('a leitura the_axiom_reading_v385 do selo ausente ou com palavra proibida')
    _axr = kf.get('axiom_report') or {}
    _fora = [n for n in ESP['nomes_lean_v385'].values() if _axr.get(n) is None or not set(_axr.get(n) or []) <= {'propext', 'Classical.choice', 'Quot.sound'}]
    V['ax_decl'] = '%d de %d' % (len(ESP['nomes_lean_v385']) - len(_fora), len(ESP['nomes_lean_v385']))
    if _fora:
        P.append('declaracoes da v385 fora do trio ou ausentes do axiom_report: %s' % _fora[:4])
    _st = os.path.join(nos, 'tgl_kernel', 'TGLExt', 'TheAxiomAndTheFalseWitness.lean')
    V['ax_pedra16'] = sha(_st)[:16] if os.path.exists(_st) else 'AUSENTE'
    if V['ax_pedra16'] != ESP['kernel']['new']['TGLExt/TheAxiomAndTheFalseWitness.lean']:
        P.append('a pedra no kernel do Nos (%s) nao e a do candidato (%s)' % (V['ax_pedra16'], ESP['kernel']['new']['TGLExt/TheAxiomAndTheFalseWitness.lean']))
    V['ax_n_pedra'] = sum(1 for f in ESP['flags_v385'] if f.startswith('ext_axm_')); V['ax_n_dks'] = sum(1 for f in ESP['flags_v385'] if f.startswith('ext_dks_'))
    # ---- (v385) A REPRODUTIBILIDADE: o que ela deu e' RESULTADO; nao ter comparado no ramo 9 e' problema; o anterior tem de ser o pinado da v384
    rp = core.get('quantum_pillar_reproducibility_v385') or {}; srp = selo.get('quantum_pillar_reproducibility_v385') or {}
    V['rp_v'] = str(rp.get('verdict') or 'AUSENTE'); V['rp_classe'] = classe_da_reprodutibilidade(V['rp_v']); V['rp_txt'] = REPRO_TXT[V['rp_classe']]
    V['rp_n_fields'] = rp.get('n_fields', 'n/d'); V['rp_n_num'] = rp.get('n_numeric_fields', 'n/d'); V['rp_n_differ'] = rp.get('n_differ', 'n/d')
    V['rp_maxrel'] = _e(rp.get('max_rel_diff')); V['rp_same_v'] = _sim(rp.get('same_pillar_verdict'))
    _pv = rp.get('previous') or {}
    V['rp_prev16'] = str(_pv.get('sha256') or 'AUSENTE')[:16]; V['rp_prev_run8'] = str(_pv.get('run_id') or 'AUSENTE')[:8]
    V['rp_why'] = str(rp.get('why') or '')
    V['rp_dif_txt'] = '; '.join('`%s`: %s → %s' % (d_.get('field'), d_.get('previous'), d_.get('this_run')) for d_ in (rp.get('first_differences') or [])[:6]) or 'nenhuma'
    if V['rp_v'] == 'AUSENTE' or V['rp_classe'] == 'DESCONHECIDO':
        P.append('o registro da reprodutibilidade ausente ou fora da forma do runtime (%s)' % V['rp_v'][:80])
    if srp.get('verdict') != rp.get('verdict'):
        P.append('o registro da reprodutibilidade no selo != o do core')
    if rp.get('compared') is True:
        if _pv.get('sha256') != ESP['pilar_v384']['result_sha256'] or _pv.get('key') != ESP['pilar_v384']['key']:
            P.append('a reprodutibilidade comparou com um resultado que NAO e o pinado da v384 (%s)' % V['rp_prev16'])
    elif V['qp_classe'] == 'RAMO_9':
        P.append('ramo 9 sem a comparacao da reprodutibilidade (%s)' % V['rp_v'][:80])
    if GUARDA.search(V['rp_v']):
        P.append('o veredito da reprodutibilidade traz palavra proibida')
    V['qp_v384'] = ESP['pilar_v384']['verdict']; V['qp_igual_v384'] = _sim(V['qp_v'] == ESP['pilar_v384']['verdict'])
    V['qp_res384_16'] = ESP['pilar_v384']['result_sha256'][:16]
    # ---- (v385) AS PALAVRAS DO OPERADOR de 05/10 (lidas do transcrito por script)
    try:
        V['op'], _falta = palavras_do_operador(A.TRANSCRITO)
    except OSError as e_:
        V['op'], _falta = {}, ['o transcrito nao foi lido: %r' % e_]
    for f_ in _falta:
        P.append('palavras do operador: ' + f_)
    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')"""))
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:120])
    s = s.replace(a, b)
assert s != s0
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
bak = P + ".bak_" + st + "_adapt"
open(bak, "wb").write(s0.encode("utf-8")); assert open(bak, "rb").read() == s0.encode("utf-8")
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); assert os.path.getsize(P + ".tmp") > len(s0.encode("utf-8")); os.replace(P + ".tmp", P)
print("OK leitura_v385.py: %d trocas; %d -> %d B" % (len(T), len(s0.encode("utf-8")), os.path.getsize(P)))
