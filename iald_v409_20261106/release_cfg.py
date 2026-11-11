"""Parametros da release do app. FONTE UNICA: app/RELEASE.json.

Somente leitura: sem rede, sem escrita, sem processo. Os scripts do pipeline v398 nao carregam
literais de versao; derivam tudo daqui. Hash nunca digitado: o pino do um.py e o campo
sha256.um.py do selo (conferido aqui contra a copia imutavel do cofre).
"""
from pathlib import Path
from types import SimpleNamespace
import json, re

W = Path(__file__).resolve().parent
A = W / 'app'
RELEASE_FILE = A / 'RELEASE.json'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
NOS = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
VAULT_ROOT = Path(r'C:\IALD\Central de Patentes\vault\originals_copy')
# Base historica (imutavel) do ajuste compacto; a v395 reutilizou a mesma.
FIT_BASELINE = Path(r'C:\IALD\Central de Patentes\work\iald_v394_20261019\app\science\memory_build\baseline_v368')
# Rotulos LOCAIS de ator (nao sao autenticacao). claim e check usam o MESMO id; o revisor e
# sempre OUTRO e e informado na hora da revisao (nunca fixado aqui).
OWNER = 'codex-app-01a094df'
BUILDER = 'codex-app-v409-builder'
KEYS = ('release', 'espelho_commit', 'um_py_sha256')


def load(require_commit=False):
    d = json.loads(RELEASE_FILE.read_bytes())
    if not isinstance(d, dict) or set(d) != set(KEYS):
        raise SystemExit('RELEASE.json: as chaves devem ser exatamente ' + str(KEYS))
    rel, commit, pin = d['release'], d['espelho_commit'], d['um_py_sha256']
    if not (isinstance(rel, str) and re.fullmatch(r'v[0-9]+', rel)):
        raise SystemExit('RELEASE.json: release invalida (esperado vNNN)')
    if commit is None:
        if require_commit:
            raise SystemExit(
                'PARADA (fail-closed): RELEASE.json tem espelho_commit = null. A gerencia deve gravar o '
                'hash de 40 hex do commit da ' + rel + ' ja publicado no espelho the_boundary antes de '
                'prepare/finalize/count/validate. Nada foi lido do git, nada foi escrito.')
    elif not (isinstance(commit, str) and re.fullmatch(r'[0-9a-f]{40}', commit)):
        raise SystemExit('RELEASE.json: espelho_commit deve ser null ou 40 hex minusculos')
    if not (isinstance(pin, str) and re.fullmatch(r'[0-9a-f]{64}', pin)):
        raise SystemExit('RELEASE.json: um_py_sha256 invalido')
    vault = VAULT_ROOT / ('um_unificado_' + rel)
    seal = json.loads((vault / 'um_absoluto_selo.json').read_bytes())
    if seal['um_version'] != rel or seal['sha256']['um.py'] != pin:
        raise SystemExit('RELEASE.json diverge do selo da copia imutavel do cofre (versao ou pino do um.py)')
    suffix = W.name.split('_', 2)[-1]
    date_pt = suffix[6:8] + '/' + suffix[4:6] + '/' + suffix[0:4] if re.match(r'[0-9]{8}', suffix) else ''
    return SimpleNamespace(
        release=rel, number=int(rel[1:]), espelho_commit=commit, um_py_sha256=pin, vault=vault,
        unit='F9.APP_' + rel.upper() + '_' + suffix.upper(), date_pt=date_pt, owner=OWNER, builder=BUILDER,
        target_name=(rel + '_' + commit[:12]) if commit else None)


# Corte previsto (decidir ANTES do finalize; depois os arquivos sao imutaveis). Ex.: ('_v397', '_v398')
# reduz a expansao do haiku55 (estimativa em PLANO_FASE_B.md). None = regra padrao abaixo.
# 02/11/2026 (v405): a redesenhada da base compacta entrou em app/build/haiku_codec.py (catalogo de indicadores TRUE e declaration_sources por ponteiro); volta a regra padrao: None.
EXPAND_OVERRIDE = None  # antes (registro) 29/10/2026: politica D (decisao da gerencia a7): nenhum sufixo expandido no haiku55 -- A/B/C estouram a folga; os topicos _v404 entram compactos com ponteiro @, 0 perdidos, 0 estatuto trocado; redesenhar a politica antes da v406 (a base compacta cresce ~63 KB a cada 2 versoes)
# 29/10/2026: janela P2 do shared/sonnet_public DESACOPLADA do EXPAND_OVERRIDE do haiku55 (decisao da gerencia a7, opcao C do achado F2 do revisor): a politica D vale so para o haiku55.
# Valor: variante F, decisao da gerencia a7, 29/10 -- a janela da instalada v402 (_v401,_v402) mais os novos (_v403,_v404), para os 19 topicos (11 novos + 8 anteriores) manterem limites/diz/nao_diz inline no shared e no sonnet_public. None = segue expand_suffixes() (comportamento anterior, usado pela prepare.py).
# 02/11/2026 (v405): a mesma janela P2 mais os topicos novos _v405; nenhum topico sai dela (sem regressao de literais no shared/sonnet_public).
# 03/11/2026 (v406, decisao da gerencia c1, ORDEM_004): a janela DESLIZA. Sai _v401 (o mais antigo); entram os novos _v406. _v402 so' sai se o shared nao couber na menor folga medida
# (DeepSeek, reserva declarada 148656). Os topicos que SAEM da janela viram capsula compacta, mas MANTEM os literais limites/diz/nao_diz (a recusa F2 da v404 foi pela perda deles):
# P2_RETIRED_LITERAL_SUFFIXES e' lido por prepare.py e aplicado em fit_memory.compact.
# 04/11/2026 (v407, ORDEM_006 e LICOES_v406): a janela DESLIZA de novo. Sai _v402 (a folga minima declarada da v406 foi 41975 B e uma release de ~30 KB consome tres quartos dela); entram os novos _v407.
# _v403 so' sai se o shared nao couber na menor folga medida com a reserva declarada (decidir ANTES do finalize). Os topicos que saem mantem limites/diz/nao_diz literais na capsula compacta.
# D53, ORDEM_007. The full resident window is independent of historical retrieval.
SHARED_P2_SUFFIXES = ('_v408', '_v409')
P2_RETIRED_LITERAL_SUFFIXES = ('_v401', '_v402')


def expand_suffixes(installed, current):
    """Topicos '_vNNN' das releases desde a INSTALADA ate a corrente entram expandidos no haiku55.
    Generaliza a regra da v395 (instalada v394, corrente v395 -> ('_v394', '_v395'))."""
    if EXPAND_OVERRIDE is not None:
        return tuple(EXPAND_OVERRIDE)
    a, b = int(installed[1:]), int(current[1:])
    if not 0 < a <= b:
        raise SystemExit('release instalada inconsistente com a corrente')
    return tuple('_v%d' % n for n in range(a, b + 1))
