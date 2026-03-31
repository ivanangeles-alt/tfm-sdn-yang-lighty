#!/bin/bash

echo 'Destroying containerlab topology with Arista cEOS routers...'

sudo containerlab destroy --topo ceos-testbed.yaml --cleanup

echo 'Done!'
echo ''
echo ''

echo 'Removing leftover Docker containers (if any)...'
sudo docker rm -f clab-ceos-testbed-pc1 clab-ceos-testbed-pc2 2>/dev/null

echo 'Done!'
echo ''
echo ''

echo 'Removing leftover Docker networks (if any)...'
sudo docker network prune -f

echo 'All cleaned up!'