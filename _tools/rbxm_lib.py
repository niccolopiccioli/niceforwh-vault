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

