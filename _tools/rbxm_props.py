"""Full-ish property reader for binary rbxm; dumps chosen classes as JSON. Read-only."""
import struct, sys, json, collections
exec(open(sys.argv[0].replace('rbxm_props.py','rbxm_lib.py')).read())
def rfloat(b):
    v = struct.unpack('>I', b)[0]
    v = ((v >> 1) | ((v & 1) << 31)) & 0xffffffff
    return struct.unpack('>f', struct.pack('>I', v))[0]
def rint(b):
    return rot_i32(b)

def parse_values(t, body, p, n):
    out = []
    if t == 0x01:
        for _ in range(n):
            sl, = struct.unpack('<I', body[p:p+4]); p += 4
            s = body[p:p+sl]; p += sl
            try: out.append(s.decode())
            except: out.append('<bin>')
    elif t == 0x02:
        out = [bool(x) for x in body[p:p+n]]; p += n
    elif t == 0x03:
        out = [rint(b) for b in deinterleave(body[p:p+4*n], n)]; p += 4*n
    elif t == 0x04:
        out = [round(rfloat(b), 5) for b in deinterleave(body[p:p+4*n], n)]; p += 4*n
    elif t == 0x05:
        out = list(struct.unpack('<%dd' % n, body[p:p+8*n])); p += 8*n
    elif t in (0x0C, 0x0D, 0x0E):
        k = {0x0C: 3, 0x0D: 2, 0x0E: 3}[t]
        cols = []
        for _ in range(k):
            cols.append([round(rfloat(b), 5) for b in deinterleave(body[p:p+4*n], n)]); p += 4*n
        out = [list(x) for x in zip(*cols)]
    elif t == 0x12:
        out = [struct.unpack('>I', b)[0] for b in deinterleave(body[p:p+4*n], n)]; p += 4*n
    elif t == 0x15:
        for _ in range(n):
            c, = struct.unpack('<I', body[p:p+4]); p += 4
            ks = [list(struct.unpack('<3f', body[p+12*i:p+12*i+12])) for i in range(c)]; p += 12*c
            out.append([[round(x, 4) for x in k] for k in ks])
    elif t == 0x16:
        for _ in range(n):
            c, = struct.unpack('<I', body[p:p+4]); p += 4
            ks = [list(struct.unpack('<5f', body[p+20*i:p+20*i+20])) for i in range(c)]; p += 20*c
            out.append([[round(x, 4) for x in k] for k in ks])
    elif t == 0x17:
        for _ in range(n):
            out.append([round(x, 4) for x in struct.unpack('<2f', body[p:p+8])]); p += 8
    elif t == 0x19:
        r = body[p:p+n]; g = body[p+n:p+2*n]; b = body[p+2*n:p+3*n]; p += 3*n
        out = [[r[i]/255, g[i]/255, b[i]/255] for i in range(n)]
    else:
        return None, p
    return out, p

data = open(sys.argv[1], 'rb').read()
want = set(sys.argv[2].split(','))
pos = 32; classes = {}; props = collections.defaultdict(dict); parent = {}
while pos < len(data):
    name = data[pos:pos+4].rstrip(b'\0').decode(); clen, ulen = struct.unpack('<II', data[pos+4:pos+12]); pos += 16
    if clen == 0: body = data[pos:pos+ulen]; pos += ulen
    else: body = lz4_block(data[pos:pos+clen], ulen); pos += clen
    if name == 'INST':
        cid, = struct.unpack('<I', body[:4]); ln, = struct.unpack('<I', body[4:8])
        cname = body[8:8+ln].decode(); p = 8+ln+1
        cnt, = struct.unpack('<I', body[p:p+4]); p += 4
        refs, p = read_refs(body, p, cnt); classes[cid] = (cname, refs)
    elif name == 'PROP':
        cid, = struct.unpack('<I', body[:4]); ln, = struct.unpack('<I', body[4:8])
        pname = body[8:8+ln].decode(); p = 8+ln; t = body[p]; p += 1
        cname, refs = classes[cid]
        if cname in want or pname == 'Name':
            vals, p = parse_values(t, body, p, len(refs))
            if vals is not None:
                for r, v in zip(refs, vals): props[r][pname] = v
    elif name == 'PRNT':
        cnt, = struct.unpack('<I', body[1:5]); p = 5
        ch, p = read_refs(body, p, cnt); pa, p = read_refs(body, p, cnt)
        for c, a in zip(ch, pa): parent[c] = a
    elif name == 'END': break
cls_of = {r: c for c, rs in classes.values() for r in rs}
def path(r):
    parts = []
    while r is not None and r >= 0:
        parts.append(props[r].get('Name', '?')); r = parent.get(r)
    return '/'.join(reversed(parts))
out = []
for r, c in cls_of.items():
    if c in want:
        d = dict(props[r]); d['_class'] = c; d['_path'] = path(r); d['_ref'] = r
        out.append(d)
json.dump(out, open(sys.argv[3], 'w'), indent=0)
print(len(out), 'objects ->', sys.argv[3])
