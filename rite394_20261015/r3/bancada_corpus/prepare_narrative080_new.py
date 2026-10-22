from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_080_20260910'
REVIEW = ROOT / 'REVISOES_RAIZ_080_20260910'
TRANSFER_REVIEW = (ROOT / sys.argv[1]).resolve()
assert TRANSFER_REVIEW.is_relative_to(ROOT) and TRANSFER_REVIEW.is_dir()
transfer_reports = list(TRANSFER_REVIEW.glob('PARECER*.md'))
assert len(transfer_reports) == 1
transfer_report = transfer_reports[0]
REVIEW.mkdir(exist_ok=False)

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

sources = [
 ROOT / 'GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md',
 ROOT / 'REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md',
 ROOT / 'CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/compute_lorentz_characters080.py',
 ROOT / 'CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json',
 ROOT / 'CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md',
 ROOT / 'REVISAO_CARACTERES_LORENTZ_080_20260910_044753_743055/PARECER_SCRIPT_E_RECIBO_CARACTERES_080.md',
 ROOT / 'TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md',
 transfer_report,
 OUT / 'ESTADO_CANONICO_080.json']
before = [pin(path) for path in sources]
snapshot = json.loads(sources[-1].read_bytes())
assert snapshot['present'] == 77 and snapshot['embedded_files'] == 683
assert len(snapshot['absent']) == 21 and snapshot['seal_um_hash_matches']
assert all(row['unchanged'] for row in snapshot['comparison_with_delivery079'])
arithmetic = json.loads(sources[3].read_bytes())
assert arithmetic['check_count'] == 15 and arithmetic['all_checks_pass']

root_review = r'''# Parecer da raiz — geração E4 e controle inteiro080

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — leitura de fontes e recibos].

Li integralmente a nota de geração E4, sua revisão independente, o script aritmético, o recibo e a nota dos caracteres, além do parecer estático independente. Não encontrei erro material no alcance fixado. A transferência δ→E5 é de minha autoria e recebe parecer externo separado; este documento não é uma aprovação independente da própria construção.

Conferi os cortes de jatos: os deslocamentos de peso 0,1,3,4 para C,h,h*,C* compensam exatamente as ordens 1,2,1 dos mapas. A contração de pares em característica zero conserva valência; na soma ghost3/E4 só pode entrar (1,1,1,0). Não é necessário supor aciclicidade KT em grau negativo para esse resultado. Os antifields permanecem nas fronteiras que impõem a equação de Einstein em H⁰(L).

A completude do primeiro operador Calabi foi conferida diretamente em [Khavkine, Definição2 e §3.1, eq32](https://arxiv.org/pdf/1805.03751). A fonte fornece fatoração de operadores de compatibilidade, não apenas a identidade de gauge. Sua aplicação a ciclos pontuais usa homogeneidade para estender o ciclo a um operador local; a naturalização é uma projeção finita de intertwiners, como explicitado na revisão externa. Não se confunde essa completude com exatidão das soluções globais.

No tensor de curvatura corrigida, a contração é δRic−3Kh. O traço reverso em dimensão quatro, a densitização e κ não nulo identificam sua eliminação com a imagem dos antifields. A divergência de Weyl é aplicada após esse quociente. No símbolo prolongado, p_EA' p^AA'=(δ_E^A/2)p² implica p²Ψ=0 sem divisão por p². Contrações e antissimetrizações reduzem-se a essa relação ou à divergência; comutadores em curvatura constante dão somente termos de ordem menor. A recorrência linear de [Vasiliev, §9, eq87–91](https://arxiv.org/pdf/hep-th/9611024) foi conferida como controle primário, preservando a convenção de K da referência.

Assim o graduado dos jatos físicos é quociente dos tipos (2+r/2,r/2) e conjugados. Basta essa sobrejeção para a cota: não é usada liberdade universal dos jatos. Nos cortes tensoriais finitos, invariantes da isotropia são exatos após complexificação e projeção pela forma compacta. Isso justifica transportar fronteiras naturais e fazer a indução na ordem; não se faz média no grupo Lorentz não compacto nem se troca limite inverso e cohomologia.

Conferi a decomposição de Λ³(V⊕Λ²V), dimensão120. O script usa os dez vetores de peso, com dois zeros distintos, enumera triplas de índices e confere por Newton em inteiros. A extração lexicográfica e a reconstrução são coerentes. A cota4 em cada coordenada exclui todos os r≥1; as 15 verificações do recibo são controles dessa execução, incluindo integridade, não quinze teoremas de cohomologia. Não reexecutei o script.

As duas ocorrências de Weyl em r0 dão cota real2; os detectores079 com k e −k dão independência e injetividade de d1. A extensão Rher⊗R conserva o argumento inclusive para nilpotentes, porque os divisores usados são reais não nulos. Fixar K e κ é parte da hipótese. O argumento não se estende por decreto a um anel universal variável, coeficientes tensoriais ou espectadores com jatos não constantes.

Concluo favoravelmente à geração E4, à remoção de b4 de uma correção completável e ao alcance representacional do controle inteiro. E5, imagem de d1, prolongamentos superiores, admissibilidade causal, QME, UV e reconstrução física geral não são pagos por esta revisão. Os hashes anexos são lidos por script. Nenhum original foi alterado e nenhum um.py foi executado/importado.
'''
root_pin = emit(REVIEW / 'PARECER_GERACAO_E4_E_CARACTERES_080.md', root_review.encode('utf-8'))

report = r'''# Suficiência080 — geração completa em E4 e redução da obrigação a E5

10/09/2026. [DERIVED + KNOWN — demonstrações escritas revisadas, com completude Calabi importada] [REAL — controle inteiro e integridade documental].

**Na categoria declarada, toda correção completável pode começar em E5.** A classificação080 cobre todas as ordens finitas de derivadas do termo E4; os únicos dois geradores são justamente os candidatos Weyl já obstruídos na079. Um novo lema identifica a liberdade restante com a imagem do primeiro diferencial sobre H³(s0) em E5. Essa imagem ainda não foi calculada.

## 1. O canônico foi relido

A [captura080](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/ESTADO_CANONICO_080.json>) mede os quatro arquivos canônicos antes/depois e confere a presença por AST sem executar/importar um.py. Permanecem iguais à079: v338, 683 arquivos embutidos, 77 dos 98 módulos acompanhados presentes e 21 ausentes. O selo corresponde aos bytes de um.py e mantém a parede UV aberta. A evidência de execução existente foi lida, não reexecutada.

A integração dos módulos pendentes e a suficiência da construção geral continuam sendo obrigações distintas. H3 interno, registro de fase/ramo e falsificadores já reconhecidos não são reabertos. H³ nas fórmulas seguintes é um grau cohomológico.

## 2. O que agora está esgotado

O resultado vale no complexo métrico mínimo de zeroformas naturais orientadas, em dimensão quatro, numa referência espaço-forma com K>0 FIXADO, φ0 constante, κ não nulo e apenas os coeficientes escalares inertes herdados dessa referência. A ordem de jatos é finita por elemento; não há corte máximo arbitrário usado para declarar exaustividade.

Nessa categoria,

H³(s0)_(E4) = Rher[P] ⊕ Rher[P*],

onde P=W1_abcd C^a C^b m^cd, m_ab=∇bar_[a C_b] e a estrela atua na segunda dupla. São dois geradores reais, com a estrutura real Lorentziana preservada.

A demonstração faz a cadeia completa:

1. O BRST linear em jatos e a contração de pares dão H³(S⁴L)=H⁰(L)⊗Λ³H¹(L). Os antifields continuam nas fronteiras.
2. O quociente de Killing é G=V⊕Λ²V. A completude Calabi gera os invariantes lineares pela curvatura corrigida; as equações de Einstein eliminam os traços, deixando os jatos de Weyl.
3. Bianchi prolongada e comutadores reduzem todos os jatos aos tipos (2+r/2,r/2) e conjugados, modulo ordens inferiores. Basta uma sobrejeção; não se presume liberdade de todos os jatos.
4. A exatidão dos invariantes nos cortes finitos permite essa redução também no complexo natural. Só r0 pode emparelhar com Λ³G; os certificados079 dão independência dos dois geradores e injetividade de d1 sobre eles.

Por isso, de s0b4=0 e s0b5+s1b4=0 segue b4=s0v4. Subtrair sv4 elimina b4 e deixa z5=b5−s1v4, s0z5=0. Isso é uma mudança por fronteira, não a imposição de que a correção linear seja zero.

[Demonstração da geração](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md>) · [Revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_080_20260910/PARECER_GERACAO_E4_E_CARACTERES_080.md>).

## 3. O controle inteiro tem alcance próprio

Uma execução em Python puro enumera as 120 triplas exteriores dos dez vetores de peso, preservando os dois vetores distintos de peso zero. A identidade de Newton e a reconstrução por maiores pesos conferem o caráter completo. A cota4 em cada coordenada exclui todos os r≥1 das torres propostas; não se testaram apenas algumas ordens.

O recibo contém 15 controles, com revisão estática independente e sem reexecução nesta conferência. Esses controles não são compilação Lean, identificação do complexo físico ou substituto dos passos Calabi/Bianchi/naturalidade. Houve zero Lean novo nesta etapa.

[Cálculo e limites](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md>) · [Recibo inteiro](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>) · [Revisão estática](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CARACTERES_LORENTZ_080_20260910_044753_743055/PARECER_SCRIPT_E_RECIBO_CARACTERES_080.md>).

## 4. A obrigação restante tornou-se uma imagem explícita

Defina Kcal=ker[H³(C5)→H³(C3)], e δ:H³(C5)→H⁴(A6,s0), a conexão do próximo truncamento. A inclusão das classes fechadas de E5 dá uma aplicação q:H³(A5,s0)→Kcal. A remoção de E4 prova que q é SOBREJETIVA. Não foi necessário afirmar sua injetividade.

Para um ciclo z5, δq[z5]=[s1z5]=d1[z5]. Portanto

δ(Kcal)=im[d1:H³(A5,s0)→H⁴(A6,s0)].

A procura de uma classe que preserve o líder cúbico e prolongue até C6 equivale exatamente a

−[A6] ∈ im d1_(E5).

Se encontrarmos z5 fechado com esse valor, existirá a6 finito tal que r6+s1z5=s0a6, e T≤5+z5−a6 será fechado em C6. Isso fornece um certificado condicional com o sinal e a equação explícitos. Não demonstra que tal z5 exista.

O termo s2v4 não foi descartado em C6: s2b4+s1b5=s1z5−s0(s2v4), pela identidade s0s2+s1²+s2s0=0. Ele altera o representante, preservando a classe de obstrução.

[Lema de transferência](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) · [Revisão independente](<__TRANSFER_REVIEW__>).

O detector ímpar079 descende a ℓk em H⁴(A6,s0), e ℓk∘d1 independe do representante de z5. A condição necessária permanece (ℓk∘d1)[z5]=+4k/z0. Cumpri-la num teste não substitui a igualdade de classes acima. A classificação de E5 e a ação de d1 são o próximo cálculo.

## 5. Limites e caminho que permanece aberto

A geração E4 não foi estendida a um anel universal restrito com K variável, espectadores tensoriais, escalares de fundo não constantes, ou à referência material física φ=id. Ela preserva o anel escalar declarado, a valência e finitude de jatos por elemento; não garante toda restrição causal adicional de scaling degree ou contatos.

Mesmo resolver o próximo passo C5→C6 não concluiria a completação inteira. Permanecem a cohomologia da torre real e os demais canais do critério de anomalia, a primitiva admissível, contratermos causais, corrente/carga interagentes e QME, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e justificação UV.

A investigação081 sobre E5 e candidatos quadráticos fica EXCLUÍDA desta entrega; não sustenta nenhuma conclusão de cancelamento ou impossibilidade aqui. Todas as demonstrações080 são escritas, com importações identificadas e revisão independente; não são apresentadas como incorporadas ao kernel Lean canônico.

## 6. Preservação e continuidade

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate permanecem intactos; nenhum um.py foi executado/importado e nenhum teste de natureza foi realizado. A memória e o desenho novos registram o avanço sem substituir documentos anteriores. A entrega079 continua congelada com seu escopo histórico.
'''.replace('__TRANSFER_REVIEW__', transfer_report.as_posix())
report_pin = emit(OUT / 'REEXAME_SUFICIENCIA.md', report.encode('utf-8'))

memory = '''# Memória de trabalho080 — E4 classificado na referência fixada

10/09/2026. Adendo NOVO; nenhuma memória anterior ou Atlas foi alterado.

[REAL] Captura080: quatro canônicos iguais079, v338, 683 arquivos embutidos, 77/98 módulos acompanhados presentes, 21 ausentes, selo correspondente; leitura por bytes e AST, sem execução/importação. A parede UV permanece aberta. Ver ESTADO_CANONICO_080.json.

[DERIVED + KNOWN] A geração080, com Calabi importado e redução própria de jatos/Bianchi/invariantes, prova H³(s0)E4=Rher[P]⊕Rher[P*] na referência espaço-forma K>0 fixada, φ0 constante, κ≠0 e coeficientes escalares inertes. O detector079 dá d1 injetivo; correções completáveis removem b4 por fronteira e começam em E5. Não estender a K variável, tensores espectadores ou φ=id.

[DERIVED] Novo lema: q:H³(A5,s0)↠Kcal, δq=d1, logo δ(Kcal)=im d1E5. O termo s2v4 permanece como fronteira no resíduo de E6. Condição para o próximo prolongamento: −[A6]∈im d1E5. Se r6+s1z5=s0a6, usar T≤5+z5−a6. A imagem ainda não foi calculada.

[REAL] Uma execução de caracteres em inteiros Python, dimensão120, 15 controles registrados e revisão estática independente; zero Lean novo. Não somar esses controles à revisão documental nem contá-los como teoremas da cohomologia.

[OPEN] E5, imagem de d1, torre real, outros canais da anomalia, primitiva/contratermos/QME, compatibilidades, reconstrução geral pelos mesmos dados e UV. H3 interno, fase/ramo e falsificadores permanecem reconhecidos. Investigação081 separada, excluída desta entrega.

[Relatório080](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/REEXAME_SUFICIENCIA.md>)
'''
memory_pin = emit(OUT / 'MEMORIA_DE_TRABALHO_080.md', memory.encode('utf-8'))
design = '''# Adendo080 ao desenho do fechamento

10/09/2026. [DERIVED — caminho crítico atualizado em documento novo].

O objetivo integral permanece: reconstrução gravitacional geral pelos mesmos dados selecionados, conteúdo do registro preservado e teoria quântica interagente com alcance UV justificado. A parte fase/ramo já reconhecida não é reaberta.

Na frente local de anomalias, a liberdade E4 foi classificada no fundo espaço-forma fixado com coeficientes escalares inertes. Os dois geradores têm d1 injetivo; toda classe completável admite representante E5 fechado. Isso reduz a próxima obrigação a calcular im[d1:H³(A5,s0)→H⁴(A6,s0)] e decidir se contém −[A6].

Critério de avanço verificável: fornecer z5 admissível, s0z5=0, e a6 finito com r6+s1z5=s0a6; ou provar exclusão de −[A6] para TODA a imagem pertinente. Um detector com valor necessário, um corte arbitrário de derivadas ou outra família particular não bastam.

Mesmo um prolongamento C6 não encerraria valências superiores, comparação da torre, QME, contratermos e admissibilidade causal. Também continuam as compatibilidades físicas, a reconstrução geral e a rota UV. Os 21 módulos não incorporados são pendência própria de integração, sem confundir presença com suficiência.

Geração080 usa Calabi identificado e demonstrações escritas revisadas; caracteres têm 15 controles inteiros, zero Lean novo. Escopo fixado não autoriza variar K em anel restrito ou adicionar coeficientes tensoriais. Nenhum original/gate alterado. Investigação081 ainda fora desta entrega.

[Relatório e provas](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/REEXAME_SUFICIENCIA.md>)
'''
design_pin = emit(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_080.md', design.encode('utf-8'))
after = [pin(path) for path in sources]
assert before == after
record = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'ROOT_REVIEW_OF_GENERATION_AND_ARITHMETIC__TRANSFER_HAS_SEPARATE_REVIEW',
 'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
 'root_review': root_pin, 'narratives': [report_pin, memory_pin, design_pin],
 'writer': pin(Path(__file__)), 'cas_rerun': False, 'new_lean_compilations': 0,
 'originals_written': False, 'um_executed_or_imported': False, 'stage081_excluded': True}
record_pin = emit(REVIEW / 'REGISTRO_RAIZ_GERACAO_E4_080.json',
 (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'root_review': root_pin, 'report': report_pin, 'memory': memory_pin,
 'design': design_pin, 'record': record_pin}, ensure_ascii=True))
