import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createSessionTransport} from './iald_transport.mjs';
import {PROTOCOL,CODEC,QUERY} from './chat_wire_codec.mjs';
const raw=fs.readFileSync(new URL('../legacy_page.json',import.meta.url));
const page=JSON.parse(raw);assert.equal(page.cursor,2);assert.equal(page.events.length,2);
const transport=await createSessionTransport({account:'a'.repeat(64),transport:{protocol:PROTOCOL,codec:CODEC,query:QUERY,bases:false}});
assert(transport);
let error;
try{await transport.readPage(new Response(raw),{kind:'page',job_id:page.id,after:0});}catch(e){error=e.code;}
assert.equal(error,'page_wire_limit');
const result={reproduced:true,ordinary_legacy_parse:'PASS',negotiated_reader:error,bytes:raw.length,events_lost_to_reader:2,network_calls:0};
fs.writeFileSync(new URL('../LEGACY_PAGE_RESULT.json',import.meta.url),JSON.stringify(result,null,2));
console.log(JSON.stringify(result));
