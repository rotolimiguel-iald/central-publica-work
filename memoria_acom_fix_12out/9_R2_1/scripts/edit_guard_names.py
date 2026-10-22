# -*- coding: utf-8 -*-
"""R2.1: troca a camada de NOMES do guard.py do candidato_r2_1 (bytes LF preservados)."""
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'candidato_r2_1' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'guard.py'
s = P.read_bytes().decode('utf-8')
a = s.index("_STRIP_SUFFIX = re.compile(")
b = s.index("def escritorio_component(path):")
new = r'''# R2.1 (13/10/2026, review N2 and the review-B name gaps): the name rules run on a SKELETON of the name.
# NFKC alone does not map Cyrillic/Greek look-alikes (U+0455 'ѕ' stays 'ѕ'), so the common ones are mapped
# explicitly, Unicode dashes become '-', and format characters (zero-width, soft hyphen, bidi marks) vanish.
_DASHES = '‐‑‒–—―⁃−﹘﹣－'
_CONFUSABLE_SRC = ('аеорсухѕіјԁһӏԛԝ'
                   'үкмнтвɡıɑ'
                   'αικνορτυχϲϳ'
                   'օս')
_CONFUSABLE_DST = ('aeopcyxsijdhlqw'
                   'ykmhtbgia'
                   'aikvoptuxcj'
                   'ou')
_SKELETON_MAP = str.maketrans(dict({ord(d): '-' for d in _DASHES},
                                   **{ord(c): t for c, t in zip(_CONFUSABLE_SRC, _CONFUSABLE_DST)}))
assert len(_CONFUSABLE_SRC) == len(_CONFUSABLE_DST)


def skeleton(value):
    """NFKC, format characters removed, casefold, look-alikes and dashes mapped to ASCII, accents stripped."""
    text = unicodedata.normalize('NFKC', str(value))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Cf').casefold().translate(_SKELETON_MAP)
    return fold(text)


_SUFFIX_WORDS = frozenset(('bak', 'backup', 'tmp', 'temp', 'orig', 'old', 'save', 'swp', 'copy'))
# One dot-free segment that is a backup/temp suffix: `bak`, `bak_20261013`, `tmp-x` ...
_SUFFIX_SEGMENT = re.compile(r'(?:bak|backup|tmp|temp|orig|old|save|swp|copy)(?:[_\-][^.]*)?')
_SEP = r'[\W_]{0,4}'
_NAME_RULES = (
    ('psion_name', re.compile(r'iald' + _SEP + r'psion' + _SEP + r'state')),      # radical, anywhere (R2.1)
    ('stack_name', re.compile(r'iald' + _SEP + r'stack' + _SEP + r'v')),           # radical, anywhere (R2.1)
    ('dotenv_name', re.compile(r'(?:\A|\.)env(?:rc)?(?:\Z|[._\-])')),             # .env, prod.env, .env.local, x.env_prod
    ('key_name', re.compile(r'\A.+\.key(?:\.|\Z)')),
    ('pem_name', re.compile(r'\A.+\.pem(?:\.|\Z)')),
)


def normalized_basename(name):
    """Skeleton of the basename with backup/temp suffixes (and trailing '~') removed repeatedly.

    R2.1 (review N1): same decision as the R2 loop `re.sub(r'\.(?:bak|...)(?:[_.\-][^.]*)?\Z', '', base)` repeated
    until stable (plus trailing '~'), but walking back from the end over at most the last two dot segments per
    step: every character is visited a bounded number of times, so the cost is LINEAR in the name (the R2 loop
    re-scanned the whole name once per suffix: 32 KB of '.bak' took seconds).
    """
    base = skeleton(name)
    end = len(base)
    while end > 0:
        tilde = end
        while tilde > 0 and base[tilde - 1] == '~':
            tilde -= 1
        if tilde != end:
            if tilde == 0:
                break
            end = tilde
            continue
        p1 = base.rfind('.', 0, end)
        if p1 < 0:
            break
        cut = None
        p2 = base.rfind('.', 0, p1)
        if p2 >= 0 and base[p2 + 1:p1] in _SUFFIX_WORDS:
            cut = p2        # '.<word>.<rest without dot>' (the leftmost match of the R2 pattern)
        elif _SUFFIX_SEGMENT.fullmatch(base, p1 + 1, end):
            cut = p1        # '.<word>' or '.<word>[_-]<rest without dot>'
        if cut is None or cut == 0:
            break           # nothing to strip, or the whole name is a suffix (kept, as in R2)
        end = cut
    return base[:end]


def confidential_basename(name):
    """Rule name when `name` (a basename) is a confidential file name, else None."""
    base = normalized_basename(name)
    for rule, pattern in _NAME_RULES:
        if pattern.search(base):
            return rule
    return None


'''
s = s[:a] + new + s[b:]
s = s.replace("        if fold(part).startswith('escritorio'):", "        if skeleton(part).startswith('escritorio'):")
assert "if skeleton(part).startswith('escritorio')" in s
P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)
