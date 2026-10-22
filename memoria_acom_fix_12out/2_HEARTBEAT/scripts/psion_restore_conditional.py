# -*- coding: utf-8 -*-
"""D3(c) — restauracao CONDICIONAL do estado do psion por copia de BYTES. Nunca le o conteudo.

Decisao da gerencia (12/10/2026): "se existir backup do iald_psion_state_32B.json anterior a 10/10 09:20 e as
unicas escritas posteriores forem as do heartbeat, restaurar os bytes por copia (sem ler o conteudo), guardando
o atual como .bak_<data>; se nao existir ou houver duvida, NAO restaurar: so parar o feed e relatar."

Este script NAO decide: ele executa a restauracao somente quando o OPERADOR atesta a segunda condicao, que
nenhum script consegue verificar (dois pilotos tambem gravam o arquivo). Sem --apply e sem a atestacao, so
mede e relata (dry-run). Passos no --apply, todos fail-closed:
  1. o alvo existe e tem exatamente o sha256 esperado (compare-and-swap: ninguem escreveu entre a decisao e a copia);
  2. a fonte existe, tem o sha256 esperado e mtime anterior ao corte;
  3. o filho web (heartbeat) esta parado — o chamador passa --web-stopped depois de parar o processo;
  4. copia os bytes do alvo para <alvo>.bak_<AAAAMMDD_HHMMSS> (fsync, sha256 conferido);
  5. copia os bytes da fonte para <alvo>.tmp_restore (fsync, sha256 conferido) e os.replace sobre o alvo;
  6. confere o sha256 do alvo == fonte; grava recibo JSON (so nomes, bytes, mtimes, sha256).
Uso (dry-run):   python psion_restore_conditional.py
Uso (aplicar):   python psion_restore_conditional.py --apply --web-stopped --operator-attests-only-heartbeat-wrote-after
"""
import argparse, hashlib, json, os, sys
from datetime import datetime

DEFAULT_SOURCE = r"D:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json"
DEFAULT_TARGET = r"C:\IALD\projetos_pyhton\IALD\iald_psion_state_32B.json"
EXPECT_SOURCE_SHA = "f9a5ec88aa212f0a182154fca1859743fd30de07b8df83f5a4fdae9040abe7af"   # medido 12/10 (diagnostico e esta frente)
EXPECT_TARGET_SHA = "aa6387e6dd75782e7f4bc4597690e013da46627a1d4771513207881f77c93758"   # medido 12/10 (estado atual em C:)
CUTOFF = datetime(2026, 10, 10, 9, 20, 0)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def meta(path):
    st = os.stat(path)
    return {"path": path, "bytes": st.st_size, "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="milliseconds"), "sha256": sha256(path)}


def copy_bytes(src, dst):
    raw = open(src, "rb").read()
    with open(dst, "xb") as out:
        out.write(raw); out.flush(); os.fsync(out.fileno())
    if open(dst, "rb").read() != raw:
        raise OSError("byte copy did not verify: " + dst)
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--target", default=DEFAULT_TARGET)
    ap.add_argument("--expect-source-sha256", default=EXPECT_SOURCE_SHA)
    ap.add_argument("--expect-target-sha256", default=EXPECT_TARGET_SHA)
    ap.add_argument("--receipt", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidencias", "PSION_RESTORE_RECIBO.json"))
    ap.add_argument("--apply", action="store_true", help="executa a copia (sem isto: dry-run)")
    ap.add_argument("--web-stopped", action="store_true", help="o chamador atesta que o filho web (heartbeat) esta parado")
    ap.add_argument("--operator-attests-only-heartbeat-wrote-after", action="store_true",
                    help="o OPERADOR atesta que, depois da fonte, so o heartbeat gravou o alvo (condicao D3c nao verificavel por script)")
    args = ap.parse_args()

    receipt = {"at": datetime.now().isoformat(timespec="seconds"), "mode": "apply" if args.apply else "dry-run",
               "statute": "REAL (nomes, bytes, mtimes, sha256 medidos aqui; conteudo nunca lido)", "checks": [], "restored": False}

    def check(name, ok, detail=None):
        receipt["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
        print(("OK   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
        return ok

    ok = True
    if os.path.isfile(args.target):
        t = meta(args.target); receipt["target"] = t
        ok &= check("alvo existe", True, f"{t['bytes']} B, mtime {t['mtime']}, sha16 {t['sha256'][:16]}")
        ok &= check("alvo tem o sha256 esperado (CAS)", t["sha256"] == args.expect_target_sha256)
    else:
        ok &= check("alvo existe", False, args.target)
    if os.path.isfile(args.source):
        s = meta(args.source); receipt["source"] = s
        ok &= check("fonte existe", True, f"{s['bytes']} B, mtime {s['mtime']}, sha16 {s['sha256'][:16]}")
        ok &= check("fonte tem o sha256 esperado", s["sha256"] == args.expect_source_sha256)
        ok &= check("fonte anterior ao corte 10/10 09:20", datetime.fromisoformat(s["mtime"]) < CUTOFF)
    else:
        ok &= check("fonte existe", False, args.source)
    ok &= check("filho web parado (atestado pelo chamador)", args.web_stopped or not args.apply,
                None if args.web_stopped else "passe --web-stopped depois de parar o processo")
    attested = args.operator_attests_only_heartbeat_wrote_after
    check("condicao D3c 'so o heartbeat gravou depois' — NAO verificavel por script", attested,
          "atestada pelo operador" if attested else "sem atestacao: duvida -> NAO restaurar")
    receipt["would_restore"] = bool(ok and attested)

    if not args.apply:
        print("dry-run: nada copiado. would_restore =", receipt["would_restore"])
    elif not (ok and attested):
        print("apply recusado: condicoes nao satisfeitas; nada copiado.")
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = args.target + ".bak_" + stamp
        receipt["backup_of_current"] = {"path": bak, "sha256": copy_bytes(args.target, bak)}
        if receipt["backup_of_current"]["sha256"] != args.expect_target_sha256:
            raise SystemExit("backup do alvo nao confere; abortado antes de tocar o alvo")
        tmp = args.target + ".tmp_restore_" + stamp
        if copy_bytes(args.source, tmp) != args.expect_source_sha256:
            os.remove(tmp); raise SystemExit("copia temporaria da fonte nao confere; alvo intocado")
        os.replace(tmp, args.target)
        final = meta(args.target); receipt["target_after"] = final
        receipt["restored"] = final["sha256"] == args.expect_source_sha256
        print("restaurado:", receipt["restored"], "sha16", final["sha256"][:16], "backup:", bak)
    os.makedirs(os.path.dirname(os.path.abspath(args.receipt)), exist_ok=True)
    with open(args.receipt, "w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=1)
    print("recibo:", os.path.abspath(args.receipt))
    return 0 if (ok or not args.apply) else 1


if __name__ == "__main__":
    sys.exit(main())
