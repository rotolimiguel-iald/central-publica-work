from pathlib import Path
from datetime import datetime
import hashlib, json, os

REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'phase_variational_final_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');H=load(RUN/'author_history.json')
assert all(v is True for k,v in C.items() if k!='records')
assert len(C['records'])==2 and len(M['declarations'])==21
assert all(hf(p)==h for p,h in M['readonly_pins'].items())
for row in C['records']:
    assert row['returncode']==0 and row['exact_targets'] and row['axioms_match_author']
    assert hf(row['command'][2])==row['output_sha256']
    assert hf(row['stdout'])==row['stdout_sha256'] and hf(row['stderr'])==row['stderr_sha256']
    assert not Path(row['stderr']).read_bytes()
    assert 'warning:' not in Path(row['stdout']).read_text(encoding='utf-8')
assert len([h for h in H if h['returncode']!=0])==6
draft=load(RUN/'phase_variational_draft_status.json')
assert C['records'][1]['axioms']==draft['targets']
report=REV/'REVIEW_PHASE_VARIATIONAL_DEV.md';old=report.read_bytes()
assert b'PHASE_VARIATIONAL_DEV_REVIEW' not in old
stamp=datetime.now().astimezone().isoformat(timespec='seconds')
tag=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    if p.exists():
        prev=p.read_bytes();bak=p.with_name(p.name+'.bak_'+tag)
        with bak.open('xb') as f:f.write(prev)
        assert bak.read_bytes()==prev
    tmp=p.with_name(p.name+'.tmp_'+tag)
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
V={'timestamp':stamp,'scope':'TWO_DEV_MODULES_21_TARGETS','DEV_review_complete':True,
   'integration_reviewed':False,'P0':[],'P1':[],'P2':[],
   'compilation_sha256':hf(RUN/'compilation.json'),'manifest_sha256':hf(RUN/'manifest.json'),
   'stage_draft_sha256':hf(ROOT/'phase_variational_draft_status.json'),
   'author_report_sha256':hf(ROOT/'RELATORIO_SELECAO_VARIACIONAL_GRAFO_ORIGINAL_DEV.md'),
   'parent_custody_sha256':M['parent_custody_sha256'],'private_helpers_reviewed_transitively':5,
   'independent_new_compiles':['ScalarPhaseVariational','PhaseVariationalAudit21'],
   'inherited_green_compile':M['inherited_real_review'],
   'project_dependencies':len(M['dependencies']),'external_direct_pins':len(M['external_direct_pins']),
   'readonly_pins_preserved':True,'memory_surfaces_rehashed_this_DEV':False,
   'author_failures_excluded':6,'own_setup_attempt_excluded':M['setup_attempt_excluded'],
   'limitations':['weighted_pair_domain_not_proved','bounded_multiplier_not_constructed',
                  'inverse_commutant_KMS_trace_not_proved','package_tree_internals_inherited']}
save(RUN/'verification.json',V)
s=M['sources']['TGLV350/ScalarPhaseVariational.lean']
concrete=C['records'][0];aud=C['records'][1]
tables='\n'.join('| `'+n.rsplit('.',1)[1]+'` | trio |' for n in s['declarations'])
url=lambda p:str(p).replace('\\','/')
text=f'''

---

## Adendo DEV final cumulativo — 21 alvos

{stamp}. **PHASE_VARIATIONAL_DEV_REVIEW**

[REAL — leitura integral, reprodução própria e auditoria de tipos/axiomas.] **Sem P0–P2 nos dois módulos congelados (12+9). Escopo DEV encerrado.** Este adendo preserva o estrato parcial acima e o amplia com ScalarPhaseVariational; a falta de aplicação concreta que constava naquele estrato foi superada somente no alcance descrito abaixo. Nenhuma integração é aprovada neste parecer.

**Pontos substantivos conferidos em ScalarPhaseVariational.lean:**

- **Linhas13–28:** a instância local de completude vem do fechamento do submódulo real Fix S já existente, obtido do gráfico fechado original. Não cria norma, hipótese sobre P ou novo operador. `scalarPhaseVariational` especializa exatamente o CLM real anterior; sua pertinência prova η∈D(S) e Sη=η no mesmo ScalarGNSHilbert P.
- **Linhas30–56:** equação real, unicidade, cota Re(z)‖η‖≤‖ξ‖ e caso z=1 são aplicações diretas dos lemas genéricos. A seleção vale para qualquer ξ do Hilbert e Re(z)>0. Re(z)=1 dá contração; z=1 dá projeção. Não é suposta simetria de B_z.
- **Linhas58–109:** a promoção do pareamento real para complexo exige explicitamente ξ∈D(F) e Fξ=ξ. Para v∈Fix S, o pareamento do adjunto máximo original dá ⟨v,ξ⟩=⟨ξ,v⟩, logo parte imaginária zero. A equação real produz 2⟨ξ,v⟩=z⟨η,v⟩+conj(z)⟨v,η⟩. `fixedComplexFromPairing` recebe hipóteses genéricas, mas a aplicação concreta descarrega-as com v.property, scalarTomitaAdjoint_pairing e a equação variacional; nenhuma ficou como premissa residual.
- **Linhas111–135:** para TODO u∈D(S) original, scalarClosedTomita_fixed_decomposition fornece u=h+ik e Su=h−ik com h,k∈Fix S. A combinação das duas identidades é hh−i·hk, respeitando a conjugação no primeiro argumento. Assim:

  **2⟨ξ,Su⟩ = z⟨η,Su⟩ + conj(z)⟨u,η⟩**, η=scalarPhaseVariational P z hz ξ.

Os tipos/universos foram lidos no auditor. O módulo concreto recebe P:SiteProfile e os objetos originais; os auxiliares privados usam H:Type. A identidade final mantém `hz : 0 < z.re`, `ξ : scalarTomitaAdjointDomain P`, `Fξ=ξ` e `u : scalarClosedTomitaDomain P`. Não exige continuidade de S/F, domínio total em H, hipótese KMS ou pertinência de pares ponderados. Foram lidos os cinco auxiliares privados e auditados transitivamente: fixedPairReal, realPairComplexIdentity, fixedComplexFromPairing, complexRelationFromDecomposition e graphEquationFromFixed. Limites de elaboração da fonte permanecem 200000; fonte final sem sorry/axiom/unsafe ou alteração de redutibilidade.

| Novo alvo — namespace TGLV350.Regular | Auditor próprio |
|---|---|
{tables}

Trio = propext/Classical.choice/Quot.sound, sem outros axiomas. O auditor cumulativo confere **exatamente21 nomes e mapas de axiomas**, iguais ao manifesto e aos streams autorais finais. Os12 nomes anteriores permanecem no estrato preservado.

**Evidência própria:** ScalarPhaseVariational rc0 em **{concrete['seconds']}s**; auditor21 separado rc0 em **{aud['seconds']}s**, ambos sem warnings/stderr. Binário concreto próprio byte a byte igual ao autoral. RealPhaseVariational reutilizado da reprodução própria verde anterior, com fonte/binário relidos; não recompilado redundantemente.

- ScalarPhaseVariational fonte SHA `{s['sha256']}`; .olean próprio/autoral `{concrete['output_sha256']}`.
- Log final autoral ScalarPhaseVariational_20260913_034056_185241.json SHA `{s['author_log_sha256']}`; stdout SHA `{s['author_stdout_sha256']}`. As quatro rc1 `_033206_169218`, `_033422_188089`, `_033608_904818` e `_033838_745756` foram lidas/preservadas e integralmente excluídas, inclusive prints “sem axiomas” e prints verdes parciais. Falhas: coerções/CompleteSpace, nomes derivados ausentes e timeouts whnf/isDefEq. Somadas às duas rc1 do genérico, **seis tentativas autorais rejeitadas**.
- Manifesto autoral phase_variational_draft_status.json SHA `{V['stage_draft_sha256']}`; relatório autoral lido integralmente SHA `{V['author_report_sha256']}`. Texto distingue seleção, identidade em D(S), obrigação dos pares ponderados e multiplicador ainda aberto; sem achado documental.
- Mãe adjoint_polar_graph_custody.json SHA `{M['parent_custody_sha256']}`, conferida com sua verificação e os pins atuais de um.py/gate. Os números209/103/7056 e as seis flags falsas são o estrato integrado da mãe; não constituem integração nem testes destes21. Não houve nova execução de gate, monólito, recorder ou reauditoria das34 memórias.

**Dependências:** {len(M['dependencies'])} módulos de projeto congelados a partir de árvores próprias, com fontes/binários e arquivos acompanhantes conferidos antes/depois; nenhum build autoral de projeto no LEAN_PATH. Origem principal `{Path(M['previous_own_dependencies']).name}`; ScalarTomitaStandardSubspace recuperado da árvore própria `{Path(M['secondary_own_catalog']['run']).name}`, cujos manifestos/compilação também foram pinados. RealPhaseVariational vem de `{Path(M['inherited_real_review']['run']).name}`. O catálogo inicial não continha ScalarTomitaStandardSubspace e parou antes de executar Lean; esse erro de preparação está preservado, resolvido sem aceitar binário autoral ou reconstruir dependências. Oito caminhos de pacotes externos readonly, {len(M['external_direct_pins'])} pins externos diretos/herdados; seus interiores não foram integralmente reconstruídos/re-hasheados. Axiomas transitivos dos21 foram efetivamente auditados nesta execução.

[Compilação própria](<{url(RUN/'compilation.json')}>) — SHA `{V['compilation_sha256']}`; [manifesto/pins](<{url(RUN/'manifest.json')}>); [21 tipos e axiomas](<{url(Path(aud['stdout']))}>); [verificação](<{url(RUN/'verification.json')}>) — SHA `{hf(RUN/'verification.json')}`; [histórico excluído](<{url(RUN/'author_history.json')}>).

[OPEN] O mapa ξ↦η é um operador limitado REAL-linear para Fix S; isso não constrói o multiplicador associado a η. A identidade complexa não demonstra que os pares ponderados pertençam a D(S), nem resolve (V)/(P), invertibilidade do bloco A ou inclusão inversa. A consulta por CFC/quadrados permanece DERIVED e fora destes21. KMS, identificação do fluxo Δ^it, traço/gate/runtime não são promovidos. **Nenhuma análise DEV necessária destes dois módulos permanece pendente; integração futura exige escopo próprio.**
'''
write(report,old+text.encode('utf-8'))
assert report.read_bytes().startswith(old)
save(RUN/'final_review_pin.json',{'timestamp':stamp,'report':str(report),'report_sha256':hf(report),'previous_prefix_sha256':hashlib.sha256(old).hexdigest(),'prefix_preserved':True,'DEV_review_complete':True,'targets':21,'P0':[],'P1':[],'P2':[],'verification_sha256':hf(RUN/'verification.json')})
print(json.dumps({'report':str(report),'report_sha256':hf(report),'marker':'PHASE_VARIATIONAL_DEV_REVIEW','targets':21,'P0':[],'P1':[],'P2':[]}))
