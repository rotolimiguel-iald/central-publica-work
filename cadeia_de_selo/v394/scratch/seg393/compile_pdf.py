def compile_pdf(texname):
    """v184 [TRAVA DO PDF]: retorno TRI-ESTADO, para separar o que e' falha do que
    nao e'.  None = pdflatex AUSENTE (caminho gracioso: o .tex sai e quem nao tem
    TeX ainda reproduz o resto; o selo NAO pode depender do ambiente).  False =
    motor PRESENTE e o PDF NAO saiu -> FALHA REAL, e o chamador trava.  True = ok.
    Achado da v183: os dois retornos eram descartados e o selo avancava com o PDF
    ausente -- um passo que nao podia reprovar."""
    eng = shutil.which("pdflatex")
    if not eng:
        print("   [PDF] pdflatex ausente -> .tex gerado; compile com MiKTeX/TeX Live."); return None
    try:
        for _ in range(2):
            subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", texname + ".tex"],
                           cwd=OUT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        ok = os.path.exists(os.path.join(OUT, texname + ".pdf"))
        print("   [PDF] %s.pdf %s" % (texname, "OK" if ok else "FALHOU (ver %s.log)" % texname))
        return ok
    except Exception as e:
        print("   [PDF] erro:", e); return False