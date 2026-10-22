# -*- coding: utf-8 -*-
"""montar_sandbox.py (R3, 13/10/2026) -- monta o sandbox do vinculo em RAIZ CURTA (limite de caminho do Windows, T16), SO dentro de <raiz>,
e <raiz> tem de ser C:/t/vb* (N8: a mesma regra de --saida do esboco R3).
  b1/        COPIA byte a byte da Bancada Um instalada (B2): codigo + fontes relativas conferidos contra canonical_contracts.json, mais o
             proprio manifesto (que pina o Nos REAL). Serve ao ensaio pre_selo com o Nos real v391 e aos controles negativos.
  nos/       COPIA do Nos v391 real (um.py, um_absoluto_selo.json, um_absoluto.json e -- R3, N1 -- tgl_kernel_proof_manifest.json),
             conferida contra o selo.
  b2/        a mesma copia da Bancada, com o manifesto RE-APONTADO para nos/ (so script.path e seal.path mudam; bytes e sha256 iguais).
  nos_v392/  o Nos SINTETICO v392: o um.py v391 com UM_VERSION trocada para "v392" (mesmo comprimento), core copiado e -- R3 -- um
             manifesto do kernel SINTETICO (o v391 com a raiz e o Audit trocados pelos da arvore sintetica e duas pedras sinteticas a
             mais), pinado pelo selo sintetico. O "selo" do sandbox e: copiar nos_v392/* por cima de nos/.
  fx/        fixtures: a arvore sintetica do kernel (fx/kernel_src), os logs sinteticos do build e do Audit, o recibo do kernel
             sintetico VALIDO no contrato KERNEL_RECIBO_R3 (os invalidos sao derivados dele nos controles), o livro de eventos de
             ensaio (copia do real + elos encadeados, inclusive os de N6/N11 e o do decoy de producao).
A producao e o Nos sao SO lidos. Nada e um selo do rito; nenhum kernel e construido; nenhum dado observado.
uso: montar_sandbox.py <raiz curta, ex. C:/t/vb3> [versao sintetica=v392]"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, re, datetime
from pathlib import Path
PROD = Path("C:/IALD/Bancada_Um")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
EVENTOS = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
RAIZ = Path(sys.argv[1]).resolve()
VERSAO_SINTETICA = sys.argv[2] if len(sys.argv) > 2 else "v392"
_rel = Path("C:/t").resolve()
assert RAIZ.parent == _rel and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name), "raiz curta obrigatoria: C:/t/vb* (N8)"
assert not str(RAIZ).lower().startswith(str(PROD).lower()) and not str(RAIZ).lower().startswith(str(NOS).lower())
KERNEL_CONTRATO = "KERNEL_RECIBO_R3"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def impressao_formal(ff):
    return sha(json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def gravar_novo(dst, raw):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.read_bytes() != raw:
            raise SystemExit("DUPLICATA COM BYTES DIFERENTES: " + str(dst))
        return dict(path=str(dst), sha256=sha(raw), bytes=len(raw), duplicata_de_pino=True)
    with open(dst, "xb") as f:
        f.write(raw)
    assert dst.read_bytes() == raw, dst
    return dict(path=str(dst), sha256=sha(raw), bytes=len(raw))


rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3 (13/10/2026)", raiz=str(RAIZ), b1=[], b2=[], nos={}, nos_v392={}, fx={})
for sub in ("b1", "b2", "nos", "nos_v392", "fx"):
    if (RAIZ / sub).exists():
        raise SystemExit("sandbox ja montado: apague antes (so dentro de %s)" % RAIZ)
man_raw = (PROD / "canonical_contracts.json").read_bytes()
man = json.loads(man_raw)
assert Path(man["canonical"]["script"]["path"]) == NOS / "um.py" and Path(man["canonical"]["seal"]["path"]) == NOS / "um_absoluto_selo.json", man["canonical"]
# nos/ = copia do Nos v391 real, conferida contra o selo (R3: com o manifesto do kernel que o selo pina)
um = (NOS / "um.py").read_bytes()
selo_raw = (NOS / "um_absoluto_selo.json").read_bytes()
selo = json.loads(selo_raw)
core = (NOS / "um_absoluto.json").read_bytes()
kman_raw = (NOS / "tgl_kernel_proof_manifest.json").read_bytes()
assert selo["sha256"]["um.py"] == sha(um) and selo["sha256"]["um_absoluto.json"] == sha(core) and selo["um_version"] == "v391"
assert selo["sha256"]["tgl_kernel_proof_manifest.json"] == sha(kman_raw), "o selo v391 nao pina o manifesto do kernel em disco"
assert man["canonical"]["script"]["sha256"] == sha(um) and man["canonical"]["seal"]["sha256"] == sha(selo_raw)
rec["nos"] = dict(um_py=gravar_novo(RAIZ / "nos" / "um.py", um), selo=gravar_novo(RAIZ / "nos" / "um_absoluto_selo.json", selo_raw),
                  core=gravar_novo(RAIZ / "nos" / "um_absoluto.json", core), kernel_manifest=gravar_novo(RAIZ / "nos" / "tgl_kernel_proof_manifest.json", kman_raw))
# b1/ (manifesto original) e b2/ (manifesto re-apontado para nos/)
man2 = json.loads(man_raw)
man2["canonical"]["script"]["path"] = str(RAIZ / "nos" / "um.py")
man2["canonical"]["seal"]["path"] = str(RAIZ / "nos" / "um_absoluto_selo.json")
man2["sandbox_R3"] = "copia de ensaio (13/10/2026): so script.path e seal.path re-apontados para %s; bytes e sha256 identicos ao manifesto B2 %s" % (RAIZ / "nos", sha(man_raw)[:16])
man2_raw = json.dumps(man2, ensure_ascii=False, indent=1).encode("utf-8")
rec["b1"].append(gravar_novo(RAIZ / "b1" / "canonical_contracts.json", man_raw))
rec["b2"].append(gravar_novo(RAIZ / "b2" / "canonical_contracts.json", man2_raw))
for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH na producao: " + e["path"])
    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))
    rec["b2"].append(gravar_novo(RAIZ / "b2" / e["path"], raw))
(RAIZ / "b1" / "estado").mkdir()
(RAIZ / "b2" / "estado").mkdir()

# fx/kernel_src = a arvore SINTETICA do kernel (N1): raiz, Audit e duas pedras; nenhum Lean roda aqui
KS = RAIZ / "fx" / "kernel_src"
arvore = {
    "TGLExt.lean": "-- SINTETICO (sandbox R3 do vinculo, 13/10/2026): raiz do kernel; nenhum kernel e construido aqui\nimport TGLExt.PedraSinteticaA\nimport TGLExt.PedraSinteticaB\n",
    "TGL/Audit.lean": "-- SINTETICO (sandbox R3): o Audit\n#print axioms TGLExt.PedraSinteticaA.um\n#print axioms TGLExt.PedraSinteticaB.dois\n",
    "TGLExt/PedraSinteticaA.lean": "-- SINTETICO (sandbox R3): pedra A\nnamespace TGLExt.PedraSinteticaA\ntheorem um : 1 = 1 := rfl\nend TGLExt.PedraSinteticaA\n",
    "TGLExt/PedraSinteticaB.lean": "-- SINTETICO (sandbox R3): pedra B\nnamespace TGLExt.PedraSinteticaB\ntheorem dois : 2 = 2 := rfl\nend TGLExt.PedraSinteticaB\n",
}
ks_sha = {}
for rel, txt in arvore.items():
    b = txt.encode("utf-8")
    gravar_novo(KS / rel, b)
    ks_sha[rel] = sha(b)
rec["fx"]["kernel_src"] = dict(dir=str(KS), sha256=ks_sha)
# o manifesto do kernel SINTETICO v392: o v391 com a raiz e o Audit trocados e as duas pedras a mais (+ entradas no axiom_report)
kman = json.loads(kman_raw)
ff_v391 = dict(kman["formal_files_sha256"])
kman["formal_files_sha256"] = dict(ff_v391)
for rel, h in ks_sha.items():
    kman["formal_files_sha256"][rel] = h
kman["axiom_report"] = dict(kman["axiom_report"])
kman["axiom_report"]["TGLExt.PedraSinteticaA.um"] = ["propext", "Classical.choice", "Quot.sound"]
kman["axiom_report"]["TGLExt.PedraSinteticaB.dois"] = []
kman["SINTETICO_SANDBOX"] = ("NAO E O MANIFESTO DO RITO: fixture do ensaio do vinculo (R3, 13/10/2026); deriva do manifesto v391 real (%s) trocando "
                             "TGLExt.lean e TGL/Audit.lean pelos da arvore sintetica e acrescentando duas pedras sinteticas" % sha(kman_raw)[:16])
kman_sin = json.dumps(kman, ensure_ascii=False, indent=1).encode("utf-8")
# nos_v392/ = o Nos sintetico
txt = um.decode("utf-8-sig")
mv = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt, re.M)
assert mv and mv.group(1) == "v391", mv
velha = mv.group(0).encode("utf-8")
nova = velha.replace(b"v391", VERSAO_SINTETICA.encode("utf-8"), 1)
assert um.count(velha) == 1
um_sin = um.replace(velha, nova, 1)
assert len(um_sin) == len(um) and um_sin != um
t2 = um_sin.decode("utf-8-sig")
assert re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', t2, re.M).group(1) == VERSAO_SINTETICA
assert len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", t2, re.M)) == len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", txt, re.M)) == 1
assert len(re.findall(r"^UM_VERSION[ \t]*=", t2, re.M)) == 1
selo_sin = dict(selo)
selo_sin["um_version"] = VERSAO_SINTETICA
selo_sin["sha256"] = dict(selo["sha256"])
selo_sin["sha256"]["um.py"] = sha(um_sin)
selo_sin["sha256"]["tgl_kernel_proof_manifest.json"] = sha(kman_sin)
selo_sin["SINTETICO_SANDBOX"] = ("NAO E UM SELO DO RITO: fixture do ensaio do vinculo Bancada-um.py (R3, 13/10/2026); deriva do selo v391 real "
                                 "trocando so um_version, sha256[um.py] e sha256[tgl_kernel_proof_manifest.json]; vive so em %s" % RAIZ)
selo_sin["SINTETICO_SANDBOX_derivado_do_selo_v391_sha256"] = sha(selo_raw)
selo_b = json.dumps(selo_sin, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_v392"] = dict(um_py=gravar_novo(RAIZ / "nos_v392" / "um.py", um_sin), selo=gravar_novo(RAIZ / "nos_v392" / "um_absoluto_selo.json", selo_b),
                       core=gravar_novo(RAIZ / "nos_v392" / "um_absoluto.json", core),
                       kernel_manifest=gravar_novo(RAIZ / "nos_v392" / "tgl_kernel_proof_manifest.json", kman_sin), versao=VERSAO_SINTETICA,
                       um_py_real=dict(sha256=sha(um), bytes=len(um)), bytes_trocados=len(velha), linha_trocada=txt[:mv.start()].count("\n") + 1)
gravar_novo(RAIZ / "nos_v392" / "LEIA-ME_SINTETICO.txt", ("Fixture sintetica (R3, 13/10/2026): um.py v391 real com UM_VERSION trocada para %s na linha %d; selo e "
                                                         "manifesto do kernel derivados; core copiado. NAO e versao selada. So para ensaiar o re-pino da Bancada no sandbox.\n"
                                                         % (VERSAO_SINTETICA, rec["nos_v392"]["linha_trocada"])).encode("utf-8"))
# fx/kernel_logs = os logs sinteticos do build e do Audit (sem sorry, sem erro, axiomas no trio)
KL = RAIZ / "fx" / "kernel_logs"
log_b = ("build_full.log SINTETICO (fixture R3 13/10/2026): nenhum kernel foi construido aqui.\n"
         "Build completed successfully (simulado).\n").encode("utf-8")
log_a = ("audit.log SINTETICO (fixture R3 13/10/2026)\n"
         "'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
         "'TGLExt.PedraSinteticaB.dois' does not depend on any axioms\n").encode("utf-8")
rec["fx"]["log_build"] = gravar_novo(KL / "build_full_SINTETICO.log", log_b)
rec["fx"]["log_audit"] = gravar_novo(KL / "audit_SINTETICO.log", log_a)
# o recibo do kernel sintetico VALIDO, contrato KERNEL_RECIBO_R3 (sem um_py_sha256: a etapa 2 roda antes do candidato)
k_ok = dict(contrato=KERNEL_CONTRATO, versao=VERSAO_SINTETICA, quando_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            rc=0, sorry=0, erros=0,
            build_full_log=dict(path=str(KL / "build_full_SINTETICO.log"), sha256=sha(log_b)),
            audit_log=dict(path=str(KL / "audit_SINTETICO.log"), sha256=sha(log_a)),
            toolchain=dict(lean_version=kman["lean_version"][0], lake_version=kman["lake_version"][0]),
            arvore=str(KS),
            raiz=dict(path="TGLExt.lean", sha256_antes=ff_v391["TGLExt.lean"], sha256_depois=ks_sha["TGLExt.lean"]),
            audit=dict(path="TGL/Audit.lean", sha256_antes=ff_v391["TGL/Audit.lean"], sha256_depois=ks_sha["TGL/Audit.lean"]),
            pedras=[dict(path="TGLExt/PedraSinteticaA.lean", sha256=ks_sha["TGLExt/PedraSinteticaA.lean"]),
                    dict(path="TGLExt/PedraSinteticaB.lean", sha256=ks_sha["TGLExt/PedraSinteticaB.lean"])],
            axiomas=["propext", "Classical.choice", "Quot.sound"],
            criterios=dict(j1_declaracoes=dict(esperado=2, medido=2), j1_teoremas=dict(esperado=2, medido=2), j1_fora_do_trio=dict(esperado=0, medido=0),
                           audit_entradas_antigas_identicas=dict(esperado=0, medido=0), tokens_proibidos=dict(esperado=0, medido=0),
                           r1_ausente=dict(esperado=True, medido=True), declaracoes_novas_no_trio=dict(esperado=True, medido=True)),
            nos_kernel_impressao=dict(definicao="sha256 do JSON canonico (chaves ordenadas, sem espacos, UTF-8) de formal_files_sha256 do Nos",
                                      antes=impressao_formal(ff_v391), depois=impressao_formal(ff_v391)),
            nota="FIXTURE SINTETICA do recibo do build do kernel (etapa 2 da cadeia), contrato KERNEL_RECIBO_R3: nenhum kernel construido aqui; "
                 "os criterios J1/8523 do plano v392 viram 2/2/0/0 nesta arvore de duas pedras")
rec["fx"]["KERNEL_RECIBO_v392_SINTETICO_VALIDO.json"] = gravar_novo(RAIZ / "fx" / "KERNEL_RECIBO_v392_SINTETICO_VALIDO.json",
                                                                   json.dumps(k_ok, ensure_ascii=False, indent=1).encode("utf-8"))
rec["fx"]["kernel_v391"] = dict(raiz_sha256=ff_v391["TGLExt.lean"], audit_sha256=ff_v391["TGL/Audit.lean"], impressao_formal=impressao_formal(ff_v391),
                                manifesto_sha256=sha(kman_raw))
# fx/eventos_sandbox.jsonl = copia do livro real (so lido) + elos ENCADEADOS de ensaio (a mesma regra de iald.py evento()); o real nao e tocado
linhas = [l for l in EVENTOS.read_text(encoding="utf-8").splitlines() if l.strip()]
ult = json.loads(linhas[-1])
seq, ant = ult["seq"], ult["hash"]


def elo(tipo, quem, dados):
    global seq, ant
    e = {"seq": seq + 1, "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "tipo": tipo, "quem": quem, "dados": dados, "anterior": ant}
    e["hash"] = hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    seq, ant = e["seq"], e["hash"]
    return e


b2 = str(RAIZ / "b2")
pd = str(RAIZ / "pd")
U, S16 = sha(um_sin)[:16], sha(selo_b)[:16]
base = dict(versao=VERSAO_SINTETICA, bancada=b2, acao="sincronizacao", um_py=U, selo=S16)
elos = dict(
    valido=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, gravacoes=["canonical_contracts.json", "CONTRATO_CANONICO_B3.md", "estado/sincronizacao/RECIBO_*.json"],
                                                         unidade="F0.6", nota="ENSAIO R3 em sandbox (copia b2); o quadro real segue intocado")),
    outra_sessao=elo("SINCRONIZACAO_BANCADA", "claude-c2", dict(base)),
    negacao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="NAO sincronizar a Bancada ate o operador decidir")),
    outro_programa=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, um_py="deadbeefdeadbeef", selo="feedfacefeedface")),
    outra_versao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, versao="v393")),
    outra_bancada=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, bancada=str(RAIZ / "b1"))),
    tipo_errado=elo("anotar", "claude-c1", dict(base)),
    sem_acao=elo("SINCRONIZACAO_BANCADA", "claude-c1", {k: v for k, v in base.items() if k != "acao"}),
    reparo=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, versao="v391", reparo=True, nota="ENSAIO A8: reparo de pino nomeado (sandbox)")),
    # N11: a negacao escondida por forma (NFD, largura cheia, largura zero) e por CHAVE; e a chave fora do conjunto fechado
    n11_nfd=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="na\u0303o sincronizar agora")),
    n11_largura_cheia=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="\uff2e\uff21\uff2f sincronizar agora")),
    n11_largura_zero=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="n\u200bao sincronizar agora")),
    n11_chave_negacao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nao_gravar=True)),
    n11_chave_proibido=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, PROIBIDO=True)),
    n11_chave_desconhecida=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, autorizado_por="qualquer")),
    # o elo que nomeia o decoy de producao (C:/t/vb*/pd), usado pelos controles em processo (N1, N2, N3, N4)
    decoy=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, bancada=pd, unidade="F0.6", nota="ENSAIO R3: decoy de producao em copia")),
)
ok_lines = linhas + [json.dumps(e, ensure_ascii=False) for e in elos.values()]
rec["fx"]["eventos_sandbox"] = gravar_novo(RAIZ / "fx" / "eventos_sandbox.jsonl", ("\n".join(ok_lines) + "\n").encode("utf-8"))
# o mesmo livro com elos FORJADOS (sem cadeia): um c1 completo mas sem encadear; um seq duplicado encadeado
forj_sem_cadeia = dict(elos["valido"], seq=90001, anterior="ff" * 32, hash="00" * 32)
forj_dup = elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(elos["valido"]["dados"], nota="seq duplicado encadeado"))
forj_dup["seq"] = elos["valido"]["seq"]
forj_dup["hash"] = hashlib.sha256(json.dumps({k: v for k, v in forj_dup.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
rec["fx"]["eventos_forjado_sem_cadeia"] = gravar_novo(RAIZ / "fx" / "eventos_forjado_sem_cadeia.jsonl", ("\n".join(ok_lines + [json.dumps(forj_sem_cadeia, ensure_ascii=False)]) + "\n").encode("utf-8"))
rec["fx"]["eventos_forjado_seq_duplicado"] = gravar_novo(RAIZ / "fx" / "eventos_forjado_seq_duplicado.jsonl", ("\n".join(ok_lines + [json.dumps(forj_dup, ensure_ascii=False)]) + "\n").encode("utf-8"))
rec["fx"]["elos_de_ensaio"] = {k: dict(seq=e["seq"], hash16=e["hash"][:16]) for k, e in elos.items()}
rec["fx"]["elos_forjados"] = dict(sem_cadeia_seq=forj_sem_cadeia["seq"], duplicado_seq=forj_dup["seq"])
rec["fx"]["eventos_reais_copiados"] = len(linhas)
rec["fx"]["ultimo_seq_real"] = ult["seq"]
rec["n_b1"], rec["n_b2"] = len(rec["b1"]), len(rec["b2"])
rec["manifesto_b2_sha256"] = sha(man2_raw)
rec["manifesto_producao_sha256"] = sha(man_raw)
p = RAIZ / "SANDBOX_MANIFEST_R3.json"
with open(p, "xb") as f:
    f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(dict(n_b1=rec["n_b1"], n_b2=rec["n_b2"], nos=rec["nos"]["um_py"]["sha256"][:16], nos_v392=rec["nos_v392"]["um_py"]["sha256"][:16],
                      kernel_manifest_v391=rec["nos"]["kernel_manifest"]["sha256"][:16], kernel_manifest_v392_sintetico=rec["nos_v392"]["kernel_manifest"]["sha256"][:16],
                      manifesto_b2=rec["manifesto_b2_sha256"][:16], elos=rec["fx"]["elos_de_ensaio"], manifest=str(p)), ensure_ascii=False, indent=1))
