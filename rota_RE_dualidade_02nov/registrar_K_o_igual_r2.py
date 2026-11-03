# -*- coding: utf-8 -*-
"""Registro r2 de 02/11/2026: errata (13 teoremas), o acervo (H3c de 22/06, I = graviton fundamental), segunda candidata, a porta da transposicao inteira. Backup de bytes. Nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_K_faz_a_funcao_do_graviton_operador_igual_que_criva_verbatim.txt"
C1 = AQUI / "OIgualCandidata.lean"
C2 = AQUI / "OIgualRestauradoCandidata.lean"
S2 = AQUI / "OIgualRestauradoCandidata_saida.txt"
S1K = AQUI / "OIgualCandidata_saida_K_pos.txt"
H3 = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/TGL_CODE_ONE_REAL_FALSIFIER/code_one_ponte_attention/TGL_H3C_BETA_PAID_ATTENTION_THEOREM.md")
NOTA = AQUI / "DERIVACAO_RE_02nov.md"
CONTAS = AQUI / "CONTAS_TRANSPOSICAO.json"
for a, b in (("C:/t/igual02nov/OIgualRestauradoCandidata.lean", C2), ("C:/t/igual02nov/saida_restaurado.txt", S2), ("C:/t/igual02nov/saida_aud.txt", S1K)):
    if not b.exists():
        shutil.copyfile(a, b)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
txt = (AQUI / "CONTAS_RE.json").read_text(encoding="utf-8")
ks = re.findall(r'"([^"]{0,40})"\s*:\s*(1\.08\d{6,})', txt)
print("candidatos K", ks[:4])
K = float(ks[0][1])
assert abs(K - 1.0838) < 1e-3
Yp, sYp = 0.2453, 0.0034
c = {"K": K, "lambda2": K * K, "fracao_densidade_1_menos_1_K2": 1 - 1 / K ** 2, "fracao_peso_1_menos_1_K": 1 - 1 / K,
     "Yp_medido_Aver_citado_em_GeCyrRacineKnox": Yp, "sigma_Yp": sYp, "Yp_exigido_Eq16_1menosYp_vezes_lambda": 1 - K * (1 - Yp),
     "distancia_sigma": (Yp - (1 - K * (1 - Yp))) / sYp, "T0_FIRAS_K": 2.7255, "T0_sobre_K": 2.7255 / K,
     "fonte_K": "CONTAS_RE.json", "regra": "Eq. 16 de arXiv:2210.16335: 1-YP -> lambda(1-YP) com rho_b fixo"}
with open(CONTAS, "x", encoding="utf-8", newline="\n") as f:
    json.dump(c, f, ensure_ascii=False, indent=1)
print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in c.items() if k in ("lambda2", "fracao_densidade_1_menos_1_K2", "Yp_exigido_Eq16_1menosYp_vezes_lambda", "distancia_sigma")})
fo, f1, f2, fh = s16(ORD), s16(C1), s16(C2), s16(H3)
yr, ds, f2d = round(c["Yp_exigido_Eq16_1menosYp_vezes_lambda"], 3), round(c["distancia_sigma"], 1), round(100 * c["fracao_densidade_1_menos_1_K2"], 1)
print("sha16", fo, f1, f2, fh)

v = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "ver", "kernel.k_operador_igual_candidata_02nov"], capture_output=True)
seq = [r for r in json.loads(v.stdout.decode("utf-8"))["registros"] if r.get("tipo") == "ROTA"][0]["seq"]
print("seq da rota", seq)

reg = [{"tipo": "ERRATA", "rota_id": "kernel.k_operador_igual_candidata_02nov", "dominio": "KERNEL_FORMAL", "corrige": seq, "estatuto": "REAL",
        "titulo": "13 teoremas, nao 12; o_fundo_e_a_media rearranja a definicao, nao e mecanismo",
        "resultado": "K_pos compilou sem #print axioms na saida; auditado em copia: trio; a candidata nao mudou. o_fundo_e_a_media e H0local rearranjado com um zero escrito pela gerencia; H0local e definicao cunhada por ordem do operador. O residuo sobre o setor de 7,7% foi mal posto: o acervo ja dizia que o vazamento vai ao espelho.",
        "artefatos": [str(S1K), str(C1)]},
       {"tipo": "ROTA", "rota_id": "kernel.o_igual_restaurado_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
        "titulo": "Candidata: o igual quebra no peso bruto, volta ao dividir pelo traco, e o divisor e o da lei de K",
        "pergunta": "K e o fator que faz o igual valer depois do custo?",
        "metodo": "sandbox k405c, lake env lean; forma de T(P)/Tr T(P) = P do H3c de 22/06 no caso em que P e modo proprio, com o peso survivingWeightContrast do kernel; kernel selado intocado", "olhou_dados": False,
        "resultado": "6 teoremas, trio, 0 sorry: o_traco_e_o_peso, o_igual_volta, o_peso_nao_e_um, o_igual_quebra, o_mesmo_denominador, o_todo_fica.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__K_E_O_INVERSO_DO_TRACO__H3C_NAO_PROVADO__NOME_DO_OPERADOR_PENDENTE",
        "defeito": "P modo proprio e hipotese embutida em transporte; o H3c segue condicional a H1-H4 e ao gerador continuo; o Q de o_todo_fica e qualquer estado, nao o espelho J; a algebra e trivial e o peso esta na leitura",
        "proximo_passo": "nome do operador; decisao de versao", "refs": ["kernel.k_operador_igual_candidata_02nov"], "artefatos": [str(C2), str(S2), str(H3)]},
       {"tipo": "ROTA", "rota_id": "hubble.k_como_transposicao_inteira_ffat_02nov", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "PROPOSTA", "estatuto": "OPEN",
        "titulo": "K como transposicao inteira: a simetria de escala FFAT deixa a regua sem ver K; helio e deuterio cobram",
        "pergunta": "A regua calculada precisa mudar 7,73% ou K e uma transposicao que ela nao ouve?",
        "dados": ["Cyr-Racine, Ge & Knox, arXiv:2107.13000", "Ge, Cyr-Racine & Knox, arXiv:2210.16335", "Ivanov, Ali-Haimoud & Lesgourgues, arXiv:2005.10656"],
        "metodo": "leitura dos resumos e do texto no corpus; conta so da Eq. 16 com K = lambda; nenhum ajuste, nenhum dado novo, nenhum CMB rodado", "olhou_dados": False,
        "resultado": "Com lambda = K = %.4f: densidade +%.1f%% do visivel; pela Eq. 16, Y_P exigido %.3f contra 0,2453 +- 0,0034 (%.1f sigma). T0 sozinho nao resolve: Planck+BAO volta ao FIRAS." % (K, 100 * (K * K - 1), yr, ds),
        "veredito": "PROPOSTA__NAO_EXAMINADA__A_PORTA_EXISTE_NA_LITERATURA__HELIO_E_DEUTERIO_COBRAM__DEPENDE_DE_O_ESPELHO_PESAR",
        "defeito": "Na literatura o espelho tem energia real; o operador ratificou perda de coerencia, nao de energia. A rota pelo helio esta morta de saida; falta outro mecanismo para o espalhamento. K nao e uniforme: cresce com o registro. A sessao de 08/08 anotou que a TGL nao escala rho_Lambda, o que a tiraria da simetria no setor tardio. Citado em 08/08 so para o canal N_eff, nunca como porta para K.",
        "proximo_passo": "resposta do operador: o que foi ao espelho pesa? Antes de qualquer conta contra helio e deuterio, ler a partitura", "refs": ["hubble.k_sem_portador_fisico_02nov", "kernel.o_igual_restaurado_candidata_02nov"], "artefatos": [str(CONTAS)]},
       {"tipo": "ANOTACAO", "rota_id": "hubble.k_sem_portador_fisico_02nov", "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "O que vazou vai ao espelho, no acervo; as seis moradas nao esgotam: falta a transposicao inteira",
        "resultado": "H3c de 22/06: Leak+ = Mirror-; condicional, fora do kernel e do Atlas. A morada H primordial mudou uma nota so; FFAT muda o acorde inteiro e nao foi examinada: rota hubble.k_como_transposicao_inteira_ffat_02nov.",
        "estatuto": "CONJECTURE", "artefatos": [str(H3), str(CONTAS)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_igual_r2_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-300:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-operador-igual-r2", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "candidata_o_igual_errata_02nov", "kind": "fact", "statute": "REAL", "text": "Ao lado de candidata_o_igual_02nov: 13 teoremas, nao 12; K_pos auditado em copia; o_fundo_e_a_media rearranja a definicao H0local, nao e mecanismo.", "sources": [SRC(S1K)]},
                                {"id": "candidata_o_igual_restaurado_02nov", "kind": "fact", "statute": "REAL", "text": "Segunda candidata no sandbox: 6 teoremas, trio, 0 sorry: o igual quebra no peso bruto, volta ao dividir pelo traco, e o divisor e o da lei de K. Fora do kernel selado; P modo proprio e hipotese; nao prova o H3c.", "sources": [SRC(C2)]},
                                {"id": "acervo_h3c_espelho_02nov", "kind": "fact", "statute": "CONJECTURE", "text": "Acervo de 22/06: T(P)/Tr T(P) = P; Leak+ = Mirror-; condicional, fora do kernel e do Atlas. Substitui a pergunta residuo_setor_7p7_02nov.", "sources": [SRC(H3)]},
                                {"id": "porta_ffat_02nov", "kind": "pending", "statute": "OPEN", "text": "Porta nao examinada: K como transposicao inteira (simetria FFAT). Com K, helio pela Eq. 16 exigiria %.3f contra 0,2453 (%.1f sigma); falta outro mecanismo. Depende de o espelho pesar." % (yr, ds), "sources": [SRC(CONTAS)]},
                                {"id": "pergunta_espelho_pesa_02nov", "kind": "pending", "statute": "OPEN", "text": "Pergunta posta ao operador nas quatro linguas: o que foi ao espelho ainda pesa?", "sources": [SRC(ORD)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:240], (d.get("result") or {}).get("revision"))
assert d.get("ok")


def anexar(p, texto):
    p = Path(p)
    b = p.read_bytes()
    nl = "\r\n" if b"\r\n" in b else "\n"
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    nb = b.rstrip() + (nl + texto.replace("\n", nl)).encode("utf-8")
    with open(tmp, "xb") as f:
        f.write(nb)
    assert tmp.stat().st_size == len(nb) and len(nb) > len(b)
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))


anexar(M / "vazar-e-luzir-02nov.md", f"""
## Ao lado (02/11/2026, gerência c1, em nome próprio; o número corrige a frase)

**Correções ao bloco acima.** (1) São **13** teoremas, não 12: `K_pos` compilou sem `#print axioms` na saída e foi auditado em cópia, trio; a candidata não mudou (sha16 `{f1}`). (2) O verbatim exato é o do arquivo: «gráviton ( que antes eu disse ser o operador “=“, aquele que criva)»; o bloco acima normalizou espaço e aspas. (3) `o_fundo_e_a_media` é a definição `H0local` rearranjada com um zero escrito por mim; a definição é cunhagem dele («o fundo atribui o registro inteiro à expansão»). Não é mecanismo. (4) O «resíduo» acima estava mal posto: o acervo já dizia para onde vai o que vaza.

**O acervo já tinha.** `TGL_H3C_BETA_PAID_ATTENTION_THEOREM.md` (22/06/2026, sha16 `{fh}`, voz não conferida): T(P)/Tr T(P) = P; «A atenção conserva identidade, não peso bruto»; Leak₊ = Mirror₋; «a profundidade do retorno é a deformação do espaço» [CONJECTURE]. Condicional a H1–H4 e ao gerador contínuo; fora do kernel (0 arquivos com attention ou invariância projetiva) e do Atlas. `FECHAMENTO_MATRIZ_S_CORE_II.md`: «1_abs = gráviton = I» [CONJ]. `GravitonPolarization.lean`: gráviton fundamental = I (spin 0, custo zero); observável = δI_modular (±2). `GravitonReading.lean` (18/07): «a estrutura que lê a fonte é o gráviton», na segunda derivada.

**Segunda candidata [REAL no sandbox]:** `work{BK}rota_RE_dualidade_02nov{BK}OIgualRestauradoCandidata.lean` (sha16 `{f2}`), 6 teoremas, trio, 0 sorry: o «=» quebra no peso bruto, volta ao dividir pelo traço, e o divisor é o da lei de K. Fora do kernel selado; P modo próprio é hipótese; não prova o H3c.

**Leitura da gerência [ONTO, a ratificar]:** K é o marco, não o gráviton. É número, logo fica no modo-traço (spin 0), nunca na onda ±2; no todo K = 1 («custo zero», `escalar_entre_normalizados_e_um`); do setor, K = 1/peso. O integrando g lê a fonte (Raychaudhuri, ρ+p).

**Porta não examinada:** `hubble.k_como_transposicao_inteira_ffat_02nov`: a simetria de escala (arXiv:2107.13000, 2210.16335) deixa a régua sem ouvir a transposição do acorde inteiro. A morada «H primordial» mudou uma nota só. Com K: densidade {f2d}% do total; hélio pela Eq. 16 exigiria {yr} contra 0,2453 ± 0,0034 ({ds}σ): essa via morre de saída. Lá o espelho tem energia; aqui ele ratificou coerência.

**Pergunta posta a ele:** o que foi ao espelho ainda pesa? Não dizer «K é o gráviton» sem a ressalva do marco. [[rota-re-k-e-landauer-02nov]] [[pergunta-nas-quatro-linguas]]
""")

anexar(NOTA, f"""
## Ao lado, r2 (02/11/2026, gerência c1)

A contagem acima não esgota as moradas: a linha «H primordial» mudou uma nota só. A transposição do acorde inteiro (taxas de queda e de espalhamento juntas; Cyr-Racine, Ge & Knox, arXiv:2107.13000; Ge, Cyr-Racine & Knox, arXiv:2210.16335) deixa as observáveis adimensionais quase invariantes e não foi examinada aqui. Com λ = K, pela Eq. 16, o hélio teria de ser {yr} contra 0,2453 ± 0,0034 ({ds}σ); a via do hélio morre de saída e falta outro mecanismo para o espalhamento. T₀ sozinho não resolve: Planck + BAO volta ao FIRAS (Ivanov et al., arXiv:2005.10656). O vazamento vai ao espelho no H3c de 22/06 (sha16 `{fh}`), condicional. Contas: `CONTAS_TRANSPOSICAO.json`. Rota: `hubble.k_como_transposicao_inteira_ffat_02nov`, PROPOSTA.
""")

AO = ("⧗ *Ao lado (02/11/2026, fala do operador, verbatim sha16 `%s`; leitura da gerência [ONTO, a ratificar]):* K faz a função do gráviton-«=»: é o fator que faz o «=» valer depois do custo (T(P)/Tr T(P) = P). K é número, logo fica no modo-traço, nunca na onda ±2: é o **marco** do gesto, não o gráviton em si; no todo K = 1. Em aberto: se o que foi ao espelho ainda pesa. <!-- k_e_o_marco_02nov -->" % fo)
REG = ("\n### 02/11/2026 — K é o marco do «=»; errata e a porta da transposição inteira <!-- k_e_o_marco_reg_02nov -->\n\n"
       "**Errata ao registro anterior:** 13 teoremas, não 12; `o_fundo_e_a_media` rearranja a definição `H0local`. **[REAL no sandbox]** segunda candidata sha16 `%s`, 6 teoremas, trio, 0 sorry, fora do kernel selado: o «=» quebra no peso bruto, volta ao dividir pelo traço, e o divisor é o da lei de K. **[CONJECTURE]** acervo de 22/06 (H3c β-pago, sha16 `%s`): o vazamento vai ao espelho; condicional, fora do kernel. **[OPEN]** rota `hubble.k_como_transposicao_inteira_ffat_02nov`, PROPOSTA: a simetria de escala [KNOWN] deixa a régua sem ouvir a transposição; o hélio pela Eq. 16 exigiria %s contra 0,2453 ± 0,0034 (%sσ).\n" % (f2, fh, yr, ds))
A = CEN / "memory/TGL_ATLAS.md"
ba = A.read_bytes()
t = ba.decode("utf-8")
assert "k_e_o_marco_02nov" not in t
nl = "\r\n" if "\r\n" in t else "\n"
ls = t.split(nl)
i = [k for k, x in enumerate(ls) if x.startswith("**Gráviton = operador de retorno da fase (forma canônica de 21/08/2026)**")]
assert len(i) == 1, i
ls.insert(i[0], AO)
nt = nl.join(ls).rstrip() + nl + REG.replace("\n", nl)
bak = A.with_name(A.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(ba)
assert bak.read_bytes() == ba
tmp = A.with_name(A.name + ".tmp_" + TS)
nb = nt.encode("utf-8")
with open(tmp, "xb") as f:
    f.write(nb)
assert tmp.stat().st_size == len(nb) > len(ba)
os.replace(tmp, A)
print("atlas", len(ba), "->", len(nb))
vv = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", vv.returncode, vv.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])
