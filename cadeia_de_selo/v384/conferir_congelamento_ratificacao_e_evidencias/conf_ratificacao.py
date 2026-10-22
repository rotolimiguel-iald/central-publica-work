# -*- coding: utf-8 -*-
# Conferencia independente da RATIFICACAO do V1 (lente ratificacao_e_evidencias). Somente leitura fora desta pasta.
import json, hashlib, os, re, sys
V1P = r"C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out\PREREGISTRO_PILAR_QUANTICO_20261003_V1.json"
TRANS_CANON = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
RASC = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\rascunho_prereg_v13\PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"
RASC_MD = RASC[:-5] + ".md"
RASC_RED = RASC.replace("B_AMPLIADO_D64", "B_REDUZIDO")
REG = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384\registro_rascunhos_apresentados_v384.json"
HERE = os.path.dirname(os.path.abspath(__file__))


def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def specsha(spec):
    return hashlib.sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


out = {}
V1 = json.load(open(V1P, encoding="utf-8"))
R = V1["ratificacao_do_operador"]
VERB = R["verbatim"]
out["v1_sha256"] = fsha(V1P)
out["verbatim"] = VERB
out["verbatim_len"] = len(VERB)
out["verbatim_eq_strip"] = (VERB == VERB.strip())

# --- 1) o transcrito, BRUTO, linha a linha
size_now = os.path.getsize(TRANS_CANON)
out["transcrito_tamanho_agora"] = size_now
hits_user = []
sub_hits = []
KEYS = [b"uma hora a mais", b"irris", b"vamos assim"]
off = 0
nline = 0
with open(TRANS_CANON, "rb") as f:
    for raw in f:
        nline += 1
        start = off
        off += len(raw)
        if not (b"uma hora a mais" in raw and b"vamos assim" in raw):
            continue
        try:
            d = json.loads(raw.decode("utf-8"))
        except Exception as e:
            sub_hits.append({"linha": nline, "erro_json": str(e)})
            continue
        ty = d.get("type")
        rec = {"linha": nline, "offset_inicio": start, "offset_fim": off, "type": ty, "timestamp": d.get("timestamp"),
               "isSidechain": d.get("isSidechain"), "isMeta": d.get("isMeta"), "userType": d.get("userType"),
               "uuid": d.get("uuid"), "parentUuid": d.get("parentUuid"), "tem_toolUseResult": "toolUseResult" in d}
        texts = []
        if ty == "user":
            m = d.get("message", {}) or {}
            rec["role"] = m.get("role")
            c = m.get("content")
            rec["content_tipo"] = type(c).__name__
            if isinstance(c, str):
                texts = [c]
            else:
                rec["blocos"] = [x.get("type") for x in (c or []) if isinstance(x, dict)]
                texts = [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif ty == "queue-operation":
            rec["operation"] = d.get("operation")
            if isinstance(d.get("content"), str):
                texts = [d["content"]]
        elif ty == "attachment":
            rec["attachment_type"] = (d.get("attachment") or {}).get("type")
        rec["n_textos"] = len(texts)
        rec["texto_igual_ao_verbatim_apos_strip"] = any(t.strip() == VERB for t in texts)
        rec["texto_igual_sem_strip"] = any(t == VERB for t in texts)
        rec["sha256_linha_sem_fim"] = hashlib.sha256(raw.rstrip(b"\r\n")).hexdigest()
        rec["fim_de_linha"] = repr(raw[len(raw.rstrip(b"\r\n")):])
        sub_hits.append(rec)
        if ty == "user" and rec["texto_igual_ao_verbatim_apos_strip"]:
            hits_user.append(rec)
out["linhas_no_transcrito_agora"] = nline
out["ocorrencias_do_trecho"] = sub_hits
out["mensagens_user_iguais_ao_verbatim"] = hits_user

# --- 2) os campos da ratificacao
rg = R["rascunho_apresentado"]
chk = {}
chk["escolha"] = R["escolha"]
chk["escolha_eq_B_AMPLIADO_D64"] = R["escolha"] == "B_AMPLIADO_D64"
chk["quantas_user_iguais"] = len(hits_user)
if hits_user:
    h = hits_user[0]
    chk["timestamp_da_mensagem_user"] = h["timestamp"]
    chk["quando_eq_timestamp_da_mensagem"] = (R["quando"] == h["timestamp"])
    chk["sha_linhas_user"] = [x["sha256_linha_sem_fim"] for x in hits_user]
    chk["sha_linha_eq_gravado"] = ([x["sha256_linha_sem_fim"] for x in hits_user] == R["transcrito"]["sha256_das_linhas_da_mensagem"])
    chk["mensagem_termina_antes_do_tamanho_na_leitura"] = h["offset_fim"] <= R["transcrito"]["tamanho_do_transcrito_na_leitura_bytes"]
chk["linhas_da_mensagem_gravado"] = R["transcrito"]["linhas_da_mensagem"]
chk["sha_gravado"] = R["transcrito"]["sha256_das_linhas_da_mensagem"]
chk["quando"] = R["quando"]
chk["rascunho_gerado_utc_gravado"] = rg["gerado_utc"]
chk["quando_posterior_ao_rascunho"] = R["quando"] > rg["gerado_utc"]
nrm = re.sub(r"[\s_\-\u2010\u2011\u2012\u2013]+", " ", VERB.lower())
chk["normalizado"] = nrm
chk["nomeia_b_ampliado"] = bool(re.search(r"\bb ampliado\b", nrm))
chk["nomeia_b_reduzido"] = bool(re.search(r"\bb reduzido\b", nrm))
chk["contem_reduzid_solto"] = "reduzid" in nrm
chk["nao_imediatamente_antes_de_verbo"] = bool(re.search(r"\bn[a\u00e3]o\s+(ratifico|concordo|aprovo|autorizo)\b", VERB.lower()))
chk["nao_antes_de_qualquer_flexao"] = bool(re.search(r"\bn[a\u00e3]o\s+(ratific|concord|aprov|autoriz)\w*", VERB.lower()))
chk["verbos_de_ratificacao_presentes"] = re.findall(r"\b(ratific\w*|concord\w*|aprov\w*|autoriz\w*)", VERB.lower())
chk["todas_as_negacoes"] = [m.group(0) for m in re.finditer(r"\bn[a\u00e3]o\s+\w+", VERB.lower())]
chk["de_teste"] = R["transcrito"]["de_teste"]
chk["caminho"] = R["transcrito"]["caminho"]
chk["caminho_eq_canonico"] = os.path.normcase(os.path.abspath(R["transcrito"]["caminho"])) == os.path.normcase(TRANS_CANON)
chk["tamanho_na_leitura"] = R["transcrito"]["tamanho_do_transcrito_na_leitura_bytes"]

# --- 3) spec
chk["spec_sha256_recalculado_do_V1"] = specsha(V1["spec"])
chk["spec_sha256_gravado"] = V1["spec_sha256"]
chk["spec_sha256_ratificada"] = R["spec_sha256_ratificada"]
chk["spec_sha256_do_rascunho_apresentado"] = R["spec_sha256_do_rascunho_apresentado"]
RJ = json.load(open(RASC, encoding="utf-8"))
chk["rascunho_spec_sha256_gravado_nele"] = RJ.get("spec_sha256")
chk["rascunho_spec_sha256_recalculado"] = specsha(RJ["spec"])
chk["rascunho_gerado_utc_no_arquivo"] = RJ.get("gerado_utc")
chk["rascunho_gerado_utc_no_arquivo_eq_gravado"] = RJ.get("gerado_utc") == rg["gerado_utc"]
chk["rascunho_escolha_no_arquivo"] = (RJ.get("desvio_do_plano_B") or {}).get("esta_especificacao", {}).get("escolha")
chk["rascunho_file_sha256_agora"] = fsha(RASC)
chk["rascunho_file_sha256_gravado"] = rg["sha256"]
chk["rascunho_file_sha_eq"] = chk["rascunho_file_sha256_agora"] == rg["sha256"]
chk["rascunho_arquivo_gravado"] = rg["arquivo"]
chk["rascunho_md_sha256_agora"] = fsha(RASC_MD)
chk["rascunho_reduzido_spec_sha256"] = specsha(json.load(open(RASC_RED, encoding="utf-8"))["spec"])
chk["a_especificacao_ratificada_e_a_do_rascunho"] = R["a_especificacao_ratificada_e_a_do_rascunho"]
chk["todos_os_spec_iguais"] = len({chk["spec_sha256_recalculado_do_V1"], chk["spec_sha256_gravado"], chk["spec_sha256_ratificada"],
                                   chk["spec_sha256_do_rascunho_apresentado"], chk["rascunho_spec_sha256_gravado_nele"], chk["rascunho_spec_sha256_recalculado"]}) == 1
try:
    REGJ = json.load(open(REG, encoding="utf-8"))
    s = json.dumps(REGJ, ensure_ascii=False)
    chk["registro_sha256"] = fsha(REG)
    chk["registro_cita_sha_do_rascunho"] = rg["sha256"] in s
    chk["registro_cita_spec_sha"] = R["spec_sha256_ratificada"] in s
    chk["registro_cita_md_sha"] = chk["rascunho_md_sha256_agora"] in s
    out["registro_rascunhos"] = REGJ
except Exception as e:
    chk["registro_erro"] = repr(e)
out["conferencias"] = chk
with open(os.path.join(HERE, "resultado_ratificacao.json"), "w", encoding="utf-8") as fo:
    json.dump(out, fo, ensure_ascii=False, indent=1)
print(json.dumps(out["conferencias"], ensure_ascii=False, indent=1))
print("OCORRENCIAS:", json.dumps(sub_hits, ensure_ascii=False, indent=1))
print("transcrito agora:", size_now, "bytes,", nline, "linhas")
