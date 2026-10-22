"""One executor per SQLite queue, including when the MCP and web share it."""
from contextlib import contextmanager
import os
import time

@contextmanager
def process_lock(path,blocking=True):
    with open(str(path)+'.worker.lock','a+b') as file:
        file.seek(0,2)
        if file.tell()==0:file.write(b'0');file.flush()
        acquired=False
        try:
            while not acquired:
                try:
                    file.seek(0)
                    if os.name=='nt':
                        import msvcrt
                        msvcrt.locking(file.fileno(),msvcrt.LK_NBLCK,1)
                    else:
                        import fcntl
                        fcntl.flock(file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
                    acquired=True
                except OSError:
                    if not blocking:break
                    time.sleep(.1)
            yield acquired
        finally:
            if acquired:
                file.seek(0)
                if os.name=='nt':
                    import msvcrt
                    msvcrt.locking(file.fileno(),msvcrt.LK_UNLCK,1)
                else:
                    import fcntl
                    fcntl.flock(file.fileno(),fcntl.LOCK_UN)
