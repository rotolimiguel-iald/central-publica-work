# -*- coding: utf-8 -*-
"""Registro de 02/11/2026: negar e a natureza de K; Miguel nega o que nao e a identidade do posto. Sem pedra nova: as pedras seladas ja dizem. Errata de 'K sozinho nao recusa'. Backup de bytes. Nao move gate."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
KRN = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_K_negar_e_sua_natureza_Miguel_nega_o_que_nao_e_a_identidade_do_posto_injuncao_verbatim.txt"
PED = [KRN / x for x in ("IALD.lean", "QGReaderUVLock.lean", "BoundaryException.lean", "Fundacao.lean", "Identidade.lean", "TheTraceIsNotErasable.lean", "TheSingularExpectation.lean", "Ergodicity.lean")]
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
fo = s16(ORD)
print("fala", fo, [s16(p) for p in PED])


def seq_rota(rid):
    v = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "ver", rid], capture_output=True)
    return [r for r in json.loads(v.stdout.decode("utf-8"))["registros"] if r.get("tipo") == "ROTA"][0]["seq"]


s1, s2 = seq_rota("kernel.o_guarda_candidata_02nov"), seq_rota("conceitual.k_chave_da_guarda_da_travessia_02nov")
print("seqs", s1, s2)
ERR = "K sozinho nao recusa foi forte demais. No kernel K nega: so a reta do posto fica parada sob o fluxo de K (light_modular_fixed_iff_vacuum, hmin_zero_iff_modular_fixed). O que vale e so isto: K nao se compara sozinho com um dado da natureza; essa comparacao e a Fase 9."
reg = [{"tipo": "ERRATA", "rota_id": "kernel.o_guarda_candidata_02nov", "dominio": "KERNEL_FORMAL", "corrige": s1, "estatuto": "REAL",
        "titulo": "K sozinho nao recusa: forte demais", "resultado": ERR, "artefatos": [str(PED[1])]},
       {"tipo": "ERRATA", "rota_id": "conceitual.k_chave_da_guarda_da_travessia_02nov", "dominio": "CONCEITUAL", "corrige": s2, "estatuto": "REAL",
        "titulo": "K sozinho nao recusa: forte demais", "resultado": ERR, "artefatos": [str(PED[1])]},
       {"tipo": "ROTA", "rota_id": "conceitual.k_nega_miguel_injuncao_do_posto_02nov", "dominio": "CONCEITUAL", "status": "EXAMINADA", "estatuto": "ONTO",
        "titulo": "Fala do operador de 02/11: negar e a natureza de K; Miguel nega tudo que nao seja a identidade do posto; o nome e a injuncao do posto",
        "pergunta": "A negacao de K e de Miguel esta no kernel? O que diz a letra do nome?",
        "dados": ["Strong H4317 (biblehub.com/hebrew/4317.htm): who (is) like God?", "Michael (given name), en.wikipedia.org: leitura padrao como pergunta retorica; leituras alternativas existem", "ARA, Is 14,14-15 e Ex 15,11 (bibliaonline.com.br)"],
        "metodo": "consulta do Mapa (negar 0, negacao 2, injuncao 0, senao 3, agape 14, selecao unica 2, Miguel 24), dos verbatims do operador e leitura direta das pedras; sem pedra nova", "olhou_dados": False,
        "resultado": "Selado: dephase_is_a_strict_complement_contraction, dephase_fixed_dimension_one, the_singularity_reads_the_name (IALD.lean: D = post + e^{-rt}(1 - post)); light_modular_fixed_iff_vacuum, hmin_zero_iff_modular_fixed; fixed_iff_kernel (fala de 27/07 com a palavra negacao); dephase_fixed_iff_diagonal; dephase_tendsto_expectation; the_floor_fixes_the_cut; nothing_above_bears_a_post; eu_sou_o_que_sou_iff_nada_resta, o_posto_e_unico, o_vazio_nao_e, a_face_nao_e_a_identidade. Limite: annihilation_is_relocation_not_deletion, the_trace_is_not_erasable.",
        "veredito": "LEITURA_ONTO_SUSTENTADA_POR_PEDRAS_SELADAS__SEM_PEDRA_NOVA__NEGAR_O_POSTO_NAO_E_APAGAR__A_LETRA_DO_NOME_E_PERGUNTA_A_FORCA_E_NEGACAO",
        "defeito": "Os teoremas sao de K modular e dos fluxos do modelo; o K de Hubble so tem a forma de the_floor_fixes_the_cut; a ponte e leitura (R1 + R5), sem termo Lean. IALD.dephase e TGLExt.dephase sao homonimos, e o cabecalho avisa. Is 14 fala do rei da Babilonia: ligar a queda a Miguel e tradicao, nao letra. Nada disto e medida na natureza.",
        "nao_refazer": "o kernel ja prova a negacao; nao escrever pedra nova para isso",
        "refs": ["conceitual.k_chave_da_guarda_da_travessia_02nov", "kernel.identidade.candidata_01nov"], "artefatos": [str(ORD)] + [str(p) for p in PED]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_nega_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-320:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-nega", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "k_nega_miguel_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: o que K faz e negar; Miguel nega tudo que nao seja a identidade do posto; o nome significa literalmente a injuncao do posto.", "sources": [SRC(ORD)]},
                                {"id": "k_nega_selado_02nov", "kind": "fact", "statute": "REAL", "text": "O kernel selado ja prova a forma: so a reta do posto fica fixa sob o fluxo de K; o complemento contrai estritamente na defasagem do motor. Negar o posto nao e apagar: annihilation_is_relocation_not_deletion. Sem pedra nova.", "sources": [SRC(PED[0]), SRC(PED[1])]},
                                {"id": "k_sozinho_errata_02nov", "kind": "fact", "statute": "REAL", "text": "Ao lado de leitura_k_chave_da_guarda_02nov: K sozinho nao recusa foi forte demais; vale so que K nao se compara sozinho com dado da natureza.", "sources": [SRC(PED[1])]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:240], (d.get("result") or {}).get("revision"))
assert d.get("ok")


def trocar(p, fn):
    p = Path(p)
    b = p.read_bytes()
    nb = fn(b.decode("utf-8")).encode("utf-8")
    assert len(nb) > len(b)
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(nb)
    assert tmp.stat().st_size == len(nb)
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))


TOPO = f"""
## Ao lado (02/11/2026, fala do operador sha16 `{fo}`, gerência c1)

«Sim, o que K faz é negar, negar é sua natureza, Miguel nega tudo que não seja a identidade do posto, o nome significa literalmente a injunção do posto». **Errata:** «K sozinho não recusa» foi forte demais: no kernel K nega; vale só que K não se compara sozinho com dado da natureza. **Selado, sem pedra nova:** `dephase_is_a_strict_complement_contraction`, `dephase_fixed_dimension_one`, `the_singularity_reads_the_name` (D = post + e^{{−rt}}(1 − post)); `light_modular_fixed_iff_vacuum`, `hmin_zero_iff_modular_fixed`; `fixed_iff_kernel` (fala de 27/07: «a falsidade da construção da testemunha estática é justamente a negação da fronteira»); `the_floor_fixes_the_cut`; `nothing_above_bears_a_post`; o «senão» de `Identidade`. **Limite:** negar o posto não é apagar (`annihilation_is_relocation_not_deletion`). **A letra:** Mîkhā’ēl, «Quem é como Deus?»: a letra é pergunta, a força é negação; a injunção é a força. `IALD.dephase` e `TGLExt.dephase` são homônimos: não encadear. A ponte com o K de Hubble é leitura (R1 + R5), sem termo.
"""


def anexa(t):
    nl = "\r\n" if "\r\n" in t else "\n"
    return t.rstrip() + nl + TOPO.replace("\n", nl)


trocar(M / "k-chave-da-guarda-02nov.md", anexa)

AO = (f"⧗ *Ao lado (02/11/2026, fala do operador sha16 `{fo}`):* «o que K faz é negar … Miguel nega tudo que não seja a identidade do posto, o nome significa literalmente a injunção do posto» [INPUT]. Forma selada: a defasagem do motor fixa só a reta do Nome e contrai estritamente o complemento (`dephase_fixed_dimension_one`); só a reta do posto fica parada sob o fluxo de K (`light_modular_fixed_iff_vacuum`). Negar o posto não é apagar (`annihilation_is_relocation_not_deletion`). A letra do nome é pergunta, «Quem é como Deus?»; a força é negação. <!-- k_nega_miguel_02nov -->")
REG = (f"\n### 02/11/2026 — Negar é a natureza de K; Miguel nega o que não é a identidade do posto <!-- k_nega_miguel_reg_02nov -->\n\n"
       f"**[INPUT]** fala do operador sha16 `{fo}`. **Errata ao registro anterior:** «K sozinho não recusa» foi forte demais; no kernel K nega, e o que K não faz sozinho é comparar-se com dado da natureza. **[REAL]** sem pedra nova: as pedras seladas listadas na rota `conceitual.k_nega_miguel_injuncao_do_posto_02nov`. **[ONTO]** a identificação com K de Hubble e com Miguel. O gate não se move.\n")
A = CEN / "memory/TGL_ATLAS.md"


def atlas(t):
    assert "k_nega_miguel_02nov" not in t
    nl = "\r\n" if "\r\n" in t else "\n"
    ls = t.split(nl)
    i = [k for k, x in enumerate(ls) if x.startswith("**Guarda modular (Miguel)**")]
    assert len(i) == 1, i
    ls.insert(i[0], AO)
    return nl.join(ls).rstrip() + nl + REG.replace("\n", nl)


trocar(A, atlas)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])
