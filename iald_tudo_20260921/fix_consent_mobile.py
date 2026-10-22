from pathlib import Path
from datetime import datetime
import hashlib, json, os

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
changes = {}
def load(name):
    p = ROOT / 'app' / name
    raw = p.read_bytes()
    return p, raw, raw.decode('utf-8').replace('\r\n', '\n')
def save(p, raw, s):
    data = s.replace('\n', '\r\n').encode('utf-8') if b'\r\n' in raw else s.encode('utf-8')
    assert p.read_bytes() == raw, 'Concurrent modification'
    backup = p.with_name(p.name + '.bak_' + stamp)
    backup.write_bytes(raw)
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data and len(data) > len(raw) * .9
    os.replace(tmp, p)
    changes[str(p)] = {'before':hashlib.sha256(raw).hexdigest(),'after':hashlib.sha256(data).hexdigest(),'backup':str(backup)}

p, raw, s = load('index.html')
old = '''      <div class="lista-botoes">
        <button class="btn-linha btn-consentir" id="btn-consentir">Concordo e continuar</button>
        <button class="btn-linha" id="btn-recusar-consentimento">Agora não</button>
      </div>'''
new = '''    </div>
    <div class="consentimento-acoes">
      <p id="consentimento-status" role="status" aria-live="polite" hidden></p>
      <div class="lista-botoes">
        <button type="button" class="btn-linha btn-consentir" id="btn-consentir">Concordo e continuar</button>
        <button type="button" class="btn-linha" id="btn-recusar-consentimento">Agora não</button>
      </div>'''
assert s.count(old) == 1
save(p, raw, s.replace(old, new))

p, raw, s = load('iald.css')
s += '''
/* Consent: constrain the sheet to the visible viewport, with persistent actions. */
#folha-consentimento {
  bottom: auto;
  top: var(--topo-util, 0px);
  height: var(--altura-util, 100dvh);
  box-sizing: border-box;
  grid-template-rows: minmax(0, 1fr);
}
#folha-consentimento .folha {
  min-height: 0;
  max-height: min(46rem, 100%);
}
#folha-consentimento .folha-topo,
#folha-consentimento .consentimento-acoes { flex: 0 0 auto; }
#folha-consentimento .folha-corpo {
  min-height: 0;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  overflow-wrap: anywhere;
}
.consentimento-acoes {
  padding: 12px max(16px, var(--safe-r)) 16px max(16px, var(--safe-l));
  border-top: 1px solid var(--borda);
}
.consentimento-acoes .btn-linha { min-height: 44px; touch-action: manipulation; }
#consentimento-status { margin: 0 0 10px; overflow-wrap: anywhere; }
@media (max-width: 699px) {
  #folha-consentimento { padding-top: calc(var(--safe-t) + 12px); }
  #folha-consentimento .folha { max-height: 100%; }
}
'''
save(p, raw, s)

p, raw, s = load('iald.js')
old = "  S.consentimentoFolha = provedor ? { provedor: String(provedor), versao } : null;\n  abrirFolha('folha-consentimento');"
new = """  S.consentimentoFolha = provedor ? { provedor: String(provedor), versao } : null;
  estadoConsentimento('');
  // Close the keyboard before measuring the sheet on iOS.
  if (document.activeElement && typeof document.activeElement.blur === 'function') document.activeElement.blur();
  abrirFolha('folha-consentimento');"""
assert s.count(old)==1
s=s.replace(old,new)
s=s.replace("    r = await postarJSON('/api/motor/consentimento', corpo);", """    r = await fetchIALD('/api/motor/consentimento', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo), signal: AbortSignal.timeout(15000),
    });""")
s=s.replace("    avisar('Sem conexão com o servidor: nada foi alterado.', 'erro');\n    return false;", "    estadoConsentimento('Não foi possível confirmar o aceite. Confira a conexão e tente novamente.');\n    return false;",1)
old="""    avisar(j.error || `O servidor recusou (HTTP ${r.status}).`, 'erro');
    if (r.status === 409) { fecharFolhas(); carregarMotor(); }
    return false;
  }
  const doMotor = S.motor && S.motor.consentimento;"""
new="""    estadoConsentimento(j.error || `O servidor recusou (HTTP ${r.status}). Tente novamente.`);
    if (r.status === 409) {
      // Read the new notice; never apply the previous click to changed terms.
      await carregarMotor();
      const atual = consentimentoDe(S.motor);
      if (atual.texto && atual.provedor && Number.isInteger(atual.versao)) {
        abrirConsentimento(atual.texto, atual.provedor, atual.versao);
        estadoConsentimento('O modelo ou os termos mudaram. Leia o aviso atualizado e decida novamente.');
      }
    }
    return false;
  }
  if (j.ok !== true || j.consentido !== aceito || (provedor && j.provedor !== provedor)) {
    estadoConsentimento('O servidor não confirmou esta autorização. Entre novamente ou tente de novo.');
    return false;
  }
  const doMotor = S.motor && S.motor.consentimento;"""
assert s.count(old)==1
s=s.replace(old,new)
start=s.index('async function consentirEContinuar() {')
end=s.index('\nasync function alternarConsentimento()',start)
s=s[:start]+'''function estadoConsentimento(texto) {
  const status = document.getElementById('consentimento-status');
  if (status) { status.textContent = texto; status.hidden = !texto; }
  if (texto) avisar(texto, 'erro');
}

async function consentirEContinuar() {
  if (S.consentimentoEnviando) return;
  const folha = S.consentimentoFolha || {};
  if (!folha.provedor || !Number.isInteger(folha.versao)) {
    estadoConsentimento('O aviso está incompleto. Feche e abra novamente os termos antes de aceitar.');
    return;
  }
  S.consentimentoEnviando = true;
  const botao = document.getElementById('btn-consentir');
  botao.disabled = true;
  botao.textContent = 'Confirmando…';
  estadoConsentimento('');
  try {
    if (!(await responderConsentimento(true, folha.provedor, folha.versao))) return;
    fecharFolhas();
    const bolha = S.avisoConsentimento;
    S.avisoConsentimento = null;
    if (bolha) { bolha.remove(); reenviarUltima(); }
    else avisar('Autorização confirmada. Você já pode conversar.');
  } finally {
    S.consentimentoEnviando = false;
    botao.disabled = false;
    botao.textContent = 'Concordo e continuar';
  }
}
''' + s[end:]
save(p,raw,s)
receipt=Path(__file__).parent / ('consent_fix_'+stamp+'.json')
receipt.write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(receipt)
