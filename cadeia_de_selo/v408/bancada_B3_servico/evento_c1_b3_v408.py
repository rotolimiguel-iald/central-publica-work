# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] molde v407/bancada_B3_servico/evento_c1_b3_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: versao v408, ESPERADOS_v408.json (candidato_sha16 LIDO, conferido contra o um.py do Nos antes de anotar), unidade F0.6, B17 sobre a producao que pina B16-v407-20261104-R1 (delta_v408.BANCADA_PINA_HOJE); nada de bundle, de contagem de modulos nem de hash digitado
"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v408 (passo simples v407 -> v408, sem salto; B17, a producao pina B16-v407-20261104-R1), no conjunto fechado de chaves do esboco R3.5. O candidato_sha16 e' LIDO de ESPERADOS_v408.json (nunca digitado) e conferido contra o um.py do Nos antes de anotar."""
import hashlib
import json
import os
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v408", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
D = os.path.dirname(os.path.abspath(__file__))
ESP = os.path.join(D, "..", "ESPERADOS_v408.json")
assert os.path.isfile(ESP), "ESPERADOS_v408.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v408): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v408.json", dados["um_py"][:16], CAND16)
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
