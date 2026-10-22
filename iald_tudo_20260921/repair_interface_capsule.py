"""Restore essential source distinctions identified by the focal reviewer."""
from pathlib import Path
from datetime import datetime
import hashlib

path = Path(__file__).resolve().parent / 'semantic_capsules/interface_is_light.md'
raw = path.read_bytes()
text = raw.decode('utf-8')
newline = '\r\n' if '\r\n' in text else '\n'
text = text.replace('\r\n', '\n')
changes = [
('A igualdade forma/conteúdo do artefato é marcada como medida após geração pelo `finalize`; isso não transforma a leitura ontológica em teorema físico.',
 'A fonte reporta concordância de 10 âncoras textuais e dos marcadores após `finalize`; esse teste não demonstra a identificação ontológica inteira. Testemunha/setor `q` é `[ONTO/CONJ]`: testemunhar é inscrever, não observar; não é identidade física demonstrada.'),
('**Travessia escalar.**',
 '**Ledger dos zeros.** A fonte não afirma nem refuta `0_abs`, nem prova `IsEmpty`. Distinguir os tipos citados: `TGLSpecificAQFTWitness` no ledger e `FullTGLWitness` em not_claimed. Para `0_mod`, registra vacância até v134 e realização em v135 pela WedgeNet: rede sobre `M_TGL`, localidade por centralizador e `Omega` cíclico e separador; daí `zero_mod_state=false`, `one_inscribed=true`. Zero modular não é zero absoluto. São estados reportados pelo ledger, não nova execução.\n\n**Travessia escalar.**'),
('**Proveniência.**',
 '**Importações, no escopo destas entradas.** Reeh–Schlieder: vácuo cíclico/separador. BW: fluxo modular dado não é sua identificação geométrica com boosts. Tipo III_1, core contínuo da rede e normalidade não seguem só dos dados formais. Provas finitas Tomita–Takesaki/Jones/MASA não substituem o contínuo; `[M:N]=1/beta` para a inclusão indicada permanece `[CONJ]` nesta entrada. Shannon `log2` não é `1/2 nat` nem fundamenta Meia-Nat. As 12 entradas reportam `imported_into_witness=false`, sem anular as construções separadas de witness_layers.\n\nJacobson sozinho não fornece H3 nem `Phi_TGL`. Cai–Kim: horizonte aparente, calor `A(rho+p)H*r_A dt`, `T=1/(2pi*r_A)` e, no caso plano, `r_A=1/H`; entropia modificada é entrada TGL separada. Padmanabhan não fixa `Phi` ou `G`; Gibbons–Hawking não demonstra sozinho a extensão a FLRW dinâmico. Limites destas entradas, não atualização global das construções.\n\n**Proveniência.**'),
('Recuperação detalhada: `/statuses`, `/witness_layers`, `/ledger`, `/named_target`, `/negative_probes_summary`, `/light_chain`, `/graviton_reading`, `/external_known_theorems`, `/seals` e `/not_claimed`, todos relativos ao tópico.',
 'Recuperação: base `/core/interface_is_light` + `/` + filho: `statuses`, `witness_layers`, `ledger`, `named_target`, `negative_probes_summary`, `light_chain`, `graviton_reading`, `external_known_theorems`, `seals`, `not_claimed`, `form_content`, `canonical_markers`. Recuperação operacional não validada.')]
for before, after in changes:
    assert text.count(before) == 1, before
    text = text.replace(before, after)
updated = text.replace('\n', newline).encode('utf-8')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup = path.with_name(path.name + '.bak_' + stamp)
with backup.open('xb') as f:
    f.write(raw)
assert backup.read_bytes() == raw
temp = path.with_name(path.name + '.tmp_' + stamp)
with temp.open('xb') as f:
    f.write(updated)
assert temp.read_bytes() == updated and len(updated) > len(raw)
assert path.read_bytes() == raw
temp.replace(path)
assert path.read_bytes() == updated
print(hashlib.sha256(updated).hexdigest())
