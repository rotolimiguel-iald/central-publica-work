from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'phase_variational_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
m,c,h=load(RUN/'manifest.json'),load(RUN/'compilation.json'),load(RUN/'author_history.json')
assert c['complete'] and all(x is True for x in c.values() if isinstance(x,bool))
assert all(hf(p)==pin for p,pin in m['readonly_pins'].items())
assert len(m['declarations'])==12 and c['records'][-1]['axioms']==m['author_axioms']
assert all(not Path(r['stderr']).read_bytes() and 'warning:' not in Path(r['stdout']).read_text(encoding='utf-8') for r in c['records'])
failed=[x for x in h if x['returncode']];assert len(failed)==2
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def atomic(p,b):
 assert p.resolve().is_relative_to(REV)
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
  with bak.open('xb') as f:f.write(old)
  assert bak.read_bytes()==old;b=old+b'\n\n'+b
 q=p.with_name(p.name+'.tmp_'+stamp)
 with q.open('xb') as f:f.write(b)
 assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
v={'timestamp':date,'complete_for_frozen_module':True,'stage_complete':False,'scope':'RealPhaseVariational: 12 declarations; no concrete module or integration',
   'source_sha256':m['source_sha256'],'own_binary_sha256':c['records'][0]['output_sha256'],'author_final_log_sha256':m['author_final_log_sha256'],
   'parent_custody_sha256':m['parent_custody_sha256'],'compilation_sha256':hf(RUN/'compilation.json'),'manifest_sha256':hf(RUN/'manifest.json'),
   'all_types_with_universes_read':True,'all_axioms_trio':True,'source_read_integrally':True,'LaxMilgram_source_read_integrally':True,
   'excluded_author_rc1':failed,'P0':[],'P1':[],'P2':[],'project_dependencies':0,'packages_rebuilt':False,'monolith_or_author_helpers_executed':False,'memory_written':False}
atomic(RUN/'verification.json',(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
table='\n'.join(f'| `{n.rsplit(".",1)[1]}` | trio |' for n in m['declarations'])
text=f'''# Revisão DEV parcial — seleção variacional de fase

{date}. [REAL — leitura integral e recompilação independente de **RealPhaseVariational.lean, 12 declarações**.] **Sem P0, P1 ou P2 neste módulo congelado.** O exame dos12 está concluído; o estágio permanece parcial, sem manifesto cumulativo e sem módulo concreto aceito neste parecer.

**Semântica/tipos conferidos:**

- **Linhas16–33:** `phaseRealMap` multiplica por conj(z) antes da restrição de escalares. Como o produto interno complexo é conjugado-linear no primeiro argumento, a compressão real produz exatamente **Re(z⟨x,y⟩)**, sem troca de sinal. K é submódulo **real**, e a projeção mantém o contradomínio K mesmo quando K não é estável por escalares complexos.
- **Linhas35–48:** B_z(x,x)=Re(z)‖x‖² prova coercividade com constante Re(z)>0. Nenhuma simetria, positividade complexa de B_z ou novo produto interno foi pressuposto. O caso não real de z está abrangido.
- **Linhas51–82:** a solução é a inversa da equivalência Lax–Milgram aplicada à projeção ortogonal de x. Equação vale para todo x∈H e todo teste v∈K; unicidade é provada entre todos os u∈K que satisfazem essa equação. A hipótese `hu` é a condição de candidato à solução, não uma hipótese residual de existência. Foi relida a implementação Mathlib `IsCoercive.continuousLinearEquivOfBilin`, que não exige simetria.
- **Linhas85–119:** Re(z)‖η‖≤‖x‖ resulta da equação testada em η e Cauchy–Schwarz, incluindo η=0. Re(z)=1 dá contração; **z=1** dá a própria projeção ortogonal. A fonte não afirma que toda fase com Re(z)=1 produza a projeção.

Os tipos do auditor usam H:`Type` (universo0), estrutura de Hilbert complexo e K:`Submodule ℝ H` com `CompleteSpace K`; a completude de H permanece nos teoremas impressos. Não há densidade, standardness ou não trivialidade de K pressuposta. K=0 é caso legítimo. Nenhum SiteProfile, F/S/J, peso ou álgebra concreta entra nestes enunciados.

Precisão sobre o alcance: **o mapa de solução x↦η é de fato um operador limitado real-linear H→K**, já construído como CLM. A cota é desse mapa e de seu vetor de saída. Ela **não** constrói nem limita o multiplicador de álgebra associado a η. Também não prova a identidade complexificada, (V)/(P), invertibilidade do bloco de gráfico ou pertinência a Fix S concreto.

| Nome, namespace TGLV350.Regular | Axiomas próprios |
|---|---|
{table}

“trio” = `propext`, `Classical.choice`, `Quot.sound`, conferido transitivamente nos12 prints. Foram lidos os12 tipos completos com universos. Quatro definições e oito teoremas; nenhum axiom/sorry/admit/unsafe novo ou atributo de redutibilidade introduzido na fonte.

**Reprodução própria:** fonte rc0 em **{c['records'][0]['seconds']}s** e auditor separado12 rc0 em **{c['records'][1]['seconds']}s**, sem warnings/stderr. Binário próprio **byte a byte igual** ao autoral. SHA fonte `{m['source_sha256']}`; .olean `{m['author_binary_sha256']}`. Log autoral final `RealPhaseVariational_20260913_032929_894153.json`, SHA `{m['author_final_log_sha256']}`. Mãe `adjoint_polar_graph_custody.json`, SHA `{m['parent_custody_sha256']}`, conferida por pin/verificação existente, sem reauditoria ampla da custódia.

O módulo importa somente quatro Mathlib: **zero dependências de projeto precisaram ser copiadas/recompiladas**. Reutilizados os oito caminhos de pacotes readonly da árvore própria anterior `{Path(m['previous_own_run']).name}`; {len(m['external_direct_pins'])} pins externos diretos/herdados relidos antes e depois. LEAN_PATH contém somente build próprio e pacotes externos, sem build autoral de projeto. A cadeia interna inteira dos pacotes não foi reconstruída nem integralmente re-hasheada; sua proveniência é herdada, com os imports diretos pinados e axiomas transitivos auditados.

**Duas tentativas autorais rc1 rejeitadas e preservadas:** `_032257_168445` (coerção `starRingEnd`, argumento de `inner_self_im` e rewrite dependente da prova de positividade) e `_032843_186947` (falha de `linarith` no caso Re(z)=1). Seus prints com `sorryAx`, e também os prints verdes parciais, não serviram de evidência de aceite. Apenas os bytes/log final rc0 e a reprodução própria foram aceitos.

{link('Compilação própria',RUN/'compilation.json')} — SHA `{hf(RUN/'compilation.json')}`; {link('manifesto próprio/pins/pacotes',RUN/'manifest.json')}; {link('12 tipos e axiomas',RUN/'logs/PhaseVariationalAudit.stdout.txt')}; {link('verificação e histórico excluído',RUN/'verification.json')} — SHA `{hf(RUN/'verification.json')}`.

[OPEN] Aplicação a Fix S original, passagem à identidade complexa e prova do teste ponderado, multiplicador limitado com adjunto, inclusão inversa, KMS/traço/gate. Não há integração deste módulo certificada aqui. Fontes/binários autorais, mãe, monólito e gate permaneceram iguais aos pins; nenhuma memória ou helper autoral foi executado/alterado. Escritas exclusivamente revisao. **Parecer parcial12 pronto para futura ampliação por adendo, sem antecipar o módulo concreto.**
'''
p=REV/'REVIEW_PHASE_VARIATIONAL_DEV.md';atomic(p,text.encode())
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'module_complete':True,'stage_complete':False,'targets':12,'P0':[],'P1':[],'P2':[],'verification_sha256':hf(RUN/'verification.json')}
atomic(RUN/'partial_review_pin.json',(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(pin,ensure_ascii=False))
