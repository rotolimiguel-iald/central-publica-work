import fs from 'node:fs';
import {pollingOptIn,restorePollingBytes} from './client_transport_adapter.mjs';
import {PROTOCOL,CODEC,QUERY} from './chat_wire_codec.mjs';
const checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
const session={account:'review_generation',transport:{protocol:PROTOCOL,codec:CODEC,query:QUERY,bases:false}};
check('native_probe_and_negotiated_optin',await pollingOptIn(session)===QUERY);
check('no_capabilities_no_optin',await pollingOptIn({account:session.account})===null);
const raw=new TextEncoder().encode('{"events":[]}');
check('plain_page_exact_identity',await restorePollingBytes(raw,session,'job1',0,null)===raw);
fs.writeFileSync(new URL('./review_adapter_node.json',import.meta.url),JSON.stringify({status:'PASS',checks}));
console.log(JSON.stringify({status:'PASS',assertions:checks.length}));
