# -*- coding: utf-8 -*-
"""Testes da máscara de dado pessoal (22/10/2026): o que deve ser trocado e o que NÃO pode ser tocado (código, tabelas, equações,
e-mails institucionais). Os números são fictícios."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar, MASK  # noqa: E402

DEVE = ["ligue [dado pessoal removido] já", "[dado pessoal removido]", "fone [dado pessoal removido]", "CEP: [dado pessoal removido]", "nascido em [dado pessoal removido]",
        "[dado pessoal removido], Setor Bueno, Goiânia", "contato [dado pessoal removido]", "CPF [dado pessoal removido]", "[dado pessoal removido] (celular)",
        "RG [dado pessoal removido]", "Carteira de Identidade nº [dado pessoal removido]", "WhatsApp ([dado pessoal removido]", "Cel: [dado pessoal removido]",
        "TELEFONE\nx/ [dado pessoal removido]", " CEP\n[dado pessoal removido]\nBAIRRO", "* Fulano <[dado pessoal removido]>", "[dado pessoal removido]"]
NAO = ["eq. (23) 20261012 ok", "tabela 34 91234 5678 12", "x = Q@K.T", "wipo pct@wipo.int", "z = (12) 3.14159", "beta = 0.012031300400803142",
       "2026-10-22 11:40:09", "sha256 5dd22afc9b0e7c7e", "a(10) 1234 5678 b", "id 99812-3456",
       'mapeamento EXATO da identidade\\", 0910-2216, 0910-2236', "a identidade 1 = 1 em 2026-10-22", "identidade: 1.0000000 exata",
       "Hotel 12 3456 7890", "célula 16 2026 0301", "Intel 12 3456 7890",
       "5,2e15 M☉ (banda RG ✓**, bate §88.27.14); aglomerado", "a RG 1.000000 é o limite clássico", "RG: limite clássico em 2026-10-22",
       "Phys. Rev. D 51 (1995) 2345-2350", "Commun. Math. Phys. 48 (1976) 1190-1300"]
falhas = 0
for t in DEVE:
    r, c = mascarar(t)
    ok = MASK in r
    falhas += not ok
    print(("ok   " if ok else "FALHA"), "troca:", repr(t), "->", repr(r))
for t in NAO:
    r, c = mascarar(t)
    ok = r == t
    falhas += not ok
    print(("ok   " if ok else "FALHA"), "intacto:", repr(t), "->", repr(r))
print("FALHAS:", falhas)
