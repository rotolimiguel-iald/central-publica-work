"""Deliver the verified A1 milestone, with b explicitly open and no gate mutation."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def newfile(p,b):
 if isinstance(b,str):b=b.encode('utf-8')
 assert not p.exists(),str(p)
 temp=p.with_name(p.name+'.tmp');temp.write_bytes(b);assert temp.stat().st_size==len(b);temp.replace(p)
audit=json.loads((ROOT/'AUDITORIA_A1.json').read_text(encoding='utf-8'))
assert audit['status']=='PASS_STRICT_MODULE_AUDIT'
source=ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean'
assert sha(source)==audit['source_sha256']
reviews=[p for p in (ROOT/'revisao').glob('REVIEW_A1*.md') if 'PRELIMINAR' not in p.name]
assert reviews,'Final independent review must exist before delivery'
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note=ROOT/'LACUNAS_A1.md';old=note.read_bytes()
newfile(note.with_name(note.name+'.bak_'+stamp),old)
addition=('\n\n## Adendo de execução — '+datetime.datetime.now().isoformat()+'\n\n'
 '[REAL] A compilação final do contrato terminou rc0, sem avisos, com 11 declarações apenas no trio. '
 'A1(a) e A1(c) pagos neste módulo; A1(b) NÃO PAGO. O controle falso 1→2 foi recusado '
 'por elaboração e auditoria. O objetivo continua ativo. Ver AUDITORIA_A1.json e a entrega do marco.\n').encode('utf-8')
temp=note.with_name(note.name+'.tmp');temp.write_bytes(old+addition);assert temp.stat().st_size>len(old);temp.replace(note)
files=[ROOT/n for n in ['REAPROVEITAMENTO_A1.md','REAPROVEITAMENTO_A1.json','ADENDO_REAPROVEITAMENTO_A1.json','LACUNAS_A1.md','AUDITORIA_A1.json','BASE_E_FONTES.json','DEPENDENCIAS_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json','compile_a1.py','copy_dependency_objects.py','audit_a1.py']]+[source]+reviews
files += [Path(audit['accepted_attempt']),Path(audit['accepted_attempt']).parent/'stdout.txt',Path(audit['negative_attempt']),Path(audit['negative_attempt']).parent/'stdout.txt',ROOT/'probes/A1FalseValue.lean',ROOT/'kernel/lean-toolchain',ROOT/'kernel/lake-manifest.json']
files += sorted(ROOT.glob('search_*.txt'))
files += sorted((ROOT/'base_v351').glob('*'))
files += sorted((ROOT/'audits').glob('*.json'))
files += sorted((ROOT/'revisao').glob('*/verification.json'))
files += sorted((ROOT/'revisao').glob('*/compilation.json'))
files += [ROOT/'build/TGLExt/V351RegularCoreTraceContract.olean']
manifest=dict(status='A1_MARCO_PARCIAL_VERIFICADO',time=datetime.datetime.now().isoformat(),goal='ATIVO_A1_B_ABERTO',program_sha256=sha(ROOT/'um.py'),embedded_files_unchanged=922,base_lean_files=918,new_candidate_lean_files=1,negative_fixture_lean_files=1,acceptance=audit['acceptance'],files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in files])
newfile(ROOT/'MANIFESTO_A1.json',json.dumps(manifest,ensure_ascii=False,indent=2))
text='''[REAL — A1 PARCIAL: contrato e recusas compilados; construção do traço canônico ABERTA]

# Entrega 011 · A1 — contrato forte e distinção entre peso dual e traço

Responde à ORDEM_011. A ficha de aproveitamento foi escrita antes do módulo Lean.
Este marco não encerra A1(b), não inicia A2–A7 e não move o gate canônico.

## Resultado exato

`TGLV351.RegularCoreTraceData P` exige, no cone positivo da MESMA
`regularCoreAlgebra P`, valor ENNReal, zero, adição, homogeneidade positiva,
monotonia, fidelidade, normalidade por IsLUB, semifinitude por minorantes positivos
finitos, τ(a*a)=τ(aa*) e escala pela MESMA `regularDualAction P`.

- `legacy_zero_trace_cannot_supply`: qualquer transporte do traço zero legado
  falha nesse contrato. Não supõe identificação inexistente entre álgebras.
- `scalarDualWeight_not_trace_provider`: o peso dual ν não pode fornecer
  diretamente τ. A lei existente ν(θ_s A)=ν(A), aplicada à média quadrática cujo
  valor é exatamente 1, contradiz a escala exigida τ(θ_1 A)=e⁻¹τ(A).
- Os fornecedores do cone, da álgebra, da ação dual, da fidelidade, da
  normalidade, da densidade e da integral da média foram reutilizados.

As recusas são paredes contra dois fornecedores incorretos; não são uma parede
contra a existência do traço canônico. O novo contrato não afirma canonicalidade
pela mera escala: falta construir a perturbação do peso fixado pelo inverso do
gerador e demonstrar suas propriedades.

## Aceitação da ordem

| Critério | Estado | Evidência/limite |
|---|---|---|
| A1(a) contrato fortalecido que recusa o zero legado | PAGO | termo e recusa compilados |
| A1(b) habitante para todo SiteProfile ou impossibilidade tipada | NÃO PAGO | nenhuma das duas alternativas demonstrada |
| A1(c) #print axioms restrito ao trio | PAGO neste módulo | 11 declarações; rc0 sem avisos; auditoria estrita |

`LACUNAS_A1.md` nomeia os antecedentes, tipos matemáticos e conclusões das pontes
restantes: identificação geral do peso dual; sua implementação modular;
gerador positivo afiliado; perturbação de Pedersen–Takesaki com escala dual.
A igualdade do fecho do grafo de Tomita do peso completo já está paga e foi
relocalizada; não voltará a ser cobrada. Os módulos DEV de energia não fornecem
por si esse traço e não foram incorporados.

A ponte posterior a `ThreeLocksCoreData` também deve tratar a diferença entre
o traço no cone positivo e o campo legado `Core → ENNReal`. Não foi fabricado
um adaptador para produtos arbitrários.

## Verificação e falhas preservadas

Lean 4.31.0, pin de mathlib do lake-manifest; 375 pares fonte/objeto importados
conferidos e copiados. Auditoria do módulo: oito controles aprovados. A prova
numérica adulterada 1→2 falhou no Lean, e o auditor a recusou. Relatórios sem
declaração, duplicados, com axioma extra ou rc não zero também são recusados.

Tentativas anteriores foram preservadas: import não localizado; erro de
parênteses com emissão de sorryAx; compilação válida com avisos; primeira sonda
negativa fora da raiz do Lean. Esta última é falha de ambiente e não foi contada
como recusa matemática. A execução aceita e a sonda negativa correta estão
individualizadas em AUDITORIA_A1.json.

O programa copiado permanece byte a byte igual à v351 de entrada. Não se alterou
Python do um.py, nenhum arquivo canônico, experimento, selo, Atlas ou memória
central. A rodada integral anterior não é apresentada como rodada deste módulo;
esta entrega não fez novo runtime integral do monólito.

## Reprodução na bancada existente

```powershell
'''
text += f"Set-Location -LiteralPath '{ROOT}'\n& 'C:\\Python314\\python.exe' -X utf8 -B .\\compile_a1.py\n& 'C:\\Python314\\python.exe' -X utf8 -B .\\compile_a1.py .\\probes\\A1FalseValue.lean\n# A segunda compilação deve retornar código 1 por erro matemático deliberado.\n& 'C:\\Python314\\python.exe' -X utf8 -B .\\audit_a1.py\n```\n\n"
text += '## Artefatos e custódia\n\n'
for p in files:
 text+=f'- [{p.name}](<{p}>) — SHA256 `{sha(p)}`.\n'
text+=f'\n[Manifesto completo](<{ROOT / "MANIFESTO_A1.json"}>) — SHA256 `{sha(ROOT / "MANIFESTO_A1.json")}`.\n'
text+='\n## Ficha de aproveitamento anexada\n\n'+(ROOT/'REAPROVEITAMENTO_A1.md').read_text(encoding='utf-8')
dest=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_011_A1_contrato_forte_e_peso_dual.md'
newfile(dest,text)
print(json.dumps(dict(delivery=str(dest),delivery_sha256=sha(dest),manifest=str(ROOT/'MANIFESTO_A1.json'),acceptance=audit['acceptance']),ensure_ascii=False,indent=2))
