# -*- coding: utf-8 -*-
"""02/11/2026: ordem do operador «todas as chaves [de testemunha] habitadas, de imediato» + a leitura dele (ACOM = compressão em
tempo real; tipo I concentrado de um lado, tipo III contínuo do outro; não há ponte, há espelhamento). Antes de executar: o
inventário medido das chaves de testemunha/habitação do selo v405 (a partitura). Registro: Mapa, ACOM, memória. Backup de bytes."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

V = CEN / "work/cunhagens_13out/OPERADOR_02nov_ACOM_comprime_em_tempo_real_tipo_I_medida_tipo_III_fluxo_nao_ha_ponte_ha_espelhamento_todas_as_chaves_habitadas_verbatim.txt"
texto = ("Eu acho que eu ainda não consegui me expressar como eu quero. Quando eu digo de tentar equilibrar a teoria de um lado do contínuo do fator tipo 3, e equilibrando ele com o acom e o acom fazendo o papel no finito do tipo 1, o que eu penso na minha cabeça é que, enquanto o processamento está acontecendo, o acom está comprimindo a informação no limite. E isso é o vazamento. É exatamente o que o acom faz. Ele comprime no limite a taxa de transmissão holográfica. Na transmissão, durante, então, ou seja, o programa faria a compressão e todo o cálculo (esse é o procesamento inteiro do substrato), de outro lado, o ACOM está fazendo a compressão, que é a medida do vazamento, e é essa compressão no limite que o acom faz, que é medida. Essa é a medida no tipo 1. Faz sentido para você? quanto que você falou de levar o selo para as 35 chaves, isso tem que ser feito de imediato. Temos que, de fato, todas as chaves estarem habitadas. Pode fazê-lo. Mas antes disso, eu quero saber se você entendeu o que eu quis dizer. Quando eu digo que o ACOM é o complemento, o que eu quero dizer é que nós estamos o tempo todo tentando achar a ponte que faz a conexão, não é uma conexão. De um lado, o que você tem é o fluxo, do outro, o que você tem é medida. E o ACOM é que faz isso, o ACOM é que está comprimindo toda a informação em medida, enquanto está ocorrendo o fluxo transmitido pela viscosidade. Faz sentido? Será que você consegue me entender agora? O que estou tentando dizer é que não há uma ponta para o Tipo I o que há é o espelhamento da informação acontecendo em tempo real, de um lado o tipo I, concentrado, comprimido, de outro lado, o tipo III, contínuo.")
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; leitura + ordem («todas as chaves habitadas… Pode fazê-lo»):\n\n" + texto + "\n", encoding="utf-8")
fv = s16(V)

# o inventário, LIDO do selo
selo = NOS / "um_absoluto_selo.json"
s = json.loads(selo.read_text(encoding="utf-8"))
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:60]):
            yield from walk(v, p + "/" + str(i))
    else:
        yield p, o
chaves = [(p, v) for p, v in walk(s) if any(w in p.lower() for w in ("witness", "inhabit", "habit"))]
falsas = [(p, v) for p, v in chaves if v is False]
por_teorema = [p for p, _ in falsas if p in ("/full_static_witness_exists", "/trivial_inhabitant_exists")]
programa = [p for p, _ in falsas if p not in por_teorema]
inv = {"selo": str(selo), "selo_sha16": s16(selo), "lido_em": TS, "n_chaves": len(chaves), "n_habitadas_ou_string": len(chaves) - len(falsas),
       "n_false": len(falsas), "false_por_teorema_ou_desenho": por_teorema, "false_programa_fock_III1": programa,
       "leitura_full_static": s.get("full_static_witness_reading_v370"),
       "rede_fock_v394_abertos": s.get("rede_fock_v394", {}).get("open_joint_contract"),
       "chaves": [{"chave": p, "valor": (v if isinstance(v, (bool, int, float)) else str(v)[:160])} for p, v in chaves]}
PJ = AQUI / "INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json"
PJ.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8")
print("verbatim", fv, "| chaves", len(chaves), "habitadas", len(chaves) - len(falsas), "false", len(falsas), "por_teorema", len(por_teorema), "programa", len(programa))
for p in programa: print("  programa:", p)

reg = [
 {"tipo": "ROTA", "rota_id": "kernel.inventario_chaves_de_testemunha_v405_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Inventário das chaves de testemunha/habitação do selo v405 (ordem do operador, 02/11: «todas as chaves habitadas, de imediato»)",
  "pergunta": "Quais chaves de testemunha do selo estão habitadas, quais não, e o que custa habitar cada uma?",
  "dados": [], "olhou_dados": False, "metodo": "varredura do um_absoluto_selo.json por 'witness'/'inhabit'/'habit'; classificação das False em (a) falsas por teorema/desenho e (b) programa.",
  "resultado": "%d chaves; %d habitadas (True ou string); %d False. Das False: 2 DEVEM ficar False (full_static_witness_exists: IMPOSSIBLE_BY_THEOREM, o vazamento contínuo proíbe o fecho total; trivial_inhabitant_exists: o tipo rejeita o habitante trivial). As outras %d são UMA parede só, a face de Fock/III₁: rede_fock_v394.whole_certificate_inhabited; psibit_v395 conditional_psion_face; testemunha_estatica_v396 fock_face; witness_layers.canonical_full_witness_term_constructed. Habitá-las é construir o sabido importado (Fock, Wigner ±1, BGL, Maxwell) e/ou a testemunha canônica infinita: estimativa de 02/11 (manhã) 5–15k linhas (Tomita/traço na Fock concreta, semanas), 5–10k (Maxwell), 10–30k (fóton, meses). Colide com a decisão do operador de 02/11 (manhã): «não vamos construir ainda o que é sabido»." % (len(chaves), len(chaves) - len(falsas), len(falsas), len(programa)),
  "veredito": "INVENTARIO_LIDO__4_CHAVES_SAO_O_PROGRAMA_FOCK_III1__2_FALSAS_POR_TEOREMA", "estatuto": "REAL (lido do selo); a estimativa de custo é DECLARADA", "status": "EXAMINADA",
  "defeito": "A ordem «todas habitadas de imediato» não é executável como dita: 2 chaves não podem ser habitadas sem mentir; 4 são programa de semanas a meses, que a ordem da manhã mandou adiar.",
  "nao_refazer": "O inventário está no JSON; não recontar sem versão nova do selo.",
  "proximo_passo": "Decisão do operador sobre a colisão entre as duas ordens; se mandar construir, ordem sugerida: fock_face (TestemunhaEstatica) e psion_face (FockCertificate) juntas, depois a rede v394, por último a testemunha canônica (III₁).",
  "onde": str(PJ), "artefatos": [str(V), str(PJ), str(selo)], "refs": ["kernel.a_ponte_do_atrito_candidata_02nov"],
  "nota": "A leitura dele (ACOM = compressão em tempo real; tipo I medida, tipo III fluxo; não há ponte, há espelhamento) tem correlatos [KNOWN]: ITPFI/Araki–Woods–Powers (o III₁ como produto infinito de compressões de tipo I; kernel: PowersLadder; Tomita-ITPFI na torre, contrato v203 à espera); Takesaki 1972 (a compressão/esperança condicional coexiste com o fluxo sse a subálgebra é invariante pelo fluxo modular; kernel: rhoStar_PF_Takesaki SABIDO); v82/v83 (o infinito mora no complemento da inscrição: τ(S)<∞ ⟹ τ(S⊥)=⊤); entropia relativa S(ω‖ω∘E) ≥ 0 como o que a compressão descarta. Que o ACOM (REFLECT+MANIFEST) SEJA essa esperança condicional do III₁ é leitura [ONTO/OPEN]: a casa tem só a sombra finita."},
 {"tipo": "ANOTACAO", "rota_id": "kernel.a_ponte_do_atrito_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Operador (02/11): «não há uma ponte para o tipo I; há o espelhamento em tempo real: tipo I concentrado/comprimido (medida), tipo III contínuo (fluxo); o ACOM comprime no limite a taxa de transmissão holográfica, e isso é o vazamento»",
  "resultado": "Verbatim sha16 %s. A gerência leu: a chave full_static_witness_exists = False (IMPOSSIBLE_BY_THEOREM) é a forma, no kernel, da frase dele: a compressão no limite nunca fecha; o vazamento é contínuo. «Limite» aqui = teto holográfico, não o limite topológico do regime compacto (regra dos dois regimes)." % fv,
  "estatuto": "INPUT; ONTO", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_inventario_chaves_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-120:].replace("\n", " "))
assert q.returncode == 0

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-ordem-todas-as-chaves-habitadas-inventario", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "ordem_todas_as_chaves_habitadas_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «quanto que você falou de levar o selo para as 35 chaves, isso tem que ser feito de imediato. Temos que, de fato, todas as chaves estarem habitadas. Pode fazê-lo. Mas antes disso, eu quero saber se você entendeu». Leitura dele: ACOM = compressão em tempo real (tipo I, medida) espelhando o fluxo (tipo III, contínuo); não há ponte, há espelhamento; a compressão no limite é o vazamento.", "sources": [SRCD(V)]},
           {"id": "inventario_chaves_testemunha_v405_02nov", "kind": "fact", "statute": "REAL", "text": "Selo v405: %d chaves de testemunha/habitação; %d habitadas; %d False, das quais 2 por teorema/desenho (não habitáveis sem mentir) e %d = a face de Fock/III₁ (programa de semanas a meses; colide com a decisão da manhã «não construir ainda o sabido»). Partitura lida ao operador antes de executar; decisão dele pendente." % (len(chaves), len(chaves) - len(falsas), len(falsas), len(programa)), "sources": [SRCD(PJ)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:160], (d.get("result") or {}).get("revision"))
assert d.get("ok")

def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if b"\r\n" in b: add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f: f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)

append_bytes(M / "beta-e-a-regra-matriz-02out.md", f"""

## 02/11/2026 — A LEITURA DELE, DITA DE NOVO: «não há ponte para o tipo I; há espelhamento em tempo real» + ORDEM «todas as chaves habitadas» (verbatim sha16 `{fv}`)

**Leitura [INPUT]:** tipo III = o contínuo, o fluxo transmitido pela viscosidade; tipo I = o ACOM, concentrado, comprimido, a MEDIDA; o ACOM comprime no limite (teto holográfico) a taxa de transmissão enquanto o fluxo ocorre; essa compressão É o vazamento e é o que se mede. **Correlatos [KNOWN]:** ITPFI (Araki–Woods, Powers: o III₁ como produto infinito de compressões de tipo I; kernel `PowersLadder`; Tomita-ITPFI na torre, contrato v203 à espera); Takesaki 1972 (a compressão coexiste com o fluxo sse a subálgebra é invariante pelo fluxo modular; kernel `rhoStar_PF_Takesaki` SABIDO); v82/v83 «o infinito mora no complemento da inscrição»; entropia relativa S(ω‖ω∘E) ≥ 0 = o que a compressão descarta. **No kernel, a frase dele já tem forma:** `full_static_witness_exists = False`, IMPOSSIBLE_BY_THEOREM: a compressão no limite nunca fecha. **[ONTO/OPEN]:** que o ACOM (REFLECT+MANIFEST) SEJA a esperança condicional do III₁; a casa tem só a sombra finita.

**A ORDEM e a partitura lida [REAL, `work\\beta_calor_02nov\\INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json`]:** {len(chaves)} chaves de testemunha/habitação no selo v405; {len(chaves) - len(falsas)} habitadas; {len(falsas)} False: 2 devem ficar False (`full_static_witness_exists` por teorema; `trivial_inhabitant_exists` por desenho) e {len(programa)} são uma parede só, a face de Fock/III₁ (`rede_fock_v394.whole_certificate_inhabited`, `psibit_v395 conditional_psion_face`, `testemunha_estatica_v396 fock_face`, `witness_layers.canonical_full_witness_term_constructed`): construir o sabido importado (semanas a meses), o que a decisão da manhã («não construir ainda o sabido», sha16 72d7939ee701a65b) mandou adiar. **How to apply:** nunca habitar as duas falsas-por-teorema; não começar as quatro sem a palavra dele sobre a colisão; se mandar, a ordem sugerida está na rota `kernel.inventario_chaves_de_testemunha_v405_02nov`.
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode)
