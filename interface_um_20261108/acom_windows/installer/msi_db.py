"""Small Windows Installer database writer. Uses only the native MSI API."""
from __future__ import annotations

import ctypes
import hashlib
import re
import uuid
from contextlib import contextmanager
from pathlib import Path

api = ctypes.WinDLL('msi')
W = ctypes.c_wchar_p
H = ctypes.c_uint32
P = ctypes.byref
for name, args in {
    'MsiOpenDatabaseW': [W, ctypes.c_void_p, ctypes.POINTER(H)],
    'MsiDatabaseImportW': [H, W, W],
    'MsiDatabaseOpenViewW': [H, W, ctypes.POINTER(H)],
    'MsiViewExecute': [H, H],
    'MsiRecordSetStringW': [H, H, W],
    'MsiRecordSetStreamW': [H, H, W],
    'MsiGetSummaryInformationW': [H, W, H, ctypes.POINTER(H)],
    'MsiSummaryInfoSetPropertyW': [H,H,H,ctypes.c_int,ctypes.c_void_p,W],
    'MsiSummaryInfoPersist': [H],
    'MsiDatabaseCommit': [H],
    'MsiCloseHandle': [H],
    'MsiCreateRecord': [H],
}.items():
    getattr(api,name).argtypes=args
    getattr(api,name).restype=H

def call(code, context):
    if code: raise RuntimeError(f'{context}: Windows Installer error {code}')

@contextmanager
def handle():
    h=H(0)
    try: yield h
    finally:
        if h.value: api.MsiCloseHandle(h)

def guid(label):
    return '{'+str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://iald.local/acom/test-windows/'+label)).upper()+'}'

def ident(prefix, name):
    return prefix+hashlib.sha256(name.encode()).hexdigest()[:25]

def short_name(name):
    if re.fullmatch(r'[\w-]{1,8}(\.[\w-]{1,3})?',name,re.ASCII):return name
    ext=re.sub(r'[^A-Z0-9]','',Path(name).suffix.upper())[:3]
    alias='A'+hashlib.sha256(name.encode()).hexdigest()[:7].upper()
    return alias+('.'+ext if ext else '')+'|'+name

# IDT schema is column names, native MSI column types, then primary key columns.
SCHEMA = {
 'Property':('Property Value','s72 l0','Property'),
 'Directory':('Directory Directory_Parent DefaultDir','s72 S72 l255','Directory'),
 'Component':('Component ComponentId Directory_ Attributes Condition KeyPath','s72 S38 s72 i2 S255 S72','Component'),
 'Feature':('Feature Feature_Parent Title Description Display Level Directory_ Attributes','s38 S38 L64 L255 I2 i2 S72 i2','Feature'),
 'FeatureComponents':('Feature_ Component_','s38 s72','Feature_ Component_'),
 'Registry':('Registry Root Key Name Value Component_','s72 i2 l255 L255 L0 s72','Registry'),
 'File':('File Component_ FileName FileSize Version Language Attributes Sequence','s72 s72 l255 i4 S72 S20 I2 i2','File'),
 'Media':('DiskId LastSequence DiskPrompt Cabinet VolumeLabel Source','i2 i2 L64 S255 S32 S72','DiskId'),
 'Shortcut':('Shortcut Directory_ Name Component_ Target Arguments Description Hotkey Icon_ IconIndex ShowCmd WkDir','s72 s72 l128 s72 s72 S255 L255 I2 S72 I2 I2 S72','Shortcut'),
 'InstallExecuteSequence':('Action Condition Sequence','s72 S255 I2','Action'),
 'AdminExecuteSequence':('Action Condition Sequence','s72 S255 I2','Action'),
 'RemoveFile':('FileKey Component_ FileName DirProperty InstallMode','s72 s72 L255 s72 i2','FileKey'),
 'Upgrade':('UpgradeCode VersionMin VersionMax Language Attributes Remove ActionProperty','s38 S20 S20 S255 i4 S255 s72','UpgradeCode VersionMin VersionMax Language Attributes'),
}

def write_msi(path, folder, files, cabinet, digest, version):
    dbrows={n:[] for n in SCHEMA}
    product=guid('product/'+version+'/'+digest)
    # Per-user product registration; one version at a time, since this pilot has no unattended upgrade policy.
    dbrows['Property']=[
        ('ProductName','ACOM · Bancada do Um (teste)'),('ProductVersion',version),
        ('ProductCode',product),('UpgradeCode',guid('upgrade')),('Manufacturer','IALD Ltda.'),
        ('ProductLanguage','1046'),('ARPNOMODIFY','1'),('ARPNOREPAIR','1'),
        ('INSTALLLEVEL','1'),('SecureCustomProperties','OLDACOMPRODUCTS'),
    ]
    dbrows['Directory']=[('TARGETDIR','','SourceDir'),('LocalAppDataFolder','TARGETDIR','.'),
                         ('ProgramsUnderLocal','LocalAppDataFolder','Programs'),('IALDRoot','ProgramsUnderLocal','IALD'),
                         ('APPDIR','IALDRoot','ACOM'),('ProgramMenuFolder','TARGETDIR','.')]
    dirs={'':'APPDIR'}
    def directory(name):
        if name not in dirs:
            p=Path(name)
            up=directory('' if p.parent==Path('.') else p.parent.as_posix())
            dirs[name]=ident('D',name)
            dbrows['Directory'].append((dirs[name],up,short_name(p.name)))
        return dirs[name]
    for seq,(rel,src) in enumerate(files,1):
        p=Path(rel); fid=ident('F',rel); cid=ident('C',rel)
        dirname=directory('' if p.parent==Path('.') else p.parent.as_posix())
        dbrows['File'].append((fid,cid,short_name(p.name),src.stat().st_size,'','',512,seq))
        dbrows['Component'].append((cid,guid('file/'+rel),dirname,256,'',fid))
        dbrows['FeatureComponents'].append(('Core',cid))
    dbrows['Media']=[(1,len(files),'','#payload.cab','','')]
    dbrows['Feature']=[('Core','','ACOM','Compactador e restaurador',1,1,'APPDIR',0),
                       ('Explorer','','Explorador','Integrar ao Explorador do Windows',2,2,'APPDIR',0)]
    wid=ident('F','runtime/pythonw.exe')
    run='"[#'+wid+']" -I -B "[APPDIR]app\\host.py" '
    regs={'Primary':('Software\\IALD\\ACOM','InstallDir','[APPDIR]'),
          'URL':('Software\\Classes\\iald-acom','','URL: IALD ACOM'),
          'URLMarker':('Software\\Classes\\iald-acom','URL Protocol',''),
          'URLCommand':('Software\\Classes\\iald-acom\\shell\\open\\command','',run+'protocol "%1"')}
    for feat, entries in [('Core',regs),('Explorer',{
          'OpenWith':('Software\\Classes\\.acom\\OpenWithProgids','IALD.ACOM.Archive.1',''),
          'ProgDescription':('Software\\Classes\\IALD.ACOM.Archive.1','','Arquivo ACOM'),
          'ProgName':('Software\\Classes\\IALD.ACOM.Archive.1\\Application','ApplicationName','ACOM - Bancada do Um'),
          'Registration':('Software\\RegisteredApplications','IALD ACOM','Software\\IALD\\ACOM\\Capabilities'),
          'Capabilities':('Software\\IALD\\ACOM\\Capabilities','ApplicationName','ACOM - Bancada do Um'),
          'CapabilityDescription':('Software\\IALD\\ACOM\\Capabilities','ApplicationDescription','Compactar e restaurar arquivos ACOM'),
          'FileAssociation':('Software\\IALD\\ACOM\\Capabilities\\FileAssociations','.acom','IALD.ACOM.Archive.1'),
          'ProgIcon':('Software\\Classes\\IALD.ACOM.Archive.1\\DefaultIcon','','[SystemFolder]shell32.dll,165'),
          'ProgCommand':('Software\\Classes\\IALD.ACOM.Archive.1\\shell\\open\\command','',run+'extract "%1"'),
          'ExplorerExtract':('Software\\Classes\\SystemFileAssociations\\.acom\\shell\\IALDACOMExtract','','Restaurar com ACOM'),
          'ExplorerExtractCommand':('Software\\Classes\\SystemFileAssociations\\.acom\\shell\\IALDACOMExtract\\command','',run+'extract "%1"'),
          'ExplorerPack':('Software\\Classes\\*\\shell\\IALDACOMPack','','Compactar com ACOM'),
          'ExplorerPackCommand':('Software\\Classes\\*\\shell\\IALDACOMPack\\command','',run+'pack "%1"'),
          'DirectoryPack':('Software\\Classes\\Directory\\shell\\IALDACOMPack','','Compactar pasta com ACOM'),
          'DirectoryPackCommand':('Software\\Classes\\Directory\\shell\\IALDACOMPack\\command','',run+'pack "%1"'),
         })]:
        cid='Reg'+feat
        dbrows['Component'].append((cid,guid('registry/'+feat),'APPDIR',260,'',next(iter(entries))))
        for key,(reg,name,value) in entries.items():
            dbrows['Registry'].append((key,1,reg,name,value,cid))
        dbrows['FeatureComponents'].append((feat,cid))
    dbrows['Shortcut']=[('Launcher','ProgramMenuFolder','IALDACOM|ACOM - Bancada do Um','RegCore',
                         '[#'+wid+']','-I -B "[APPDIR]app\\host.py" home','Abrir ACOM','','','','1','APPDIR')]
    dbrows['RemoveFile']=[('CleanupMenu','RegCore','','APPDIR',2)]
    dbrows['Upgrade']=[(guid('upgrade'),'',version,'',512,'','OLDACOMPRODUCTS')]
    dbrows['InstallExecuteSequence']=[(a,cond,s) for a,cond,s in [
        ('FindRelatedProducts','',25),('CostInitialize','',800),('FileCost','',900),('CostFinalize','',1000),('InstallValidate','',1400),
        ('InstallInitialize','',1500),('RemoveExistingProducts','OLDACOMPRODUCTS',1510),('ProcessComponents','',1600),('UnpublishFeatures','',1800),
        ('RemoveRegistryValues','',2600),('RemoveShortcuts','',3200),('RemoveFiles','',3500),('RemoveFolders','',3600),
        ('InstallFiles','',4000),('CreateShortcuts','',4500),('WriteRegistryValues','',5000),
        ('RegisterUser','',6000),('RegisterProduct','',6100),('PublishFeatures','',6300),('PublishProduct','',6400),
        ('InstallFinalize','',6600)]]
    dbrows['AdminExecuteSequence']=[(a,'',s) for a,s in [('CostInitialize',800),('FileCost',900),('CostFinalize',1000),
        ('InstallValidate',1400),('InstallInitialize',1500),('InstallAdminPackage',3900),('InstallFiles',4000),('InstallFinalize',6600)]]
    with handle() as db:
        call(api.MsiOpenDatabaseW(str(path),3,P(db)),'create database')
        for name,rows in dbrows.items():
            cols,types,keys=SCHEMA[name]
            lines=[cols.split(),types.split(),[name,*keys.split()],*rows]
            text='\r\n'.join('\t'.join(map(str,row)) for row in lines)+'\r\n'
            (folder/(name+'.idt')).write_bytes(text.encode('cp1252'))
            call(api.MsiDatabaseImportW(db,str(folder),name+'.idt'),f'import {name}')
        with handle() as info:
            call(api.MsiGetSummaryInformationW(db,None,12,P(info)),'summary')
            for property_id,value in [(1,1252),(2,'Installation Database'),(3,'ACOM'),(4,'IALD Ltda.'),
                                  (7,'x64;1046'),(9,guid('package/'+digest)),(14,500),(15,10),(18,'IALD ACOM Builder')]:
                typ=(2 if property_id==1 else 3) if isinstance(value,int) else 30
                call(api.MsiSummaryInfoSetPropertyW(info,property_id,typ,value if isinstance(value,int) else 0,None,value if isinstance(value,str) else None),'summary field')
            call(api.MsiSummaryInfoPersist(info),'persist summary')
        with handle() as view:
            call(api.MsiDatabaseOpenViewW(db,"INSERT INTO \x60_Streams\x60 (\x60Name\x60,\x60Data\x60) VALUES (?,?)",P(view)),'cabinet view')
            r=api.MsiCreateRecord(2)
            try:
                call(api.MsiRecordSetStringW(r,1,'payload.cab'),'name')
                call(api.MsiRecordSetStreamW(r,2,str(cabinet)),'embed cabinet')
                call(api.MsiViewExecute(view,r),'store cabinet')
            finally: api.MsiCloseHandle(r)
        call(api.MsiDatabaseCommit(db),'commit')
    return product

