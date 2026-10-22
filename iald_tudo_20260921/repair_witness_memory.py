"""Preserve source construction layers and their exact scope in the draft."""
from pathlib import Path
from datetime import datetime

WORK = Path(__file__).resolve().parent

def replace_exact(name, old, new):
    path = WORK / name
    raw = path.read_bytes()
    before = old.replace('\n', '\r\n').encode() if b'\r\n' in raw else old.encode()
    after = new.replace('\n', '\r\n').encode() if b'\r\n' in raw else new.encode()
    assert raw.count(before) == 1, name
    updated = raw.replace(before, after)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(raw)
    assert backup.read_bytes() == raw
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(updated)
    assert temp.read_bytes() == updated and len(updated) > len(raw)
    assert path.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == updated

replace_exact('build_haiku_candidate.py',
    'def capsule(value, pointer, depth=0):\n',
    '''def capsule(value, pointer, depth=0):
    # These records distinguish constructed regular witnesses from the specific
    # canonical target. Dropping them leaves historical negatives unbalanced.
    if pointer in ('/core/interface_is_light/witness_layers',
                   '/core/interface_is_light/light_chain'):
        return value
''')
replace_exact('test_haiku_source_contract.py',
    '    def test_only_boolean_audit_rows_are_externalized(self):\n',
    '''    def test_interface_construction_layers_and_light_chain_survive(self):
        self.assert_source_subtree('/core/interface_is_light/witness_layers')
        self.assert_source_subtree('/core/interface_is_light/light_chain')

    def test_only_boolean_audit_rows_are_externalized(self):
''')
print('Draft builder and independent source contract updated; originals untouched.')
