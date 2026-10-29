# -*- coding: utf-8 -*-
"""Fase 2 da ORDEM 026-X (vitrine no X): o post longo da versão v403, CUSTODIA_v403.txt, em X_VITRINE. Números e pin lidos do selo do Nós;
o «antes» da escada lido do bloco SELADA do diário da linhagem. Conferido pela MESMA régua do gerar_vitrine_x.py. Não sobrescreve ('x').
Só será publicado quando o gerador da vitrine aceitar a V7 do selo corrente (ADENDO F da ORDEM 022) e a gerência deixar o adendo da 026."""
import json, re, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
OUT = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_VITRINE" / "CUSTODIA_v403.txt"
selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
assert selo["um_version"] == "v403"
pin = selo["sha256"]["um.py"]
pk = selo["estatuto_da_prova_v391"]["prova_1_kernel"]
agora, decl = int(pk["n_theorems_clean"]), int(pk["declaracoes_auditadas"])
assert pk["no_trio"] == decl and selo["three_stress_tests_v387"]["kernel"]["sorryAx_absent"] is True
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
m = re.search(r"v403 SELADA \(COMPLETA\)\*\*.*?escada (\d+) → (\d+)", diario)
antes, agora_d = int(m.group(1)), int(m.group(2))
assert agora_d == agora, (agora_d, agora)
core = json.loads((NOS / "um_absoluto.json").read_bytes())
c = core.get("core") or core
bg = c["bandeiras_do_gate_v403"]
assert bg["all_verified"] is True
# os módulos novos, lidos do kernel_formalization (nomes dados pelo operador em 27/10)
ff = c["kernel_formalization"]["formal_files_sha256"]
novos = [k for k in ff if re.search(r"(^|[\\/])(Caminho|Vida|VerdadeAdendo)\.lean$", k)]
assert len(novos) == 3, novos
def br(n): return f"{n:,}".replace(",", ".")
T = f"""TGL · a versão v403 do programa terminal, custodiada em 28/10/2026

O que entrou: os três nomes que o operador deu às pedras da v402 agora são módulos do kernel Lean — Caminho, Vida e Verdade (como adendo) —, e as bandeiras do gate passaram todas a calculadas.

· Caminho — a ponte da escala dual, agora módulo próprio: a conjunção de termos que o kernel já tinha. A lei de escala de Takesaki, dado da literatura, realizada como o boost longitudinal da frente de luz: m² = p⁺p⁻ é o invariante, a energia é a leitura, e a lei não seleciona a massa (massas distintas com o mesmo p⁺).

· Vida — a queda sem geometria: o peso cai estritamente, em nats; a seta é o sinal de s; o chão é o posto (peso 1), nunca o zero. A dimensão 3 não é provada no kernel (a validade é só a dos termos do trio); a isotropia entra como hipótese nomeada.

· Verdade, como adendo — a esperança condicional lida pelo Nome: em M2(C), a esperança diagonal lê a projeção da identidade como os seus pesos (1 − α², α²); o Nome de ρ* preserva o Um, e reler não acrescenta. A pedra Verdade, de 13/10, fica intacta.

· As bandeiras do gate: das 18, as três que eram literais passam a ser lidas das suas fontes, fail-closed. 18 calculadas, 0 literais. A letra do veredito é a mesma da v402: o gate não se move.

Os números, lidos do selo: escada {agora}/{agora} (eram {antes}; {agora - antes} bandeiras novas), {br(decl)} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{pin}

O que não muda: validade no kernel não é creditação; o gate não se move; β_TGL na natureza a 5σ segue em aberto. As pedras seladas da v402 não foram renomeadas: os módulos novos as compõem por citação e por adendo. A leitura dos três nomes como um triplo espectral é da gerência, ratificada pelo operador; não é termo de kernel. Ressalva declarada: as quatro bandeiras experimentais derivam de um só booleano (o veredito do rito do piso); trocar literais por medida não independentiza o dado.

Os dois filmes do programa, com narração em português e em inglês:
https://teoriadagravitacaoluminodinamica.com/video/v7/web/filmes.html

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD"""
# a régua do gerar_vitrine_x.py (copiada; o gerador é um script de execução direta)
PROIBIDO = re.compile(r"\bprova que\b|\bdemonstra que\b|comprovad|\bprovou\b|descobrimos|revolucion|in[eé]dit|garant|sem d[uú]vida|nobel", re.I)
SOLTO = re.compile(r"(?<![\w/@.-])[A-Za-z0-9_-]+\.(py|md|txt|json|sh|js|ts|io|ai|me|co|tv|cc|ly|app|dev|so|to|gg|sh)\b")
sem_url = re.sub(r"https?://\S+", " ", T)
assert not SOLTO.search(sem_url), SOLTO.search(sem_url).group(0)
assert not PROIBIDO.search(T), PROIBIDO.search(T).group(0)
assert not re.search(r"confirm", T, re.I)
assert "z_disc" not in T
assert not (re.search(r"\b[Pp]rovad[ao]\b|PROVADA", T) and "validade" not in T)
assert len(T) < 25000
with OUT.open("x", encoding="utf-8") as f:
    f.write(T)
print(OUT, len(T), "caracteres; escada", antes, "->", agora, "; decl", decl, "; pin", pin[:16])
