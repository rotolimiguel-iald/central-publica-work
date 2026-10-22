# -*- coding: utf-8 -*-
"""A GUARDA PÚBLICA da Central aberta (22/10/2026). Pela ordem do operador — «não há nenhum segredo industrial a proteger libere tudo,
segredo são dados pessoais, somente» —, o que barra um arquivo é CREDENCIAL (em qualquer lugar) ou DADO PESSOAL FORTE (CPF, RG, telefone)
onde a máscara visível não alcança: PDF, compactado, documento de escritório, carga embutida em base64. Os marcadores privados da casa
deixam de barrar (os nomes da stack, o protocolo desclassificado em 28/09/2026); do conjunto privado ficam só os de CREDENCIAL (padrões
nunca impressos). Achados de 22/10/2026 que esta guarda fecha, medidos antes de publicar:
  1. a guarda antiga barrava 862 arquivos do núcleo pelos nomes da casa — só 3 batiam em credencial, e nenhum era credencial;
  2. «AIza…» dentro de base64 é acaso da codificação, não chave: o blob é DECODIFICADO (zip, gzip, zlib, xz) e a carga é varrida;
  3. compactados (zip, docx…) eram copiados sem abrir — os PDFs de depósito do INPI dentro deles trazem CPF e telefone: cada membro é varrido;
  4. a senha de teste errada de propósito («senha-errada-999») e os canários sintéticos não são credencial.
API: avaliar_texto(t) -> (n_credenciais, {pii forte nos blobs}); avaliar_bytes(nome, b) -> (n_credenciais, {pii forte | motivo});
arquivo_de_credencial(nome) -> bool; pdf_da_casa(b) -> bool; png_de_rito(b) -> bool."""
import base64, binascii, gzip, io, json, lzma, re, sys, tarfile, zipfile, zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar  # noqa: E402

CRED = re.compile(r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|"
                  r"sk-[A-Za-z0-9]{32,}|hf_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|"
                  r"-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i:(password|passwd|senha|secret_key|api_key|apikey|access_token|client_secret|smtp_pass)"
                  r"[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']))")
CRED_ARQ = re.compile(r"(?i)(^\.env|\.env$|\.env\.|\.key$|\.pem$|\.p8$|\.p12$|\.pfx$|\.jks$|\.keystore$|\.mobileprovision$|auth\.json$|"
                      r"credentials?[^/]*\.json$|client_secret|token_huggin|central\.env|_authorization\.json$|^authorization\.json$|"
                      r"cookies?(\.json|\.txt|\.sqlite)?$|login data|web data)")
# valores sabidamente falsos (testes que exercitam a recusa): não são credencial
FAKE = re.compile(r"(?i)(senha-errada-\d+|FAKE_SYNTHETIC|NOT_A_SECRET|CANARY|<valor>|<senha>|<token>|<password>|\$\{[A-Z_]+\}|x{8,}|\*{8,}|"
                  r"changeme|placeholder)")
SENS = ("cpf", "cpf_rotulado", "rg_rotulado", "telefone", "telefone_br", "cep_rotulado", "endereco", "nascimento")
DOC_NOME = re.compile(r"(?i)(comprovante|recibo|\bgru\b|\bpix\b|procura[cç]|peti[cç]|formul|guia|boleto|pagamento|dep[oó]sito|protocolo|"
                      r"notifica|despacho|exig[eê]ncia|\btaxa|\bfee\b|receipt|invoice|epct|\brg\b|\bcnh\b|\bcpf\b|identidade)")
DOC_EXT = (".pdf", ".doc", ".docx", ".odt", ".rtf", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".eml", ".msg", ".xls", ".xlsx")
B64 = re.compile(r"[A-Za-z0-9+/]{1000,}={0,2}")
_IDS_CRED = {"K01_openai", "K02_github", "K03_aws", "K04_slack", "K05_google", "K06_assign", "K07_privkey", "K11_url_token"}
_PRIV = Path.home() / ".iald_privado" / "marcadores_privado.json"
assert _PRIV.is_file(), "conjunto privado de marcadores ausente em ~/.iald_privado — PARAR"
MARC = [re.compile(m["re"], re.I if "i" in (m.get("flags") or "") else 0)
        for m in json.loads(_PRIV.read_text(encoding="utf-8"))["markers"] if m["id"] in _IDS_CRED]
assert len(MARC) == len(_IDS_CRED), "marcadores de credencial incompletos — PARAR"
CASA = re.compile(r"(?i)(rotoli|\biald\b|luminodin|\bTGL\b|um\.py|haja luz|β_TGL|beta_tgl|gravita[cç][aã]o lumino|matplotlib)")


def _cred(t):
    n = 0
    for rx in [CRED] + MARC:
        for m in rx.finditer(t):
            if not FAKE.search(m.group(0)):
                n += 1
    return n


def _pii(t):
    _, c = mascarar(t)
    return {k for k in c if k in SENS}


def _b64(s):
    try:
        return base64.b64decode(s + "=" * (-len(s) % 4))
    except (binascii.Error, ValueError):
        return None


def pdf_texto(b):
    import logging
    logging.disable(logging.CRITICAL)
    from pypdf import PdfReader
    r = PdfReader(io.BytesIO(b))
    meta = " ".join(str(v) for v in (r.metadata or {}).values())
    return " ".join((pg.extract_text() or "") for pg in r.pages), meta


MAX_CARGA = 64 * 1024 * 1024   # teto de descompressão: os fixtures do ACOM trazem BOMBAS de compressão (achado de 22/10/2026 — o
                               # preparo do work travou em fixtures/bad_bomb.json, 2,9 KB que se expandem sem fim)


def _descomprimir(b, wbits):
    """zlib/gzip com teto: além de MAX_CARGA é bomba — recusa (fail-closed), nunca expande."""
    d = zlib.decompressobj(wbits)
    out = d.decompress(b, MAX_CARGA)
    if d.unconsumed_tail or len(out) >= MAX_CARGA:
        raise OverflowError("carga_grande_demais")
    return out


def _deslzma(b):
    d = lzma.LZMADecompressor()
    out = d.decompress(b, max_length=MAX_CARGA)
    if len(out) >= MAX_CARGA or (not d.eof and not d.needs_input):
        raise OverflowError("carga_grande_demais")
    return out


def avaliar_texto(t, prof=0):
    """O texto fora dos blobs base64 é avaliado por CREDENCIAL (o dado pessoal visível a máscara troca); o que está DENTRO de cada blob é
    decodificado e avaliado por credencial E por dado pessoal forte, porque a máscara não o alcança."""
    fora = B64.sub(" ", t) if len(t) >= 1000 else t
    n, k = _cred(fora), set()
    if prof < 3 and len(t) >= 1000:
        for m in B64.finditer(t):
            b = _b64(m.group(0))
            if b:
                nn, kk = avaliar_bytes("blob", b, prof + 1)
                n += nn
                k |= kk
    return n, k


def avaliar_bytes(nome, b, prof=0):
    """(n_credenciais, {pii forte | motivo de recusa}) de uma carga binária, abrindo compactados e documentos."""
    if prof > 5:
        return 0, {"carga_profunda_demais"}
    nl = nome.lower()
    try:
        if b[:2] == b"PK":
            z = zipfile.ZipFile(io.BytesIO(b))
            n, k = 0, set()
            if sum(i.file_size for i in z.infolist()) > 4 * MAX_CARGA:
                return 0, {"carga_grande_demais"}
            for info in z.infolist():
                if info.is_dir():
                    continue
                if info.flag_bits & 0x1:
                    k.add("compactado_cifrado")
                    continue
                if info.file_size > MAX_CARGA:
                    k.add("carga_grande_demais")
                    continue
                base = info.filename.rsplit("/", 1)[-1]
                # o nome só conta em DOCUMENTO (o código «tgl_formula_completa.py» não é formulário — achado do teste de 22/10/2026)
                if base.lower().endswith(DOC_EXT) and DOC_NOME.search(base) and not nl.endswith((".docx", ".xlsx", ".pptx", ".odt")):
                    k.add("documento_de_protocolo_no_compactado")
                nn, kk = avaliar_bytes(info.filename, z.read(info), prof + 1)
                n += nn
                k |= kk
            return n, k
        if len(b) > 262 and b[257:262] == b"ustar":
            n, k = 0, set()
            with tarfile.open(fileobj=io.BytesIO(b)) as tf:
                for m in tf.getmembers():
                    if m.isfile() and m.size > MAX_CARGA:
                        k.add("carga_grande_demais")
                    elif m.isfile():
                        nn, kk = avaliar_bytes(m.name, tf.extractfile(m).read(), prof + 1)
                        n += nn
                        k |= kk
            return n, k
        if b[:2] == b"\x1f\x8b":
            return avaliar_bytes(nome[:-3] if nl.endswith(".gz") else nome, _descomprimir(b, 31), prof + 1)
        if b[:6] == b"\xfd7zXZ\x00":
            return avaliar_bytes(nome, _deslzma(b), prof + 1)
        if b[:1] == b"\x78" and b[1:2] in (b"\x01", b"\x5e", b"\x9c", b"\xda"):
            try:
                return avaliar_bytes(nome, _descomprimir(b, 15), prof + 1)
            except zlib.error:
                pass
        if b[:6] in (b"7z\xbc\xaf\x27\x1c",) or b[:4] in (b"Rar!",):
            return 0, {"compactado_nao_verificavel"}
        if b[:4] == b"%PDF":
            t, _meta = pdf_texto(b)
            return _cred(t), _pii(t)
        if b[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":   # OLE (doc, xls, msg): texto bruto em latin-1 e utf-16
            t = b.decode("latin-1") + " " + b.decode("utf-16-le", "replace")
            return _cred(t), _pii(t)
        if b[:8] == b"\x89PNG\r\n\x1a\n" or b[:3] == b"\xff\xd8\xff" or b[4:8] == b"ftyp" or b[:4] in (b"GIF8", b"RIFF"):
            return 0, set()
    except OverflowError:  # bomba de compressão: recusa
        return 0, {"carga_grande_demais"}
    except Exception as ex:  # ilegível: fail-closed
        return 0, {"ilegivel:" + type(ex).__name__}
    t = b.decode("utf-8", "replace")
    if t.count("�") > max(64, len(t) // 20):
        return _cred(b.decode("latin-1")), set()
    if nl.endswith(".xml") or "<w:t" in t[:20000]:
        t = re.sub(r"<[^>]+>", "", t)
    n, k = avaliar_texto(t, prof)
    return n, k | _pii(t)


def arquivo_de_credencial(nome):
    return bool(CRED_ARQ.search(nome))


# O ACERVO DO ESCRITÓRIO (PJ separada; regra das casas) nunca entra: um log de busca no acervo da bancada listou caminhos de dentro de
# C:\Escritorio com nomes de partes de audiência (achado de 22/10/2026, antes de publicar). Barra caminho PARA DENTRO do acervo (uma
# subpasta), audiência realizada e número de processo no padrão CNJ; a menção estrutural («o Escritório, raiz C:\Escritorio, é PJ
# separada»; CLAUDE.md e INSTRUCOES.md dele) fica.
ESCRITORIO = re.compile(r"(?i)[A-Z]:(?:\\\\|\\|/){1,2}Escrit[oó]rio(?:\\\\|\\|/){1,2}(?!(?:CLAUDE|INSTRUCOES)\.md\b)[^\\/\s\"'`|*<>]+(?:\\\\|\\|/)|"
                        r"audi[eê]ncias?\s+realizad|\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b|"
                        # (22/10/2026, 2º achado) peças dos tribunais superiores: «agravo_interno_AREsp_<número>_GO.docx», «filesSTJ <partes>»
                        r"\b(?:AREsp|REsp|AgInt|AgRg|RHC|RMS|EDcl)[ _.nº]{0,4}\d{5,7}\b|agravo[ _]interno|\bfilesSTJ\b")


def toca_escritorio(t):
    return bool(ESCRITORIO.search(t))


def pdf_da_casa(b):
    """PDF da casa: o texto ou os metadados trazem a casa (autor, IALD, TGL) ou é figura do matplotlib. O resto é obra de terceiro."""
    try:
        t, meta = pdf_texto(b)
    except Exception:
        return False
    return bool(CASA.search(t[:200000] + " " + meta))


def png_de_rito(b):
    """PNG gerado pelos ritos: traz a marca do matplotlib nos blocos de texto. Captura de tela, página renderizada e ícone não trazem."""
    return b[:8] == b"\x89PNG\r\n\x1a\n" and b"matplotlib" in b[:8192].lower()
