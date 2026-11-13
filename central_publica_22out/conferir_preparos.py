# -*- coding: utf-8 -*-
"""CONFERÊNCIA INDEPENDENTE dos preparos públicos (22/10/2026) — quem constrói não é quem aprova: este script NÃO importa a guarda nem a
máscara; reimplementa as checagens e varre o que foi PREPARADO (o que iria ao GitHub). Reprova (exit 1) se achar: pasta de estado/perfil/
login/segredo/sessão; artefato de navegador; credencial; CPF/RG/telefone/e-mail pessoal sem máscara; PDF ou compactado com dado pessoal
forte; nas regiões, PDF de terceiro ou imagem que não é figura de rito; arquivo acima de 95 MB; arquivo fora do índice ou índice sem
arquivo. Relatório: conferencia_<preparo>.json (contagens e caminhos; nunca o valor achado).
Uso: C:\\Python314\\python.exe conferir_preparos.py <pasta_do_preparo> [regiao]"""
import base64, binascii, hashlib, io, json, os, re, sys, zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
import logging
logging.disable(logging.CRITICAL)
from pypdf import PdfReader

D = Path(sys.argv[1])
REGIAO = len(sys.argv) > 2 and sys.argv[2] == "regiao"
PASTA_PROIBIDA = re.compile(r"(?i)^(state|secrets?|profiles?|login|logins|credentials?|cookies?|session_requests?|sessions|memoria_iald|"
                            r"fontes_externas|vendor|intermediates|leveldb|local storage|indexeddb|kimi-runs)$")
NAVEGADOR = re.compile(r"(?i)^(cookies|login data|web data|local state|history|preferences|network persistent state|current session|"
                       r"last session|.*\.ldb)$")
TOKENS = re.compile(r"(gh[posu]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|"
                    r"\bsk-[A-Za-z0-9]{32,}|\bhf_[A-Za-z0-9]{30,}|\bAKIA[0-9A-Z]{16}\b|\bAIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|"
                    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,})")
ATRIB = re.compile(r"(?i)(password|passwd|senha|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|bearer|"
                   r"authorization|cookie)[\"']?\s*[:=]\s*[\"']([^\"'\s]{12,})[\"']")
FALSO = re.compile(r"(?i)(errada|fake|synthetic|canary|not_a_secret|example|exemplo|placeholder|changeme|dummy|<|\$\{|x{6,}|\*{6,}|"
                   r"dado pessoal removido|redacted|test|teste|__Host-|__Secure-|_session\b|\.(?:txt|json|md|py|yaml)$|(?-i:^[A-Z0-9_]+$)|_only$|DO_NOT|(?-i:^[0-9a-f]{40,64}$))")   # (nome de cookie não é valor)
# (22/10/2026) o ACERVO DO ESCRITÓRIO (PJ separada): caminho para dentro dele, audiência realizada, número de processo CNJ
ESCRIT = re.compile(r"(?i)[A-Z]:(?:\\\\|\\|/){1,2}Escrit[oó]rio(?:\\\\|\\|/){1,2}(?!(?:CLAUDE|INSTRUCOES)\.md\b)[^\\/\s\"'`|*<>]+(?:\\\\|\\|/)|"
                    r"audi[eê]ncias?\s+realizad|\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b|"
                    r"\b(?:AREsp|REsp|AgInt|AgRg|RHC|RMS|EDcl)[ _.nº]{0,4}\d{5,7}\b|agravo[ _]interno|\bfilesSTJ\b")
CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|(?i:\bCPF\b[^\n\d]{0,12}\d{11}\b)")
# (22/10/2026) RG com rótulo de documento e no formato real — na TGL «RG» é Relatividade Geral e «identidade» é termo central
RG = re.compile(r"(?i)(\bRG\b|\bR\.G\.|registro geral|(?:carteira|c[ée]dula|documento) de identidade|identidade\s*(?:n\.?\s?[º°]|n[úu]m))"
                r"[\s:.\-nº°]{0,6}\d{1,2}(?:\.\d{3}\.\d{3}|\d{5,6})(?:-[\dXx])?(?![\d.])")
FONE = re.compile(r"(?i)\b(tel|fone|cel|whats|whatsapp|telefone|celular)\b[^\n\d]{0,12}(\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}|"
                  r"\+55\s?\(?\d{2}\)?\s?9?\d{4}-?\d{4}|\(\d{2}\)\s?9\d{4}-?\d{4}|\(0\d{2,3}\)\s?\d{4,5}-\d{4}\b")   # (22/10: DDD com zero)
ENDERECO = re.compile(r"(?i)\bCEP\b[^\d]{0,6}\d{2}\.?\d{3}-?\d{3}\b|\b(?:Qd|Quadra)\.?\s*\d+[^\n]{0,30}?\b(?:Lt|Lote)\.?\s*\d+|"
                      r"(data de nascimento|nascid[oa] em)\s*[:\-]?\s*\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}")
EMAIL_PESSOAL = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]++@(hotmail|gmail|icloud|outlook|yahoo|live|uol|bol|terra|msn|me|protonmail|"
                           r"rmiguel\.adv)\.[a-z.]{2,6}", re.I)   # possessiva: linear em trechos longos sem @
CASA = re.compile(r"(?i)(rotoli|\biald\b|luminodin|\bTGL\b|um\.py|haja luz|matplotlib)")
# (22/10/2026) identificadores de pessoas privadas (lista LOCAL ~/.iald_privado/terceiros_privados.json; nunca no código publicado)
_TPP = Path.home() / ".iald_privado" / "terceiros_privados.json"
TERC = (re.compile(r"(?i)(?<![A-Za-zÀ-ú])(?:" + "|".join(json.loads(_TPP.read_text(encoding="utf-8"))["nomes"]) + r")(?![A-Za-zÀ-ú])")
        if _TPP.is_file() else None)
TXT_EXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
           ".jsx", ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".xml", ".svg", ".dat",
           ".log", ".out", ".diff", ".patch", ".spec", ".gitignore", ".gitattributes", ".example", ".r", ".jl", ".c", ".h", ".cpp", ".rs"}
achados = defaultdict(list)
cont = Counter()


def marca(cat, rel):
    cont[cat] += 1
    if len(achados[cat]) < 200:
        achados[cat].append(rel)


def texto_pdf(b):
    try:
        r = PdfReader(io.BytesIO(b))
        return " ".join((pg.extract_text() or "") for pg in r.pages) + " " + " ".join(str(v) for v in (r.metadata or {}).values())
    except Exception:
        return None


def _sem_b64_zip(t):
    """O texto sem os blocos base64 longos que decodificam para ZIP (PK): esses são varridos por dentro por varrer_zip (05/11/2026)."""
    if len(t) < 1000:
        return t

    def _tira(m):
        try:
            bb = base64.b64decode(m.group(0) + "=" * (-len(m.group(0)) % 4))
        except (binascii.Error, ValueError):
            return m.group(0)
        return " " if bb[:2] == b"PK" else m.group(0)
    return re.sub(r"[A-Za-z0-9+/]{1000,}={0,2}", _tira, t)


def pii_forte(t):
    return bool(CPF.search(t) or RG.search(t) or FONE.search(t) or ENDERECO.search(t))


# valores que o OPERADOR declarou não serem credencial (por sha256 do valor, sem repetir o literal): a frase do autoteste do ACOM Crypto
# (acom_crypto_auth.py, _selftest) — «É diferente — publique», resposta do operador em 22/10/2026 à pergunta se era a frase-chave de acesso
# (02/11/2026, custódia v405) rótulo de fluxo do Codex, sem segredo: chave authorization em filmes_v7_20261024/adendo_h_v404 (MEDIA_GO.json, release_media.py); valor lido e aceito pela gerência c1, não pelo operador
APROVADOS = {"c521b24d2889ff6204f5c7b1c76a9524306dc2cdba8cd807c6cd64a69b72d8ab", "d1e00e0d2979f7f78e31b374bb718939733768bc9480b6d9b5ce96a634b4d9e1"}


def cred(t):
    if TOKENS.search(t):
        return True
    # (o rótulo falso se lê no VALOR também: nome de arquivo, constante em maiúsculas, «…_only», «DO_NOT_…»)
    return any(not (FALSO.search(m.group(0)) or FALSO.search(m.group(2))) and hashlib.sha256(m.group(2).encode()).hexdigest() not in APROVADOS
               for m in ATRIB.finditer(t))


def varrer_zip(b, rel, prof=0):
    try:
        z = zipfile.ZipFile(io.BytesIO(b))
    except zipfile.BadZipFile:
        marca("compactado ilegível", rel); return
    for n in z.namelist():
        if n.endswith("/"):
            continue
        mb = z.read(n)
        if mb[:2] == b"PK" and prof < 3:
            varrer_zip(mb, rel + "!" + n, prof + 1); continue
        t = texto_pdf(mb) if mb[:4] == b"%PDF" else mb.decode("utf-8", "replace")
        if t is None:
            marca("PDF ilegível dentro de compactado", rel + "!" + n); continue
        t = re.sub(r"<[^>]+>", "", t) if n.lower().endswith(".xml") else t
        if pii_forte(t) or EMAIL_PESSOAL.search(t):
            marca("compactado com dado pessoal", rel + "!" + n)
        if cred(t):
            marca("compactado com credencial", rel + "!" + n)


SEM_INDICE = not (D / "INDICE_PUBLICO.json").is_file()   # 22/10/2026: a pasta central/ do site não tem índice — só as checagens de conteúdo
idx = {"arquivos": []} if SEM_INDICE else json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))
no_indice = {a["caminho"]: a for a in idx["arquivos"]}
vistos = set()
_RAIZ = "\\\\?\\" + str(D.resolve())
# (11/11/2026, claude-site-custodia) RECONSTRUIR_COPIAS.py: o script que recria as cópias referenciadas num clone (a cópia vira referência)
_RAIZ_NOMES = {"INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", "README.md", "PATENTES.md", "vinculo_patentario.json", ".gitattributes",
               "llms.txt", "RECONSTRUIR_COPIAS.py"}
def _todos():
    for dp, dns, fns in os.walk(_RAIZ):
        dns[:] = [x for x in dns if x != ".git"]
        for f in fns:
            yield Path(os.path.join(dp, f))
for p in _todos():
    rel = os.path.relpath(str(p), _RAIZ).replace(os.sep, "/")
    # (23/10/2026) os gerados da raiz e o llms.txt (curadoria à mão, do Kimi) não precisam estar no índice — mas o CONTEÚDO deles passa
    # pelas mesmas checagens de todo o resto (antes, a raiz era pulada inteira)
    raiz_gerada = rel in _RAIZ_NOMES or rel.startswith("INDICE_PUBLICO_PARTES/")   # (11/11/2026, v410) as partes do índice
    vistos.add(rel)
    partes = rel.split("/")
    if any(PASTA_PROIBIDA.match(x) for x in partes[:-1]):
        marca("pasta proibida (estado, perfil, login, segredo, sessão, terceiros)", rel)
    if NAVEGADOR.match(partes[-1]):
        marca("artefato de navegador", rel)
    b = p.read_bytes()
    # AO LADO (11/11/2026, custódia v410): o índice inteiro acima do teto, com as partes no preparo, não vai ao git — as partes vão; o que
    # o isenta aqui é conferido depois do laço (partes = índice, entrada por entrada; o inteiro fora do git), senão reprova
    if len(b) > 95 * 1024 * 1024 and not (rel == "INDICE_PUBLICO.json" and (D / "INDICE_PUBLICO_PARTES" / "PARTES.json").is_file()):
        marca("acima de 95 MB", rel)
    a = no_indice.get(rel)
    if SEM_INDICE or raiz_gerada:
        pass
    elif a is None:
        marca("arquivo fora do índice", rel)
    elif a.get("igual_a"):                      # (11/11/2026) a cópia referenciada não fica no preparo: o índice aponta o original
        marca("cópia referenciada ainda no preparo", rel)
    elif a["sha256"] != hashlib.sha256(b).hexdigest():
        marca("sha256 diferente do índice", rel)
    e = p.suffix.lower() if p.suffix else ("." + p.name.lstrip(".")).lower()
    if b[:4] == b"%PDF":
        t = texto_pdf(b)
        if t is None:
            marca("PDF ilegível", rel); continue
        if pii_forte(t):
            marca("PDF com dado pessoal forte", rel)
        if REGIAO and not CASA.search(t):
            marca("PDF sem marca da casa (possível obra de terceiro)", rel)
        continue
    if b[:2] == b"PK":
        varrer_zip(b, rel); continue
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        if REGIAO and b"matplotlib" not in b[:8192].lower():
            marca("PNG que não é figura de rito", rel)
        continue
    if b[:3] == b"\xff\xd8\xff" or b[:4] in (b"GIF8", b"RIFF"):
        if REGIAO:
            marca("imagem não-PNG em região", rel)
        continue
    if e in TXT_EXT or b[:1] in (b"{", b"[", b"#"):
        t = b.decode("utf-8", "replace")
        # ERRATA AO LADO (05/11/2026, custódia v408, claude-site-custodia, em nome próprio): as cinco regras de PII abaixo liam também o texto
        # cru dos blocos base64 que embutem ZIP, e a regra de quadra/lote casou num trecho aleatório do base64 (8 *_FINAL.py da v408). Esses
        # blocos são varridos POR DENTRO por varrer_zip com as mesmas regras (pii_forte + EMAIL_PESSOAL), logo saem só do texto cru; bloco
        # base64 que não é ZIP segue varrido cru, como antes. TERC, Escritório e credencial não mudam. Antes: as regras liam `t`.
        t_pii = _sem_b64_zip(t)
        if CPF.search(t_pii) or RG.search(t_pii):
            marca("CPF/RG sem máscara", rel)
        if FONE.search(t_pii):
            marca("telefone sem máscara", rel)
        if EMAIL_PESSOAL.search(t_pii):
            marca("e-mail pessoal sem máscara", rel)
        if ENDERECO.search(t_pii):
            marca("endereço, CEP ou nascimento sem máscara", rel)
        if TERC is not None and TERC.search(t):
            marca("identificador de terceiro sem máscara", rel)
        # os 4 scripts da esteira trazem os PADRÕES da regra e exemplos fictícios (revistos em 22/10/2026) — só eles, só nesta pasta
        esteira = rel.startswith("central_publica_22out/") and partes[-1] in ("aplicar_regra_escritorio.py", "conferir_preparos.py",
                                                                              "guarda_publica.py", "testar_regra_escritorio.py")
        if (ESCRIT.search(t) or ESCRIT.search(rel)) and not esteira:
            marca("toca o acervo do Escritório", rel)
        fora_b64 = re.sub(r"[A-Za-z0-9+/]{1000,}={0,2}", " ", t) if len(t) >= 1000 else t
        if cred(fora_b64):
            marca("credencial em texto", rel)
        for m in re.finditer(r"[A-Za-z0-9+/]{1000,}={0,2}", t):
            try:
                bb = base64.b64decode(m.group(0) + "=" * (-len(m.group(0)) % 4))
            except (binascii.Error, ValueError):
                continue
            if bb[:2] == b"PK":
                varrer_zip(bb, rel + "!base64")
for rel in no_indice:
    if rel not in vistos and not no_indice[rel].get("igual_a") and not os.path.isfile("\\\\?\\" + str((D / rel).resolve())):
        marca("índice sem arquivo", rel)
# AO LADO (11/11/2026, claude-site-custodia; decisão do operador: a cópia vira referência, a partir da v411), conferido por conta própria
# (não importa copias_referencia.py): cada entrada com "igual_a" aponta para uma entrada do MESMO índice que não é referência, com os mesmos
# bytes e o mesmo sha256, e o arquivo desse original está no preparo com esse sha256 (cada original lido uma vez); a cópia não é arquivo da
# raiz nem parte do índice; com alguma referência, a raiz traz RECONSTRUIR_COPIAS.py. A cópia física que ficou no preparo é marcada no laço.
_refs = [a for a in idx["arquivos"] if a.get("igual_a")]
if _refs:
    _alvos = {}
    for a in _refs:
        o = no_indice.get(a["igual_a"])
        if (o is None or o.get("igual_a") or a["igual_a"] == a["caminho"] or o["sha256"] != a["sha256"] or o["bytes"] != a["bytes"]
                or a["caminho"] in _RAIZ_NOMES or a["caminho"].startswith("INDICE_PUBLICO_PARTES/")):
            marca("referência de cópia não confere com o original", a["caminho"]); continue
        _alvos[a["igual_a"]] = o["sha256"]
    for _r, _s in sorted(_alvos.items()):
        try:
            _h = hashlib.sha256()
            with open(_RAIZ + "\\" + _r.replace("/", "\\"), "rb") as _f:
                for _bl in iter(lambda: _f.read(1 << 20), b""):
                    _h.update(_bl)
            _ok_o = _h.hexdigest() == _s
        except OSError:
            _ok_o = False
        if not _ok_o:
            marca("original de cópia ausente ou diferente do índice", _r)
    if not (D / "RECONSTRUIR_COPIAS.py").is_file():
        marca("cópias referenciadas sem RECONSTRUIR_COPIAS.py na raiz", "RECONSTRUIR_COPIAS.py")
# AO LADO (11/11/2026, custódia v410, claude-site-custodia): o ÍNDICE EM PARTES, conferido por conta própria (não importa indice_partes.py):
# cada parte com os bytes e o sha256 do cabeçalho, nenhuma acima de 95 MiB, nada além delas na pasta; a lista «arquivos» das partes,
# concatenada na ordem, igual à do índice inteiro, entrada por entrada; e o índice inteiro fora do git (nem rastreado, nem visível ao status)
_PD = D / "INDICE_PUBLICO_PARTES"
if not SEM_INDICE and _PD.exists():
    import subprocess
    _ok_p = True
    try:
        _cab = json.loads((_PD / "PARTES.json").read_text(encoding="utf-8"))
        _uniao, _nomes = [], {"PARTES.json"}
        for _pt in _cab["partes"]:
            _arq = _pt["arquivo"]
            if not re.fullmatch(r"INDICE_PUBLICO_PARTES/parte_\d{3}\.json", _arq):
                _ok_p = False; break
            _pb = (D / _arq).read_bytes()
            if len(_pb) != _pt["bytes"] or len(_pb) > 95 * 1024 * 1024 or hashlib.sha256(_pb).hexdigest() != _pt["sha256"]:
                _ok_p = False
            _uniao += json.loads(_pb.decode("utf-8"))["arquivos"]
            _nomes.add(_arq.split("/")[-1])
        if _uniao != idx["arquivos"] or _cab.get("entradas") != len(idx["arquivos"]) or set(os.listdir(_PD)) != _nomes:
            _ok_p = False
    except Exception:  # noqa: BLE001
        _ok_p = False
    if not _ok_p:
        marca("partes do índice não conferem com o índice", "INDICE_PUBLICO_PARTES/PARTES.json")
    _env = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}   # check-ignore recusa a magia 'literal' (rc 128)
    _ign = subprocess.run(["git", "-C", str(D), "check-ignore", "-q", "INDICE_PUBLICO.json"], capture_output=True, env=_env).returncode == 0
    _rastr = subprocess.run(["git", "-C", str(D), "ls-files", "--cached", "--", "INDICE_PUBLICO.json"], capture_output=True, text=True, env=_env).stdout.strip()
    if not _ign or _rastr:
        marca("índice inteiro ainda no git (as partes o substituem)", "INDICE_PUBLICO.json")
ok = not any(k for k in cont)
rel_p = Path(__file__).with_name("varredura_conferencia_%s.json" % D.name)
rel_p.write_text(json.dumps({"preparo": str(D), "regiao": REGIAO, "arquivos_varridos": len(vistos), "aprovado": ok, "contagem": dict(cont),
                             "amostra_de_caminhos": achados}, ensure_ascii=False, indent=1), encoding="utf-8")
print("%s: %d arquivos varridos | %s | %s" % (D.name, len(vistos), "APROVADO" if ok else "REPROVADO", dict(cont)))
sys.exit(0 if ok else 1)
