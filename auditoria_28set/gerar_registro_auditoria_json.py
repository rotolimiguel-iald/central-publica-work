# -*- coding: utf-8 -*-
"""Gera AUDITORIA_28SET_REGISTRO.json — o REGISTRO da auditoria dos testes passados (28/09/2026) que o um.py v376 lê POR HASH
(prove_audit_28set_v376): achados por família com o veredicto do verificador adversarial e a severidade revista, os achados novos, o crítico
de completude, as erratas da gerência (em nome próprio) e os hashes do relatório e do anexo, lidos do disco. Fonte: o diário do workflow
wf_58da7663-e79 (a mesma leitura de gerar_anexo_achados.py). Nada transcrito à mão. Grava no work/ e copia para <cache>/auditoria/ (o
cache do rito), com tmp -> conferir -> replace."""
import hashlib
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
J = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\subagents\workflows\wf_58da7663-e79\journal.jsonl"
AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
ORDEM = ["gate_vazios", "d1_fundo", "gw_eco", "ringdown", "relogios_neutrinos_coma", "estatistica_veredito", "consistencia_teorica"]
SEV = ["CRITICO", "ALTO", "MEDIO", "BAIXO", "INFO"]
sha = lambda b: hashlib.sha256(b).hexdigest()
aud, ver, crit = {}, {}, None
jb = open(J, "rb").read()
for l in jb.decode("utf-8", "replace").splitlines():
    try:
        e = json.loads(l)
    except Exception:
        continue
    if e.get("type") != "result":
        continue
    r = e.get("result") or e.get("value") or e.get("output")
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except Exception:
            continue
    if not isinstance(r, dict):
        continue
    if "veredictos" in r:
        ver[r["familia"].split(" ")[0]] = r
    elif "achados" in r:
        aud[r["familia"]] = r
    elif "sem_auditoria" in r:
        crit = r
assert crit and len(aud) == 7 and len(ver) == 7, (len(aud), len(ver), bool(crit))
achados, novos = [], []
tot = dict(achados=0, sustentados=0, parciais=0, refutados=0, nao_verif=0, sem_verif=0, novos=0)
por_sev = {s: 0 for s in SEV}
for fam in ORDEM:
    a, v = aud[fam], ver[fam]
    vv = {x["id"]: x for x in v["veredictos"]}
    for x in a["achados"]:
        w = vv.get(x["id"])
        vered = w["veredicto"] if w else "SEM_VERIFICACAO"
        sev = w["severidade_revista"] if w else x["severidade"]
        tot["achados"] += 1
        tot[{"SUSTENTADO": "sustentados", "PARCIAL": "parciais", "REFUTADO": "refutados", "NAO_VERIFICAVEL": "nao_verif"}.get(vered, "sem_verif")] += 1
        if vered in ("SUSTENTADO", "PARCIAL"):
            por_sev[sev] += 1
        achados.append(dict(id=x["id"], familia=fam, severidade_original=x["severidade"], severidade_revista=sev, classe=x["classe"],
                            veredicto_verificador=vered, titulo=x["titulo"], rota_id=x["rota_id"],
                            correcao_proposta=x["correcao_proposta"].replace("\n", " ")[:600],
                            razao_verificador=(w["razao"].replace("\n", " ")[:600] if w else None)))
    for x in v.get("achados_novos") or []:
        tot["novos"] += 1
        por_sev[x["severidade"]] += 1
        novos.append(dict(id=x["id"], familia=fam, severidade=x["severidade"], classe=x["classe"], titulo=x["titulo"],
                          correcao_proposta=x["correcao_proposta"].replace("\n", " ")[:600]))
rel = os.path.join(AQUI, "RELATORIO_AUDITORIA_E_INVESTIGACAO_20260928.md")
anx = os.path.join(AQUI, "ANEXO_ACHADOS.md")
rb, ab = open(rel, "rb").read(), open(anx, "rb").read()
# as erratas da gerência de 28/09, em nome próprio (lei da assinatura da errata): o que a própria gerência afirmou e o número corrigiu
ERRATAS_GERENCIA = [
    dict(id="G-01", data="2026-09-28", frase="«a QG fechada não usa β / β é de outro setor»",
         correcao="β é o FUNDAMENTO, derivado (ω(I)=1 → ½ nat → √e → β = α·√e); a implicação da QG é provada sem tomar β como hipótese e β entra a jusante, "
                  "no código derivado (ordem do operador, 28/09, verbatim no registro)"),
    dict(id="G-02", data="2026-09-28", frase="DR2 «TENSAO_FORTE» e «o CMB limita β» como fatos",
         correcao="condicionais ao mapa de Ω_m em R (Ω_m^ν | (1+β)Ω_m), escolha de modelo [INPUT] não derivada; com Ω_m efetivo a tensão cai"),
    dict(id="G-03", data="2026-09-28", frase="«a covariância do Pantheon+ não está em disco»", correcao="está: pantheon_covariance.dat, 1701×1701, sha256 lida por script (fontes.py)"),
    dict(id="G-04", data="2026-09-28", frase="«0,26σ» na investigação P1/P2", correcao="0,26σ é P2; P1 dá 0,23σ — dito lado a lado"),
    dict(id="G-05", data="2026-09-28", frase="rota Fisher V9 criada em duplicata no mapa", correcao="marcada SUPERADA; a rota original vale"),
]
reg = dict(
    protocolo="AUDITORIA_TESTES_PASSADOS_28SET_2026", gerado_em=time.strftime("%Y-%m-%d %H:%M:%S"),
    ordem_do_operador_28set=("agora que fechamos toda a formulação da gravidade quantica é possível que tenhamos feito algum teste passado no um.py de "
                             "maneira errada, precisamos investigar […] usasse a bancada para fazer uma investigação autonoma […] autorizo vc a usar as "
                             "outras IA's […] quero um relatório no final"),
    fonte_journal=dict(caminho=J, sha256=sha(jb), bytes=len(jb)),
    relatorio=dict(caminho=rel, sha256=sha(rb), bytes=len(rb)), anexo=dict(caminho=anx, sha256=sha(ab), bytes=len(ab)),
    metodo=("7 famílias × (aferidor + verificador adversarial instruído a refutar) + crítico de completude; consulta ao inventário/selo/kernel antes de "
            "«falta»; artefatos com sha256; registro no MAPA DE ROTAS"),
    contagem=tot, por_severidade_revista=por_sev, familias=ORDEM,
    nota_por_severidade="por_severidade_revista conta os SUSTENTADOS + PARCIAIS (severidade revista) + os NOVOS dos verificadores; o(s) REFUTADO(s) nao entram -- por isso a soma e achados - refutados + novos (aferidor B2, 28/09)",
    achados=achados, achados_novos=novos,
    critico=dict(resumo=crit["resumo"].replace("\n", " ")[:2000], sem_auditoria=crit["sem_auditoria"], perguntas_sem_resposta=crit["perguntas_sem_resposta"],
                 contradicoes=crit["contradicoes"], recomendacoes=crit["recomendacoes"]),
    erratas_da_gerencia=ERRATAS_GERENCIA,
    o_que_nao_e=["nenhum número selado errado por aritmética; os erros são de entrada, desenho, estatística e leitura",
                 "NOT_FALSIFIED nunca é CONFIRMED; nada aqui confirma a TGL nem a refuta; o gate não se move por auditoria"],
)
b = json.dumps(reg, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
for dest in (os.path.join(AQUI, "AUDITORIA_28SET_REGISTRO.json"), os.path.join(CACHE, "auditoria", "AUDITORIA_28SET_REGISTRO.json")):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        bak = dest + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
        open(bak, "wb").write(open(dest, "rb").read())
    open(dest + ".tmp", "wb").write(b)
    assert open(dest + ".tmp", "rb").read() == b
    os.replace(dest + ".tmp", dest)
    print("ok", dest, len(b), sha(b)[:16])
# o C6 do ringdown (GW250114) entra no cache do rito byte a byte (o um.py v376 o lê por hash)
src = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C6_RESULTS.json"
cb = open(src, "rb").read()
dest = os.path.join(CACHE, "gw", "C6_RESULTS_GW250114.json")
if not (os.path.exists(dest) and open(dest, "rb").read() == cb):
    open(dest + ".tmp", "wb").write(cb)
    assert open(dest + ".tmp", "rb").read() == cb
    os.replace(dest + ".tmp", dest)
print("ok", dest, len(cb), sha(cb)[:16], "(byte a byte de", src + ")")
print(json.dumps(dict(tot, por_sev=por_sev), ensure_ascii=False))
