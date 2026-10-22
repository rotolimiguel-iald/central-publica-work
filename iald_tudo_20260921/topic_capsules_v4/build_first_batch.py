"""Offline construction: compact only the three loaded candidate blocks."""
import hashlib
import json
import os
from pathlib import Path
import re
import socket

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
SOURCE = WORK / 'haiku_reviewed_section_20260922_130747_311801.md'
os.environ['TIKTOKEN_CACHE_DIR'] = r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache'
def deny_network(*args, **kwargs):
    raise RuntimeError('Network prohibited in local measurement')
socket.socket = deny_network
import tiktoken
ENC = tiktoken.get_encoding('o200k_base')

DRAFTS = {
'cocycle_to_einstein': '''[REAL: E1–E6, tipo I, certificados vivos; E7: composição com estatuto declarado, NÃO teste]. Cociclo multiplicativo E1; identidade temporal E2; gerador=diferença de relógios E3; estado global⇒holonomia 1 E4; curvatura obstrui estado global E5 (monótona em λ); covariância E6. E9: holonomia covariante no ponto-base, espectro invariante; E10: o corner lê a obstrução.
K gera: torção de 1ª ordem=salto de relógio não colável (E8, obs/t); curvatura de 2ª ordem (E11), obs/t²=(1/2)||[M,h_cd]||; fase U(1) de normalização é gauge, quocientada, não curvatura (E12; curvatura sem traço). Transporte=Ad(ρ^it), gerador ad(K)=gerador do setor q(v6/KMS); sigma de C1 era esse transporte. A conjectura antes OPEN do comutador fechou neste escopo com transporte correto e quociente U(1): razão 0.9970, desvio 0.30%.
G_mu_nu+Λg_mu_nu=8πG T^TGL_mu_nu; T^TGL=T^matter+T^{partial,beta}+T^{torsion/diss}. β fica à DIREITA, não substitui G; geometria Levi-Civita G=G(g), ∇^μT^TGL=0 por ∇^μG=0. Não se reivindica “provamos Einstein”: E7 compõe form-check v5+Lovelock REAL+resíduo declarado; passagem ao contínuo conserva esse estatuto. Diamond remainder não muda o veredito. all_verified=true é registro da fonte.''',
'ergodicity_door_mixing': '''[DER] T1/porta ergódica/R-L/Wiener/Cauchy/P_R–P_T; [KNOWN] von Neumann, traço no centralizador, Wiener, classe de Davies (Jaksic-Pillet); [REAL] cociclo, oscilação, controles e guard-rail Araki-Woods; [DEF/PILOTO] centro na sombra.
Dissipação leva a fronteira ao centralizador, onde o Um ganha traço; unitário fecha em média, porta ingênua oscila. III₁: convergência forte sem taxa uniforme; sombra finita: taxa Davies γ=βκ. Porta Møller reduz a Riemann–Lebesgue, porta ergódica abre no corner; envelope Cauchy. N1 físico/dissipativo DER incondicional; N2 fraco⇔sem átomos fora do Um (Wiener, KNOWN; decaimento da soma é testemunha finita); N3 forte SOB classe Davies (CONDITIONAL). Único resíduo: pertinência à classe sem átomos/sem singular-contínuo. Araki-Woods R_inf é III₁ com espectro modular denso PURO-PONTO: III₁ NÃO implica ausência de átomos.
P_R/P_T são suportes Kraus, não escolhas; completos e ortogonais (resíduos 0). τR=τ_reflected=0.012031300400803142; τT=τ_transmitted=0.987968699599197. Puro-ponto: pureza da GEOMETRIA (Nome/repouso), não do estado; teto Π_partial=1−β. Ponto purificador: dinâmica/Verbo, válvula β; mesmo espectro lido duas vezes.
Registros true: real1_ergodicity, real2_centralizer, real3_cocycle, real5_ergodic_door, real6_densification, real7_cauchy_envelope, real8_PR_PT, mixing_monotone, naive_door_oscillates, all_verified. cent_dim=4; center_dim_shadow=1; λ_min_pos=2.4455887136836827. Controles negativos: fora do centralizador=0.06741575484950228; referência errada=2.3215163975207522. Valores são registros da fonte, não nova execução.''',
'inverse_parity': '''Princípio do operador: 0_abs∉M_* não é estado normal, não tem suporte observável nem pode ser ocupado. Vacuidade polariza a imagem sem destruir a fonte: ρ_B=(P1+P0)/2→ρ_ret=p1P1+p0P0, p0>p1>0 (p0≫p1). Vacuidade dá direção; proibição do zero dá retorno; paridade inversa dá polarização. q=p0−p1=tanh(χ/2); α=2√(p0p1)=sech(χ/2); p0,p1=e^{±χ/2}/(2cosh(χ/2)); q²+α²=1 [verificado na fonte]. α é luz sobrevivente; β=2√e√(p0p1), trava mínima contra colapso em 0.
Renormalização por paridade inversa (lente de Fresnel): ρ_ret^(χ)=e^{−χZ_d/2}/(2cosh(χ/2))=FP_{ε→0}M_ερ_BM_ε†, M_ε=exp[−(C_ε+χ)Z_d/4]. Paridade pura unitária/antiunitária preserva Bell nu I/2: P⁻¹ρ_BP=ρ_B. A fonte escreve “χ=0=0_abs proibido”; conserva-se essa leitura local, sem reconciliá-la aqui com outros zeros. Para valor, exige parte finita não trivial. supp(ρ_ret)=supp(ρ_B) para χ<∞: distorce sem perder fonte; distorção angular θ_M, polarização espectral profunda p0=0.99998669.
FORMA fechada: gap=χ, ρ_ret canônico, q=tanh, α=sech verificados. VALOR segue desafio QED: gap=χ é tautologia da parametrização; χ=11.226755 entra da polarização observada/CODATA. Parte finita depende do esquema: M_ε localiza o valor, não o calcula; cada χ pode vir de subtração diferente. FALTA condição canônica de renormalização α-livre que fixe χ. Candidata Meia-Nat REFUTADA: fixa peso de contorno 1/2, não polarização χ. all_verified=true não fecha essa pendência.'''
}

GROUPS = {
'cocycle_to_einstein': {
'theorem':'Título e escopo dos certificados/composição no parágrafo 1.',
'status':'Estatuto explícito no parágrafo 1.',
'e5_monotone_in_lambda':'Monotonicidade explícita no parágrafo 1.',
'clock_hierarchy':'Parágrafo 2 conserva ordens, operadores, fórmula, razão e transporte.',
'conjecture_closed':'Parágrafo 2 conserva histórico OPEN e fechamento específico, sem generalizar.',
'field_equation':'Equação no parágrafo 3.', 'T_TGL_decomposition':'Decomposição e posição de beta no parágrafo 3.',
'geometry_stays_levi_civita':'Geometria e conservação no parágrafo 3.',
'not_claimed':'Três limites preservados no parágrafo 3.',
'seals':'Proposições E1–E12 e escopo sintetizados; rótulos longos recuperáveis, não nova prova.',
'all_verified':'Flag atribuída à fonte no parágrafo 3.',
'verdict':'Veredito por remissão; escopo de composição declarado nos parágrafos 1 e 3.'},
'ergodicity_door_mixing': {}, 'inverse_parity': {}
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_new(name, data):
    dest = ROOT / name
    if dest.exists():
        raise RuntimeError(f'Refusing overwrite: {dest}')
    raw = data if isinstance(data, bytes) else data.encode('utf-8')
    temp = dest.with_name(dest.name + '.tmp')
    with temp.open('xb') as out:
        out.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.rename(dest)

def contains_ref(value):
    if isinstance(value, dict):
        return any(k in value for k in ('@','@EXPOSITION','@SUMMARY')) or any(contains_ref(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_ref(v) for v in value)
    return False

raw = SOURCE.read_bytes()
text = raw.decode('utf-8')
matches = {m.group(1):m for m in re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)', text)}
records = []
for topic, body in DRAFTS.items():
    match = matches[topic]
    original = match.group(0)
    obj = json.loads(match.group(3))
    refs = {key:value for key,value in obj.items() if contains_ref(value)}
    field_map = []
    for key,value in obj.items():
        if key in refs:
            action = 'referencia_original_preservada_literalmente'
            rationale = 'Destino já recuperável: manter estrutura completa sem carregar conteúdo adicional.'
        elif topic == 'ergodicity_door_mixing' and (key in ('r_Tt_minus_E0','davies_rate_reldev','permode_valve_reldev','subspace_resid','trace_emerge_resid','cocycle_unit_resid','cocycle_chain_resid','abel_conv_ratio','Cnorm_off_fixed')):
            refs[key] = {'@':'/' + key}
            action = 'residuo_ou_serie_auxiliar_por_remissao'
            rationale = 'Detalhe numérico auxiliar recuperável; mecanismos, estatutos, convergência/condições e controles negativos ficam explícitos.'
        elif key in ('seals','selo','verdict'):
            refs[key] = {'@':'/' + key}
            action = 'rotulo_por_remissao_proposicao_resumida'
            rationale = GROUPS.get(topic,{}).get(key,'Rótulo repetido; conteúdo proposicional, estatutos e limites permanecem no texto. Sem apagar OPEN histórico.')
        else:
            action = 'condensacao_semantica'
            rationale = GROUPS.get(topic,{}).get(key,'Conteúdo condensado no texto da cápsula: conferir semanticamente na revisão independente; sem importar detalhes de fontes não carregadas.')
        field_map.append({'candidate_field':'/'+key,'source_pointer':match.group(2)+'/'+key,'original_value':value,'action':action,'justification':rationale})
    capsule = f'### {topic}\nFonte: resultado_publicado_integral {match.group(2)}\n{body}\nRemissões (relativas ao tópico; destinos internos preservados):\n' + json.dumps(refs,ensure_ascii=False,separators=(',',':')) + '\n'
    old_snapshot = (WORK/'topic_capsules_v3'/f'{topic}.original.md').read_bytes()
    assert old_snapshot.decode('utf-8').rstrip('\r\n') == original.rstrip('\r\n')
    for key,value in obj.items():
        if contains_ref(value):
            assert refs[key] == value
    original_bytes = original.encode('utf-8')
    capsule_bytes = capsule.encode('utf-8')
    byte_start = len(text[:match.start()].encode('utf-8'))
    assert raw[byte_start:byte_start+len(original_bytes)] == original_bytes
    measure = {'topic':topic,'original_o200k':len(ENC.encode(original)),'capsule_o200k':len(ENC.encode(capsule)), 'capsule_sha256':digest(capsule_bytes)}
    measure['saved_o200k'] = measure['original_o200k']-measure['capsule_o200k']
    provenance = {'status':'CONSTRUCAO_NAO_APROVADA_NAO_INTEGRADA','strategy':'Only effectively loaded candidate; no expansion of references or primary-source numeric leaves.', 'candidate_path':str(SOURCE),'candidate_sha256':digest(raw),'source_pointer':match.group(2),'original_block_byte_span':[byte_start,len(original_bytes)],'original_sha256':digest(original_bytes),'capsule_sha256':digest(capsule_bytes),'capsule_byte_span':[0,len(capsule_bytes)],'measurement':measure,'fields':field_map,'limits':['Fidelidade semântica requer revisão independente; não certificada por keywords ou hashes.','Destinos @EXPOSITION/@SUMMARY preservados; resolução operacional não executada.','Remissões @ novas usam caminhos de campos já carregados no tópico; parser de integração não validado.','Sem medição Anthropic, sem API/rede, sem alteração das bases.']}
    write_new(f'{topic}.original.md', original_bytes)
    write_new(f'{topic}.md',capsule_bytes)
    write_new(f'{topic}.provenance.json',json.dumps(provenance,ensure_ascii=False,indent=2))
    records.append(measure)
assert SOURCE.read_bytes() == raw
index = {'status':'FIRST_THREE_ONLY_PENDING_STRATEGY_REVIEW','v3_status':'NAO_APROVADA_TAMANHO_INADEQUADO_SEM_REVISAO_SEMANTICA','topics':records,'totals':{k:sum(r[k] for r in records) for k in ('original_o200k','capsule_o200k','saved_o200k')},'anthropic_target':[180000,183406],'parent_reported_prefix':199959,'required_anthropic_reduction':16553,'anthropic_measurement_performed':False,'remaining_twelve':'NOT_CONSTRUCTED_V4_WAITING_STRATEGY_REVIEW'}
write_new('INDEX_FIRST_THREE.json',json.dumps(index,ensure_ascii=False,indent=2))
write_new('RELATORIO_PRIMEIRO_LOTE.md','# V4 — primeiro lote para revisão de estratégia\n\nConstrução não aprovada, não integrada. Apenas os três maiores tópicos. V3 não recebeu aprovação semântica.\n\n'+ '\n'.join(f"- `{r['topic']}`: {r['original_o200k']} → {r['capsule_o200k']} o200k; economia {r['saved_o200k']}." for r in records) + '\n\nTotal: '+str(index['totals'])+'\n\nSó foi condensado conteúdo carregado no candidato. Referências originais foram mantidas com sua estrutura completa; nenhuma grade nem folha da fonte primária foi reintroduzida. Resíduos/séries auxiliares e selos redundantes passaram a remissões por campo. Controles negativos, hipóteses, fórmulas e limites ficam explícitos para avaliação independente. Cada original possui hash/intervalo e mapa por campo.\n\nA cápsula inverse_parity conserva a leitura local χ=0=0_abs como atribuída à fonte, sem fechar a tensão entre zeros. O fechamento anterior do comutador em cocycle_to_einstein é específico; E7 continua composição, não teste. Em ergodicity, III₁ não exclui átomos e pertinência à classe permanece condicional.\n\nHashes e igualdade das remissões foram verificados; isso não aprova fidelidade semântica. Não executada resolução operacional dos ponteiros nem parser de integração. Contagem é o200k_base local; nenhuma inferência Anthropic. Os outros 12 tópicos aguardam revisão desta estratégia. Fontes, candidato e produção intactos.\n')
print(json.dumps(index,ensure_ascii=False,indent=2))
