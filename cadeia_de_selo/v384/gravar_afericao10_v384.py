# -*- coding: utf-8 -*-
"""Registro da 10a afericao (estreita; gerencia, em nome proprio; so acrescimo): VERBATIM por entrada, com as disposicoes. AO LADO (10N3): os scripts da
memoria (memoria_bloco10_v384.py, memoria_errata_bloco10_v384.py) e os rascunhos v10 (intermediario) e v11 com os sha256 -- nenhum registro os nomeava.
Backup de BYTES conferido; temporario -> tamanho -> substituir -> conferir."""
import glob, hashlib, json, os, re, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A10P = os.path.join(HERE, "afericao10_resultado.json"); A10 = json.load(open(A10P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A10["grupos"] for a in (g.get("itens") or [])]
NOV = A10["novos"]; V10 = {v["i"]: v for v in (A10.get("verificacao") or {}).get("veredictos", [])}
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")


def gravar(p, novo, conferir_prefixo=None):
    raw = open(p, "rb").read()
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw, "backup nao confere"
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo), "temporario com tamanho errado"
    os.replace(p + ".tmp", p); assert open(p, "rb").read() == novo, "o gravado nao confere"
    if conferir_prefixo is not None:
        assert novo[:len(conferir_prefixo)] == conferir_prefixo


F = {k: os.path.join(HERE, k) for k in ("salvar_afericao10.py", "aplicar_afer10_lancador_ensaio.py", "aplicar_afer10_gerador_prereg.py", "gravar_afericao10_v384.py")}
F["gerador_do_pre_registro"] = GEN
AO_LADO = {os.path.relpath(p, HERE).replace(os.sep, "/"): h(p) for p in
           [os.path.join(HERE, "memoria_bloco10_v384.py"), os.path.join(HERE, "memoria_errata_bloco10_v384.py")]
           + sorted(glob.glob(os.path.join(HERE, "rascunho_prereg_v10", "*"))) + sorted(glob.glob(os.path.join(HERE, "rascunho_prereg_v11", "*")))}
ACAO_IT = {"9N14": "= 10N4 (os sinais giram ANTES do log real: toda recusa 17 dos giros acontece com o log real ainda no lugar, e o registro dela fica no .fase0)."}
ACAO_NOV = {
    0: "o escopo (em d = 64) vem ANTES dos numeros na nota antiga; o «d = 8 a 64» do cabecalho do paragrafo no MD e' gerado dos d das sondas.",
    1: ("o texto do lancador: o PID sai em qualquer saida antecipada e, armada a restauracao, so no FIM dela; o escopo do registro de uma tentativa recusada "
        "(depois da fase 0: no .fase0; as recusas 6 a 9 e 16, e a 17 da guarda do proprio .fase0, so na saida do lancador); o .fase0 de tentativas anteriores "
        "ACRESCENTADO ao .fase0.anterior (10N5)."),
    2: "o ensaio a seco RECUSA rodar com -O/PYTHONOPTIMIZE; rodado com -O: recusou.",
    3: ("registrados AO LADO (passada9.registros_ao_lado_na_10a): o memoria_bloco10_v384.py e o memoria_errata_bloco10_v384.py e os arquivos do "
        "rascunho_prereg_v10 (intermediario) e do rascunho_prereg_v11, com os sha256; os rascunhos desta rodada (v12) entram em passada10."),
    4: "os sinais giram ANTES do log real: toda recusa 17 dos giros acontece com o log real ainda no lugar, e o registro dela fica no .fase0.",
    5: ("o .fase0 de tentativas anteriores e' ACRESCENTADO ao .fase0.anterior com separador datado, nunca sobrescrito (testado com tres tentativas seguidas: "
        "as tres preservadas)."),
    6: "= 2.",
    7: "= 1.",
}
c10 = Counter(a["estado"] for _, a in ENT)
falta = sorted({a["id"] for _, a in ENT if a["estado"] != "RESOLVIDO"} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dupc = lambda d: sum(1 for v in d.values() if re.search(r"(^|: )= ", str(v)))
sev10 = Counter(v["severidade_ajustada"] for v in V10.values() if not v["refutado"])
sob10 = sum(1 for i in range(len(NOV)) if not (V10.get(i) or {}).get("refutado"))
toca = sum(1 for i in range(len(NOV)) if (V10.get(i) or {}).get("toca_rascunho"))
L = ["\n" + "=" * 80, "10a PASSADA (estreita) -- as correcoes da 9a (VERBATIM de afericao10_resultado.json, sha256 %s; POR ENTRADA) e DISPOSICOES (%s)" % (h(A10P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["estado"] != "RESOLVIDO":
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    v = V10.get(i) or {}
    L.append("\n[10N%d] (%s/%s -> %s, severidade ajustada %s, toca o rascunho: %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE",
                                                                                       v.get("severidade_ajustada"), v.get("toca_rascunho"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nEVIDENCIAS NOVAS DA GERENCIA NESTA RODADA (sha256): " + "; ".join("%s %s" % (k, h(p)[:16]) for k, p in F.items()))
L.append("\nREGISTRADOS AO LADO (10N3; sha256): " + "; ".join("%s %s" % (k, v[:16]) for k, v in AO_LADO.items()))
L.append("\nO QUE CADA LENTE EXAMINOU (10a passada, verbatim):")
for g in A10["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
assert b"10a PASSADA (estreita)" not in raw
novo = raw + ("\n".join(L) + "\n").encode("utf-8"); gravar(p, novo, conferir_prefixo=raw); print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
assert "passada10" not in D
t = D["texto_para_o_pre_registro"]; assert "; 10ª passada" not in t
reg = c10.get("REGRESSAO", 0)
t += ("; 10ª passada (estreita, as correções da 9ª): %d entradas — %d resolvidas e %d regressão (a recusa 17 do giro dos sinais vinha depois do giro do log "
      "real; corrigida: os sinais giram primeiro); %d achados novos, %d sobreviventes à verificação (%d repetem outro achado ou item; severidades: %s; %d tocavam "
      "o texto deste rascunho), tratados no código ou no texto antes deste documento; o caso que a gerência não alcançou (o V1 igual com a pasta de evidências "
      "adulterada) foi refeito pela aferição com relógio fixo: recusa sem mover nada") % (
    len(ENT), c10.get("RESOLVIDO", 0), reg, len(NOV), sob10, dupc({str(k): v for k, v in ACAO_NOV.items()}), ", ".join("%s %d" % (k, v) for k, v in sorted(sev10.items())), toca)
assert reg == 1 and c10.get("PARCIAL", 0) == 0, dict(c10)
D["texto_para_o_pre_registro"] = t
D["passada9"]["registros_ao_lado_na_10a"] = AO_LADO
D["passada10"] = {"arquivo": os.path.basename(A10P), "sha256": h(A10P), "entradas": dict(c10), "n_entradas": len(ENT), "novos": len(NOV), "sobreviventes": sob10,
                  "severidades_ajustadas": dict(sev10), "tocam_o_rascunho": toca, "repetem_outro": dupc({str(k): v for k, v in ACAO_NOV.items()}),
                  "criterio_das_repeticoes": "«= x» no comeco da disposicao ou depois de «: » (regex (^|: )= )", "evidencias_novas": {k: h(p_) for k, p_ in F.items()}}
D["disposicoes_10a_itens"] = ACAO_IT; D["disposicoes_10a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); gravar(dp, b)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 10a:", dict(c10), "novos", len(NOV), "sob", sob10, "sev", dict(sev10), "toca", toca, "| repeticoes", D["passada10"]["repetem_outro"])
print(t[-700:])
