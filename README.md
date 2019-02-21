# kpf #

kpf (**k**huxkm **p**atch **f**ile) files are ROM patches, designed for easy programmatic usage.

## Example usage ##

If you have this file:

```
00000000: 0001 0003 04                             .....
```

And you want to turn byte 2 from 0x00 to 0x02, you use a patch file like so:

```
.patch
.name Byte 2 to 2
.filehash 1661dd5ceb50868475112bae4b13f0115e8e419f384363e36722c399b45b892b
00000002=0x02
.endpatch
```

kpf files can contain more than one patch, allowing for customization.

## Reference implementation ##

Eventually, this repo will be used to host the reference implementation of the KPF format.

A proper explanation of the format will exist in KPF.md eventually.
