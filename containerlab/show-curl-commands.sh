#!/bin/bash

# Script para GENERAR comandos curl listos para usar
# Esto muestra los comandos sin ejecutarlos, listos para copiar y pegar

CERT_DIR="clab-ceos-testbed/.tls"
LIGHTY_URL="http://127.0.0.1:8888/restconf/operations/gnmi-certificate-storage:add-keystore-certificate"

# Leer certificados
CA_CERT=$(cat $CERT_DIR/ca/ca.pem)
R1_CERT=$(cat $CERT_DIR/r1/r1.pem)
R1_KEY=$(cat $CERT_DIR/r1/r1.key)
R2_CERT=$(cat $CERT_DIR/r2/r2.pem)
R2_KEY=$(cat $CERT_DIR/r2/r2.key)

echo ""
echo "=========================================="
echo "COMANDO CURL PARA R1"
echo "=========================================="
echo ""
echo "curl --request POST '$LIGHTY_URL' \\"
echo "--header 'Content-Type: application/json' \\"
echo "--data-raw '{"
echo "    \"input\": {"
echo "        \"keystore-id\": \"keystore-r1\","
echo "        \"ca-certificate\": \"$CA_CERT\","
echo "        \"client-key\": \"$R1_KEY\","
echo "        \"client-cert\": \"$R1_CERT\""
echo "    }"
echo "}'"
echo ""

echo ""
echo "=========================================="
echo "COMANDO CURL PARA R2"
echo "=========================================="
echo ""
echo "curl --request POST '$LIGHTY_URL' \\"
echo "--header 'Content-Type: application/json' \\"
echo "--data-raw '{"
echo "    \"input\": {"
echo "        \"keystore-id\": \"keystore-r2\","
echo "        \"ca-certificate\": \"$CA_CERT\","
echo "        \"client-key\": \"$R2_KEY\","
echo "        \"client-cert\": \"$R2_CERT\""
echo "    }"
echo "}'"
echo ""
