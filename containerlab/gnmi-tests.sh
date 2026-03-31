#!/bin/bash

R1=172.20.20.4
USER=admin
PASS=admin

echo "=== gNMI TEST SUITE ==="
echo ""

echo "[1] CAPABILITIES"
gnmic -a $R1:6030 --insecure -u $USER -p $PASS capabilities
echo ""

echo "[2] GET Ethernet1"
gnmic -a $R1:6030 --insecure -u $USER -p $PASS get \
  --path /interfaces/interface[name=Ethernet1]
echo ""

echo "[3] SET description"
gnmic -a $R1:6030 --insecure -u $USER -p $PASS set \
  --update-path /interfaces/interface[name=Ethernet1]/openconfig-interfaces:config/description \
  --update-value "Configured via gNMI"
echo ""

echo "[4] SUBSCRIBE counters (5 seconds)"
gnmic -a $R1:6030 --insecure -u $USER -p $PASS subscribe \
  --path /interfaces/interface[name=Ethernet1]/state/counters \
  --stream-mode sample --sample-interval 2s --timeout 5s
echo ""

echo "=== TESTS COMPLETED ==="