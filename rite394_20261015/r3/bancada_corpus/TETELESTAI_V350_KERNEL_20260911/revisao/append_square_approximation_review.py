from pathlib import Path
import datetime, hashlib, json, os, re
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'square_approximation_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');hist=load(RUN/'author_history.json')
for k in ['complete','all_exit_zero','exact_9_and_15_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author','inherited_first_binary_preserved','source_snapshots_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved']:assert c[k],k
report=REV/'REVIEW_SQUARE_RESOLVENT_DEV.md';old=report.read_bytes();assert sha(old)==m['readonly_pins'][str(report)]
for p,h in m['readonly_pins'].items():assert hf(p)==h,p
d=m['sources']['TGLV350/ScalarRightSquareApproximation.lean'];raw=Path(d['snapshot']).read_bytes();assert hf(d['path'])==sha(raw)==d['sha256']
new=c['records'][0];audit=c['records'][1]
probe=REV/'difference_squares_probe_20260913_050749_578468'
minimal=load(probe/'MinimalClasses.json');abstract=load(probe/'AbstractSubalgebra.json')
assert minimal['returncode']==1 and abstract['returncode']==0
for name,r in [('MinimalClasses',minimal),('AbstractSubalgebra',abstract)]:
 assert hf(probe/(name+'.lean'))==r['source_sha256'] and hf(probe/(name+'.stdout.txt'))==r['stdout_sha256']
lines=raw.decode().splitlines()
def ln(name):return next(i+1 for i,l in enumerate(lines) if re.match(r'(?:private )?(?:theorem|def) '+re.escape(name)+r'\b',l))
failed=[r for r in hist if r['returncode']!=0 and 'ScalarRightSquareApproximation_' in Path(r['log']).name]
stamp=datetime.datetime.now().astimezone().isoformat();suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
targetrows='\n'.join('- `'+n+'`' for n in d['declarations'])
text=f'''

## Adendo DEV cumulativo 15 = 6 + 9 — {stamp}

SQUARE_RESOLVENT_DEV_REVIEW

[REAL — revisão de fontes e reprodução independente.] **Nenhum P0–P2 identificado no escopo cumulativo de dois módulos/15 alvos.** O estrato dos seis acima permanece byte a byte. Este adendo inclui o arquivo COMPLETO `kernel/TGLV350/ScalarRightSquareApproximation.lean`, inclusive os teoremas de vetor e convergência após a diferença de quadrados. Não é aceite integrado; `ScalarSquareAdjointTest.lean` não foi lido ou compilado nesta ampliação.

**Composição e hipóteses conferidas.**

- Linhas {ln('squareResolvent_mem')} e {ln('squareResolvent_complement_eq')}: em Hilbert complexo completo, A é limitado e recebe `star A = A`. Pertinência A∈N implica R_n∈N; positividade de (n+1)A² é provada. A identidade `(n+1) • (A*(R_n*A)) = I-R_n` usa a inversa positiva e a comutação já demonstrada. Os coeficientes real/complexo são os mesmos e n=0 dá coeficiente 1. Nenhuma inversa de A, lacuna espectral ou injetividade é pressuposta.
- Linhas {ln('scalarRightResolventPair')}–{ln('scalarRightSquareCutoff_commutes')}: para P e a=a* na álgebra não unital E=`scalarPairedRightAlgebra P`, a.val pertence ao comutante da mesma representação GNS. R_n é auto-adjunto, pertence a esse comutante e comuta com a.val. Isso descarrega todas as hipóteses de `scalarSelfadjointRightMultiplier`, produzindo b_n com valor R_n a. Define-se d_n=(n+1)a b_n EM E e só então se identifica seu valor ambiente com I-R_n. Não se assume R_n∈E ou I∈E. A auto-adjunticidade de d_n e sua comutação com a são provadas por igualdade dos valores do subtipo.
- Linhas {ln('scalarRightSquareApproximation')}–{ln('scalarRightSquareApproximation_difference_of_squares')}: c_n=a d_n é auto-adjunto e satisfaz c_n=¼[(a+d_n)²−(a−d_n)²]. O `let d` e o tipo explícito no lado direito nomeiam o MESMO corte; não acrescentam hipótese. O auxiliar algébrico exige somente NonUnitalRing, Module ℂ e a comutação; o auxiliar de subálgebra aplica `Subtype.ext` no Hilbert abstrato. A igualdade é de elementos de E, não apenas de avaliações em um vetor.
- Linhas {ln('scalarRightSquareApproximation_vector')} e {ln('scalarRightSquareApproximation_vector_tendsto')}: a comutação troca a d_n por d_n a, permitindo aplicar exatamente `j(ab)=a.val(j(b))`. Segue j(c_n)=j(a)−R_n j(a). O suporte `j(a)∈closure(Ran a.val)` vem de `ScalarRightFunctionalStability`; o módulo dos seis fornece R_n j(a)→0. O alvo final é convergência em norma no mesmo `ScalarGNSHilbert P`, sem hipótese residual de suporte ou convergência. As escolhas de vetor são as de `scalarRightPairVector`, com sua unicidade herdada; não se troca o peso, P ou representação.

**Evidência própria, distinguida do histórico.** O primeiro módulo conserva a reprodução verde do estrato anterior; não foi recompilado. Nesta chamada:

| Execução nova própria | rc | segundos |
|---|---:|---:|
| ScalarRightSquareApproximation completo, 9 alvos | {new['returncode']} | {new['seconds']} |
| Auditor cumulativo15, `#check` com universos + `#print axioms` | {audit['returncode']} | {audit['seconds']} |

Ambos os mapas de axiomas coincidem exatamente com os respectivos logs finais autorais, exclusivamente `propext`, `Classical.choice`, `Quot.sound`. Os sete auxiliares privados e as três definições novas estão cobertos transitivamente. Fonte sem sorry/admit/axiom novo/unsafe ou alteração de redutibilidade; orçamento final preservado em 200000. O binário próprio do módulo completo é byte a byte igual ao autoral, e o binário próprio herdado do primeiro módulo permaneceu idêntico.

- Fonte nova SHA256: `{d['sha256']}`.
- .olean novo próprio = autoral: `{new['output_sha256']}`.
- Log autoral final `{Path(d['author_log']).name}`: `{d['author_log_sha256']}`.
- Stdout final autoral: `{d['author_stdout_sha256']}`; stderr vazio.
- Auditor15 próprio .olean: `{audit['output_sha256']}`.
- Mãe `bidual_right_support_custody.json`: `{m['parent_custody_sha256']}`.

Artefatos próprios: `{RUN.relative_to(ROOT)}/manifest.json`, `compilation.json` (SHA `{hf(RUN/'compilation.json')}`), `sources/`, `logs/` e `author_history/`. Foram reutilizadas {len(m['dependencies'])} dependências de projeto, com hashes relidos e preservados, provenientes das árvores próprias `square_resolvent_independent_20260913_045003_406702` e `bidual_support_final_independent_20260913_042239_895782`; origens transitivas constam do manifesto. A preparação diagnóstica foi usada apenas como depósito de cópias dessas dependências: NENHUM binário de variante experimental integra a cadeia formal. LEAN_PATH tem uma raiz própria de projeto e oito pacotes externos readonly; {len(m['external_direct_pins'])} pins externos diretos foram relidos. Não se recompilou biblioteca/dependência antiga nem se utilizou build autoral como importação. A auditoria integral dos binários externos permanece herdada, não refeita aqui.

**Histórico e diagnóstico, sem inferir causalidade interna.** Foram preservados e excluídos {len(failed)} rc1 autorais deste segundo módulo, além do rc1 do primeiro já descrito. A lista exata e hashes dos streams estão em `author_history.json`. Prints parcialmente no trio, `sorryAx` ou a mensagem “does not depend on any axioms” dentro de arquivo rc1 não foram aceitos. A única versão autoral aceita do segundo é a fonte final pinada acima.

No diagnóstico próprio `difference_squares_probe_20260913_050749_578468`, retirar isoladamente SMulCommClass/IsScalarTower ainda produziu rc1/whnf ({minimal['seconds']} s). O log autoral `_051211_700682` registra a falha posterior na ponte concreta por rfl. A variante própria de subálgebra abstrata com aplicação direta passou rc0 ({abstract['seconds']} s), mas era um recorte diagnóstico, não o módulo completo. A versão FINAL DO AUTOR com let, tipo explícito e refine direto também passou, agora reproduzida integralmente nesta árvore. Esses resultados NÃO demonstram a causa interna única do gargalo. [DECLARADO pelo agente principal] O auxiliar genérico de subálgebra foi autorado por ele em paralelo antes; nenhuma variante do probe foi copiada após seu resultado. Este parecer não reivindica autoria dessa correção. Nenhum processo autoral foi interrompido pelo revisor.

**Nove novos alvos auditados (os seis anteriores permanecem enumerados no primeiro estrato):**

{targetrows}

**Limite final deste estrato.** Estão conferidas a aplicação racional aos pares auto-adjuntos, a diferença de dois quadrados e a convergência de seus vetores. Não se declara aqui densidade geral de quadrados no gráfico, pertencimento automático de pares ponderados a domínio adjunto, estimativa de multiplicador, inclusão inversa por J, KMS ou traço. Não se confunde diferença/span de quadrados com cone positivo denso. Sem promoção de flags, gate ou runtime. Cópia/gate/mãe e fontes/binários pinados foram apenas lidos e permaneceram iguais durante a execução; não houve reauditoria das 34 memórias, alteração de memórias ou execução de monólito, helpers autorais, recorders, integrações ou controles autorais. DEV15 encerrado, com qualquer módulo posterior e integração fora deste aceite.
'''
b=text.encode('utf-8');backup=report.with_name(report.name+'.bak_'+suffix)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
tmp=report.with_name(report.name+'.tmp_'+suffix)
with tmp.open('xb') as f:f.write(old+b)
assert tmp.read_bytes()==old+b and tmp.stat().st_size>len(old)
os.replace(tmp,report);assert report.read_bytes().startswith(old)
pin={'timestamp':stamp,'report':str(report),'report_sha256':hf(report),'backup':str(backup),'backup_sha256':hf(backup),'preserved_prefix_bytes':len(old),'size':report.stat().st_size,'marker':'SQUARE_RESOLVENT_DEV_REVIEW','scope':'DEV15_ONLY','findings':[],'compilation_sha256':hf(RUN/'compilation.json')}
pp=RUN/'review_pin.json';pt=pp.with_suffix('.json.tmp');assert not pp.exists();pt.write_bytes((json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode());os.replace(pt,pp)
print(json.dumps(pin,ensure_ascii=False))
