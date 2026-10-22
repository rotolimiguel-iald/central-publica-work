from pathlib import Path
import json
import hashlib
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
changes = {
 'iald_orcamento.py': [('    def summary(self):', '''    def used_today(self):
        """Same amount as the reservation guard: settled costs plus active holds."""
        with self._connect() as db:
            amount = db.execute(
                "SELECT COALESCE(SUM(COALESCE(actual, cap)), 0) FROM calls WHERE day=?",
                (_today(self.clock),)).fetchone()[0]
        if not math.isfinite(amount) or amount < 0:
            raise BudgetError(MSG_LIMITES_INVALIDOS, "razao")
        return float(amount)

    def summary(self):''')],
 'iald_web_server.py': [('    if "erro" not in estado:\n        estado["bloqueado_por"] = _bloqueio_da_cota(estado)\n    return estado', '''    if "erro" not in estado and cfg.somente_limite_global:
        try:
            total = max(estado["global_usd_dia"]["usado"], _guarda_openai().used_today())
            estado["global_usd_dia"]["usado"] = round(total, 8)
        except Exception:
            estado["erro"] = "O controle de uso global está indisponível agora."
    if "erro" not in estado:
        estado["bloqueado_por"] = _bloqueio_da_cota(estado)
    return estado''')],
}
for name in ['app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js','iald-app/android/app/src/main/assets/public/iald.js']:
    changes[name] = [('`Uso global hoje: ${usd(global.usado)}', '`Uso global hoje (inclui reservas): ${usd(global.usado)}')]
baseline = {}
for name, edits in changes.items():
    path = WORK / 'stage' / name
    before = (ROOT / name).read_bytes()
    assert path.read_bytes() == before, 'Concurrent edit ' + name
    text = before.decode().replace('\r\n','\n')
    for old, new in edits:
        assert text.count(old) == 1, name
        text = text.replace(old,new)
    if b'\r\n' in before:
        text = text.replace('\n','\r\n')
    temp = path.with_suffix(path.suffix + '.display.tmp')
    with temp.open('xb') as f: f.write(text.encode())
    temp.replace(path)
    baseline[name] = hashlib.sha256(before).hexdigest()
with (WORK / 'display_baseline.json').open('x') as f:
    json.dump(baseline, f, indent=2)
print('Prepared global usage display from reservation ledger.')
