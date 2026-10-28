import pathlib, re
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\aprendizado_folhas.tex')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


# ---- preambulo: texto da caixa [1] (principal = so o visivel no depositado; ALTPHOT = alternativa com PHOT inteiro), grade e folhas em paisagem
rep(r'\newcommand{\sheetend}{\vss\egroup}',
    r'''\newcommand{\sheetend}{\vss\egroup}
\newcommand{\sheetbeginL}[1]{\sheetbegin{#1}\vskip 0.35cm}% folhas em paisagem: figura mais abaixo (canto superior direito livre para o carimbo do RO)
\ifdefined\ALTPHOT\newcommand{\PHOTtxt}{VACUUM/GRAV/PHOT}\else\newcommand{\PHOTtxt}{VACUUM/GRAV/PHO}\fi
\newcommand{\gv}[3]{\draw[dotted,line width=0.6pt] (axis cs:#1,#2) -- (axis cs:#1,#3);}% grade vertical (x,y0,y1)
\newcommand{\gh}[3]{\draw[dotted,line width=0.6pt] (axis cs:#2,#1) -- (axis cs:#3,#1);}% grade horizontal (y,x0,x1)''')
# ---- Fig 1
rep(r'lbl/.style={fill=white,inner sep=1.5pt}]', r'lbl/.style={inner sep=1.5pt}]')
rep(r'{[1] Quantizer\\v4.1\\VACUUM/GRAV/PHOT}', r'{[1] Quantizer\\v4.1\\\PHOTtxt}')
rep(r'(out) at (23.4,0)', r'(out) at (23.2,0)')
rep(r'\draw[arrow] ($(quant.east)+(0,0.5)$) -- ($(cache.west)+(0,0.5)$);',
    r'\draw[arrow] ($(cache.west)+(0,0.5)$) -- ($(quant.east)+(0,0.5)$);% sentido VISIVEL no depositado ([3]->[1]); a fonte TikZ tem [1]->[3]')
rep(r'\draw[arrow] (hash.east) -- (chain.west);', r'\draw[arrow] (chain.west) -- (hash.east);% sentido VISIVEL no depositado ([5]->[4]); a fonte TikZ tem [4]->[5]')
rep(r'\sheetbegin{1}', r'\sheetbeginL{1}')
rep(r'\sheetbegin{6}', r'\sheetbeginL{6}')
# ---- Fig 2: rotulos sem fundo, afastados da seta
rep(r'node[above left=0.12cm,sloped,fill=white,inner sep=2pt,pos=0.45] {Comprimir}', r'node[above=3pt,sloped,inner sep=2pt,pos=0.45] {Comprimir}')
rep(r'node[above right=0.12cm,sloped,fill=white,inner sep=2pt,pos=0.45] {Filtrar}', r'node[above=3pt,sloped,inner sep=2pt,pos=0.45] {Filtrar}')
# ---- Fig 3: bloco novo
a = s.index('% ======================== FIGURA 3 ========================')
b = s.index('% ======================== FOLHA 2 = Figuras 2 e 3')
fig3 = r'''% ======================== FIGURA 3 ========================
\figcap{\FB}{%
\begin{tikzpicture}
\begin{axis}[width=12.6cm,height=7.5cm,
  xlabel={$g_{\text{ratio}} = g / g_{\max}$},
  ylabel={$\theta = \arcsin(g_{\text{ratio}})$ (graus)},
  xmin=0,xmax=1,ymin=0,ymax=95,
  xtick={0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1},ytick={0,20,40,60,80},
  legend style={at={(0.5,1.06)},anchor=south}]
% grade pontilhada desenhada a mao, com lacunas onde ha rotulo (nenhum fundo branco apaga traco)
\gv{0.1}{0}{22}\gv{0.1}{68}{95}\gv{0.2}{0}{95}\gv{0.3}{0}{95}\gv{0.4}{0}{95}
\gv{0.5}{0}{33.5}\gv{0.5}{56.5}{95}\gv{0.6}{0}{33.5}\gv{0.6}{56.5}{95}\gv{0.7}{0}{95}\gv{0.8}{0}{95}\gv{0.9}{0}{95}
\gh{20}{0}{1}\gh{40}{0}{0.036}\gh{40}{0.104}{0.46}\gh{40}{0.64}{1}\gh{60}{0}{0.036}\gh{60}{0.104}{1}\gh{80}{0}{1}
\addplot[line width=1.4pt,domain=0:0.999,samples=200] {deg(asin(x))};
\addlegendentry{$\theta = \arcsin(g/g_{\max})$}
\addplot[line width=1pt,dashed] coordinates {(0.1097,0) (0.1097,90)};
\addplot[line width=1pt,dashed] coordinates {(0.994,0) (0.994,90)};
\addplot[line width=1pt,dash pattern=on 3pt off 3pt] coordinates {(0,6.29) (1,6.29)};
\addplot[line width=1pt,dash pattern=on 3pt off 3pt] coordinates {(0,83.7) (1,83.7)};
\node[rotate=90,inner sep=2pt] at (axis cs:0.07,45) {VACUUM 6 bits};
\node[align=center,inner sep=2pt] at (axis cs:0.55,45) {GRAVITON\\10 bits};
\end{axis}
\node[rotate=90,anchor=north,inner sep=3pt] at (current axis.east) {PHOTON 16b};
\end{tikzpicture}}{Figura 3}
\report{Fig3}{\FB}

'''
s = s[:a] + fig3 + s[b:]
# ---- Fig 5: rotulo fora da linha e sem fundo
rep(r'\draw[arrow] (save.west) -| node[pos=0.78,above,sloped,fill=white,inner sep=2pt] {Pr\'oxima gera\c{c}\~ao} (load.south);',
    r'''\draw[arrow] (save.west) -| (load.south);
\node[align=center,anchor=north,inner sep=2pt] at (1.75,-5.05) {Pr\'oxima\\gera\c{c}\~ao};''')
# ---- Fig 6: limiares em segmentos entre as colunas (nenhum fundo branco apaga traco); sem fundos nos quadros da legenda
a = s.index('% ======================== FIGURA 6 ========================')
b = s.index('% ======================== FIGURA 7 ========================')
fig6 = r'''% ======================== FIGURA 6 ========================
\figcap{\FA}{%
\begin{tikzpicture}
% limiares tracejados, desenhados so ENTRE as colunas (as colunas cobriam o traco no depositado)
\draw[dash pattern=on 7pt off 4pt] (0,4.5) -- (7.6,4.5);
\draw[dash pattern=on 7pt off 4pt] (8.4,4.5) -- (9.8,4.5) node[right,anchor=west] {$v_\ell > 0{,}95$ (VACUUM)};
\foreach \a/\b in {0/0.4,1.2/1.6,2.4/2.8,3.6/4.0,4.8/5.2,6.0/6.4,7.2/7.6,8.4/9.8}{\draw[dash pattern=on 7pt off 4pt] (\a,0.5) -- (\b,0.5);}
\node[anchor=west] at (9.8,0.5) {$\phi_\ell > 0{,}99$ (GRACE)};
\draw[-{Stealth[length=4mm]}] (0,0) -- (9.8,0) node[below,anchor=north east] {Camada $\ell$};
\draw[-{Stealth[length=4mm]}] (0,0) -- (0,6.6) node[above] {Esparsidade};
\foreach \x/\h/\st in {0.4/2.2/hatchA,1.6/2.0/hatchA,2.8/2.1/hatchA,4.0/3.0/hatchB,5.2/2.8/hatchB,6.4/3.2/hatchB,7.6/4.8/hatchC}{
  \path[draw=black,\st] (\x,0) rectangle (\x+0.8,\h);}
\node at (0.8,2.75) {$\ell_0$};
\node at (2.0,2.55) {$\ell_1$};
\node at (3.2,2.65) {$\ell_2$};
\node at (4.4,3.55) {$\ell_k$};
\node at (8.0,5.35) {$\ell_{27}$};
\foreach \x/\t/\st in {1.9/GRACE/hatchA,5.7/FRONTIER/hatchB,9.5/VACUUM/hatchC}{
  \node[draw,minimum width=3.7cm,minimum height=1.0cm] at (\x,-2.1) {};
  \path[draw=black,\st] (\x-1.85+0.12,-2.1-0.38) rectangle (\x-1.85+0.12+0.76,-2.1+0.38);
  \node[anchor=east] at (\x+1.75,-2.1) {\t};}
\end{tikzpicture}}{Figura 6}
\report{Fig6}{\FA}

'''
s = s[:a] + fig6 + s[b:]
# ---- Fig 8: rotulo FORA do quadro (como no depositado), seta oblíqua, sem fundo
a = s.index('% ======================== FIGURA 8 ========================')
b = s.index(r'\report{Fig8}{\FA}')
fig8 = r'''% ======================== FIGURA 8 ========================
\figcap{\FA}{%
\begin{tikzpicture}
\begin{axis}[width=13cm,height=8.5cm,xlabel={Bucket angular $b$},ylabel={Hits acumulados (3 gera\c{c}\~oes)},
  ymin=0,ymax=4,xmin=-0.5,xmax=14.5,xtick={0,1,2,...,14},ytick={0,1,2,3,4},grid=major,ybar,bar width=0.5cm]
\addplot[draw=black,line width=1pt,hatchA] coordinates {(0,3) (1,3) (2,3) (3,3) (4,3) (5,3) (6,3) (7,3) (8,3) (9,3) (10,3) (11,3) (12,3) (13,0) (14,0)};
\end{axis}
% anotacao FORA do quadro, com seta oblíqua para os buckets 13-14 vazios (nada de fundo branco sobre a moldura ou a grade)
\node[align=center,anchor=west,inner sep=2pt] (vac) at ([xshift=0.9cm,yshift=2.1cm]current axis.south east) {V\'acuo\\angular};
\draw[-{Stealth[length=3.5mm]}] (vac.south west) -- ([xshift=-0.45cm,yshift=0.75cm]current axis.south east);
\end{tikzpicture}}{Figura 8}
'''
s = s[:a] + fig8 + s[b:]
p.write_text(s, encoding='utf-8')
print('ok')
