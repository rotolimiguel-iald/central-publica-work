"""Append-only research route ledger. No model, shell or scientific execution."""
from contextlib import contextmanager, closing
from datetime import datetime, timezone
import hashlib,json,sqlite3,uuid
from pathlib import Path

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def now():return datetime.now(timezone.utc).isoformat()

class Routes:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS routes(id TEXT PRIMARY KEY, fingerprint TEXT UNIQUE NOT NULL,
                created TEXT NOT NULL, record TEXT NOT NULL, sha256 TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,
                route_id TEXT NOT NULL REFERENCES routes(id), created TEXT NOT NULL,
                state TEXT NOT NULL, body TEXT NOT NULL, sha256 TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS claims(route_id TEXT PRIMARY KEY REFERENCES routes(id),created TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS legacy(id TEXT PRIMARY KEY, source TEXT NOT NULL,
                source_key TEXT NOT NULL, record TEXT NOT NULL, sha256 TEXT NOT NULL);
            ''')
            for table in ('routes','events','claims','legacy'):
                for verb in ('UPDATE','DELETE'):
                    db.execute(f"CREATE TRIGGER IF NOT EXISTS {table}_no_{verb.lower()} BEFORE {verb} ON {table} BEGIN SELECT RAISE(ABORT,'Research records are append-only'); END")

    @contextmanager
    def db(self):
        db=sqlite3.connect(self.path,timeout=10);db.row_factory=sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys=ON');db.execute('PRAGMA synchronous=FULL')
            with db:yield db
        finally:db.close()

    def plan(self,operation,parameters,provenance,objective,hypothesis,falsifier,parent_id=None):
        fingerprint=digest({'schema':1,'operation':operation,'parameters':parameters,'provenance':provenance})
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            old=db.execute('SELECT id FROM routes WHERE fingerprint=?',(fingerprint,)).fetchone()
            if old:return self.get(old['id']),True
            if parent_id and not (db.execute('SELECT 1 FROM routes WHERE id=?',(parent_id,)).fetchone()
                    or db.execute('SELECT 1 FROM legacy WHERE id=?',(parent_id,)).fetchone()):
                raise ValueError('Unknown parent route')
            record=dict(id=uuid.uuid4().hex,operation=operation,parameters=parameters,provenance=provenance,
                objective=objective,hypothesis=hypothesis,falsifier=falsifier,parent_id=parent_id,
                fingerprint=fingerprint,created=now(),owner='luiz',scope='RESEARCH_NOT_CANON_RATIFICATION')
            body=canonical(record)
            db.execute('INSERT INTO routes VALUES(?,?,?,?,?)',(record['id'],fingerprint,record['created'],body,hashlib.sha256(body.encode()).hexdigest()))
            self._event(db,record['id'],'PLANNED',{'notice':'Parameters and provenance frozen before execution.'})
        return self.get(record['id']),False

    def _event(self,db,identifier,state,value):
        body=canonical(value)
        db.execute('INSERT INTO events(route_id,created,state,body,sha256) VALUES(?,?,?,?,?)',
            (identifier,now(),state,body,hashlib.sha256(body.encode()).hexdigest()))

    def event(self,identifier,state,value):
        with self.db() as db:self._event(db,identifier,state,value)

    def claim(self,identifier):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            if not db.execute('SELECT 1 FROM routes WHERE id=?',(identifier,)).fetchone():raise ValueError('Unknown route')
            if db.execute('SELECT 1 FROM claims WHERE route_id=?',(identifier,)).fetchone():return False
            latest=db.execute('SELECT state FROM events WHERE route_id=? ORDER BY id DESC LIMIT 1',(identifier,)).fetchone()
            if not latest or latest['state']!='PLANNED':return False
            # A crash/timeout in another process can leave the resident backend busy.
            # Never dispatch another computation merely because this process has no Future.
            if db.execute("SELECT 1 FROM claims c JOIN events e ON e.id=(SELECT MAX(id) FROM events WHERE route_id=c.route_id) WHERE e.state IN ('DISPATCHING','UNCERTAIN','RESULT_RECEIVED','PENDING_BACKEND') LIMIT 1").fetchone():
                raise ValueError('An unresolved computation requires reconciliation')
            db.execute('INSERT INTO claims VALUES(?,?)',(identifier,now()))
            self._event(db,identifier,'DISPATCHING',{'notice':'Durable claim; never resend this route automatically.'})
        return True

    def stale_unclaimed(self,identifier):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            latest=db.execute('SELECT state FROM events WHERE route_id=? ORDER BY id DESC LIMIT 1',(identifier,)).fetchone()
            if not latest or latest['state']!='PLANNED' or db.execute('SELECT 1 FROM claims WHERE route_id=?',(identifier,)).fetchone():
                return False
            self._event(db,identifier,'STALE_PLAN',{'notice':'Data or code changed before claim; no dispatch.'})
        return True

    def historical_matches(self,operation,parameters,normalize,provenance):
        """Only byte-pinned old scalar calculations are eligible for exact reuse.

        Missing engine/input pins are explicitly candidates, never asserted identical.
        Other historic domains remain searchable, without inventing equivalence.
        """
        if operation not in ('identity_chain','dephasing'):return []
        pins={x['source']:x['sha256'] for section in ('executors','inputs') for x in provenance.get(section,[])}
        matches=[]
        with self.db() as db:
            for row in db.execute("SELECT * FROM legacy WHERE source='runs.sqlite3:runs'"):
                r=self._decode(row);old=r['original']
                if old.get('operation')!=operation:continue
                args=json.loads(old['parameters_json']);args.pop('operation',None)
                if canonical(normalize(operation,args))!=canonical(parameters):continue
                result=json.loads(old['result_json'])
                exact=bool(pins.get('bench/app.py') and pins.get('TGL_ATLAS.md') and pins.get('historical_v368/estrutura_v368.json')
                    and result.get('engine_sha256')==pins['bench/app.py'] and result.get('atlas_sha256')==pins['TGL_ATLAS.md']
                    and old.get('source_sha256')==pins['historical_v368/estrutura_v368.json'])
                matches.append({'route_id':r['id'],'same_parameters':True,'same_recorded_sources':exact,
                    'scope':'Recorded disk hashes only; old live process generation not attested.'})
        return matches

    def _decode(self,row,field='record'):
        raw=row[field]
        if hashlib.sha256(raw.encode()).hexdigest()!=row['sha256']:raise ValueError('Research ledger integrity mismatch')
        return json.loads(raw)

    def get(self,identifier):
        if not isinstance(identifier,str) or len(identifier)>100:raise ValueError('Invalid route identifier')
        with self.db() as db:
            row=db.execute('SELECT * FROM routes WHERE id=?',(identifier,)).fetchone()
            if row:
                record=self._decode(row)
                events=[dict(id=e['id'],created=e['created'],state=e['state'],body=self._decode(e,'body'))
                    for e in db.execute('SELECT * FROM events WHERE route_id=? ORDER BY id',(identifier,))]
                return dict(record=record,events=events,state=events[-1]['state'] if events else 'PLANNED')
            row=db.execute('SELECT * FROM legacy WHERE id=?',(identifier,)).fetchone()
            if row:return {'record':self._decode(row),'state':'IMPORTED_HISTORICAL','events':[]}
        raise ValueError('Unknown research route')

    def search(self,query='',offset=0,limit=20):
        if type(query)is not str or len(query)>200 or type(offset)is not int or not 0<=offset<=100000 or type(limit)is not int or not 1<=limit<=30:
            raise ValueError('Invalid map search')
        with self.db() as db:
            needle='%'+query.replace('!','!!').replace('%','!%').replace('_','!_')+'%'
            rows=db.execute("SELECT id,record,'route' kind FROM routes WHERE record LIKE ? ESCAPE '!' UNION ALL SELECT id,record,'historical' kind FROM legacy WHERE record LIKE ? ESCAPE '!' ORDER BY id LIMIT ? OFFSET ?",(needle,needle,limit+1,offset)).fetchall()
            counts={table:db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('routes','legacy','events')}
        records=[]
        for row in rows[:limit]:
            full=self.get(row['id']);r=full['record']
            records.append({k:r.get(k) for k in ('id','operation','objective','parent_id','created','fingerprint','source_links')}|{'state':full['state'],'kind':row['kind']})
        return dict(nodes=records,counts=counts,next_offset=offset+limit if len(rows)>limit else None,
            coverage='Chat research routes plus imported available bench records; not all historical scientific work.')

    def import_history(self,bench):
        """Read originals, preserve every record; source changes are separate nodes."""
        bench=Path(bench);records=[];coverage=[]
        for filename,tables in [('runs.sqlite3',('runs','inquiries','inquiry_events')),('cosmology_scenarios.sqlite3',('scenarios',))]:
            path=bench/'state'/filename
            if not path.is_file():coverage.append({'source':filename,'status':'ABSENT'});continue
            with closing(sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)) as source:
                source.row_factory=sqlite3.Row
                for table in tables:
                    if not source.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(table,)).fetchone():
                        coverage.append({'source':filename+':'+table,'status':'TABLE_ABSENT'});continue
                    for row in source.execute('SELECT * FROM '+table):
                        item=dict(row);key=str(item['id'])
                        records.append((filename+':'+table,key,item))
            coverage.append({'source':filename,'status':'READ_ONLY_IMPORTED'})
        folder=bench/'state/resident_runs'
        if folder.is_dir():
            for path in sorted(folder.glob('*.json')):
                if path.stat().st_size>32*1024**2:raise ValueError('Historical receipt exceeds admitted size')
                records.append(('resident_runs',path.name,json.loads(path.read_bytes())))
            coverage.append({'source':'resident_runs','status':'READ_ONLY_IMPORTED'})
        inserted=0
        identities={(source,key):uuid.uuid5(uuid.NAMESPACE_URL,source+':'+key+':'+digest(item)).hex for source,key,item in records}
        with self.db() as db:
            for source,key,item in records:
                source_hash=digest(item);identifier=uuid.uuid5(uuid.NAMESPACE_URL,source+':'+key+':'+source_hash).hex
                record=dict(id=identifier,operation=item.get('operation',source),created=item.get('created_utc',item.get('created_at_utc')),
                    objective=item.get('question',source+':'+key),source=source,source_key=key,source_sha256=source_hash,
                    original=item,scope='HISTORICAL_RECORD_NOT_REEXECUTED')
                if source=='runs.sqlite3:inquiry_events':
                    record['source_links']=[{'relation':field,'route_id':identities.get(('runs.sqlite3:inquiries',str(item[field]))),
                        'original_inquiry_id':item[field]} for field in ('inquiry_id','related_inquiry_id') if item.get(field) is not None]
                body=canonical(record)
                inserted+=db.execute('INSERT OR IGNORE INTO legacy VALUES(?,?,?,?,?)',
                    (identifier,source,key,body,hashlib.sha256(body.encode()).hexdigest())).rowcount
        return {'inserted':inserted,'sources':coverage,'records_read':len(records)}
