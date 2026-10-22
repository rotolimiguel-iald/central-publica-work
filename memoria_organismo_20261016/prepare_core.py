"""Pin the exact existing core before editing isolated candidates."""
from mission_io import WORK, CORE, pin, save

files = ['__init__.py', 'guard.py', 'journal.py', 'migrate.py', 'mission.py', 'snapshots.py', 'store.py']
save(WORK/'CORE_BASELINE.json', [pin(CORE/'lib'/'iald_memory'/name) for name in files])
print('Core baseline recorded; originals unchanged.')
