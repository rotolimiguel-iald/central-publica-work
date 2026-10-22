"""Append verified deployment handoff to established memory surfaces, byte-atomically."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
w=Path(__file__).resolve().parent
sys.path.insert(0,str(w))
from transaction import atomic,backup,write_evidence
r=Path(r'C:\IALD\projetos_pyhton\IALD');c=Path(r'C:\IALD\Central de Patentes')
paths=[r/'CLAUDE.md',c/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',r/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',c/'memory/TGL_ATLAS.md',c/'memory/TGL_INDICE_VIVO.md',Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
for name in ['memory_fix/restart.json','restart.json','validation/deployed_runtime.json','validation/review_final.json']:
    assert json.loads((w/name).read_bytes())['status']=='PASS',name
assert json.loads((w/'validation/browser_verification.json').read_bytes())['status']=='PASS'
marker='<!-- IALD_HAIKU55_JEV_EXECUTION_GUIDE_20261007 -->'
body='''

## 07/10/2026 — Haiku 5.5 único e parametrização operacional do JEV

<!-- IALD_HAIKU55_JEV_EXECUTION_GUIDE_20261007 -->

[INPUT] Operador pediu somente Haiku 5.5, memória pública máxima e JEV parametrizado com capacidades de cada IA, custo-benefício, ferramentas, fontes científicas e uso da bancada. Mantidos automático para usuários comuns, manual somente luiz, Sonnet somente luiz e bancada somente luiz com papel operador. Não há Opus integrado. A preferência por Claude na arquitetura/revisão de código é do operador, não um benchmark comparativo.

[REAL — implantação] Haiku usa claude-haiku-5-5, janela 1.000.000, saída reservada 16.384, raciocínio adaptativo médio. O núcleo público completo disponibilizado para contexto pela camada canônica v390, com kernel-mãe v5 e cluster, foi contado pelo provedor: 573.879 tokens permanentes; pedido de referência 575.283, margem 1.024 e saldo de referência 407.309. Não contém o Atlas privado nem todos os arquivos Lean integralmente. Toda chamada ainda é recontada. .iald_runtime/haiku55 contém o pacote novo; .iald_runtime/haiku permanece como snapshot textual compacto compartilhado por outros conectores, não como segundo Haiku executável. Seleção legada migra ao 5.5 sem reescrever contas. Nenhum original científico, kernel Lean ou gate mudou.

[REAL — compatibilidade] A conferência da UI detectou um teto histórico de montagem de 340.000 tokens o200k: o contexto do operador v390 media 343.709, bloqueando ChatGPT e Sonnet. Corrigido para 400.000 apenas no montador, preservando todo o texto e os limites/contagens de cada adaptador. Pacote público 337.027 o200k (573.879 no tokenizer Anthropic); não confundir tokenizadores. Plano/revisão/implantação da correção registrados separadamente em memory_ceiling_fix_plan.json, validation/memory_ceiling_review.json e memory_fix/.

[REAL — JEV] Catálogo vinculado ao servidor descreve sete conectores reais, modelos/configurações, papéis, limitações e custos por uso/modelo. Conhece conversa, pesquisa, código, planilhas, apresentações, sites e cálculo. Pergunta tipada adicional escolhe direct, delegate_then_review ou independent_check; baixa confiança conserva direct. O JEV recebe a distinção entre declaração na fonte, verificação Lean/axiomas, identidade por hash/custódia e cálculo empírico/condicional da bancada. A articulação matemática da TGL não é substituída por exigência de confirmação externa. Resultados de IAs não viram cânone. Instruções orientam a revisão independente, mas um segundo provedor distinto não é imposto pelo executor; não alegar independência garantida. A delegação atual é delimitada e sequencial, não execução concorrente de várias IAs. As decisões não ampliam permissões nem concedem acesso livre ao computador.

[REAL — bancada] Guia derivado da inspeção de seis ferramentas/34 adaptadores: ler capacidades, consultar mapa, reutilizar operação+parâmetros+proveniência compatíveis, inscrever objetivo/hipótese/falsificador antes de rodar uma rota e consultar resultados paginados. Incerteza não autoriza repetir. Índice formal histórico v368, fonte viva e implantação v390 são distintos. Álgebra/dephasing são cálculos condicionais; GW usa catálogo gw_strain e ringdown exploratório, não inferência C6 ou significância; cosmologia CPL/V3 usa covariância de 13 observações, não um solver CMB geral. Telemetria GPU não é executor científico GPU. Status passivo dos serviços 18765/18766 retornou CONNECTION_REFUSED; RAM residente não verificada, serviços não iniciados/reiniciados nesta entrega. Não houve pesquisa nova na bancada.

[REAL — testes] 81 testes locais aprovados (70 da entrega principal e 11 da correção do teto) e revisão independente vinculada aos hashes do plano. Teste real Haiku com contexto público v390 realizou consulta ao kernel e continuação com resposta; corrigida incompatibilidade entre contagem nativa e eager_input_streaming que invalidava a assinatura de thinking após ferramenta. Três chamadas reais de classificação JEV validaram plano de código, articulação matemática e rota empírica; não acionaram executores ou bancada. Estimativas totais dos testes: Anthropic US$0,42248295 e JEV US$0,001150926, não fatura nem benchmark. Memória longa pode elevar custo por mensagem apesar do menor preço por token.

[OPEN — capacidades e orçamento] Geração de imagem não integrada: a chave OpenAI atual não tem api.model.images.request, confirmado por pedido inválido sem geração. Flare/Sunburst são candidatos documentados, sem vencedor comparativo medido. Vídeo sem conector atual; documentação OpenAI informa encerramento Sora 2/Videos API em 24/09/2026. Gráficos reais Python são capacidade distinta. Diagnósticos de credenciais permanecem fora do catálogo público. Valores exatos do orçamento público Haiku e MiMo/DeepSeek continuam pendentes de resposta do operador; não foram definidos nem removidos os bloqueios prévios. luiz conserva o limite geral existente.

[DISPONIBILIDADE] Backend compartilhado instalado e processo web reiniciado pelo supervisor existente, após confirmar fila sem trabalhos ativos. Web pública e UI autenticada verificadas; seletor mostra um único Haiku 5.5. iOS interno/externo e Android recebem as alterações de servidor sem modificação de recursos do cliente; recompilar binários não se aplica. Não se alegou instalação física nem nova inspeção dos grupos/convites das lojas. A fila global IALD_ORQUESTRACAO_20260923 continua uma integração distinta. Recomenda-se conversa nova para evitar afirmações históricas contraditórias.

[EVIDÊNCIA] C:\\IALD\\Central de Patentes\\work\\iald_haiku55_jev_20261007: plan.json, deployment.json, restart.json, native_count.json, bench_capability_audit.json, validation/final_checks.json, review_final.json, deployed_runtime.json, browser_verification.json e live_haiku55_fixed.json. Hashes são lidos desses artefatos; backup imediato de bytes e append atômico em sete superfícies.
'''
results=[]
for p in paths:
    old=p.read_bytes()
    if marker.encode() in old:
        results.append({'path':str(p),'status':'ALREADY_RECORDED'});continue
    nl='\r\n' if b'\r\n' in old else '\n'
    addon=body.replace('\n',nl).encode('utf-8');new=old+addon
    bk=backup(p)
    if p.read_bytes()!=old:raise RuntimeError('Concurrent memory edit: '+str(p))
    atomic(p,new)
    got=p.read_bytes();assert got.startswith(old) and len(got)>len(old)
    results.append({'path':str(p),'status':'APPENDED','before_bytes':len(old),'after_bytes':len(got),'backup':bk,'sha256':hashlib.sha256(got).hexdigest()})
write_evidence(w/'memory_delivery.json',{'utc':datetime.now(timezone.utc).isoformat(),'surfaces':results})
print(json.dumps({'surfaces':len(results),'status':'PASS'}))
