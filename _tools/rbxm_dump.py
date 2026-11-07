"""Offline reader for binary .rbxm: class counts, tree, string props, script sources. Read-only."""
import struct, sys, json, collections

def lz4_block(src, out_len):
    dst = bytearray(); i = 0; n = len(src)
    while i < n:
        tok = src[i]; i += 1
        lit = tok >> 4
        if lit == 15:
            while True:
                b = src[i]; i += 1; lit += b
                if b != 255: break
        dst += src[i:i+lit]; i += lit
        if i >= n: break
        off = src[i] | (src[i+1] << 8); i += 2
        ml = tok & 15
        if ml == 15:
            while True:
                b = src[i]; i += 1; ml += b
                if b != 255: break
        ml += 4
        start = len(dst) - off
        for k in range(ml):
            dst.append(dst[start + k])
    return bytes(dst)

def deinterleave(buf, count, width=4):
    out = []
    for i in range(count):
        out.append(bytes(buf[j*count + i] for j in range(width)))
    return out

def rot_i32(b):
    v = struct.unpack('>I', b)[0]
    return (v >> 1) ^ (-(v & 1))

def read_refs(buf, pos, count):
    raw = buf[pos:pos+4*count]
    vals = [rot_i32(b) for b in deinterleave(raw, count)]
    acc = 0; out = []
    for v in vals:
        acc += v; out.append(acc)
    return out, pos + 4*count

data = open(sys.argv[1], 'rb').read()
assert data[:8] == b'<roblox!', 'not binary rbxm'
pos = 32
classes = {}   # id -> (name, refs)
props = collections.defaultdict(dict)  # ref -> {prop: value}
parent = {}
while pos < len(data):
    name = data[pos:pos+4].rstrip(b'\0').decode(); clen, ulen = struct.unpack('<II', data[pos+4:pos+12]); pos += 16
    if clen == 0:
        body = data[pos:pos+ulen]; pos += ulen
    else:
        comp = data[pos:pos+clen]; pos += clen
        if comp[:4] == b'\x28\xb5\x2f\xfd':
            raise SystemExit('zstd chunk: need zstd decoder')
        body = lz4_block(comp, ulen)
    if name == 'INST':
        cid, = struct.unpack('<I', body[:4]); ln, = struct.unpack('<I', body[4:8])
        cname = body[8:8+ln].decode(); p = 8+ln+1
        cnt, = struct.unpack('<I', body[p:p+4]); p += 4
        refs, p = read_refs(body, p, cnt)
        classes[cid] = (cname, refs)
    elif name == 'PROP':
        cid, = struct.unpack('<I', body[:4]); ln, = struct.unpack('<I', body[4:8])
        pname = body[8:8+ln].decode(); p = 8+ln
        t = body[p]; p += 1
        cname, refs = classes[cid]
        if t == 0x01:  # String
            for r in refs:
                sl, = struct.unpack('<I', body[p:p+4]); p += 4
                s = body[p:p+sl]; p += sl
                try: s = s.decode('utf-8')
                except UnicodeDecodeError: s = '<binary %d bytes>' % len(s)
                props[r][pname] = s
    elif name == 'PRNT':
        cnt, = struct.unpack('<I', body[1:5]); p = 5
        ch, p = read_refs(body, p, cnt)
        pa, p = read_refs(body, p, cnt)
        for c, a in zip(ch, pa): parent[c] = a
    elif name == 'END':
        break

cls_of = {}
for cid, (cname, refs) in classes.items():
    for r in refs: cls_of[r] = cname

def path(r):
    parts = []
    while r is not None and r >= 0:
        parts.append(props[r].get('Name', '?') + ':' + cls_of.get(r, '?'))
        r = parent.get(r)
    return '/'.join(reversed(parts))

mode = sys.argv[2] if len(sys.argv) > 2 else 'summary'
if mode == 'summary':
    cnt = collections.Counter(cls_of.values())
    print('CLASSES:', dict(cnt.most_common()))
    scripts = [r for r, c in cls_of.items() if c in ('Script', 'LocalScript', 'ModuleScript')]
    print('SCRIPTS:', len(scripts))
    for r in scripts:
        src = props[r].get('Source', '')
        print('---', path(r), len(src), 'chars')
elif mode == 'sources':
    for r, c in cls_of.items():
        if c in ('Script', 'LocalScript', 'ModuleScript'):
            print('=====', path(r)); print(props[r].get('Source', ''))
elif mode == 'tree':
    for r in sorted(cls_of, key=path):
        extra = {k: v for k, v in props[r].items() if k in ('Texture', 'MeshId', 'TextureID', 'TextureId', 'SoundId')}
        print(path(r), json.dumps(extra) if extra else '')
