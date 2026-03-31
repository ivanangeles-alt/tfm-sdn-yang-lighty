from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele, to_xml

with manager.connect(
    host="172.20.20.4",
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:

    # Crear RPC <edit-config>
    rpc = new_ele("edit-config")
    target = sub_ele(rpc, "target")
    sub_ele(target, "running")

    config = sub_ele(rpc, "config")
    cli = sub_ele(config, "cli-config-data", xmlns="http://arista.com/yang/cli-config")
    cmd = sub_ele(cli, "cmd")
    cmd.text = "hostname R1-NETCONF"

    # Enviar RPC
    response = m.dispatch(rpc)
    print(to_xml(response.data))