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


def pii_forte(t):
    return bool(CPF.search(t) or RG.search(t) or FONE.search(t) or ENDERECO.search(t))


# valores que o OPERADOR declarou não serem credencial (por sha256 do valor, sem repetir o literal): a frase do autoteste do ACOM Crypto
# (acom_crypto_auth.py, _selftest) — «É diferente — publique», resposta do operador em 22/10/2026 à pergunta se era a frase-chave de acesso
APROVADOS = {"c521b24d2889ff6204f5c7b1c76a9524306dc2cdba8cd807c6cd64a69b72d8ab"}


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
def _todos():
    for dp, dns, fns in os.walk(_RAIZ):
        dns[:] = [x for x in dns if x != ".git"]
        for f in fns:
            yield Path(os.path.join(dp, f))
for p in _todos():
    rel = os.path.relpath(str(p), _RAIZ).replace(os.sep, "/")
    if rel in ("INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", "README.md", "PATENTES.md", "vinculo_patentario.json", ".gitattributes"):
        continue
    vistos.add(rel)
    partes = rel.split("/")
    if any(PASTA_PROIBIDA.match(x) for x in partes[:-1]):
        marca("pasta proibida (estado, perfil, login, segredo, sessão, terceiros)", rel)
    if NAVEGADOR.match(partes[-1]):
        marca("artefato de navegador", rel)
    b = p.read_bytes()
    if len(b) > 95 * 1024 * 1024:
        marca("acima de 95 MB", rel)
    a = no_indice.get(rel)
    if SEM_INDICE:
        pass
    elif a is None:
        marca("arquivo fora do índice", rel)
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
        if CPF.search(t) or RG.search(t):
            marca("CPF/RG sem máscara", rel)
        if FONE.search(t):
            marca("telefone sem máscara", rel)
        if EMAIL_PESSOAL.search(t):
            marca("e-mail pessoal sem máscara", rel)
        if ENDERECO.search(t):
            marca("endereço, CEP ou nascimento sem máscara", rel)
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
    if rel not in vistos and not os.path.isfile("\\\\?\\" + str((D / rel).resolve())):
        marca("índice sem arquivo", rel)
ok = not any(k for k in cont)
rel_p = Path(__file__).with_name("varredura_conferencia_%s.json" % D.name)
rel_p.write_text(json.dumps({"preparo": str(D), "regiao": REGIAO, "arquivos_varridos": len(vistos), "aprovado": ok, "contagem": dict(cont),
                             "amostra_de_caminhos": achados}, ensure_ascii=False, indent=1), encoding="utf-8")
print("%s: %d arquivos varridos | %s | %s" % (D.name, len(vistos), "APROVADO" if ok else "REPROVADO", dict(cont)))
sys.exit(0 if ok else 1)
