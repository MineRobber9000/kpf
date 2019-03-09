# kpf v0.2.0 Spec

kpf is a specification for patch files. These files define modifications to be made to a binary file, usually a game ROM.

These specs will be semantically versioned, if you like that.

## Why bother?

One question I anticipate is "why"? IPS, BPS, and other formats exist for expressing patch information. So why reinvent the wheel?

### Fun

This reason is the least compelling. It's fun to imagine a system. I can come up with a standard and at least use it myself.

### Addressing limitations

Binary patch files can only do so much. There's only so much information you can fit in a binary format without specifying length bytes and the like.

Also, to the best of my knowledge, no current patch format can specify multiple patches in one file.

### Ease of reading (for humans)

Let's be honest. Which is easier to read, this:

```
00000000: 5041 5443 4800 0002 0001 0245 4f46       PATCH......EOF
```

Or:

```
.patch
.name Set byte 2 to 2
000002=02
.endpatch
```

I personally think it's quite obvious which is easier to read. (For the human, at least.)

## File Spec

1. All files MUST contain at least one patch object.
2. Patch objects MUST start with ".patch" on its own line and end with ".endpatch" on its own line.
3. Patch objects MAY have a line stating a name. This line is in the format of ".name <name>".
4. Patch objects MAY have a line stating a file hash. This line is in the format of ".filehash <hash>". The hash algorithm supported is SHA-256.
5. Patch objects MUST contain at least one record. They MAY contain more than one.
6. Direct one-to-one byte changes can be given using the format "<address>=<val>". The spec is currently missing multi-byte changes and RLE-encoded changes. These will be added in a later version of the spec.
7. Lines outside of the ".patch"/".endpatch" combo MUST be ignored.
