from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out = root / 'REVISOES_RAIZ_073_20260910'
source = root / 'COMUTANTE_FOCK_SUAVE_073_20260910/COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md'

def pin(p):
    raw = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

before = pin(source)

def new(p, value):
    assert p.resolve().is_relative_to(root) and not p.exists()
    raw = value.encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return pin(p)

note = '''# Parecer da raiz — comutante no domínio Fock suave

10/09/2026. [DERIVED — revisão matemática por leitor distinto do autor] [REAL — leitura integral e pins]. Favorável no alcance condicional indicado. Não houve Lean/CAS, execução de um.py ou alteração de qualquer fonte.

O suporte temporal de [L,chi]Psi, junto à compacidade de S3, torna o teste da fórmula (2.1) compacto. As duas soluções de Green têm diferença Psi, incluindo o bloco auxiliar algébrico. A faixa inteira de Cauchy permite, portanto, acessar todos os dados suaves. A polarização pura e a conjugação separam os criadores e aniquiladores quando os testes são complexificados. Isso não é uma afirmação sobre a comutante de uma região espacial própria.

O núcleo comum dos aniquiladores no domínio de partículas finitas suaves contém somente o vácuo: as contrações de cada componente de número positivo contra todos os vetores suaves anulam sua função de onda. A forma auxiliar indefinida não atrapalha, porque sua simetria fundamental é invertível e fornece o mesmo conjunto completo de aniquiladores Hilbert. Assim B Omega=c Omega, e a comutação com criadores determina B nas palavras simples.

A passagem ao domínio completado usa a hipótese correta: continuidade de B em cada grau nuclear, com imagem numa soma finita de graus. Os tensores simples são densos nessa topologia e o contradomínio é Hausdorff. Densidade apenas Hilbert não foi usada para um operador arbitrário. Os coeficientes Wick polinomiais da fonte Fock satisfazem a hipótese que se consome aqui.

Na recorrência formal, os coeficientes de ordens menores de B são escalares, de modo que suas contribuições aos comutadores na próxima ordem somem. Isso prova a comutante escalar formal. A identidade [Q,[Q,A]_gr]_gr=[Q²,A] para Q ímpar e d=i[Q,.]/hbar tem o fator correto -hbar^{-2} na segunda derivação. Q² torna-se escalar sob implementação e d²=0; sobre C[[z]] de ghost zero, sua graduação +2 o força a zero.

A restrição do anel importa: fontes centrais de ghost não nulo podem produzir um escalar de ghost2. O corolário é aplicado depois da especialização dessas fontes, não à álgebra estendida072 sem outra demonstração.

O argumento da supercomutante ímpar também confere: T Omega teria de ser simultaneamente múltiplo de um vácuo par e ímpar, logo é zero; depois vêm criadores e continuidade. A involução graduada torna Q-Q^times supercentral. Sua anulação é condicional à existência do adjunto no domínio comum e à identidade de involução. Não demonstra conservação da corrente ou existência do implementador, nem auto-adjunticidade Hilbert da carga.

Precisão tipográfica aditiva: na equação (3.3) da fonte há uma vírgula entre B e a palavra de criadores. A identidade demonstrada é B(a†(v1)...a†(vN)Omega)=c a†(v1)...a†(vN)Omega. A vírgula não representa um bracket; o texto anterior e posterior fixa essa leitura. A fonte congelada não foi alterada.

Na notação dos domínios, a simetrização graduada indica a projeção do tensor nuclear de N slots sobre seu setor simétrico/exterior, seguida da soma algébrica sobre N. Não se aplica uma segunda potência simétrica que produzisse N² slots.

Este resultado remove uma condição não demonstrada de comutante no domínio efetivamente construído, mantendo como hipóteses a implementação de d_z, sua nilpotência/QME e a carga renormalizada. Não foi contado como prova da interação livre de anomalias.
'''
op = new(out / 'PARECER_COMUTANTE_SUAVE_073.md', note)
assert pin(source) == before
rp = new(out / 'REGISTRO_PARECER_COMUTANTE_073.json', json.dumps({
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'FAVORABLE_INTERNAL_REVIEW__IMPLEMENTATION_AND_QME_STILL_CONDITIONAL',
    'source': before, 'review': op, 'source_unchanged': True,
    'new_cas_controls': 0, 'new_lean_compilations': 0}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'review': op, 'receipt': rp}, ensure_ascii=True))
