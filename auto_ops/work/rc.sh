python <<EOF
import json
import psutil as pu
memInfo = {}
mem = pu.virtual_memory()
memInfo["total"] = mem.total
memInfo["available"] = mem.available
memInfo["percent"] = mem.percent
memInfo["used"] = mem.used
memInfo["free"] = mem.free
data = json.dumps(memInfo)
print(data)
EOF
