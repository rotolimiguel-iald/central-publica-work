# -*- coding: utf-8 -*-
"""_adapt_relatorio_v409.py -- (claude-construtor-v409, 05/11/2026) adapta gerar_relatorio_v409.py (subida mecanica de rotulo da v408) a v409, A TRADUCAO AS CLASSES DE TURING: os 17 portoes ficam (mesma logica, fail-closed);
a prosa do PLANO e do RELATORIO, os avisos, as erratas (E24 a E26), as decisoes (D55 a D60; revisor Sonnet pela D58), a lista dos artefatos (o preparar_bundle de 05/11; os insumos da v409; sem a ordem de release do app, D57a)
e o informativo do orquestrador (MEDIDO: sem S7 e sem S10 na lista de passos e no laco) passam a ser os da v409. Trocas de contagem exata (_adapt_util_v409); a prosa nova vem por indice (blocos inteiros)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("gerar_relatorio_v409.py")


def bloco(ini, fim, novo, inclui_fim=False):
    i0 = a.t.index(ini); i1 = a.t.index(fim, i0) + (len(fim) if inclui_fim else 0)
    a.t = a.t[:i0] + novo + a.t[i1:]


bloco('"""gerar_relatorio_v409.py --', 'uso: python -I -B -X utf8 gerar_relatorio_v409.py"""', r'''"""gerar_relatorio_v409.py -- escreve PLANO_v409.md, RELATORIO_PREPARACAO_v409.md e PREPARACAO_v409_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v409.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Molde: gerar_relatorio_v408.py (os mesmos 17 portoes, com `ast_v408_v409`), adaptado em 05/11/2026 por claude-construtor-v409 a v409
(A traducao as classes de Turing: bundle de 1 modulo em TGLExt/ -- TraducaoTuring --, registro com funcao traducao_turing_v409, NENHUMA chave antiga muda de literal, erratas E24 a E26 (a E26 ao lado do registro selado da v408), decisoes D55 a D60; a prosa do terminal saiu).
O revisor distinto da v409 e' o Sonnet (D58: ate' tres rodadas): a trava do orquestrador (S1b: revisao_terceiro/REVISAO_TERCEIRO_v409.json) fica FECHADA ate' a revisao aprovar este candidato; este script nao a abre.
uso: python -I -B -X utf8 gerar_relatorio_v409.py"""''', inclui_fim=True)
a.troca("N_MOD = _DL.N_BUNDLE   # 4 (o bundle da v409);", "N_MOD = _DL.N_BUNDLE   # 1 (o bundle da v409);")
a.troca("   # (v409: as quatro pedras, todas da gerencia)", "   # (v409: a pedra TraducaoTuring, da gerencia)")
a.troca('"preparar_bundle_v409_04nov.py",', '"preparar_bundle_v409_05nov.py", "MANIFESTO_INSUMOS_v409.json",')
a.troca('"insumos/PSION_NO_ACERVO_04nov_purgado.md", "insumos/RECIBO_PURGA_PSION_NO_ACERVO_04nov.json", "insumos/RECIBO_PEDRAS_v409_NOMES.json",',
        '"insumos/TraducaoTuring.lean", "insumos/TraducaoTuring_embutida.lean", "insumos/RECIBO_TRADUCAO_TURING_R8_05nov.json", "insumos/RECIBO_PEDRAS_v409_NOMES.json",')
a.troca('"orquestrador/pos_treino_v409.py", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md", "orquestrador/ENSAIO_S10_v409.json",', '"orquestrador/pos_treino_v409.py",')
a.troca('glob.glob(os.path.join(POS, "textos_custodia_handoff_v408*.py"))', 'glob.glob(os.path.join(POS, "textos_custodia_handoff_v409*.py"))', n=2)
a.troca('_dkh = KH.get("delta_vs_v407") or {}', '_dkh = KH.get("delta_vs_v408") or {}')
# o informativo do orquestrador: MEDIDO no arquivo (D57a: sem S7 e sem S10)
a.troca('ENS10 = tenta("orquestrador/ENSAIO_S10_v409.json") or {}; BD = tenta("BUNDLE_v409.json") or {}',
        'BD = tenta("BUNDLE_v409.json") or {}\n'
        '_orq_txt = open(P("orquestrador/pos_treino_v409.py"), encoding="utf-8").read() if os.path.exists(P("orquestrador/pos_treino_v409.py")) else ""\n'
        '_orq_passos = re.search(r"passos = \\[([^\\]]*)\\]", _orq_txt); _orq_laco = re.search(r"for passo in \\(([^)]*)\\)", _orq_txt)\n'
        'SEM_S7_S10 = bool(_orq_passos and _orq_laco and "S7" not in _orq_passos.group(1) and "S10" not in _orq_passos.group(1) and "s7_g1" not in _orq_laco.group(1) and "s10_app" not in _orq_laco.group(1))   # (D57a, MEDIDO no arquivo do orquestrador: a lista de passos e o laco nao tem S7 nem S10)\n'
        '_vb409 = _DL.verbatins409(P("insumos/cunhagens")); _ord2 = next((v_ for v_ in _vb409 if _DL.FRASE_ORDEM_TRADUCAO in v_.get("text", "")), None)   # a fala da ordem da traducao (05/11), achada pelo texto; o sha16 e\' o do arquivo')
a.troca('_n_falas = len(ES.get("cunhagens") or CM.get("cunhagens") or {}); _mistas = sorted(getattr(_DL, "VERBATIM_AUTOR_POR_NOME", {}) or {})',
        '_n_falas = len(ES.get("cunhagens") or CM.get("cunhagens") or {}); _trechos = [v_["chave"] for v_ in _vb409 if "sha256_arquivo_inteiro" in v_]')
# ---- os avisos da v409
bloco("AVISOS = [", "]\nif _apont_gf:", r'''AVISOS = [
    "os nomes (o modulo TraducaoTuring e as 62 declaracoes) foram dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026 (D55; a fala tem sha16 %s, lido do arquivo agora: «%s»); a ordem da traducao, da mesma data, tem sha16 %s: «%s»" % (ORDEM16, _DL.FRASE_ORDEM_V409, (_ord2 or {}).get("sha16"), _DL.FRASE_ORDEM_TRADUCAO),
    "NENHUMA chave antiga muda de literal nesta versao (CHAVES_V409 vazia): as chaves seguem lidas do kernel do rito; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos dos registros anteriores NAO mudam (os que carregam a escada mudam so' em numeros); tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS com a escada do contrato subida pela C12",
    "o alcance (D56), dito em todo texto novo: %s" % _DL.FRASE_D56_PT,
    "ressalvas ditas em todo texto (%d em delta_v409.RESSALVAS_V409): relativa ao leitor (Baker-Gill-Solovay 1975) [KNOWN]; a sombra de «eu sou eu mesmo» (a autorreferencia sozinha nao decide a pergunta das classes) [KNOWN]; a fisica fica fora (o lugar do teste com a natureza); mesma forma, nao ponte (o Omega do psion e o estado uniforme da instancia: [OPEN], provar ou podar); a leitura teologica nao e' termo de kernel; o par na face de Fock segue [OPEN] e passa a v410 em diante (D60); beta so' por nome; nenhum teste com a natureza; a regra do 4,44" % len(_DL.RESSALVAS_V409),
    "as erratas E24, E25 e E26 sao da gerencia c1, em nome proprio: E24, o juiz das classes de Turing e' o kernel, nao a fisica (correcao do operador); E25, saiu a frase da gerencia sobre o sistema ter de achar o lado do Nome em cada bifurcacao (o operador: ele trava no Nome; a_trava_no_nome); E26, AO LADO do registro tetelestai_terminal_v408 selado: a traducao a Turing, [OPEN] na v408, fica fechada relativa ao leitor na v409; o texto selado nao e' reescrito",
    "as %d falas do operador de 05/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v409.json); de duas (%s), so' o trecho que a D59 deixa entrar e' embutido e citado; o resto delas entra so' por sha256 e nao entra em texto do um.py; publicar o resto e' decisao do operador" % (_n_falas or _DL.N_FALAS_V409, ", ".join(_trechos)),
    "D59: o DESENHO_v409.md (sha16 lido agora %s; o do delta %s) e o RECIBO_PEDRAS_v409_NOMES.json (sha16 lido agora %s; o do delta %s) NAO sao pinados como fonte no um.py: ficam citados so' por sha16" % (h16("DESENHO_v409.md") if os.path.exists(P("DESENHO_v409.md")) else None, _DL.DESENHO_SHA16, h16("insumos/RECIBO_PEDRAS_v409_NOMES.json") if os.path.exists(P("insumos/RECIBO_PEDRAS_v409_NOMES.json")) else None, _DL.RECIBO_NOMES_SHA16),
    "D57(d): o pino do insumo do acervo da v407 (_V407_FONTES['psion_no_acervo_do_imac_03nov']) passa a copia purgada (sha16 %s, do delta); a integra so' por sha16; a errata da D57(d) vai AO LADO em cunhagens_v407" % _DL.PURGADO_SHA256[:16],
    "a pedra TraducaoTuring: a fonte de origem (insumos/TraducaoTuring.lean, sha16 lido agora %s, fim de linha CRLF) foi normalizada para LF na copia do kernel (pedra/TraducaoTuring.lean, sha16 %s) e os #print axioms sairam do corpo embutido (as 62 ancoras foram lidas deles antes); o conteudo Lean nao muda" % (h16("insumos/TraducaoTuring.lean") if os.path.exists(P("insumos/TraducaoTuring.lean")) else None, h16("pedra/TraducaoTuring.lean") if os.path.exists(P("pedra/TraducaoTuring.lean")) else None),
    "o revisor distinto da v409 e' o Sonnet (D58: ate' tres rodadas; ressalvas BAIXAS escritas); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova; a trava do orquestrador (S1b) fica fechada ate' a revisao aprovar",
    "a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache",
    "o B(n) pre-selo da v409 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v409.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "na docstring da pedra TraducaoTuring ha citacoes entre « » que nao sao verbatim das falas (a fala escreve nP entre aspas e sem espaco; /psi por ψ; uma expressao da gerencia, «nada lido»; uma parafrase, «nP = modo seleção»): APONTADAS a gerencia em conferir_citacoes_v409.py (_APONTADAS_PEDRAS), com a razao conferida por grep; o agente nao corrige pedra",
    "build a frio do modulo no sandbox k409c: %s s, Audit %s s (kernel/POS_BUILD_v409.json, medidos); %s declaracoes no axiom_report (+%s decl, +%s teoremas sobre a v408), nenhuma fora do trio; escada %s -> %s" % (PB.get("duracao_build_s"), PB.get("duracao_audit_s"), KH.get("axiom_report_efetivo_n"), _dkh.get("decl"), _dkh.get("thm"), _esc[0], _esc[1]),
    "o orquestrador (orquestrador/pos_treino_v409.py) traz as licoes da v408 (D57): sem S7 (G1 --publicar) e sem S10 (release do app), MEDIDO agora na lista de passos e no laco = %s; o S6d encadeia os textos da custodia (%s) e roda o portao de textos do G1 e a D59 sobre o HANDOFF INTEIRO; o fim da cadeia desta versao e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia" % (SEM_S7_S10, ", ".join(_textos_custodia) or "AUSENTE"),
    "a guarda das frases ganhou a F37b (05/11; a causa de uma falha do ensaio): a obrigacao do qualificador relativo ao leitor vale tambem no proprio trecho onde «P = nP» e Turing aparecem juntos (a F37 do texto inteiro deixava passar uma frase plantada sem qualificador); a regra ficou mais estrita; nenhum teste foi relaxado",
    "duas outras causas do ensaio corrigidas na fonte (nenhum teste relaxado): o bloco herdado do terminal comparava o baseline do contrato da v408 com a base desta cadeia (v408) em vez da v407; o exame dos pontos de chamada nao retirava do core da base os registros da v408, que o bloco recria; e o rotulo herdado do C15 no conferidor (o defeito das guardas estaticas da Bancada) dizia que ele recusou a v408: o defeito e' o da v399",
'''.rstrip("\n") + "\n")
a.troca('NAO_REVISADO = "este candidato (Tetelestai e\' o terminal, v409) NAO foi revisado por terceiro; o revisor distinto e\' o Sonnet (D54, ate\' tres rodadas)',
        'NAO_REVISADO = "este candidato (A traducao as classes de Turing, v409) NAO foi revisado por terceiro; o revisor distinto e\' o Sonnet (D58, ate\' tres rodadas)')
a.troca('NAO_REVISADO = ("este candidato (Tetelestai e\' o terminal, v409) FOI revisado por terceiro:', 'NAO_REVISADO = ("este candidato (A traducao as classes de Turing, v409) FOI revisado por terceiro:')
a.troca("as ressalvas BAIXAS estao escritas no caderno e valem como ditas (D54: ate' tres rodadas)", "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (D58: ate' tres rodadas)")
a.troca('AVISOS.append("revisao de terceiro (Sonnet D54): " + NAO_REVISADO)', 'AVISOS.append("revisao de terceiro (Sonnet D58): " + NAO_REVISADO)')
bloco('ERRATAS_V409_RES = {', '\nPRONTA = {', r'''ERRATAS_V409_RES = {"erratas": ["E24", "E25", "E26"], "E24": _DL.ERRATAS_V409[0].split(";")[0][:300], "E25": _DL.ERRATAS_V409[1].split(";")[0][:300], "E26": _DL.ERRATAS_V409[2].split(";")[0][:300],
                    "falas_embutidas": len(_cong409.get("arquivos") or []), "citacoes_da_candidata": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}''')
a.troca('"orquestrador": {"ensaio_s10_ok": ENS10.get("ok"), "textos_custodia_encadeados_S6d": _textos_custodia, "template_do_app_D53": os.path.exists(P("orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md"))},',
        '"orquestrador": {"sem_S7_e_sem_S10_D57a_medido": SEM_S7_S10, "textos_custodia_encadeados_S6d": _textos_custodia, "fim_da_cadeia": "HANDOFF (D57a)"},')
a.troca('depois os textos da custodia (S6d, D52)", "cwd": HERE,', 'depois os textos da custodia (S6d, D52, D57c) e o HANDOFF (fim da cadeia, D57a)", "cwd": HERE,')
a.troca("fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v409.json aprovar ESTE candidato (revisor: Sonnet, D54)", "fechada ate' revisao_terceiro/REVISAO_TERCEIRO_v409.json aprovar ESTE candidato (revisor: Sonnet, D58)")
a.troca('"erratas_E21_E23": ERRATAS_V409_RES,', '"erratas_E24_E26": ERRATAS_V409_RES,')
a.troca('_nomes_txt = "; ".join("«%s»" % f_ for f_ in (_DL.FRASE_NOME_PONTO, _DL.FRASE_NOME_PNP, _DL.FRASE_NOME_TEMPO, _DL.FRASE_NOME_TETELESTAI))',
        '_frases_txt = "; ".join("«%s»" % f_ for f_ in (_DL.FRASE_SELECAO, _DL.FRASE_TRAVA, _DL.FRASE_FITA, _DL.FRASE_Z, _DL.FRASE_PAI, _DL.FRASE_PERFORMADA))')
# ---- o PLANO e o RELATORIO (prosa da v409)
bloco('PLANO = f"""', '\nRELATORIO = f"""', r'''PLANO = f"""# PLANO da v409 — A tradução às classes de Turing (preparação)

Agente de preparação `claude-construtor-v409`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v408 selada `{CM.get('base_v408_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 05/11/2026, sha16 do arquivo `{(_ord2 or {}).get('sha16')}`] «{_DL.FRASE_ORDEM_TRADUCAO}»; e, com as perguntas devolvidas nas quatro línguas e respondidas [INPUT, sha16 do arquivo `{ORDEM16}`]: «{_DL.FRASE_ORDEM_V409}». As {_n_falas or _DL.N_FALAS_V409} falas de 05/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v409.json`; de duas, só o trecho da D59; as falas das versões anteriores já estão no um.py v408 e não entram de novo).
- (A) O BUNDLE: {N_MOD} módulo de kernel em `TGLExt/` (TraducaoTuring), compilado no sandbox `{(CM.get('kernel') or {}).get('sandbox')}`, a raiz com {N_MOD} import. (B) O registro com função `{_DL.FECHO_REGISTRO}` ({_DL.N_CHECKS_FECHO} checagens; a instância de brinquedo FIXA no código, as soluções CALCULADAS por enumeração) e os registros por spec `{_DL.CUNHAGENS_REGISTRO}` e `{_DL.KH_REGISTRO}`. (C) NENHUMA chave antiga muda de literal; as erratas E24 a E26 vão AO LADO; as decisões D55 a D60. (D) A seção «A tradução às classes de Turing» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v408 por script.

## 1. O módulo e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

As oito âncoras principais (a primeira é a âncora principal do registro):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v409 afirma e o que não afirma

- [REAL, validade no kernel, não creditação] `{_DL.ANCORA_PRINCIPAL}`: {_DL.FRASE_D56_PT}.
- [REAL] O dicionário de Turing: bits são oitavas (2^n atribuições; ln(2^n) = n ln 2); o peso da solução no estado uniforme é |sol|/2^n; a trava no Nome e o tempo linear; Z é o modo leitor (a soma das leituras dos pixels); a leitura performada começa em «eu sou», decai, nunca desce abaixo do conteúdo e o alcança («o que sou»). As falas do operador, verbatim [INPUT]: {_frases_txt}.
- [INPUT/ONTO] A máquina sem leitor (a pergunta do Clay) fica FORA e não é decidida aqui: é lida como a fita sem escala («eu sou eu mesmo»).
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); nenhuma chave antiga muda.
- [OPEN] Fica aberto: o par na face de Fock (D60: da v410 em diante); «o Ω do psíon da luz é o uniforme da instância» (provar ou podar); a ponte Bell-TT.
- Ressalvas ditas ({len(_DL.RESSALVAS_V409)}):
{_ressalvas_txt}
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v409_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v408')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v409.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d) e o HANDOFF, que é o fim da cadeia desta versão (D57a: sem S7 e sem S10).

## 4. Gates

Ver `PREPARACAO_v409_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""''')
bloco('RELATORIO = f"""', '\ngrava("PLANO_v409.md"', r'''RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v409 — A tradução às classes de Turing

Agente de preparação `claude-construtor-v409` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v408 `{CM.get('base_v408_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulo(s) no recibo; `KERNEL_RECIBO_v409.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v408 × v409 | {PORTOES['ast_v408_v409']}: {CMP.get('nos_nomeados_v408')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência nos textos (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e a pedra: {len(GF.get('pedras') or {})}) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v409.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v409.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v409.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v409.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v409.json`, zero ocorrências |

Fora dos portões, informativo: o orquestrador sem S7 e sem S10 (D57a), medido na lista de passos e no laço de `orquestrador/pos_treino_v409.py` = {SEM_S7_S10}; os textos da custódia encadeados no S6d: {', '.join(_textos_custodia) or 'AUSENTE'}.

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo, os textos da custódia e o HANDOFF; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D58: até três rodadas), nesta ordem, antes de qualquer publicação: `delta_v409.py` (moldura, erratas E24 a E26, decisões D55 a D60, as leituras, as ressalvas), `registros_v409.py`, `runtime_v409.py` (as {_DL.N_CHECKS_FECHO} checagens de `{_DL.FECHO_REGISTRO}` e a guarda das frases com a F37b), a pedra em `pedra/` (TraducaoTuring), as seções do artigo (`artigo_pt_v409.pysnip`, `artigo_en_v409.pysnip`) e `pos_rito/textos_v409.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v409 NÃO entrega: validade no kernel não é creditação; P = nP é teorema da TGL no modo seleção, relativo ao leitor (o psíon); a máquina sem leitor (a pergunta do Clay) fica fora e não é decidida aqui; o par na face de Fock segue aberto (D60); o Ω do psíon e o uniforme da instância têm a mesma forma, e que sejam o mesmo segue aberto; as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; nenhum teste com a natureza entra nesta versão.
3. O orquestrador lê `PREPARACAO_v409_PRONTA.json` e segue: `instalar_v409.py`, `rito_v409.sh`, `pos_rito/chain_pos_rito_v409.sh` (0 → 10, 10a, 10b, 10c → 14), os textos da custódia encadeados (S6d) e o HANDOFF (fim da cadeia, D57a), com a trava S1b aberta só pela revisão aprovada; a custódia completa e o release do app são da sessão de custódia.
4. Se o rito cair: `reverter_v409.py` é decisão da gerência; `refazer_candidato_v409.sh --regerar` refaz o candidato.

## 6. O módulo e as âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
{tab_pedras}

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
{tab_chave}

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
{tab_arq}
"""''')
a.marca("a v409 (A TRADUCAO AS CLASSES DE TURING): os 17 portoes da v408; a prosa, os avisos, as erratas E24-E26, as decisoes D55-D60 (Sonnet pela D58), os artefatos e o orquestrador MEDIDO sem S7/S10 (D57a)")
a.grava()
