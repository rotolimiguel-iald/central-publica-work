from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_081_20260910'
DOC_DIR = (ROOT / sys.argv[1]).resolve()
assert DOC_DIR.is_relative_to(ROOT) and DOC_DIR.is_dir()
doc_reports = list(DOC_DIR.glob('PARECER*.md'))
assert len(doc_reports) == 1
doc_report = doc_reports[0]

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

source = OUT / 'finalize_delivery081.py'
before = pin(source)
raw = source.read_bytes()
replacements = [(b'new_exact_integer_controls', b'new_exact_algebraic_controls'),
                (b'exact_integer_controls_and_no_lean', b'exact_algebraic_controls_and_no_lean')]
changes = []
for old, new in replacements:
    count = raw.count(old)
    assert count == 1
    raw = raw.replace(old, new)
    changes.append({'old': old.decode(), 'new': new.decode(), 'count': count})
ast.parse(raw)
finalizer_pin = emit(OUT / 'finalize_delivery081_algebraic.py', raw)
after = pin(source)
assert before == after
provenance = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'NEW_METADATA_LABEL_COPY_NOT_EXECUTED_YET',
 'source_before': before, 'source_after': after, 'target': finalizer_pin,
 'replacements': changes, 'scope': 'Use algebraic instead of integer for controls involving Fraction and exterior algebra; no check algorithm changed.',
 'source_preserved': True}
provenance_pin = emit(OUT / 'PROVENIENCIA_FINALIZADOR_ALGEBRICO_081.json',
 (json.dumps(provenance, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

adendum = '''# Revisões e precisões da entrega081

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — evidência documental].

As notas e os manifestos escritos antes de suas revisões conservam seu estatuto histórico. Nesta entrega, devem ser lidos conjuntamente com:

- [Revisão da redução E5](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md>).
- [Revisão do candidato e do cálculo](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_DETECTOR_WEYL_QUADRATICO_081_20260910/PARECER_DETECTOR_IMPAR_E_CLASSE_E5_081.md>).
- [Revisão das duas avaliações e retração](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_INDEPENDENCIA_RESIDUO_081_20260910_050818_526290/PARECER_DUAS_AVALIACOES_E_RETRACAO_081.md>).
- [Revisão da raiz de E5 e detector](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_081_20260910/PARECER_REDUCAO_E5_E_DETECTOR_081.md>).
- [Conferência documental](<__DOC__>).

A fatoração Bianchi079 foi construída por Herschel e revisada externamente pela raiz. O parecer081 de Herschel examina a nova aplicação pontual e a composição de Singer, sem ser contado como aprovação independente da própria fatoração079. A nota das duas avaliações é da raiz e possui parecer externo próprio. O cálculo do candidato tem revisão independente de Singer e conferência da raiz.

O recibo do candidato contém 14 registros TRUE: 13 algébricos e 1 de integridade, all_sources_unchanged. As cinco fontes possuem pins antes/depois. O próprio código matemático tem apenas pin final da execução; não se reconstrói um pin inicial a partir da medição atual. Janelas do finalizador ou da revisão são posteriores. As formas Weyl são entradas do script; sua derivação geométrica foi escrita e revisada separadamente. Não houve rerun ou Lean novo.

Neste relatório, J_W e Bgh nomeiam o pseudoscalar e a cúbica de ghosts chamados J e β na fonte do candidato. São definições locais com tipo explícito. O Q da representação081 designa o representante inteiro; quando se usa a parametrização079 de Q[h,h;C³]/2, tomar Q079/2=b5 evita duplicar o candidato.

O primeiro auxiliar de finalização081 foi preservado sem execução. Uma cópia nova troca somente o rótulo integer por algebraic nas chaves de controle, pois a execução inclui frações racionais e álgebra exterior. PROVENIENCIA_FINALIZADOR_ALGEBRICO_081.json mede essa mudança por bytes; os algoritmos de conferência permanecem iguais. Os estatutos PREPARED_NOT_EXECUTED são históricos e a execução posterior terá recibo próprio.

Na referência fixa, a classe construída tem imagem não nula, mas é independente de [A6]. A exclusão obtida vale para sua linha de múltiplos escalares, não para toda a imagem de d1. A apresentação de E5 por Sym²M mantém M como quociente, sem base ou dimensão finita presumida. Investigação082 excluída. Nenhum original, memória canônica ou gate alterado.
'''.replace('__DOC__', doc_report.as_posix())
adendum_pin = emit(OUT / 'ADENDO_REVISOES_081.md', adendum.encode('utf-8'))

tunnel = '''# Entrega081 — representantes E5, imagem não nula e independência

10/09/2026. Para a sessão que codifica um.py. [DERIVED — provas escritas revisadas] [REAL — controles exatos].

Domínio obrigatório: complexo métrico mínimo, zeroformas naturais orientadas, referência espaço-forma FIXADA em quatro dimensões, K>0, κ real não nulo, φ0 constante projetada e escalares herdados inertes. Jatos finitos por elemento; não ampliar por nome para φ=id, K variável, espectadores tensoriais ou todas as normalizações Q2.

1. H⁻¹(L,s0)=0 pela fatoração Bianchi aplicada ao módulo linear pontual, preservando ordem finita. Com Sym⁵ e invariantes: H³(s0)E5≅Rher⊗[Sym²M⊗Λ³G]^Lorentz. M é quociente dos jatos Weyl; não declarar liberdade, base finita ou dimensão dez.
2. Todo ciclo b5=Q+s0χ5, com Q quadrático em jatos Weyl e s0Q=0 off-shell. Conservar primitivas h³C², h*hC³, C*C⁴. Retirar antifields do representante não autoriza retirá-los das relações.
3. Candidato b5=κJ_W Bgh, com J_W=tr(W1∧W1)/vol_g0 e Bgh=εCCm/2: s0b5=0 e Lk(s1b5)=κ(24k³/z0−96k/z0³). Sua classe tem imagem não nula; δ(Kcal)≠0. Preservar s1J_W+s0J3=C∂J_W antes da avaliação.
4. Para a=[A6], b=[s1b5], as avaliações k1=1/z0 e k2=2/z0 dão matriz [[−4/z0²,−72κ/z0⁴],[−8/z0²,0]], det−576κ/z0⁶. Há retração explícita e somando livre Rher². −a não pertence à linha Rher b; a imagem inteira de d1 continua sem decisão.
5. Próximo filtro: ℓ_(2/z0)(d1Q)=+8/z0². Igualar esse valor ainda não paga a identidade r6+s1Q=s0a6.

O recibo tem 13 controles algébricos e 1 de integridade das cinco fontes; uma execução Python puro, revisão estática, zero rerun/Lean. Pin próprio do script somente final. As formas Weyl são entradas do código e têm derivação geométrica escrita separada. As duas avaliações não são contadas como execução nova.

Canônico relido: v338, quatro pins iguais080, 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum um.py executado/importado e nenhum original alterado. H3 interno, fase/ramo e falsificadores preservados.082 excluída.

[Relatório completo](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/REEXAME_SUFICIENCIA.md>)

[Revisões e precisões](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/ADENDO_REVISOES_081.md>)

[Memória](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/MEMORIA_DE_TRABALHO_081.md>)

[Desenho do fechamento](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/DESENHO_DO_FECHAMENTO_ADENDO_081.md>)

[Manifesto](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/MANIFESTO_ENTREGA_081.json>)

Persistem a imagem total, cancelamento, torre/anomalias, contratermos/QME, compatibilidades, reconstrução pelos mesmos dados e rota UV. A incorporação dos módulos pendentes é obrigação distinta.
'''
tunnel_pin = emit(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_081_ESPONTANEA_representantes_E5_imagem_nao_nula_e_independencia.md', tunnel.encode('utf-8'))
config = {
 'source_directories': [
  'COHOMOLOGIA_QUADRATICA_WEYL_081_20260910',
  'REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909',
  'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199',
  'REVISAO_DETECTOR_WEYL_QUADRATICO_081_20260910',
  'INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910',
  'REVISAO_INDEPENDENCIA_RESIDUO_081_20260910_050818_526290',
  'REVISOES_RAIZ_081_20260910', DOC_DIR.name],
 'new_exact_arithmetic_controls': 13,
 'new_source_integrity_controls': 1,
 'new_lean_compilations': 0,
 'status': 'E5_HAS_CLOSED_QUADRATIC_WEYL_REPRESENTATIVES__DELTA_KERNEL_NONZERO__CONSTRUCTED_IMAGE_INDEPENDENT_OF_A6__FULL_CANCELLATION_OPEN',
 'written_results': [
  'Bianchi finite differential factorization gives Hminus1 of the linear jet complex equal to zero, including pointwise coefficient maps.',
  'H3(s0)E5 is represented by natural quadratic Weyl jets times three Killing ghost classes; M remains a quotient, and mixed antifield boundaries are preserved.',
  'The explicit b5=kappa J beta is s0-closed and its odd detector is kappa(24k^3/z0-96k/z0^3), proving a nonzero class in delta(kernel).',
  'Evaluations at k=1/z0 and2/z0 show [A6] and [s1b5] generate a split free rank2 submodule over the fixed nonzero real coefficient algebra; the residual class is outside the line of this candidate.',
  'One exact rational/exterior/character execution has13 algebraic controls plus1 source-integrity control; independent static review, no rerun or Lean.'],
 'remaining': [
  'Determine the full d1 image on quadratic Weyl jet classes; decide minus[A6] membership using the same admissible coefficient domain.',
  'Construct another candidate and a finite primitive of r6+s1Q, or exclude the target for the entire relevant image; matching a detector alone is insufficient.',
  'Actual tower cohomology and comparison, remaining anomaly channels, higher lifts, admissible primitive and causal counterterms.',
  'Interacting current/charge and QME; compatible backgrounds/states/cutoffs; general gravitational reconstruction from the same selected data and ultraviolet justification.',
  'Canonical integration and formal verification of approved constructions and21 absent tracked modules.'],
 'limits': 'Fixed oriented four-dimensional constant-curvature Einstein reference with K>0, constant sigma projected out and inherited inert scalars; no variable restricted K ring, tensor spectators or physical phi=id comparison. Quadratic module not asserted free or finite. Nonzero image and split independence exclude only the constructed candidate line, not the full d1 image. Execution controls are13 algebraic+1 source-integrity; own script has only final execution pin. Weyl geometry is written proof rather than full metric CAS. No Lean, um execution/import, nature test, original/memory modification or gate change. Stage082 excluded.'}
config_pin = emit(OUT / 'CONFIG_ENTREGA_081.json',
 (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'finalizer': finalizer_pin, 'provenance': provenance_pin,
 'adendum': adendum_pin, 'tunnel': tunnel_pin, 'config': config_pin}, ensure_ascii=True))
