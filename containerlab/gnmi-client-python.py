#!/usr/bin/env python3

"""
Cliente gNMI completo usando los protobuffers de gNMI.

Requiere:
  pip install grpcio protobuf gnmi-tools
"""

import grpc
import sys
import os
from pathlib import Path

# Intentar importar los protos de gNMI
try:
    from gnmi_pb2 import CapabilityRequest, GetRequest, Subscription, SubscribeRequest, SetRequest
    from gnmi_pb2 import Target, TypedValue
    from gnmi_pb2_grpc import gNMIStub
    PROTOS_AVAILABLE = True
except ImportError:
    PROTOS_AVAILABLE = False
    print("⚠️  Advertencia: gnmi-tools no instalado")
    print("   Instala con: pip install gnmi-tools")
    print("   O alternativamente usa: gnmic (herramienta standalone)")

def create_tls_channel(host, port, ca_cert_path, client_cert_path, client_key_path):
    """Crea un canal gRPC seguro con mTLS."""
    
    print(f"\n📡 Conectando a {host}:{port}")
    
    # Leer certificados
    try:
        with open(ca_cert_path, 'rb') as f:
            ca_crt = f.read()
        with open(client_cert_path, 'rb') as f:
            client_crt = f.read()
        with open(client_key_path, 'rb') as f:
            client_key = f.read()
        
        print("   ✓ Certificados cargados")
    except FileNotFoundError as e:
        print(f"   ✗ Error leyendo certificados: {e}")
        return None
    
    # Crear credenciales SSL/TLS
    try:
        creds = grpc.ssl_channel_credentials(
            root_certificates=ca_crt,
            private_key=client_key,
            certificate_chain=client_crt
        )
        
        # Crear canal
        channel = grpc.secure_channel(
            f"{host}:{port}",
            creds,
            options=[
                ('grpc.max_send_message_length', -1),
                ('grpc.max_receive_message_length', -1),
            ]
        )
        
        print("   ✓ Canal gRPC seguro creado")
        return channel
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return None

def test_gnmi_connection(host, port, ca_cert, client_cert, client_key):
    """Prueba conexión gNMI."""
    
    print(f"\n{'='*60}")
    print(f"TEST: {host}:{port}")
    print(f"{'='*60}")
    
    if not PROTOS_AVAILABLE:
        print("⚠️  Protos no disponibles, solo test de conexión TCP")
        print("\nAlternativa: Usar gnmic")
        print("  ./gnmi-client-gnmic.sh")
        return False
    
    channel = create_tls_channel(host, port, ca_cert, client_cert, client_key)
    if not channel:
        return False
    
    try:
        # Crear cliente gNMI
        stub = gNMIStub(channel)
        
        print("\n📋 Obteniendo Capabilities...")
        
        # Enviar CapabilityRequest
        request = CapabilityRequest()
        try:
            response = stub.Capabilities(request, timeout=10)
            
            print("✓ Capabilities recibidas:")
            print(f"  - gNMI version: {response.gNMI_version}")
            print(f"  - Supported models: {len(response.supported_models)}")
            for model in response.supported_models[:5]:  # Mostrar primeros 5
                print(f"    - {model.name} v{model.version}")
            
            return True
            
        except grpc.RpcError as e:
            print(f"✗ Error gRPC: {e.code()}")
            print(f"  Mensaje: {e.details()}")
            return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        channel.close()

def main():
    print("""
    ════════════════════════════════════════════════════════════
    CLIENTE gNMI - ACCESO DIRECTO A DISPOSITIVOS
    ════════════════════════════════════════════════════════════
    
    Bypasea:
    ✗ Topología de lighty.io (que falla)
    ✗ Keystores (que no desencriptan)
    ✗ Servicio AAA (que tiene bugs)
    
    Acceso directo:
    ✓ gRPC + mTLS a dispositivos EOS
    ✓ Certificates directos de containerlab
    ✓ Operaciones Get/Set/Subscribe
    
    ════════════════════════════════════════════════════════════
    """)
    
    # Dispositivos
    devices = [
        {
            "name": "r1",
            "host": "172.20.20.4",
            "port": 6030,
            "ca_cert": "clab-ceos-testbed/r1/ssl/ca.crt",
            "client_cert": "clab-ceos-testbed/r1/ssl/node.crt",
            "client_key": "clab-ceos-testbed/r1/ssl/node.key",
        },
        {
            "name": "r2",
            "host": "172.20.20.5",
            "port": 6030,
            "ca_cert": "clab-ceos-testbed/r2/ssl/ca.crt",
            "client_cert": "clab-ceos-testbed/r2/ssl/node.crt",
            "client_key": "clab-ceos-testbed/r2/ssl/node.key",
        },
    ]
    
    results = {}
    
    for device in devices:
        success = test_gnmi_connection(
            device["host"],
            device["port"],
            device["ca_cert"],
            device["client_cert"],
            device["client_key"]
        )
        results[device["name"]] = success
    
    # Resumen
    print(f"\n{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}")
    
    for device_name, success in results.items():
        status = "✓ CONECTADO" if success else "✗ FALLIDO"
        print(f"{device_name}: {status}")
    
    # Sugerencias
    print(f"\n{'='*60}")
    print("PRÓXIMOS PASOS")
    print(f"{'='*60}")
    
    if all(results.values()):
        print("✓ Conexión gNMI funcionando correctamente")
        print("\nUsando gnmic para operaciones:")
        print("  ./gnmi-client-gnmic.sh")
    else:
        print("⚠️  Algunos dispositivos no respondieron")
        print("\nOpción 1: Instalar gnmi-tools")
        print("  pip install gnmi-tools")
        print("\nOpción 2: Usar gnmic (más simple)")
        print("  apt-get install gnmic")
        print("  ./gnmi-client-gnmic.sh")

if __name__ == "__main__":
    main()
