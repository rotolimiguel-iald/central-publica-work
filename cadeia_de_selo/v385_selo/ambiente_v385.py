# -*- coding: utf-8 -*-
"""O AMBIENTE da cadeia pos-rito v385 (comum a todos os scripts): onde esta o Nos, o pacote, as superficies e as ferramentas.
Regra fail-closed: as variaveis de ENSAIO (V385_CONF_DIR, V385_HORARIOS, V385_PIDF, V385_ESPERA_SEM_VIGIA, V385_UMEM, V385_ATLAS_DIR, V385_TOOLS,
V385_SAIDAS) so valem com um Nos SINTETICO (V385_NOS apontando para uma pasta com a marca SINTETICO_ENSAIO_V385.txt). Com o Nos REAL, qualquer uma
delas setada e' RECUSA (nada roda). E o Nos REAL com a marca SINTETICO tambem e' recusa: o sintetico nunca se confunde com o real.
V385_REMAP_DIR / V385_WRITE_ROOT (copias das superficies, o ensaio dentro da cadeia) valem sempre: so redirecionam ESCRITAS para uma pasta de copias."""
import os

SP = r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad'
SEL = os.path.join(SP, 'v385_selo')
PK = os.path.join(SP, 'v385')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
UMEM_REAL = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory'
ATLAS_DIR_REAL = r'C:\IALD\Central de Patentes\memory'
TOOLS_REAL = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'
PRDIR = r'C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out'
PR_JSON = os.path.join(PRDIR, 'PREREGISTRO_PILAR_QUANTICO_20261003_V1.json')
PR_MD = os.path.join(PRDIR, 'PREREGISTRO_PILAR_QUANTICO_20261003_V1.md')
# v385: o pacote da v384 (a fumaca, a conferencia do congelamento e as afericoes do pilar, que a v385 herda: o trabalhador e o V1 sao os mesmos) e o
# transcrito desta sessao (as palavras do operador de 05/10 sao LIDAS dele por script, nunca digitadas)
PK384 = os.path.join(SP, 'v384')
TRANSCRITO = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl'
MARCA_SINT = 'SINTETICO_ENSAIO_V385.txt'
VARS_DE_ENSAIO = ('V385_CONF_DIR', 'V385_HORARIOS', 'V385_PIDF', 'V385_ESPERA_SEM_VIGIA', 'V385_UMEM', 'V385_ATLAS_DIR', 'V385_TOOLS', 'V385_SAIDAS', 'V385_ARQ_DEST')


def _mesmo(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def ambiente():
    """Devolve um dicionario com os caminhos efetivos e a marca 'sint' (True so com o Nos sintetico). Recusa (SystemExit 2) o que for ambiguo."""
    nos = os.environ.get('V385_NOS') or NOS_REAL
    sint = os.path.exists(os.path.join(nos, MARCA_SINT))
    if _mesmo(nos, NOS_REAL) and sint:
        raise SystemExit('RECUSO: o Nos REAL carrega a marca %s -- o sintetico nunca se confunde com o real' % MARCA_SINT)
    if os.environ.get('V385_NOS') and not _mesmo(nos, NOS_REAL) and not sint:
        raise SystemExit('RECUSO: V385_NOS aponta para uma pasta sem a marca %s (%s)' % (MARCA_SINT, nos))
    if not sint:
        ruins = [k for k in VARS_DE_ENSAIO if os.environ.get(k)]
        if ruins:
            raise SystemExit('RECUSO: variaveis de ENSAIO %s setadas com o Nos REAL -- nada roda' % ruins)
    g = (lambda k, d: os.environ.get(k) or d) if sint else (lambda k, d: d)
    return {'sint': sint, 'nos': nos, 'pk': PK, 'sel': SEL,
            'umem': g('V385_UMEM', UMEM_REAL), 'atlas_dir': g('V385_ATLAS_DIR', ATLAS_DIR_REAL),
            'tools': g('V385_TOOLS', os.path.join(SEL, 'ensaio_tools')) if sint else TOOLS_REAL,   # com o Nos sintetico, NUNCA as ferramentas reais
            'conf_dir': g('V385_CONF_DIR', os.path.join(SEL, 'conferidor')), 'horarios': g('V385_HORARIOS', os.path.join(PK, 'rito_horarios_v385.txt')),
            'pidf': g('V385_PIDF', os.path.join(PK, '.rito_v385.pid')), 'sem_vigia': bool(sint and os.environ.get('V385_ESPERA_SEM_VIGIA') == '1'),
            'saidas': g('V385_SAIDAS', os.path.join(SEL, 'ensaio_saidas')) if sint else SEL,
            'arq_dest': g('V385_ARQ_DEST', os.path.join(SEL, 'ensaio_arquivo')) if sint else TOOLS_REAL,   # com o Nos sintetico, NUNCA o arquivo real
            'remap': os.environ.get('V385_REMAP_DIR'), 'write_root': os.environ.get('V385_WRITE_ROOT')}


def pode_escrever(p, amb):
    """A guarda de TODA escrita da cadeia: com o Nos SINTETICO, so dentro de v385_selo; com V385_WRITE_ROOT, so dentro dela. Falha = AssertionError (nada escrito)."""
    rp = os.path.realpath(p).lower()
    if amb['sint']:
        assert rp.startswith(os.path.realpath(SEL).lower() + os.sep), 'ENSAIO: escrita fora de v385_selo recusada: %s' % p
    if amb['write_root']:
        assert rp.startswith(os.path.realpath(amb['write_root']).lower() + os.sep), 'ESCRITA FORA DA RAIZ PERMITIDA: %s' % p
    return p
