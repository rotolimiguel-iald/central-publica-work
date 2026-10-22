"""Evento c1 SINCRONIZACAO_BANCADA da B3 da v392, no conjunto fechado de chaves do esboço R3.3."""
import hashlib
import json
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v392", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
