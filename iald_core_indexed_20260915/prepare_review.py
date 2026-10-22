"""Generate a reviewable change report from measured artifacts, without deployment."""
import difflib
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
report = json.loads((WORK/'verification.json').read_bytes())
old = json.loads((WORK.parent/'iald_mother_kernel_20260915/verification_narrow.json').read_bytes())
current = report['checks'][0]['context_tokens']
before = old['context_tokens']
files = list(json.loads((WORK/'prepared.json').read_bytes())['baseline'])
changes = []
for name in files:
    live = ROOT/name
    baseline = json.loads((WORK/'prepared.json').read_bytes())['baseline'][name]
    actual = hashlib.sha256(live.read_bytes()).hexdigest() if live.exists() else None
    assert actual == baseline, 'Production changed concurrently: '+name
    if name.endswith('.py'):
        compile((WORK/name).read_bytes(), name, 'exec')
    if live.exists():
        changes.extend(difflib.unified_diff(live.read_text(encoding='utf-8').splitlines(True),
                       (WORK/name).read_text(encoding='utf-8').splitlines(True), fromfile='production/'+name,
                       tofile='prepared/'+name))
with (WORK/'integration.diff').open('x',encoding='utf-8') as handle:
    handle.write(''.join(changes))
text = f'''# Núcleo IALD v357 — integração preparada

**Estado: validado localmente; ainda não ativado no aplicativo.**

A referência corrente é **v357**. A seção v334 do documento recebido permanece intacta
como retrato histórico. O programa da publicação é vinculado por SHA-256 à seleção v357;
uma troca de arquivo não passa silenciosamente por nova versão autorizada.

## Conteúdo e integridade

| Camada | Tratamento |
|---|---|
| IALD_Kernel_v5.txt | Integral em cada contexto preparado; original preservado |
| IALD_TGL_MEMORY_CORE_v1_20260915.md | Integral, cópia idêntica em bytes; original preservado |
| Lagrangiana, equação mestra, H≥0, Lindblad, fase, comutação | Mantidos no núcleo e complemento matemático |
| Cinco fontes Lean de H1/H2/H3 | Inteiras no contexto, com fonte e escopo |
| Sete documentos científicos | Inteiros no servidor; busca e leitura paginada com hash e URL |
| Atlas e kernel Lean completo | Ferramentas existentes preservadas; Atlas privado restrito |

As conciliações são explícitas, ao lado do conteúdo original: v334/v357; G_rot²=-I versus
G_proj²=G_proj; J antiunitário versus involuções auxiliares; Pi± versus C±; face hiperbólica
versus leitura angular; dephasing puro versus hipótese de estado fixo único; identidade
da interface versus capacidades reais do motor. Nenhuma inferência é ratificada
automaticamente como cânone.

## Medições e testes

- Contexto anterior preparado com v5: **{before:,} tokens**.
- Novo contexto do operador: **{current:,} tokens** — redução de **{(1-current/before)*100:.1f}%**.
- Contexto público: **{report['checks'][2]['context_tokens']:,} tokens**, sem Atlas privado ou diário.
- Sete documentos reconstruídos integralmente por **{sum(d['pages'] for d in report['documents'])} páginas**, sem perda de texto.
- Oito consultas de conceitos localizaram trechos com posições e proveniência.
- **18 testes de integridade, isolamento e roteamento passaram**.
- **53 verificações das rotas de testadores passaram**. Duas expectativas antigas foram
  atualizadas para incluir exatamente search_tgl e fetch_tgl; a restrição do Atlas permaneceu.
- Sintaxe dos módulos preparada e conferida; hashes dos arquivos de produção continuam no baseline.

A redução acima é de contexto medido, não promessa de latência, qualidade ou custo faturado.
Esta implementação usa **busca lexical local** e as ferramentas existentes. Não foi criado
Vector Store remoto, Conversations API nem servidor MCP. Essas integrações podem ser feitas
depois sem substituir a fonte canônica.

## Ativação pendente

O teste externo e a ativação do v5 aguardam autorização específica de envio à
**api.openai.com**. A revisão automática anterior rejeitou a autorização genérica
“faça tudo” para o conteúdo integral do v5. O teste proposto usa v5 + novo MD + fontes
públicas, sem Atlas privado, com teto de **US$ 0,03** e preservando o limite global.

Após autorização: avaliar a resposta real, aplicar os arquivos com backups de bytes e
checagem de concorrência, executar a regressão obrigatória e reiniciar somente o web.
O modelo nativo, pesos, documentos científicos e arquivos originais não são alterados.
Nenhuma instalação móvel ou publicação nas lojas foi realizada nesta etapa.

Evidências: verification.json, free_staged_updated_expectations.log, test_indexed_core.py,
integration.diff e prepared.json, nesta pasta.
'''
with (WORK/'REVISAO_NUCLEO_V357.md').open('x',encoding='utf-8') as handle:
    handle.write(text)
print(json.dumps({'review': str(WORK/'REVISAO_NUCLEO_V357.md'), 'production_baseline_unchanged': True,
                  'context_reduction_percent': round((1-current/before)*100,1)}))
