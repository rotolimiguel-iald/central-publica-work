p = "m_flags_audit.py"
t = open(p, encoding="utf-8").read()
t = t.replace("ext_tt409_", "ext_tu409_").replace("ext_tt408_", "ext_tu409_")
t = t.replace('print("flags base:", len(F6), "cand:", len(F7), "novas:", len(novas), "| base e\' sub-dict igual:", all(F7.get(k) == v for k, v in F6.items()), "| prefixo ext_tu409_:", all(k.startswith("ext_tu409_") for k in novas))',
              'print("flags base:", len(F6), "cand:", len(F7), "novas:", len(novas), "(esperado 158) | base e\' sub-dict igual:", all(F7.get(k) == v for k, v in F6.items()), "| prefixo ext_tu409_:", all(k.startswith("ext_tu409_") for k in novas))')
t = t.replace("os 9 modulos", "os 2 modulos").replace("nos 9 modulos", "nos 2 modulos").replace("os 44 bandeiras", "as 158 bandeiras").replace("as 42 ancoras", "as 82 ancoras")
open(p, "w", encoding="utf-8", newline="\n").write(t)
