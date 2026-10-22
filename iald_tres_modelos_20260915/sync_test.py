from pathlib import Path
from datetime import datetime
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
data=(WORK/'test_two_models.py').read_bytes()
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for path in [ROOT/'tests/test_two_models.py',WORK/'stage/tests/test_two_models.py']:
    before=path.read_bytes()
    assert b"self.assertEqual(chunks[1:],original)" in before
    backup=path.with_name(path.name+'.bak_'+stamp)
    with backup.open('xb') as f:f.write(before)
    temp=path.with_name(path.name+'.tmp_'+stamp)
    with temp.open('xb') as f:f.write(data)
    assert path.read_bytes()==before and temp.read_bytes()==data
    temp.replace(path)
print('Focused stream test updated to verify bytes and unchanged number of yields.')
