// Pure staging adapter. Existing fetchIALD owns auth, cookies/CSRF and actual fetch.
import {PROTOCOL,CODEC,QUERY,codecAvailable,decodePage,WireError} from './chat_wire_codec.mjs';
export async function pollingOptIn(session){
 const c=session?.transport;
 return c?.protocol===PROTOCOL&&c.codec===CODEC&&c.bases===false&&c.query===QUERY&&await codecAvailable()?QUERY:null;
}
export async function restorePollingBytes(raw,session,jobId,after,optIn){
 if(optIn!==QUERY)return raw;
 if(!session?.account||!await codecAvailable())throw new WireError('negotiation_unavailable');
 return decodePage(raw,session.account,{kind:'page',job_id:jobId,after});
}
// Use sendOnce/prepareRequest from codec for POST. No retry handler is introduced.
