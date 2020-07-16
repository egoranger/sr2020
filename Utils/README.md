# Utilities

## VXD
VXD object remembers robots structure. It can create a .vxd file from vxa (or vxc) file.

When using `create_bot_from_vxa` you can minimize the structure as well as the number of materials. These are by default set to `False` but you can simply change (check out the example).

```python
from Utils.VXD import VXD

vxd = VXD()
vxd.create_bot_from_vxa( "file.vxa", minimize=True, change_mats=True )
#or
vxd.create_bot_from_vxc( "file.vxc", minimize=True, change_mats=True )
vxd.write_to_xml()
```
