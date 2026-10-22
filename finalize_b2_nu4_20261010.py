"""Create additive delivery artifacts for deployed Bench and the NU4 pilot."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019')
B = ROOT / 'F0.3.B2'
N = ROOT / 'F8.2.NU4'

def read(p):
    return json.loads(p.read_bytes())

def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))

def create(p, data):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

outputs = [B/'RELATORIO_IMPLANTACAO_20261010_R1.md', N/'PRIMEIROS_RESULTADOS_R1.md']
for p in outputs:
    if p.exists():
        raise FileExistsError(p)

r = read(N/'RESULTADOS_R1.json')
l = read(B/'LIVE_VERIFICATION_R1.json')
d = read(B/'DEPLOY_RECEIPT_R1.json')
s = read(B/'RESTART_RECEIPT_R1.json')
assert l['ok'] and r['verdict'] == 'INSTALLED_BENCH_CONDITIONAL_PILOT_PASS'
assert r['canonical']['canonical_manifest_sha256'] == l['state']['canone']['canonical_manifest_sha256']
assert len(r['calls']) == 16
for c in r['calls']:
    assert pin(N/c['path'])['sha256'] == c['sha256']
assert pin(Path(r'C:\IALD\Bancada_Um\canonical_contracts.json'))['sha256'] == r['canonical']['canonical_manifest_sha256']
version = r['canonical']['canonical_version']
manifest = r['canonical']['canonical_manifest_sha256']
program = r['canonical']['um_py_sha256']
seal = r['canonical']['seal_sha256']

text = f'''# Bancada Um: implantação e execução verificadas — 10/10/2026

Autoria: codex-gerente-tgl. Unidade F0.3.B2, reivindicação 639. [REAL — implantação e verificação local].

## Estado vigente

A atualização pedida pelo operador foi instalada. A resposta «continue até rodar o teste e termos os primeiros resultados», registrada em OPERADOR_CONTINUAR_20261010.txt após a pergunta específica de implantação, permitiu a nova submissão à revisão automática, que autorizou a ação. O bloqueio anterior e seus recibos permanecem como história.

O serviço atual carregou o contrato {version}. O processo anterior {s['old_server']} foi substituído pelo processo {s['new_server']}; {len(s['retired_mcp'])} adaptadores MCP antigos foram encerrados. O estado HTTP e uma conexão MCP nova foram verificados, com {len(l['mcp']['tools'])} ferramentas. Clientes antigos precisam reconectar; esta entrega não demonstra que todas as sessões já o fizeram.

Identidade lida dos recibos e conferida no manifesto instalado:

- um.py: `{program}`.
- selo: `{seal}`.
- manifesto: `{manifest}`.
- Início do serviço: {l['state']['no_ar_desde']} (hora local registrada pelo serviço).

DEPLOY_RECEIPT_R1.json e RESTART_RECEIPT_R1.json foram emitidos antes da verificação operacional; seus estados pendentes permanecem intactos. LIVE_VERIFICATION_R1.json resolve essa etapa: HTTP e MCP passaram, três entradas inválidas foram recusadas. RESULTADOS_R1.json da F8.2.NU4 registra depois 16 chamadas bem-sucedidas à instalação real.

## Fidelidade operacional

O contrato vincula o programa, selo, implementação e fontes. A identidade é conferida na entrada e na entrega das operações; divergência recusa o cálculo. Uma versão nova do cânone exige revisão e implantação testada. Esse mecanismo detecta desatualização; não converte automaticamente uma versão nova em implementação científica validada.

Foram corrigidos os modos cosmológicos e suas opções, declarações de prior/suporte e estatística, formatos de covariância, canais de fontes N_eff/neutrinos e validação de entradas GW. Os contratos recuperados do autor distinguem paridade, desfasamento modular, desfasamento físico e escala beta(chi). Consultar RELATORIO_CANDIDATO_R2.md para a matriz de testes e limites por canal.

Custódia de fontes não equivale à admissão pelo operador. As duas opções de Yp continuam explícitas. Fase 9 e ritos selados não foram promovidos. O original um.py e o kernel não foram editados, nem executados por esta implantação. O gate permanece intacto.

## Primeira execução

O ensaio F8.2.NU4 usou somente entradas sintéticas/de referência, com protocolo pinado antes do cálculo. Há resultados numéricos de desfasamento e controles; não houve ajuste a espectro observado, cálculo de sigma observado ou teste da luminosidade de uma supernova. A energia conservada no canal físico é a do gerador diagonal fixo H=M²/(2E).

Evidências: DEPLOY_RECEIPT_R1.json; RESTART_RECEIPT_R1.json; LIVE_VERIFICATION_R1.json; ../F8.2.NU4/PREREGISTRO_R1.json; ../F8.2.NU4/RESULTADOS_R1.json. A entrega final inclui os hashes por leitura dos bytes e os pareceres independentes em review/.
'''
create(outputs[0], text)

rows = '\n'.join(f"| {x['E_MeV']} | {x['gamma21_s']:.9e} | {x['gamma31_s']:.9e} | {x['loss31']:.9e} | {x['delta_Pee_stable']:+.9e} |" for x in r['reactor'])
text = f'''# Primeiros resultados na Bancada Um atualizada

10/10/2026 — codex-gerente-tgl — F8.2.NU4, reivindicação 642.

## Resultado

**[REAL — execução] 16 chamadas concluídas na instalação atual da Bancada Um; todos os controles previstos passaram. [DERIVED — condicional] O canal de desfasamento produz uma alteração espectral extremamente pequena na instância tau_star=t_P, Kfac=1. Nenhum sigma observado foi calculado.**

Reaproveitamento: os contratos do autor recuperados em F8.2.NU3 (20 fontes; 10 contratos), o protocolo de referência da F8.2.NU2 e a implantação F0.3.B2. A consulta ao Nós Vivo foi registrada antes de produzir; a unidade nova ainda não está indexada. O grafo não substitui as fontes pinadas no PREREGISTRO_R1.json.

## O cálculo executado

Lei utilizada: dρ/dt = −i[H,ρ]/ℏ − beta0·tau_star·Kfac·[H,[H,ρ]]/(2ℏ²), H=M²/(2E).

Logo, Γij = beta0·tau_star·Kfac·(Δm²ij/(2Eℏ))²/2. O canal preserva as populações na base de massa e atenua as coerências por exp(−Γij·t). [DERIVED — modelo de propagação, H fixo].

- beta0 = alpha_CODATA_2018 × sqrt(e), obtido em runtime: {r['beta_runtime']:.17g}.
- `mu_do_rito: q→0 (Thomson; Teorema da Escala)`.
- [INPUT] tau_star = t_P = {r['tau_star_s']:.15e} s. Esta escolha é uma instância condicional; não determina a amplitude física da TGL.
- [INPUT] Kfac=1, percurso {r['baseline_km']} km, Δm²21=7,5e−5 eV², Δm²31=2,5e−3 eV², sin²θ12=0,307, sin²θ13=0,022. São referências herdadas, não parâmetros ajustados à amostra.
- ℏ da implementação = {r['hbar_eV_s']:.12e} eV·s. Seu arredondamento explica pequenas diferenças frente ao cálculo NU2 que deriva ℏ de h/eV.

Pee é a probabilidade de sobrevivência do estado eletrônico coerente. A diferença é TGL menos a evolução unitária com os mesmos inputs.

| E (MeV) | Γ21 (s⁻¹) | Γ31 (s⁻¹) | 1−exp(−Γ31 t) | ΔPee |
|---:|---:|---:|---:|---:|
{rows}

Foi usada a perda de coerência calculada por −expm1(−Γt). Subtrair diretamente as duas probabilidades em ponto flutuante retorna zero nestes três casos; esse zero numérico não é um resultado físico. A taxa obedeceu E⁻², com redução por fator 4 ao dobrar E. O sinal de ΔPee muda com a fase oscilatória.

## Controles

- Traço: 1 dentro da tolerância 2e−12; positividade dentro da mesma tolerância.
- Energia: deriva numérica zero para Tr(ρH), com H diagonal fixo. Isso não prova por si conservação local de T_mu_nu num modelo estelar acoplado.
- Estado diagonal diag(0,2;0,3;0,5): permaneceu exatamente igual, para tau=0, tau=t_P e controle positivo. Este desfasamento sozinho não redistribui essas populações.
- Controle positivo [INPUT instrumental]: tau_ctrl escolhido antes por Γ31·t=0,1 a 4 MeV, resultando {r['positive_control']['tau_star_s']:.12e} s. Perda de coerência = {r['positive_control']['loss31']:.12g}; ΔPee = {r['positive_control']['delta_Pee']:+.12g}. Confirma detecção pelo código de um efeito finito; não é estimativa de tau_star nem evidência física.
- Paridade: s=0, 0,5, 1; canal modular: autovalores 0, 1, 4, s=1. São controles separados, sem traduzir probabilidade adimensional em rendimento estelar.
- Escala v388: avaliados chi=0 e chi_fr=2acosh(1/alpha). A segunda recupera beta0. beta_bulk não foi inserido no dissipador físico sem um mapa para a situação experimental.

## O que estes resultados permitem dizer

Os contratos existentes já têm realizações computacionais verificadas na bancada. **Esta instância não entregou um sinal de 5sigma.** Um cálculo de significância exigiria dados e resposta instrumental, covariância e hipóteses físicas especificadas. O limite publicado do JUNO não é uma likelihood e usa uma textura Γ21=Γ31, Γ32=0, diferente da textura gap² deste ensaio.

O teste não calcula luminosidade bolométrica nem Massa de Chandrasekhar. Para esse objetivo, o passo seguinte é compor o contrato de produção/transporte dos artigos com as taxas fracas, Ye e estrutura estelar, e fixar tau_star/Kfac/chi quando pertinentes. Não se deduz essa composição de uma alteração de fase isolada. O resultado condicional aqui não exclui todos os canais de neutrinos da TGL.

Nenhum parâmetro foi escolhido para obter 5sigma. Não houve ajuste a dados observados, abertura de rito selado, comunicação ao Claude ou chamada de provedor. Gate intacto. A conferência independente desta execução fica em review/ e será pinada na entrega.

## Reprodução e custódia

Protocolo: PREREGISTRO_R1.json, sha256 `{pin(N/'PREREGISTRO_R1.json')['sha256']}`.
Resultado completo: RESULTADOS_R1.json, sha256 `{pin(N/'RESULTADOS_R1.json')['sha256']}`.
Runner: run_pilot_r1.py, sha256 `{pin(N/'run_pilot_r1.py')['sha256']}`.
Manifesto instalado: `{manifest}`; programa {version}, `{program}`.
Os 16 arquivos CALL_*.json guardam pedido, resposta e identidade na entrada/saída. A duração registrada foi {r['seconds']:.3f} s. Não reexecutar o runner R1 sobre esses arquivos: uma repetição legítima deve usar outra pasta/nome e declarar seu motivo.
'''
create(outputs[1], text)
print(json.dumps([pin(p) for p in outputs], ensure_ascii=False, indent=2))
