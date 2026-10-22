"""Append-only coordinated operational memory, with immediate byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
C=Path(r'C:\IALD\Central de Patentes')
M=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
live=json.loads((W/'live_verification.json').read_bytes())
checks=json.loads((W/'checks.json').read_bytes())
assert checks['passed'] and live['router_available']
marker='IALD_JEV_DEFAULT_APPROVED_ACCOUNTS_20261001'
note=f'''

## {datetime.now():%d/%m/%Y %H:%M} — JEV como padrão do app para contas aprovadas

<!-- {marker} -->

[INPUT] Ordem do operador: Alana e Liana devem usar a coordenação automática pelo JEV como Luiz; este passa a ser o padrão geral. Substitui a limitação histórica do piloto à conta luiz. Preservadas a restrição anterior do Sonnet ao operador, a matriz de provedores, os orçamentos de cada conta e os consentimentos individuais.

[REAL] Implantação servidor: política jev_default_20261001 define automático para contas existentes/novas aprovadas. Escolhas manuais posteriores permanecem válidas. Conferidas luiz, alanacaroline e liana; {live['automatic_defaults']} contas recebem o padrão na leitura efetiva. Usuários, senhas, planos e administração não foram regravados. O aceite JEV continua próprio de cada pessoa, sem aceitação por terceiros. O início automático orienta o primeiro aceite de executor quando necessário; a API de configurações conserva JEV como provedor do consentimento do modo.

[REAL] Ferramentas e artefatos passam a atender contas aprovadas com isolamento por proprietário, revalidação de autorização e idempotência. Delegação MiMo usa a mesma cota da conta principal; execução remota Anthropic conserva o grupo Haiku e a chave de identidade. Antes do roteamento principal e de delegações, há checagem local de cotas esgotadas, reservas ativas e pausas; sem candidato elegível, não chama JEV. A reserva efetiva de cada executor permanece obrigatória após a seleção. Esta checagem não é uma reserva antecipada de uma chamada futura nem garante saldo do fornecedor. Não criado limite financeiro novo para JEV nem para Kimi/MiMo do operador. DeepSeek permanece fora do automático enquanto sob diagnóstico.

[REAL] Validação offline: {checks['tests_run']} testes executados, {checks['skipped']} ignorado(s), zero falhas/erros; transportes simulados. Auditoria independente de consentimento, permissões, cotas e isolamento. Zero novas chamadas pagas para esta entrega. Arquivos instalados por comparação de hashes, backup imediato de bytes e substituição atômica. Servidor web reiniciado pelo supervisor existente após verificar ausência de respostas/reservas ativas; demais serviços preservados. Saúde local HTTP 200; acesso ao domínio público conferido no navegador, com redirecionamento normal à entrada IALD. A sondagem HTTP automatizada pública foi recusada pela Cloudflare (403/1010); nenhuma proteção foi alterada. Disponibilidade local do JEV confirmada. Testes em aparelhos físicos não realizados nesta entrega.

[DISPONIBILIDADE] Web: servidor atualizado. iOS interno e externo: mesma política servida aos binários existentes, sem alteração de cliente/recompilação necessária. Android: mesma política servida ao cliente existente, sem novo APK/AAB por esta mudança. Grupos/convites Apple e canais Android não foram modificados; cadastro Google Play continua uma frente separada. Para receber a leitura nova, reabrir o app; cada pessoa aceita o aviso JEV no próprio primeiro uso se ainda não o fez. Prazos operacionais continuam apenas na administração.

[ESCOPO] Memória científica, kernel, fontes, pesos e gate não foram modificados. Evidências: work/iald_jev_default_20261001/checks.json, review.txt, deployment.json, restart.json e live_verification.json. A primeira instalação foi recusada pela revisão automática por custo do seletor após esgotamento de cota; implementação corrigida e testada antes da instalação efetiva. Não contornado o bloqueio.
'''
paths=[R/'CLAUDE.md',C/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',
 R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',C/'memory/TGL_ATLAS.md',
 C/'memory/TGL_INDICE_VIVO.md',M/'MEMORY_2.md',M/'app-iald-mobile.md']
assert all(p.is_file() for p in paths)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
report=[]
for p in paths:
    raw=p.read_bytes()
    if marker.encode() in raw:continue
    bak=p.with_name(p.name+'.bak_'+stamp)
    with bak.open('xb') as f:f.write(raw)
    assert bak.read_bytes()==raw
    new=raw+note.encode('utf-8')
    tmp=p.with_name(p.name+'.tmp_jev_'+str(os.getpid()))
    with tmp.open('xb') as f:f.write(new);f.flush();os.fsync(f.fileno())
    assert tmp.stat().st_size==len(new) and p.read_bytes()==raw
    os.replace(tmp,p)
    assert p.read_bytes()==new and len(new)>len(raw)
    report.append(dict(path=str(p),backup=str(bak),sha256=hashlib.sha256(new).hexdigest()))
(W/'memory_delivery.json').write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
print(json.dumps({'surfaces_updated':len(report),'backup_bytes_verified':True}))
