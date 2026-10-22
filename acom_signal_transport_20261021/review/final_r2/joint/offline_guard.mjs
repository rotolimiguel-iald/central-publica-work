import net from 'node:net';
import tls from 'node:tls';
import http from 'node:http';
import https from 'node:https';
import dns from 'node:dns';
import child from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
const deny=()=>{throw new Error('REVIEW_OFFLINE_ONLY');};
globalThis.fetch=deny;globalThis.WebSocket=class {constructor(){deny();}};
net.connect=net.createConnection=net.createServer=deny;net.Socket.prototype.connect=deny;
tls.connect=tls.createServer=deny;http.request=http.get=http.createServer=deny;https.request=https.get=https.createServer=deny;
for(const key of Object.keys(dns))if(typeof dns[key]==='function')dns[key]=deny;
for(const key of Object.keys(dns.promises))if(typeof dns.promises[key]==='function')dns.promises[key]=deny;
for(const key of ['spawnSync','exec','execSync','execFile','execFileSync','fork'])child[key]=deny;
syncBuiltinESMExports();

const originalSpawn=child.spawn;
child.spawn=(cmd,args,options)=>{if(cmd!=='C:/Python314/python.exe'||args.length!==4||args[0]!=='-B'||args[1]!=='-X'||args[2]!=='utf8'||!args[3].replaceAll('\\','/').endsWith('/review/final_r2/joint/flask_rpc.py'))deny();return originalSpawn(cmd,args,options);};
syncBuiltinESMExports();
