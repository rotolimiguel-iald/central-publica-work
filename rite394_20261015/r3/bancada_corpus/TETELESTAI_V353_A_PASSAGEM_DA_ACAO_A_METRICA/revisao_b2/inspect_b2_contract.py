from pathlib import Path
from datetime import datetime
import hashlib, json, os, re

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=ROOT/'revisao_b2'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def save(p,b):
    if p.exists():
        old=p.read_bytes()
        bp=p.with_name(p.name+'.bak_'+STAMP)
        with bp.open('xb') as f:f.write(old)
        assert bp.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+STAMP)
    with tmp.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    os.replace(tmp,p)

order=ROOT.parent/'TUNEL'/'PARA_CHATGPT'/'ORDEM_012_a_passagem_da_acao_a_metrica.md'
fiche=json.loads((ROOT/'REAPROVEITAMENTO_B2.json').read_bytes())
providers=[]
for item in fiche['providers']:
    p=Path(item['path'])
    data=pin(p)
    lines=p.read_text(encoding='utf-8-sig').splitlines()
    locations=[i+1 for i,line in enumerate(lines) if re.match(r'^\s*(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+'+re.escape(item['name'])+r'\b',line)]
    providers.append(dict(**data,name=item['name'],fiche_line=item['line'],actual_lines=locations,hash_matches=data['sha256']==item['sha256'],line_matches=item['line'] in locations,statement_in_fiche=item['statement'],decision=item['decision']))
checks=dict(all_provider_hashes_match=all(p['hash_matches'] for p in providers),all_provider_locators_match=all(p['line_matches'] for p in providers))
assert all(checks.values()),checks
state=json.loads((OUT/'state.json').read_bytes())
result=dict(timestamp=datetime.now().astimezone().isoformat(),status='PREPARACAO_DE_FORNECEDORES_E_CONTRATO__B2_NAO_ACEITO',P0=[],P1=[],P2=[],findings=[],order=pin(order),fiche=[pin(ROOT/'REAPROVEITAMENTO_B2.md'),pin(ROOT/'REAPROVEITAMENTO_B2.json')],provider_count=len(providers),provider_files=len(set(p['path'] for p in providers)),providers=providers,checks=checks,consumer_scope='Nomes/ligações propostos lidos da ficha; nenhum um.py lido/importado/executado nesta preparação.',proposed_consumers=fiche['proposed_consumers'],build_state_at_read=state,B2_sources_read=False,B2_sources_snapshotted=False,B2_accepted=False,notes=[
    'A assinatura (+---) e as definições de derivada, conexão, Ricci e Einstein foram conferidas nas fontes existentes.',
    'metric_only_einstein_equation recebe abertura/preconexidade, suavidade, LorentzByCongruence, regularidade/simetria de T, balanço nulo e conservação; produz Lambda constante existencial.',
    'As componentes FLRW devem ser resultados sobre geometricEinsteinTensor da mesma métrica e sua inversa/conexão, sem campos que pressuponham as conclusões.',
    'G+Lambda*g=kappa*T implica o sinal -Lambda/3 na equação 00. Nenhuma identificação com Lambda físico foi assumida.',
    'Eta=1/(4G) e G>0 continuam entradas explícitas. O coeficiente 8*pi*G/3 ainda deve ser consumido/provado na especialização.',
    'GeneralMetricClausius é fornecedor alternativo na ficha, não alvo deste build GeneralMetricEinstein.',
    'Preservar hipóteses locais em U e pontos x em U; preconexidade é usada para uma única constante Lambda.',
    'Sem geometria nova aceita, D1, dados, Atlas, integração ou alteração de B1.'
])
save(OUT/'REVIEW_B2_PREPARACAO.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
md=f'''# B2 — preparação independente dos fornecedores

{result['timestamp']}

[REAL — leitura] Ficha B2 MD/JSON e cláusula B2 da ORDEM 012 lidas. {len(providers)} locadores em {result['provider_files']} arquivos de fornecedores conferidos por nome, linha e SHA256; todos coincidem com a ficha. P0/P1/P2: nenhum achado no contrato pretendido. Isto não aceita as fontes FLRW em desenvolvimento.

[DERIVED — exame do contrato] A ficha corresponde ao FLRW plano solicitado: métrica diag(1,-a²,-a²,-a²), calculada pelas definições existentes de derivada, inversa, Levi-Civita, Ricci e Einstein. A aplicação pretendida de `ChatgptAudit.GeneralMetric.metric_only_einstein_equation` preserva balanço nulo e conservação como hipóteses explícitas; não os substitui por componentes Einstein pressupostas. A suavidade/positividade permanecem locais em U. A preconexidade pertence à obtenção de uma única constante cosmológica.

A convenção `G+Lambda*g=kappa*T` dá `H²=kappa*rho/3-Lambda/3`, compatível com o sinal escrito na ficha. `H'=-(pi/eta)(rho+p)` e a equação de aceleração são compatíveis com essa mesma convenção. A avaliação efetiva dessas identidades pela maquinaria Lean continua pendente das fontes finais. `eta=1/(4G)` e `G>0` permanecem INPUT; nenhum valor de beta nem novo parâmetro é introduzido aqui.

O alvo de infraestrutura é somente `lake build TGLExt.GeneralMetricEinstein` em `{ROOT/'s'}`. Foram copiadas suas 88 fontes transitivas, sem FLRWGeometry/FLRWFieldEquations nem objetos TGL/TGLExt. Os pacotes são cópias de bytes do cache privado anterior em `R/r/.lake/packages`, com revisões Git e hashes por arquivo; não há alegação de reconstrução independente de Mathlib. A configuração/toolchain é a mesma, com LEAN_PATH e LEAN_SRC_PATH externos removidos.

[REAL — preparação] Uma primeira falha do preparador próprio (`utf8-sig`, nome de encoding inválido) foi preservada e corrigida em script novo. A preparação posterior ficou sem processo vivo antes de iniciar Lake; foram encontrados 88 fontes e parte do cache, sem diretório de objetos de projeto. A retomada verifica os bytes já presentes e preserva o estado anterior. Nenhum desses eventos é recusa matemática de B2.

[OPEN — nesta leitura] Estado registrado: `{state['status']}`. Os resultados de Lake devem ser lidos no run.json próprio quando emitido; esta nota não antecipa rc0. Nenhum snapshot final ou aprovação de B2, nenhuma integração. R/r, relatórios/pins B1 e código autoral permanecem somente leitura. Não foram lidos/executados um.py, dados ou Atlas.

Evidência: [REVIEW_B2_PREPARACAO.json]({OUT/'REVIEW_B2_PREPARACAO.json'}), com hashes da ordem/ficha e fornecedores. Os consumidores são os nomes propostos na ficha; sua instalação no mapa não foi verificada nesta preparação.
'''
save(OUT/'REVIEW_B2_PREPARACAO.md',md.encode('utf8'))
print(json.dumps(dict(checks=checks,provider_count=len(providers),provider_files=result['provider_files'],report=pin(OUT/'REVIEW_B2_PREPARACAO.md'),evidence=pin(OUT/'REVIEW_B2_PREPARACAO.json')),ensure_ascii=False,indent=2))
