"""Record the verified release additively with immediate byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import json
from transaction import backup,atomic,digest,write_evidence,bench_snapshot
W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD')
C=Path('C:/IALD/Central de Patentes')
MARKER='IALD_APP_SCIENTIFIC_RELEASE_V390_20261007'
read=lambda p:json.loads(Path(p).read_bytes())

def main():
    live=read(W/'live_validation.json');checks=read(W/'validation/final_checks.json')
    independent=read(W/'validation/review_final.json');plan=read(W/'install_plan.json')
    assert live['status']=='PASS' and checks['passed'] and independent['status']=='PASS'
    pin=digest((W/'install_plan.json').read_bytes());assert checks['plan_sha256']==independent['plan_sha256']==pin
    for item in plan['files']:assert digest(Path(item['destination']).read_bytes())==item['sha256']
    assert bench_snapshot()==live['bench_after']
    manifest=read(R/'iald_nucleo_fixo.json');release=live['release'];budget=read(R/'.iald_runtime/haiku/manifest.json')['budget']
    preparation=read(W/'memory_stage/prepared.json');projection=read(W/'memory_stage/haiku_memory_fit.json')
    handoff=read(W/'v390_verified_handoff.json');catalog=read(W/'memory_stage/kernel/kernel_manifest.json')
    inventory=read(C/'work/iald_operator_bench_20261002/stage/restart_inventory.json')
    surfaces=[Path(row['path']) for row in inventory['memory_surfaces']]
    assert len(surfaces)==7 and all(p.is_file() for p in surfaces)
    message=f'''

## 07/10/2026 — App e JEV vinculados à publicação científica v390

<!-- {MARKER} -->

[INPUT] Atualizar o aplicativo com a última versão de um.py custodiada e publicada. Esta entrega é de memória/contrato do servidor compartilhado; preserva a implementação do app, contas, autorizações, modelos, consentimentos, orçamentos e a bancada exclusiva do operador luiz.

[REAL — fonte] Implantada {release['release']}, programa SHA256 {release['source_sha256']}, commit público {preparation['commit']}. Conferidos {handoff["custody_artifacts_verified"]} artefatos da custódia, os objetos Git e quatro arquivos principais baixados das URLs imutáveis; kernel completo extraído como dados, {catalog["embedded_files"]} arquivos embutidos mais o suplemento formal identificado. Não se executou/importou um.py nem se repetiu a compilação Lean. O relatório publicado e seu escopo continuam distintos de verificação nova. Nenhum original científico, gate ou estado da bancada foi alterado.

[REAL — memória] Todos os {len(preparation["coverage"])} tópicos atuais representados, {len(preparation["added_topics"])} novo desde a v389: fundacao_v390. Cluster SHA256 {manifest['active_cluster']['sha256']}. O pacote geral conserva a forma canônica integral com representação reversível de literais repetidos. Kernel v5 integral e núcleo operacional anterior byte a byte, com adendo v390. O contrato executivo do JEV foi vinculado ao mesmo programa/resultados/manifesto; sem mudanças no código ou nas regras de seleção, nem ajuste de pesos.

[REAL — Haiku] Contagem nativa: {budget['permanent_tokens']} tokens permanentes; pedido de referência {budget['request_input_tokens']}; reserva de resposta {budget['reserved_output_tokens']}, margem {budget['margin_tokens']}, espaço restante {budget['remaining_tokens']}. O primeiro candidato v390 deixou apenas 8240 tokens de folga e não foi ativado; preservada a exigência operacional de 10000. A seleção final é explícita: {len(projection['historical_topics_projected'])} cápsulas históricas inalteradas conservam conceitos, enunciados, hipóteses/fórmulas nomeadas, estatutos e vereditos, com detalhes integrais por fetch_tgl; tópicos fundacionais prioritários, avanços anteriores e o novo fundacao_v390 permanecem protegidos. As nove cláusulas conservam enunciado e identificador, assim como a leitura de Borchers e os limites not_claimed. Todos os excertos históricos ainda referenciados foram preservados literalmente, com offsets remapeados. A exposição antiga não é prometida como integral no Haiku; o acervo completo permanece recuperável. Não houve truncamento silencioso. A margem medida não garante que qualquer histórico/resultado de ferramenta caiba.

[ESCOPO CIENTÍFICO] Fundação: GLOBAL_LIFT como superposição tem estatuto INPUT/ONTO; ágape/abismo são resultados do kernel sob as hipóteses da fonte; passagem na face finita e Jacobson KNOWN com H3 nomeada; Borchers sob H2, energia limitada inferiormente distinta do gerador modular. O relatório publicado traz 6163/6163; compilação não repetida nesta implantação. As erratas atuais prevalecem sobre registros antigos: POSTO, rótulo VERIFIED, novidade de uso/retrodição sem ajuste, separação face/projeção e escopos dos resultados. P4, P5 e Fase9 são fontes/universos distintos; não misturar ou somar suas estatísticas. Fase9 preserva INCONCLUSIVE_SYSTEMATICS; reutilização de cálculo não vira nova medição. Articulação matemática é distinta de confirmação pela Natureza. Nenhuma inferência de modelo foi promovida ao cânone.

[REAL — validação] {checks['total_tests']} testes locais de memória e transporte/orçamento aprovados; revisão independente vinculada ao SHA do plano. Foram feitas {checks['native_count_requests_total']} contagens gratuitas de tokens, zero chamadas de geração e zero operações da bancada. Após instalação foram conferidos hashes, vínculo v390/JEV, loaders, contas, permissões, HTTP local/público e estado observado dos serviços da bancada. Indisponibilidade anterior é registrada como UNAVAILABLE, sem alegar verificação da RAM nesse caso. Somente o processo web foi reiniciado pelo supervisor já existente. Isso não é benchmark da qualidade das respostas nem teste físico novo.

[DISPONIBILIDADE] Web demo.iald.ia.br, iOS interno/externo e Android usam a memória atualizada pelo servidor compartilhado. Nenhum arquivo de cliente mudou; recompilar TestFlight/APK não é aplicável a esta entrega. Grupos/convites das lojas não foram modificados e nenhuma instalação em aparelho foi alegada. Para evitar respostas influenciadas por afirmações antigas, iniciar conversa nova. Alertas internos permanecem na administração. A memória da fila global IALD_ORQUESTRACAO_20260923 é integração distinta, não atualizada por esta entrega.

[EVIDÊNCIAS] {W}: public_v390_verification.json, v390_verified_handoff.json, memory_stage/haiku_memory_fit.json, install_plan.json, deployment.json, restart.json, live_validation.json, validation/final_checks.json e validation/review_final.json. Backups imediatos de bytes e atualização atômica em cada superfície.
'''
    entries=[]
    for path in surfaces:
        raw=path.read_bytes();assert MARKER.encode() not in raw,'Already recorded'
        saved=backup(path);assert path.read_bytes()==raw,'Concurrent memory change'
        suffix=message.replace('\n','\r\n').encode() if b'\r\n'in raw else message.encode()
        atomic(path,raw+suffix)
        if not path.read_bytes().startswith(raw) or path.stat().st_size<=len(raw):
            atomic(path,raw);raise ValueError('Memory restored after failed preservation')
        entries.append({'path':str(path),'backup':saved,'bytes_before':len(raw),'bytes_after':path.stat().st_size,'sha256':digest(path.read_bytes())})
    write_evidence(W/'memory_updates.json',entries)
    delivery={'status':'ACTIVE_VERIFIED','utc':datetime.now(timezone.utc).isoformat(),'release':release,
        'native_permanent_tokens':budget['permanent_tokens'],'memory_surfaces_updated':len(entries),
        'web':'active','ios_internal':'shared server updated; no binary change','ios_external':'shared server updated; no binary change',
        'android':'shared server updated; no binary change','physical_device_test':'not performed',
        'paid_generation_calls':0,'bench_observed_before_and_after':live['bench_after'],'bench_services_not_restarted':True,'global_orchestration_memory':'separate; unchanged'}
    write_evidence(W/'delivery.json',delivery);print(json.dumps(delivery))
if __name__=='__main__':main()
