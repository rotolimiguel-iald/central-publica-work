# -*- coding: utf-8 -*-
"""regerar_handoff_v403.py (gerência c1, 28/10/2026) -- a lição 23 da v402 repetida na v403: o portão de texto do G1 (tools/custodia_g1/textos.py, regra 2) reprovou
«a dimensão 3 NÃO é provada e o 1 + 3 é leitura [ONTO]» no parágrafo pronto do handoff (provada/proved exige, na mesma frase, validade, creditação, ≠, judgement ou nature;
o estatuto entre colchetes não conta). Correção NA FONTE (textos_v403_novo.pysnip, a mesma frase da v402 corrigida em 27/10: «NÃO é provada no kernel (a validade é só a dos termos
do trio)»), montar, conferir citações, REGERAR o handoff pelo passo 11 da cadeia (fechar; backup do anterior pelo próprio fechar), nota ao lado e errata no mapa (sha antes/depois lidos).
uso: python -X utf8 regerar_handoff_v403.py"""
import datetime, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
PY = r"C:\Python314\python.exe"; SH = r"C:\Program Files\Git\usr\bin\sh.exe"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def run(args, cwd=None, env=None, shell_sh=False):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# (1) a fonte
P = os.path.join(HERE, "textos_v403_novo.pysnip")
b = open(P, "rb").read(); t = b.decode("utf-8")
bak = P + ".bak_%s_c1_provada" % ts; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
velho = "A dimensão 3 NÃO é provada e o 1 + 3 é leitura [ONTO]."   # a frase do PARAGRAFO pronto (README/site), a que o portao citou; a minuscula (limites) ja foi corrigida na 1a passagem
novo = "A dimensão 3 NÃO é provada no kernel (a validade é só a dos termos do trio) e o 1 + 3 é leitura [ONTO]."
n = t.count(velho); assert n == 1, ("ocorrencias da frase", n)
t = t.replace(velho, novo)
assert "a dimensão 3 NÃO é provada no kernel (a validade é só a dos termos do trio)" in t   # a correcao da 1a passagem (limites) esta la
assert t.count("NÃO é provada") >= 2   # a frase corrigida + a string de checagem da lista (substring preservada)
nb = t.encode("utf-8"); tmp = P + ".tmp_c1"; open(tmp, "wb").write(nb); assert len(open(tmp, "rb").read()) == len(nb); os.replace(tmp, P)
print("fonte:", os.path.basename(P), len(b), "->", len(nb), "sha16", sha(P)[:16])
# (2) montar + (3) citações
rc, out = run([PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "montar_textos_v403.py")], cwd=HERE); print("montar rc", rc, out.strip().splitlines()[-2:] if out.strip() else ""); assert rc == 0
rc, out = run([PY, "-I", "-B", "-X", "utf8", os.path.join(PK, "conferir_citacoes_v403.py")], cwd=PK); print("citacoes rc", rc, out.strip().splitlines()[-1:]); assert rc == 0
assert "NÃO é provada no kernel (a validade" in open(os.path.join(HERE, "textos_v403.py"), encoding="utf-8").read()
# (4) o handoff antes
H = os.path.join(NOS, "HANDOFF_v403_CUSTODIA.md"); M = os.path.expanduser(r"~\.claude\projects\c--IALD-Central-de-Patentes\memory\handoff-v403-custodia.md")
antes = sha(H); antes_mem = sha(M) if os.path.exists(M) else None
print("handoff antes:", antes[:16], "| memoria antes:", (antes_mem or "")[:16])
# (5) regerar pelo passo 11
env = dict(os.environ, CHAIN_DE="11", CHAIN_ATE="11")
rc, out = run([SH, "./chain_pos_rito_v403.sh"], cwd=HERE, env=env)
open(os.path.join(HERE, "chain_11_regerar_out_v403.txt"), "w", encoding="utf-8").write(out)
print("chain 11 rc", rc); print("\n".join(l[:200] for l in out.strip().splitlines()[-6:])); assert rc == 0, "o fechar falhou: ver chain_11_regerar_out_v403.txt"
depois = sha(H); depois_mem = sha(M) if os.path.exists(M) else None
baks = sorted(f for f in os.listdir(NOS) if f.startswith("HANDOFF_v403_CUSTODIA.md.bak_"))
print("handoff depois:", depois[:16], "| memoria depois:", (depois_mem or "")[:16], "| backups:", baks[-2:])
assert depois != antes and novo in open(H, encoding="utf-8").read()
# (6) nota ao lado
nota = os.path.join(HERE, "NOTA_AO_LADO_HANDOFF_REGERADO_v403.md")
texto = ("# NOTA AO LADO — o handoff da v403 foi REGERADO pelo passo 11 em %s (gerência c1, em nome próprio)\n\n"
         "O portão de texto do G1 (`tools/custodia_g1/textos.py`, regra 2: «provada/proved» exige, na mesma frase, validade, creditação, ≠, judgement ou nature; o estatuto entre colchetes não conta) "
         "reprovou a frase do parágrafo pronto da v403 «%s» — a mesma frase que a v402 corrigiu em 27/10 (lição 23), e que voltou porque a fonte da v403 (`textos_v403_novo.pysnip`) foi derivada do fragmento da v402 ANTERIOR àquela correção. "
         "A correção foi feita NA FONTE (`textos_v403_novo.pysnip`, `_paragrafo`): «%s»; `montar_textos_v403.py` remontou `textos_v403.py`; `conferir_citacoes_v403.py` TODAS CONFEREM; o passo 11 (fechar) regerou o handoff.\n\n"
         "Hashes (lidos agora por script):\n- Nós `HANDOFF_v403_CUSTODIA.md`: antes `%s`; agora `%s`. Backup do fechar no Nós: %s.\n- memória `handoff-v403-custodia.md`: antes `%s`; agora `%s`.\n\n"
         "O conteúdo factual não mudou; só a frase citada. As superfícies já gravadas no passo 7 (diário, Atlas) que trazem a frase antiga ficam como estão (append-only); esta nota é a correção ao lado; a errata do mapa corrige o artefato da rota selada (seq 1491).\n"
         ) % (datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), velho, novo, antes[:16], depois[:16], (baks[-1] if baks else "(nenhum)"), (antes_mem or "n/d")[:16], (depois_mem or "n/d")[:16])
open(nota, "w", encoding="utf-8", newline="\n").write(texto)
# (7) errata no mapa (corrige o artefato do handoff da rota selada, seq 1491)
err = [{"tipo": "ERRATA", "rota_id": "umpy.v403.selada_caminho_verdade_vida_27out", "corrige": 1491, "estatuto": "REAL", "olhou_dados": False,
        "titulo": "Errata ao lado: o HANDOFF_v403_CUSTODIA.md do registro 1491 foi REGERADO (portao de texto do G1, regra 2: «provada» sem estatuto na mesma frase)",
        "nota": "[ERRATA AO LADO, gerencia c1, em nome proprio, %s] Corrige o artefato HANDOFF_v403_CUSTODIA.md do registro seq 1491 (sha256 %s...): regerado pelo passo 11 depois que o portao de texto do G1 reprovou «%s» (a mesma licao 23 da v402; a fonte da v403 vinha do fragmento da v402 anterior aquela correcao). Correcao na fonte textos_v403_novo.pysnip: «%s». Conteudo factual inalterado. Handoff novo: sha256 %s...; backup do antigo pelo fechar: %s; memoria handoff-v403-custodia.md regerada (antes %s). As superficies do passo 7 (diario, Atlas) ficam como estao (append-only)." % (datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), antes[:16], velho, novo, depois[:16], (baks[-1] if baks else "n/d"), (antes_mem or "n/d")[:16]),
        "artefatos": [H] + ([os.path.join(NOS, baks[-1])] if baks else []) + [P, bak, nota]}]
pj = os.path.join(HERE, "errata_mapa_handoff_regerado_v403.json"); json.dump(err, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rc, out = run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), cadeia v403"]); print("mapa rc", rc, out.strip()[-300:]); assert rc == 0
print("OK: handoff regerado", antes[:16], "->", depois[:16])
