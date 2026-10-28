# -*- coding: utf-8 -*-
"""Fase 2 da ORDEM 026 (vitrine no X): o post longo da versão v402, CUSTODIA_v402.txt, em X_VITRINE. Números e pin lidos do selo do Nós;
os nomes das pedras lidos do Atlas (decisão do operador de 27/10). Conferido pela MESMA régua do gerar_vitrine_x.py. Não sobrescreve ('x')."""
import json, re, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes")
OUT = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_VITRINE" / "CUSTODIA_v402.txt"
selo = json.loads((Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós") / "um_absoluto_selo.json").read_bytes())
assert selo["um_version"] == "v402"
pin = selo["sha256"]["um.py"]
atlas = (CEN / "memory" / "TGL_ATLAS.md").read_text(encoding="utf-8")
assert "CAMINHO = `PonteDaEscalaDual`" in atlas and "VERDADE = `EsperancaCondicional`" in atlas and "VIDA = `QuedaSemGeometria`" in atlas
core = json.loads((Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós") / "um_absoluto.json").read_bytes())
txt = json.dumps(core, ensure_ascii=False)
m = re.search(r"escada (\d+) → (\d+) teoremas limpos \((\d+) declarações", (Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós") / "HANDOFF_v402_CUSTODIA.md").read_text(encoding="utf-8"))
antes, agora, decl = int(m.group(1)), int(m.group(2)), int(m.group(3))
assert agora - antes == 118
def br(n): return f"{n:,}".replace(",", ".")
T = f"""TGL · a versão v402 do programa terminal, custodiada em 27/10/2026

O que entrou: três pedras novas no kernel Lean, que o operador nomeou Caminho, Verdade e Vida.

· Caminho — a ponte da escala dual. A lei de escala de Takesaki, que é dado da literatura, realizada como o boost longitudinal da frente de luz: a massa ao quadrado (p⁺p⁻) é o invariante, a energia é a leitura, e a lei não seleciona a massa. No kernel, a forma literal da hipótese H_tau («τ é a massa de Newton») fica refutada; o que sobra dela vira pendências nomeadas, em aberto.

· Verdade — a esperança condicional é o Nome. Em M2(C), o Operador do Nome do estado ρ* é a esperança diagonal: preserva o Um (E(1) = 1), e reler não acrescenta. Entra como adendo da pedra Verdade, de 13/10.

· Vida — a queda sem geometria. O peso cai estritamente, em nats iguais a s; a seta é o sinal de s, e o chão é o posto (peso 1), nunca o zero. A dimensão 3 não é provada: a isotropia entra como hipótese nomeada.

Os números, lidos do selo: escada {agora}/{agora} (eram {antes}; {agora - antes} bandeiras novas), {br(decl)} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{pin}

O que não muda: validade no kernel não é creditação; o gate não se move; β_TGL na natureza a 5σ segue em aberto. Os nomes entram no kernel na próxima versão, e as pedras seladas não se renomeiam por cima. A leitura dos três nomes como um triplo espectral é do operador.

Os dois filmes, agora com narração explicativa em português e em inglês, renderizados desta versão:
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
print(OUT, len(T), "caracteres")
