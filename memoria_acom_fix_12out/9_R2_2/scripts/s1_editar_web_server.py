# -*- coding: utf-8 -*-
"""R2.2, passo 1: edita SÓ o necessário no iald_web_server.py do candidato_r2_2 (N1 e N3 pela via do app).

O arquivo carrega a chave de API de produção: este script nunca imprime o conteúdo, só contagens e sha256; a edição
é feita no lugar, dentro da pasta do candidato (tempário -> conferência -> os.replace). Três trocas por âncora EXATA
(cada âncora tem de aparecer uma vez só; senão nada é escrito):
  A. agi_validate_path: teto de forma do caminho ANTES do realpath (N1) e conferência do arquivo pelo HANDLE do
     guard, com o caminho final do mesmo handle dentro da whitelist (N3).
  B. agi_files_read: os bytes vêm do guard.read_checked (o mesmo handle conferido), nunca de um segundo open por nome.
  C. ação «read» do agi_execute: idem.
Fim de linha: o arquivo é todo CRLF; a edição é feita em LF e devolvida em CRLF (conferido).
Também grava a cópia REDIGIDA (chave trocada por R do mesmo tamanho) em runs/ para as cópias de teste e o patch.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WEB = R22 / 'candidato_r2_2' / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')

OLD_A = r'''def agi_validate_path(path_str):
    """Validate that a path is within ALLOWED_ROOTS and has no traversal.
    Returns (resolved_path, error_string). Error is None if valid."""
    if not path_str:
        return None, "Path vazio"
    # Normalize separators
    path_str = path_str.replace("/", os.sep)
    # Block traversal
    if ".." in path_str:
        return None, "Path traversal (..) bloqueado"
    try:
        resolved = os.path.realpath(path_str)
    except (ValueError, OSError) as e:
        return None, f"Path invalido: {e}"
    if app_memory.protected_path(resolved):
        return None, "Arquivo confidencial fora da memória e do transporte"
    # Check whitelist
    allowed = False
    for root in ALLOWED_ROOTS:
        try:
            root_real = os.path.realpath(root)
            if os.path.commonpath([resolved.lower(), root_real.lower()]) == root_real.lower():
                allowed = True
                break
        except Exception:
            continue
    if not allowed:
        return None, f"Path fora da whitelist: {path_str}"
    return resolved, None
'''

NEW_A = r'''def agi_validate_path(path_str):
    """Validate that a path is within ALLOWED_ROOTS and has no traversal.
    Returns (resolved_path, error_string). Error is None if valid.

    R2.2 (review R2.1, 13/10/2026):
      * N1 -- the SHAPE of the path (length, number of components) is refused BEFORE os.path.realpath, whose cost on
        a path that does not exist grows with the square of the number of components (16,000 components: 2.8 s).
      * N3 -- an existing regular file is opened through the guard's HANDLE (guard.read_checked: read access without
        FILE_SHARE_DELETE; link count, file identity and the FINAL path of that same handle are checked), and that
        final path must also be inside the whitelist. The reads themselves (files/read and the 'read' action) take
        their bytes from read_checked, never from a second open by name."""
    if not path_str:
        return None, "Path vazio"
    # Normalize separators
    path_str = path_str.replace("/", os.sep)
    # Block traversal
    if ".." in path_str:
        return None, "Path traversal (..) bloqueado"
    guard = app_memory.guard
    shape = guard.path_shape_reason(path_str)          # R2.2 (N1): before realpath
    if shape:
        return None, f"Path recusado pelo guard ({shape})"
    try:
        resolved = os.path.realpath(path_str)
    except (ValueError, OSError) as e:
        return None, f"Path invalido: {e}"
    if app_memory.protected_path(resolved):
        return None, "Arquivo confidencial fora da memória e do transporte"

    def inside_whitelist(candidate):
        for root in ALLOWED_ROOTS:
            try:
                root_real = os.path.realpath(root)
                if os.path.commonpath([candidate.lower(), root_real.lower()]) == root_real.lower():
                    return True
            except Exception:
                continue
        return False

    # Check whitelist
    if not inside_whitelist(resolved):
        return None, f"Path fora da whitelist: {path_str}"
    if os.path.isfile(resolved):
        # R2.2 (N3): the FILE OBJECT behind the name, checked through its handle (no byte is used here)
        try:
            final, _ = guard.read_checked(resolved, max_bytes=0, log_path=app_memory._guard_log(),
                                          where='app.agi_validate_path')
        except guard.PathRefused:
            return None, "Arquivo confidencial fora da memória e do transporte"
        except guard.NotRegularFile:
            final = resolved
        except FileNotFoundError:
            final = resolved          # vanished after isfile: the caller reports "nao encontrado"
        except OSError as e:
            return None, f"Path invalido: {e}"
        if not inside_whitelist(final):
            return None, f"Path fora da whitelist: {path_str}"
    return resolved, None
'''

OLD_B = r'''    if not os.path.isfile(resolved):
        return jsonify({"error": f"Arquivo nao encontrado: {path_str}"}), 404
    file_size = os.path.getsize(resolved)
    if file_size > AGI_MAX_READ_BYTES:
        return jsonify({"error": f"Arquivo muito grande ({file_size} bytes, max {AGI_MAX_READ_BYTES})"}), 413
    try:
        # Try UTF-8 first, then latin-1 as fallback
        try:
            with open(resolved, "r", encoding="utf-8") as f:
                content = f.read()
            encoding = "utf-8"
        except UnicodeDecodeError:
            with open(resolved, "r", encoding="latin-1") as f:
                content = f.read()
            encoding = "latin-1"
        lines = content.count("\n") + 1
'''

NEW_B = r'''    if not os.path.isfile(resolved):
        return jsonify({"error": f"Arquivo nao encontrado: {path_str}"}), 404
    file_size = os.path.getsize(resolved)
    if file_size > AGI_MAX_READ_BYTES:
        return jsonify({"error": f"Arquivo muito grande ({file_size} bytes, max {AGI_MAX_READ_BYTES})"}), 413
    try:
        # R2.2 (review R2.1, N3 via the app): the bytes come from the guard's HANDLE (read_checked), never from a
        # second open by name: link count, identity and the FINAL path of that same handle were checked first.
        guard = app_memory.guard
        try:
            final, raw = guard.read_checked(resolved, max_bytes=AGI_MAX_READ_BYTES, log_path=app_memory._guard_log(),
                                            where='app.agi_files_read')
        except guard.PathRefused:
            log_request(session.get("username", "?"), "/admin/api/agi/files/read", "GET",
                        status="error", error="guard_handle_refused")
            return jsonify({"error": "Arquivo confidencial fora da memória e do transporte"}), 403
        except guard.NotRegularFile:
            return jsonify({"error": f"Arquivo nao encontrado: {path_str}"}), 404
        final_err = agi_validate_path(final)[1]
        if final_err:
            return jsonify({"error": final_err}), 403
        if len(raw) > AGI_MAX_READ_BYTES:
            return jsonify({"error": f"Arquivo muito grande (mais de {AGI_MAX_READ_BYTES} bytes)"}), 413
        resolved = final
        file_size = len(raw)
        # Try UTF-8 first, then latin-1 as fallback (newlines as open(..., "r") gives them)
        try:
            content = raw.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            content = raw.decode("latin-1")
            encoding = "latin-1"
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        lines = content.count("\n") + 1
'''

OLD_C = r'''                    else:
                        try:
                            with open(resolved, "r", encoding="utf-8") as f:
                                file_content = f.read()
                        except UnicodeDecodeError:
                            with open(resolved, "r", encoding="latin-1") as f:
                                file_content = f.read()
                        result["ok"] = True
                        result["content"] = file_content
                        result["size"] = file_size
                        result["lines"] = file_content.count("\n") + 1
'''

NEW_C = r'''                    else:
                        # R2.2 (review R2.1, N3 via the app): bytes from the guard's HANDLE, never a 2nd open by name
                        guard = app_memory.guard
                        try:
                            final, raw = guard.read_checked(resolved, max_bytes=AGI_MAX_READ_BYTES,
                                                            log_path=app_memory._guard_log(),
                                                            where='app.agi_execute.read')
                            final_err = agi_validate_path(final)[1]
                        except guard.PathRefused:
                            raw, final_err = None, "Arquivo confidencial fora da memória e do transporte"
                        if final_err or raw is None or len(raw) > AGI_MAX_READ_BYTES:
                            result["ok"] = False
                            result["error"] = final_err or f"Muito grande (mais de {AGI_MAX_READ_BYTES} bytes)"
                        else:
                            try:
                                file_content = raw.decode("utf-8")
                            except UnicodeDecodeError:
                                file_content = raw.decode("latin-1")
                            file_content = file_content.replace("\r\n", "\n").replace("\r", "\n")
                            result["ok"] = True
                            result["content"] = file_content
                            result["size"] = len(raw)
                            result["lines"] = file_content.count("\n") + 1
'''


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = WEB.read_bytes()
    out = {'antes_sha256': sha(raw), 'antes_bytes': len(raw), 'chaves_no_arquivo': len(KEY.findall(raw))}
    text = raw.decode('utf-8')
    n_crlf, n_lf, n_cr = text.count('\r\n'), text.count('\n'), text.count('\r')
    assert n_crlf == n_lf == n_cr, 'fim de linha misto: nada escrito'
    t = text.replace('\r\n', '\n')
    for nome, old, new in (('A', OLD_A, NEW_A), ('B', OLD_B, NEW_B), ('C', OLD_C, NEW_C)):
        c = t.count(old)
        out['ancora_' + nome] = c
        if c != 1:
            print(json.dumps(out))
            raise SystemExit('âncora %s aparece %d vez(es): nada escrito' % (nome, c))
        t = t.replace(old, new)
    novo = t.replace('\n', '\r\n').encode('utf-8')
    assert novo.count(b'\r\n') == novo.count(b'\n')
    assert KEY.findall(novo) == KEY.findall(raw), 'a chave mudou: nada escrito'
    compile(novo.decode('utf-8'), str(WEB), 'exec')          # sintaxe
    tmp = WEB.with_name(WEB.name + '.tmp_r2_2')
    with open(tmp, 'xb') as f:
        f.write(novo)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == novo
    os.replace(tmp, WEB)
    assert WEB.read_bytes() == novo
    red = KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), novo)
    (R22 / 'runs' / 'iald_web_server_r2_2_redigido.py').write_bytes(red)
    out.update(depois_sha256=sha(novo), depois_bytes=len(novo), redigido_sha256=sha(red))
    # conferência: a redigida não tem nenhuma das chaves originais
    out['redigida_sem_chave_original'] = all(k not in red for k in KEY.findall(novo))
    (R22 / 'runs' / 's1_editar_web_server.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())
