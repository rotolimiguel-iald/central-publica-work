from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
ML=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
hf=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=[
(ROOT/'kernel/TGLV350/HilbertProjectionOrder.lean',127,'hilbertBlockB_mul_adjoint; complexGraph_blockA_injective (154)'),
(ROOT/'kernel/TGLV350/ScalarPairedProjectionBlocks.lean',45,'scalarPairedCommutant_mem_GNS; A_injective (82); BBstar (88)'),
(ROOT/'kernel/TGLV350/ScaledPositiveResolvent.lean',26,'scaledResolventDenominator_positive; ring_inverse_commutes_of_unit (48)'),
(ML/'Analysis/SpecialFunctions/ContinuousFunctionalCalculus/PosPart/Basic.lean',41,'CFC.posPart_def; posPart_mul_negPart (58); posPart_sub_negPart (77); posPart_nonneg (142); posPart_eq_zero_iff (198)'),
(ML/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean',172,'IsSelfAdjoint.commute_cfcₙ'),
(ML/'Analysis/CStarAlgebra/Basic.lean',146,'CStarRing.star_mul_self_eq_zero_iff'),
(ML/'Algebra/Order/Star/Basic.lean',197,'star_mul_self_nonneg'),
(ML/'Algebra/Order/Module/Defs.lean',608,'smul_nonpos_of_nonpos_of_nonneg; inv_smul_le_iff_of_pos (885)'),
(ML/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean',304,'CStarAlgebra.isUnit_of_le; IsStrictlyPositive.of_le (402)'),
(ML/'Algebra/Algebra/StrictPositivity.lean',48,'IsStrictlyPositive.iff_of_unital; IsStrictlyPositive.isUnit (56)'),
(ML/'Algebra/GroupWithZero/Units/Basic.lean',100,'Ring.mul_inverse_cancel; Ring.inverse_mul_cancel (104)')]
pins={str(p):{'sha256':hf(p),'line':line,'references':desc} for p,line,desc in refs}
table='\n'.join('| ['+p.name+'](<'+p.as_posix()+':'+str(line)+'>) | '+desc+' |' for p,line,desc in refs)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Consulta — anular a parte positiva e obter inversibilidade do bloco

{now}. **[DERIVED — consulta matemática/API; nenhum código abaixo foi compilado nesta consulta.]** Leituras locais readonly; nenhuma modificação de fonte autoral, memória, monólito ou parecer anterior. Mãe lida `paired_blocks_custody.json`, SHA256 `{hf(ROOT/'paired_blocks_custody.json')}`. Não é revisão DEV nem aprovação de um estágio novo.

A cadeia proposta é válida. Recomendo separar a álgebra do cancelamento injetivo e usar a decomposição positiva/negativa para o único passo CFC. Não é necessário PVM, `[A,B]=0`, inversa prévia de A ou completude do subtipo da álgebra de von Neumann.

## Hipóteses exatas e prova

Trabalhar genericamente em `H →L[ℂ] H`, para H Hilbert complexo completo. Hipóteses suficientes: A auto-adjunto, `Function.Injective A`, `B * star B = A * (1-A)`, c real com `1 ≤ c`; definir `X=1-c • A` e `e=X⁺`. Receber **eB=0 como resultado efetivamente provado na etapa de energia**, não como consequência já disponível deste parecer. As cotas `0≤A≤1` existentes podem ser mantidas, mas o encadeamento abaixo só precisa delas indiretamente para fornecer a auto-adjunção.

1. `X` é auto-adjunto e comuta com A, por ser combinação real de I e A. Por `IsSelfAdjoint.commute_cfcₙ` e `CFC.posPart_def`, **e comuta com A**. `CFC.posPart_nonneg X` fornece e≥0, logo e*=e. Não há comutação com B.

2. Multiplicando **eB=0 à direita por B***, e usando somente eA=Ae:

   `A*(e*(1-A)) = e*(A*(1-A)) = e*(B*B*) = (e*B)*B* = 0`.

   Cancelar A **como função injetiva em cada vetor**, não via `mul_left_cancel` de um anel sem divisores de zero: de `A((e*(1-A))v)=A0` resulta `(e*(1-A))v=0`. Extensionalidade dá `e*(1-A)=0`.

3. `e*(1-A)=e-e*A=0`, portanto **e*A=e**. Até aqui somente associação/distribuição, a comutação especificada e injetividade.

4. Escrever `X=e-X⁻` usando `CFC.posPart_sub_negPart X hX`. Como `e*X⁻=0` (`CFC.posPart_mul_negPart X`):

   `e*e = e*X = e*(1-c • A) = e-c • (e*A) = (1-c) • e`.

   Isso evita uma nova prova de composição CFC ou estimativa de espectro. No Lean, usar igualdade intermediária `X=e-X⁻` e `congrArg (fun Z => e*Z)` evita que um `rw` reescreva também X dentro da definição de e.

5. O membro esquerdo é positivo: `e*e=star e*e≥0`. O direito é não positivo, pois `1-c≤0` e e≥0. Por antissimetria, e²=0, e `CStarRing.star_mul_self_eq_zero_iff e` dá **e=0**. Não dividir por c−1: o argumento inclui **c=1**. A hipótese c≥1 importa: A=I, B=0 e 0<c<1 satisfazem os demais dados com e=(1−c)I≠0.

6. `CFC.posPart_eq_zero_iff X hX` fornece `X≤0`, portanto `I≤c • A`. Como c>0, `inv_smul_le_iff_of_pos` dá **c⁻¹ • I≤A**. Passagem no cone ordenado real de B(H); não existe ordem complexa a usar sobre c.

7. Somente **depois** dessa cota, c⁻¹I é positivo e uma unidade; `IsStrictlyPositive.of_le` fornece `IsStrictlyPositive A`, e `.isUnit` fornece `IsUnit A`. `Ring.inverse A` já tem tipo `H →L[ℂ] H`; as duas identidades de inversa tornam-se legítimas por esse `IsUnit`.

## Esboços Lean locais, não compilados

As assinaturas das APIs abaixo foram lidas; a montagem é uma proposta, não um novo log rc0. Recomendo lemas genéricos no Hilbert abstrato, depois aplicação ao H_I com argumentos explícitos.

```lean
-- Dados intermediários: hEA : Commute e A,
-- hBB : B * star B = A * (1-A), heB : e * B = 0.
have hAz : A * (e * (1-A)) = 0 := by
  calc
    _ = (A * e) * (1-A) := (mul_assoc _ _ _).symm
    _ = (e * A) * (1-A) := by rw [hEA.eq]
    _ = e * (A * (1-A)) := mul_assoc _ _ _
    _ = e * (B * star B) := by rw [hBB]
    _ = (e * B) * star B := (mul_assoc _ _ _).symm
    _ = 0 := by rw [heB, zero_mul]
-- Agora ext1 v; aplicar hAinj à igualdade pontual obtida de hAz.

-- Depois de provar hsquare : e*e = (1-c) • e:
have he0 : 0 ≤ e := CFC.posPart_nonneg X
have heSA : IsSelfAdjoint e := he0.isSelfAdjoint
have hsq0 : 0 ≤ e*e := by
  simpa only [heSA.star_eq] using (star_mul_self_nonneg e)
have hsq1 : e*e ≤ 0 := by
  rw [hsquare]
  exact smul_nonpos_of_nonpos_of_nonneg (sub_nonpos.mpr hc) he0
have hsq : e*e = 0 := le_antisymm hsq1 hsq0
have hezero : e = 0 :=
  (CStarRing.star_mul_self_eq_zero_iff e).mp (by
    simpa only [heSA.star_eq] using hsq)
```

No primeiro `calc`, o rewrite da comutação é apenas a igualdade `e*A=A*e`; pode-se usar `congrArg (fun Z => Z*(1-A)) hEA.eq.symm` se o `rw` escolher ocorrência inconveniente. O código é esboço, não diagnóstico de elaboração já testado.

```lean
-- X = 1-c • A, e=X⁺, hX : IsSelfAdjoint X, hc : 1 ≤ c.
have hcpos : 0 < c := lt_of_lt_of_le zero_lt_one hc
have hle : (1 : H →L[ℂ] H) ≤ c • A :=
  sub_nonpos.mp ((CFC.posPart_eq_zero_iff X hX).mp hezero)
have hbound : c⁻¹ • (1 : H →L[ℂ] H) ≤ A :=
  (inv_smul_le_iff_of_pos hcpos).mpr hle
have hbase : IsStrictlyPositive (c⁻¹ • (1 : H →L[ℂ] H)) := by
  rw [IsStrictlyPositive.iff_of_unital]
  refine ⟨smul_nonneg (inv_pos.mpr hcpos).le zero_le_one, ?_⟩
  rw [← Algebra.algebraMap_eq_smul_one]
  exact (isUnit_iff_ne_zero.mpr (inv_pos.mpr hcpos).ne').map
    (algebraMap ℝ (H →L[ℂ] H))
have hstrict : IsStrictlyPositive A := hbase.of_le hbound
have hunit : IsUnit A := hstrict.isUnit
have hright : A * Ring.inverse A = 1 := Ring.mul_inverse_cancel A hunit
have hleft : Ring.inverse A * A = 1 := Ring.inverse_mul_cancel A hunit
```

A construção de `hbase` reaproveita literalmente o padrão já presente em `scaledResolventDenominator_positive`. Alternativa direta depois da cota: `CStarAlgebra.isUnit_of_le (c⁻¹ • 1) hbound hbase`.

## Interfaces lidas e ressalvas

Imports úteis: `Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.PosPart.Basic`, `Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute`, `Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order`, e a instância de operadores positivos já utilizada por `HilbertProjectionOrder`.

| Arquivo/linha | APIs pertinentes lidas |
|---|---|
{table}

**Cuidado com a totalização:** `CFC.posPart_eq_zero_of_not_isSelfAdjoint` também existe. Por isso a auto-adjunção de X deve estar explícita ao converter e=0 em X≤0; não usar o valor de fallback como prova de ordem. `IsStrictlyPositive` significa aqui **não negativo e invertível**, não mera injetividade/positividade estrita vetor a vetor.

Todo o CFC/inverso é feito no ambiente B(H), que é completo. Se depois for necessária pertinência de `Ring.inverse A` à mesma M, transportar sua comutação com E por `ring_inverse_commutes_of_unit` e aplicar `scalarPairedCommutant_mem_GNS`; isso não requer fabricar `CompleteSpace M`. Essa pertença adicional não é necessária para a conclusão de inversibilidade solicitada.

**Próximo lema concreto proposto [DERIVED]:** sob os dados acima, `(1-c • A)⁺ * B=0` implica `c⁻¹ • I≤A ∧ IsStrictlyPositive A`. A obtenção de eB=0 pela energia variacional, a pertinente escolha e∈M e a instanciação do mesmo bloco continuam obrigações da nova fonte autoral. Nenhuma revisão DEV nova, compilação, inclusão inversa JMJ, KMS ou traço é afirmada aqui.
'''
def new(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
p=REV/'CONSULTA_COTA_BLOCO_POSPART_INVERSIVEL.md'
if p.exists():
    old=p.read_bytes();new(p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')),old)
    b=old+b'\n\n'+text.encode();q=p.with_name(p.name+'.pending');new(q,b);assert p.read_bytes()==old;q.replace(p)
else:new(p,text.encode())
pin={'timestamp':now,'mode':'READONLY_SOURCE_CONSULTATION_NO_LEAN_EXECUTION','report':str(p),'report_sha256':hf(p),'sources_read':pins,'parent_custody_sha256':hf(ROOT/'paired_blocks_custody.json'),'claims_status':'DERIVED_NOT_COMPILED','author_files_modified':False,'memory_writes':False}
new(REV/('consulta_cota_bloco_pospart_pins_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json'),(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'report':str(p),'sha256':hf(p),'bytes':p.stat().st_size,'compiled':False}))
