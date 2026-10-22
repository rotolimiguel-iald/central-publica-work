from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / ('RETRACAO_BRST_FUNDOS_072_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
assert OUT.is_relative_to(ROOT) and not OUT.exists()
OUT.mkdir()


def new_file(name, content):
    dest = OUT / name
    assert not dest.exists()
    raw = content.encode('utf-8')
    assert raw
    temp = OUT / (name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw)
    temp.rename(dest)
    assert dest.read_bytes() == raw
    return pin(dest)


def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


proof = r'''# Retração BRST relativa dos fundos para os campos completos

10/09/2026, arco 072. [DERIVED — demonstração algébrica escrita]. Somente arquivos novos na bancada Chatgpt. Nenhum um.py, Lean, CAS, produto temporal ou teste de natureza executado.

## 1. Enunciado e limite de aplicação

Construímos uma retração explícita do complexo clássico estendido por fundos e seus parceiros ímpares sobre o complexo dos campos completos. A retração é natural, mantém ordem local finita coeficiente a coeficiente e não avalia uma métrica em zero. Para S³, ela é definida na vizinhança da diagonal do par de mapas, globalmente sobre o alvo. Também fornecemos a fórmula que transporta uma primitiva relativa.

Isso resolve um subproblema algébrico de comparação. Para aplicá-lo à anomalia causal é necessário construir uma quebra estendida que satisfaça a identidade desse complexo. Os produtos Q2 existentes variam com o fundo e não satisfazem automaticamente tal identidade. O teorema desta nota não pressupõe nem prova a QME.

O mecanismo de contração de fontes de fundo é relacionado ao Apêndice B de [Barvinsky et al., 1705.03480v2](https://arxiv.org/pdf/1705.03480v2). Aqui a seção final também transporta os parceiros ímpares para os valores BRST dos campos, e a diferença entre mapas é tratada pela exponencial de S³. Não importamos a ausência de anomalias: ela é uma hipótese explícita do teorema de renormalização daquela referência.

## 2. Complexo antes do gauge fixado

Seja A o complexo BV completo da ação ambiente Einstein–sigma, incluindo campos, ghosts, fontes/antifields e jatos. Seu diferencial s tem grau fantasma um, s²=0 e anticomuta com d_H. A métrica e a matéria completas obedecem

\[
s g=\mathcal L_c g,\qquad s\phi=c^\mu\partial_\mu\phi.
\tag{2.1}
\]

Pode-se usar a apresentação métrica ou a apresentação por vielbein do arco071: neste último caso g=e^Tηe e a parte Lorentz cancela em sg. Nada abaixo contrai ghosts ou antifields pertencentes a A.

Acrescente fundos independentes B_g e B_phi, com parceiros ímpares Omega_g e Omega_phi de ghost um. São fontes externas, sem propagador. Trabalhe em jatos não submetidos às equações de movimento dos fundos. Em coordenadas locais do alvo,

\[
d_B B=\Omega,\quad d_B\Omega=0,\quad d_B|_A=0,
\qquad s B=s\Omega=0.
\]

Os diferenciais são prolongados aos jatos como derivações evolutivas. Defina D=s+d_B, com a convenção graduada usual. Os dois operadores anticomutam, pois suas ações originais usam conjuntos independentes de geradores. Logo D²=0 e Dd_H+d_HD=0. A regra d_BOmega=0 é a expressão coordenada do diferencial de de Rham no espaço de valores do fundo, não uma escolha de conexão plana global em TS³.

Para a matéria, Omega_phi pertence ao tangente ímpar em B_phi. Sob y'=f(y), suas componentes mudam por Omega'=f'(B)Omega; o termo f''(B)Omega Omega é zero pela simetria/antissimetria. Assim a definição de D é compatível entre cartas.

## 3. Os pares relativos corretos

No setor métrico use

\[
u_g=B_g-g,\qquad v_g=D u_g=\Omega_g-\mathcal L_cg.
\tag{3.1}
\]

Então Du_g=v_g e Dv_g=0. A mudança é triangular e invertível: B_g=g+u_g, Omega_g=sg+v_g. A projeção natural que é um mapa de complexos é

\[
B_g\mapsto g,\qquad\Omega_g\mapsto sg.
\tag{3.2}
\]

Em particular, B_g=g,Omega_g=0 NÃO é uma seção de complexos: D(B_g-g) nela vale −sg em geral. O parceiro ímpar deve acompanhar a seção.

No setor sigma tome, para pares próximos,

\[
u_\phi=\operatorname{Log}_{\phi}(B_\phi),\qquad
v_\phi=D u_\phi.
\tag{3.3}
\]

A exponencial da esfera redonda dá a inversa B_phi=Exp_phi(u_phi). O inverso do diferencial vertical de Exp é regular na seção zero. Portanto Omega_phi é recuperado pela regra da cadeia

\[
\Omega_\phi=
 (d_\phi\operatorname{Exp}_\phi)(u_\phi)[s\phi]
 +(d_u\operatorname{Exp}_\phi)(u_\phi)[v_\phi],
\tag{3.4}
\]

em coordenadas do fibrado tangente. Por construção Du_phi=v_phi e Dv_phi=0. Na diagonal, a projeção é B_phi=phi,Omega_phi=sphi. Ela é natural para mudanças de cartas e isometrias O(4).

Uma precisão de tipo é necessária: u_phi é um vetor baseado em phi, mas v_phi=D u_phi não transforma como um vetor isolado. Se u'=J(phi)u, então v'=J(phi)v+(sJ(phi))u. Esse termo é mantido; não se substitui v por uma derivada covariante com quadrado zero presumido. As duas operações usadas abaixo, u∂_v e a escala simultânea de u,v, são compatíveis com essa lei de transformação. Isso torna a homotopia global sobre a vizinhança da diagonal, sem escolher uma carta única de S³.

## 4. Classe local e homotopia

Complete formalmente a álgebra ao longo da diagonal, isto é, em u e v. Cada coeficiente considerado tem ordem de jatos finita e é polinomial nos jatos diferenciados; os coeficientes nos valores dos campos completos pertencem à classe A escolhida. Esta é uma conclusão coeficiente a coeficiente. Não se afirma um limite uniforme de ordem de jatos para uma série arbitrária.

Em jatos coordenados u_I,v_I, escreva

\[
h=\sum_{A,I}u_I^A\frac{\partial_L}{\partial v_I^A},\qquad
N=\sum_{A,I}\left(u_I^A\frac{\partial}{\partial u_I^A}
                    +v_I^A\frac{\partial_L}{\partial v_I^A}\right).
\tag{4.1}
\]

A soma age em somente um número finito de jatos em cada coeficiente. h é a derivação de ghost −1 que anula A e u e envia v a u. As identidades Du=v,Dv=0 implicam, verificando os geradores e prolongando por Leibniz,

\[
Dh+hD=N.
\tag{4.2}
\]

O termo (sJ)u na transformação de v não contribui para h(v'), pois h anula os coeficientes de A e u. Logo h(v')=Ju=u'; h é bem definido entre cartas. O mesmo vale para N. Prolongar uma transformação de ordem zero aos jatos preserva essa naturalidade.

Se p avalia u=v=0 e i inclui A, defina K como zero em grau N=0 e como h/n no componente de grau n>0. Equivalentemente, para T_lambda(u,v)=(lambda u,lambda v),

\[
K a=\int_0^1\frac{d\lambda}{\lambda}\,h T_\lambda a.
\tag{4.3}
\]

O componente de grau zero é anulado por h, de modo que não há divergência em lambda=0. Na série formal, integrar significa dividir cada coeficiente de grau positivo pelo inteiro correspondente. Não é uma avaliação de uma série em uma perturbação finita. Segue

\[
DK+KD=1-ip,\qquad pi=1,\qquad pD=sp,\quad Di=is.
\tag{4.4}
\]

Como h é evolutivo, comuta com as derivadas totais sobre coeficientes. Estendendo-o às formas com os sinais do grau total, Kd_H+d_HK=0. T_lambda também comuta com a derivada horizontal. Assim a retração vale na cohomologia relativa, não somente em zeroformas.

Em variáveis originais, a homotopia métrica é B_g(lambda)=g+lambda(B_g−g), Omega_g(lambda)=sg+lambda(Omega_g−sg). Para a matéria, B_phi(lambda)=Exp_phi(lambda u_phi) e Omega_phi(lambda)=D B_phi(lambda). Esta última igualdade inclui o termo de variação da base phi na exponencial. O caminho nunca manda g para a matriz nula. A métrica de fundo permanece não degenerada numa vizinhança suficientemente pequena da diagonal; na versão formal, sua inversa é a série regular em torno de g.

## 5. Fórmula explícita para a primitiva relativa

Se a tem ghost um e forma quatro e satisfaz Da+d_Hb=0, aplicar (4.4) fornece

\[
a=i(pa)+D(Ka)+d_H(Kb).
\tag{5.1}
\]

Aqui usamos KDa=−Kd_Hb=d_HKb, o que fixa o sinal. Suponha que a projeção no complexo de campos completos tenha uma primitiva

\[
pa=sB+d_HC.
\tag{5.2}
\]

Então a própria primitiva estendida é

\[
\boxed{a=D(iB+Ka)+d_H(iC+Kb).}
\tag{5.3}
\]

Esta é uma construção, não apenas uma igualdade de dimensões de grupos. Reciprocamente, i,p identificam as classes relativas dos dois complexos. Se A é exatamente a classe suave071, seu H¹,⁴ nulo pode ser consumido aqui na extensão formal declarada. Se A impõe covariância, analiticidade ou outra restrição adicional à primitiva B, (5.2) precisa valer nessa subclasse; a retração não fornece a propriedade que faltasse na entrada.

Há uma segunda avaliação, e não se deve confundi-la com p. Defina e_0 por Omega=0, conservando B como fundo independente. Na apresentação não gauge fixada, e_0D=s_B e_0, onde s_B é s com B inerte. Se a_ext é um cociclo estendido cuja restrição é a anomalia desejada a_Q2=e_0a_ext, então aplicar e_0 a (5.3) fornece uma primitiva de a_Q2. A condição de existência desse levantamento a_ext é essencial. A derivação de (5.3) não constrói a_ext a partir de um cociclo arbitrário com fundos inertes.

## 6. Propriedades preservadas e retorno ao gauge

As operações K,i,p atuam em valores de campos e parceiros e seus prolongamentos, sem propagadores e sem integração sobre pontos distintos do espaço-tempo. Assim preservam localidade e suporte das densidades testadas. A identidade modulo d_H para uma densidade multiplicada por cutoff f inclui o termo df correspondente; ele não é apagado. As afirmações sobre QME local continuam restritas à região em que o cutoff pertinente é constante.

Na apresentação métrica, dê a u o mesmo peso do respectivo campo e a v esse peso mais o peso homogêneo de s. h substitui v_I por u_I e reduz exatamente o peso de s. Portanto a primitiva K tem a dimensão necessária para corrigir uma quebra por s, e não acrescenta uma ordem diferencial. A mudança para variáveis originais pode introduzir derivadas de c e de campos já contidas em sg e sphi; são finitas e devem ser contabilizadas na classe, sem prometer uma cota de grau polinomial nas apresentações não lineares. Restrições de escala de Q2 precisam usar os pesos dos ghosts efetivamente adotados.

As transformações B_g=g+u_g e B_phi=Exp_phi(u_phi) são analíticas na variável de diferença perto da diagonal da esfera redonda. Elas e K preservam séries formais com coeficientes analíticos quando esses coeficientes já são analíticos. Nenhuma partição suave de unidade é introduzida nesta retração. Isso não converte uma primitiva B apenas suave em uma primitiva analítica.

Para incorporar o gauge fixado, pode-se primeiro introduzir os antifields externos conjugados de B e Omega, com a ação mínima estendida que gera DB=Omega,DOmega=0 e s em A. Ela satisfaz a CME pelo produto dos dois sistemas independentes. A transformação canônica gerada pela mesma férmion Psi(fields,B) de069 preserva a CME. Ela desloca também o antifield de B: manter só o deslocamento dos antifields dinâmicos omitiria o termo de fonte Omega proveniente de Psi. Não descartamos esse termo.

Denotando por C_Psi a transformação canônica, o diferencial correto é D_Psi=C_Psi D C_Psi⁻¹, e a homotopia se transporta por K_Psi=C_Psi K C_Psi⁻¹, com p_Psi=p C_Psi⁻¹ e i_Psi=C_Psi i. A identidade (4.4) é preservada por conjugação. As convenções esquerda/direita da ação e dos antifields são as do dicionário069; esta formulação por conjugação evita mudar isoladamente um sinal do termo Omega. Na restrição Omega=0 recupera-se o BRST do gauge escolhido com os fundos inertes. Os parceiros de fundo continuam fontes externas, sem novas linhas internas.

## 7. O que ainda falta para a identidade causal

O resultado de069 constrói produtos a partir de operadores e parametrices dependentes de B. Na álgebra assim parametrizada, d_B não é automaticamente uma derivação: ele diferencia o kernel usado no produto. Uma mudança de ordenação simétrica, por si só, também não corrige a variação da parte antissimétrica determinada pelo propagador causal. É necessário construir o transporte dos campos e a identidade de acordo perturbativo correspondente antes de importar a Ward estendida. Esta é uma obrigação analítica, além da retração (4.4).

Também há uma questão de domínio dos fundos. A expansão069 usa um fundo que resolve as equações e retira o termo linear da ação. Os B independentes usados nesta prova não satisfazem essa restrição. Se se impõe E(B)=0, os parceiros precisam obedecer à condição tangente linearizada e deixam de ser pares de jatos livres. Para realizar a extensão no esquema causal, é necessário organizar as variações permitidas, ou preservar a ação completa com seus termos lineares e fontes numa extensão apropriada. A CME clássica completa permanece válida; a invariância da parte quadrática isolada fora das soluções não foi deduzida dela.

[DERIVED] Portanto estão construídos a seção correta Omega=s(fields), os pares relativos naturais inclusive em S³, a homotopia finita por coeficiente e o transporte explícito de primitivas. [OPEN] Permanecem o levantamento causal a_ext, sua condição de consistência com transporte dos fundos, a admissibilidade da entrada B no espaço Q2 e a remoção quântica em todas as ordens. Nada aqui altera o estado dos módulos canônicos, o alcance físico da reconstrução gravitacional ou a obrigação UV.
'''

sources = [
    ROOT / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    ROOT / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
    ROOT / 'COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md',
    ROOT / 'REEXAME_SUFICIENCIA_071_20260910/MANIFESTO_ENTREGA_071.json',
]
source_pins = [pin(path) for path in sources]
output_pin = new_file('RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md', proof)
assert source_pins == [pin(path) for path in sources]
manifest = {'status': 'WRITTEN_DERIVATION_PENDING_INDEPENDENT_REVIEW',
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'sources': source_pins, 'output': output_pin,
            'script': pin(__file__), 'new_lean': 0, 'new_cas': 0,
            'originals_written': False, 'um_executed_or_imported': False,
            'qme_claimed': False, 'scope': 'Classical local formal background retraction, not a quantum Ward theorem.'}
manifest_pin = new_file('MANIFESTO_INICIAL_RETRACAO_072.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'directory': OUT.as_posix(), 'proof': output_pin, 'manifest': manifest_pin}, ensure_ascii=True))
