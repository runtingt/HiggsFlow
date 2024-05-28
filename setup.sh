#!/usr/bin/env bash

# Define some colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

action() {
    # Get current directories and shell information.
    local shell_is_zsh="$( [ -z "${ZSH_VERSION}" ] && echo "false" || echo "true" )"
    local this_file="$( ${shell_is_zsh} && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "${this_file}" )" && pwd )"

    echo -e "${GREEN}Getting current directories and shell information...${NC}"

    # Check the law executable is available
    if ! command -v law > /dev/null; then
        echo -e "${RED}law executable not found. Please make sure it is installed and available in your PATH.${NC}"
        return 1
    fi
    echo -e "${GREEN}Setting python/law environment variables...${NC}"

    # Set python/law environment variables
    export PYTHONPATH="${this_dir}:${PYTHONPATH}"
    export LAW_HOME="${this_dir}/.law"
    export LAW_CONFIG_FILE="${this_dir}/law.cfg"

    # Set analysis environment variables
    echo -e "${GREEN}Setting analysis environment variables...${NC}"
    export ANALYSIS_PATH="${this_dir}"
    export DATA_PATH="${ANALYSIS_PATH}/data"
    export CMSSW_PATH="/home/hep/tr1123/CMSSW_14_0_0_pre0/src" # TODO get this from the user

    # Set up law completion
    echo -e "${GREEN}Setting up law completion...${NC}"
    local law_completion="$( law completion )"
    if [ -f "${law_completion}" ]; then
        source "${law_completion}" ""
    else
        echo -e "${RED}File ${law_completion} not found${NC}"
        return 1
    fi

    echo -e "${GREEN}Analysis environment set up.${NC}"
}
action