# Gera ESTADO.json e README.md com os hashes e medidas LIDOS dos arquivos (nunca de memoria). Rodada 2 (reparos pos-revisao).
import json, hashlib, pathlib, datetime, subprocess, sys
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


subprocess.run([sys.executable, '-X', 'utf8', str(W / 'fontes' / 'montar_conferencia.py'), '050576'], check=True)   # MQC congelado: nao se regenera
ts = (W / '_tmp' / 'ts_backup.txt').read_text().strip()
ts3 = (W / '_tmp' / 'ts_backup_r3.txt').read_text().strip()
mqc_antes = (W / '_tmp' / 'mqc_hashes_antes_r3.txt').read_text().split()
nomes = []
for k in ('050576', '050579'):
    nomes += [f'FOLHAS_SUBSTITUTIVAS_{k}.pdf', f'CARTA_REGRA_26_4_{k}.md', f'CARTA_REGRA_26_4_{k}.pdf', f'CONFERENCIA_{k}.json']
nomes += ['ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'CARTA_REGRA_26_4_050576_PHOT.md', 'CARTA_REGRA_26_4_050576_PHOT.pdf']
ent = {}
for nome in nomes:
    p = W / nome
    ent[nome] = {'bytes': p.stat().st_size, 'sha256': sha(p), 'sha16': sha(p)[:16]}
for nome in ('prancha_antes_depois_050576.png', 'prancha_antes_depois_050579.png', 'reparos_rodada2.json', 'mqc_legendas_do_depositado.json', 'contato_texto_grafico_r3.json'):
    p = W / 'conferencia' / nome
    ent['conferencia/' + nome] = {'bytes': p.stat().st_size, 'sha256': sha(p), 'sha16': sha(p)[:16]}
c76 = json.load(open(W / 'CONFERENCIA_050576.json', encoding='utf-8'))
c79 = json.load(open(W / 'CONFERENCIA_050579.json', encoding='utf-8'))
rr = json.load(open(W / 'conferencia' / 'reparos_rodada2.json', encoding='utf-8'))
res = {k: c['medidas_das_folhas_novas']['resumo'] for k, c in (('050576', c76), ('050579', c79))}
bak3 = {f: sha(W / (f + '.bak_' + ts3))[:16] for f in ('FOLHAS_SUBSTITUTIVAS_050576.pdf', 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'CARTA_REGRA_26_4_050576.pdf', 'CARTA_REGRA_26_4_050576_PHOT.pdf', 'CONFERENCIA_050576.json', 'README.md', 'ESTADO.json')}
mqc_depois = [sha(W / n)[:16] for n in ('FOLHAS_SUBSTITUTIVAS_050579.pdf', 'CARTA_REGRA_26_4_050579.pdf', 'CONFERENCIA_050579.json')]
ct3 = json.load(open(W / 'conferencia' / 'contato_texto_grafico_r3.json', encoding='utf-8'))
old_bak = {f: sha(W / (f + '.bak_' + ts))[:16] for f in ('FOLHAS_SUBSTITUTIVAS_050576.pdf', 'FOLHAS_SUBSTITUTIVAS_050579.pdf', 'CARTA_REGRA_26_4_050576.pdf', 'CARTA_REGRA_26_4_050579.pdf', 'CONFERENCIA_050576.json', 'CONFERENCIA_050579.json', 'README.md', 'ESTADO.json')}


def antes(c):
    b = c['como_depositado']['medida_antes (método A5, 300 dpi)']
    mins = [x['h_cap_min_cm'] for x in b]
    n = sum(x['linhas'] for x in b)
    nb = sum(x['linhas_abaixo_0_32'] for x in b)
    return 'mínimo por folha %s-%s cm; %d de %d linhas < 0,32 cm' % (str(min(mins)).replace('.', ','), str(max(mins)).replace('.', ','), nb, n)


def totais(k):
    a = sum(r['antes']['oclusoes'] for r in rr[k]['folhas'] if 'antes' in r)
    ap = sum(r['antes']['pontos_de_traco_cobertos_por_fundo_branco'] for r in rr[k]['folhas'] if 'antes' in r)
    d = sum(r['depois']['oclusoes'] for r in rr[k]['folhas'] if 'depois' in r)
    ro_a = [r['folha'] for r in rr[k]['folhas'] if 'antes' in r and not r['antes']['RO_livre']]
    ro_d = [r['folha'] for r in rr[k]['folhas'] if 'depois' in r and not r['depois']['RO_livre']]
    return a, ap, d, ro_a, ro_d


A76, A79 = antes(c76), antes(c79)
t76, t79 = totais('050576'), totais('050579')


def linhas_folhas(k):
    out = []
    for r in rr[k]['folhas']:
        a = r.get('antes', {})
        d = r.get('depois', {})
        out.append('| %d | %s (%s pts) | %s | %s -> %s |' % (r['folha'], a.get('oclusoes', '-'), a.get('pontos_de_traco_cobertos_por_fundo_branco', '-'), d.get('oclusoes', '-'),
                                                      'livre' if a.get('RO_livre', True) else 'OCUPADO', 'livre' if d.get('RO_livre', True) else 'OCUPADO'))
    return '\n'.join(out)


folga = rr['050576']['folga_texto_traco_cm']
setas = rr['050576']['setas_fig1']
estado = {
    'estado': 'RODADA_3_R2-1_REPARADO__050576_AGUARDA_RECONFERENCIA_SO_DO_R2-1__050579_ACEITA_E_CONGELADA__NADA_ENVIADO',
    'preparado_em': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'preparador': 'sonnet-ro106-preparador',
    'revisao_recebida': 'REVISAO_RO106_050576.md e REVISAO_RO106_050579.md: ACEITA COM REPAROS (B4 segue bloqueada ate ACEITA)',
    'decisao_do_operador_27_10_2026': 'A Central prepara as folhas substitutivas e a carta da Regra 26.4 para o operador liberar; ainda não respondeu ao RO/106',
    'prazo': {'RO106_expedido': '2026-10-09', 'fatal': '2026-12-09 [DERIVED, R.26.2 e R.80.2]', 'meta_interna': '2026-11-19'},
    'backups_da_rodada_1': {'sufixo': '.bak_' + ts, 'sha16': old_bak},
    'backups_da_rodada_3': {'sufixo': '.bak_' + ts3, 'sha16': bak3},
    'MQC_050579_congelado': {'sha16_antes_da_rodada_3 (FOLHAS, CARTA.pdf, CONFERENCIA)': [x for x in mqc_antes], 'sha16_depois': mqc_depois, 'inalterado': [a[:16] == b[:16] for a, b in zip(mqc_antes, mqc_depois)] if False else (mqc_antes == mqc_depois)},
    'revisao_rodada_2': {'050579': 'ACEITA (congelado)', '050576': 'ACEITA COM REPAROS: unico bloqueio R2-1 (grade tocava o pe do V de VACUUM); reparado na rodada 3'},
    'testes_novos': {'contato texto x grafico (pixel a pixel, 600 dpi; rodada 3)': {'050576_rodada2_antes': ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['total_de_contatos'], '050576_principal_depois': ct3['rodada3_050576_principal']['total_de_contatos'], 'variante_PHOT_depois': ct3['rodada3_050576_variante_PHOT']['total_de_contatos'], 'MQC_so_leitura': ct3['MQC_050579_congelado (so leitura)']['total_de_contatos']},
                     'oclusao (fundo branco/opaco sobre traco ou marca de dado)': {'050576': {'antes': t76[0], 'depois': t76[2]}, '050579': {'antes': t79[0], 'depois': t79[2]}},
                     'marcacao_do_RO (canto sup. direito e margem inferior livres)': {'050576': {'folhas_ocupadas_antes': t76[3], 'folhas_ocupadas_depois': t76[4]}, '050579': {'folhas_ocupadas_antes': t79[3], 'folhas_ocupadas_depois': t79[4]}}},
    'pedidos': {
        '050576': {'nome': 'Aprendizado Contínuo', 'folhas_depositadas': 5, 'folhas_substitutivas': 6, 'figuras': 9,
                   'altura_minima_caractere_cm': res['050576']['altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo'], 'pixels_nem_preto_nem_branco': res['050576']['pixels_nem_preto_nem_branco_total'],
                   'oclusoes': res['050576']['oclusoes_total'], 'folhas_com_marcacao_do_RO_livre': res['050576']['folhas_com_marcacao_do_RO_livre'], 'palavras_cruzadas_por_traco': res['050576']['palavras_cruzadas_por_traco_total']},
        '050579': {'nome': 'MQC', 'folhas_depositadas': 3, 'folhas_substitutivas': 8, 'figuras': 8,
                   'altura_minima_caractere_cm': res['050579']['altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo'], 'pixels_nem_preto_nem_branco': res['050579']['pixels_nem_preto_nem_branco_total'],
                   'oclusoes': res['050579']['oclusoes_total'], 'folhas_com_marcacao_do_RO_livre': res['050579']['folhas_com_marcacao_do_RO_livre'], 'palavras_cruzadas_por_traco': res['050579']['palavras_cruzadas_por_traco_total']}},
    'arquivos': ent,
    'o_que_falta': [
        'RECONFERÊNCIA só do R2-1 (README, seção «Rodada 3») para o Aprendizado; a B4 do operador segue bloqueada até ACEITA (050576); o MQC já está ACEITA',
        'OPERADOR: liberar (ou não) as folhas e as cartas; assinar/datar; escolher, com o agente de PI, a folha 1/6 principal (PHO) ou a alternativa (PHOT) e a carta correspondente',
        '[LEGAL] agente de PI: (a) PHOT; (b) sentido das setas [3]->[1] e [5]->[4] da Fig. 1 (descrição silenciosa/ambígua); (c) forma do glifo A_C e E_Psi na Fig. 8 do MQC; (d) leitura de 0,32 cm por maiúscula/algarismo/ascendente; (e) substituição integral das folhas e numeração n/N com o novo total; (f) declaração de «sem matéria nova»',
        'UPLOAD pelo Codex (ePCT) só depois da REVISÃO ACEITA e da frase do operador; nome exato da ação no ePCT para folhas de substituição [OPEN]',
        'ainda sem RO/106 para Mirror, IALD, Ψ-NET e Supercondutor (ver ORDEM 009 P1); este kit não os cobre'],
    'nao_feito': ['nada foi enviado, carregado, pago ou logado; nada foi escrito em EPCT\\ ou patents\\ nem em REVISAO\\; sem rede; nenhum processo encerrado']}
(W / 'ESTADO.json').write_text(json.dumps(estado, indent=1, ensure_ascii=False), encoding='utf-8')

readme = f"""# RO/106 de 09/10/2026 — folhas substitutivas e carta da Regra 26.4 (MQC 050579 e Aprendizado 050576)

Preparado em 27/10/2026 por `sonnet-ro106-preparador`, por decisão do operador: *«a Central prepara as folhas substitutivas e a carta da Regra 26.4 para eu liberar»*.
**Rodada 3 (só Aprendizado 050576):** a segunda revisão deu ACEITA ao MQC 050579 (congelado: nada dele foi tocado) e ACEITA COM REPAROS ao Aprendizado, com **um** bloqueio (R2-1); está reparado e há duas sugestões aplicadas (seção «Rodada 3»).
**Rodada 2:** a revisão independente deu **ACEITA COM REPAROS** aos dois PCT (`REVISAO\\REVISAO_RO106_050576.md` e `..._050579.md`); os reparos estão feitos abaixo e a frase do operador (B4) **continua bloqueada** até a segunda rodada dar ACEITA.
**Nada foi enviado.** Prazo fatal 09/12/2026 [DERIVED]; meta interna 19/11/2026. Estatutos: o que foi medido aqui é [REAL]; suficiência jurídica é [LEGAL] (operador / agente de PI).
Backups byte a byte das saídas da rodada 1: arquivos `*.bak_{ts}` na mesma pasta (e em `fontes\\`).

## Entregas (por script, com sha16 lido do arquivo)

| arquivo | o que é | sha16 |
|---|---|---|
""" + '\n'.join(f"| `{n}` | {d} | `{ent[n]['sha16']}` |" for n, d in (
    ('FOLHAS_SUBSTITUTIVAS_050576.pdf', 'Aprendizado: 6 folhas A4 (substituem as 5 depositadas), vetorial; caixa [1] = «VACUUM/GRAV/PHO» (o que o depositado mostra)'),
    ('ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'só a folha 1/6 com «PHOT» inteiro, para o agente de PI escolher (as folhas 2-6 são as mesmas)'),
    ('FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'VARIANTE PHOT completa: 6 folhas (1/6 alternativa + 2/6 a 6/6 iguais às principais), para ser enviada sozinha'),
    ('CARTA_REGRA_26_4_050576.md', 'carta Regra 26.4 (Aprendizado, folhas principais), minuta, assinatura em branco'),
    ('CARTA_REGRA_26_4_050576.pdf', 'idem, PDF'),
    ('CARTA_REGRA_26_4_050576_PHOT.md', 'carta da variante PHOT (frase da caixa [1] coerente com a folha alternativa)'),
    ('CARTA_REGRA_26_4_050576_PHOT.pdf', 'idem, PDF'),
    ('CONFERENCIA_050576.json', 'medidas, testes novos, provas de identidade, cotejo de palavras, reparos antes/depois, sha256 de entradas e saídas'),
    ('FOLHAS_SUBSTITUTIVAS_050579.pdf', 'MQC: 8 folhas A4 (substituem as 3 depositadas), vetorial'),
    ('CARTA_REGRA_26_4_050579.md', 'carta Regra 26.4 (MQC), minuta, assinatura em branco'),
    ('CARTA_REGRA_26_4_050579.pdf', 'idem, PDF'),
    ('CONFERENCIA_050579.json', 'idem para o MQC'))) + f"""

Também: `conferencia/prancha_antes_depois_<6>.png` (depositado em cima, substitutivo embaixo, mesma escala), `conferencia/reparos_rodada2.json` (medidas antes/depois), `conferencia/mqc_legendas_do_depositado.json`, `conferencia/*.json` (provas parciais), `ESTADO.json`, `entrada/`, `fontes/` (scripts), `_tmp/` (descartável; `_tmp\\base\\` guarda os PDFs da rodada 1 usados nas medidas «antes»).

## O que as folhas corrigem (e só isso)

Caixas marcadas, lidas nas imagens dos PDFs [REAL] — detalhe e método em `CONFERENCIA_<6>.json`:

* **RO/106 (09/10/2026), os dois PCT:** item 1 + Anexo C1; Anexo C1 item 1 (publicação internacional razoavelmente uniforme); Desenhos **d** (tinta preta durável; traços uniformes e bem definidos) e **k** (altura < 0,32 cm); observação «ver form IB/313»; prazo «DOIS MESES a partir da data de expedição». Nenhuma caixa de «Folhas contendo desenhos».
* **IB/313 [15] (07/10/2026):** MQC — Desenhos **d, f, h, k**; Aprendizado — Desenhos **a, d, f, h, k** (o «a» é de Desenhos/Regra 11.13, não de Folhas). Confirma a leitura da Central de 12/10 e a do revisor.

Corrigido: preto puro sobre branco, traço uniforme, letras e números com altura mínima de 0,32 cm, rótulos e legendas sem cobrir traço, A4 com margens 2,5/2,5/1,5/1,0 cm, sem moldura, numeração n/N centrada no alto, figuras numeradas como no depositado, **canto superior direito e margem inferior livres** para o carimbo do RO.

## Como foi feito

| | Aprendizado 050576 | MQC 050579 |
|---|---|---|
| desenhos como depositados | `04_DESENHOS.pdf` (5 folhas, sha16 {c76['como_depositado']['sha256'][:16]}); = páginas 19-23 do appb do ePCT (hash de imagem igual, folha a folha) | `04_DESENHOS_CINZA.pdf` do Codex (3 folhas, sha16 {c79['como_depositado']['sha256'][:16]}); = páginas 20-22 do appb do ePCT (idem) |
| fonte | LaTeX/TikZ de origem; **a compilação sem alteração reproduz o depositado** (correlação de forma 0,998-1,000 em 8/9; Fig. 4 = mesmo desenho) | funções de simulação do script de origem **sem alteração**; arrays de linhas/pontos/barras das Figs. 1-7 idênticos aos do script (max \\|diff\\| = 0, reconferido na rodada 2) e as 40 células da Fig. 8 idênticas |
| método | figuras redesenhadas em vetor (TikZ/pgfplots, xelatex, Arial Narrow 15 pt); nenhuma limiarização de raster | plotagem nova em matplotlib (Arial Narrow 14 pt), PDF vetorial montado com PyMuPDF |
| folhas | 5 -> 6 (Figs. 1 e 9 em paisagem) | 3 -> 8 (Figs. 1, 4 e 8 em paisagem) |
| altura mínima medida (maiúscula/algarismo/ascendente) | {res['050576']['altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo']} cm (antes: {A76}) | {res['050579']['altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo']} cm (antes: {A79}) |
| pixels nem pretos nem brancos (600 dpi, sem antialias) | {res['050576']['pixels_nem_preto_nem_branco_total']} | {res['050579']['pixels_nem_preto_nem_branco_total']} |
| margens / A4 / moldura | 6/6 folhas ok; nenhuma moldura | 8/8 folhas ok; nenhuma moldura |
| texto cruzado por traço / texto sobre texto | {res['050576']['palavras_cruzadas_por_traco_total']} / {res['050576']['palavras_sobrepostas_total']} | {res['050579']['palavras_cruzadas_por_traco_total']} / {res['050579']['palavras_sobrepostas_total']} |
| **oclusão** (fundo branco/opaco sobre traço ou marca) | **{res['050576']['oclusoes_total']}** (rodada 1: {t76[0]}) | **{res['050579']['oclusoes_total']}** (rodada 1: {t79[0]}) |
| **marcação do RO livre** (canto sup. direito, margem inferior) | {res['050576']['folhas_com_marcacao_do_RO_livre']}/6 (rodada 1: folha(s) {t76[3] or 'todas livres'} ocupada(s)) | {res['050579']['folhas_com_marcacao_do_RO_livre']}/8 |
| mesmas palavras | conjuntos iguais em 6/6; diferenças só «PHO» (principal) vs «PHOT» (fonte) e «vacuum» vs «cuum» cortado no depositado | iguais em 8/8 (diferenças = artefatos de extração, explicados no JSON) |

Por que mais folhas: letras de no mínimo 0,32 cm obrigam corpo 14-15 pt; os painéis e blocos de texto não cabem nas mesmas folhas. Total do pedido: Aprendizado 23 -> 24 páginas; MQC 22 -> 27 (ambos abaixo de 30; taxa por folha excedente [LEGAL/OPEN]).

## Os dois testes novos (rodada 2) — definição e resultado

1. **Oclusão** (`conferir.py: oclusao`, vetorial, em ordem de pintura): qualquer elemento de fundo branco/opaco (caixa de rótulo, legenda, caixa de texto, coluna, marcador vazado) que cubra um traço ou marca de dado pintado **antes** dele; conta pontos de traço (amostra a cada ~0,8 pt) dentro do polígono branco reduzido de 0,5 pt, ignorando o fundo da tela. Resultado: Aprendizado {res['050576']['oclusoes_total']} (rodada 1: {t76[0]} ocorrências, {t76[1]} pontos), MQC {res['050579']['oclusoes_total']} (rodada 1: {t79[0]} ocorrências, {t79[1]} pontos). Os marcadores vazados do MQC passaram a ter face transparente; as colunas, face transparente; onde a grade passaria por legenda/caixa/coluna ela é desenhada com lacuna.
2. **Marcação do RO** (`conferir.py: marcacao_RO`): pela Seção 325 das Instruções Administrativas [DECLARADO pela coordenação, lido de wipo.int em 27/10/2026] o RO marca cada folha de substituição no canto superior direito (número do pedido, data de recebimento) e na margem inferior («SUBSTITUTE SHEET (RULE 26)»). Teste a 600 dpi sem antialias: nenhuma tinta no canto superior direito (x >= 12 cm, y < 3,5 cm), na margem superior (y < 2,5 cm), na margem inferior (y >= 28,7 cm) nem na margem direita (x >= 19,5 cm). Resultado: Aprendizado {res['050576']['folhas_com_marcacao_do_RO_livre']}/6 folhas livres (rodada 1: a folha 6 tinha tinta no canto), MQC {res['050579']['folhas_com_marcacao_do_RO_livre']}/8. A folha alternativa PHOT também passa.

## Rodada 3 (Aprendizado 050576; o MQC 050579 está ACEITA e congelado)

* **R2-1 (único bloqueio):** na Fig. 3 (folha 2/6) a linha horizontal da grade em θ = 20 tocava o pé do «V» de «VACUUM 6 bits» (28 px a 600 dpi, segundo a revisão). **Reparo:** lacuna da grade ampliada (θ = 20 interrompida entre x = 0,036 e 0,104; a vertical x = 0,1 interrompida entre θ = 15 e 75; o rótulo ocupa θ 18,7-71,6 e x 0,044-0,087 em unidades do eixo). **Medida antes -> depois:** teste de contato texto x gráfico (novo, abaixo) {ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['total_de_contatos']} componente(s), {ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['pixels_em_contato']} px (folha 2, «VACUUM») -> **0** nas 6 folhas principais, nas 6 da variante PHOT e na folha alternativa; palavras cruzadas por traço (vetorial, ajustado): {res['050576']['palavras_cruzadas_por_traco_total']}; oclusões: {res['050576']['oclusoes_total']}; marcação do RO livre: {res['050576']['folhas_com_marcacao_do_RO_livre']}/6.
* **O teste agora pega o caso.** (1) *Contato texto x gráfico* (`conferir.py: contato_texto_grafico`): texto e gráfico renderizados em separado (600 dpi, sem antialias; redação em cópia na memória) e contato = pixel de tinta comum, componentes >= 3 px, excluída a régua do radical. Sobre o PDF da rodada 2 acusa a folha 2 («VACUUM», 25 px); sobre os PDFs desta rodada, 0 em todas as folhas. (2) O teste vetorial «palavras cruzadas por traço» **não via** o caso porque reduzia a caixa da palavra em 4% ao longo do texto e o pé do «V» fica na ponta de «VACUUM»; a redução ao longo do texto agora é 0% (a perpendicular segue 22%): acusa a folha 2 da rodada 2 e passa nas reparadas. Rodado sobre todas as folhas de ambas as variantes: 0. O MQC foi rodado só para leitura no teste de contato: 0 (`conferencia/contato_texto_grafico_r3.json`).
* **Sugestão 1 aplicada:** `FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf` (6 folhas: 1/6 alternativa + 2/6 a 6/6 iguais às principais — texto e pixels a 100 dpi conferidos), passa em todos os testes; a carta da variante PHOT cita esse arquivo como anexo.
* **Sugestão 2 aplicada:** item 3(c) das duas cartas do Aprendizado: «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)». A carta do MQC não foi tocada.
* **Sugestão da revisão (linha da Fig. 3, aplicada):** «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto).
* **MQC congelado:** hashes antes e depois desta rodada iguais ({', '.join(mqc_antes)} -> {', '.join(mqc_depois)}); `CONFERENCIA_050579.json`, folhas e carta do MQC não foram regenerados.
* Backups desta rodada: `*.bak_{ts3}`.

## Numeração das folhas (achado da coordenação, registrado)

A Seção 207 das Instruções Administrativas **não prevê esquema de sufixo** para folhas acrescentadas: as folhas de desenhos são numeradas n/N com o **novo total**. As séries do kit (1/6 a 6/6 e 1/8 a 8/8) estão de acordo com o texto (lido de wipo.int, s207 e s325, em 27/10/2026 [DECLARADO pela coordenação; o preparador não tem rede e não releu a fonte]). Substituir **todo** o conjunto de desenhos continua sendo decisão [LEGAL] do operador/agente de PI.

## Rodada 2 — pontos reparados, com medidas antes -> depois (para a segunda revisão, só estes)

### Aprendizado 050576

| id | pedido da revisão | o que foi feito | medida antes -> depois |
|---|---|---|---|
| R1 | setas [1]-[3] e [4]-[5] da Fig. 1: decidir e documentar o sentido | a descrição é **silenciosa** sobre o fluxo [1]-[3] ([002], [031]-[033], [041]) e só **sugestiva e ambígua** sobre [4]-[5] ([045] o hash opera também sobre «certificados»; [046] a cadeia registra hashes): pela regra da coordenação, reproduzido o **sentido visível no depositado** ([3] para [1], [5] para [4]); a fonte TikZ ([1]->[3], [4]->[5]) fica comentada em uma linha cada. **[LEGAL]** | cabeças de seta lidas no vetor: antes [1]-[3] {setas['antes']['[1]-[3]']}; [4]-[5] {setas['antes']['[4]-[5]']} -> depois [1]-[3] {setas['depois']['[1]-[3]']}; [4]-[5] {setas['depois']['[4]-[5]']} |
| PHOT | ponto 3: o principal reproduz só o visível; alternativa para o agente de PI | principal: «VACUUM/GRAV/PHO» (a caixa [3] cobre o T no depositado); `ALTERNATIVA_FOLHA_1_050576_PHOT.pdf` com «PHOT»; duas cartas, cada uma com a frase da sua folha. «PHOT» não está na descrição (só «PHOTON», [033]). **[LEGAL]** | texto vivo da folha 1: «PHOT» -> «PHO» (principal) / «PHOT» (alternativa); folhas 2-6 idênticas nas duas |
| R2 | Fig. 5 «Próxima geração» cortava a borda da caixa CARGA | rótulo em duas linhas, sem fundo, abaixo do trecho horizontal da seta; borda contínua | oclusões da folha 3: 1 (29 pontos) -> 0; folga da caixa do texto ao traço: «Próxima» {folga['antes']['Próxima']} -> {folga['depois']['Próxima']} cm, «geração» {folga['antes']['geração']} -> {folga['depois']['geração']} cm |
| R3 | Fig. 8 «Vácuo angular» cortava moldura, marca de eixo e grade | rótulo **fora** do quadro, sem fundo, seta oblíqua para os buckets 13-14 vazios (como no depositado) | oclusões da folha 5: 1 (193 pontos) -> 0; folga «Vácuo» {folga['antes']['Vácuo']} -> {folga['depois']['Vácuo']} cm, «angular» {folga['antes']['angular']} -> {folga['depois']['angular']} cm (o traço mais próximo de «angular» é o início da própria seta, que nasce junto ao rótulo; a caixa medida é a da fonte, maior que a tinta) |
| R3b | Fig. 3: rótulos de fundo branco sobre a grade | grade pontilhada desenhada à mão com lacunas ao redor de «VACUUM 6 bits» e «GRAVITON 10 bits»; legenda acima do quadro | oclusões da folha 2: 5 (330 pontos, incl. Figs. 2 e 3) -> 0; palavras cruzadas por traço: 0 |
| extra | Fig. 6 (não pedida): colunas de fundo branco cobriam o limiar tracejado | limiares desenhados só entre as colunas | oclusões da folha 4: 7 (216 pontos) -> 0 |
| R4 | corrigir a carta (3(d), setas, Figs. 3, 5, 8) | cartas reescritas: 3(d) descreve o que foi feito; linhas das Figs. 1, 3, 5, 6, 8; VACUUM/PHOTON só por estarem na descrição; PHOT só na variante | `CARTA_REGRA_26_4_050576*.md/.pdf` |

Oclusões por folha (antes = rodada 1) e marcação do RO:

| folha | oclusões antes (pontos de traço cobertos) | depois | marcação do RO antes -> depois |
|---|---|---|---|
{linhas_folhas('050576')}

### MQC 050579

| id | pedido da revisão | o que foi feito | medida antes -> depois |
|---|---|---|---|
| R1 | legendas 3(a), 4(a), 4(b) e 4(d) escondiam dado ou encostavam em caixa | legenda **dentro** do quadro só em região sem dado (varredura de posições contra linhas, pontos, colunas e hachuras, folga de 6 px); onde não há região livre (3(a), 3(c), 4(a), 4(b), 4(d)) a legenda fica **acima** do quadro; a caixa de métricas de 4(d) vai à direita da linha vertical; grade com lacuna sob legenda/caixa | oclusões: {t79[0]} ocorrências ({t79[1]} pontos) -> 0 nas 8 folhas; 3(a) 12 de 82 pontos cobertos (revisão) -> 0 |
| R1b | listar na carta o que ficar visível e estava escondido no depositado | medido nas figuras do script de origem: **só a Fig. 4(d)**: a caixa de métricas do depositado cobria o trecho da curva α² 0,00167-0,00225 (η 0,99675-0,99760, 2 vértices); as demais legendas/caixas do depositado não cobriam dado. Figs. 5 e 7 (variante do PCT): legendas em cantos vazios. Está na carta (nota do item 3) | `conferencia/mqc_legendas_do_depositado.json` |
| R2 | a carta deve citar a troca de glifo ausente por 𝒜/ℰ na Fig. 8 | linha da Fig. 8 da carta cita: A_C (coluna «Equação Governante», linha «Controlador Hierárquico») e E_Ψ (colunas «Elemento Original» e «Equação Governante», linha «Correção de Erros Adaptativa»), com A_C no [0056]/eq. (22) e E_Ψ na Tabela 1 da descrição; 3(d) corrigido; graduação dos eixos e o limite superior de 4(c) citados | `CARTA_REGRA_26_4_050579.md/.pdf` |
| R3 | forma do glifo na Fig. 8 | **nota ao agente de PI [LEGAL]:** desenhados A em script regular (U+1D49C, igual ao A_C da Fig. 5 **depositada**) e E em script regular (U+2130); a descrição ([0056], eq. (22), Tabela 1) escreve A_C e E_Ψ em letra **romana** e nenhum desenho depositado traz E em script. Alternativa conservadora: romano (uma linha em `fontes\\mqc_folhas.py`, `SPECIAL`). O preparador não decide. | texto das 40 células idêntico ao do script |
| R4 | conferência com teste de oclusão | incluído em `CONFERENCIA_050579.json` (por folha e no resumo), além do teste da marcação do RO | oclusões {res['050579']['oclusoes_total']}; marcação do RO {res['050579']['folhas_com_marcacao_do_RO_livre']}/8 |

Oclusões por folha (antes = rodada 1) e marcação do RO:

| folha | oclusões antes (pontos de traço cobertos) | depois | marcação do RO antes -> depois |
|---|---|---|---|
{linhas_folhas('050579')}

## Pontos para decisão [LEGAL] (o preparador NÃO decidiu)

1. **Critério de 0,32 cm:** medido como altura de maiúscula, algarismo e ascendente (método do A5, linha de texto vivo). Letras minúsculas sem haste (altura-x) ficam abaixo de 0,32 cm em qualquer desenho, em qualquer corpo razoável (ex.: «α», «v = c»); estão listadas no JSON. Sub e sobrescritos foram postos em corpo pleno.
2. **Aprendizado, Fig. 3:** a curva da fonte usa `deg(asin(x))` e o pgfplots já devolve graus, então o traço sobe quase na vertical e sai do quadro — **é assim no depositado e foi mantido** (corrigir seria mudar o desenho; Regra 91).
3. **Aprendizado, Fig. 1:** setas (R1) e «PHOT» (acima). Fig. 3: «VACUUM 6 bits» (as três primeiras letras estavam cortadas; «VACUUM» está na descrição, [033] e legenda da Fig. 3) e «PHOTON 16b» parcialmente cortado no depositado; «VACUUM6 bits» (sem quebra) virou «VACUUM 6 bits».
4. **MQC, Fig. 1:** o rótulo do eixo Z existe no script mas não aparece no depositado (cortado); **não foi acrescentado**.
5. **MQC, Fig. 8:** glifo (R3 acima).
6. **MQC, Figs. 5 e 7:** o depositado já é a regeneração da Central de agosto (marcadores; sem a caixa de anotação da 7a; 𝒜_C em mathtext; `00_DOSSIE.json`, `epct_corrections_2026_08_03`). Seguiram essa variante; a identidade com o raster depositado nessas duas é pela mesma função de simulação e sementes, e **não** por correlação de imagem completa (o revisor confirmou a 5(c): correlação 0,998).
7. **Cartas:** a declaração «sem matéria nova» e a lista de diferenças são minuta; assinatura, local e data em branco. Dados pessoais só o nome do requerente e a referência já constantes do RO/106.
8. **Cores:** as descrições dos pedidos citam cores (A5: MQC 9 menções; Fig. 5 do MQC: «azul», «vermelho» na breve descrição); tratar sem matéria nova é [LEGAL] e não foi tocado aqui.
9. **Numeração e substituição integral:** ver a seção «Numeração das folhas».

## O que falta

Segunda rodada de revisão (só os pontos acima); liberação e assinatura do operador (e escolha PHO/PHOT com o agente de PI); parecer [LEGAL] nos itens acima; upload pelo Codex no ePCT só depois da REVISÃO ACEITA e da frase do operador (nome exato da ação [OPEN]). Nada disto foi feito.

## Reproduzir

```
python fontes\\apr_01_originais.py ; python fontes\\apr_02_identidade_fonte.py     # fonte do Aprendizado = depositado
python fontes\\compilar.py aprendizado_folhas ; python fontes\\compilar.py aprendizado_folhas 0 ALTPHOT   # xelatex (principal e PHOT)
python fontes\\mqc_01_regenerar_originais.py ; python fontes\\mqc_folhas.py ; python fontes\\mqc_02_dados_identicos.py
copy _tmp\\aprendizado_folhas\\aprendizado_folhas.pdf FOLHAS_SUBSTITUTIVAS_050576.pdf ; copy _tmp\\mqc_folhas\\mqc_folhas.pdf FOLHAS_SUBSTITUTIVAS_050579.pdf
(a folha alternativa = pagina 1 de _tmp\\aprendizado_folhas_ALTPHOT\\aprendizado_folhas_ALTPHOT.pdf -> ALTERNATIVA_FOLHA_1_050576_PHOT.pdf)
python fontes\\conferir.py FOLHAS_SUBSTITUTIVAS_050576.pdf 050576 --rot 1,6 --ref-pdf entrada\\aprendizado\\04_DESENHOS_como_depositado.pdf
python fontes\\conferir.py FOLHAS_SUBSTITUTIVAS_050579.pdf 050579 --rot 1,4,8 --ref-pdf entrada\\mqc\\04_DESENHOS_CINZA_como_depositado.pdf
python fontes\\conferir.py ALTERNATIVA_FOLHA_1_050576_PHOT.pdf ALT_PHOT --rot 1
python fontes\\palavras.py apr FOLHAS_SUBSTITUTIVAS_050576.pdf ; python fontes\\palavras.py mqc <caminho absoluto de FOLHAS_SUBSTITUTIVAS_050579.pdf>
python fontes\\mqc_03_legendas_depositado.py ; python fontes\\reparos_medidas.py     # antes = _tmp\\base\\*_antes.pdf
python fontes\\contato_json.py ; python fontes\\carta.py ; python fontes\\prancha.py 050576 ; python fontes\\finalizar.py     # rodada 3: carta.py so gera o Aprendizado (use `carta.py mqc` para o MQC)
```
Ferramentas: Python 3.14, PyMuPDF 1.28.0, numpy, scipy, matplotlib 3.11.0, fontTools, MiKTeX (xelatex, pdflatex), fonte Arial Narrow do Windows (embutida nos PDFs).
"""
(W / 'README.md').write_text(readme, encoding='utf-8')
print('ESTADO.json e README.md gravados')
for n, v in ent.items():
    print(n, v['sha16'])
