from pathlib import Path
import datetime, hashlib, json, os
R = Path(__file__).resolve().parent
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def put(p, b):
    assert p.is_relative_to(R) and not p.exists() and b
    t = p.with_name(p.name + '.tmp')
    t.write_bytes(b)
    assert t.read_bytes() == b
    os.replace(t, p)
p = R/'k/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean'
s = p.read_text(encoding='utf8')
start = s.index('protected theorem IsSelfAdjoint.commute_cfc {')
end = s.index(' :=', start)
statement = s[start:end]
line = s[:start].count('\n') + 1
assert line == 87 and 'commute_cfcHom' not in statement
d = dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    status='CORRECTION_BESIDE_HISTORICAL_FICHE__NO_LEAN_CHANGE',
    supersedes_provider_zero_of=pin(R/'ADENDO_FICHA_COMUTACAO_CFC.json'),
    historical_md=pin(R/'ADENDO_FICHA_COMUTACAO_CFC.md'),
    source=pin(p), providers=[dict(name='IsSelfAdjoint.commute_cfc', line=line, statement=statement)],
    reason='O adendo anterior nomeava commute_cfc mas transcrevia commute_cfcHom. Corrigidos localizador e enunciado; os bytes anteriores são preservados como histórico. Nenhuma fonte ou compilação Lean foi alterada.')
stem='ADENDO_FICHA_COMUTACAO_CFC_CORRECAO'
put(R/(stem+'.json'), json.dumps(d, ensure_ascii=False, indent=2).encode('utf8'))
md='[REAL — correção documental ao lado; sem mudança Lean]\n\n# Correção da referência de comutação CFC\n\n'+d['timestamp']+'\n\n'+d['reason']+'\n\n'+str(p)+':'+str(line)+'\n\n```lean\n'+statement+'\n```\n\nO segundo fornecedor, Commute.cfcₙ_nnreal, permanece como no adendo anterior. O P2 foi documental; a construção já usava commute_cfc. Esta correção não é uma alegação de ficha anterior ao código: a ficha histórica permanece visível.\n'
put(R/(stem+'.md'), md.encode('utf8'))
print(json.dumps(d, ensure_ascii=False))
