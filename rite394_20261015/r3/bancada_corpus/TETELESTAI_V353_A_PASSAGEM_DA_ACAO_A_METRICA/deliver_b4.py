from pathlib import Path
import datetime, hashlib, json, os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B4_rotas_termodinamicas_e_diferenca.md'
def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) or p==OUT
    assert not p.exists(),p
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
a=load(R/'AUDITORIA_B4.json');v=load(R/'revisao_b4/REVIEW_B4_FINAL.json')
assert v['status']=='B4_DEV_REVIEW_ACCEPTED_WITH_EXPLICIT_CONTRACT_CORRECTIONS__INTEGRATION_NOT_REVIEWED'
assert not v['literal_original_contract_certified'] and all(not v[k] for k in ['P0','P1','P2'])
c=load(Path(v['compilation']['path']))
assert a['all_trio'] and a['negative_controls_rejected'] and c['all_accepted_builds_exit_zero']
assert c['all_axioms_allowed'] and not c['author_project_objects_copied'] and not c['new_warnings']
assert c['exact_target_count']==len(a['targets'])==28 and load(Path(v['run']['path']))['returncode']==0
files=set()
def accept(x):
    if isinstance(x,dict):
        if {'path','bytes','sha256'}<=x.keys():
            p=Path(x['path']);assert pin(p)=={k:x[k] for k in ['path','bytes','sha256']},p;files.add(p)
        for y in x.values():accept(y)
    elif isinstance(x,list):
        for y in x:accept(y)
accept(a);accept(v);accept(c)
for x in v['new_source_object_pins']:
    if x['author'] is not None:assert x['equal_to_author']
main=[Path(x['path']) for x in a['sources']]+[R/x for x in ['REAPROVEITAMENTO_B4.md','REAPROVEITAMENTO_B4.json','AUDITORIA_B4.json','ALVOS_B4.json','BUSCAS_B4_GRUPOS.json','revisao_b4/REVIEW_B4_FINAL.md','revisao_b4/REVIEW_B4_FINAL.json','revisao_b4/compilation.json','run_b4_lake.py','audit_b4.py','prepare_b4_ficha.py','prepare_b4_audit.py','deliver_b4.py']]
files.update(main)
for folder in ['audit_B4','probes_B4','searches_B4']:
    files.update(p for p in (R/folder).rglob('*') if p.is_file())
attempts=[]
for p in sorted((R/'attempts').glob('*/run.json')):
    if p.parent.name>'20260914_165527_813445':continue
    x=load(p)
    if any(any(n in str(s) for n in ['ThermodynamicFriedmann','SectorRouteComparison','AuditThermodynamics']) for s in x['command']):
        attempts.append(dict(directory=str(p.parent),returncode=x['returncode'],command=x['command']))
        files.update(q for q in p.parent.rglob('*') if q.is_file())
stamp=datetime.datetime.now().astimezone().isoformat()
ax='\n'.join(f"| `{k}` | {', '.join(w) or 'nenhum'} |" for k,w in a['axioms'].items())
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
body=f'''[REAL — B4 entregue com teoremas condicionais e paredes que corrigem quatro enunciados do contrato original. Contrato literal NÃO certificado; nenhuma rota escolhida.]

# ENTREGA 012 / B4 — rota termodinâmica, diferença e fator de fluxo

{stamp}

**22 teoremas, cinco definições e uma estrutura** foram compilados e reproduzidos por revisão independente. A revisão aceitou o resultado matemático com as correções obrigatórias abaixo. Não se atribui à literatura a entropia modificada da TGL; ela entra como hipótese nomeada.

## Critérios pagos e correções obrigatórias

| Critério | Estado e alcance |
|---|---|
| Ficha antes do código, fornecedores e seis modalidades de busca | PAGO; ficha integral ao final, MD/JSON preservados e 13 fornecedores conferidos. Buscas por variância também encontram invariância: esses homônimos não foram tratados como ponte. |
| Derivada real de A=4π/H² e Clausius | PAGO; hubble_area_derivative e HubbleHorizonInput, com H>0, G>0, Φ>0. A segunda equação não é campo dessa estrutura. |
| Segunda equação Ḣ=−4πGΦ(ρ+p) | PAGO para fluxo **A(ρ+p)H r_A**, r_A=1/H. **NÃO PAGO na escrita literal sem r_A**: radius_free_flux_consequence prova o fator H extra. |
| Entropia modificada | PAGO como entrada diferencial dS=dA/(4GΦ). **NÃO se identifica automaticamente com a derivada de S=A/(4GΦ(t))**; variable_entropy_derivative prova o termo adicional −AΦ'/(4GΦ²). |
| Primeira equação, w constante | PAGO: H²=(8πG/3)Φρ+C, com continuidade e C explícito. Não prova C=0. |
| Primeira equação, Φ variável | PAGO sob primitiva fornecida com derivada Φρ'; não se prova existência de uma primitiva para função arbitrária. H²=(8πG/3)P+C. O produto Φρ tem defeito de derivada −(8πG/3)Φ'ρ. |
| Diferença entre rotas | PAGO: diferença das fontes = β·variância≥0. Diferença de Ḣ = **−4πG** vezes essa expressão. |
| Critério de igualdade | PAGO com **suporte ρ_i>0**, incluindo vácuo. **Critério literal ρ_i+p_i≠0 é refutado** por um exemplo Fin2 matéria+vácuo. |
| Fator reconciliador único | PAGO com **entalpia total E≠0**. No fluxo zero zero_flux_has_no_unique_factor prova ¬∃! fator. |
| Fator comum quando w constante | PAGO sob suporte de densidade comum, E≠0 e 1+w≥0; a última hipótese permite a leitura absoluta. |
| Revisão e axiomas | PAGO DEV: 28 alvos no trio; Lake próprio rc0; sem P0–P2 ou avisos novos. Aceite de integração permanece com a gerência. |

## Cadeia e tipagem das entradas

HubbleHorizonInput contém H positivo/diferenciável, G/Φ positivos, taxa de entropia, taxa de calor, **differential_entropy**, **enthalpy_flux** e **clausius**. Usa calor com orientação δQ=−dE. Com T=H/(2π), r_A=1/H, a taxa de calor é A(ρ+p). A álgebra e a derivada de A produzem Ḣ=−4πGΦ(ρ+p); o coeficiente reutiliza einstein_coefficient_from_clausius.

O raio é parte da prescrição primária de [Cai–Kim, eq. 2.12](https://arxiv.org/html/hep-th/0501055). A correção diferencial Φ_TGL é INPUT da construção. Sua identificação com uma entropia de estado variável exigiria controlar o termo Φ' ou introduzir uma lei adicional explicitamente — nenhuma foi presumida. O fato de a primeira lei valer sob essas entradas não constrói H3 para a realização microscópica.

Para setores de B3, escreva R=Σρ_i, E=Σ(1+w_i)ρ_i e M₂=Σ(1+w_i)²ρ_i. Sob R>0 e E≥0:

```text
fonte setorial = E + β M₂
fonte total = (1+β|1+w_eff|)E = E + β E²/R
diferença = β(M₂−E²/R)
variância = Σρ_i[(1+w_i)−E/R]² ≥ 0
```

A diferença é zero exatamente quando todos os w_i de densidade positiva coincidem. Dois setores com ρ_m>0 e ρ_Λ>0, w_m=0 e w_Λ=−1, têm só um setor de fluxo não nulo, mas variância **ρ_mρ_Λ/(ρ_m+ρ_Λ)>0**. Esse contraexemplo tipado impede a implementação do critério incorreto da ordem.

Se E≠0, a solução única de fator·E=E+βM₂ é Φ_flux=1+βM₂/E. sector_clausius_matches_closed_rate aplica o teorema termodinâmico a esse fator e recupera a taxa setorial. Se E=0, ou nenhuma solução existe ou todos os fatores resolvem; não há unicidade. Estes resultados não escolhem a lei a usar no D1.

A integração usa intervalos/domínios abertos preconexos e a constância obtida de derivada zero. Sob w constante, a primitiva escolhida é Φρ. A constante C sobrevive; B3 também mantém Λ na equação 00 e exige H_zero_cosmological para eliminá-lo. **A hipótese de não-troca H_nx e w_i constante permanece de B3.** Escala G/η INPUT, Lema3 global OPEN, fechamento perturbativo TGL-S/TGL-L OPEN.

## Reprodução, controles e tentativas

Na bancada `{R}`, o runner pinado run_b4_lake.py invoca `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics` na raiz kernel. Run final: `{a['positive_build']['path']}`, rc0, fontes idênticas antes/depois. O auditor executa `lake env lean` no auditor e nas duas sondas: BadThermodynamicFactor omite Φ; BadVarianceSign troca o sinal da variância. Ambas falham por Type mismatch com imports funcionando.

Reprodução independente: `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics TGLExt.ReviewThermodynamics` em s, run `{v['run']['path']}`. Quatro objetos próprios novos; 113 objetos próprios anteriores preservados, 117 no total. Os três objetos do candidato coincidem com os autorais. **Nenhum olean de projeto autoral foi copiado.** Mathlib e oito pacotes auxiliares são caches herdados/pinados; não se alega recompilação desses componentes.

O revisor executou tipos e axiomas próprios e leu fontes/sondas autorais; não repetiu os negativos nem a varredura completa das 941 fontes-base. Esta preservação e a do um.py copiado foram medidas pelo auditor autoral, distinguindo os dois escopos. A revisão verificou o papel do raio em Cai–Kim. O inteiro original e o kernel canônico não foram executados ou escritos.

Tentativas intermediárias preservadas: provas de positividade, normalização da potência pontual e tática após meta fechada; builds positivos com avisos de ring/sum_mul dispensáveis foram substituídos pelo build final sem avisos novos. Todos os runs e snapshots pertinentes estão no manifesto. Falhas não foram apagadas nem contadas como controles adversariais.

## Axiomas medidos, nomes completos

| Alvo | Axiomas |
|---|---|
{ax}

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
{table}

MANIFESTO_B4 e RECIBO_B4 na bancada vinculam os objetos, fontes, runs e revisão. A gerência integra os consumidores ext_* propostos na ficha **com estas correções**, sem remover hipóteses. Não foram alterados D1, gate, protocolos, originais, Atlas ou memórias; nenhuma escolha empírica foi feita.

## Ficha integral

'''+(R/'REAPROVEITAMENTO_B4.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
m=dict(timestamp=stamp,status='B4_DELIVERED_WITH_CONTRACT_CORRECTIONS__INTEGRATION_PENDING',literal_original_contract_certified=False,attempts=attempts,files=[pin(p) for p in sorted(files,key=str)])
put(R/'MANIFESTO_B4.json',json.dumps(m,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B4.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B4.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in m['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B4.json'),files=len(files)),ensure_ascii=False))
