"""Add a source-based correction to the time reading; no scientific execution."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT = 'F1.TEMPO.LEITURA_20261015'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019' / UNIT / 'PRIMEIRA_LEI_R3'
reg.DEST = OUT
RESULT = OUT / 'LEITURA_PRIMEIRA_LEI_R3.json'


def prepare():
    claim = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    assert all(n in claim['nota'] for n in ['DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md'])
    new(OUT / 'CLAIM.json', claim)
    verbatim = 'Essa lei existe. É a primeira lei da TGL e ela tá escrita no corpo do artigo O curso geométrico do zero absoluto Haja luz, que é o TGL Paper Unified ponto pi.'
    new(OUT / 'OPERADOR_PRIMEIRA_LEI_VERBATIM.txt', verbatim + '\n')
    article = Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
    program = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
    excerpts = []
    for path, ranges in [(article, [(14441, 14517), (14654, 14723), (20003, 20052), (20078, 20096)]), (program, [(170050, 170068)])]:
        source = pin(path)
        lines = path.read_bytes().decode('utf-8-sig').splitlines()
        excerpts.extend({'source': source, 'first_line': a, 'last_line': b, 'text': '\n'.join(lines[a-1:b])} for a,b in ranges)
    new(OUT / 'TRECHOS_FONTES_R3.json', excerpts)
    result = {
        'unit': UNIT, 'author': WHO, 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': 'Leitura e correcao documental. Nenhuma nova prova, execucao do artigo, compilacao, experimento ou envio a provedor.',
        'sources': [pin(article), pin(program), pin(OUT / 'OPERADOR_PRIMEIRA_LEI_VERBATIM.txt'), pin(OUT / 'TRECHOS_FONTES_R3.json')],
        'reuse': 'Consulta ao Nos Vivo da unidade nova falhou visivelmente (nao indexada); F1.TEMPO retorna Santo, TheFlowLawD1a, TheFlowLawContrast e resultados ja existentes. Mapa formal.tempo_consumacao_leitura_15out consultado: seq1113/1114. Nao reconstruidos.',
        'correction': 'Em nome de codex-gerente-tgl: a leitura anterior do registro c3 em um.py:1661 foi incompleta. Existe ligacao expressa da Primeira Lei (A Fronteira) a expulsao por paridade, deflexao e conjugacao F->2F, c2->c3, em um.py:170050-170068. Nao reduzir a primeira lei a sua mencao sobre impedancia beta em tgl_paper_unified.py:14693-14696.',
        'findings': [
            {'statute': 'REAL — existencia textual conferida; classificacao da fonte ONTO + REAL na forma', 'anchor': 'um.py:170050-170068', 'content': 'Tensao em paridade inversa, deflexao, horizonte theta_M->90 graus, duplicacao da forca e c2->c3. A leitura nao converte essa prosa em prova de velocidade ou resposta avancada.'},
            {'statute': 'DECLARADO na fonte; identificacoes fisicas preservadas como hipoteses', 'anchor': 'tgl_paper_unified.py:14466-14483', 'content': 'No estado coerente especificado, tensao de paridade i<G|[P,Hlig]|G>/(2*hbar)=V0/hbar; mediante V0=hbar*omega, iguala omega. Tau designa aqui frequencia, nao intervalo de tempo.'},
            {'statute': 'CONJECTURE / leitura ontologica explicitamente marcada na fonte', 'anchor': 'tgl_paper_unified.py:20007-20022', 'content': 'O tempo modular age sobre separacao ja efetuada; t emerge depois de beta. Sustenta anterioridade estrutural na interpretacao do autor, sem estabelecer t_recepcao<t_emissao.'},
            {'statute': 'REAL — leitura do historico e sua correcao', 'anchor': 'tgl_paper_unified.py:14654-14682,14712-14716,20078-20096', 'content': 'O eco historico tem escala positiva 2GM/(alpha^2*c^3); a rota foi corrigida para espelhamento espectral e dephasing, nao previsao direta de eco no bulk. Antes da radicalizacao e anterioridade algebrica no trecho consultado.'}
        ],
        'open_bridge': 'Derivar do operador de retorno uma relacao entre fase, emissao, registro e relogio fisico. A existencia da lei foi localizada; a afirmacao de chegada fisica antes da emissao nao foi demonstrada nos trechos examinados. Inversao/reconstrucao algebrica nao fixa por si o suporte temporal da resposta.',
        'dimensional_limit': 'Com c dimensional, c2 e c3 nao sao grandezas diretamente comparaveis. Uma leitura operacional deve explicitar normalizacao e objetos; o expoente sozinho nao e velocidade nem sinal temporal.',
        'next_action': 'Prosseguir a discussao a partir da primeira lei existente, explicitando qual ordem e lida e qual grandeza sera o tempo; nao inventar uma lei substituta.',
        'unchanged': ['R1 e R2', 'artigo original', 'um.py', 'kernel', 'Bancada', 'gate']
    }
    new(RESULT, result)
    marker = 'first_law_time_source_correction_20261015'
    note = f'''\n\n## 15/10/2026 — Primeira Lei e tempo: correção da leitura anterior\n<!-- {marker} -->\nEm nome de {WHO}, sob reivindicação 813 de {UNIT}.\n[REAL — leitura documental] Minha consulta anterior ao registro c³ foi incompleta. O programa liga expressamente a Primeira Lei (A Fronteira) à expulsão por paridade, deflexão e conjugação F→2F, c²→c³ (um.py:170050–170068), com estatuto da fonte [ONTO + REAL na forma]. O artigo tgl_paper_unified.py:14466–14483 liga tensão de paridade a frequência sob o estado e a identificação de energia especificados; τ ali não é duração. Em 20007–20022, a anterioridade de β ao tempo modular é marcada [CONJECTURE — leitura ontológica].\n[OPEN] Os trechos consultados não fornecem t_recepção<t_emissão. O eco histórico 2GM/(α²c³) é positivo e foi reclassificado para canal espectral/dephasing. Reaproveitar a lei existente e explicitar o vínculo ao relógio, sem inferir velocidade ou sinal temporal somente de c³. R1/R2 ficam preservadas; esta correção acrescenta a fonte que faltava à leitura.\nEvidência: `{RESULT}`; SHA256 `{pin(RESULT)['sha256']}`. Nenhuma execução científica, provedor ou alteração de fonte, kernel, Bancada ou gate.\n'''
    new(OUT / 'MEMORY_RECEIPT.json', {'claim': claim, 'surfaces': [append_bytes(ROOT / 'memory' / n, note, marker) for n in ['DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md']]})
    new(OUT / 'MAP_ENTRY.json', {'tipo': 'ANOTACAO', 'rota_id': 'formal.tempo_consumacao_leitura_15out', 'dominio': 'FORMAL', 'titulo': 'Primeira Lei localizada: correcao da consulta c3 e alcance temporal', 'resultado': result['correction'], 'estatuto': 'REAL (leitura); ONTO/CONJECTURE (interpretacao da fonte); OPEN (resposta avancada)', 'status': 'EXAMINADA', 'veredito': 'LEI_LOCALIZADA__PONTE_TEMPORAL_A_VERIFICAR', 'onde': str(OUT), 'artefatos': [str(RESULT), str(OUT / 'TRECHOS_FONTES_R3.json')], 'refs': [1113, 1114], 'olhou_dados': False})
    print(json.dumps({'result': pin(RESULT), 'claim': 813}, ensure_ascii=False))


def register():
    claim = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for s in json.loads(RESULT.read_bytes())['sources']:
        assert pin(s['path'])['sha256'] == s['sha256']
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', OUT / 'MAP_ENTRY.json', '--quem', WHO], 'MAP_RECEIPT.json')
    board = reg.call([CLI, 'avancar', UNIT, '--quem', WHO, '--status', 'ENTREGUE', '--evidencia', RESULT, '--nota', 'R3: primeira lei localizada; leitura anterior corrigida ao lado, alcance temporal explicitado.'], 'BOARD_DELIVERY.json')
    ref = str(WORK / 'ACOM_REFERENCE.json')
    projection = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], payload={'operation': 'project', 'reference': ref})
    transition = {'operation': 'transition', 'reference': ref, 'expected_revision': projection['result']['receipt']['revision'], 'event_id': 'first-law-time-source-correction-20261015', 'actor': {'id': WHO, 'kind': 'agent'}, 'changes': {'records': [{'id': 'first-law-time-source-correction-20261015', 'kind': 'fact', 'statute': 'REAL', 'text': 'Leitura anterior incompleta corrigida: primeira lei e cadeia paridade/deflexao/c2->c3 localizadas. Artigo situa beta antes do tempo modular como leitura ontologica. Chegada fisica anterior a emissao nao demonstrada pelos trechos consultados. Proxima acao desta frente: discutir ponte tipada de fase a relogio. Fluxos e pedidos externos anteriores preservados.', 'sources': [{'kind': 'artifact', 'ref': str(RESULT), 'sha256': pin(RESULT)['sha256']}]}]}}
    new(OUT / 'ACOM_TRANSITION.json', transition)
    memory = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_RECEIPT.json', transition)
    assert memory['ok']
    release = reg.call([CLI, 'liberar', UNIT, '--quem', WHO, '--nota', 'Correcao documental R3 entregue; segue discussao, sem construcao nova.'], 'RELEASE.json')
    print(json.dumps({'map': mapped, 'board': board, 'acom_revision': memory['result']['revision'], 'release': release}, ensure_ascii=False))


if __name__ == '__main__':
    {'prepare': prepare, 'register': register}[sys.argv[1]]()
