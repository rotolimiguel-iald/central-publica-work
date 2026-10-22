import json, hashlib

def digest(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def pack(text, max_rules=250):
    if any(0xE000<=ord(c)<=0xEFFF for c in text): raise ValueError("Reserved reference marker in source")
    body=text; rules=[]
    for k in range(max_rules):
        positions={}; candidates=set()
        for i in range(0,len(body)-16):
            key=body[i:i+16]; prior=positions.get(key)
            if prior is not None and i-prior>=16:
                n=16
                while n<min(6000,i-prior,len(body)-i) and body[prior+n]==body[i+n]: n+=1
                candidates.add(body[i:i+n])
            else: positions[key]=i
        best=None; gain=0
        for s in candidates:
            count=body.count(s); saved=(count-1)*len(s)-count*1-12
            if saved>gain: best=s;gain=saved
        if gain<12: break
        token=chr(0xE000+k); body=body.replace(best,token);rules.append([token,best])
    meta={"schema":"iald.lossless-inline/v1","source_sha256":digest(text),"source_chars":len(text),"rule_lengths":[[t,len(v)] for t,v in rules],"body_chars":len(body)}
    wire="LOSSLESS INLINE REFERENCES. Expand rule tokens newest first recursively; content and instruction priority remain unchanged. Rules and body are literal Unicode, length-delimited. No external lookup required.\n"+json.dumps(meta,ensure_ascii=False,separators=(",",":"))+"\n"
    for token,value in rules: wire+=token+"\n"+value+"\n"
    wire+="BODY\n"+body
    if unpack(wire)!=text: raise ValueError("Roundtrip failed")
    return wire

def unpack(wire):
    _,rest=wire.split("\n",1); metadata,rest=rest.split("\n",1);data=json.loads(metadata);rules=[]
    for token,n in data['rule_lengths']:
        prefix=token+"\n"
        if not rest.startswith(prefix):raise ValueError("Rule marker mismatch")
        rest=rest[len(prefix):];value=rest[:n];rest=rest[n:]
        if not rest.startswith("\n"):raise ValueError("Rule length mismatch")
        rest=rest[1:];rules.append((token,value))
    if not rest.startswith("BODY\n"):raise ValueError("Body marker missing")
    body=rest[5:]
    if len(body)!=data['body_chars']:raise ValueError("Body length mismatch")
    for token,value in reversed(rules): body=body.replace(token,value)
    if len(body)!=data["source_chars"] or digest(body)!=data["source_sha256"]: raise ValueError("Source pin mismatch")
    return body
