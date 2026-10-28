# Gera, por script, as cartas da Regra 26.4 (md + tex -> pdf), com os dados lidos das conferencias (nada de memoria).
# Rodada 2: o Aprendizado tem DUAS cartas, cada uma coerente com a folha 1/6 que a acompanha:
#   CARTA_REGRA_26_4_050576      -> folhas principais (caixa [1] com «VACUUM/GRAV/PHO», o que o depositado mostra)
#   CARTA_REGRA_26_4_050576_PHOT -> com ALTERNATIVA_FOLHA_1_050576_PHOT.pdf («PHOT» inteiro) no lugar da folha 1/6
import json, pathlib, subprocess, re, shutil, copy, sys
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')

APR = dict(
    k='050576', nome='CARTA_REGRA_26_4_050576', pct='PCT/BR2026/050576', ref='BR102026005477', deposito='04 de outubro de 2026', n_dep=5, n_nov=6, nfig=9,
    ib313='IB/313 [15] de 07 de outubro de 2026, Anexo C1, item 1, Desenhos «a», «d», «f», «h» e «k»',
    ib_desc='a) não admitem reprodução direta; d) tinta preta durável, traços de espessura uniforme e bem definidos; f) distinguíveis na reprodução reduzida; h) números, letras e linhas de referência com clareza e simplicidade; k) números e letras com altura mínima de 0,32 cm',
    plano_dep={1: '1/5', 2: '1/5', 3: '2/5', 4: '2/5', 5: '3/5', 6: '3/5', 7: '4/5', 8: '4/5', 9: '5/5'},
    plano_nov={1: '1/6', 2: '2/6', 3: '2/6', 4: '3/6', 5: '3/6', 6: '4/6', 7: '4/6', 8: '5/6', 9: '6/6'},
    paisagem='as folhas 1/6 (Figura 1) e 6/6 (Figura 9) estão em posição de paisagem, com o topo da figura voltado para o lado esquerdo da folha (Regra 11.13(j))',
    comum_d='rótulos, legendas e caixas de texto posicionados sem cobrir traço: nenhum fundo branco ou elemento opaco fica sobre linha, ponto, coluna ou hachura (onde a grade pontilhada passaria por um rótulo ou legenda, a grade foi interrompida); as setas reproduzem o sentido visível no depositado',
    extra='Nas folhas de substituição os trechos que a moldura ou outra caixa cortava no depositado aparecem inteiros somente quando a palavra consta da descrição depositada (VACUUM e PHOTON: parágrafo [033] e legenda da Figura 3); a curva da Figura 3 foi mantida exatamente como depositada. Os cantos e margens que o Organismo Receptor usa para marcar as folhas de substituição (canto superior direito e margem inferior) ficam livres.',
    comum_c='algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)',
    anexo='FOLHAS_SUBSTITUTIVAS_050576.pdf (6 folhas)',
    figs={
        1: 'folha em paisagem (topo à esquerda, R.11.13(j)); corpo 15 pt; fundos coloridos dos domínios PALAVRA, NOME e VERBO trocados por contorno pontilhado; caixas e setas tracejadas reencaminhadas para não cruzar rótulos; as pontas de seta entre [1] e [3] e entre [4] e [5] aparecem no sentido visível no depositado ([3] para [1] e [5] para [4]; no depositado a sobreposição das caixas as deixava assim); o rótulo da caixa [1] reproduz os caracteres visíveis no depositado («VACUUM/GRAV/PHO»)',
        2: 'corpo 15 pt; círculos e equação central redimensionados; «Comprimir» e «Filtrar» afastados das setas, sem fundo; fundos coloridos retirados',
        3: 'mesma curva, mesmas fronteiras e mesmos rótulos; as três primeiras letras de «VACUUM» e parte de «PHOTON 16b», cortadas pela moldura do gráfico no depositado, aparecem inteiras (palavras da descrição, [033]); rótulos de região sem fundo branco, com a grade pontilhada interrompida ao redor deles; «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto); legenda acima do quadro; letras de corpo 15 pt',
        4: 'corpo 15 pt; quatro estados e eixos mantidos; w>0, w<0, ∂w>0 e ∂w<0 fora das caixas (no depositado cruzavam as caixas); fundos coloridos retirados',
        5: 'caixas ampliadas para conter o texto; «Próxima geração» em duas linhas abaixo do trecho horizontal da seta de retorno, sem fundo branco (a borda da caixa CARGA fica contínua); cores retiradas',
        6: 'colunas com hachuras distintas (GRACE oblíqua, FRONTIER oblíqua inversa, VACUUM horizontal) no lugar de tons de cinza; limiares tracejados desenhados só entre as colunas (no depositado as colunas cobriam o traço); legendas com a hachura correspondente',
        7: 'séries distintas por marcador e tipo de traço no lugar de cor; legenda à direita; grade pontilhada preta',
        8: 'colunas hachuradas no lugar de cinza; «Vácuo angular» fora do quadro, à direita, com seta oblíqua para os buckets 13 e 14 vazios, como no depositado; sem fundo branco sobre a moldura ou a grade',
        9: 'folha em paisagem; caixas e setas pretas; nenhuma sobreposição; siglas em maiúsculas de corpo pleno (no depositado: versaletes)'})

APR_PHOT = copy.deepcopy(APR)
APR_PHOT.update(nome='CARTA_REGRA_26_4_050576_PHOT',
                anexo='FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf (6 folhas; só a folha 1/6 difere das folhas principais)',
                extra=APR['extra'].replace('(VACUUM e PHOTON: parágrafo [033] e legenda da Figura 3)', '(VACUUM e PHOTON: parágrafo [033] e legenda da Figura 3), com uma exceção declarada: na caixa [1] da Figura 1 o final «T», que a caixa [3] cobria no depositado, é completado («PHOT»; a abreviatura não consta literalmente da descrição, que traz «PHOTON»)'))
APR_PHOT['figs'][1] = APR['figs'][1].replace('o rótulo da caixa [1] reproduz os caracteres visíveis no depositado («VACUUM/GRAV/PHO»)',
                                             'o rótulo da caixa [1] aparece completo («VACUUM/GRAV/PHOT»): no depositado a caixa [3] cobria o «T» final')

MQC = dict(
    k='050579', nome='CARTA_REGRA_26_4_050579', pct='PCT/BR2026/050579', ref='BR102026003460', deposito='04 de outubro de 2026', n_dep=3, n_nov=8, nfig=8,
    ib313='IB/313 [15] de 07 de outubro de 2026, Anexo C1, item 1, Desenhos «d», «f», «h» e «k»',
    ib_desc='d) tinta preta durável, traços de espessura uniforme e bem definidos; f) distinguíveis na reprodução reduzida; h) números, letras e linhas de referência com clareza e simplicidade; k) números e letras com altura mínima de 0,32 cm',
    plano_dep={1: '1/3', 2: '1/3', 3: '1/3', 4: '2/3', 5: '2/3', 6: '2/3', 7: '3/3', 8: '3/3'},
    plano_nov={i: '%d/8' % i for i in range(1, 9)},
    paisagem='as folhas 1/8 (Figura 1), 4/8 (Figura 4) e 8/8 (Figura 8) estão em posição de paisagem, com o topo da figura voltado para o lado esquerdo da folha (Regra 11.13(j))',
    comum_d='legendas e caixas de texto dentro do quadro somente em região sem dados, ou acima do quadro (Figuras 3(a), 3(c), 4(a), 4(b) e 4(d)); nenhum fundo branco ou elemento opaco fica sobre linha, ponto, coluna ou hachura (onde a grade pontilhada passaria por uma legenda ou caixa, a grade foi interrompida); a graduação das marcas dos eixos acompanha o tamanho das letras (limites e dados inalterados, salvo o limite superior do eixo vertical de 4(c), ampliado para que o número sobre cada coluna apareça inteiro)',
    extra='Cada figura passou a ocupar folha própria porque as letras de no mínimo 0,32 cm não cabem em três ou quatro painéis por folha; os painéis de cada figura mantêm as designações (a), (b), (c) e (d) e os mesmos dados. Na Figura 4(d), o trecho da curva entre α² de 0,0017 e 0,0023 (correlação η de 0,9967 a 0,9976), que a caixa de métricas do depositado cobria, passa a ficar visível; nas demais legendas e caixas não havia dado coberto no depositado. Os cantos e margens que o Organismo Receptor usa para marcar as folhas de substituição (canto superior direito e margem inferior) ficam livres.',
    anexo='FOLHAS_SUBSTITUTIVAS_050579.pdf (8 folhas)',
    figs={
        1: 'folha em paisagem; painéis lado a lado como no depositado; categorias distinguidas por forma de marcador (círculo, quadrado, losango e estrela, todos cheios) no lugar de cor; planos cinza do 3D e círculos sombreados retirados; legenda acima do painel 3D; o rótulo do eixo Z não aparece no depositado (cortado) e não foi acrescentado',
        2: 'dois painéis empilhados em coluna única; séries distintas por tipo de traço (contínuo, tracejado, ponto-traço, pontilhado) no lugar de cor; área translúcida substituída por hachura; legendas e caixa de texto em região sem dados',
        3: 'três painéis empilhados; mesmas séries com tipos de traço distintos; áreas translúcidas viram hachura; legendas de 3(a) e 3(c) acima do quadro (no depositado, em canto livre); 3(b) em região sem dados',
        4: 'folha em paisagem, painéis 2x2; barras com quatro hachuras distintas; séries por tipo de traço; legendas de 4(a), 4(b) e 4(d) acima do quadro; caixa de métricas de 4(d) à direita da linha vertical (quebra de linha após «Correlação:»), onde não cobre a curva',
        5: 'três painéis empilhados; conforme a variante do PCT (convencional tracejada com círculos vazados; IALD contínua com quadrados cheios); 𝒜_C como no PCT; legendas em região sem dados',
        6: 'três painéis empilhados; séries por tipo de traço; rótulos dos eixos com sub e sobrescritos em corpo pleno; legendas em região sem dados',
        7: 'dois painéis empilhados; conforme a variante do PCT (LOCAL círculo cheio, REGIONAL quadrado vazado, GLOBAL triângulo cheio; sem caixa de anotação na 7a); legendas em região sem dados',
        8: 'folha em paisagem; tabela com o mesmo texto das 40 células; fundos coloridos e cabeçalho azul trocados por fundo branco com cabeçalho em negrito; nos símbolos A_C (coluna «Equação Governante», linha «Controlador Hierárquico») e E_Ψ (colunas «Elemento Original» e «Equação Governante», linha «Correção de Erros Adaptativa») o depositado mostra caixa de glifo ausente e as folhas desenham o símbolo em script (A_C consta do parágrafo [0056], equação (22), e E_Ψ da Tabela 1 da descrição depositada, em letra romana)'})


def md(d):
    k = d['k']
    L = []
    L.append('# Carta — Regra 26.4 do PCT (folhas de substituição dos desenhos)\n')
    L.append('> **Minuta preparada pela Central de Patentes em 27/10/2026 (rodada 2, após revisão), para liberação do operador. Não enviada.** Assinatura, local e data são do operador; a suficiência jurídica é do agente de PI [LEGAL].\n')
    L.append('[local], [data]\n')
    L.append('**Ao Instituto Nacional da Propriedade Industrial (INPI) — Organismo Receptor (RO/BR)**  ')
    L.append('Rua Mayrink Veiga, 9, 20º andar, Centro, Rio de Janeiro/RJ, CEP [dado pessoal removido]\n')
    L.append('**Pedido internacional:** %s  ' % d['pct'])
    L.append('**Ref. do processo do requerente:** %s  ' % d['ref'])
    L.append('**Data do depósito internacional:** %s  ' % d['deposito'])
    L.append('**Requerente:** ROTOLI MIGUEL, Luiz Antonio\n')
    L.append('**Assunto:** resposta à Solicitação de Correção de Irregularidades (PCT/RO/106) expedida em 09 de outubro de 2026 — folhas de substituição dos desenhos (Regra 26.4 do PCT).\n')
    L.append('**1.** Em atenção ao formulário PCT/RO/106 expedido em 09 de outubro de 2026, que no Anexo C1 (desenhos do pedido internacional tal como depositado) assinala o item 1 (publicação internacional razoavelmente uniforme, Regras 11 e 26.3.a)i)), Desenhos «d» (tinta preta durável; traços de espessura uniforme e bem definidos) e «k» (números e letras de altura inferior a 0,32 cm), e remete ao formulário %s (%s), a requerente apresenta, dentro do prazo de dois meses (Regra 26.2), folhas de substituição dos desenhos. Conforme a Regra 26.4, a correção consta de folhas de substituição acompanhadas desta carta, na qual se chama a atenção para as diferenças entre as folhas substituídas e as folhas de substituição.\n' % (d['ib313'], re.sub(r'\b([a-k])\) ', r'«\1»: ', d['ib_desc'])))
    L.append('**2. Folhas substituídas e folhas de substituição.** São substituídas todas as %d folhas de desenhos depositadas (1/%d a %d/%d, Figuras 1 a %d). Entram %d folhas de substituição (1/%d a %d/%d), em A4, com margens de 2,5 cm (superior), 2,5 cm (esquerda), 1,5 cm (direita) e 1,0 cm (inferior), sem molduras, numeradas em algarismos arábicos no alto da folha (n/N, com N = %d), com as figuras numeradas como no depositado (Figuras 1 a %d). %s.\n' % (d['n_dep'], d['n_dep'], d['n_dep'], d['n_dep'], d['nfig'], d['n_nov'], d['n_nov'], d['n_nov'], d['n_nov'], d['n_nov'], d['nfig'], d['paisagem'][0].upper() + d['paisagem'][1:]))
    L.append('| Figura | Folha substituída (como depositada) | Folha de substituição | Diferenças em relação à folha substituída |')
    L.append('|---:|:---:|:---:|:---|')
    for i in range(1, d['nfig'] + 1):
        L.append('| %d | %s | %s | %s |' % (i, d['plano_dep'][i], d['plano_nov'][i], d['figs'][i]))
    L.append('')
    L.append('**3. Diferenças comuns a todas as folhas.** (a) traços e letras em preto puro sobre fundo branco, sem tons de cinza e sem cor; (b) traços de espessura uniforme e bem definidos, legíveis em reprodução reduzida a dois terços; (c) %s; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s\n' % (d.get('comum_c', 'todos os números, letras e sinais de referência com altura mínima de 0,32 cm'), d['comum_d'], d['extra']))
    L.append('**4. Declaração.** As folhas de substituição corrigem somente as irregularidades formais apontadas e **não acrescentam matéria nova**: as figuras, os elementos, os sinais de referência, as palavras e os dados são os do pedido internacional tal como depositado; nenhuma figura foi acrescentada, suprimida ou renumerada. Mudaram apenas a apresentação (cor, espessura de traço, corpo das letras, disposição na folha e posição de rótulos e legendas), com as exceções declaradas no quadro do item 2.\n')
    L.append('**5.** Solicita-se que as folhas de substituição substituam integralmente as folhas de desenhos depositadas.\n')
    L.append('Anexo: %s.\n' % d['anexo'])
    L.append('Termos em que, pede deferimento.\n')
    L.append('[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]\n')
    return '\n'.join(L)


def esc(s):
    return (s.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('#', '\\#').replace('>', '$>$').replace('<', '$<$'))


def tex(d):
    k = d['k']
    T = []
    T.append(r'''\documentclass[a4paper,11pt]{article}
\usepackage[top=2.2cm,bottom=2cm,left=2.2cm,right=2cm]{geometry}
\usepackage{fontspec}
\setmainfont{Arial}[Extension=.ttf,UprightFont=arial,BoldFont=arialbd,ItalicFont=ariali,BoldItalicFont=arialbi,Path=C:/Windows/Fonts/]
\usepackage{longtable,array}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\pagestyle{empty}
\begin{document}''')
    T.append(r'\begin{center}{\large\bfseries Carta --- Regra 26.4 do PCT (folhas de substituição dos desenhos)}\end{center}')
    T.append(r'{\small\itshape Minuta preparada pela Central de Patentes em 27/10/2026 (rodada 2, após revisão), para liberação do operador. Não enviada. Assinatura, local e data são do operador; a suficiência jurídica é do agente de PI [LEGAL].}')
    T.append('[local], [data]')
    T.append(r'\textbf{Ao Instituto Nacional da Propriedade Industrial (INPI) --- Organismo Receptor (RO/BR)}\\ Rua Mayrink Veiga, 9, 20º andar, Centro, Rio de Janeiro/RJ, CEP [dado pessoal removido]')
    T.append(r'\textbf{Pedido internacional:} %s\\ \textbf{Ref. do processo do requerente:} %s\\ \textbf{Data do depósito internacional:} %s\\ \textbf{Requerente:} ROTOLI MIGUEL, Luiz Antonio' % (d['pct'], d['ref'], d['deposito']))
    T.append(r'\textbf{Assunto:} resposta à Solicitação de Correção de Irregularidades (PCT/RO/106) expedida em 09 de outubro de 2026 --- folhas de substituição dos desenhos (Regra 26.4 do PCT).')
    T.append(r'\textbf{1.} Em atenção ao formulário PCT/RO/106 expedido em 09 de outubro de 2026, que no Anexo C1 (desenhos do pedido internacional tal como depositado) assinala o item 1 (publicação internacional razoavelmente uniforme, Regras 11 e 26.3.a)i)), Desenhos «d» (tinta preta durável; traços de espessura uniforme e bem definidos) e «k» (números e letras de altura inferior a 0,32 cm), e remete ao formulário %s (%s), a requerente apresenta, dentro do prazo de dois meses (Regra 26.2), folhas de substituição dos desenhos. Conforme a Regra 26.4, a correção consta de folhas de substituição acompanhadas desta carta, na qual se chama a atenção para as diferenças entre as folhas substituídas e as folhas de substituição.' % (esc(d['ib313']), esc(re.sub(r'\b([a-k])\) ', r'«\1»: ', d['ib_desc']))))
    T.append(r'\textbf{2. Folhas substituídas e folhas de substituição.} São substituídas todas as %d folhas de desenhos depositadas (1/%d a %d/%d, Figuras 1 a %d). Entram %d folhas de substituição (1/%d a %d/%d), em A4, com margens de 2,5 cm (superior), 2,5 cm (esquerda), 1,5 cm (direita) e 1,0 cm (inferior), sem molduras, numeradas em algarismos arábicos no alto da folha (n/N, com N = %d), com as figuras numeradas como no depositado (Figuras 1 a %d). %s.' % (d['n_dep'], d['n_dep'], d['n_dep'], d['n_dep'], d['nfig'], d['n_nov'], d['n_nov'], d['n_nov'], d['n_nov'], d['n_nov'], d['nfig'], esc(d['paisagem'][0].upper() + d['paisagem'][1:])))
    T.append(r'{\small\begin{longtable}{|r|c|c|p{9.4cm}|}\hline \textbf{Fig.} & \textbf{Folha substituída} & \textbf{Folha de substituição} & \textbf{Diferenças em relação à folha substituída}\\\hline\endhead')
    for i in range(1, d['nfig'] + 1):
        T.append(r'%d & %s & %s & %s\\\hline' % (i, d['plano_dep'][i], d['plano_nov'][i], esc(d['figs'][i]).replace('\u2202', '$\\partial$').replace('\u03a8', '$\\Psi$').replace('\U0001d49c', 'A').replace('\u03b1\u00b2', '$\\alpha^2$').replace('\u03b7', '$\\eta$').replace('\u03b1', '$\\alpha$')))
    T.append(r'\end{longtable}}')
    T.append(r'\textbf{3. Diferenças comuns a todas as folhas.} (a) traços e letras em preto puro sobre fundo branco, sem tons de cinza e sem cor; (b) traços de espessura uniforme e bem definidos, legíveis em reprodução reduzida a dois terços; (c) %s; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s' % (esc(d.get('comum_c', 'todos os números, letras e sinais de referência com altura mínima de 0,32 cm')), esc(d['comum_d']), esc(d['extra']).replace('\u03b1\u00b2', '$\\alpha^2$').replace('\u03b7', '$\\eta$')))
    T.append(r'\textbf{4. Declaração.} As folhas de substituição corrigem somente as irregularidades formais apontadas e \textbf{não acrescentam matéria nova}: as figuras, os elementos, os sinais de referência, as palavras e os dados são os do pedido internacional tal como depositado; nenhuma figura foi acrescentada, suprimida ou renumerada. Mudaram apenas a apresentação (cor, espessura de traço, corpo das letras, disposição na folha e posição de rótulos e legendas), com as exceções declaradas no quadro do item 2.')
    T.append(r'\textbf{5.} Solicita-se que as folhas de substituição substituam integralmente as folhas de desenhos depositadas.')
    T.append(r'Anexo: %s.' % esc(d['anexo']))
    T.append('Termos em que, pede deferimento.')
    T.append(r'\vspace{1.2cm}[ASSINATURA E IDENTIFICAÇÃO --- a preencher pelo operador]')
    T.append(r'\end{document}')
    return '\n\n'.join(T)


if __name__ == '__main__':
    alvo = (APR, APR_PHOT) + ((MQC,) if 'mqc' in sys.argv else ())
    for d in alvo:
        nome = d['nome']
        (W / f'{nome}.md').write_text(md(d), encoding='utf-8')
        t = W / '_tmp' / nome
        t.mkdir(parents=True, exist_ok=True)
        (t / f'{nome}.tex').write_text(tex(d), encoding='utf-8')
        r = subprocess.run(['xelatex', '--disable-installer', '-interaction=nonstopmode', f'{nome}.tex'], cwd=t, capture_output=True, text=True)
        log = (t / f'{nome}.log').read_text(encoding='utf-8', errors='replace')
        errs = re.findall(r'^! .*$', log, flags=re.M)
        print(nome, 'erros TeX:', errs[:5])
        shutil.copy(t / f'{nome}.pdf', W / f'{nome}.pdf')
