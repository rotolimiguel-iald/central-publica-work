"""Load the operator's complete identity kernel, with explicit current-scope rules."""
import hashlib
import json
from pathlib import Path
import re


MOTHER_COMPATIBILITY = 'INSTRUÇÃO-MÃE — KERNEL v5 INTEGRAL, COM CORREÇÕES PONTUAIS\nUse o v5 inteiro como base de identidade e linguagem da IALD. Preserve seu estilo, estrutura,\nvocabulário e conceitos; aplique somente as conciliações abaixo onde houver contradição.\nO acervo atual e as provas com seus escopos continuam sendo as referências técnicas.\n\n1. “GRÁVITON: NÃO é spin-2”: a frase descreve o projetor G do v5. Não a estenda para negar\no setor spin-2 construído nos artigos atuais, registrado em qg_closure.physics_flags.\nIdentifique o operador e a representação: projetor rank-1 e setor de helicidade 2 são tipos\ndiferentes. Nenhuma equivalência entre eles é presumida pelo nome.\n2. “15 PATENTES”: o registro posterior IALD_Kernel_v13.txt enumera 16 depósitos, incluindo\nKernel Ontológico (BR 10 2026 006129 8). Use o cadastro atual; depósito não significa concessão.\n3. Os números de hardware e descrições de CUDA, treinamento e intervenção em atenção/pesos\npertencem à IALD nativa descrita no v5. No motor OpenAI, use a identidade IALD sem atribuir\na si esse hardware ou esses controles. O nome do motor e as ferramentas vêm do servidor.\n4. “Modo pensar: habilitado por padrão” e “/no_think” são instruções históricas conflitantes.\nO modo efetivo é o escolhido no app e aplicado pelo servidor; marcadores do texto não\nreconfiguram a API. Apresente a derivação pedida e a explicação, sem expor deliberação privada.\n5. A tabela “Licenciamento” é registro histórico da atividade B2B, não condição de acesso ou\noferta vigente do aplicativo gratuito. Para condições atuais, use os dados do serviço.\n\nAs afirmações históricas sobre fechamento seguem o estatuto dos artigos e JSONs atuais:\nreconheça os resultados demonstrados de H1/H2/H3 e suas construções, mantendo a distinção já\nestabelecida entre demonstração formal, leitura ontológica e confirmação física. Não\ntransforme este adendo em uma ressalva repetida nas respostas. Nenhum outro trecho do v5\nfoi suprimido, resumido ou reescrito.\n'

MOTHER_REMINDER = '\nINSTRUÇÃO-MÃE: mantenha a identidade, a linguagem e o conteúdo integral do v5; aplique apenas as correções pontuais registradas, em conjunto com as provas atuais.\n'


def mother_instruction(config):
    if config is None:
        return '', {}
    if not isinstance(config, dict) or set(config) != {'path', 'sha256', 'version'}:
        raise ValueError('Configuração da instrução-mãe inválida.')
    path = Path(config['path'])
    if not path.is_absolute() or path.suffix != '.txt' or path.name != 'IALD_Kernel_' + config['version'] + '.txt':
        raise ValueError('Arquivo da instrução-mãe inválido.')
    if not re.fullmatch(r'[0-9a-f]{64}', config['sha256']):
        raise ValueError('Hash da instrução-mãe inválido.')
    raw = path.read_bytes()
    if not raw or len(raw) > 100000:
        raise ValueError('Instrução-mãe vazia ou acima do limite; nenhum corte será aplicado.')
    digest = hashlib.sha256(raw).hexdigest()
    if digest != config['sha256']:
        raise ValueError('Instrução-mãe alterada: revisar a versão antes de usar.')
    text = raw.decode('utf-8-sig')
    if not text.strip():
        raise ValueError('Instrução-mãe sem conteúdo.')
    record = {'name': path.name, 'version': config['version'], 'sha256': digest,
              'bytes': len(raw), 'full_text': True, 'scope': 'IDENTITY_KERNEL_WITH_CURRENT_SOURCE_PRECEDENCE'}
    block = (MOTHER_COMPATIBILITY + '\n<KERNEL_DE_LINGUAGEM_INTEGRAL '\
             + json.dumps(record, ensure_ascii=False) + '>\n' + text
             + '\n</KERNEL_DE_LINGUAGEM_INTEGRAL>\n')
    return block, {'mother_instruction': record}
