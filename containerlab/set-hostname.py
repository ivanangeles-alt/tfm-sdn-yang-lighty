from ncclient import manager

config = """
<config>
  <system xmlns="http://openconfig.net/yang/system">
    <config>
      <hostname>r1</hostname>
    </config>
  </system>
</config>
"""

with manager.connect(
    host="172.20.20.4",
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False,
    device_params={'name': 'default'}
) as m:
    response = m.edit_config(target="running", config=config)
    print(response)