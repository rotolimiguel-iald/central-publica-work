# -*- coding: utf-8 -*-
"""gerar_custodia_v404_txt.py -- gerência c1, 28/10/2026: escreve X_VITRINE\\CUSTODIA_v404.txt (o post longo da versão para a Fase 2 da vitrine do X,
ORDEM 026-X), no molde do CUSTODIA_v403.txt. Os números são LIDOS do selo e do core do Nós (nunca digitados); o texto passa pela régua do X:
nenhum nome de arquivo ou domínio solto fora de URL (o X transforma «um.py» em link para fora), nada de «confirmada», α nunca escrito como β/√e.
Temporário -> conferir -> substituir; recusa sobrescrever."""
import hashlib
import json
import os
import re
import time
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
X = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
core = json.loads((NOS / "um_absoluto.json").read_bytes())
c = core.get("core") or core
assert selo["um_version"] == "v404"
pin = selo["sha256"]["um.py"]
assert pin == sha(NOS / "um.py")
pk = selo["estatuto_da_prova_v391"]["prova_1_kernel"]
kf = c["kernel_formalization"]
escada = int(pk["n_theorems_clean"])
decl = len(kf["axiom_report"])
assert decl == int(pk["declaracoes_auditadas"]) == int(pk["no_trio"])
bg = c["bandeiras_do_gate_v403"]["values"]
assert (int(bg["n_flags"]), int(bg["n_calculated"]), int(bg["n_literal"])) == (18, 18, 0)
pj = c["projecao_transversal_v404"]
assert pj.get("runtime_executed") is True and pj.get("does_not_gate_core") is True
jo = c["jo8v32_v404"]
assert jo.get("does_not_gate_core") is True
f2 = c["f2b_errata_v404"]
assert f2.get("does_not_gate_core") is True
# a escada anterior (v403) vem do CUSTODIA_v403.txt, por regex (o número de lá foi lido do selo da v403)
ant = (X / "CUSTODIA_v403.txt").read_text(encoding="utf-8")
m = re.search(r"escada (\d+)/\1 \(eram (\d+); (\d+) bandeiras novas\)", ant)
esc403 = int(m.group(1))
assert escada - esc403 == 14, (escada, esc403)
novas = escada - esc403
hoje = time.strftime("%d/%m/%Y")
decl_fmt = f"{decl:,}".replace(",", ".")
txt = f"""TGL · a versão v404 do programa terminal, custodiada em {hoje}

O que entrou: duas pedras novas no kernel Lean e uma errata ao lado. A primeira pedra deriva o ângulo do neutrino; a segunda dá ao triplo da v403 o nome que o operador escolheu, Jo 8,32.

· A projeção transversal da Meia-Nat — o seno de 45° do neutrino deixa de ser postulado: da fronteira autoconjugada (x = 1 − x) sai x = ½, e a amplitude transversal de um peso ½ é √½ = sen(π/4), único em [0, π/2]. A forma da massa do neutrino, β · sen 45° · E₀, fica derivada no kernel, condicional a uma identificação que é leitura do operador, não termo de kernel: a matéria como projeção do eixo transversal do estado inscrito (não proporcional ao raio de β: a derivada). E₀ = 1 eV segue declarado; a pedra não deriva E₀ nem β.

· Jo 8,32 — o nome do triplo inteiro (Caminho · Verdade · Vida), dado pelo operador em 28/10/2026: a pedra é a conjunção, por citação, das três estrelas da v403, sem matemática nova; as pedras seladas da v403 não foram editadas nem renomeadas. A leitura por Jo 8,31-32 (permanecer, conhecer, libertar) é da gerência, ratificada pelo operador; não é termo de kernel.

· A errata de F2b — o canal do ramo B do ringdown (v386) sai de «aguardando» para «retirado antes do dado», ao lado: a calibração pública (não cega) deu uma deformação comum fora do intervalo da previsão do par e de sinal oposto. Nenhum desfecho sai dessa calibração; o conjunto cego não é aberto; o registro original fica congelado por hash e é lido como antes. Calibrar não é validar.

· O gate: o mesmo da v403 — 18 bandeiras, todas calculadas, 0 literais; a letra do veredito não muda. O gate não se move; nenhuma bandeira dele depende das pedras da v404.

Os números, lidos do selo: escada {escada}/{escada} (eram {esc403}; {novas} bandeiras novas), {decl_fmt} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{pin}

O que não muda: validade no kernel não é creditação; o gate não se move; β_TGL na natureza a 5σ segue em aberto. Ressalva declarada: as quatro bandeiras experimentais derivam de um só booleano (o veredito do rito do piso); isto não é teste e não acrescenta dado.

Os dois filmes do programa, com narração em português e em inglês:
https://teoriadagravitacaoluminodinamica.com/video/v7/web/filmes.html

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
# a régua do X: nenhum token «nome.ext» ou domínio solto fora de URL; nada de confirmação; α nunca β/√e; sem o nome do arquivo do programa
sem_urls = re.sub(r"https?://\S+", "", txt)
soltos = re.findall(r"\b[\w-]+\.(?:py|json|md|com|br|org|net|io|txt|cff)\b", sem_urls)
assert not soltos, ("nome de arquivo ou domínio solto fora de URL", soltos)
assert "um.py" not in sem_urls
assert not re.search(r"confirmad[ao]", txt, re.I)
assert "β/√e" not in txt and "beta/raiz" not in txt.lower()
assert "pós-dição" not in txt
assert f"{escada}/{escada}" in txt and pin in txt
dest = X / "CUSTODIA_v404.txt"
assert not dest.exists(), "já existe: não sobrescrevo"
tmp = dest.with_suffix(".txt.tmp")
tmp.write_bytes(txt.encode("utf-8"))
assert tmp.read_bytes().decode("utf-8") == txt
os.replace(tmp, dest)
print("gravado", dest, len(txt), "chars", "sha16", sha(dest)[:16])
print("numeros:", {"escada": (esc403, escada), "novas": novas, "decl": decl, "pin16": pin[:16], "gate": (bg["n_flags"], bg["n_calculated"], bg["n_literal"])})
