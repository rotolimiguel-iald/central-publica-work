# -*- coding: utf-8 -*-
"""Deriva, por trocas CONTADAS a partir dos scripts da custódia v396, a parte mecânica do lado da Central para a v397 (23/10/2026, sessão a7;
regra do operador: custodiar quando o handoff aparecer): cofre_v397.py, medir_v397_contra_v396.py, snapshot_chatgpt_v397.py,
conferencia_final_v397.py, registro_v397_publicada.py e acom_transicao.py. Os números vêm de fatos_v397.json (lidos do selo, do core e do
manifesto por sondar_v397.py), nunca digitados aqui. Os patches com texto novo (runner v62, módulo dos 16, registro) são arquivos próprios."""
import json, re
from pathlib import Path

W6 = Path(r"C:\IALD\Central de Patentes\work\custodia_v396_22out")
W7 = Path(r"C:\IALD\Central de Patentes\work\custodia_v397_23out")
F = json.loads((W7 / "fatos_v397.json").read_text(encoding="utf-8"))
assert F["versao"] == "v397" and F["registros_novos"] == ["cunhagens_v397", "kh_n1_cobertura_v397", "teste_de_veracidade_fase9_v397"], F["registros_novos"]
PIN16, PIN16_6 = F["pin16"], "0a4395a89eeebbb7"
ESC, ESC6 = F["escada"], F["escada_v396"]
FORM, DECL, FORM6, DECL6 = F["kernel"]["formais"], F["kernel"]["declaracoes"], F["kernel"]["formais_v396"], F["kernel"]["declaracoes_v396"]
assert (FORM6, DECL6) == (1425, 29228) and ESC6 == "9498/9498", (FORM6, DECL6, ESC6)   # o molde (v396) é o que está escrito nos scripts


def derivar(orig, novo, trocas, regexes=()):
    s = (W6 / orig).read_text(encoding="utf-8")
    for a, b, n in trocas:
        c = s.count(a)
        assert c == n, (novo, a[:100], c, n)
        s = s.replace(a, b)
    for pat, rep in regexes:
        s, n = re.subn(pat, rep, s, flags=re.S)
        assert n == 1, (novo, pat[:60], n)
    d = W7 / novo
    assert not d.exists(), ("já existe — PARAR", novo)
    compile(s, str(d), "exec")
    d.write_text(s, encoding="utf-8")
    print("ok", novo, len(s))


derivar("cofre_v396.py", "cofre_v397.py", [
    ('"""CUSTÓDIA v396 — O COFRE DA CENTRAL (22/10/2026, sessão a7, por ordem do operador; molde: cofre_v395.py, base = o cofre v395).',
     '"""CUSTÓDIA v397 — O COFRE DA CENTRAL (23/10/2026, sessão a7, pela regra do operador de 23/10; molde: cofre_v396.py, base = o cofre v396).\n'
     'Do molde: CUSTÓDIA v396 — O COFRE DA CENTRAL (22/10/2026, sessão a7, por ordem do operador; molde: cofre_v395.py, base = o cofre v395).', 1),
    ('Ordem de 22/10 (verbatim no arquivo ORDEM, sha256 lido): «… Atualize tudo com a nova versão do um.py».',
     'Ordem de 23/10 (verbatim no arquivo ORDEM, sha256 lido): «pode custodiar sempre que o handoff aparecer, como regra».', 1),
    ('V = OC / "um_unificado_v396"\nKV = OC / "tgl_kernel_v396"\nV391 = OC / "um_unificado_v395"   # (nome herdado do molde: é a BASE, o cofre v395)\nKV391 = OC / "tgl_kernel_v395"',
     'V = OC / "um_unificado_v397"\nKV = OC / "tgl_kernel_v397"\nV391 = OC / "um_unificado_v396"   # (nome herdado do molde: é a BASE, o cofre v396)\nKV391 = OC / "tgl_kernel_v396"', 1),
    ('ORDEM = CEN / "work" / "custodia_v396_22out" / "OPERADOR_22out_custodia_v396_verbatim.txt"',
     'ORDEM = CEN / "work" / "php_e_v396_22out" / "OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt"', 1),
    ('"o cofre v396 já existe — PARAR (nada se sobrescreve)"', '"o cofre v397 já existe — PARAR (nada se sobrescreve)"', 1),
    ('pin.startswith("%s") and selo.get("um_version") == "v396"' % PIN16_6, 'pin.startswith("%s") and selo.get("um_version") == "v397"' % PIN16, 1),
    ('"gate != cofre v395 — PARAR"', '"gate != cofre v396 — PARAR"', 1),
    ('st = (NOS / "rodada_v396_stdout.txt")', 'st = (NOS / "rodada_v397_stdout.txt")', 1),
    ('assert "%s" in st, "a escada %s não está no stdout da v396 — PARAR"' % (ESC6, ESC6), 'assert "%s" in st, "a escada %s não está no stdout da v397 — PARAR"' % (ESC, ESC), 1),
    ('"HANDOFF_v395_CUSTODIA.md", "rodada_v395_stdout.txt")]', '"HANDOFF_v395_CUSTODIA.md", "rodada_v395_stdout.txt", "HANDOFF_v396_CUSTODIA.md", "rodada_v396_stdout.txt")]', 1),
    ('extra = ["rodada_v396_stdout.txt", "HANDOFF_v396_CUSTODIA.md"]', 'extra = ["rodada_v397_stdout.txt", "HANDOFF_v397_CUSTODIA.md"]', 1),
    ('"estatuto": "DOCUMENTO (do cofre v395)"})', '"estatuto": "DOCUMENTO (do cofre v396)"})', 1),
    ('worker e spec do cofre v395 == Nós', 'worker e spec do cofre v396 == Nós', 1),
    ('for n in ("v396_incorporacao_manifesto.json",):', 'for n in ("v397_incorporacao_manifesto.json",):', 1),
    ('(o kernel vai inteiro em tgl_kernel_v396)', '(o kernel vai inteiro em tgl_kernel_v397)', 1),
    ('for d in ("v396", "v396_selo"):', 'for d in ("v397", "v397_selo"):', 1),
    ('"cadeia_de_selo_v396"', '"cadeia_de_selo_v397"', 3),
    ('"MANIFESTO_CADEIA_DE_SELO_v396.json"', '"MANIFESTO_CADEIA_DE_SELO_v397.json"', 1),
    ('km = {"version": "v396",', 'km = {"version": "v397",', 1),
    ('"delta_v395_v396": {', '"delta_v396_v397": {', 1),
    ('"formal_files_v395": k391.get("formal_files"), "declaracoes_v395": k391.get("declaracoes_no_axiom_report")},',
     '"formal_files_v396": k391.get("formal_files"), "declaracoes_v396": k391.get("declaracoes_no_axiom_report")},', 1),
    ('"modulos_novos_v396": novos,', '"modulos_novos_v397": novos,', 1),
    ('if isinstance(v, dict) and re.search(r"_v396$", k)}', 'if isinstance(v, dict) and re.search(r"_v397$", k)}', 1),
    ('mv = {"version": "v396", "custodia": ["v396"],', 'mv = {"version": "v397", "custodia": ["v397"],', 1),
    ('"um_version_no_selo": "v396",', '"um_version_no_selo": "v397",', 1),
    ('"gate_identico_ao_da_v395": True,', '"gate_identico_ao_da_v396": True,', 1),
    ('"escada": "%s (rodada_v396_stdout.txt)",' % ESC6, '"escada": "%s (rodada_v397_stdout.txt)",' % ESC, 1),
    ('"lean_novos_desde_v395": len(novos)},', '"lean_novos_desde_v396": len(novos)},', 1),
    ('"registros_novos_v396": regs,', '"registros_novos_v397": regs,', 1),
    (r'um_v395_8918b17803792cf2 (a v395 que estava no espelho; feito no passo zero da custódia do espelho)',
     r'um_v396_%s (a v396 que estava no espelho; feito no passo zero da custódia do espelho)' % PIN16_6, 1),
    (r'"work\\cadeia_de_selo v396 e v396_selo filtradas em cadeia_de_selo_v396/ (ver MANIFESTO_CADEIA_DE_SELO_v396.json)"',
     r'"work\\cadeia_de_selo v397 e v397_selo filtradas em cadeia_de_selo_v397/ (ver MANIFESTO_CADEIA_DE_SELO_v397.json)"', 1),
    ('"handoff": "HANDOFF_v396_CUSTODIA.md fica no Nós e neste cofre privado",', '"handoff": "HANDOFF_v397_CUSTODIA.md fica no Nós e neste cofre privado",', 1),
    ('print("COFRE v396: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v395), "',
     'print("COFRE v397: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v396), "', 1),
    ('"axiom_report %d, gate = cofre v395"', '"axiom_report %d, gate = cofre v396"', 1),
], regexes=[(r'"errata_da_gerencia_c1_22out": "kh_n1_cobertura_v395 passa a cobrar pisos.*?os vereditos anteriores não mudam"\},',
             '"errata_da_gerencia_c1_23out": "kh_n1_cobertura_v396 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "\n'
             '                                                "os cinco contratos (três da v394, o do Psibit da v395 e o da testemunha da v396) passam a ler expected_ladder = %s; "\n'
             '                                                "os vereditos anteriores não mudam"},' % ESC.split("/")[0])])

derivar("medir_v396_contra_v395.py", "medir_v397_contra_v396.py", [
    ('C4, C1 = OC / "um_unificado_v396", OC / "um_unificado_v395"', 'C4, C1 = OC / "um_unificado_v397", OC / "um_unificado_v396"', 1),
    ('"""Medição (só leitura) do cofre v396 contra o cofre v395, para a pedra v45 do runner da Fronteira (v61).',
     '"""Medição (só leitura) do cofre v397 contra o cofre v396, para a pedra v46 do runner da Fronteira (v62).', 1),
])

derivar("snapshot_chatgpt_v396.py", "snapshot_chatgpt_v397.py", [
    ("custódia v396 (22/10/2026, sessão a7)", "custódia v397 (23/10/2026, sessão a7)", 1),
    ('assert base.name == "Chatgpt_20261021_175747_delta_de_20261019_190704", base.name', 'assert base.name == "Chatgpt_20261022_201134_delta_de_20261021_175747", base.name', 1),
    ("v2 (custodia v396, 22/10; exclusoes iguais as de 15/09)", "v2 (custodia v397, 23/10; exclusoes iguais as de 15/09)", 1),
])

derivar("conferencia_final_v396.py", "conferencia_final_v397.py", [
    ('"""CONFERÊNCIA FINAL INDEPENDENTE da custódia v396 (22/10/2026, sessão a7; molde: a da v395).', '"""CONFERÊNCIA FINAL INDEPENDENTE da custódia v397 (23/10/2026, sessão a7; molde: a da v396).', 1),
    ('um.py v396 = o pino', 'um.py v397 = o pino', 1),
    ('o cofre um_unificado_v396:', 'o cofre um_unificado_v397:', 1),
    ('o cofre tgl_kernel_v396: cada arquivo formal do manifesto de prova bate (%d)' % FORM6, 'o cofre tgl_kernel_v397: cada arquivo formal do manifesto de prova bate (%d)' % FORM, 1),
    ('o index traz «v396 · <pin16>»', 'o index traz «v397 · <pin16>»', 1),
    ('V, KV = CEN / "vault" / "originals_copy" / "um_unificado_v396", CEN / "vault" / "originals_copy" / "tgl_kernel_v396"',
     'V, KV = CEN / "vault" / "originals_copy" / "um_unificado_v397", CEN / "vault" / "originals_copy" / "tgl_kernel_v397"', 1),
    ('"User-Agent": "conferencia-final-v396"', '"User-Agent": "conferencia-final-v397"', 1),
    ('item("1 selo do Nós = v396 e o pino", selo.get("um_version") == "v396" and sha(b_nos) == pin, p16)',
     'item("1 selo do Nós = v397 e o pino", selo.get("um_version") == "v397" and sha(b_nos) == pin, p16)', 1),
    ('item("2 cofre v396: artefatos do selo presentes conferem"', 'item("2 cofre v397: artefatos do selo presentes conferem"', 1),
    ('item("3 cofre do kernel: arquivos formais conferem", len(ff) == %d and not kdiv,' % FORM6, 'item("3 cofre do kernel: arquivos formais conferem", len(ff) == %d and not kdiv,' % FORM, 1),
    ('item("3 axiom_report no trio", len(pm["axiom_report"]) == %d and not fora,' % DECL6, 'item("3 axiom_report no trio", len(pm["axiom_report"]) == %d and not fora,' % DECL, 1),
    ('item("5 site no ar: index com «v396 · pin16»", ("v396 \\u00b7 " + p16) in si)', 'item("5 site no ar: index com «v397 · pin16»", ("v397 \\u00b7 " + p16) in si)', 1),
    ('["vault/originals_copy/um_unificado_v396", "vault/originals_copy/tgl_kernel_v396", "fronteira_tgl",',
     '["vault/originals_copy/um_unificado_v397", "vault/originals_copy/tgl_kernel_v397", "fronteira_tgl",', 1),
    ('out = CEN / "work" / "custodia_v396_22out" / "CONFERENCIA_FINAL_v396.json"', 'out = CEN / "work" / "custodia_v397_23out" / "CONFERENCIA_FINAL_v397.json"', 1),
])

derivar("registro_v396_publicada.py", "registro_v397_publicada.py", [
    ('"""Pós-push da custódia v396 (22/10/2026, sessão a7; molde: o da v395)', '"""Pós-push da custódia v397 (23/10/2026, sessão a7; molde: o da v396)', 1),
    (r'W = r"C:\IALD\Central de Patentes\work\custodia_v396_22out"', r'W = r"C:\IALD\Central de Patentes\work\custodia_v397_23out"', 1),
    ('cf = json.load(open(os.path.join(W, "CONFERENCIA_FINAL_v396.json"), encoding="utf-8"))', 'cf = json.load(open(os.path.join(W, "CONFERENCIA_FINAL_v397.json"), encoding="utf-8"))', 1),
    ('"(`work/custodia_v396_22out/conferencia_final_v396.py`, sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no "',
     '"(`work/custodia_v397_23out/conferencia_final_v397.py`, sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no "', 1),
    ('"raw do GitHub (o pino); o cofre e o kernel (%d formais; %d declarações no trio) conferem; o site no ar e o README raw trazem o pino; "' % (FORM6, DECL6),
     '"raw do GitHub (o pino); o cofre e o kernel (%d formais; %d declarações no trio) conferem; o site no ar e o README raw trazem o pino; "' % (FORM, DECL), 1),
    ('ap(os.path.join(MEM, "handoff-v396-custodia.md"), "## %s — PUBLICADA (pós-push)\\n\\n%s" % (AGORA, TXT))',
     'ap(os.path.join(MEM, "handoff-v397-custodia.md"), "## %s — PUBLICADA (pós-push)\\n\\n%s" % (AGORA, TXT))', 1),
    ('ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v396 publicada\\n\\n%s" % (AGORA, TXT))',
     'ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v397 publicada\\n\\n%s" % (AGORA, TXT))', 1),
    ('ap(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\DIARIO_DO_SITE.md", "## %s — a custódia v396 PUBLICADA\\n\\n%s" % (AGORA, TXT))',
     'ap(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\DIARIO_DO_SITE.md", "## %s — a custódia v397 PUBLICADA\\n\\n%s" % (AGORA, TXT))', 1),
    # a linha do MEMORY.md: o título do handoff v397 é o que a gerência c1 escreveu; lê-se pelo prefixo, e o título é preservado
    ('old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md)")]',
     'old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v397 ")]', 1),
    ('nova = ("- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md) — **22/10: PUBLICADA** "\n'
     '        "(the_boundary `%s`; Central `%s`; site no ar; cofre v396, runner v61, 16/16, FINAL, ledger 0; conferência final %d/%d) · `0a4395a89eeebbb7`"',
     'nova = (old[0].split(" — **")[0].split(") — ")[0] + ") — **23/10: PUBLICADA** "\n'
     '        "(the_boundary `%s`; Central `%s`; site no ar; cofre v397, runner v62, 16/16, FINAL, ledger 0; conferência final %d/%d) · `' + PIN16 + '`"', 1),
])

s = (W6 / "acom_transicao.py").read_text(encoding="utf-8")
for a, b in (("custodia_v396_22out", "custodia_v397_23out"), ("claude-central-a7_php-v396-22out.json", "claude-central-a7_custodia-v397-23out.json"),
             ("custódia v396 + PHP", "custódia v397")):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
(W7 / "acom_transicao.py").write_text(s, encoding="utf-8")
print("ok acom_transicao.py")
