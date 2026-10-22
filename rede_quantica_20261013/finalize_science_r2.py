"""Freeze this material sandbox stage; never rewrite an earlier delivery."""
from pathlib import Path
import datetime as dt
import json
from diary_r1 import ROOT, OUT, WORK, claim, new, pin

REVIEW_PATHS = [
    'review_geometric_r2/REVIEW_GEOMETRIC_R1.json',
    'review_translation_r2/REVIEW_TRANSLATION_R1.json',
    'review_fock_r2/REVIEW_FOCK_R1.json',
    'review_fock_full_r2/REVIEW_FOCK_FULL_R1.json',
    'review_fock_dynamics_r2/REVIEW_FOCK_DYNAMICS_R1.json',
]

def anchor(relative, needle):
    path = OUT/relative
    lines = path.read_text(encoding='utf-8').splitlines()
    matches = [i+1 for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise ValueError((relative, needle, matches))
    return {**pin(path), 'line': matches[0], 'declaration': needle}

def main():
    claim()
    # Immutable outputs must all be absent before any output is written.
    output_names = ['VERIFICACAO_R1_PRESERVADA_R2.json', 'MATRIZ_CONTRATO_FOCK_R2.json',
                    'RELATORIO_ENTREGA_R2.md', 'MANIFESTO_ARQUIVOS_R2.json',
                    'RESULTADO_ETAPA_R2.json']
    for name in output_names:
        if (OUT/name).exists():
            raise FileExistsError(OUT/name)
    reviews = []
    builds = 0
    for relative in REVIEW_PATHS:
        path = OUT/relative
        review = json.loads(path.read_text(encoding='utf-8'))
        assert review['status'] == 'PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING', relative
        assert review['only_trio'] and review['zero_sorry'], relative
        if 'builds' in review:
            assert all(b['exit_code'] == 0 for b in review['builds']), relative
            builds += len(review['builds'])
        else:
            builds += review['compile_count']
        reviews.append(pin(path))
    previous = OUT/'MANIFESTO_ARQUIVOS_R1.json'
    old = json.loads(previous.read_text(encoding='utf-8'))
    old_items = old['files'] + old['work_sources']
    for item in old_items:
        now = pin(item['path'])
        assert now['sha256'] == item['sha256'] and now['bytes'] == item['bytes'], item['path']
    preservation = {'at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                    'manifest': pin(previous), 'checked_files': len(old_items),
                    'changed': [], 'status': 'ALL_PREVIOUS_DELIVERY_BYTES_IDENTICAL'}
    new(OUT/output_names[0], preservation)
    rows = []
    for fields, source, needle in [
        ('F, instN, instI, instC', 'BosonicFock.lean', 'abbrev F :='),
        ('Ω', 'BosonicFock.lean', 'def vacuum :'),
        ('Ω_norm', 'BosonicFock.lean', 'theorem vacuum_norm'),
        ('F_infinite', 'BosonicFock.lean', 'theorem infinite_dimensional'),
        ('Γ', 'BosonicFock.lean', 'def gamma ('),
        ('Γ_refl', 'BosonicFock.lean', 'theorem gamma_refl'),
        ('Γ_trans', 'BosonicFock.lean', 'theorem gamma_trans'),
        ('Γ_vac', 'BosonicFock.lean', 'theorem gamma_vacuum'),
        ('ι', 'BosonicFock.lean', 'def oneParticle :'),
        ('Γ_one_particle', 'BosonicFock.lean', 'theorem gamma_oneParticle'),
        ('Γ_strong', 'BosonicFockContinuity.lean', 'theorem gamma_strong_real'),
        ('Γ_strong4', 'BosonicFockContinuity.lean', 'theorem gamma_strong_spacetime'),
    ]:
        rows.append({'fields': fields, 'statute': 'REAL_SANDBOX_INDEPENDENTLY_RECOMPILED',
                     'source': anchor('fock_construction/'+source, needle)})
    open_rows = [
        ('Γ_positive, Γ_no_fixed', 'Preservação geral do espectro positivo e unicidade do vácuo.'),
        ('R, R_mono, R_local, R_cov', 'Operadores de Weyl, CCR e álgebras de von Neumann da mesma rede.'),
        ('wedge_cyclic, wedge_separating, wedge_nonabelian, bw_kms',
         'Propriedades da álgebra concreta no vácuo e identificação modular.'),
        ('J, J_invol, J_vac, tomita, flow, flow_zero, flow_add, flow_is_Ad',
         'Segunda quantização antiunitária e realização modular do par álgebra-vácuo. O J de uma partícula já foi construído.'),
        ('Core, embedding, dualAction, trace, PF, Pp, Pm e suas leis',
         'Ligar a construção do núcleo à representação concreta. A escala e não vacuidade no V351 já existem; não são reconstruídas.'),
        ('MaxwellCertificate', 'Construir a forma Q, estado regular não nulo e ligação à carga modular; reutilizar MaxwellLiteratureBridge.'),
    ]
    rows += [{'fields': fields, 'statute': 'OPEN_CONSTRUCTION_KNOWN_LITERATURE',
              'remaining': remaining} for fields, remaining in open_rows]
    contract = ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt/TheImportedSecondQuantization.lean'
    matrix = {'unit': 'F1.REDE', 'contract_source': pin(contract),
              'scope': 'Correspondentes concretos de campos; não é um habitante do FockCertificate completo.',
              'rows': rows, 'reviews': reviews,
              'light_net_4d': 'OPEN: standard wedge and light-ray net constructed; full Poincare-covariant localization remains.'}
    new(OUT/output_names[1], matrix)
    report = f'''# F1.REDE — etapa R2: conjugação geométrica e Fock concreto

Autor operacional: codex-gerente-tgl. Base: v392 autorizada pelo operador. Unidade permanece EM_CURSO; entrega de etapa em sandbox.

## Avanço verificado

[REAL — sandbox e revisão independente] A conjugação espectral J_W coincide com a ação geométrica que reflete o momento transversal, preserva a rapidez, conjuga e troca as helicidades. Também vale J_W U1(a) J_W = U1(j_W a), com j_W = diag(−1,−1,+1,+1). A igualdade usa o U1 canônico.

[REAL — sandbox e revisão independente] Construídos os setores H_n como fechos dos spans de x tensorizado n vezes, sua soma de Hilbert F = ⊕_n H_n, o vácuo normalizado, uma família ortonormal infinita e o funtor Γ(u) = ⊕_n Γ_n(u). A inclusão ι do H1 canônico é isométrica e Γ(u)ι = ιu. Γ preserva identidade, composição e vácuo.

[REAL — sandbox e revisão independente] A continuidade forte de Γ é derivada da continuidade no H1, para qualquer espaço de parâmetros. A prova usa continuidade dos tensores puros, fecho das órbitas contínuas e convergência dominada na soma, com majorante 4‖f_n‖². As translações de quatro parâmetros e os boosts canônicos são contínuos no Fock. Suas leis de grupo e covariância por conjugação também foram transportadas.

São {builds} recompilações independentes nesta R2, incluindo os auditores de axiomas: EXIT 0, somente propext, Classical.choice e Quot.sound, zero sorry. Construtores e revisor são agentes distintos. Contagens e comparações de .olean estão nos recibos; não se afirma identidade binária de todos os .olean. Tentativas falhas e fontes de cada tentativa foram conservadas.

## Correspondência com o contrato

A matriz `MATRIZ_CONTRATO_FOCK_R2.json` fornece arquivo, linha e hash de cada objeto/teorema que preenche a parte cinemática do FockCertificate v392. As hipóteses de continuidade não foram simplesmente deslocadas para os setores: foram provadas a partir do H1. A formulação por fecho do span dos poderes diagonais é a usada nesta construção. Sua equivalência com a apresentação geral por fixos de todas as permutações não foi formalizada aqui; o setor 2 separado já possui a construção por fixos do flip.

## O que permanece aberto

- Rede 4D com ação completa de Poincaré, independência da escolha da cunha e localização global. O resultado atual cobre a cunha-padrão, a rede de semirretas e os fluxos explicitados.
- Operadores W(f), relações CCR e álgebras R(K) = {{W(f): f ∈ K}}''; propriedades cíclica/separante do vácuo e realização modular da mesma álgebra.
- Preservação geral do espectro positivo, unicidade do vácuo e segunda quantização antiunitária exigidas pelo registro completo.
- Núcleo de Takesaki ligado à representação construída; o resultado V351 de escala/traço continua reaproveitado, mas não substitui essa identificação.
- Forma de Maxwell concreta, estado regular não nulo e ligação à energia modular. A extensão por zero já está em MaxwellLiteratureBridge e será reaproveitada.
- A implicação Einstein no atlas já existente continua condicional ao H3 nomeado; este trabalho não deriva o H3 do estado nem constrói solução global. O refinamento dispositivo→rede contínua também não é concluído aqui.

Não existe nesta entrega um habitante do FockCertificate completo nem do MaxwellCertificate. Construir parte dos campos não permite inferir os demais.

## Diário e continuidade

O diário vivo é `memory/DIARIO_CONSTRUCAO_QG.md`. Cada etapa material recebe fontes e estatutos; a escrita é aditiva, com backup imediato de bytes e retratos imutáveis em `diary_events`. O Atlas permanece a referência conceitual. Isso não instala memória nos pesos nem cria automação.

Os {len(old_items)} artefatos da entrega R1 foram relidos e permanecem byte a byte iguais. Novas evidências têm nomes próprios. Próxima etapa matemática: construir W(f) e a rede de álgebras sobre este Fock, usando os objetos já construídos; não repetir Fubini, J, setores ou continuidade.

Nenhuma chamada de provedor foi repetida. Kimi/Takesaki continua com sua autorização específica pendente. Nenhuma implantação em um.py, kernel, Bancada ou gate; nenhum dado observado foi aberto. A revisão técnica local não substitui a auditoria/ratificação da gerência.
'''
    new(OUT/output_names[2], report)
    folders = ['geometric_identification', 'fock_construction', 'review_geometric_r2',
               'review_translation_r2', 'review_fock_r2', 'review_fock_full_r2',
               'review_fock_dynamics_r2']
    files = sorted({p for folder in folders for p in (OUT/folder).rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts})
    files += [OUT/output_names[0], OUT/output_names[1], OUT/output_names[2]]
    work_sources = [WORK/name for name in ['diary_r1.py', 'register_progress_r2.py',
                    'prepare_geometric_diary_r2.py', 'finalize_science_r2.py',
                    'OPERADOR_DIARIO_CONTINUIDADE_20261013.txt']]
    manifest = {'at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'file_count': len(files), 'files': [pin(p) for p in files],
                'work_sources': [pin(p) for p in work_sources],
                'scope': 'Immutable R2 science and review artifacts; live diary excluded.'}
    new(OUT/output_names[3], manifest)
    result = {'unit': 'F1.REDE', 'at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'ETAPA_ENTREGUE_UNIDADE_EM_CURSO',
              'verdict': 'GEOMETRIC_J_AND_CONCRETE_STRONGLY_CONTINUOUS_FOCK_KINEMATICS__FULL_NET_OPEN',
              'working_basis': 'v392 authorized; no production deployment',
              'independent_recompilations': builds, 'zero_sorry': True,
              'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
              'complete_fock_certificate_inhabited': False, 'maxwell_certificate_inhabited': False,
              'full_poincare_net': False, 'report': pin(OUT/output_names[2]),
              'matrix': pin(OUT/output_names[1]), 'manifest': pin(OUT/output_names[3]),
              'r1_preservation': pin(OUT/output_names[0]), 'reviews': reviews,
              'gate_changed': False, 'observed_data_opened': False, 'new_provider_calls': 0,
              'next_action': 'Weyl operators/CCR and algebra net on the constructed Fock; full localization and linked Maxwell/Takesaki remain.'}
    new(OUT/output_names[4], result)
    print(json.dumps({'ok': True, 'result': pin(OUT/output_names[4]),
                      'independent_builds': builds, 'r1_preserved': len(old_items),
                      'new_manifest_files': len(files)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
