from pathlib import Path
from datetime import datetime
import hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'square_resolvent_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m,c=load(RUN/'manifest.json'),load(RUN/'compilation.json')
assert c['complete'] and all(v is True for v in c.values() if isinstance(v,bool))
assert c['exact_6_targets'] and len(m['declarations'])==6
d=m['sources']['TGLV350/SquareResolventSupport.lean']
assert hf(d['path'])==hf(d['snapshot'])==d['sha256']
assert hf(d['author_binary'])==c['records'][0]['output_sha256']==d['author_binary_sha256']
for p,h in m['readonly_pins'].items():assert hf(p)==h
date=datetime.now().astimezone();tag=date.strftime('%Y%m%d_%H%M%S_%f')
targets='\n'.join('- `'+x+'`' for x in m['declarations'])
text=f'''# Revisão DEV — resolvente quadrático e suporte

## Estrato parcial de seis alvos — {date.isoformat()}

SQUARE_RESOLVENT_DEV_REVIEW

[REAL — leitura integral e recompilação independente.] **Nenhum P0–P2 identificado** em `kernel/TGLV350/SquareResolventSupport.lean`. O escopo deste aceite é somente a fonte congelada de seis alvos; não inclui aplicações aos pares, diferenças de quadrados ou integração futura.

**Tipos e composição.** H é Hilbert complexo completo; A é CLM em TODO H. Todas as seis conclusões recebem explicitamente `star A = A`. A definição da linha 15 é total, `positiveResolvent (((n:ℝ)+1) • (A*A))`; suas leis não atribuem positividade a um A arbitrário. `A*A` é composição, convertida em A* A pela auto-adjunticidade, e não uma troca tácita de operador.

- Linhas 26–42: positividade e cota R_n≤I seguem da positividade de (n+1)A². A ordem dos coeficientes é crescente; a ordem das inversas é antítona. O primeiro coeficiente é 1, inclusive n=0.
- Linhas 44–51: A comuta com o denominador por álgebra; `ring_inverse_commutes_of_unit` exige IsUnit, descarregada por `one_add_strictlyPositive`. Não se inverte A nem se presume gap.
- Linhas 54–70: a energia é exatamente `(n+1)||R_n(A v)||²≤||v||²/4`. O lema genérico `positiveResolvent_energy_bound` de `DualResolvent.lean:74` vem da equação (I+C)r=v e Cauchy–Schwarz, sem hipótese do peso dual. Simetria de A converte Re⟨r,A²r⟩ em ||Ar||²; a comutação já provada troca AR_n v por R_n Av. Coerções ℝ→ℂ e orientação dos produtos internos foram conferidas.
- Linhas 72–88: para cada k fixo, a energia limita k||LAv||² passando ao limite forte. A hipótese de valor positivo é estabelecida antes da divisão no argumento arquimediano. O auxiliar recebe o limite como hipótese; a declaração final o constrói, portanto não há hipótese residual de convergência forte no resultado público.
- Linhas 91–105: `vonNeumann_antitone_contraction_limit` fornece L no filtro atTop de ℕ, dirigido e não vazio. `generatedAlgebra Set.univ` e `generator_mem (Set.mem_univ ...)` descarregam a pertinência de TODOS os R_n à mesma VNA. Isso evita depender de uma instância `Top` inexistente e não acrescenta premissa sobre A. L anula Ran A pela energia; seu núcleo é fechado porque L é CLM. `closure_minimal` dá Lx=0 no fecho da imagem e, então, R_n x→0.

**Suporte correto.** O alvo é `closure (Set.range A)` no H normado, não apenas Ran A nem suporte de outro operador. Como A=A*, não há discrepância entre Ran A e Ran A* aqui. Não se permite retirar hA e manter a mesma conclusão para A* A sem examinar o suporte. Não se conclui convergência a zero em todo H ou em norma de operador, nem se usa separabilidade, injetividade ou gap. Nenhuma PVM foi construída. A infraestrutura de inversos positivos e limites já compilada foi reaproveitada; isso não elimina suas dependências transitivas de CFC.

**Reprodução própria:**

| Execução própria | rc | segundos |
|---|---:|---:|
| SquareResolventSupport | {c['records'][0]['returncode']} | {c['records'][0]['seconds']} |
| Auditor6, tipos com universos e axiomas | {c['records'][1]['returncode']} | {c['records'][1]['seconds']} |

Os seis alvos imprimiram exclusivamente `propext`, `Classical.choice`, `Quot.sound`; o mapa coincide exatamente com o stdout final autoral. Três auxiliares privados e a definição do resolvente estão cobertos transitivamente. Não foi aceito `sorry`, `axiom` novo, `unsafe` ou manipulação de redutibilidade na fonte. O .olean próprio é byte a byte igual ao autoral final.

- Fonte SHA256: `{d['sha256']}`.
- .olean próprio = autoral: `{d['author_binary_sha256']}`.
- Log final: `{Path(d['author_log']).name}`, SHA `{d['author_log_sha256']}`.
- Stdout autoral: `{d['author_stdout_sha256']}`; stderr vazio.
- Auditor próprio: `{c['records'][1]['stdout_sha256']}`.

Evidência: `{RUN.relative_to(ROOT)}/manifest.json` e `compilation.json` (SHA `{hf(RUN/'compilation.json')}`), fontes congeladas, logs próprios e histórico autoral na mesma pasta. {len(m['dependencies'])} dependências de projeto foram copiadas exclusivamente de árvores próprias com hashes conferidos: 329 da árvore `bidual_support_final_independent_20260913_042239_895782` e duas do catálogo `matrix_root_independent_20260912_182039_835827` (`PositiveRootIntertwining` e `ScaledPositiveResolvent`). Origens anteriores individuais constam do manifesto. LEAN_PATH contém uma única raiz própria de projeto e oito pacotes externos readonly; {len(m['external_direct_pins'])} pins diretos externos herdados foram relidos. Sem recompilar dependências/pacotes e sem usar build autoral no LEAN_PATH. Não houve reauditoria binária de toda a biblioteca externa.

**Histórico recusado.** `_044527_655878` é rc1: ordem da adição no coeficiente, coerção/rewrite do produto interno, ausência de `Top (VonNeumannAlgebra H)` e consequência no limite. Seus prints parcialmente no trio não foram aproveitados; os prints com `sorryAx` também foram rejeitados. Log e streams foram preservados em `author_history`. A única versão aceita é a fonte final acima; a reprodução própria passou sem correções de fonte ou alteração de orçamento.

**Custódia e limite.** Mãe `bidual_right_support_custody.json`, SHA lido `{m['parent_custody_sha256']}`, confrontado com sua verificação. Fonte/binário do autor, dependências próprias, pins externos e cópia/gate da mãe permaneceram iguais durante a execução. A mãe conserva seis flags falsas; não foi repetida auditoria das 34 memórias. Nenhuma escrita em fontes, originais, integração ou memórias; nenhum monólito/recorder/integrador/teste autoral executado. Não existe aceite integrado nesta nota.

**Seis alvos auditados:**

{targets}

[OPEN] Aplicação aos pares direitos, identidade de diferenças de quadrados, densidade desses quadrados no gráfico, teste ponderado/multiplicador, inclusão inversa por J, KMS e traço não são resultados deste módulo. A revisão DEV6 está encerrada; módulos posteriores exigem novo congelamento e adendo, preservando este estrato.
'''
p=REV/'REVIEW_SQUARE_RESOLVENT_DEV.md';b=text.encode('utf-8');before=b'';backup=None
if p.exists():
    before=p.read_bytes();backup=p.with_name(p.name+'.bak_'+tag);backup.write_bytes(before);assert backup.read_bytes()==before;b=before+b'\n\n'+b
tmp=p.with_name(p.name+'.tmp_'+tag);tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p);assert p.read_bytes()==b
pin={'timestamp':date.isoformat(),'review_path':str(p),'review_sha256':hf(p),'review_bytes':len(b),'complete_DEV6':True,'integrated_review':False,'backup':str(backup) if backup else None,'prefix_bytes':len(before),'compilation_sha256':hf(RUN/'compilation.json'),'P0':[],'P1':[],'P2':[]}
q=RUN/'review_pin.json';assert not q.exists();tmp=q.with_suffix('.json.tmp');raw=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,q)
print(json.dumps(pin,ensure_ascii=False))
