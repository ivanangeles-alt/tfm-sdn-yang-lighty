from ncclient import manager

routers = [
    ("r1", "172.20.20.4"),
    ("r2", "172.20.20.5")
]

for name, ip in routers:
    print(f"\nProbando {name} ({ip})...")
    try:
        with manager.connect(
            host=ip,
            port=830,
            username="admin",
            password="admin",
            hostkey_verify=False,
            device_params={'name': 'default'}
        ) as m:
            print(f"✔ {name} conectado correctamente")
            print("Capabilities:")
            for cap in m.server_capabilities:
                print("  -", cap)
    except Exception as e:
        print(f"✘ Error conectando a {name}: {e}")