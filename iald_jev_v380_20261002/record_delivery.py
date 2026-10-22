"""Append the measured deployment to existing memories, preserving original bytes."""
from datetime import datetime, timezone
from pathlib import Path
import json

from transaction import atomic, backup, bench_snapshot, digest, write_evidence

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
C = Path(r'C:\IALD\Central de Patentes')
MARKER = 'IALD_JEV_EXECUTIVE_CONTROL_V380_20261002'


def main():
    live = json.loads((W / 'live_validation.json').read_bytes())
    checks = json.loads((W / 'validation/final_checks.json').read_bytes())
    independent = json.loads((W / 'validation/review_final.json').read_bytes())
    plan = json.loads((W / 'install_plan.json').read_bytes())
    probe = json.loads((W / 'live_jev_probe.json').read_bytes())
    count = json.loads((W / 'count_20261002_113914_901730.json').read_bytes())
    if (live['status'] != 'PASS' or not checks['passed'] or independent['status'] != 'PASS'
            or probe['status'] != 'PASS' or not count['budget']['ready']):
        raise ValueError('Incomplete delivery evidence')
    plan_pin = digest((W / 'install_plan.json').read_bytes())
    if independent['plan_sha256'] != plan_pin or checks['plan_sha256'] != plan_pin:
        raise ValueError('Unreviewed plan')
    for item in plan['files']:
        if digest(Path(item['destination']).read_bytes()) != item['sha256']:
            raise ValueError('Installed file changed after verification')
    if bench_snapshot() != live['bench_after']:
        raise ValueError('Resident data changed after verification')
    manifest = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
    evidence = json.loads((C / 'work/iald_operator_bench_20261002/stage/restart_inventory.json').read_bytes())
    surfaces = [Path(row['path']) for row in evidence['memory_surfaces']]
    release = live['release']
    message = f'''

## 02/10/2026 — JEV como controlador executivo IALD e memória científica v380

<!-- {MARKER} -->

[INPUT] O operador pediu examinar o chaveamento do JEV, parametrizá-lo pelo regime IALD definido no um.py e atualizar o app com a versão v380 custodiada. Esta entrega sucede a bancada pelo chat e conserva a classe operador exclusiva de Luiz, o mapa persistente e a RAM residente.

[REAL — fonte e implantação] O aplicativo utiliza {release['release']}, programa SHA256 {release['source_sha256']}, conferido contra a custódia local e o commit público fixado no manifesto de implantação. Fontes, resultado, selo e manifesto formal foram conferidos; não houve execução/importação de um.py nem nova compilação Lean. O catálogo conserva os 1209 arquivos formais. Foram instalados {live['installed_files']} arquivos derivados/fontes em versão separada, quatro módulos de integração e os manifestos verificados, com backups imediatos de bytes antes de substituir arquivos existentes. O original IALD_Kernel_v5.txt foi preservado. Nenhum gate ou original científico foi alterado.

[REAL — controle operacional] Contrato JSON derivado do registro integral iald_executive_runtime e das âncoras TheIALDSelector, TheSelectionIsTheBallast e TheVerbalCoupling. O JEV responde escolhas tipadas para domínio científico, via de trabalho, ação documental e executor; o servidor valida opções, probabilidade finita, fonte e capacidades. Entrada e candidatos autorizados são inscritos antes do envio; poda só reduz o conjunto; resultado incerto não é reenviado automaticamente. O plano restringe as ferramentas existentes e sua diretiva chega também aos gestores sem ferramentas. Observações de latência/custo são dados locais de tarefas diferentes, não benchmark de superioridade. As métricas enviadas não contêm conversas ou identidades de usuários.

[ESCOPO] É uma implementação de controle inspirada no regime documentado, não alteração de pesos nem novo teorema Lean. O registro de origem conserva DEF + ONTO + COMPUTATIONAL e o paralelo GKLS permanece analogia declarada. JEV recebe o contrato completo e um trecho público delimitado para escolher caminhos; o programa completo, o kernel e o acervo permanecem no servidor, com contexto e recuperação nos executores. Não se afirma que os 33 MB de um.py caibam na API do JEV. Probabilidades não equivalem a beta, pesos físicos, zero absoluto, autorização de acesso ou confirmação científica.

[REAL — memória] Cluster {manifest['active_cluster']['release']} SHA256 {manifest['active_cluster']['sha256']}; kernel v5 integral e núcleo anterior preservado com adendo atual. Fórmulas, estatutos e vereditos relevantes permanecem na memória, com detalhes recuperáveis e proveniência. Haiku: {count['budget']['permanent_tokens']} tokens permanentes medidos pelo contador nativo; pedido de referência {count['budget']['request_input_tokens']}, reserva de saída {count['budget']['reserved_output_tokens']}, margem {count['budget']['margin_tokens']}, folga {count['budget']['remaining_tokens']}. A medida não se transfere a outro tokenizer nem garante que qualquer histórico caiba. Cada transporte conserva sua admissão e seu orçamento. Solução matemática é apresentada com hipóteses/alcance e não é confundida com confirmação experimental.

[REAL — validação] Revisão científica independente 56/56 aprovada; suites locais e revisão de integração registradas em validation/final_checks.json e review_final.json. Quatro consultas reais curtas ao JEV distinguiram matemática, página HTML, cálculo Python e bancada, com custo estimado total US$ {probe['estimated_actual_usd']:.9f}; não acionaram executores nem operações da bancada. A validação após implantação conferiu os arquivos ativos, vínculo das fontes, carregamento do pacote, permissões de operador e HTTP local/público. Foram preservados os 180 arquivos GW, {live['bench_after']['gw']['resident_bytes']} bytes em RAM e seus hashes/carga, além da geração/carga cosmológica. Somente o processo web foi reiniciado pelo supervisor existente. Não se alega avaliação end-to-end da qualidade de respostas ou novo teste de natureza.

[DISPONIBILIDADE] Site demo.iald.ia.br e app iOS/Android utilizam o servidor atualizado em modo Automático. A entrega não altera arquivos de cliente ou recursos nativos; não exige nova build TestFlight/APK. Não houve nova instalação física, envio ou alteração de grupos das lojas nesta etapa. Autorizações, modelos, consentimentos e limites de todas as contas foram preservados; bancada exclusiva de luiz. Alertas de infraestrutura continuam apenas na administração. A fila global IALD_ORQUESTRACAO_20260923 é integração distinta; esta entrega não declara atualização de sua memória nem duplica seus jobs/heartbeat.

[EVIDÊNCIAS] {W}: install_plan.json, deployment.json, restart.json, live_validation.json, live_jev_probe.json, public_v380_verification.json, count_20261002_113914_901730.json, validation/final_checks.json e validation/review_final.json. Contrato ativo apontado em {R / 'iald_nucleo_fixo.json'}. Memórias atualizadas por append com backup imediato; resultados de modelos não se tornam cânone automaticamente.
'''
    entries = []
    for path in surfaces:
        original = path.read_bytes()
        if MARKER.encode() in original:
            raise ValueError('Delivery already recorded: inspect before repeating')
        preserved = backup(path)
        addition = message.replace('\n', '\r\n').encode('utf-8') if b'\r\n' in original else message.encode('utf-8')
        if path.read_bytes() != original:
            raise ValueError('Concurrent memory edit')
        raw = original + addition
        atomic(path, raw)
        if not path.read_bytes().startswith(original) or path.stat().st_size <= len(original):
            atomic(path, original)
            raise ValueError('Memory preservation failed; restored')
        entries.append({'path': str(path), 'backup': preserved, 'bytes_before': len(original),
                        'bytes_after': len(raw), 'sha256': digest(raw)})
    write_evidence(W / 'memory_updates.json', entries)
    delivery = {'status': 'ACTIVE_VERIFIED', 'utc': datetime.now(timezone.utc).isoformat(),
                'release': release, 'control_contract_sha256': manifest['jev_control']['sha256'],
                'native_permanent_tokens': count['budget']['permanent_tokens'],
                'paid_decision_tests': len(probe['cases']), 'estimated_test_cost_usd': probe['estimated_actual_usd'],
                'resident_bench_preserved': True, 'memory_surfaces_updated': len(entries),
                'web': 'active', 'ios': 'server updated; existing client; no new binary needed',
                'android': 'server updated; existing client; no new binary needed',
                'physical_device_test': 'not performed', 'global_orchestration_memory': 'separate; unchanged'}
    write_evidence(W / 'delivery.json', delivery)
    print(json.dumps({'status': delivery['status'], 'release': release['release'], 'memory_surfaces': len(entries)}))


if __name__ == '__main__':
    main()
