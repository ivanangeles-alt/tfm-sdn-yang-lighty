from ncclient import manager

config = """
<config>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>Ethernet1</name>
      <config>
        <name>Ethernet1</name>
        <description>Test desde NETCONF</description>
      </config>
    </interface>
  </interfaces>
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