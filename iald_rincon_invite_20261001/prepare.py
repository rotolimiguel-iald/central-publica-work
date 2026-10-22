from pathlib import Path
import ast, hashlib, json
W=Path(__file__).parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
S=W/'stage';S.mkdir(exist_ok=True)
p=R/'iald_motores.py';raw=p.read_bytes();text=raw.decode('utf-8').replace('\r\n','\n')
def edit(old,new):
 global text
 assert text.count(old)==1,old[:80]
 text=text.replace(old,new)
edit('    return conta\n\n\n'+ 'def limites_do_plano', '''    # Trusted account-only token exemption; never changes admin or monetary caps.
    conta.tokens_sem_limite = (
        registro.get("tokens_sem_limite") is True
        and not registro.get("bloqueado") and not registro.get("acesso_bloqueado")
    )
    return conta


def limites_do_plano''')
edit('    return {"tokens_dia": int(bruto["tokens_dia"]), "tokens_mes": int(bruto["tokens_mes"]),', '''    unlimited = getattr(cfg, "tokens_sem_limite", False) is True
    return {"tokens_dia": None if unlimited else int(bruto["tokens_dia"]),
            "tokens_mes": None if unlimited else int(bruto["tokens_mes"]),''')
edit('    if lido["tokens_dia"] >= limites["tokens_dia"]:', '    if limites["tokens_dia"] is not None and lido["tokens_dia"] >= limites["tokens_dia"]:')
edit('    if lido["tokens_mes"] >= limites["tokens_mes"]:', '    if limites["tokens_mes"] is not None and lido["tokens_mes"] >= limites["tokens_mes"]:')
edit('    dia = int(limites["tokens_dia"]) - int(lido["tokens_dia"]) - int(em_voo)\n    mes = int(limites["tokens_mes"]) - int(lido["tokens_mes"]) - int(em_voo)', '''    dia = (float("inf") if limites["tokens_dia"] is None else
           int(limites["tokens_dia"]) - int(lido["tokens_dia"]) - int(em_voo))
    mes = (float("inf") if limites["tokens_mes"] is None else
           int(limites["tokens_mes"]) - int(lido["tokens_mes"]) - int(em_voo))''')
edit('        cabe = saldo - self.entrada_estimada(payload)', '''        if saldo == float("inf"):
            # The model/window still supplies a finite per-response maximum.
            if _inteiro(payload.get("max_completion_tokens")) <= 0:
                raise CotaEsgotada("Limite técnico de saída ausente.", "razao")
            self.chamadas += 1
            return payload
        cabe = saldo - self.entrada_estimada(payload)''')
# Keep original CRLF style where applicable, including inserted lines.
if b'\r\n' in raw:text=text.replace('\r\n','\n').replace('\n','\r\n')
out=text.encode('utf-8');ast.parse(out)
(S/p.name).write_bytes(out)
(W/'baseline.json').write_text(json.dumps({p.name:hashlib.sha256(raw).hexdigest()},indent=2))
print('Staged account-scoped token exemption; financial policy unchanged.')
