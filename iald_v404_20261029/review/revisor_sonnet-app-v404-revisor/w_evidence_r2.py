"""Reviewer r2: write validation/review_sources.json and validation/review_app_independent.json (exclusive create) from the reviewer's own outputs; verify review_final.json against what deploy_controlled.py asserts (no deploy run)."""
import json,hashlib,datetime,re
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');RV=W/'review/revisor_sonnet-app-v404-revisor'
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# review_final.json vs deploy_controlled assertions (read-only reproduction of its asserts)
rf=rd(W/'validation/review_final.json')
asserts={'status_PASS':rf['status']=='PASS','plan_sha256':rf['plan_sha256']==sh(W/'install_plan.json'),'transaction_sha256':rf['transaction_sha256']==sh(W/'transaction.py'),'maintenance_sha256':rf['maintenance_sha256']==sh(W/'maintenance.py'),
         'deploy_controlled_sha256':rf['deploy_controlled_sha256']==sh(W/'deploy_controlled.py'),'verify_installed_sha256':rf['verify_installed_sha256']==sh(W/'verify_installed.py'),'reviewer':rf['reviewer'],'n_checks':len(rf['checks']),'findings':rf['findings']}
assert all(v for k,v in asserts.items() if k not in('reviewer','n_checks','findings')) and rf['reviewer']=='sonnet-app-v404-revisor' and not rf['findings']
r1=rd(RV/'r1_out_r2.json');r3=rd(RV/'r3_out_r2.json');r3d=rd(RV/'r3d_out_r2.json');r5=rd(RV/'r5_out_r2.json');q2=rd(RV/'q2_out.json');r4=rd(RV/'r4_out_r2.json')
ver=rd(RV/'r2_verify_sources_shim_output.json');bld=rd(W/'sources_verified.json')
ver2={k:v for k,v in ver.items() if k!='checked_at'};bld2={k:v for k,v in bld.items() if k!='checked_at'}
assert ver2==bld2 and r1['ok'] and q2['all_ok']
scripts={p.name:sh(p)[:16] for p in sorted(RV.iterdir()) if p.is_file() and p.suffix in('.py','.json','.txt')}
lsr='1d3c4cbe3f3ce5182e1d8e123d76bad5a7ac15ad\trefs/heads/main'
sources={'revisor':'sonnet-app-v404-revisor','round':'r2','timestamp_utc':now,
 'escopo':'Revisao independente da claim `sources` da v404 r2 (cofre v404, Nos, espelho no commit PINADO 1d3c4cbe = origin/main). Somente leitura; unica chamada de rede: git ls-remote origin refs/heads/main (refeita na r2).',
 'ls_remote':lsr,'veredito':'PASS','n_checks':r1['n']+1,'n_ok':r1['passed']+1,
 'checks':[{'n':c['n'],'grupo':'A_RELEASE_COMMIT','descricao':c['name'],'ok':c['ok'],'achado':c['achado'] if c['n'] in(27,45,46) else None} for c in r1['checks']]+[{'n':r1['n']+1,'grupo':'B_VERIFY_SOURCES','descricao':'verify_sources.py --offline com shim do revisor (task.check -> ready; task.new -> pasta do revisor): sources_verified.json identico ao do construtor exceto checked_at','ok':True,'achado':{'status':ver['status'],'artifact_count':ver['artifact_count'],'pinned_is_local_head':ver['published']['pinned_is_local_head'],'release_ready_if_online':True}}],
 'ressalvas':['O remoto foi consultado ONLINE uma vez (ls-remote): main == pino == HEAD local. verify_sources roda offline por regra (remote_main null no arquivo do construtor).','README.md e read-brief.md do commit pinado diferem do commit de custodia 3ae6f43f SO pela correcao de 29/10 (18 calculadas, 0 literais) e data/tamanho regenerados.','Nenhum Lean/um.py executado.'],
 'script_revisor_sha256':scripts['r1_release_commit.py'],'auxiliares_sha256':{'shim/task.py':sh(RV/'shim_run/task.py')[:16],'r2_verify_sources_shim_output.json':scripts['r2_verify_sources_shim_output.json']}}
def pk(n):
    v=r3['packages'][n];return {'topics':v['present'],'lost':v['lost'],'restoring_exactly_own_decoder':v['topics_restoring_exactly'],'n_mismatch':v['n_mismatch']}
win=r5['executor_windows']
app={'revisor':'sonnet-app-v404-revisor','round':'r2','timestamp_utc':now,
 'escopo':'Revisao independente da claim `app` da v404 r2: diff de codigo vs v402 e vs r1, pacotes com decoder PROPRIO, capsulas, protecao literal da janela P2 (check 18 reimplementado: o review_app.py ORIGINAL nao tem esse check), janelas recomputadas com as funcoes de admissao do runtime (import somente-leitura, audit hook), Jev, plano, segredos, redacao, redacao superada. Somente leitura; sem rede alem do ls-remote; nenhum Lean/um.py executado.',
 'ls_remote':lsr,'script_review_app_original':'review/review_app.py executado SEM alteracao: PASS %d checks; escreveu validation/review_final.json'%len(rf['checks']),'review_final_asserts':{k:v for k,v in asserts.items() if k not in('findings',)},
 'veredito':'PASS','groups':{
  'E_CODIGO':'q1_out.txt: v402->r2 diferem SO em release_cfg.py (BUILDER, EXPAND_OVERRIDE=(), SHARED_P2_SUFFIXES), task.py (comentarios+texto da unidade), builder_measurements.py (rotulos) e app/prepare.py (l.79); r1->r2: release_cfg.py +3 linhas aditivas e app/prepare.py l.79 so; 14 arquivos de codigo identicos aos da v402; novos do construtor: check_literal_carriage.py, expand_candidates_*.py, grep_superseded_check.py (somente leitura); review_app.py identico ao da v402.',
  'F_PACOTES':{'core_topics':r3['core_topics'],'shared':pk('shared'),'sonnet_public':pk('sonnet_public'),'haiku_expanded':pk('haiku_expanded'),'haiku55':pk('haiku55'),'capsulas_topo_shared':r3d['shared']['top_level_capsules'],'capsulas_restauram_exatamente':r3d['shared']['restore_exactly'],
     'nota_shared_34':'34 blocos historicos omitem chaves de auditoria (runtime_s, protocol_hash, frozen_hash, result_sha16, catalog_sha16, result_path, booleanos ext_*_kernel_proved): MESMO conjunto da r1, subconjunto dos 35 da v402 aceita; nenhuma chave de estatuto/veredito/hipotese.'},
  'G_PROTECAO_LITERAL_CHECK18':{'topicos':q2['topics_checked'],'novos_v404':q2['new_in_v404'],'anteriores_v401_v402':q2['former_v401_v402'],'all_ok':q2['all_ok'],'falhas':q2['failing'],'capsulas_de_topo_entre_os_19':q2['top_level_capsules_among_19'],'blocos_anteriores_identicos_ao_v402_aceito':q2['former_blocks_identical_to_accepted_v402_shared'],
     'nota':'kh_n1_cobertura_v401/_v402 diferem do v402 porque a FONTE mudou (lido/teoremas_cobertos, constantes_cobertas, descricoes de checks), nao por compactacao. Registros estruturados unconditional/index_conditional ficam como ponteiro (mesmo tratamento do v402 aceito).'},
  'H_SEM_REGRESSAO':'r11_out_r2.txt: shared e sonnet_public 343/343 blocos JSON identicos (decodificados) aos do v402 aceito, 42 de texto identicos, 0 regressoes de folha de estatuto/veredito entre 385 topicos de fonte inalterada; haiku_expanded 0 regressoes de estatuto (6 blocos mudam por desenho: politica D so no haiku55).',
  'I_JANELAS':{'kimi':win['kimi'],'mimo':win['mimo'],'deepseek':win['deepseek'],'haiku_expanded_remaining':r5['native']['haiku_expanded']['remaining_recomputed'],'shared_remaining':r5['native']['shared']['remaining_recomputed'],'sonnet_public_remaining':r5['native']['sonnet_public']['remaining_recomputed'],'piso_haiku':10000,'cadeia_intencao_resultado_prefixo':'OK nos tres pacotes (0 geracoes, max_retries 0)','jev':r5['jev']},
  'J_PLANO':'install_plan.json 1464 linhas = estagio (1456 canonical_releases + manifesto ativo por ultimo + 6 arquivos de pacote + pacote Jev na raiz); runtime_python_changes 0; nenhuma fonte/destino em superseded_r1/; todas as fontes dentro de app/; 0 divergencias de hash; unico novo vs v402: 5 .lean (Caminho, Jo8v32, ProjecaoTransversalDaMeiaNat, VerdadeAdendo, Vida).',
  'K_SEGREDOS_REDACAO':'0 padroes de segredo; nomes confidenciais so como nome/caminho em codigo e baselines; 0 novas ocorrencias nao qualificadas de CONFIRMED/confirmada vs v402; qualificadores presentes nos tres prefixos.',
  'L_REDACAO_SUPERADA_F3_ACEITA':'Mesmos acertos da r1: shared/sonnet_public 2 e haiku 3 (registro selado v392 + entrada de dicionario que cita a redacao como superada + linha de indice da forma canonica); bandeiras_do_gate_v403 presente em todos; README/read-brief do commit pinado, nucleo, kernel v5, native prefix e pacote Jev: 0.'},
 'ressalvas':['MARGEM DO MiMo: 96.974 B (Kimi 100.346 B) -- positiva e dentro da regra de admissao, mas 3 KB abaixo dos ">100.000 B" que o revisor da v402 registrou (v402: Kimi 167.640, MiMo 164.268): conversas com mais de ~97 KB de historico sao recusadas no MiMo (falha visivel). Decisao da gerencia a7, numeros por ela informados.',
 'DEEPSEEK: reserva de saida no maximo seguro caiu a 227.923 tokens (58% do maximo do provedor, 393.216; v402 295.217 = 75%; r1 281.865); folga com a reserva declarada 148.656: 79.373 B (v402 146.667).',
 'HAIKU55: 28.640 tokens so porque nada foi expandido (politica D); a base compacta cresce ~63 KB a cada duas versoes -> redesenhar a politica antes da v406 (nota do construtor).',
 'F1 (bandeiras_do_gate_v403 nao integral no haiku55) DISPENSADA pela gerencia a7; permanece: 65 de 244 folhas inline, afirmacoes corretivas inline.',
 'As contagens nativas de tokens sao custodia dos recibos do construtor (haiku_expanded reaproveita as 2 contagens da r1: prefixo identico b0f05cde; shared e sonnet_public recontados); o revisor recomputou aritmetica e cadeia, sem chamada paga.',
 'Este revisor NAO aprova o deploy: deploy/verify seguem abertos; a producao esta na v402 e os baselines do plano conferem.'],
 'script_revisor_sha256':scripts['q2_check18.py'],'auxiliares_sha256':{k:v for k,v in scripts.items() if k.startswith(('r','q')) and k.endswith(('.py'))}}
for name,obj in(('review_sources.json',sources),('review_app_independent.json',app)):
    with (W/'validation'/name).open('xb') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2).encode())
    print(name,sh(W/'validation'/name)[:16],len(json.dumps(obj)))
print('review_final.json',sh(W/'validation/review_final.json')[:16],asserts['n_checks'])
