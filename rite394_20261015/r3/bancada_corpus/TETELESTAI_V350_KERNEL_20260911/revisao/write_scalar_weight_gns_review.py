"""Create the completed DEV review atomically; write exclusively below revisao."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');V=load(RUN/'verification_dev.json')
assert all(v for k,v in C.items() if isinstance(v,bool))
assert V['all_60_types_printed'] and V['all_9_own_binaries_byte_equal_author']
assert all(hf(s['path'])==s['sha256'] for s in M['sources'].values())
assert all(hf(p)==h for p,h in M['previous_reviews'].items())
assert hf(ROOT/'scalar_weight_gns_draft_status.json')==M['draft_status_sha256']
assert hf(ROOT/'RELATORIO_GNS_PESO_COMPLETO_DEV.md')==M['report_sha256']
assert hf(ROOT/'um.py')==M['initial_um_sha256']
def link(label,p,line=None):
    target=Path(p).as_posix()+((':'+str(line)) if line else '')
    return f'[{label}](<{target}>)'
def source(name,line):return link(name+'.lean:'+str(line),ROOT/'kernel/TGLV350'/(name+'.lean'),line)
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
audit=C['records'][-1]
rows=[]
for rel,s in M['sources'].items():
    r=next(r for r in C['records'] if r['module']==rel)
    rows.append(f"| {link(Path(rel).stem,s['path'])} | {len(r['axioms'])} | `rc0` / {r['seconds']:.3f}s | `{s['sha256']}` | `{r['output_sha256']}` |")
history=[]
for h in load(RUN/'author_history.json'):
    if not h['accepted_final']:
        history.append(f"- {Path(h['log']).name}: rc{h['returncode']}; excluído da aceitação final.")
text=f'''SCALAR_WEIGHT_GNS_DEV_REVIEW

{stamp} — revisão adversarial independente, exclusivamente DEV, nove módulos / 60 alvos.

**Conclusão: nenhum achado P0, P1 ou P2 no escopo examinado.** [REAL — recompilação própria] As nove fontes e o auditor de 60 tipos/axiomas passaram com rc0. Os nove binários próprios coincidem **byte a byte** com os binários finais do autor. As fontes e o relatório foram lidos integralmente; a inspeção das provas, das hipóteses e da composição sustenta a identificação do completamento GNS do domínio escalar e do fecho de seu gráfico involutivo com os objetos anteriores, no mesmo H_I. Não resta análise DEV necessária neste pacote.

**Alcance matemático conferido.** Escrevo N=regularCoreAlgebra P, Ω=regularVacuum P, c=dualHaarFactor=(2π)⁻¹, I=finiteDualLeftIdeal P e n_ν=scalarWeightLeftIdeal P. Estas são as definições efetivamente usadas, não objetos homônimos introduzidos pelo parecer.

- {source('ScalarWeightDomain',14)}: n_ν é a finitude de q_(A* A)(Ω), que coincide por definição com a avaliação do peso escalar já construído. As leis de soma, escala complexa e produto à esquerda controlam quadrados positivos; não exigem A positivo. O submódulo é um ideal à esquerda de N pela lei adicional explícita. {source('ScalarWeightDomain',50)} prova I⊆n_ν; não há igualdade de ideais como hipótese ou conclusão.
- {source('ScalarWeightOrbit',13)}: a finitude escalar e c>0 dão MemLp 2 da órbita s↦θ_s(A)Ω. A definição na linha 37 usa √c e a mesma medida de Lebesgue no mesmo L² ambiente, RegularHilbert (RegularHilbert (TowerHilbert P)). As identidades de norma ENNReal e real respeitam esse fator. A passagem à integral real usa a integrabilidade obtida de MemLp, sem extrair valor real de uma integral infinita. A linearidade complexa é igualdade em L², com interseções AE finitas; a injetividade recebe a fidelidade escalar anterior em N sobre A* A. Na linha 122 a inscrição sobre I coincide literalmente com scalarGNSOrbit.
- {source('ShiftCharacterAverage',13)} e {source('ScalarRightAverage',14)}: a família integra **vetores** por Bochner; o operador limitado resultante não presume integrabilidade em norma de B(H). A fase é characterPhase s t=exp(-i s t), e θ_s(Aλ_t)Ω=exp(-i s t) shift_t(θ_s(A)Ω) usa λ_tΩ=shift_tΩ e shift_t∈N′, com θ_s(A)∈N. A cota de contração vale inclusive h=0; a convergência é forte, em cada vetor, para h→0 puncturado. Nenhuma convergência em norma de operador é afirmada. A pertinência A X_h∈I recebe explicitamente h>0 ({source('ScalarRightAverage',87)}).
- {source('ScalarWeightCompletion',16)}: o erro quadrático é dominado por 4‖θ_s(A)Ω‖², integrável porque A∈n_ν. O DCT Mathlib usado requer filtro de base enumerável, satisfeito pelo filtro real puncturado aqui; o teorema deste módulo não promete DCT em filtros arbitrários. As funções contínuas explícitas fornecem as hipóteses AE sem interseção não enumerável de representantes L². A restrição h>0 é usada com filtro não trivial para obter pertença ao fecho de I. {source('ScalarWeightCompletion',79)} identifica exatamente o fecho da imagem de scalarWeightLinear com scalarGNSSubspace P, e codRestrict coloca a inscrição completa no H_I anterior.
- {source('ScalarWeightAction',20)}: a ação ambiente é a mesma dualOrbitRepresentation e sua restrição é a mesma scalarGNSRepresentation P. O entrelaçamento é π(B)Λ_ν(A)=Λ_ν(BA), para B∈N e A∈n_ν; as coerções preservam esses objetos. Norma, injetividade e DenseRange justificam a realização do completamento do domínio escalar no H_I já completo. Não se presume que a imagem algébrica seja todo H_I.
- {source('ScalarWeightSandwich',14)}: o sanduíche é efetivamente X_h* A X_h. Seu limite GNS combina a aproximação pela direita com π(X_h*) e a estimativa de aplicação a vetor variável uniformemente limitada. A convergência forte de X_h* vem do lema anterior para **contrações convergindo a I**; não há uso de continuidade SOT geral da operação star. O transporte forte limitado da representação é dependência anterior, não hipótese nova de normalidade/KMS nem conclusão usada circularmente.
- {source('ScalarWeightStarCore',14)} define o domínio involutivo algébrico n_ν∩n_ν* como subálgebra sem unidade, com ambas as finitudes explícitas. A inclusão do núcleo anterior respeita estrela e inscrição. {source('ScalarWeightTomitaIdentification',25)} aproxima as duas coordenadas pelo **mesmo h>0**, aplicando a convergência a A e a A* e a igualdade exata (X_h* A X_h)*=X_h* A* X_h. Daí o gráfico completo fica no fecho do gráfico anterior. A inclusão inversa já segue de I⊆n_ν. Nas linhas 50 e 58 são provadas as igualdades de **fechos**, inclusive com o gráfico do S fechado original; nas linhas 65 e 71, Λ_ν(A)∈D(S) e SΛ_ν(A)=Λ_ν(A*) para todo A∈n_ν∩n_ν*. Não há redefinição de S ou substituição de H_I.

**Hipóteses e não circularidade.** Os enunciados concretos recebem P:SiteProfile e as pertinências/finitudes indicadas, sem hipótese nova sobre P, KMS, igualdade I=n_ν, densidade suposta do novo domínio ou igualdade prévia de gráficos. O auxiliar de médias usa o Hilbert complexo genérico H:Type e suas instâncias usuais. Os 60 tipos foram impressos com universos e lidos; não há promessa adicional de generalidade de universo além desses tipos. O DAG congelado tem {V['project_import_graph_modules']} módulos de projeto, é acíclico, e nenhuma dependência antiga importa os nove novos. A fidelidade, os limites fortes limitados de π, a aproximação uniforme e a fechabilidade/univalência do gráfico antigo são resultados herdados explicitamente utilizados. Não foram reconstruídos nesta rodada.

**Recompilação independente e proveniência.** Árvore própria: {link(RUN.name,RUN)}. Foram executados somente nove compilações na ordem do manifesto e um auditor novo, total 10 processos Lean rc0; auditor: {audit['seconds']:.3f}s. Os 60 alvos são exatamente todos os nomes impressos nas nove fontes, sem auxiliares nomeados omitidos, e todos dependem exatamente de propext, Classical.choice e Quot.sound. Nenhum axiom/sorry/admit/unsafe, alteração de redutibilidade ou nova instância local foi encontrado. Os únicos avisos finais são duas depreciações de nomes Mathlib: ShiftCharacterAverage:59 e ScalarWeightSandwich:45, sem efeito no enunciado/prova.

Lean: `{M['lean_version']}`; SHA256 do executável `{M['compiler_sha256']}`. O LEAN_PATH contém apenas o build desta árvore e oito caminhos readonly de pacotes; nenhum build autoral de projeto ou build canônico de projeto. Reutilizei {len(M['dependencies'])} pares fonte/binário próprios pinados do catálogo anterior. Duas dependências ausentes no catálogo imediato foram recuperadas das revisões próprias modular_domain_independent_20260912_064113_846118 (ScalarModularInvariance) e gns_normality_independent_20260912_081001_179488 (ScalarGNSStrongContinuity), com hashes de manifesto, compilation, fonte e binário relidos. A preparação inicial parou antes de qualquer compilação ao detectar essa lacuna; não foi contornada com build autoral. A única diferença herdada em relação à fonte autoral viva é a errata **somente de comentário** de DualSemifiniteIdeal, já revisada e conferida por substituição literal; a cópia congelada preserva o estrato anterior. Pacotes e dependências não foram recompilados; sua validação é herdada e os pins foram reconferidos.

**Pins das nove fontes e comparação binária.** SHA256 lidos por script. Em todas as linhas, o hash .olean abaixo é simultaneamente o binário próprio e o final autoral, com comparação direta de bytes além do hash.

| Módulo DEV | Alvos | Compilação própria | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---:|---|---|---|
{chr(10).join(rows)}

Os caminhos dos logs finais autorais, hashes de seus JSON/stdout, fontes congeladas, dependências e origens estão em {link('manifest.json',RUN/'manifest.json')} (SHA256 `{hf(RUN/'manifest.json')}`), no manifesto autoral congelado e em {link('verification_dev.json',RUN/'verification_dev.json')} (SHA256 `{hf(RUN/'verification_dev.json')}`). Os dez comandos próprios, rc0, tempos, hashes de stdout/stderr e .olean e mapas de axiomas estão em {link('compilation.json',RUN/'compilation.json')} (SHA256 `{hf(RUN/'compilation.json')}`). Auditor próprio: {link('fonte #check/#print',RUN/'sources/ScalarWeightGNSAudit.lean')} (SHA256 `{hf(RUN/'sources/ScalarWeightGNSAudit.lean')}`) e {link('saída integral dos 60 tipos/axiomas',audit['stdout'])} (SHA256 `{audit['stdout_sha256']}`). Não é mera releitura dos rc0 autorais.

**Histórico preservado.** {link('author_history.json',RUN/'author_history.json')} e os streams congelados conservam 14 tentativas: nove rc0 finais aceitos, quatro rc1 excluídos e um rc0 substituído. As falhas antigas de elaboração/simplificação/timeout não foram promovidas a prova nem tratadas como defeitos pendentes das fontes finais. O rc0 anterior de ShiftCharacterAverage tinha fonte anterior à adição do sexto alvo.

{chr(10).join(history)}

**Manifesto, documentação e fronteira.** Li integralmente {link('RELATORIO_GNS_PESO_COMPLETO_DEV.md',ROOT/'RELATORIO_GNS_PESO_COMPLETO_DEV.md')} e {link('scalar_weight_gns_draft_status.json',ROOT/'scalar_weight_gns_draft_status.json')}. Seus SHA256 relidos são, respectivamente, `{M['report_sha256']}` e `{M['draft_status_sha256']}`. Contagem, ordem, 60 alvos, fonte/log/binário final e axiomas conferem; a redação distingue completamento e fecho de gráfico de igualdade de ideais ou de domínio algébrico. Não identifiquei P2 documental.

A mãe integrada é tomita_involution_custody.json, SHA256 `{V['custody_sha256']}`; sua verificação relida tem SHA256 `{V['custody_verification_sha256']}`. A cópia permanece `{V['working_sha256']}`; original readonly relido `{V['original_sha256']}`. Nenhum dos 60 novos alvos está no Audit integrado corrente. Gate_extension permanece byte a byte no pin materno `{V['gate_extension_sha256']}`; as seis flags maiores estão false na evidência relida, com legacy_gate_changed=false, full_plan_complete=false e full_monolithic_runtime_run=false nos registros anteriores. Esses registros são **herança de integração**, não novos testes executados nem integração deste pacote. Não houve execução/importação do monólito, recorders, testes autorais ou scripts de integração; todas as escritas desta revisão ficaram em revisao, e os pareceres anteriores foram reconferidos intactos.

**Limites.** [REAL — neste DEV] está identificada a realização GNS do domínio de finitude escalar completo e o fecho de seu gráfico de estrela com H_I e S anteriores. Não se provou I=n_ν, sobrejetividade algébrica de Λ_ν, nem D(S)=Λ_ν(n_ν∩n_ν*); não são premissas residuais exigidas por estas provas. [OPEN — fora do pacote] identificação do fluxo modular com o candidato, KMS, traço canônico/escala dual/canto Three Locks, obrigações físicas e consumo por certificado/runtime. Não há promoção de gate, QG ou identificação automática com outro operador chamado J. O parecer encerra este escopo DEV; eventual integração exige conferência própria posterior.
'''
dest=REV/'REVIEW_SCALAR_WEIGHT_GNS.md';assert not dest.exists(), 'New report expected; sealed reviews must remain untouched.'
data=text.encode('utf-8');tmp=dest.with_name(dest.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data and len(data)>10000;tmp.replace(dest)
assert dest.read_bytes()==data
closure={'timestamp':stamp,'report':str(dest),'sha256':hf(dest),'bytes':len(data),'lines':len(text.splitlines()),
 'findings_P0':0,'findings_P1':0,'findings_P2':0,'remaining_DEV_analysis':False,
 'compilation_sha256':hf(RUN/'compilation.json'),'verification_sha256':hf(RUN/'verification_dev.json')}
p=RUN/'closure_dev.json';assert not p.exists();q=p.with_name(p.name+'.tmp');raw=json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8')
with q.open('xb') as f:f.write(raw)
assert q.read_bytes()==raw;q.replace(p)
print(json.dumps(closure,ensure_ascii=False,indent=2))
