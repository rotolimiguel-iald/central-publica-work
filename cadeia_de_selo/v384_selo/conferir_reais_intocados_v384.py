# -*- coding: utf-8 -*-
"""SO LEITURA: prova que o ENSAIO nao tocou nada real. `foto` grava o sha256 das superficies e ferramentas REAIS (e a lista das pastas reais) em
ensaio_saidas\\foto_reais_v384.json; `compara` refaz e compara, e procura nas pastas reais qualquer arquivo com as marcas que SO esta cadeia escreve
(_sup384, _comp384, _p384, _handoff384, v384_incorporacao_manifesto, handoff-v384-custodia, HANDOFF_v384_CUSTODIA). uso: python conferir_reais_intocados_v384.py foto|compara"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
TOP = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'beta-e-a-regra-matriz-02out.md', 'regra-dos-dois-regimes.md', 'v382-custodia-suspensa.md', 'v384-pilar-quantico-gpu-02out.md',
       'MEMORY.md', 'MEMORY_2.md')
ARQ = [os.path.join(A.NOS_REAL, f) for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'A_PROVA_DA_QG_TGL_arvore.md')]
ARQ += [os.path.join(A.ATLAS_DIR_REAL, f) for f in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md')] + [os.path.join(A.UMEM_REAL, f) for f in TOP]
ARQ += [os.path.join(A.TOOLS_REAL, f) for f in ('arvore_da_prova.py', 'atlas_indice.py')] + [r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl', A.PR_JSON, A.PR_MD]
PASTAS = [A.NOS_REAL, A.UMEM_REAL, A.ATLAS_DIR_REAL, A.TOOLS_REAL, r'C:\IALD\MAPA_DE_ROTAS']
MARCAS = ('_sup384', '_comp384', '_p384', '_handoff384', 'v384_incorporacao_manifesto', 'handoff-v384-custodia', 'HANDOFF_v384_CUSTODIA', 'SINTETICO_ENSAIO_V384',
          '_m384', 'tmp_m384', '_corretor', 'SINTETICO_VARIANTE_V384')   # corretor 04/10: o backup do manifesto em TOOLS e as marcas do corretor
FOTO = os.path.join(HERE, 'ensaio_saidas', 'foto_reais_v384.json')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def tirar():
    return {'arquivos': {p: ([os.path.getsize(p), sha(p)] if os.path.exists(p) else None) for p in ARQ},
            'pastas': {d: sorted(os.listdir(d)) for d in PASTAS}}


cmd = sys.argv[1] if len(sys.argv) > 1 else 'compara'
F = tirar()
marcadas = sorted({os.path.join(d, f) for d in PASTAS for f in F['pastas'][d] if any(m in f for m in MARCAS)})
if cmd == 'foto':
    os.makedirs(os.path.dirname(FOTO), exist_ok=True)
    open(FOTO, 'w', encoding='utf-8').write(json.dumps(F, ensure_ascii=False))
    print('foto: %d arquivos reais, %d pastas; arquivos com as marcas desta cadeia nas pastas reais: %s' % (len(ARQ), len(PASTAS), marcadas or 'nenhum'))
    sys.exit(0 if not marcadas else 1)
F0 = json.load(open(FOTO, encoding='utf-8'))
mud = [p for p in ARQ if F0['arquivos'].get(p) != F['arquivos'][p]]
novos = {d: sorted(set(F['pastas'][d]) - set(F0['pastas'].get(d, []))) for d in PASTAS}
novos = {d: v for d, v in novos.items() if v}
print('arquivos reais conferidos: %d; mudaram: %s' % (len(ARQ), mud or 'nenhum'))
print('arquivos novos nas pastas reais desde a foto: %s' % (novos or 'nenhum'))
print('arquivos com as marcas desta cadeia nas pastas reais: %s' % (marcadas or 'nenhum'))
sys.exit(0 if not mud and not marcadas else 1)
