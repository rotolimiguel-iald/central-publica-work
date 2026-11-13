# -*- coding: utf-8 -*-
"""A medida do README da v411 com o handoff da frente pós-rito (12/11/2026, claude-site-custodia; pedido da gerência c1).

Nada aqui escreve no espelho, no Nós nem na Central: o handoff vai para uma pasta temporária com o NOME real (HANDOFF_v411_CUSTODIA.md),
com os sufixos _v411 dos marcadores trocados pelo da versão do selo em disco (o primordial lê os marcadores pela versão do selo); o registro
offline é injetado no core CARREGADO em memória. Os campos do selo saem da v410 selada (largura fixa: pin, timestamp, contagens).
Confere, como a G1 confere na custódia: primordial.montar (forma, F67, números, cabeça, acervo), o portão e a regra do 4,44 do --gerar,
o portão dos segmentos gerados, a regra do 4,44 da página, a F67 da página (só blocos novos), a NOTA_EN (F67, números, acervo, portão), e
que os marcadores do handoff são os mesmos textos do TESTE_BLOCOS.
Uso: python -X utf8 medir_readme_v411.py <HANDOFF_v411_CUSTODIA.md> <TESTE_BLOCOS_CUSTODIA_v411.json>"""
import hashlib, json, os, re, sys, tempfile
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
# AO LADO (13/11/2026): G1_TESTE_TOOLS aponta uma CÓPIA da G1 (ensaio da errata do registro antes do handoff, com a G1 real congelada)
sys.path.insert(0, os.environ.get("G1_TESTE_TOOLS") or str(CEN / "tools"))
from custodia_g1 import h0dn, primordial as PRIM, readme_pinado as RP, textos  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TPL = TB / "tools" / "readme_pinado" / "readme_template.md"
PARTES = TB / "tools" / "readme_pinado" / "readme_partes"
REGF = CEN / "work" / "cadeia_de_selo" / "v411" / "TESTE_H0DN_OFFLINE_v411_registro.json"
HP, BP = Path(sys.argv[1]), Path(sys.argv[2])
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, detalhe)


hb, bb = HP.read_bytes(), BP.read_bytes()
print("handoff %s %d B sha256 %s" % (HP.name, len(hb), hashlib.sha256(hb).hexdigest()))
print("blocos  %s %d B sha256 %s" % (BP.name, len(bb), hashlib.sha256(bb).hexdigest()))
reg = json.loads(REGF.read_text(encoding="utf-8"))
reg = reg.get("h0dn_bg1_v411", reg)
V = h0dn.valores(reg)
VS = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))["um_version"]
H = hb.decode("utf-8")
BL = json.loads(bb.decode("utf-8"))["textos"]

print("1. os marcadores do handoff = os textos do TESTE_BLOCOS")
rx = re.compile(r"<!-- INICIO_([A-Za-z0-9_]+?)_v411 -->\n?(.*?)\n?<!-- FIM_\1_v411 -->", re.S)
marc = {m.group(1): m.group(2) for m in rx.finditer(H)}
lista = (h0dn.MARCADOR_NOTA,) + h0dn.MARCADORES_README + h0dn.MARCADORES_ESTATUTO
caso("os %d marcadores da G1 estão no handoff" % len(lista), all(k in marc for k in lista), [k for k in lista if k not in marc])
dif = [k for k in lista if k in marc and marc[k].strip("\n") != BL.get(k, "").strip("\n")]
caso("cada um é o mesmo texto do TESTE_BLOCOS", not dif, dif)
caso("nenhum marcador com sufixo da versão do selo em disco (%s) no handoff" % VS, ("_%s -->" % VS) not in H)

print("2. primordial.montar com o registro aberto (as conferências da G1 nos sete README_*)")
T = Path(tempfile.mkdtemp(prefix="h0dn_readme_"))
hp2 = T / "HANDOFF_v411_CUSTODIA.md"
hp2.write_text(re.sub(r"(<!-- (?:INICIO|FIM)_[A-Za-z0-9_]+?)_v411 -->", r"\1_%s -->" % VS, H), encoding="utf-8")
_fonte_orig = PRIM.Construtor.fonte


def _fonte(self, nome, caminho, json_=True, papel=""):
    r = _fonte_orig(self, nome, caminho, json_, papel)
    if nome == "core":
        r["core"]["h0dn_bg1_v411"] = reg
    return r


PRIM.Construtor.fonte = _fonte
try:
    P = PRIM.montar({"handoff": str(hp2)})
    caso("o PRIMORDIAL monta (forma, F67, números, cabeça, acervo)", True)
except Exception as e:  # noqa: BLE001
    caso("o PRIMORDIAL monta (forma, F67, números, cabeça, acervo)", False, str(e)[:600])
    print("\nRESULTADO: %d ok, %d falha(s)" % (RES["ok"], len(RES["falhas"])))
    sys.exit(1)
finally:
    PRIM.Construtor.fonte = _fonte_orig
it = P["itens"]
caso("h0dn.aberto e o registro", it["h0dn.aberto"]["valor"] is True and it["h0dn.registro"]["valor"] == "h0dn_bg1_v411")
pb = PRIM.serializar(P)
C = RP.Ctx(P, pb)
readme_disco = (TB / "README.md").read_text(encoding="utf-8")
texto, segs = RP.renderizar(C, TPL, PARTES, RP.extrair_portas(readme_disco))
b = texto.encode("utf-8")

print("3. a medida")
print("     README da v411 (ensaio): %d bytes; teto %d; folga %d (hoje %d bytes)" % (len(b), RP.TETO, RP.TETO - len(b), len(readme_disco.encode("utf-8"))))
caso("cabe no teto", len(b) <= RP.TETO, len(b))
cab = re.search(r"## What changed in this version[^\n]*\n\n([^\n]*)", texto)
print("     «What changed»: %r" % (cab.group(1)[:220] if cab else None))

print("4. as conferências do --gerar e da página")
conh = RP.conhecidos_de(pb.decode("utf-8"))
reg_txt = RP.registro_fase9_v2(C)
_reg_sha = {RP._regra_fala()[1]} if hasattr(RP, "_regra_fala") else set()   # AO LADO (13/11/2026): o sha16 da regra de 12/11 citado no registro
print("     registro: a frase do autor %s; a citação %s" % ("TRANSCRITA" if "«" in reg_txt else "não transcrita", "presente" if "not transcribed" in reg_txt else "AUSENTE"))
vh = textos.portao(RP._neutraliza(reg_txt), conh | {C.prim_sha16} | _reg_sha, rotulo=RP.REGISTRO_FASE9_V2) + RP.regra_444(reg_txt, C.P)
for id_ in ("painel", "fase9_v2", "primordial_5sigma", "status_5sigma", "paragrafo", "paragrafo_en", "ritos"):
    t_ = C.v("h0dn.readme." + id_)
    vh += textos.portao(RP._neutraliza(t_), conh, rotulo="h0dn.readme." + id_) + RP.regra_444(t_, C.P)
caso("o portão e a regra do 4,44 do --gerar (registro da Fase 9 V2 e os sete textos)", not vh, vh[:4])
vg = [x for t_, nm, ct in segs if t_ == "gerado" for x in textos.portao(RP._neutraliza(ct), conh | {C.prim_sha16}, rotulo=nm)]
caso("o portão dos segmentos gerados", not vg, vg[:4])
caso("a regra do 4,44 da página", not RP.regra_444(texto, P), RP.regra_444(texto, P)[:3])
caso("a linha EN e a frase PT velhas do H0DN saíram", RP.H0DN_LINHA_VELHA_P_IGUAL_NP_EN not in texto and RP.H0DN_FRASE_VELHA_P_IGUAL_NP not in texto)
caso("os dois apontadores estão na página", marc["README_H0DN_EN"].strip("\n") in texto and marc["README_H0DN"].strip("\n") in texto)
f_hoje = {t_ for _, t_ in h0dn.f67(readme_disco)}
f_novo = [x for x in h0dn.f67(texto) if x[1] not in f_hoje]
caso("a F67 da página: nenhum bloco novo sem as obrigações", not f_novo, f_novo[:3])
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
A = h0dn.acervo(core)
nota = marc["NOTA_EN"].strip("\n")
vn = h0dn.conferir_bloco(nota, V, "NOTA_EN", acervo=A) + textos.portao(nota, conh | {x.lower() for x in re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?:[0-9a-f]{48})?(?![0-9a-fA-F])", H)}, rotulo="NOTA_EN")
caso("a NOTA_EN (F67, números, acervo, portão)", not vn, vn[:4])

print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
