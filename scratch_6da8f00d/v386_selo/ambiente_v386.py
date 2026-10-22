# -*- coding: utf-8 -*-
"""O AMBIENTE da cadeia pos-rito v386 (comum a todos os scripts; molde: ambiente_v385.py): onde esta o Nos, o pacote, os dados da v386, as superficies
e as ferramentas.
Regra fail-closed: as variaveis de ENSAIO (V386_CONF_DIR, V386_HORARIOS, V386_PIDF, V386_ESPERA_SEM_VIGIA, V386_ESPERA_LANCADOR_FINGE, V386_UMEM,
V386_ATLAS_DIR, V386_TOOLS, V386_SAIDAS, V386_ARQ_DEST, V386_HAJA_LUZ) so valem com um Nos SINTETICO (V386_NOS apontando para uma pasta com a marca
SINTETICO_ENSAIO_V386.txt). Com o Nos REAL, qualquer uma delas setada e' RECUSA (nada roda). E o Nos REAL com a marca SINTETICO tambem e' recusa.
V386_REMAP_DIR / V386_WRITE_ROOT (copias das superficies, o ensaio dentro da cadeia) valem sempre: so redirecionam ESCRITAS para uma pasta de copias.
v386: a superficie NOVA da linhagem e' C:\\IALD\\Artigo\\Haja_Luz\\CLAUDE.md (decisao do operador de 05/10, item 16 da delegacao) -- entra em 'haja_luz'."""
import os

SP = r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad'
SEL = os.path.join(SP, 'v386_selo')
PK = os.path.join(SP, 'v386', 'pacote')          # o pacote v386 (candidato, esperados, conferidor, rito, runtime, pinos)
DAT = os.path.join(SP, 'v386')                   # os dados da v386 (os verbatins do operador, o ramo B, o kernel do sandbox, as afericoes)
PK385 = os.path.join(SP, 'v385'); SEL385 = os.path.join(SP, 'v385_selo')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
UMEM_REAL = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory'
ATLAS_DIR_REAL = r'C:\IALD\Central de Patentes\memory'
TOOLS_REAL = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'
HAJA_LUZ_REAL = r'C:\IALD\Artigo\Haja_Luz\CLAUDE.md'
PRDIR_B = r'C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out'        # o V1 do ramo B (so leitura)
PRDIR_PILAR = r'C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out'
PRDIR_DOIS_LADOS = r'C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out'
TRANSCRITO = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl'
# os quatro arquivos do operador de 05/10 (lidos por sha256: os hashes vem do CANDIDATO_v386.json, nunca daqui)
OP_FILES = {'verbo_20261005_1653': os.path.join(DAT, 'VERBO_operador_05out.txt'),
            'ramo_b_decision_20261005_1711': os.path.join(DAT, 'ramo_b', 'DECISAO_OPERADOR_RAMO_B_05out.json'),
            'respostas_20261005_1829': os.path.join(DAT, 'RESPOSTAS_operador_05out.txt'),
            'respostas_json_20261005_1829': os.path.join(DAT, 'RESPOSTAS_operador_05out.json')}
MARCA_SINT = 'SINTETICO_ENSAIO_V386.txt'
VARS_DE_ENSAIO = ('V386_CONF_DIR', 'V386_HORARIOS', 'V386_PIDF', 'V386_ESPERA_SEM_VIGIA', 'V386_ESPERA_LANCADOR_FINGE', 'V386_UMEM', 'V386_ATLAS_DIR',
                  'V386_TOOLS', 'V386_SAIDAS', 'V386_ARQ_DEST', 'V386_HAJA_LUZ')


def _mesmo(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def ambiente():
    """Devolve um dicionario com os caminhos efetivos e a marca 'sint' (True so com o Nos sintetico). Recusa (SystemExit 2) o que for ambiguo."""
    nos = os.environ.get('V386_NOS') or NOS_REAL
    sint = os.path.exists(os.path.join(nos, MARCA_SINT))
    if _mesmo(nos, NOS_REAL) and sint:
        raise SystemExit('RECUSO: o Nos REAL carrega a marca %s -- o sintetico nunca se confunde com o real' % MARCA_SINT)
    if os.environ.get('V386_NOS') and not _mesmo(nos, NOS_REAL) and not sint:
        raise SystemExit('RECUSO: V386_NOS aponta para uma pasta sem a marca %s (%s)' % (MARCA_SINT, nos))
    if not sint:
        ruins = [k for k in VARS_DE_ENSAIO if os.environ.get(k)]
        if ruins:
            raise SystemExit('RECUSO: variaveis de ENSAIO %s setadas com o Nos REAL -- nada roda' % ruins)
    g = (lambda k, d: os.environ.get(k) or d) if sint else (lambda k, d: d)
    return {'sint': sint, 'nos': nos, 'pk': PK, 'dat': DAT, 'sel': SEL,
            'umem': g('V386_UMEM', UMEM_REAL), 'atlas_dir': g('V386_ATLAS_DIR', ATLAS_DIR_REAL), 'haja_luz': g('V386_HAJA_LUZ', HAJA_LUZ_REAL),
            'tools': g('V386_TOOLS', os.path.join(SEL, 'ensaio_tools')) if sint else TOOLS_REAL,   # com o Nos sintetico, NUNCA as ferramentas reais
            'conf_dir': g('V386_CONF_DIR', os.path.join(SEL, 'conferidor')), 'horarios': g('V386_HORARIOS', os.path.join(PK, 'rito_horarios_v386.txt')),
            'pidf': g('V386_PIDF', os.path.join(PK, '.rito_v386.pid')), 'sem_vigia': bool(sint and os.environ.get('V386_ESPERA_SEM_VIGIA') == '1'),
            'lancador_finge': (os.environ.get('V386_ESPERA_LANCADOR_FINGE') if sint else None),
            'saidas': g('V386_SAIDAS', os.path.join(SEL, 'ensaio_saidas')) if sint else SEL,
            'arq_dest': g('V386_ARQ_DEST', os.path.join(SEL, 'ensaio_arquivo')) if sint else TOOLS_REAL,   # com o Nos sintetico, NUNCA o arquivo real
            'remap': os.environ.get('V386_REMAP_DIR'), 'write_root': os.environ.get('V386_WRITE_ROOT')}


def pode_escrever(p, amb):
    """A guarda de TODA escrita da cadeia: com o Nos SINTETICO, so dentro de v386_selo; com V386_WRITE_ROOT, so dentro dela. Falha = AssertionError (nada escrito)."""
    rp = os.path.realpath(p).lower()
    if amb['sint']:
        assert rp.startswith(os.path.realpath(SEL).lower() + os.sep), 'ENSAIO: escrita fora de v386_selo recusada: %s' % p
    if amb['write_root']:
        assert rp.startswith(os.path.realpath(amb['write_root']).lower() + os.sep), 'ESCRITA FORA DA RAIZ PERMITIDA: %s' % p
    return p
