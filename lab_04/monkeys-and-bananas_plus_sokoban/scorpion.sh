#! /bin/bash

DOMAIN="$1"
PROBLEM="$2"

./scorpion/fast-downward.py \
    --transform-task preprocess-h2 \
    "$DOMAIN" \
    "$PROBLEM" \
    --search "astar(scp_online([
        projections(sys_scp(max_time=100, max_time_per_restart=10)),
        cartesian()],
        saturator=perimstar, max_time=1000, interval=10K, orders=greedy_orders()),
        pruning=limited_pruning(pruning=atom_centric_stubborn_sets(), min_required_pruning_ratio=0.2))"