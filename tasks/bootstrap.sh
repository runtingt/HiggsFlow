#!/usr/bin/env bash

# Bootstrap file for batch jobs that is sent with all jobs and
# automatically called by the law remote job wrapper script to find the
# setup.sh file of this example which sets up software and some environment
# variables. The "{{analysis_path}}" variable is defined in the workflow
# base tasks in analysis/framework.py.

action() {
    echo "Running CUDA setup"
    source /vols/software/cuda/setup.sh
    nvidia-smi
    echo "Running law setup"
    source "{{analysis_path}}/setup.sh"
    echo "Bootstrap done"
}
action