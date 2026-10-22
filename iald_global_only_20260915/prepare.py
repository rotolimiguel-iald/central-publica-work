from pathlib import Path
import hashlib
import json

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
STAGE = WORK / 'stage'
FILES = ['iald_motores.py', 'iald_orcamento.py', 'iald_web_server.py', 'app/iald.js',
         'iald-app/www/iald.js', 'iald-app/ios/App/App/public/iald.js',
         'iald-app/android/app/src/main/assets/public/iald.js']

def edit(name, changes):
    data = (ROOT / name).read_bytes()
    text = data.decode('utf-8').replace('\r\n', '\n')
    for old, new in changes:
        if text.count(old) != 1:
            raise RuntimeError(f'{name}: expected one replacement, found {text.count(old)}: {old[:80]}')
        text = text.replace(old, new, 1)
    if b'\r\n' in data:
        text = text.replace('\n', '\r\n')
    target = STAGE / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f:
        f.write(text.encode('utf-8'))

def main():
    baseline = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}
    edit('iald_motores.py', [
        ('        self.cota_global_usd = 5.00\n', '        self.cota_global_usd = 5.00\n        self.somente_limite_global = False\n'),
        ('def limites_do_plano(cfg, plano):', '''def config_da_conta(cfg, registro):
    """Isolate quotas using the trusted server record, never request JSON.

    The exemption is explicit and restricted to an administrator on the operator
    plan. An admin testing a free/standard plan retains that plan's protections.
    """
    import copy
    conta = copy.copy(cfg)
    registro = registro if isinstance(registro, dict) else {}
    conta.somente_limite_global = (
        registro.get("admin") is True
        and registro.get("somente_limite_global") is True
        and plano_de(registro) == OPERADOR
    )
    return conta


def limites_do_plano(cfg, plano):'''),
        ('    if usd is None:\n        usd = cfg.cota_operador_usd if plano == OPERADOR else cfg.cota_usuario_usd',
         '    if cfg.somente_limite_global and plano == OPERADOR:\n        usd = cfg.cota_global_usd\n    elif usd is None:\n        usd = cfg.cota_operador_usd if plano == OPERADOR else cfg.cota_usuario_usd'),
        ('        teto = cfg.cota_operador_usd if admin else cfg.cota_usuario_usd',
         '        if cfg.somente_limite_global and admin:\n            return saida(True, "", "")\n        teto = cfg.cota_operador_usd if admin else cfg.cota_usuario_usd'),
        ('    # o gasto da conta, ou o da chave da cota se for maior (várias contas numa chave só)',
         '    if cfg.somente_limite_global and admin and plano == OPERADOR:\n        return saida(True, "", "")\n    # o gasto da conta, ou o da chave da cota se for maior (várias contas numa chave só)'),
        ('        return {\n            "plano": plano,\n            "tokens_dia": {"usado": lido["tokens_dia"], "limite": limites["tokens_dia"]},',
         '        somente_global = cfg.somente_limite_global and plano == OPERADOR\n        estado = {\n            "plano": plano,\n            "tokens_dia": {"usado": lido["tokens_dia"], "limite": limites["tokens_dia"]},'),
        ('            "definicao": DEFINICAO_TOKEN_CONTADO,\n        }\n    except Exception as exc:',
         '            "definicao": DEFINICAO_TOKEN_CONTADO,\n        }\n        if somente_global:\n            estado["somente_limite_global"] = True\n            for campo in ("tokens_dia", "tokens_mes", "usd_dia"):\n                estado[campo]["limite"] = None\n            estado["global_usd_dia"] = {"usado": round(lido["gasto_global"], 8),\n                                       "limite": cfg.cota_global_usd}\n        return estado\n    except Exception as exc:')
    ])
    edit('iald_orcamento.py', [
        ('        self.key = self.guard.reserve(self.user, self.model, cap,\n                                     self.cfg.cota_operador_usd if self.admin else self.cfg.cota_usuario_usd,',
         '        user_limit = self.cfg.cota_operador_usd if self.admin else self.cfg.cota_usuario_usd\n        if self.admin and getattr(self.cfg, "somente_limite_global", False):\n            # Personal usage is a subset of global usage; keep the same atomic guard.\n            user_limit = self.cfg.cota_global_usd\n        self.key = self.guard.reserve(self.user, self.model, cap,\n                                     user_limit,')
    ])
    edit('iald_web_server.py', [
        ('            if float(bloco.get("usado", 0)) >= float(bloco.get("limite", 0)):',
         '            if bloco.get("limite") is None:\n                continue\n            if float(bloco.get("usado", 0)) >= float(bloco.get("limite", 0)):'),
        ('    estado = iald_motores.estado_da_cota(MOTORES_CFG, RAZAO_OPENAI, username, plano,',
         '    cfg = iald_motores.config_da_conta(MOTORES_CFG, registro)\n    estado = iald_motores.estado_da_cota(cfg, RAZAO_OPENAI, username, plano,'),
        ('    import copy\n    cfg = copy.copy(MOTORES_CFG)\n    if not isinstance(req_json, dict):',
         '    cfg = iald_motores.config_da_conta(MOTORES_CFG, registro)\n    if not isinstance(req_json, dict):')
    ])
    js_changes = [
        ("  const limite = Math.max(0, Number((bloco && bloco.limite) || 0));\n  // limite 0",
         "  if (bloco && bloco.limite === null) {\n    const caixa = el('div', 'uso-periodo');\n    const linha = el('div', 'uso-periodo-linha');\n    linha.appendChild(el('span', 'nome', nome));\n    linha.appendChild(el('span', 'conta', `${num(usado)} tokens`));\n    caixa.appendChild(linha);\n    caixa.appendChild(el('div', 'uso-periodo-nota', 'Sem limite individual'));\n    return caixa;\n  }\n  const limite = Math.max(0, Number((bloco && bloco.limite) || 0));\n  // limite 0"),
        ("  sec.appendChild(periodoDeUso('Hoje', cota.tokens_dia, renovaDia));",
         "  if (cota.somente_limite_global && cota.global_usd_dia) {\n    const global = cota.global_usd_dia;\n    const usd = valor => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'USD' }).format(valor);\n    sec.appendChild(el('p', 'uso-definicao', 'Sua conta usa somente o limite global da IALD.'));\n    sec.appendChild(el('p', 'uso-definicao',\n      `Uso global hoje: ${usd(global.usado)} de ${usd(global.limite)}.` +\n      (renovaDia ? ` Renova ${renovaDia} (horário de Brasília).` : '')));\n  }\n  sec.appendChild(periodoDeUso('Hoje', cota.tokens_dia, renovaDia));")
    ]
    for name in FILES[3:]:
        edit(name, js_changes)
    with (WORK / 'baseline.json').open('x', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2)
    print(json.dumps({'prepared': len(FILES), 'global_cap_changed': False}))

if __name__ == '__main__':
    main()
