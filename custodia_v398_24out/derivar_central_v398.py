# -*- coding: utf-8 -*-
"""Deriva, da custódia v397 (work/custodia_v397_23out), a parte mecânica do lado da Central para a v398 (24/10/2026, sessão a7; regra do
operador de 23/10: custodiar quando o handoff aparecer): cofre_v398.py, medir_v398_contra_v397.py, snapshot_chatgpt_v398.py,
conferencia_final_v398.py, registro_v398_publicada.py e acom_transicao.py. Método: DESLOCAMENTO ordenado de versões/pinos/contagens/datas
(cada string lida de fatos_v398.json ou de fatos_v397.json, nunca digitada quando o artefato a traz) com proteção dos nomes que não mudam
(a ordem verbatim, as pastas de outras custódias), depois a errata do cofre reescrita por regex. Sintaxe conferida; sobras de «v397» listadas."""
import json, re
from pathlib import Path

W7 = Path(r"C:\IALD\Central de Patentes\work\custodia_v397_23out")
W8 = Path(r"C:\IALD\Central de Patentes\work\custodia_v398_24out")
F8 = json.loads((W8 / "fatos_v398.json").read_text(encoding="utf-8"))
F7 = json.loads((W7 / "fatos_v397.json").read_text(encoding="utf-8"))
assert F8["versao"] == "v398" and F7["versao"] == "v397"
assert F8["registros_novos"] == ["afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "sonico_v398"], F8["registros_novos"]
P8, P7, P6 = F8["pin16"], F7["pin16"], "0a4395a89eeebbb7"
assert P7 == "388cc3742323421c" and F8["kernel"]["formais_v397"] == F7["kernel"]["formais"] == 1426 and F8["kernel"]["declaracoes_v397"] == 29229
ESC8, ESC7, ESC6 = F8["escada"], F7["escada"], "9498/9498"
FORM8, DECL8, FORM7, DECL7, FORM6, DECL6 = F8["kernel"]["formais"], F8["kernel"]["declaracoes"], 1426, 29229, 1425, 29228
SNAP7 = "Chatgpt_20261022_201134_delta_de_20261021_175747"          # a base que o snapshot da v397 exigiu
SNAP8 = "Chatgpt_20261023_174138_delta_de_20261022_201134"          # o snapshot feito na custódia v397 (base da v398)
assert (Path(r"C:\IALD\Central de Patentes_BACKUPS") / SNAP8 / "MANIFEST.json").is_file(), "a base do snapshot (v397) não está em BACKUPS — PARAR"

PROTEGE = {"php_e_v396_22out": "\x00P0\x00", "OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt": "\x00P1\x00"}
ORDEM = [  # ordem importa: do mais específico ao mais geral; o novo antes do velho para não encadear
    ("custodia_v397_23out", "custodia_v398_24out"), ("custodia_v396_22out", "custodia_v397_23out"),
    ("errata_da_gerencia_c1_23out", "errata_da_gerencia_c1_24out"),
    (SNAP7, SNAP8),
    (P7, P8), (P6, P7),
    (str(DECL7), str(DECL8)), (str(DECL6), str(DECL7)), (str(FORM7), str(FORM8)), (str(FORM6), str(FORM7)),
    (ESC7, ESC8), (ESC6, ESC7),
    ("23/10/2026", "24/10/2026"), ("22/10/2026", "23/10/2026"), ("23/10", "24/10"), ("22/10", "23/10"),
    ("pedra v46", "pedra v47"), ("(v62)", "(v63)"), ("runner v62", "runner v63"), ("v62", "v63"),
    ("v397", "v398"), ("v396", "v397"), ("v395", "v396"),
]


def deslocar(nome, extra=(), regexes=()):
    s = (W7 / nome).read_text(encoding="utf-8")
    for k, ph in PROTEGE.items():
        s = s.replace(k, ph)
    for a, b in ORDEM:
        s = s.replace(a, b)
    for a, b, n in extra:
        c = s.count(a)
        assert c == n, (nome, a[:90], c, n)
        s = s.replace(a, b)
    for pat, rep in regexes:
        s, n = re.subn(pat, rep, s, flags=re.S)
        assert n == 1, (nome, pat[:60], n)
    for k, ph in PROTEGE.items():
        s = s.replace(ph, k)
    novo = nome.replace("v397", "v398").replace("v396", "v397")
    d = W8 / novo
    assert not d.exists(), ("já existe — PARAR", novo)
    compile(s, str(d), "exec")
    d.write_text(s, encoding="utf-8")
    sobras = [l.strip()[:110] for l in s.splitlines() if "v397" in l and "v398" not in l and "molde" not in l.lower() and "base" not in l.lower()]
    print("ok", novo, len(s), "| linhas só-v397 (base esperada):", len(sobras))
    for l in sobras[:6]:
        print("     ", l)


deslocar("cofre_v397.py", regexes=[(r'"errata_da_gerencia_c1_24out": "kh_n1_cobertura_v397 passa a cobrar pisos.*?os vereditos anteriores não mudam"\},',
                                    '"errata_da_gerencia_c1_24out": "kh_n1_cobertura_v397 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "\n'
                                    '                                                "os sete contratos (três da v394, o do Psibit da v395, o da testemunha da v396, o do sônico e o da afinação da v398) passam a ler expected_ladder = %s; "\n'
                                    '                                                "os vereditos anteriores não mudam"},' % ESC8.split("/")[0])])
deslocar("medir_v397_contra_v396.py")
deslocar("snapshot_chatgpt_v397.py")
deslocar("conferencia_final_v397.py")
deslocar("registro_v397_publicada.py")
s = (W7 / "acom_transicao.py").read_text(encoding="utf-8")
for a, b in (("custodia_v397_23out", "custodia_v398_24out"), ("claude-central-a7_custodia-v397-23out.json", "claude-central-a7_custodia-v398-24out.json"), ("custódia v397", "custódia v398")):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
(W8 / "acom_transicao.py").write_text(s, encoding="utf-8")
print("ok acom_transicao.py")
