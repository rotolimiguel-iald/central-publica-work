from pathlib import Path
import json,hashlib,datetime,os
ROOT=Path(__file__).resolve().parent
CHAT=ROOT.parents[1]; S=CHAT/'SANEAMENTO_ADENDO_001_012'; OUT=CHAT/'TUNEL/DO_CHATGPT'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
    assert p.is_relative_to(CHAT) and not p.exists() and b
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
seal=load(S/'SELOS.json')
for item in seal.values(): assert pin(Path(item['path']))==item
manifest=load(S/'MANIFESTO.json')
verified=[]
for item in manifest['artifacts']:
    p=Path(item['path'])
    assert p.resolve().is_relative_to(S)
    got=pin(p);assert got['sha256']==item['sha256'] and got['bytes']==item['bytes']
    verified.append(got)
receipts=load(S/'RECIBOS.json')
assert receipts['audited_declarations']==108 and not receipts['axioms_missing'] and not receipts['axioms_outside']
assert set(receipts['axiom_union'])<= {'Classical.choice','Quot.sound','propext'}
assert len(load(S/'CONTROLES_PLANO.json'))==7
errata=load(ROOT/'ERRATA_LACUNAS_A1_REGISTRO.json')
assert pin(Path(errata['before']['path']))==errata['before']
assert pin(Path(errata['after']['path']))==errata['after']
assert Path(errata['after']['path']).read_bytes().startswith(Path(errata['before']['path']).read_bytes())
files=[S/n for n in ['ENTREGA.md','FICHA_SANEAMENTO.md','FICHA_SANEAMENTO.json','PROPOSTA.patch','DELTA_FONTES.json',
    'RECIBOS.json','RECIBO_B.md','RECIBO_C.md','RECIBO_D.md','RECIBO_F.md','binary/RECIBO_G.md','heartbeat/RECIBO_H.md',
    'heartbeat/RESUMO.json','PODA_COROLARIO_PONTUAL.json','MANIFESTO.json','SELOS.json','FALHAS_E_LIMITES.md']]
files += [ROOT/'ERRATA_LACUNAS_A1_REGISTRO.json',Path(errata['after']['path']),Path(errata['before']['path'])]
files += [Path(r['proposal']) for r in load(S/'DELTA_FONTES.json')]
files=list(dict.fromkeys(files))
packet=OUT/'ENTREGA_012_ADENDO001_saneamentos_manifesto.json'
put(packet,json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    status='AUTHOR_SANITATION_DELIVERED_FOR_MANAGEMENT_REVIEW',
    primary_custody_verification_count=len(verified),custody_mismatches=0,
    source=pin(S/'MANIFESTO.json'),files=[pin(p) for p in files],
    items={k:v['status'] for k,v in receipts['items'].items()},
    a_e=errata['requirements_paid'],no_independent_rebuild_by_primary=True,
    limits=['historical heartbeat motives not located remain not recovered',
        'complete causal reconstruction of historical AreaScale binary difference remains open',
        'seven negative controls reject changed applications, not universal propositions'],
    gate_changed=False),ensure_ascii=False,indent=2).encode('utf8'))
text='''[REAL — saneamentos a–h respondidos no escopo abaixo; b/c/d/f/g/h são entrega autoral para auditoria da gerência, sem incorporação]

# ENTREGA 012 — saneamentos do adendo001

| Item | Estado e alcance |
|---|---|
| a — namespace | PAGO documental: TGLV350.Regular identifica os objetos base; V351 nos arquivos identifica a etapa de prova. A renomeação em massa não criaria ponte matemática. A explicação está no adendo a LACUNAS_A1 |
| b — H_nx | PAGO autoral: H_sector_nonexchange e H_singlefluid_continuity distinguem os dois contratos; consumidores atualizados e fecho recompilado |
| c — sete órfãos | PAGO autoral: sete pares com aplicação correta compilada e aplicação adulterada recusada semanticamente; não são sete teoremas de falsidade universal das variantes |
| d — antiunitárias duplicadas | PAGO autoral: preservado fornecedor único e feita importação explícita, com grafo acíclico e dependentes recompilados |
| e — LACUNAS_A1 | PAGO: adendo ao lado com backup imediato em bytes; registra habitante A1, pontes2/3/4 pelos fornecedores efetivos e dispensa da1 pela rota escolhida |
| f — Friedmann aditivo | PAGO autoral: somente tgl_friedmann_from_sector_closure_additive, com uma constante Λ comum, sem hr/he. Corolário pontual sem consumidor podado; seus controles ficaram históricos |
| g — três objetos B6 | PAGO como investigação: diferenças de MixedLadder/SecondCone localizadas; ensaio ABA em AreaScale separa caminho relativo/absoluto. A causa integral do par histórico AreaScale permanece OPEN |
| h — orçamentos | PAGO documental:44 módulos examinados,39 com maxHeartbeats explícito neste snapshot, em contraste com34 citados no adendo. Política atual por módulo: manter configuração aceita sem otimização nesta rodada. Motivo histórico não encontrado permanece NÃO RECUPERADO |

O build cobriu28 módulos, com rc0; após a poda de f foram recompilados o alvo e a auditoria afetada, conservando os resultados anteriores não afetados. Auditoria comum:108 declarações; auditoria B6:25. Todas as listas efetivamente impressas ficaram no trio. Esses números incluem fornecedores antigos, não representam133 teoremas novos. Mathlib e demais dependências não foram reconstruídos integralmente.

A principal leu os enunciados e delimitou a poda e o alcance dos controles; conferiu todos os artefatos do manifesto abaixo. Isso é revisão de fonte e custódia, não uma recompilação independente adicional dos28 módulos. A auditoria de integração é da gerência.

F preserva Λ, mas não determina seu valor. Uma troca apenas de sinal de um testemunho existencial pode ser absorvida por renomeação; não foi vendida como teste de falsidade. Os probes históricos de f fixavam a mesma constante na mesma equação métrica e removiam seu termo; após a poda não participam da validação do alvo geral.

## Reprodução e evidência

RECIBOS.json registra comando, fonte e resultado por item. Nesta máquina, na cópia exclusiva, estes são os roteiros de reprodução com novas pastas de logs:

```powershell
Set-Location -LiteralPath 'C:\\IALD\\Central de Patentes\\Chatgpt\\SANEAMENTO_ADENDO_001_012'
& 'C:\\Python314\\python.exe' -X utf8 -B .\\build_direct.py
& 'C:\\Python314\\python.exe' -X utf8 -B .\\run_checks.py
```

Não repetir prepare/finalize para reproduzir a prova. build_direct recompila o fecho e atualiza apenas o cache isolado da cópia. As falhas Lake amplas, erros iniciais de probes e comparações binárias incompletas estão preservados em FALHAS_E_LIMITES e nos logs; falha de infraestrutura não conta como controle negativo. Nenhum um.py, D1, Atlas, selo canônico ou kernel canônico foi editado. Os documentos de a/e são memórias da bancada dentro de Chatgpt, com backup de bytes.

## Arquivos e hashes lidos nesta transmissão

'''
for p in files:
    r=pin(p);text+=f"- [{p.name}](<{p.as_posix()}>) — SHA256 `{r['sha256']}`.\n"
text+=f"\nConferência de custódia da principal: {len(verified)} artefatos, zero divergências. Manifesto desta transmissão: [{packet.name}](<{packet.as_posix()}>) — SHA256 `{pin(packet)['sha256']}`.\n"
target=OUT/'ENTREGA_012_ADENDO001_saneamentos.md';put(target,text.encode('utf8'))
print(json.dumps(dict(receipt=pin(target),verified=len(verified)),ensure_ascii=False))
