from pathlib import Path
import os
R=Path(__file__).resolve().parent
def put(p,s):
 assert p.is_relative_to(R) and not p.exists()
 b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
changes={'modular_cut_balance':'quadratic_trace','ModularCutBalance':'QuadraticTrace',
 'MODULAR_CUT_BALANCE':'QUADRATIC_TRACE','AUDITORIA_BALANCO_DOS_CORTES_A1B':'AUDITORIA_TRACIALIDADE_QUADRATICA_A1B',
 'AUDITORIA_IMPLEMENTADOR_MODULAR_A1B':'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO'}
for old in ['run_modular_cut_balance_replay','validate_modular_cut_balance']:
 s=(R/(old+'.py')).read_text(encoding='utf8')
 for a,b in changes.items():s=s.replace(a,b)
 if old.startswith('run_'):
  s=s.replace("['V351QuadraticTrace.lean', 'AuditA1QuadraticTrace.lean']","['V351QuadraticTrace.lean', 'V351RegularCoreTraceConstruction.lean', 'AuditA1QuadraticTrace.lean']")
 put(R/(old.replace('modular_cut_balance','quadratic_trace')+'.py'),s)
 print(old.replace('modular_cut_balance','quadratic_trace')+'.py')
