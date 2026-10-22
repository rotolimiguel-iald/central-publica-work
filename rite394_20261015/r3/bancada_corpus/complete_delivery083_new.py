from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_083_20260910'
DOC_DIR = (ROOT / sys.argv[1]).resolve()
assert DOC_DIR.is_relative_to(ROOT) and DOC_DIR.is_dir()
found = list(DOC_DIR.glob('PARECER*.md'))
assert len(found) == 1
DOC_REPORT = found[0]
def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

adendum = r'''# Revisões e precisões da entrega083

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — custódia documental]. Os estatutos de revisão pendente nos documentos de origem conservam a história anterior à revisão. A entrega os lê com os pareceres posteriores:

- [J1 covariante](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>).
- [Combinação e isotropia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COMBINACAO_ISOTROPIA_083_20260910_054522_9585399/PARECER_COMBINACAO_E_RESIDUO_ISOTROPIA_083.md>).
- [Revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_083_20260910/PARECER_J1_E_FALHA_DA_COMBINACAO_083.md>).
- [Conferência documental](<__DOC__>).

Singer construiu as duas notas; Turing fez as revisões matemáticas independentes, e a raiz as conferiu. A identidade de corrente gradiente usada da082 foi construída pela raiz e tem revisão externa própria. A conferência documental083 não é contada como segunda aprovação matemática dos pareceres de seu autor.

O cálculo J1 tem dez predicados algébricos. Seu guardião de integridade é único e combinado: ele falha se os pins das três fontes mudarem OU se os bytes do próprio script mudarem. As duas igualdades e as quatro janelas estão registradas no recibo. No manifesto da entrega, new_source_integrity_controls=1 designa esse guardião combinado; não acrescenta um teorema algébrico. A nota da combinação tem zero novas execuções matemáticas. Nenhum rerun ou Lean foi feito.

Os controles de J1 comparam duas rotas que compartilham o Weyl e a EDO: a derivada covariante direta e a identidade de onda. A conexão em todos os slots, o peso conforme e a derivada temporal do tensor estão preservados. A simetria helicoidal é o argumento que torna o pseudoscalar independente de τ; não torna o tensor Weyl independente de τ. A onda geral e as EOM da vizinhança são provas escritas, não atribuídas a uma amostra do código.

J1 tem paridade Grassmann par e é pseudoscalar de orientação; seu valor na família TT é ímpar em k. Na passagem da fonte que diz “J1 é par”, o tipo é Grassmann, não a paridade em k. J_W, J1 e βo são símbolos locais tipados e não designam J=Luz ou β_TGL.

Mghost=antisym∇C=−g0⁻¹m na nota CE/combinação. Os Jab do contraexemplo são definidos por ENTRADAS: J02 e J03 têm +1 nos dois lugares da dupla; J23[2,3]=−1 e J23[3,2]=+1. Não se identifica por homônimo com e_a e_b♭−e_b e_a♭ sem conferir os sinais de assinatura. Isso conserva Mghost²=−θ23J23 e ev(dβo)=+2θ0123.

O detector TT original anula o defeito de Q para todo k. A avaliação alternativa aplica o diferencial completo primeiro, e só então usa os quatro Killing escolhidos, sem presumir uma subálgebra fechada. Ela deixa4/3 em k2/z0 e anula toda fronteira s0. Logo a combinação específica falha modulo as relações; outras classes continuam abertas.

1/K é de K real fixo não nulo, não uma conclusão em anel universal polinomial restrito. Engenharia zero não é toda admissibilidade causal. A investigação084 fica excluída. Os arquivos canônicos, memórias e gate não foram alterados.

O parecer de J1 registra uma tentativa de orquestração que falhou por sintaxe JavaScript antes de qualquer ferramenta ser executada. A chamada corrigida escreveu arquivos novos; não houve execução matemática extra ou alteração de fonte nessa tentativa. Os auxiliares083 preservam seus antecessores e registram as substituições de bytes em PROVENIENCIA_AUXILIARES_083.json. PREPARED_NOT_EXECUTED é o estatuto histórico antes de seus recibos de execução.
'''.replace('__DOC__', DOC_REPORT.as_posix())
adendum_pin = emit(OUT / 'ADENDO_REVISOES_083.md', adendum.encode('utf-8'))
tunnel = r'''# Entrega083 — derivadas de Weyl e limite do detector

10/09/2026. Para a sessão que codifica um.py. [DERIVED — demonstrações escritas revisadas] [REAL — dez predicados algébricos].

Domínio obrigatório: setor métrico mínimo natural orientado, quatro dimensões, referência espaço-forma FIXADA K>0, κ real não nulo fixado, φ0 constante projetada, escalares herdados inertes e jatos finitos por elemento. Não transportar por nome a φ=id, outros fundos, tensores espectadores ou anel variável restrito.

1. J1=g0^{ef}tr(∇eW1∧∇fW1)/vol, com derivada nos quatro slots e normalização Hodge1/2. Candidato κ²J1βo s0-fechado off-shell, engenharia zero. A onda □W1=6KW1 e J1=□J_W/2−6KJ_W valem no shell Einstein linear.
2. Perfil novo: κ²[48k⁵/z0−1608k³/z0³+1920k/z0⁵], com valor−7488κ²/z0⁶ em k2/z0. O setor sem derivadas082 dava zero ali. A imagem nova é não nula e fora da linha do perfil anterior, mas os dois perfis sozinhos não geram o alvo linear.
3. Usando a corrente horizontal082 e □J_W(p0)=112k/z0³−56k³/z0, Q=−J_Wβo/(12K)−q_grad/(28K) reproduz+4k/z0 no detector TT inteiro. Conservar s0q6 da realização da corrente.
4. A combinação NÃO cancela A6 universalmente. dβo=−εppMghost²/2−12Kν. Outros Killing locais dão p=θ0e0+θ1e1, Mghost=θ2J02+θ3J03, ev(dβo)=+2θ0123. O defeito é2k/(3Kz0)θ0123, igual a4/3θ0123 em k2/z0. Essa avaliação anula toda fronteira s0 e exclui a classe desse Q.
5. Aplicar dCE antes de avaliar: os quatro Killing alternativos não foram declarados uma subálgebra fechada. Os dois boosts têm entradas+1, e J23[2,3]=−1, J23[3,2]=+1. Mghost=antisym∇C=−g0⁻¹m; Mcal é outro objeto. 1/K pertence ao domínio real fixado, sem regularidade automática em K variável.

Validação: dez predicados algébricos numa execução Python puro; integridade do código e das três fontes por guardião combinado; revisão estática, sem rerun; zero Lean. Combinação e resíduo são provas escritas sem execução matemática adicional. A preservação da helicoidal, dos slots e dos fatores de volume consta das notas.

Canônico relido: v338, quatro pins iguais082, 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum um.py executado/importado, original ou gate alterado. H3 interno, fase/ramo e falsificadores preservados.084 excluída.

[Relatório](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/REEXAME_SUFICIENCIA.md>) · [Revisões e precisões](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/ADENDO_REVISOES_083.md>) · [Memória](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/MEMORIA_DE_TRABALHO_083.md>) · [Desenho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/DESENHO_DO_FECHAMENTO_ADENDO_083.md>) · [Manifesto](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_083_20260910/MANIFESTO_ENTREGA_083.json>).

Persistem outro cancelamento na imagem CE completa, primitiva admissível, graus posteriores, anomalias/QME, contratermos, compatibilidades, reconstrução pelos mesmos dados e rota UV. A integração dos módulos ausentes é obrigação distinta.
'''
tunnel_pin = emit(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_083_ESPONTANEA_derivadas_Weyl_e_limite_do_detector.md', tunnel.encode('utf-8'))
config = {
 'source_directories': [
  'CANDIDATO_DERIVADA_WEYL_083_20260910',
  'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304',
  'COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910',
  'REVISAO_COMBINACAO_ISOTROPIA_083_20260910_054522_9585399',
  'REVISOES_RAIZ_083_20260910', DOC_DIR.name],
 'new_exact_arithmetic_controls': 10,
 'new_source_integrity_controls': 1,
 'new_lean_compilations': 0,
 'status': 'FIRST_WEYL_DERIVATIVE_IMAGE_NONZERO__COMBINATION_MATCHES_ALL_TT_PROFILES_BUT_FAILS_ISOTROPY_MOD_S0__FULL_CE_TARGET_OPEN',
 'written_results': [
  'The first-derivative Weyl pseudoscalar J1 has a direct covariant calculation agreeing with Box J/2-6KJ on the linear Einstein shell; the new s0-closed candidate has detector -7488 kappa^2/z0^6 at k=2/z0.',
  'The natural gradient current gives the profile of Box J. The fixed-reference combination -J beta/(12K)-qgrad/(28K) matches the required +4k/z0 for the entire original TT detector family.',
  'A different realizable Killing evaluation with two value ghosts and two isotropy boosts leaves the nonzero residual +4/3; it annihilates every finite s0 boundary and therefore excludes that candidate class as universal cancellation.',
  'The different Killing selection is evaluated after the complete CE differential; it is not assumed to be a closed subalgebra. Fixed real K is distinguished from a variable restricted coefficient ring.',
  'Ten exact algebraic predicates in one Python execution, one combined integrity guard on sources and script; written combination proof, independent static reviews, no rerun or Lean.'],
 'remaining': [
  'Find another admissible quadratic Weyl jet cochain whose complete CE image cancels the target, or prove exclusion for the full relevant image.',
  'Pay isotropy and horizontal components together, construct a finite original BRST primitive, and establish causal admissibility and later lifts.',
  'Actual tower cohomology, remaining anomaly channels, causal counterterms, interacting charge/current, QME and compatible backgrounds, states and cutoffs.',
  'General gravitational reconstruction from the same selected data and justification of the ultraviolet route.',
  'Canonical integration and formal verification of approved constructions and the 21 absent tracked modules.'],
 'limits': 'Fixed oriented four-dimensional constant-curvature metric reference K>0 and nonzero real kappa, constant sigma projected out, inherited inert scalars and finite jets per element. The candidate J1 broadens detector image, not a complete classification. The combination passes the original TT detector but is excluded by one nonzero isotropy component modulo s0. Other candidate classes remain open. 1/K is for the fixed real background, not a polynomial universal ring. Ten algebraic predicates, one combined integrity guard, no extra mathematical execution for the combination, no rerun/Lean. No um execution/import, nature test, original or canonical memory write, or gate change. Investigation084 excluded.'}
config_pin = emit(OUT / 'CONFIG_ENTREGA_083.json',
                   (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'adendum': adendum_pin, 'tunnel': tunnel_pin, 'config': config_pin}, ensure_ascii=True))
