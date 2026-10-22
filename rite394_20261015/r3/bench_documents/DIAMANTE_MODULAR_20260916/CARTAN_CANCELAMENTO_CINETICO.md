# O termo induzido não acrescenta sozinho um modo propagante

17/09/2026. [DERIVED — cálculo clássico condicional, ainda sem revisão independente]. Hipóteses herdadas de CARTAN_F_PSI_E_FONTE.md: quatro dimensões, F positivo e independente da conexão, coframe invertível, sem fontes adicionais na variação da conexão. Não é conclusão sobre toda a TGL.

Escolha uma constante positiva F* com as mesmas unidades de F e defina gE=(F/F*)g, f=ln(F/F*). Essa constante serve à mudança de variáveis, não é parâmetro físico adicional ajustado.

A transformação conforme dá, com todas as densidades explícitas,

√|g| F R(g) = √|gE| F* [RE + 3 BoxE f − (3/2)(∂f)E²],
√|g| [3(∂F)g²/(2F)] = √|gE| F* (3/2)(∂f)E²,
√|g| Boxg F = √|gE| F* BoxE f.

Assim a expressão completa obtida ao eliminar a conexão satisfaz exatamente

√|g| [F R(g)+3(∂F)g²/(2F)−3Boxg F] = √|gE| F* RE.

Os termos cinéticos cancelam; as divergências também, quando ambas são mantidas. Não usamos condições de bordo para descartar uma integral. É uma identidade local da densidade após a mudança invertível de variáveis no domínio F>0.

Verificação geométrica alternativa: a conexão de Lorentz eliminada é LC do coframe eE=√(F/F*)e. A reconstrução afim no coframe original difere da LC(gE) pelo termo −δρσ ∂μ(f/2). Essa mudança escalar da conexão altera a curvatura por −δρσ d(df/2)=0. Portanto R(Γ,g)=(F/F*)RE e √|g|F R(Γ,g)=√|gE|F* RE diretamente. A conexão original não é LC(gE), embora a curvatura coincida neste sentido.

## Consequência física delimitada

O termo positivo 3(∂F)²/(2F), isoladamente, não prova um novo campo propagante nem uma energia positiva independente: sua contribuição cancela a mistura cinética do acoplamento não mínimo no setor gravitacional. Isso não torna ψ inteiro não dinâmico. Sua cinética original, o potencial, os acoplamentos de matéria e fontes de spin precisam ser transformados junto com a métrica. Não se conclui equivalência quântica sem examinar medida, renormalização, estado e observáveis.

Se, apenas como caso escalar separado, a ação restante contém −(1/2)Z(ψ)(∂ψ)g²−U(ψ), então ela se transforma em −(1/2)(F*/F)Z(ψ)(∂ψ)E²−(F*/F)²U(ψ). A dinâmica escalar remanescente vem desse setor; não do termo induzido contado uma segunda vez. O artigo lido mistura uma cinética de forma Ψμ com a expressão 'escalar': não substituímos automaticamente sua cinética por este exemplo.

## Relação com o resto modular

Uma redefinição clássica de campos não entrega um isomorfismo implementado das álgebras quânticas regionais, nem transporta automaticamente ω e T renormalizado. Logo esta identidade não demonstra que R modular desapareça, ou que seja central. Ela exclui uma inferência anterior possível: contar a contorção eliminada como um novo modo livre já fornecido à quantização. Para avançar o problema modular, o fornecedor necessário continua sendo a dinâmica completa do mesmo estado e dos mesmos observáveis regionais.

Conferência bibliográfica de fenômeno relacionado: https://link.springer.com/article/10.1140/epjc/s10052-019-6836-y (Palatini frames in scalar–tensor theories of gravity). Palatini e Cartan não foram identificados como formulações gerais iguais; a identidade acima foi derivada para a solução Cartan específica desta bancada.
