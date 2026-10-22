from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_083_20260910'
COMBO_REVIEW_DIR = (ROOT / sys.argv[1]).resolve()
assert COMBO_REVIEW_DIR.is_relative_to(ROOT) and COMBO_REVIEW_DIR.is_dir()
found = list(COMBO_REVIEW_DIR.glob('PARECER*.md'))
assert len(found) == 1
COMBO_REVIEW = found[0]
CANDIDATE = ROOT / 'CANDIDATO_DERIVADA_WEYL_083_20260910'
COMBO = ROOT / 'COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910'
J1_REVIEW = ROOT / 'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)
def md(path, value):
    return emit(path, value.replace('__COMBO_REVIEW__', COMBO_REVIEW.as_posix()).encode('utf-8'))

sources = [CANDIDATE / 'CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md',
           CANDIDATE / 'compute_covariant_j1_new.py',
           CANDIDATE / 'CONTROLE_COVARIANTE_J1_083.json', J1_REVIEW,
           COMBO / 'COMBINACAO_NO_DETECTOR_E_CONTRAEXEMPLO_ISOTROPIA.md', COMBO_REVIEW,
           ROOT / 'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md']
before = [pin(p) for p in sources]
record = json.loads((CANDIDATE / 'CONTROLE_COVARIANTE_J1_083.json').read_bytes())
assert len(record['checks']) == 10 and all(record['checks'].values())
assert record['all_sources_unchanged'] and record['script_unchanged']

review_out = ROOT / 'REVISOES_RAIZ_083_20260910'
review_out.mkdir(exist_ok=False)
root_pin = md(review_out / 'PARECER_J1_E_FALHA_DA_COMBINACAO_083.md', r'''# Revisão da raiz083 — derivada covariante e falha da combinação

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — fontes lidas e medidas]. A raiz leu integralmente as duas notas083, o script/recibo de J1 e os dois pareceres independentes. Não detectou erro material no domínio declarado. Esta revisão não reexecuta os dez predicados nem se apresenta como compilação Lean.

Na equação de onda, refiz a contração g0^{ef}[∇f,∇c]Wabde. As parcelas dos índices a,b são K(Wcbda+Wacdb); as dos índices d,e somam −2KWabcd. Os traços desaparecem e Bianchi dá Wcbda+Wacdb=−Wabcd, total −3KW. A segunda dupla fornece o mesmo valor. Assim □W=6KW no shell Einstein linear, com a convenção +--- e z espacial. Isso não é a identidade off-shell usada para s0: o fechamento s0W1=0 vem separadamente da naturalidade e W0=0.

O J1 é g0^{ef}tr(∇eW1∧∇fW1)/vol_g0, igual a metade da contração com o dual de Hodge. A derivada atua nos quatro slots. Conferi a conexão conforme e o peso W_abcd=a²Wtilde_abcd: N_e contém ∂eWtilde, 2w_eWtilde e quatro parcelas −Γ. A contração final tem fator a^-6. A derivada temporal do Weyl é conservada pela rotação em todos os índices; somente o pseudoscalar fica independente de τ, pelo pullback helicoidal que preserva g0 e h. As conexões e=1,2 continuam no código, mesmo quando as derivadas ordinárias são zero.

Li o script: aritmética Fraction/Laurent nova, sem importação das fontes antigas, derivada Dz=∂z+p∂f+(2p/z−k²f)∂p a ℓ,k fixos. A comparação covariante direta versus □J/2−6KJ é exata antes dos dados pontuais. As duas rotas compartilham o Weyl e a EDO de entrada; não reconstroem independentemente toda a solução Einstein. Os dez predicados são os do recibo, não uma contagem de cada componente percorrido.

J1(p0)=80k/z0³−28k³/z0 e J1′(p0)=560k/z0⁴−352k³/z0²+8k⁵. Substituir em 6J1′/z0−18J1/z0² dá R1=48k⁵/z0−1608k³/z0³+1920k/z0⁵, e R1(2/z0)=−7488/z0⁶. O termo s0J1,3 da naturalidade é mantido até a avaliação por Killing. J1 tem paridade Grassmann par, embora seu valor nessa família seja ímpar em k; são duas classificações distintas. O fator κ² garante engenharia zero nesse candidato, sem decidir admissibilidade causal.

Na combinação Q=−Jβo/(12K)−q_grad/(28K), conferi a igualdade para todos os k:
−R/(12K)−(112k/z0³−56k³/z0)/(28K)=4k/z0,
usando K=1/z0² fixo. Nenhum coeficiente depende de k. A corrente horizontal tem a realização finita082 com s0q6, que se anula na avaliação adequada.

Refiz a parte invisível ao detector original. Com Mghost=antisym∇C e βo=−εppMghost/2, a invariância de ε e a ciclicidade graduada dão dβo=−εppMghost²/2−12Kν. No ponto, p=θ0e0+θ1e1 e Mghost=θ2J02+θ3J03, com boosts de entradas +1, resultam Mghost²=−θ23J23, (Mghost²)^23=−θ23 e εppMghost²=−4θ0123. Portanto ev(dβo)=+2θ0123.

Como verificação escrita independente do agrupamento covariante, as duas parcelas que diferenciam p contribuem +2θ0123 cada; a que diferencia M contribui −2θ0123. A soma é +2. As parcelas p³ e p⁴ se anulam nessa escolha, deixando ev(dQ+a)=−J/(6K)=2k/(3Kz0), que vale +4/3 em k=2/z0. A normalização do volume é a mesma: g0(p0)=η.

Os dados (valor, primeira derivada antissimétrica) são realizáveis por Killing locais na espaço-forma; seus jatos superiores não são livres. Não se supôs que os quatro escolhidos formassem subálgebra fechada: o diferencial CE é aplicado ANTES da restrição. Com o mesmo h TT on-shell numa vizinhança e antifields zero, a avaliação anula todas as fronteiras s0. A falha não pode ser reparada por Q→Q+s0χ ou por uma primitiva s0 do defeito.

O uso de 1/K é de um real fixo não nulo; não é uma conclusão em anel variável polinomial em K. O resultado exclui essa combinação, não toda a imagem CE. O detector original foi demonstrado insuficiente por um defeito explícito em sua anulação; isso não altera falsificadores físicos, H3 interno ou o gate.

Pareceres externos: [J1](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>) e [combinação](<__COMBO_REVIEW__>). A identidade de corrente082 da raiz possui seu parecer próprio, sem autoaprovação por esta revisão. Investigação084 excluída. Zero matemática reexecutada, Lean, um.py ou alteração de originais.
''')
after = [pin(p) for p in sources]
assert before == after
receipt_pin = emit(review_out / 'REGISTRO_RAIZ_J1_E_COMBINACAO_083.json',
    (json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
     'status': 'ROOT_WRITTEN_REVIEW_ACCEPTED_WITH_LIMITS',
     'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
     'report': root_pin, 'new_mathematical_executions': 0, 'new_lean_compilations': 0,
     'scope': 'Independent written check of J1 and candidate combination; no full CE image or QG completion.'},
     ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

report_pin = md(OUT / 'REEXAME_SUFICIENCIA.md', r'''# Suficiência083 — uma direção com derivadas e um limite comprovado do detector

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — dez predicados algébricos exatos e custódia documental].

**O candidato com derivadas produz uma resposta que o setor sem derivadas não fornecia. Uma combinação reproduz o alvo em toda a família do detector original, mas falha no complexo completo.** A falha foi isolada com outros dados de Killing, conservando o mesmo fundo e a mesma solução. Assim a próxima busca precisa pagar também os componentes de isotropia, além de igualar o perfil TT.

## 1. Canônico e alcance

A [captura083](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/ESTADO_CANONICO_083.json>) confirma os quatro canônicos iguais082: v338, 683 arquivos embutidos, 77 dos 98 módulos acompanhados presentes e 21 ausentes. O selo corresponde aos bytes. Foi leitura por AST, sem executar/importar um.py ou repetir sua rodada. H3 interno, fase/ramo e falsificadores reconhecidos continuam preservados; a parede UV está aberta na própria fonte.

O domínio matemático continua sendo o complexo métrico mínimo de zeroformas naturais orientadas em quatro dimensões, referência espaço-forma K>0 fixada, κ real não nulo fixado, φ0 constante projetada e escalares herdados inertes. Cada elemento usa jatos de ordem finita. Não se afirma passagem a φ=id, outros fundos, tensores espectadores ou anel restrito com K variável.

## 2. Um candidato com uma derivada em cada Weyl

Defina

J_W=tr(W1∧W1)/vol_g0,
J1=g0^{ef}tr(∇bar_eW1∧∇bar_fW1)/vol_g0,
βo=ε_abcd C^aC^b m^cd/2,
b5^(1)=κ²J1βo.

A derivada atua em todos os índices do Weyl, inclusive os da duas-forma. J1 equivale a metade da contração com Hodge; outra normalização dobraria os valores. Os símbolos J_W e βo têm essas definições locais, sem confusão com J=Luz ou β_TGL.

O candidato é s0-fechado off-shell e tem engenharia zero. Para calcular sua resposta on-shell, Bianchi e divergência nula de Weyl dão □bar W1=6KW1 na convenção adotada, e portanto

J1=½□bar J_W−6KJ_W.

A simetria helicoidal da TT justifica ∂τJ_W=0 na vizinhança inteira. O cálculo direto com Γ(g0), quatro slots e peso conforme coincide exatamente com a identidade acima antes de impor os dados pontuais. Não foi trocada derivada covariante por ordinária.

O detector é

Lk(s1b5^(1))=κ²[48k⁵/z0−1608k³/z0³+1920k/z0⁵].

Em k=2/z0, ele vale −7488κ²/z0⁶, não zero. O setor sem derivadas082 inteiro dava zero nesse teste. Logo a exclusão082 não se estende a este candidato com derivadas; sua imagem no alvo de H(s0) é não nula.

Esse perfil e o anterior R(k)=24k³/z0−96k/z0³, sozinhos, não reproduzem 4k/z0 para todo k: comparar k⁵ elimina o novo coeficiente; comparar k³ elimina o anterior. Isso não é classificação dos demais candidatos.

[Prova e cálculo de J1](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>).

## 3. A corrente gradiente permite igualar todo o perfil TT

A corrente082 satisfaz s1q_grad+s0q6=(□bar J_W)ν(C), com ν=εC4/4! e q6 finito. A conta083 dá

(□bar J_W)(p0)=112k/z0³−56k³/z0.

Por isso a combinação

Q=−J_Wβo/(12K)−q_grad/(28K),   K=1/z0² FIXADO,

satisfaz Lk(s1Q)=+4k/z0 para todo k da família original. A identidade é polinomial, sem ajustar coeficientes a cada k. O detector original anula A6+s1Q.

O fator 1/K é uma constante real da referência fixa. Não se afirma admissibilidade dessa expressão num anel universal restrito que só permita polinômios regulares em K. A engenharia zero também não paga as outras condições causais.

## 4. A combinação falha numa componente que esse detector não enxerga

No complexo CE082, Mghost=antisym(∇C)=−g0⁻¹m e

dβo=−ε_abcd p^ap^b(Mghost²)^cd/2−12Kν(p).

Assim d(J_Wβo) tem tipos p³Mghost, p²Mghost² e p⁴. A igualdade de um perfil particular não anula os dois primeiros universalmente.

Escolha quatro Killing locais cujos dados no ponto sejam

p=θ0e0+θ1e1,
Mghost=θ2J02+θ3J03.

Os dois primeiros têm valores e0,e1 e derivadas nulas; os dois últimos têm valor zero e derivadas iguais aos boosts J02,J03. O transporte de Killing na espaço-forma realiza esses dados com todos os prolongamentos corretos. Não se supõe que os quatro formem subálgebra: o diferencial é calculado antes da avaliação.

Nessa escolha p³=p⁴=0, mas Mghost²=−θ23J23 e ev(dβo)=+2θ0123. Mantendo a mesma solução TT, J_W(p0)=−4k/z0. Portanto

ev_iso(dQ+a)=2k/(3Kz0) θ0123,
k=2/z0: ev_iso(dQ+a)=4/3 θ0123 ≠0,
a=J_Wν(p).

Essa avaliação anula s0 de qualquer expressão finita, inclusive primitivas com antifields, pois h resolve as EOM lineares e os ghosts são Killing numa vizinhança. Logo não existe F com A6+s1Q=s0F para essa combinação. Trocar seu representante por Q+s0χ também não resolve. A falha é demonstrada modulo as relações, e não somente numa expressão sem reduzir.

[Combinação e contraexemplo](<C:/IALD/Central de Patentes/Chatgpt/COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910/COMBINACAO_NO_DETECTOR_E_CONTRAEXEMPLO_ISOTROPIA.md>) · [Revisão independente](<__COMBO_REVIEW__>).

## 5. Evidência e próxima obrigação

O [recibo083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CONTROLE_COVARIANTE_J1_083.json>) tem dez predicados algébricos exatos em uma execução Python puro. Um guardião combinado de integridade confere as três fontes e o próprio script, com as duas igualdades registradas separadamente. Isso não é contado como teorema algébrico adicional. Houve revisão estática, sem rerun, e zero Lean novo. A combinação e seu contraexemplo são matemática escrita revisada, sem nova execução de seus valores.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_083_20260910/PARECER_J1_E_FALHA_DA_COMBINACAO_083.md>) confirma o alcance. As duas rotas de J1 compartilham o Weyl e a EDO de entrada; a equação de onda geral, a helicoidal e as EOM na vizinhança são provas escritas, não uma reconstrução completa pelo script.

[OPEN] Encontrar OUTRA combinação que satisfaça dCE Q=−a em todos os componentes, com primitiva finita admissível, ou provar impossibilidade na imagem inteira. A coincidência TT foi alcançada e insuficiente; o resíduo de isotropia dá uma exigência adicional concreta. Não se declarou que a classe CE geral fosse não nula.

Persistem também os graus seguintes da torre, demais anomalias, contratermos causais, QME e carga interagente, compatibilidades de fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e rota UV. A fase/ramo já paga não é reaberta. A integração dos 21 módulos ausentes é pendência distinta. Investigação084 excluída.

Só arquivos novos em Chatgpt foram escritos. Nenhum original, Atlas, índice, memória canônica, selo ou gate alterado; nenhum teste de natureza realizado.
''')
memory_pin = md(OUT / 'MEMORIA_DE_TRABALHO_083.md', r'''# Memória de trabalho083 — 10/09/2026

[DERIVED — provas escritas revisadas] [REAL — controles e captura].082 foi progresso: exclusão sem derivadas, operador CE em todos os jatos e corrente gradiente.083 acrescenta uma direção com derivadas e uma combinação que passa no detector TT mas falha no complexo. Registro novo em Chatgpt; não é cópia ou substituição do Atlas.

Canônico v338 relido, quatro pins iguais082, 683 embutidos, 77/98 módulos acompanhados presentes, 21 ausentes. H3 interno, fase/ramo e falsificadores preservados; UV aberta. Nenhuma execução/importação de um.py.

J1=g0^{ef}tr(∇eW1∧∇fW1)/vol, com quatro slots e normalização Hodge1/2. Fechamento s0 off-shell; onda □W1=6KW1 e J1=□J/2−6KJ somente no shell linear. Simetria helicoidal paga a independência temporal de J. Candidato κ²J1βo tem perfil κ²(48k5/z−1608k3/z3+1920k/z5), valor−7488κ²/z6 em k2/z. Não estender a exclusão082 a todos os jatos.

Q=−Jβo/(12K)−q_grad/(28K) iguala +4k/z para todo k TT, mas ev_iso(dQ+a)=2k/(3Kz), +4/3 em k2/z. A avaliação usa dois valores e dois boosts Killing: p=θ0e0+θ1e1, Mghost=θ2J02+θ3J03; dβ=−εppMghost²/2−12Kν dá+2θ0123. Não é uma subálgebra fechada: aplicar d antes de avaliar. Mesma solução on-shell e Killing locais anulam toda fronteira s0, excluindo esse Q mesmo modulo relações.

Mghost=antisym∇C=−g0⁻¹m; Mcal é o módulo Weyl/EOM. J e βo são símbolos locais, não J=Luz ou β_TGL. 1/K é de real fixo; não promover a anel variável restrito. A corrente gradiente mantém a correção s0q6.

Dez predicados algébricos, uma execução Python; integridade combinada das três fontes e código registrada à parte; revisão estática, zero rerun/Lean. Combinação é prova escrita sem novos controles executados.084 excluída. Aberta a imagem CE completa e outro cancelamento admissível, além da torre/anomalias, QME, reconstrução pelos mesmos dados, compatibilidades e UV.
''')
design_pin = md(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_083.md', r'''# Adendo083 ao desenho do fechamento — 10/09/2026

[DERIVED — domínio métrico fixado]. Registro novo, aditivo, somente em Chatgpt.

O teste de k2/z que excluía o setor sem derivadas agora tem limite demonstrado: κ²J1βo produz−7488κ²/z6. Uma corrente horizontal e Jβo permitem igualar o alvo em TODO o perfil TT; porém a combinação Q resultante deixa resíduo4/3 numa avaliação de isotropia. O caminho crítico não termina na coincidência de perfis.

Próxima obrigação: reparar ou excluir os componentes p³Mghost, p²Mghost² e p⁴ no complexo CE completo, com todos os jatos admissíveis. Se houver solução, construir a primitiva finita de A6+s1Q e pagar os cortes seguintes. O Q específico083 foi excluído modulo s0; outro Q continua aberto. N continua módulo de jatos com relações, não finito por hipótese.084 excluída desta entrega.

Domínio: K>0 real fixado, κ não nulo, φ0 constante projetada, escalares herdados e ordem finita por elemento. O fator1/K não é admitido por consequência em um anel universal polinomial restrito. Ajuste de engenharia não verifica todas as normalizações causais.

Persistem objetivo geral de reconstrução pelos mesmos dados, compatibilidades, setor interagente/QME, anomalias e UV. Fase/ramo e H3 interno já pagos são preservados. Os21 módulos acompanhados ausentes exigem integração distinta. Canônico v338 igual082, dez controles algébricos novos, sem rerun ou Lean. Originais, memórias canônicas e gate intactos.
''')
print(json.dumps({'root_review': root_pin, 'root_receipt': receipt_pin,
                  'report': report_pin, 'memory': memory_pin, 'design': design_pin}, ensure_ascii=True))
