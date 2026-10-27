"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v400 (passo simples v398 -> v400, sem salto), no conjunto fechado de chaves do esboco R3.5."""
import hashlib
import json
import os
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v400", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
D = os.path.dirname(os.path.abspath(__file__))
ESP = os.path.join(D, "..", "ESPERADOS_v400.json")
assert os.path.isfile(ESP), "ESPERADOS_v400.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v400): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v400.json", dados["um_py"][:16], CAND16)
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
