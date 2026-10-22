def compile_pdf(texname):
    """v394 PDF tri-state, with explicit MiKTeX offline process options.

    None means pdflatex absent; False means an available engine failed; True
    means both engine passes returned zero and the output PDF exists. In TGL_NO_NETWORK=1 the executable is identified
    by its actual version output before the existing two compilation passes.
    MiKTeX gets options overriding its configuration/registry installer setting
    and disabling write18. This is not an OS network or filesystem sandbox.
    """
    eng = shutil.which("pdflatex")
    if not eng:
        print("   [PDF] pdflatex ausente -> .tex gerado; compile com MiKTeX/TeX Live.")
        return None
    try:
        offline_options = []
        if os.environ.get("TGL_NO_NETWORK") == "1":
            identity = subprocess.run(
                [eng, "--version"], cwd=OUT, capture_output=True,
                text=True, encoding="utf-8", errors="replace", timeout=15)
            if identity.returncode != 0:
                print("   [PDF] nao foi possivel identificar o motor offline.")
                return False
            if "miktex" in (identity.stdout + identity.stderr).lower():
                offline_options = ["--disable-installer", "--disable-write18"]
        for _ in range(2):
            compiled = subprocess.run(
                [eng] + offline_options +
                ["-interaction=nonstopmode", "-halt-on-error", texname + ".tex"],
                cwd=OUT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=180)
            if compiled.returncode != 0:
                print("   [PDF] motor terminou com codigo %s (ver %s.log)" %
                      (compiled.returncode, texname))
                return False
        ok = os.path.exists(os.path.join(OUT, texname + ".pdf"))
        print("   [PDF] %s.pdf %s" % (
            texname, "OK" if ok else "FALHOU (ver %s.log)" % texname))
        return ok
    except Exception as e:
        print("   [PDF] erro:", e)
        return False