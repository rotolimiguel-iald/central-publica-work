from pathlib import Path
import hashlib,json,os,re,datetime
R=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
run=(R/'run_absorption_replay.py').read_text(encoding='utf8')
for a,b in [('AUDITORIA_ACAO_CORE_A1B','AUDITORIA_ABSORCAO_A1B'),('V351RegularFlowAbsorption','V351FourierTranslation'),('AuditA1Absorption','AuditA1FourierTranslation'),('absorption_attempts','fourier_translation_attempts')]:run=run.replace(a,b)
put(R/'run_fourier_translation_replay.py',run.encode('utf8'))
audit=(R/'audit_absorption.py').read_text(encoding='utf8')
for a,b in [('V351RegularFlowAbsorption','V351FourierTranslation'),('AuditA1Absorption','AuditA1FourierTranslation'),('BadAbsorptionTime','BadFourierTranslationSign'),('absorption_attempts','fourier_translation_attempts'),('audit_absorption','audit_fourier_translation'),('len(targets)==6','len(targets)==3'),("t['kind']=='theorem' for t in targets)==4","t['kind']=='theorem' for t in targets)==3"),('AUTHOR_STANDALONE_ABSORPTION_PASS','AUTHOR_STANDALONE_FOURIER_TRANSLATION_PASS'),('new_theorems=4','new_theorems=3'),('new_definitions=2','new_definitions=0'),('AUDITORIA_ABSORCAO_A1B','AUDITORIA_FOURIER_TRANSLACAO_A1B')]:audit=audit.replace(a,b)
put(R/'audit_fourier_translation.py',audit.encode('utf8'))
# Append-only correction: two original fiche excerpts stopped at a named binder (:=).
# Preserve the original fiche and give all provider declarations with balanced delimiters.
old=json.loads((R/'REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO.json').read_text(encoding='utf8'))
rows=[]
for q in old['providers']:
    p=Path(q['source']['path']);s=p.read_text(encoding='utf8')
    start=re.search(r'^(?:def|theorem|lemma) '+re.escape(q['name'])+r'(?:\s|\()',s,re.M).start()
    depth=0;end=None
    for i in range(start,len(s)):
        c=s[i]
        if c in '([{':depth+=1
        elif c in ')]}':depth-=1
        if depth==0 and (s.startswith(' :=',i) or s.startswith(' where',i)):
            end=i;break
    assert end is not None
    rows.append(dict(name=q['name'],source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end]))
search=Path(old['searches']['path']);queries=json.loads(search.read_text(encoding='utf8'))
acervo=next(q for q in queries if q['label']=='acervo')
text=Path(acervo['stdout']['path']).read_text(encoding='utf8')
headers=[s[:500] for s in text.splitlines() if s.startswith('===')]
# Bounded snippets, to avoid reproducing an entire one-line index dump.
matches=[]
for m in re.finditer(r'(?i)fourier.{0,120}translation|fourier.{0,120}characterMultiplier|shift.{0,120}fourier|fourier_shift|regular_unitary_positive_generator',text):
    matches.append(text[max(0,m.start()-100):m.end()+120])
doc=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='DOCUMENTARY_CORRECTION__EXACT_PROVIDER_STATEMENTS',original_fiche=pin(R/'REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO.json'),providers=rows,acervo_headers=headers,bounded_matching_snippets=matches[:30],matched_snippets_total=len(matches),scope='Original regex excerpts prematurely stopped at named arguments in two providers. Full declarations supplied here without editing the previous fiche. Broad acervo regex matched long index/log lines; bounded snippets below do not assert a complete missing-provider search.')
put(R/'ADENDO_FICHA_FOURIER_TRANSLACAO.json',json.dumps(doc,ensure_ascii=False,indent=2).encode('utf8'))
s='[REAL — correção documental ao lado; não acrescenta teorema]\n\n# Tipos completos da ficha Fourier/translação\n\nO extrator anterior cortou dois enunciados no := de um argumento nomeado. A ficha original sobrevive intacta. Abaixo estão as declarações completas, extraídas respeitando os delimitadores; os caminhos e hashes continuam os dos fornecedores. A busca ampla do acervo atingiu quatro arquivos de índice/log, cinco trechos, e não localizou uma declaração Lean substitutiva. O recorte da busca permanece explícito.\n\n'
for q in rows:s+=f"`{q['source']['path']}:{q['line']}` — `{q['source']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
put(R/'ADENDO_FICHA_FOURIER_TRANSLACAO.md',s.encode('utf8'))
print(json.dumps(dict(provider_count=len(rows),acervo_headers=headers,bounded_matching_snippets=matches[:6]),ensure_ascii=False))
