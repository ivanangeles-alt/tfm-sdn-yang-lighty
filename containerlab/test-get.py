from ncclient import manager

filter = """
<interfaces xmlns="http://openconfig.net/yang/interfaces"/>
"""

with manager.connect(
    host="172.20.20.4",
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False,
    device_params={'name': 'default'}
) as m:
    response = m.get_config(source="running", filter=("subtree", filter))
    print(response.xml)