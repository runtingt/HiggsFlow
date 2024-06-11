#`!/bin/bash

mode=${1:-ssh}
prefix="ssh://git@gitlab.cern.ch:7999"

clean=${2:-noclean}

ch=${3:-all}

reference=${4:-noref}

if [ "$reference" == "ref" ]; then
  ref="--reference /eos/user/h/hcombbot/HiggsCombination/cadi"
fi

if [ "$mode" == "https" ]; then
  prefix="https://gitlab.cern.ch"
fi

if [ "$mode" == "krb5" ]; then
  prefix="https://:@gitlab.cern.ch:8443"
fi

if [ "$mode" == "https" ] && [ ! -z ${CI_JOB_TOKEN+x} ] ; then
  prefix="https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.cern.ch"
fi

echo "Cloning via the ${mode} url..."

if [ "$ch" != "all" ]; then
  echo " --> Channel: ${ch}"
else
  echo " --> All channels"
fi

PIDS=""

if [ "$ch" == "hww_incl" ] || [ "$ch" == "hww_stxs" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hww} ${prefix}/cms-hcg/cadi/hig-20-013.git hww &
  PIDS+="$! "
fi

if [ "$ch" == "tthll" ] || [ "$ch" == "tth_multilepton" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/tthll} ${prefix}/cms-hcg/cadi/hig-19-008.git tthll & 
  PIDS+="$! "
fi

if [ "$ch" == "hgg" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hgg} ${prefix}/cms-hcg/cadi/hig-19-015.git hgg -b ForCombination &
  PIDS+="$! "
fi

if [ "$ch" == "htautau" ] || [ "$ch" == "htt_incl" ] || [ "$ch" == "htt_stxs" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/htautau} ${prefix}/cms-hcg/cadi/hig-19-010.git htautau -b comb-21 & 
  PIDS+="$! "
fi

if [ "$ch" == "tthbb" ] || [ "$ch" == "tth_hbb" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/tthbb} ${prefix}/cms-hcg/cadi/hig-19-011.git tthbb -b lightweight &
  PIDS+="$! "
fi

if [ "$ch" == "vhbb_stxs" ] || [ "$ch" == "all" ]; then
  mkdir vhbb_stxs
  pushd vhbb_stxs
  curl -L -o comb_fullrun2.inputs.root https://cernbox.cern.ch/s/8jLALux664YbTYx/download
  curl -L -o comb_fullrun2.txt https://cernbox.cern.ch/s/Ij0EF1uU8Xn1Tte/download
  popd
  #git lfs install
  #git lfs clone ${ref:+${ref}/vhbb_stxs} ${prefix}/cms-analysis/hig/hig-20-001/datacards.git vhbb_stxs -b master &
  #PIDS+="$! "
fi

#if [ "$ch" == "vhbb" ] || [ "$ch" == "all" ]; then
#  git clone ${ref:+${ref}/vhbb} ${prefix}/cms-hcg/cadi/hig-20-001.git vhbb &
#  PIDS+="$! "
#fi


if [ "$ch" == "hzz" ] || [ "$ch" == "all" ]; then
  #git clone ${ref:+${ref}/hzz} ${prefix}/cms-hcg/cadi/hig-19-001.git hzz -b LegacyCards & 
  #git clone ${ref:+${ref}/hzz} ${prefix}/cms-hcg/cadi/hig-19-001.git hzz -b LegacyCardsPreStep & 
  git clone ${ref:+${ref}/hzz} ${prefix}/cms-hcg/cadi/hig-19-001.git hzz -b LegacyFixed & 
  PIDS+="$! "
fi

if [ "$ch" == "hmm" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hmm} ${prefix}/cms-hcg/cadi/hig-19-006.git hmm -b LegacyCards & 
  PIDS+="$! "
fi

if [ "$ch" == "hbb_boosted_partial" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hbb_boosted_partial} ${prefix}/cms-hcg/cadi/hig-19-003.git hbb_boosted_partial & 
  PIDS+="$! "
fi

if [ "$ch" == "hbb_boosted" ] || [ "$ch" == "hbb_boosted_stxs" ] || [ "$ch" == "hbb_boosted_incl" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hbb_boosted} ${prefix}/cms-hcg/cadi/hig-21-020.git hbb_boosted -b ForComb &
  PIDS+="$! "
fi

if [ "$ch" == "hinv" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hinv} ${prefix}/cms-hcg/cadi/hig-21-007.git hinv &
  PIDS+="$! "
fi


if [ "$ch" == "hzg" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/hzg} ${prefix}/cms-hcg/cadi/HIG-19-014.git hzg &
  PIDS+="$! "
fi


if [ "$ch" == "vbfhbb" ] || [ "$ch" == "all" ]; then
  git clone ${ref:+${ref}/vbfhbb} ${prefix}/cms-hcg/cadi/hig-22-009.git vbfhbb -b ForComb &
  PIDS+="$! "
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REMOVE FOR LEGACY
if [ "$ch" == "tthbb_partial" ] || [ "$ch" == "all" ]; then
  ## tthbb from HIG-17-031 (preparsed)
  mkdir tthbb_partial
  pushd tthbb_partial
  xrdcp root://eosuser.cern.ch:1094//eos/user/h/hcombbot/HiggsCombination/prepared_datacards/tthbb/comb_2017_tth_hbb_hadronic.inputs.root .
  xrdcp root://eosuser.cern.ch:1094//eos/user/h/hcombbot/HiggsCombination/prepared_datacards/tthbb/comb_2017_tth_hbb_hadronic.txt .
  xrdcp root://eosuser.cern.ch:1094//eos/user/h/hcombbot/HiggsCombination/prepared_datacards/tthbb/comb_2017_tth_hbb_leptonic.inputs.root .
  xrdcp root://eosuser.cern.ch:1094//eos/user/h/hcombbot/HiggsCombination/prepared_datacards/tthbb/comb_2017_tth_hbb_leptonic.txt .
  #curl -L -o comb_2017_tth_hbb_hadronic.inputs.root https://cernbox.cern.ch/index.php/s/v3IJPEKRXMxLlgf/download
  #curl -L -o comb_2017_tth_hbb_hadronic.txt https://cernbox.cern.ch/index.php/s/Dx46oVPamhZZdyB/download
  #curl -L -o comb_2017_tth_hbb_leptonic.inputs.root https://cernbox.cern.ch/index.php/s/Z1ZifSvkMvvXujR/download
  #curl -L -o comb_2017_tth_hbb_leptonic.txt https://cernbox.cern.ch/index.php/s/yZ7wpfGn4lJ73UB/download
  popd
fi

if [ "$ch" == "vhbb_partial" ] || [ "$ch" == "all" ]; then
  ##  vhbb from HIG-19-005 (preparsed)
  mkdir vhbb
  pushd vhbb
  curl -L -o comb_2019_vhbb.inputs.root https://cernbox.cern.ch/index.php/s/ANheWM9dE0XlZqi/download
  curl -L -o comb_2019_vhbb.txt.gz https://cernbox.cern.ch/index.php/s/DHy5CVPGPWryrrj/download
  curl -L -o comb_2019_vhbb2017.inputs.root https://cernbox.cern.ch/index.php/s/doHkkUKGav5DBVm/download
  curl -L -o comb_2019_vhbb2017.txt.gz https://cernbox.cern.ch/index.php/s/OGzVnEnabhE3Uer/download
  popd
fi

for pid in $PIDS; do
    echo "Waiting for $pid"
    wait $pid
    [ "$?" == "0" ] || { echo "$pid failed"; echo $PIDS; exit 1 ; }
done

# remove the git revision control fo the cadi lines
if [ "$clean" == "clean" ]; then
  echo rm -rf */.git
  rm -rf */.git
fi
