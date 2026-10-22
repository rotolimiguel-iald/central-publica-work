# -*- coding: utf-8 -*-
"""R2.2: registro_mapa_F9.MEMORIA_ACOM_R2_2.json (só campos do `rotas.py modelo`; artefatos existentes conferidos).
Não registra no mapa: a gerência registra."""
import json
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
arts = ['RESULTADO_R2_2.md', 'TESTES_R2_2.md', 'RUNBOOK_OPERADOR.md', 'CANDIDATO_MANIFESTO_R2_2.json', 'DIFF_R2_1_R2_2.patch',
        'DIFF_R2_1_R2_2_APPLY_CHECK.json', 'implantar.py', 'reverter.py', 'implantacao_lib.py',
        'implantar_config_producao_r2_2.json', 'MANIFESTO_R2_2.json', 'copia/testes_r2/RESULTADOS_TESTES.json',
        'copia_r2_1/testes_r2/RESULTADOS_TESTES_parcial.json', 'runs/s5_ensaio_r2_2.json',
        'runs/s5_ensaio_r2_2_rodada1_bug_P8b.json', 'runs/s6_guarda_resumo.json', 'src_r2_2/test_r2_2.py',
        'src_r2_2/test_app_r2_2.py']
artefatos = []
for a in arts:
    p = R22 / a
    assert p.exists(), p
    artefatos.append(str(p))
reg = {
    'tipo': 'RESULTADO',
    'rota_id': 'programa.memoria_acom.conserto_delta_12out',
    'dominio': 'INFRA',
    'titulo': 'R2.2 do conserto ACOM: K4c, K4b, K3r no reverter, P8b (lento x laco de queda), N1 por componentes, N3 pela via do app, manifesto; runbook do operador',
    'pergunta': 'Os achados da revisao independente da R2.1 (K4c, K4b, K3r, P8b, N1 por componentes, N3 via app, campo ferramentas) ficam corrigidos sem quebrar as 259 da suite, e o ensaio K1-K6/K2b-K6c/P8/P8b fecha?',
    'dados': ['candidato_r2_1 e ferramentas R2.1 (manifesto f7ccb802d2388ac3; implantar b913952cb2592b84; reverter b6e3906baa88a7e5; lib c72ddd0a5686a4e0), conferidos por script',
              'REVISAO_R2_1.md 8d113857fd263bb0 e os scripts do revisor (s4_ataques, s5_ensaio_rev)',
              'somente sintetico: banco v1 por store_v1_frozen, psion e hardlinks sinteticos, backend de processos simulado'],
    'metodo': 'Consertos no candidato (guard.py, session_memory.py comentario, iald_web_server.py por script com ancora exata, chave nunca impressa) e nas ferramentas; 19 testes novos rodados na copia R2.1 (devem falhar) e na copia R2.2 (devem passar), N3 pelo handler real do app extraido por AST; suite inteira da R2.2 sob a guarda; ensaio com os 21 cenarios do construtor R2.1 e do revisor R2.1, ferramentas R2.2; patch R2.1->R2.2 provado por git apply (autocrlf=false). Nada em producao.',
    'resultado': 'Suite R2.2 278/278 PASSA (259 + 19), 3 bloqueios BLOCK_NETWORK IPv6. Testes novos na R2.1: 15 falham, 4 controles passam; na R2.2 19/19. N1: 16.000 componentes 2,8-3,7 s -> < 50 ms com recusa path_too_many_components (path_reason, read_allowed_file, dispatch init, agi_validate_path); 40.000 caracteres: R2.1 ValueError, R2.2 path_too_long. N3 via app (handler real, hardlink 12 s): canario lido R2.1 294, R2.2 0 (2.059 recusas). Ensaio 2a rodada: K4c 1o reverter FALHOU_EM_reiniciar_app rc 1 sem religar e trava pendente, 2o REVERTIDA; K4b acao preenchida; K3r FALHOU_EM_parar_app, tarefa reabilitada, estado lido, sem fica parado; P8 rc 3 LENTO sem mandar reverter; P8b rc 3 LACO com como distinguir; CFG ok; originais identicos e banco = original em todos menos K2b/c/d (recibo mexido pelo operador, como na R2.1). 1a rodada do ensaio achou defeito da propria R2.2 (P8b filho nunca de pe: UnboundLocalError, rc 1), corrigido com teste. Patch 991fe46e8dffe6bd reproduz 18 arquivos byte a byte.',
    'veredito': 'R2_2__K4C_K4B_K3R_P8B_N1_N3APP_MANIFESTO_CORRIGIDOS_NAS_COPIAS__278_DE_278__19_NOVOS_15_FALHAM_NA_R2_1__ENSAIO_21_CENARIOS__RUNBOOK_DO_OPERADOR__NADA_EM_PRODUCAO__IMPLANTACAO_E_ATO_DO_OPERADOR',
    'estatuto': 'REAL',
    'status': 'EXAMINADA_COM_DEFEITO',
    'olhou_dados': False,
    'defeito': 'Restam: classe conteudo do N2 (*.env.txt, ADS) aberta em D4; N3 por renomeio (equivale a copia); cmdlets reais do Agendador nunca exercitados; recuperacao automatica perdida se o operador renomear/apagar recibo (K2b/K2c); amostragem P8b em producao nao medida (PowerShell 1-2 s por amostra); escala dos instantaneos (D1-B) inalterada; instabilidade do simulador vista 1 vez no parar_app do implantar (nao repetiu em 3 rodadas). A R2.2 nao foi revista por terceiro.',
    'nao_refazer': 'Nao refazer: a suite inteira e os 19 testes antes/depois, o ensaio de 21 cenarios, a medida N1 por componentes e o N3 pelo handler real do app; ler 9_R2_2/RESULTADO_R2_2.md, TESTES_R2_2.md e runs/.',
    'proximo_passo': 'Revisao independente curta da R2.2 (gerencia); depois o operador segue o RUNBOOK_OPERADOR.md (dry-run DRY_RUN_OK, implantar --pular-mover-backups CONCLUIDA, conferencias, 7_VERIFICACAO com janela > 30 min e llama online, mover backups).',
    'onde': str(R22 / 'RESULTADO_R2_2.md'),
    'artefatos': artefatos,
    'refs': ['infra.memoria_acom.core_20261010', 'infra.memoria_acom.integracao_20261010', 'infra.memoria_acom.sessoes_20261010'],
    'nota': 'Construtor: subagente c1, 13/10/2026. Desvio deliberado: init/transition da memoria ACOM nao executados (escreveriam no banco de producao). O iald_web_server.py do candidato_r2_2 carrega a chave de producao (e o que se instala); nenhum outro arquivo de 9_R2_2 a contem (conferido por script); o patch nao a contem.',
}
(R22 / 'registro_mapa_F9.MEMORIA_ACOM_R2_2.json').write_text(json.dumps(reg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('ok', len(artefatos))
