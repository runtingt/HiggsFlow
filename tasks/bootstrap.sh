#!/usr/bin/env bash

# Bootstrap file for batch jobs that is sent with all jobs and
# automatically called by the law remote job wrapper script to find the
# setup.sh file of this example which sets up software and some environment
# variables. The "{{analysis_path}}" variable is defined in the workflow
# base tasks in analysis/framework.py.

action() {
    export LD_LIBRARY_PATH= # clear LD_LIBRARY_PATH to avoid conflicts
    echo "CUDA_VISIBLE_DEVICES:"$CUDA_VISIBLE_DEVICES;
    eval "$(micromamba shell hook --shell bash)"
    echo "Running CUDA setup"
    source /vols/software/cuda/setup.sh
    nvidia-smi
    source /vols/grid/cms/setup.sh
    echo "Running law setup"
    source "${ANALYSIS_PATH}/setup.sh" "--remote"
    # cwd=$(pwd)
    # cd "${CMSSW_PATH}"
    # cmsenv
    # cd "${cwd}"
    which law
    echo "Bootstrap done"
}
action