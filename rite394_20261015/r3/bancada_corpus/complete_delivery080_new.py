from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_080_20260910'
DOC_DIR = (ROOT / sys.argv[1]).resolve()
assert DOC_DIR.is_relative_to(ROOT) and DOC_DIR.is_dir()
doc_reports = list(DOC_DIR.glob('PARECER*.md'))
assert len(doc_reports) == 1
doc_report = doc_reports[0]
TRANSFER_DIR = ROOT / 'REVISAO_TRANSFERENCIA_DELTA_080_20260910_045028_826573'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + '.tmp_new')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

adendum = '''# Revisões e alcance da entrega080

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — evidências documentais].

A fonte de geração E4 e o manifesto da transferência foram escritos antes de seus pareceres e conservam o estatuto histórico de espera por revisão. Para o estado desta entrega, devem ser lidos junto dos pareceres posteriores:

- [Geração E4: revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md>).
- [Caracteres: revisão estática independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CARACTERES_LORENTZ_080_20260910_044753_743055/PARECER_SCRIPT_E_RECIBO_CARACTERES_080.md>).
- [Transferência da imagem de δ: revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSFERENCIA_DELTA_080_20260910_045028_826573/PARECER_TRANSFERENCIA_DELTA_E5_080.md>).
- [Geração e caracteres: revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_080_20260910/PARECER_GERACAO_E4_E_CARACTERES_080.md>).
- [Relatório: conferência documental](<__DOC__>).

A geração é válida no fundo espaço-forma fixado e com coeficientes escalares inertes declarados. O argumento Calabi, o quociente por Einstein, Bianchi em todas as ordens finitas e a naturalidade foram revisados separadamente do caráter de dimensão120. A transferência usa q sobrejetiva, sem afirmar q injetiva. O termo s2v4 foi conservado na componente E6 como fronteira, com sinal explicitado no parecer.

As 15 verificações são as do recibo aritmético080: uma execução em inteiros Python, sem SymPy e sem nova execução nesta revisão. Não são todas identidades físicas; incluem controle de integridade do script. As verificações documentais têm contagem própria. Não houve compilação Lean nova. A nota final dos caracteres preserva o rascunho anterior e documenta sua precisão do produto exterior de dez fatores.

O adendo PROVENIENCIA_AUXILIARES_080.json registra cópias novas dos auxiliares079. O finalizador original079 teve uma falha histórica de caminho temporário, resolvida por adendo naquela entrega; aqui seu texto é somente a origem declarada de um código novo, cuja execução080 verifica os próprios dados. Nenhum sucesso079 foi presumido por reutilizar esse código. O estado PREPARED_NOT_EXECUTED dessa proveniência é temporal: a captura e a finalização posteriores possuem recibos próprios.

Investigação081 permanece fora da entrega080. A imagem de d1, o cancelamento de A6, valências superiores, anomalia/QME/UV e o objetivo físico geral não são declarados resolvidos. Nenhum original, memória canônica ou gate foi alterado.
'''.replace('__DOC__', doc_report.as_posix())
adendum_pin = emit(OUT / 'ADENDO_REVISOES_080.md', adendum.encode('utf-8'))
tunnel = '''# Entrega080 — geração E4 e redução da imagem de δ

10/09/2026. Para a sessão que codifica um.py. [DERIVED + KNOWN — matemática escrita revisada] [REAL — aritmética inteira].

Incorporar os resultados com seu domínio explícito: complexo métrico mínimo, zeroformas naturais orientadas, referência espaço-forma FIXADA K>0, φ0 constante, κ≠0 e coeficientes escalares inertes herdados. Ordem finita de jatos por elemento; nenhuma generalização silenciosa para K variável, tensores espectadores ou φ=id.

1. Geração completa de H³(s0)E4 por P=W1CCm e P*=W1*CCm. Calabi é importação nomeada; o quociente pelas EOM, redução triangular de jatos e invariantes finitos são partes efetivas da prova. Não basta inserir uma tabela de representações.
2. Detectores079 tornam d1 injetivo nesse módulo; se b4+b5 fecha em C5, escrever b4=s0v4 e z5=b5−s1v4, s0z5=0. Remoção por fronteira, preservando antifields e o termo s2v4 em C6.
3. A inclusão q:H³(A5,s0)→Kcal é sobrejetiva; δq=d1. Logo δ(Kcal)=im[d1 em E5]. Não declarar q injetiva nem a imagem calculada.
4. Critério exato para o próximo truncamento: −[A6]∈im d1E5. Se r6+s1z5=s0a6, T≤5+z5−a6 fecha em C6. Não extrapolar a todas as ordens ou QME.
5. O detector ℓk∘d1 é bem definido no quociente; seu valor +4k/z0 é condição necessária, não suficiente para igualdade de classes.

O caráter Λ³(V⊕Λ²V), dimensão120, tem um tipo Weyl por quiralidade em r0 e nenhum em r≥1 por cota de pesos. Uma execução Python em inteiros registra15 controles; revisão estática independente, sem rerun; zeroLean novo. Os controles não substituem a demonstração do transporte para jatos naturais.

Canônico relido: v338, quatro pins iguais079, 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum um.py executado/importado e nenhum original alterado. H3 interno, fase/ramo e falsificadores permanecem reconhecidos. Investigação081 excluída.

[Relatório completo](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/REEXAME_SUFICIENCIA.md>)

[Revisões e alcance](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/ADENDO_REVISOES_080.md>)

[Memória](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/MEMORIA_DE_TRABALHO_080.md>)

[Desenho do fechamento](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/DESENHO_DO_FECHAMENTO_ADENDO_080.md>)

[Manifesto](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_080_20260910/MANIFESTO_ENTREGA_080.json>)

Pendência imediata: calcular a imagem efetiva de d1 sobre E5. O objetivo integral mantém torre/anomalias, contratermos/QME, compatibilidades, reconstrução geral pelos mesmos dados selecionados e rotaUV abertos.
'''
tunnel_pin = emit(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_080_ESPONTANEA_geracao_E4_e_reducao_da_imagem_delta.md', tunnel.encode('utf-8'))
config = {
 'source_directories': [
  'GERACAO_WEYL_H3_E4_080_20260910',
  'REVISAO_GERACAO_WEYL_080_20260910_044142_861011',
  'CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368',
  'REVISAO_CARACTERES_LORENTZ_080_20260910_044753_743055',
  'TRANSFERENCIA_DELTA_PARA_E5_080_20260910',
  TRANSFER_DIR.name,
  'REVISOES_RAIZ_080_20260910',
  DOC_DIR.name],
 'new_exact_arithmetic_controls': 15,
 'new_lean_compilations': 0,
 'status': 'E4_GENERATED_BY_WEYL_PAIR_AT_FIXED_REFERENCE__COMPLETABLE_E4_REMOVABLE__DELTA_KERNEL_EQUALS_E5_D1_IMAGE__IMAGE_UNDECIDED',
 'written_results': [
  'In the fixed constant-curvature metric reference with inert scalar inherited coefficients, all natural finite-jet E4 ghost3 classes are generated by W1 CCm and its dual.',
  'Calabi compatibility, Einstein trace quotient, triangular Weyl jet reduction and finite invariant exactness justify the cohomological passage; characters alone do not.',
  'The previously verified Weyl detectors make d1 injective on E4; every completable correction can be represented by an s0-closed E5 term after a BRST boundary.',
  'The inclusion q from H3(s0)E5 onto kernel(H3(C5)->H3(C3)) is surjective and delta q=d1, hence delta(kernel)=image(d1 at E5).',
  'Minus[A6] belonging to that image is equivalent to the next C5->C6 lift with the same cubic cohomology class; explicit conditional representative T<=5+z5-a6.',
  'One pure-Python integer character execution records15 controls and dimension120, independently reviewed statically without rerun or Lean.'],
 'remaining': [
  'Classify/reduce H3(s0)E5 further and determine the actual d1 image; decide minus[A6] membership.',
  'Actual tower cohomology and comparison, remaining anomaly-criterion channels and higher lifts.',
  'Admissible anomaly primitive, causal counterterms, interacting current/charge, QME and compatible backgrounds/states/cutoffs.',
  'General gravitational reconstruction from the same selected data and justification of the ultraviolet route.',
  'Canonical integration and formal verification of the approved constructions and21 tracked absent modules.'],
 'limits': 'Fixed four-dimensional oriented constant-curvature Einstein reference K>0, constant sigma projected out with inherited inert scalar coefficients; no universal K-dependent restricted ring, tensor spectators or physical phi=id comparison. Full finite-jet E4 classification only; E5 image not determined. Integer controls/documentary checks/written proofs have distinct scopes. No Lean, um execution/import, nature test, original or memory modification or gate change. Stage081 excluded.'}
config_pin = emit(OUT / 'CONFIG_ENTREGA_080.json',
 (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'adendum': adendum_pin, 'tunnel': tunnel_pin, 'config': config_pin}, ensure_ascii=True))
