p = "d_kernel.py"
t = open(p, encoding="utf-8").read()
bad_start = t.index('    for i, l in enumerate(Ec[rel].split("')
bad_end = t.index("# diff pedra x origem")
NL = chr(92) + "n"
good = ('    for i, l in enumerate(Ec[rel].split("' + NL + '")):\n'
        '        if re.search(r"' + chr(92) + 'bsorry' + chr(92) + 'b|^' + chr(92) + 's*axiom' + chr(92) + 'b|native_decide|' + chr(92) + 'bunsafe' + chr(92) + 'b|#eval|ofReduceBool|implemented_by|' + chr(92) + 'bextern' + chr(92) + 'b|@' + chr(92) + '[csimp' + chr(92) + ']|' + chr(92) + 'bopaque' + chr(92) + 'b", l): print("   ", rel, i + 1, l.strip()[:160])\n')
t = t[:bad_start] + good + t[bad_end:]
open(p, "w", encoding="utf-8", newline="\n").write(t)
