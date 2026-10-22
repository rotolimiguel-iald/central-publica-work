def emit_article(core, verdict, data_path, lang):
    if lang == "pt":
        p = os.path.join(OUT, "um_absoluto_pt.tex")
        _tx = _tex_guard_nan(build_pt(core, verdict, data_path))
        _write_text_atomic(p, _tx)   # v376: escrita atomica
        _write_text_atomic(os.path.join(OUT, "um_absoluto_pt.txt"), _tex_to_txt(_tx))          # v168: PDF E TXT
        return p
    p = os.path.join(OUT, "um_absoluto_en.tex")
    _tx = _tex_guard_nan(build_en(core, verdict, data_path))
    _write_text_atomic(p, _tx)   # v376: escrita atomica
    _write_text_atomic(os.path.join(OUT, "um_absoluto_en.txt"), _tex_to_txt(_tx))              # v168: PDF E TXT
    return p