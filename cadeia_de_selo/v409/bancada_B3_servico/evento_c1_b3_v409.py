# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] evento do B(n) da v409 (B18, passo simples v408 -> v409); candidato_sha16 LIDO de ESPERADOS_v409.json e conferido contra o um.py do Nos antes de anotar
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v409) molde v408/bancada_B3_servico/evento_c1_b3_v408.py (rotulos subidos por _bump_copia_v409.py; diff em bump/); conferido em 04/11/2026: versao v409, ESPERADOS_v409.json (candidato_sha16 LIDO, conferido contra o um.py do Nos antes de anotar), unidade F0.6, B18 sobre a producao que pina B17-v408-20261105-R1 (delta_v409.BANCADA_PINA_HOJE); nada de bundle, de contagem de modulos nem de hash digitado
"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v409 (passo simples v408 -> v409, sem salto; B18, a producao pina B17-v408-20261105-R1), no conjunto fechado de chaves do esboco R3.5. O candidato_sha16 e' LIDO de ESPERADOS_v409.json (nunca digitado) e conferido contra o um.py do Nos antes de anotar."""
import hashlib
import json
import os
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v409", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
D = os.path.dirname(os.path.abspath(__file__))
ESP = os.path.join(D, "..", "ESPERADOS_v409.json")
assert os.path.isfile(ESP), "ESPERADOS_v409.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v409): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v409.json", dados["um_py"][:16], CAND16)
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
