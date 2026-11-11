# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] evento do B(n) da v410 (B19, passo simples v409 -> v410); candidato_sha16 LIDO de ESPERADOS_v410.json e conferido contra o um.py do Nos antes de anotar; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos) molde v409/bancada_B3_servico/evento_c1_b3_v409.py (rotulos subidos por _bump_copia_v410.py; diff em bump/); conferido em 04/11/2026: versao v410, ESPERADOS_v410.json (candidato_sha16 LIDO, conferido contra o um.py do Nos antes de anotar), unidade F0.6, B19 sobre a producao que pina B18-v409-20261106-R1 (delta_v410.BANCADA_PINA_HOJE); nada de bundle, de contagem de modulos nem de hash digitado
"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v410 (passo simples v409 -> v410, sem salto; B19, a producao pina B18-v409-20261106-R1), no conjunto fechado de chaves do esboco R3.5. O candidato_sha16 e' LIDO de ESPERADOS_v410.json (nunca digitado) e conferido contra o um.py do Nos antes de anotar."""
import hashlib
import json
import os
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v410", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
D = os.path.dirname(os.path.abspath(__file__))
ESP = os.path.join(D, "..", "ESPERADOS_v410.json")
assert os.path.isfile(ESP), "ESPERADOS_v410.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v410): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v410.json", dados["um_py"][:16], CAND16)
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
