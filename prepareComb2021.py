from __future__ import absolute_import
from __future__ import print_function
import CombineHarvester.CombineTools.ch as ch
import chtools.utils as utils
import ROOT
import time
import datetime
import sys
import argparse
import re
import pprint
import os
import gzip,shutil
import numpy as np
from collections import defaultdict
import six

start_=datetime.datetime.now() ## global start

def Timing(mex,start):
    end=datetime.datetime.now()
    print(">>",mex,end-start)
    sys.stdout.flush()
    start=datetime.datetime.now()
    return start

parser = argparse.ArgumentParser()
parser.add_argument( '--select', help='Comma separated list of channels to process (default=all)', default=None)
parser.add_argument( '--veto', help='Comma separated list of channels to veto (default=none)', default=None)
parser.add_argument( '--postfix', help='Postfix string for output', default='')
parser.add_argument( '--save-unmodified', help='Save copies of datacards before any modifications', action='store_true')
parser.add_argument( '--drop-procs', help='Drop small signal processes', action='store_true')
parser.add_argument( '--drop-shapes', help='Convert signal shape uncertainties that do not have a significant shape effect to lnN', action='store_true')
parser.add_argument( '--drop-shapes-vhbbBTag', help='Convert signal bTag shape uncertainties in vhbb_stxs analysis that do not have a significant shape effect to lnN', action='store_true')
parser.add_argument( '--diagnostics', help='Print diagnostic info about the model', action='store_true')
parser.add_argument( '--signalnames', help='Print signal names after renaming', action='store_true')
parser.add_argument( '--includehinv', help='Include hinv cards', action='store_true')
parser.add_argument( '--includehzg', help='Include hzg cards', action='store_true')
parser.add_argument( '--no-systs', help='Drop all systematics', action='store_true')
parser.add_argument( '--prune-asymm-lnN', help='Change Asymm. logN into symm ones if difference is tiny', action='store_true')
parser.add_argument( '--replace-mc-stats', help='Replace mcstats in htt', action='store_true')

args = parser.parse_args()

#threshold = float(args.threshold)
#bound = float(args.bound)

postfix = args.postfix
select_chns = []
veto_chns = []
if args.select is not None:
    select_chns = args.select.split(',')
if args.veto is not None:
    veto_chns = args.veto.split(',')

if not args.includehinv:
    veto_chns.append('hinv')

if not args.includehzg:
    veto_chns.append('hzg')


ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

if not hasattr(ROOT, "RooModZPdf"):
    # hmm pdfs not in this version of combine, load them ourself
    if not os.path.isfile('lib/HMuMuRooPdfs_cc.so'):
        ROOT.gROOT.ProcessLine('.L lib/HMuMuRooPdfs.cc++')
    ROOT.gSystem.Load('lib/HMuMuRooPdfs_cc.so')

cb = ch.CombineHarvester()
cb.SetFlag('workspaces-use-clone', True)
cb.SetFlag('import-parameter-err', False)
cb.SetFlag('filters-use-regex', True)
cb.SetFlag("check-negative-bins-on-import", False)
cb.SetFlag('fix-rooconstvar', True) ## only works with clone workspaces

cb.SetVerbosity(0)

all_cards = {
    'hbb_boosted_partial' : [
        'hbb_boosted_partial/cms_datacard_hig-19-003.txt'
        ],
    'hbb_boosted_stxs' : [
        'hbb_boosted/stxs-stage1-2-fine/testModel/model_combined.txt'
    ],
    'hbb_boosted_incl' : [
        'hbb_boosted/signal-strength/testModel/model_combined.txt'
    ],
    'tth_hbb': [
        'tthbb/combined_cards/STXS/v16p2/all_years/combined_DLFHSL_all_years.txt'
    ],
    'tth_hbb_partial': [
        'tthbb_partial/comb_2017_tth_hbb_hadronic.txt',
        'tthbb_partial/comb_2017_tth_hbb_leptonic.txt',
    ],
    'tth_multilepton': [
        'tthll/combination.dat'
    ],
    'vhbb': [
        #'vhbb/comb_fullrun2_Xbb_6ffb98f7.txt' # LEGACY
        'vhbb/comb_2019_vhbb2017.txt',
        'vhbb/comb_2019_vhbb.txt',
    ],
    'vhbb_stxs': [
        #'vhbb_stxs/input/comb_fullrun2.txt',
        'vhbb_stxs/comb_fullrun2.txt',
    ],
    'hww_incl': [
        #'hww/STXS_run2_DF_full_pruned.txt',
        'hww/HWW_run2_legacy_full.txt',
    ],
    'hww_stxs' : [
        'hww/comb_card_HWW_STXS_ALL_pruned.txt',
    ],
    'htt_incl': [
        'htautau/ML_STXS/stage0/125/combined.txt.cmb',
        'htautau/WH_STXS/combined.txt.cmb',
        'htautau/ZH_STXS/combined.txt.cmb'
    ],
    'htt_stxs': [
        'htautau/ML_STXS/stage1/125/combined.txt.cmb',
        'htautau/WH_STXS/combined.txt.cmb',
        'htautau/ZH_STXS/combined.txt.cmb'
    ],
    'hzz': [
      'hzz/stxs_trueBins/legacy/card_run2_hzzLowMem.txt'
    ],
    'hmm': [
        # parsing the combined datacard fails for some reason.
        #'hmm/combination/cms_hmm_combination.txt'
        'hmm/combination/check_2020_ggh.txt',
        'hmm/combination/check_2020_tth.txt',
        'hmm/combination/check_2020_vbf.txt',
        'hmm/combination/check_2020_wh.txt',
        'hmm/combination/check_2020_zh.txt',
    ],
    # Cannot parse hgg currently! Runs out of memory
    'hgg': [
        'hgg/DatacardLowMem.txt'
    ],
    'hzg' : [
       'hzg/comb21/card_run2_comb_all_12538_m105_cleaned.txt'
    ],
    # hinv has nuisance edit statements that cant be parsed at the moment.
    # more and more annoying ones
    'hinv' : [
        'hinv/combination_alltime/hinv_combination_run2.txt'
    ],
    'vbfhbb' : [
        'vbfhbb/datacards_inclusive_run2_paper_version.txt'
    ]
}

start=datetime.datetime.now()
print("-> Importing cards")
sys.stdout.flush()

if(os.path.isfile("htautau/ML_STXS/stage1/125/combined.txt.cmb.gz")):
    with gzip.open("htautau/ML_STXS/stage1/125/combined.txt.cmb.gz","r") as f_in, open("htautau/ML_STXS/stage1/125/combined.txt.cmb","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)

if(os.path.isfile("htautau/ML_STXS/stage0/125/combined.txt.cmb.gz")):
    with gzip.open("htautau/ML_STXS/stage0/125/combined.txt.cmb.gz","r") as f_in, open("htautau/ML_STXS/stage0/125/combined.txt.cmb","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)

if(os.path.isfile('hww/comb_card_HWW_STXS_ALL_pruned.txt.gz')):
    with gzip.open("hww/comb_card_HWW_STXS_ALL_pruned.txt.gz","r") as f_in, open("hww/comb_card_HWW_STXS_ALL_pruned.txt","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)

if(os.path.isfile('hinv/combination_alltime/hinv_combination_run2.txt.gz')):
    with gzip.open("hinv/combination_alltime/hinv_combination_run2.txt.gz","r") as f_in, open("hinv/combination_alltime/hinv_combination_run2.txt","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)

##REMOVE FOR LEGACY
if(os.path.isfile("vhbb/comb_2019_vhbb2017.txt.gz")):
    with gzip.open("vhbb/comb_2019_vhbb2017.txt.gz","r") as f_in, open("vhbb/comb_2019_vhbb2017.txt","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)
if(os.path.isfile("vhbb/comb_2019_vhbb.txt.gz")):
    with gzip.open("vhbb/comb_2019_vhbb.txt.gz","r") as f_in, open("vhbb/comb_2019_vhbb.txt","wb") as f_out:
        shutil.copyfileobj(f_in,f_out)

#if(os.path.isfile("vhbb_stxs/LegacyComb_test/comb_fullrun2.txt.gz")):
#    with gzip.open("vhbb_stxs/LegacyComb_test/comb_fullrun2.txt.gz","r") as f_in, open("vhbb_stxs/LegacyComb_test/comb_fullrun2.txt","wb") as f_out:
#        shutil.copyfileobj(f_in,f_out)

import chtools.nuisance_edit as ne
from subprocess import call

nuisance_edits={}

##
for chn in ['hinv','tth_hbb','tth_hbb_partial','hww_incl','hww_stxs']:  # LEGACY
    if (len(select_chns) > 0 and chn not in select_chns) or chn in veto_chns:
        print('>> Skipping %s' % chn)
        continue
    nuisance_edits[chn]=ne.ReadNuisanceEdit(all_cards[chn])

## chang dc on the fly. This is to have combine harvester to parse cards w/o nuisance edit statements
for chn in nuisance_edits:
    if (len(select_chns) > 0 and chn not in select_chns) or chn in veto_chns:
        print('>> Skipping %s' % chn)
        continue
    print('>> Checking nuisance edits in channel %s ' % chn)

    for idx, card in enumerate(all_cards[chn]):
        ## 1. remove nuisance edit from the txt card
        card2 = re.sub('.txt','_no_ne.txt',card)
        cmd="cat %s | grep -v '^nuisance \+edit' > %s "%(card,card2)
        call(cmd, shell=True)
        ## 2. run combine cards to fix bin names: not needed with the new combined card
        #print ("DEBUG","CARD","->",card2)
        #card3 = re.sub('.txt','_comb_final.txt',card)
        #extra=card.split('/')[1] ## fix for same bin names
        #if chn == 'hinv' and extra=='photons':
        #    if 'vbf_photons_2017' in card: extra='vbf_photons_2017'
        #    if 'vbf_photons_2018' in card: extra='vbf_photons_2018'
        #cmd='cd %s && combineCards.py %s=%s > %s' %( os.path.dirname(card) ,extra ,os.path.basename(card2),os.path.basename(card3)) ## multiple datacards with the same region. SR ...
        #print ("DEBUG","calling cmd:",cmd)
        #call(cmd,shell=True)
        #print ("DEBUG","CARD","->",card3)
        #all_cards[chn][idx]=card3
        all_cards[chn][idx]=card2
    print(("DEBUG","CARDS of",chn,":",','.join(all_cards[chn])))

## check for nuisance edits in cards not accounted for
for chn in all_cards.keys():
    if (len(select_chns) > 0 and chn not in select_chns) or chn in veto_chns:
        print('>> Skipping %s' % chn)
        continue
    if chn in nuisance_edits: continue ## nuisance edits are accounted for
    print('>> Checking nuisance edits in channel %s ' % chn)
    ne.AbortOnNuisanceEdit(all_cards[chn])

for chn in all_cards.keys():
    if (len(select_chns) > 0 and chn not in select_chns) or chn in veto_chns:
        print('>> Skipping %s' % chn)
        continue
    print('>> Parsing %s cards' % chn)
    for card in all_cards[chn]:
        if chn == 'vhbb_stxs':
            # FIXME: when t2w
            #raise RuntimeError("Failed to find %s in file %s (from pattern %s, %s)" % (objname, finalNames[0], names[1], names[0]))
            #RuntimeError: Failed to find vhbb_Wen_14_13TeV2018/WH_lep_PTV_150_250_0J_hbb125.38 in file comb_2021_vhbb_stxs.inputs.root (from pattern vhbb_Wen_14_13TeV2018/WH_lep_PTV_150_250_0J_hbb$MASS, comb_2021_vhbb_stxs.inputs.root)
            cb.ParseDatacard(card, analysis='comb', channel=chn, mass='')
        else:
            cb.ParseDatacard(card, analysis='comb', channel=chn, mass='125.38' if chn=='hmm' else '125')

    print('>> Finish Parsing %s cards' % chn)

start=Timing("Cards imported",start)
## nuisance edits
for chn in nuisance_edits:
    #for b,x in nuisance_edits[chn]['freeze']:  # drop syst in chn that wanted to be freeze. Freezing them could actually change something else in other cards
    #    print ("DEBUG","DROP",chn,x)
    #    cb.FilterSysts(lambda s: s.channel()==chn and s.bin() ==b and s.name()==x)

    #for p,b,x in nuisance_edits[chn]['drop']:
    #    print ("DEBUG","DROP",chn,x,p,b)
    #    cb.FilterSysts(lambda s: s.channel()==chn and s.bin() ==b and s.process() == p and s.name()==x)

    rate_param_to_freeze=[]
    for b,s in nuisance_edits[chn]['freeze']:
        cb.cp().channel([chn]).bin([b]).syst_name([s]).ForEachSyst(
                lambda x:[ rate_param_to_freeze.append(s) if x.type() == 'rateParam' else None]
                )
    rate_param_to_freeze=list(set(rate_param_to_freeze))

    rate_param_to_keep=[]
    for pn in rate_param_to_freeze:
        value=cb.GetParameter(pn).val()
        if value != 1.0:
            rate_param_to_keep.append(pn)
    rate_param_to_keep=list(set(rate_param_to_keep))

    print(("DEBUG","DROP",chn, [ (b,n) for (b,n) in nuisance_edits[chn]['freeze'] if n not in rate_param_to_keep]))
    cb.FilterSysts(lambda s: s.channel()==chn and  (s.bin(),s.name()) in nuisance_edits[chn]['freeze'] and s.name() not in rate_param_to_keep)
    print(("DEBUG","FREEZE","rateParam",rate_param_to_keep))
    for pn in rate_param_to_keep:
        cb.GetParameter(pn).set_frozen(True)

    print(("DEBUG","DROP",chn,nuisance_edits[chn]['drop']))
    cb.FilterSysts(lambda s: s.channel()==chn and (s.bin(),s.process(),s.name()) in nuisance_edits[chn]['drop'] )

    for b, name, name2 in nuisance_edits[chn]['rename']:
        print(("DEBUG","RENAME",chn,b,name,"->",name2))
        cb.cp().channel([chn]).bin([b]).syst_name([name]).ForEachSyst(lambda x: x.set_name(name2))

        ## maybe still issue a nuisance edit to change the parameter name?
        if cb.GetParameter(name): # warning global renaming
            print((">>>>DEBUG","WARNING","GLOBAL RENAME from",chn,b,"of Par",name,"->",name2))
            cb.GetParameter(name).set_name(name2) ## does this rename also the parameters in the workspace? w.var().SetName()?
            cb.cp().channel([chn]).bin([b]).renameParInWs(name,name2,'') ##

    for b,p, name, name2 in nuisance_edits[chn]['rename2']:
        print(("DEBUG","RENAME2",chn,b,p,name,"->",name2))
        (
            cb.cp()
            .channel([chn])
            .bin([b])
            .process([p])
            .syst_name([name])
            .ForEachSyst(lambda x: x.set_name(name2))
        )
        if cb.GetParameter(name): # warning global renaming
            print((">>>>DEBUG","WARNING","GLOBAL RENAME from",chn,b,"of Par",name,"->",name2))
            cb.GetParameter(name).set_name(name2) ## does this rename also the parameters in the workspace? w.var().SetName()?
            (
                cb.cp()
                .channel([chn])
                .bin([b])
                .renameParInWs(name,name2,'')
            )

    for p,b,n ,val in nuisance_edits[chn]['add']:
        print(("DEBUG","ADD",chn,b,p,n,val))
        cb.cp().channel([chn]).process([p]).bin([b]).AddSyst(cb, n, "lnN", ch.SystMap()(val));

start=Timing("Nuisance edits done",start)

#cb.bin(['vhbb_Wen_5_13TeV2016','vhbb_Wen_6_13TeV2016','vhbb_Wen_7_13TeV2016','vhbb_Wen_8_13TeV2016'])
#Drop uncertainty in hww that has bogus norm - need to do it here otherwise the unmodified cards won't work
#cb.FilterSysts(lambda s: s.process()=='bbH_fwd_hww' and s.name()=='CMS_scale_met' and s.bin()=='ggHtag_of0j_em_pm_0j_pt2lt20' and s.channel()=='hww')
if args.no_systs:
    cb.FilterSysts(lambda s: 'shape' in s.type() or 'ln' in s.type())
    autoMCStatsBins = list(cb.GetAutoMCStatsBins())
    for b in autoMCStatsBins:
        cb_bin = cb.cp().bin([b])
        cb_bin.SetAutoMCStats(cb, -1.)

if args.save_unmodified:
    for chn in cb.channel_set():
        print('>> Writing %s card' % chn)
        cb.cp().channel([chn]).WriteDatacard(
            'comb_2021_%s_unmodified.txt.gz' % chn, 'comb_2021_%s_unmodified.inputs.root' % chn)

################################## 
if args.drop_procs:
    #Drop signals contributing less than 0.1% of the total signal rate in a given bin. Third argument can be set to True just to print the processes that can be dropped
    #Skip attempting to drop in hgg since the input card is already pruned
    utils.DropSmallSignalsWithBoundsFast(cb, cb.cp().channel(['hgg','hmm','hzz','hinv','vbfhbb'],False), 0.01, 0.005, 0.05,False, 1)
    utils.DropSmallSignalsWithBoundsFast(cb, cb.cp().channel(['hzz'],True),0.01,0,0.05,False, 1)
    start=Timing("Drop small processes",start)

if args.drop_shapes:
    #utils.CheckUncertaintyVariation(cb)
    # thresholds = {"channel":{"syst_name": threshold for this syst} }
    thresholds = {"vhbb_stxs":{"CMS_bTagWeightDeepB":2} }  # Any value >1 means do not convert this nuissance
    utils.CheckUncertaintyVariation(cb, thresholds)
if args.drop_shapes_vhbbBTag:
    thresholds_group={"vhbb_stxs":([
             'CMS_bTagWeightDeepBHFStats1_13TeV','CMS_bTagWeightDeepBHFStats2_13TeV',
             'CMS_bTagWeightDeepBHF_13TeV', 'CMS_bTagWeightDeepBJES_13TeV',
             'CMS_bTagWeightDeepBLFStats1_13TeV', 'CMS_bTagWeightDeepBLFStats2_13TeV',
             'CMS_bTagWeightDeepBLF_13TeV', 'CMS_bTagWeightDeepBcErr1_13TeV',
             'CMS_bTagWeightDeepBcErr2_13TeV'],0.95)
          } # each has 15 bins in pt-eta, we multiply the shapes and decide if convert the whole group tp lnN
    utils.CheckUncertaintygroupVariation(cb, thresholds_group)  # drop a group of nuissance that from the same source

    start=Timing("Drop shapes",start)

# Replace shape-based MC stat uncertainties with autoMCStats,
# but only for bins and processes that are currently modified by
# these shape uncertainties.
# The flag `strict=True` enforces that the current Up and Down
# shifts are symmetric. If not, the shape systematic is retained.
# Setting `strict=False` will drop the shape systematic in this case,
# and set the bin error to the max of the Up and Down shifts
if args.replace_mc_stats:
    for chn, pattern in [
      #('hbb_boosted','.*mcstat')
      ('htt_incl','.*EMB_binomial_bin_[0-9]*'), ## this should sqr sum to the existing ones in autoMCstats
      ('htt_stxs','.*EMB_binomial_bin_[0-9]*') ## this should sqr sum to the existing ones in autoMCstats
      ]:
        print("->", "replacing mc stat for",chn,pattern)
        #utils.ReplaceMCStats(cb, cb.cp().channel([chn]), pattern, strict=False, alwaysConvert=True, verbosity=1)
        utils.AddToMCStats(cb, cb.cp().channel([chn]), pattern, strict=False, alwaysConvert=True, verbosity=1)

    start=Timing("Replace MC stats",start)


def SwitchToSignal(p):
    if p.process() in ['ttH_htt', 'ggH_hww', 'qqH_hww', 'WH_htt', 'ZH_htt','ggH_hzz','tHq_htt','tHq_hzz','tHq_hww','tHW_htt','tHW_hww','tHW_hzz','tHW','tHq','tHW_hbb','tHq_hbb','tHq_hcc','tHW_hcc','tHq_hgluglu','tHW_hgluglu','tHW_hzg','tHq_hzg','tHq_hgg','WH_hww','ZH_hww','WH_bkg_16_hmm','WH_bkg_17_hmm','WH_bkg_18_hmm','ZH_bkg_16_hmm','ZH_bkg_17_hmm','ZH_bkg_18_hmm','ggH_bkg_16_hmm','ggH_bkg_17_hmm','ggH_bkg_18_hmm','qqH_bkg_16_hmm','qqH_bkg_17_hmm','qqH_bkg_18_hmm','ttH_bkg_16_hmm','ttH_bkg_17_hmm','ttH_bkg_18_hmm','ZH_lep_PTV_0_75_hww125','ZH_lep_PTV_75_150_hww125','ZH_lep_PTV_150_250_0J_hww125','ZH_lep_PTV_150_250_GE1J_hww125','ZH_lep_PTV_GT250_hww125','ggZH_lep_PTV_0_75_hww125','ggZH_lep_PTV_75_150_hww125','ggZH_lep_PTV_150_250_0J_hww125','ggZH_lep_PTV_150_250_GE1J_hww125','ggZH_lep_PTV_GT250_hww125','WH_lep_PTV_0_75_hww125','WH_lep_PTV_75_150_hww125','WH_lep_PTV_150_250_0J_hww125','WH_lep_PTV_150_250_GE1J_hww125','WH_lep_PTV_GT250_hww125','WH','ZH','ttH']:
        p.set_signal(True)

def SwitchToBackground(p):
    if p.process() in ['HH','HH_wwww','HH_ttzz','HH_ttww']:
        p.set_signal(False)

cb.ForEachProc(SwitchToSignal)
cb.ForEachSyst(SwitchToSignal)
cb.ForEachProc(SwitchToBackground)
cb.ForEachSyst(SwitchToBackground)

## Need to add rateParams for ttHll as in the published analysis they are included via multiSignalModel commands
cb.cp().channel(['tth_multilepton']).process(['TTW']).AddSyst(cb,'rate_tthll_ttW','rateParam', ch.SystMap()(1.0))
cb.cp().channel(['tth_multilepton']).process(['TTWW']).AddSyst(cb,'rate_tthll_ttW','rateParam', ch.SystMap()(1.0))
cb.cp().channel(['tth_multilepton']).process(['TTZ']).AddSyst(cb,'rate_tthll_ttZ','rateParam', ch.SystMap()(1.0))

for syst in cb.cp().channel(['tth_multilepton']).syst_type(["rateParam"]).syst_name_set():
    cb.GetParameter(syst).set_range(0.0,5.0)


## rename signals
utils.ForEachProcAndSyst(cb.cp().channel(['hmm']).signals(),
        lambda x : utils.MultiReplace(x, [('qqZH_hmm','ZH_hmm')] ,useRegex=True)
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### LEGACY: do we still need this!
###utils.ForEachProcAndSyst(cb.cp().channel(['tth_hbb']).signals(),
###    lambda x: x.set_process(x.process() + '_hbb'))
###
###utils.ForEachProcAndSyst(cb.cp().channel(['tth_hbb']).signals(),
###    lambda x: x.set_process(x.process().replace('hbb_hbb','hbb')))
###
###
###utils.ForEachProcAndSyst(cb.cp().channel(['tth_hbb']).signals(),
###    lambda x: x.set_process(x.process().replace('TTH','ttH')))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('ttH_PTH_300_infty','ttH_PTH_GT300')))

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('ttH_PTH_fwd','ttH_FWDH')))

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('WH_PTV','WH_lep_PTV')))

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('ZH_PTV','ZH_lep_PTV')))

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('ggH_GG2H','ggH')))

utils.ForEachProcAndSyst(cb.cp().channel(['tth_multilepton']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_QQ2HQQ','qqH')))


utils.ForEachProcAndSyst(cb.cp().channel(['htt_incl','htt_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('hww125','hww')))

utils.ForEachProcAndSyst(cb.cp().channel(['hzz']).signals(),
    lambda x: x.set_process(x.process().replace('BBH','bbH')))

utils.ForEachProcAndSyst(cb.cp().channel(['hbb_boosted_incl']).signals(),
    lambda x: utils.MultiReplace(x, [
        ('VBF', 'qqH'),
        ('ggF', 'ggH')], useRegex=False))

#utils.ForEachProcAndSyst(cb.cp().channel(['hzz']).signals(),
#    lambda x: utils.MultiReplace(x, [
#        ('_Had', '_had'),
#        ('TH', 'tHq'),
#        ('ZH_', 'ZH_lep_PTV_'),
#        ('WH_', 'WH_lep_PTV_'),
#        ('TTH', 'ttH_PTH'),
#        ('BBH', 'bbH'),
#        ('ggH_0j_10_200','ggH_0J_PTH_GT10'),
#        ('ggH_0j_0_10','ggH_0J_PTH_0_10'),
#        ('ggH_1j_', 'ggH_1J_PTH_'),
#        ('ggH_2j_', 'ggH_GE2J_MJJ_0_350_PTH_'),
#        ('ggH_VBF_lt700_2j','ggH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25'),
#        ('ggH_VBF_lt700_3j','ggH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25'),
#        ('ggH_VBF_gt700_2j','ggH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25'),
#        ('ggH_VBF_gt700_3j','ggH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25'),
#        ('ggH_200_300','ggH_PTH_200_300'),
#        ('ggH_300_450','ggH_PTH_300_450'),
#        ('ggH_450_650','ggH_PTH_450_650'),
#        ('ggH_GT650','ggH_PTH_GT650'),
#        ('VBF_2j_mjj_350_700_2j','qqH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25'),
#        ('VBF_2j_mjj_350_700_3j','qqH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25'),
#        ('VBF_2j_mjj_GT700_2j','qqH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25'),
#        ('VBF_2j_mjj_GT700_3j','qqH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25'),
#        ('VBF_2j_mjj_120_350', 'qqH_GE2J_MJJ_120_350'),
#        ('VBF_2j_mjj_60_120', 'qqH_GE2J_MJJ_60_120'),
#        ('VBF_2j_mjj_0_60', 'qqH_GE2J_MJJ_0_60'),
#        ('VBF_0j', 'qqH_0J'),
#        ('VBF_1j', 'qqH_1J'),
#        ('VBF_', 'qqH_')], useRegex=False))

#utils.ForEachProcAndSyst(cb.cp().channel(['hzz']).signals(),
#    lambda x: x.set_process(x.process() + '_hzz'))


utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs','hww_incl']).signals(),
    lambda x: x.set_process(x.process().replace('_hww_','_')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_MJJ_350_700_PTHJJ_0_25','qqH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ggH_GE2J_MJJ_350_700_PTHJJ_0_25','ggH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_MJJ_350_700_PTHJJ_GT25','qqH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ggH_GE2J_MJJ_350_700_PTHJJ_GT25','ggH_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_MJJ_GT700_PTHJJ_0_25','qqH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ggH_GE2J_MJJ_GT700_PTHJJ_0_25','ggH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_MJJ_GT700_PTHJJ_GT25','qqH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ggH_GE2J_MJJ_GT700_PTHJJ_GT25','ggH_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('WH_had_MJJ','WH_had_GE2J_MJJ')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ZH_had_MJJ','ZH_had_GE2J_MJJ')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('qqH_MJJ','qqH_GE2J_MJJ')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('ZH_PTV','ZH_lep_PTV')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs']).signals(),
    lambda x: x.set_process(x.process().replace('WH_PTV','WH_lep_PTV')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs','hww_incl']).signals(),
    lambda x: x.set_process(x.process() + '_hww'))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs','hww_incl']).signals(),
    lambda x: x.set_process(x.process().replace('hww_hww','hww')))

utils.ForEachProcAndSyst(cb.cp().channel(['hww_stxs','hww_incl']).signals(),
    lambda x: x.set_process(x.process().replace('htt_hww','htt')))

utils.ForEachProcAndSyst(cb.cp().channel(['hbb_boosted_stxs']).signals(),
    lambda x: x.set_process(x.process() + '_hbb'))

utils.ForEachProcAndSyst(cb.cp().channel(['hbb_boosted_incl']).signals(),
    lambda x: x.set_process(x.process() + '_hbb'))


#single_bins_in_channels = {}
#for chn in cb.cp().channel_set():
#    single_bins_in_channels[chn] = []
#    for binid in cb.cp().channel([chn]).bin_set():
#        procname = cb.cp().channel([chn]).bin([binid]).process_set()[0]
#        cb.cp().channel([chn]).bin([binid]).ForEachProc(lambda x: utils.PrintNBins(x,procname,single_bins_in_channels[chn],binid))

#print single_bins_in_channels


#for chn in cb.cp().channel_set():
#    for binid in single_bins_in_channels[chn]:
#        cb.cp().channel([chn]).bin([binid]).ForEachSyst(lambda x:x.set_type('lnN'))


if args.signalnames:
    for chn in cb.channel_set():
        print('>> signal processes after renaming in channel ',chn)
        signals = cb.cp().channel([chn]).signals().process_set()
        #backgrounds = cb.cp().channel([chn]).backgrounds().process_set()
        for proc in signals:
            print('      ',proc)
        #print '>> background processes after renaming in channel ',chn
        #for proc in backgrounds:
        #    print '      ',proc


start=Timing("Signal/Background renaming/promoting",start)

    # Filter all BR_hXX nuisances:
cb.syst_name(['BR_h(zz|bb|gg|mm|tt|vv|ww).*'], False)
###

############### SCALE TO LEGACY LUMINOSITY ##########3
if True:
    lumi_old = np.array([35.92,41.53,59.74])
    lumi_new = np.array([36.33,41.53,59.74]) ## only 2016 changed, but I need the waited average for the sums
    bin_proc={'2016':[],'2017':[],'2018':[]}
    values={}
    ## except vbf
    for year in bin_proc:
        cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_'+year]).ForEachSyst(
            lambda s: [
                bin_proc[year].append( (s.bin(),s.process() ) )
                if ( not s.bin().startswith('vbf'))
                else None
            ])
    for year in bin_proc:
        cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']).ForEachSyst(
            lambda s: [
                bin_proc[year].append( (s.bin(),s.process() ) )  if
                (s.bin().startswith('vbf_ch1') and year=='2016') or ## some unactive syst are marked as 1.
                (s.bin().startswith('vbf_ch2') and year=='2017') or
                (s.bin().startswith('vbf_ch3') and year=='2018')
                else None
            ])
    ## derive the full Run 2 bin, and purge the full Run2 from 2016.
    ## python set operations: union |, intersection &, difference -, symm_difference ^
    bin_proc['2016'] = set(bin_proc['2016'])
    bin_proc['2017'] = set(bin_proc['2017'])
    bin_proc['2018'] = set(bin_proc['2018'])
    bin_proc['Run2'] = bin_proc['2016'] & bin_proc['2017'] & bin_proc['2018'] ## the one that are all of them
    bin_proc['2017_2018'] = bin_proc['2017'] | bin_proc['2018']
    bin_proc['2016_2017_2018'] = bin_proc['2016'] |  bin_proc['2017'] | bin_proc['2018']
    bin_proc['2016_only'] = bin_proc['2016'] - bin_proc['Run2']
    bin_proc['2017_only'] = bin_proc['2017'] - bin_proc['Run2']
    bin_proc['2018_only'] = bin_proc['2018'] - bin_proc['Run2']

    #print ("DEBUG",bin_proc)
    for b,p in bin_proc['2016_only']:
        #print ("DEBUG","hmm", "want to scale", b,p,"by",lumi_new[0]/lumi_old[0])
        cb.cp().channel(['hmm']).bin([b]).process([p]).AddSyst(cb,'rate_lumiscale_2016_only','rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))
    for b,p in bin_proc['Run2']:
        #print ("DEBUG","hmm", "want to scale", b,p,"by",np.sum(lumi_new)/np.sum(lumi_old) )
        cb.cp().channel(['hmm']).bin([b]).process([p]).AddSyst(cb,'rate_lumiscale_fullrun2','rateParam', ch.SystMap()(  np.sum(lumi_new)/np.sum(lumi_old) ))

    if (len(select_chns) > 0 and 'hmm' in select_chns) and 'hmm' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only").set_frozen(True)
        cb.cp().GetParameter("rate_lumiscale_fullrun2").set_frozen(True)


    ## update luminosity uncertainties -- before renaming
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_2016' and (x.bin(),x.process()) not in bin_proc['2016'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_2017' and (x.bin(),x.process()) not in bin_proc['2017'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_2018' and (x.bin(),x.process()) not in bin_proc['2018'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_BBD' and (x.bin(),x.process()) not in bin_proc['2017_2018'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_BCC' and (x.bin(),x.process()) not in bin_proc['2016_2017_2018'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_GS' and (x.bin(),x.process()) not in bin_proc['2016_2017_2018'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_LS' and (x.bin(),x.process()) not in bin_proc['2016_2017_2018'] )
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_XY' and (x.bin(),x.process()) not in bin_proc['2016_2017_2018'] )

    ## this is not there in the updated scheme anymore, just drop it
    cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()=='lumi_13TeV_DB' )

    #Update ttH multilepton
    import chtools.scaleprocs as scaleprocs
    scale_procs_multilepton = scaleprocs.mcnames['tth_multilepton']


    bins_tthll = set(cb.cp().channel(['tth_multilepton']).bin_set())
    bins_tthll_2016 = []
    for cat in bins_tthll:
        if '2016' in cat:
            bins_tthll_2016.append(cat)

    for b in bins_tthll_2016:
        for p in scale_procs_multilepton:
            cb.cp().channel(['tth_multilepton']).bin([b]).process([p]).AddSyst(cb,'rate_lumiscale_2016_only_tthll','rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))


    if (len(select_chns) > 0 and 'tth_multilepton' in select_chns) and 'tth_multilepton' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only_tthll").set_frozen(True)

    #Update vhbb (NB NOT NEEDED FOR LEGACY). All processes from MC
    bins_vhbb = set(cb.cp().channel(['vhbb']).bin_set())
    bins_vhbb_2016 = []
    for cat in bins_vhbb:
        if not '2017' in cat:
            bins_vhbb_2016.append(cat)

    vhbb_procs = set(cb.cp().channel(['vhbb']).process_set())
    for b in bins_vhbb_2016:
        cb.cp().channel(['vhbb']).bin([b]).AddSyst(cb,'rate_lumiscale_2016_only_vhbb', 'rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))

    if (len(select_chns) > 0 and 'vhbb' in select_chns) and 'vhbb' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only_vhbb").set_frozen(True)
    
    #bins_vhbb_stxs = set(cb.cp().channel(['vhbb_stxs']).bin_set())
    #bins_vhbb_stxs_2016 = []
    #for cat in bins_vhbb_stxs:
    #    if not '2017' in cat:
    #        bins_vhbb_stxs_2016.append(cat)
    #
    #vhbb_stxs_procs = set(cb.cp().channel(['vhbb_stxs']).process_set())
    #for b in bins_vhbb_stxs_2016:
    #    for p in vhbb_stxs_procs:
    #        cb.cp().channel(['vhbb_stxs']).bin([b]).process([p]).AddSyst(cb,'rate_lumiscale_2016_only_vhbb', 'rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))
    #     cb.cp().channel(['vhbb_stxs']).bin([b]).AddSyst(cb,'rate_lumiscale_2016_only_vhbb', 'rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))
    #
    #if (len(select_chns) > 0 and 'vhbb_stxs' in select_chns) and 'vhbb_stxs' not in veto_chns:
    #    cb.cp().GetParameter("rate_lumiscale_2016_only_vhbb").set_frozen(True)
    

    #Update tthbb_partial. All processes from MC except ddQCD
    tthbb_partial_procs = set(cb.cp().channel(['tth_hbb_partial']).process_set())
    if len(tthbb_partial_procs) > 0:
        tthbb_partial_procs.remove('ddQCD')

    for p in tthbb_partial_procs:
        cb.cp().channel(['tth_hbb_partial']).process([p]).AddSyst(cb,'rate_lumiscale_2016_only_tthbb', 'rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))

    if (len(select_chns) > 0 and 'tth_hbb_partial' in select_chns) and 'tth_hbb_partial' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only_tthbb").set_frozen(True)

    #Update boosted hbb (partial). All processes from MC except qcd
    hbb_boosted_partial_bins = set(cb.cp().channel(['hbb_boosted_partial']).bin_set())
    hbb_boosted_partial_bins_2016 = []
    for cat in hbb_boosted_partial_bins:
        if '2016' in cat:
            hbb_boosted_partial_bins_2016.append(cat)

    hbb_boosted_partial_procs = set(cb.cp().channel(['hbb_boosted_partial']).process_set())

    if len(hbb_boosted_partial_procs) > 0:
        hbb_boosted_partial_procs.remove('qcd')

    for b in hbb_boosted_partial_bins_2016:
        for p in hbb_boosted_partial_procs:
            cb.cp().channel(['hbb_boosted_partial']).bin([b]).process([p]).AddSyst(cb, 'rate_lumiscale_2016_only_hbbboosted','rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))

    if (len(select_chns) > 0 and 'hbb_boosted_partial' in select_chns) and 'hbb_boosted_partial' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only_hbbboosted").set_frozen(True)

    #Update hzg.
    hzg_procs = set(cb.cp().channel(['hzg']).process_set())
    hzg_procs_16 = []

    for proc in hzg_procs:
        if '16' in proc:
            hzg_procs_16.append(proc)

    for p in hzg_procs_16:
        cb.cp().channel(['hzg']).process([p]).AddSyst(cb,'rate_lumiscale_2016_only_hzg', 'rateParam', ch.SystMap()( lumi_new[0]/lumi_old[0]))

    if (len(select_chns) > 0 and 'hzg' in select_chns) and 'hzg' not in veto_chns:
        cb.cp().GetParameter("rate_lumiscale_2016_only_hzg").set_frozen(True)



    def scale_to_fullrun2(val, y):
        '''Scale value to the relative fraction of the luminosity'''
        return val * lumi_new[y]/np.sum(lumi_new)

    def updateHmmUncert(s,vals=[0.01,0.0,0.0]):
        s.set_type('lnN')
        if (s.bin(),s.process()) in bin_proc['2016_only']: utils.UpdateUncert(s,1.+vals[0])
        elif (s.bin(),s.process()) in bin_proc['2017_only']: utils.UpdateUncert(s,1.+vals[1])
        elif (s.bin(),s.process()) in bin_proc['2018_only']: utils.UpdateUncert(s,1.+vals[2])
        elif (s.bin(),s.process()) in bin_proc['Run2']: utils.UpdateUncert(s,1.+scale_to_fullrun2(vals[0],0)+scale_to_fullrun2(vals[1],1)+scale_to_fullrun2(vals[2],2))
        else:
            print(("ERROR", "Unable to update UNcertainty",s.bin(),s.process(),s.name()))
            raise ValueError()


    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_2016']).ForEachSyst(lambda s:  updateHmmUncert(s,[0.01,0.,0.]) )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_2017']).ForEachSyst(lambda s:  updateHmmUncert(s,[0.,.02,0.])   )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_2018']).ForEachSyst(lambda s:  updateHmmUncert(s,[0.,0.,.015])  )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_BCC']).ForEachSyst(lambda s:   updateHmmUncert(s,[0.002,.003,.002])  )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_BBD']).ForEachSyst(lambda s:  updateHmmUncert(s,[0.0,.006,.002])  )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_GS']).ForEachSyst(lambda s:   updateHmmUncert(s,[0.001,.001,.001])  )
    cb.cp().channel(['hmm']).syst_name(['lumi_13TeV_XY']).ForEachSyst(lambda s:   updateHmmUncert(s,[0.005,.008,.02])  )

# Scale signal process yields to mH=125.38 GeV
# XS arrays have values at 125, 125.09, 125.38 GeV to accommodate the different scalings needed.
ggh_xs = np.array([48.58,48.52,48.313802])
vbf_xs = np.array([3.782, 3.779, 3.7706137])
tth_xs = np.array([0.5071,0.5065,0.50347179])
wh_xs = np.array([1.373,1.369,1.3587757])
zh_xs = np.array([0.8839,0.8824,0.87707138])
ggzh_xs = np.array([0.1227,0.1227,0.12234856])
thq_xs = np.array([0.07713,0.07714,0.077031100])

hbb_br = np.array([0.5824,0.5809,0.576316])
hcc_br = np.array([0.02891,0.02884,0.0286158])
htt_br = np.array([0.06272,0.06256,0.0621104])
hmm_br = np.array([0.0002176,0.0002171,0.000215408])
hww_br = np.array([0.2137,0.2152,0.219967])
hzz_br = np.array([0.02619,0.02641,0.0271116])
hzg_br = np.array([0.001533,0.001541,0.00156509])
hgg_br = np.array([0.00227,0.00227,0.00226991])
hgluglu_br = np.array([0.0819,0.0818,0.0815118])

# Hbb boosted (partial) is simple as no stxs in the card being used currently. Yields were fixed at mH=125 GeV
cb.cp().channel(['hbb_boosted_partial']).process(['ggH_hbb']).AddSyst(cb, 'rate_gghbbscal_hbbboosted','rateParam', ch.SystMap()( ggh_xs[2]*hbb_br[2]/(ggh_xs[0]*hbb_br[0])))
cb.cp().channel(['hbb_boosted_partial']).process(['qqH_hbb']).AddSyst(cb, 'rate_qqhbbscal_hbbboosted','rateParam', ch.SystMap()( vbf_xs[2]*hbb_br[2]/(vbf_xs[0]*hbb_br[0])))
cb.cp().channel(['hbb_boosted_partial']).process(['ttH_hbb']).AddSyst(cb, 'rate_tthbbscal_hbbboosted','rateParam', ch.SystMap()( tth_xs[2]*hbb_br[2]/(tth_xs[0]*hbb_br[0])))
cb.cp().channel(['hbb_boosted_partial']).process(['ZH_hbb']).AddSyst(cb, 'rate_zhbbscal_hbbboosted','rateParam', ch.SystMap()( zh_xs[2]*hbb_br[2]/(zh_xs[0]*hbb_br[0])))
cb.cp().channel(['hbb_boosted_partial']).process(['WH_hbb']).AddSyst(cb, 'rate_whbbscal_hbbboosted','rateParam', ch.SystMap()( wh_xs[2]*hbb_br[2]/(wh_xs[0]*hbb_br[0])))

if (len(select_chns) > 0 and 'hbb_boosted_partial' in select_chns) and 'hbb_boosted_partial' not in veto_chns:
    cb.cp().GetParameter("rate_gghbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_qqhbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_tthbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_zhbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_whbbscal_hbbboosted").set_frozen(True)


# Hbb boosted. Yields fixed at mH=125 GeV
hbb_boosted_stxs_signals = set(cb.cp().channel(['hbb_boosted_stxs']).signals().process_set())
for proc in hbb_boosted_stxs_signals:
    splitproc = proc.split('_')
    if splitproc[0]=='ggH':
        cb.cp().channel(['hbb_boosted_stxs']).process([proc]).AddSyst(cb, 'rate_gghbbscal_hbbboosted','rateParam', ch.SystMap()( ggh_xs[2]*hbb_br[2]/(ggh_xs[0]*hbb_br[0])))
    if splitproc[0]=='qqH':
        cb.cp().channel(['hbb_boosted_stxs']).process([proc]).AddSyst(cb, 'rate_qqhbbscal_hbbboosted','rateParam', ch.SystMap()( vbf_xs[2]*hbb_br[2]/(vbf_xs[0]*hbb_br[0])))
    if splitproc[0]=='ttH':
        cb.cp().channel(['hbb_boosted_stxs']).process([proc]).AddSyst(cb, 'rate_tthbbscal_hbbboosted','rateParam', ch.SystMap()( tth_xs[2]*hbb_br[2]/(tth_xs[0]*hbb_br[0])))
    #No ZH, WH, ggZH in the datacard

if (len(select_chns) > 0 and 'hbb_boosted_stxs' in select_chns) and 'hbb_boosted_stxs' not in veto_chns:
    cb.cp().GetParameter("rate_gghbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_qqhbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_tthbbscal_hbbboosted").set_frozen(True)

hbb_boosted_incl_signals = set(cb.cp().channel(['hbb_boosted_incl']).signals().process_set())
for proc in hbb_boosted_incl_signals:
    splitproc = proc.split('_')
    if splitproc[0]=='ggH':
        cb.cp().channel(['hbb_boosted_incl']).process([proc]).AddSyst(cb, 'rate_gghbbscal_hbbboosted','rateParam', ch.SystMap()( ggh_xs[2]*hbb_br[2]/(ggh_xs[0]*hbb_br[0])))
    if splitproc[0]=='qqH':
        cb.cp().channel(['hbb_boosted_incl']).process([proc]).AddSyst(cb, 'rate_qqhbbscal_hbbboosted','rateParam', ch.SystMap()( vbf_xs[2]*hbb_br[2]/(vbf_xs[0]*hbb_br[0])))
    if splitproc[0]=='WH':
        cb.cp().channel(['hbb_boosted_incl']).process([proc]).AddSyst(cb, 'rate_whbbscal_hbbboosted','rateParam', ch.SystMap()( wh_xs[2]*hbb_br[2]/(wh_xs[0]*hbb_br[0])))
    if splitproc[0]=='ZH':
        cb.cp().channel(['hbb_boosted_incl']).process([proc]).AddSyst(cb, 'rate_zhbbscal_hbbboosted','rateParam', ch.SystMap()( zh_xs[2]*hbb_br[2]/(zh_xs[0]*hbb_br[0])))
    if splitproc[0]=='ttH':
        cb.cp().channel(['hbb_boosted_incl']).process([proc]).AddSyst(cb, 'rate_tthbbscal_hbbboosted','rateParam', ch.SystMap()( tth_xs[2]*hbb_br[2]/(tth_xs[0]*hbb_br[0])))
    #ggZH in the datacard

if (len(select_chns) > 0 and 'hbb_boosted_incl' in select_chns) and 'hbb_boosted_incl' not in veto_chns:
    cb.cp().GetParameter("rate_gghbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_qqhbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_tthbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_whbbscal_hbbboosted").set_frozen(True)
    cb.cp().GetParameter("rate_zhbbscal_hbbboosted").set_frozen(True)


# tth multilepton. Yields fixed at mH=125 GeV
tthll_signals = set(cb.cp().channel(['tth_multilepton']).signals().process_set())
for proc in tthll_signals:
    splitproc = proc.split('_')
    if splitproc[0]=='ggH':
        if splitproc[-1]=='htt': #No ggH ww in the datacard
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_gghttscal_tthll','rateParam', ch.SystMap()( ggh_xs[2]*htt_br[2]/(ggh_xs[0]*htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_gghzzscal_tthll','rateParam', ch.SystMap()( ggh_xs[2]*hzz_br[2]/(ggh_xs[0]*hzz_br[0])))
    if splitproc[0]=='qqH':
        if splitproc[-1]=='htt':#No VBF ZZ,WW in the datacard
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_qqhttscal_tthll','rateParam', ch.SystMap()( vbf_xs[2]*htt_br[2]/(vbf_xs[0]*htt_br[0])))
    if splitproc[0]=='ttH':
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_tthttscal_tthll','rateParam', ch.SystMap()( tth_xs[2]*htt_br[2]/(tth_xs[0]*htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_tthzzscal_tthll','rateParam', ch.SystMap()( tth_xs[2]*hzz_br[2]/(tth_xs[0]*hzz_br[0])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_tthwwscal_tthll','rateParam', ch.SystMap()( tth_xs[2]*hww_br[2]/(tth_xs[0]*hww_br[0])))
    if splitproc[0]=='tHq':
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thqttscal_tthll','rateParam', ch.SystMap()( thq_xs[2]*htt_br[2]/(thq_xs[0]*htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thqzzscal_tthll','rateParam', ch.SystMap()( thq_xs[2]*hzz_br[2]/(thq_xs[0]*hzz_br[0])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thqwwscal_tthll','rateParam', ch.SystMap()( thq_xs[2]*hww_br[2]/(thq_xs[0]*hww_br[0])))
    if splitproc[0]=='tHW':
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thwttscal_tthll','rateParam', ch.SystMap()( htt_br[2]/(htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thwzzscal_tthll','rateParam', ch.SystMap()( hzz_br[2]/(hzz_br[0])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_thwwwscal_tthll','rateParam', ch.SystMap()( hww_br[2]/(hww_br[0])))
    if splitproc[0]=='ZH':
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_zhttscal_tthll','rateParam', ch.SystMap()( zh_xs[2]*htt_br[2]/(zh_xs[0]*htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_zhzzscal_tthll','rateParam', ch.SystMap()( zh_xs[2]*hzz_br[2]/(zh_xs[0]*hzz_br[0])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_zhwwscal_tthll','rateParam', ch.SystMap()( zh_xs[2]*hww_br[2]/(zh_xs[0]*hww_br[0])))
    if splitproc[0]=='WH':
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_whttscal_tthll','rateParam', ch.SystMap()( wh_xs[2]*htt_br[2]/(wh_xs[0]*htt_br[0])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_whzzscal_tthll','rateParam', ch.SystMap()( wh_xs[2]*hzz_br[2]/(wh_xs[0]*hzz_br[0])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_multilepton']).process([proc]).AddSyst(cb, 'rate_whwwscal_tthll','rateParam', ch.SystMap()( wh_xs[2]*hww_br[2]/(wh_xs[0]*hww_br[0])))

if (len(select_chns) > 0 and 'tth_multilepton' in select_chns) and 'tth_multilepton' not in veto_chns:
    if cb.cp().GetParameter("rate_gghttscal_tthll") : cb.cp().GetParameter("rate_gghttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_gghzzscal_tthll") : cb.cp().GetParameter("rate_gghzzscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_qqhttscal_tthll") : cb.cp().GetParameter("rate_qqhttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_tthttscal_tthll") : cb.cp().GetParameter("rate_tthttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_tthwwscal_tthll") : cb.cp().GetParameter("rate_tthwwscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_tthzzscal_tthll") : cb.cp().GetParameter("rate_tthzzscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thqttscal_tthll") : cb.cp().GetParameter("rate_thqttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thqwwscal_tthll") : cb.cp().GetParameter("rate_thqwwscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thqzzscal_tthll") : cb.cp().GetParameter("rate_thqzzscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thwttscal_tthll") : cb.cp().GetParameter("rate_thwttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thwwwscal_tthll") : cb.cp().GetParameter("rate_thwwwscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_thwzzscal_tthll") : cb.cp().GetParameter("rate_thwzzscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_whttscal_tthll" ) : cb.cp().GetParameter("rate_whttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_whwwscal_tthll" ) : cb.cp().GetParameter("rate_whwwscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_whzzscal_tthll" ) : cb.cp().GetParameter("rate_whzzscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_zhttscal_tthll" ) : cb.cp().GetParameter("rate_zhttscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_zhwwscal_tthll" ) : cb.cp().GetParameter("rate_zhwwscal_tthll").set_frozen(True)
    if cb.cp().GetParameter("rate_zhzzscal_tthll" ) : cb.cp().GetParameter("rate_zhzzscal_tthll").set_frozen(True)

#ttHbb partial - set at 125.09 GeV, legacy analysis scaled to 125.38 GeV
tthbb_signals = set(cb.cp().channel(['tth_hbb_partial']).signals().process_set())
for proc in tthbb_signals:
    splitproc = proc.split('_')
    if splitproc[0]=='ttH':
        if splitproc[-1]=='hbb':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthbbscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hbb_br[2]/(tth_xs[1]*hbb_br[1])))
        if splitproc[-1]=='htt':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthttscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*htt_br[2]/(tth_xs[1]*htt_br[1])))
        if splitproc[-1]=='hzz':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthzzscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hzz_br[2]/(tth_xs[1]*hzz_br[1])))
        if splitproc[-1]=='hww':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthwwscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hww_br[2]/(tth_xs[1]*hww_br[1])))
        if splitproc[-1]=='hgg':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthggscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hgg_br[2]/(tth_xs[1]*hgg_br[1])))
        if splitproc[-1]=='hzg':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthzgscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hzg_br[2]/(tth_xs[1]*hzg_br[1])))
        if splitproc[-1]=='hcc':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthccscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hcc_br[2]/(tth_xs[1]*hcc_br[1])))
        if splitproc[-1]=='hgluglu':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_tthglugluscal_tthbb','rateParam', ch.SystMap()( tth_xs[2]*hgluglu_br[2]/(tth_xs[1]*hgluglu_br[1])))
    if splitproc[0]=='tHq':
        if splitproc[-1]=='hbb':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_thqbbscal_tthbb','rateParam', ch.SystMap()( thq_xs[2]*hbb_br[2]/(thq_xs[1]*hbb_br[1])))
    if splitproc[0]=='tHW':
        if splitproc[-1]=='hbb':
            cb.cp().channel(['tth_hbb_partial']).process([proc]).AddSyst(cb, 'rate_thwbbscal_tthbb','rateParam', ch.SystMap()( hbb_br[2]/(hbb_br[1])))

if (len(select_chns) > 0 and 'tth_hbb_partial' in select_chns) and 'tth_hbb_partial' not in veto_chns:
    if cb.cp().GetParameter("rate_tthbbscal_tthbb") : cb.cp().GetParameter("rate_tthbbscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthttscal_tthbb") : cb.cp().GetParameter("rate_tthttscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthzzscal_tthbb") : cb.cp().GetParameter("rate_tthzzscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthwwscal_tthbb") : cb.cp().GetParameter("rate_tthwwscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthggscal_tthbb") : cb.cp().GetParameter("rate_tthggscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthzgscal_tthbb") : cb.cp().GetParameter("rate_tthzgscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthccscal_tthbb") : cb.cp().GetParameter("rate_tthccscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_tthglugluscal_tthbb") : cb.cp().GetParameter("rate_tthglugluscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_thqbbscal_tthbb") : cb.cp().GetParameter("rate_thqbbscal_tthbb").set_frozen(True)
    if cb.cp().GetParameter("rate_thwbbscal_tthbb") : cb.cp().GetParameter("rate_thwbbscal_tthbb").set_frozen(True)


#VHbb - already at 125.09 GeV

cb.cp().channel(['vhbb']).process(['ZH_lep_hbb']).AddSyst(cb, 'rate_zhbbscal_vhbb','rateParam', ch.SystMap()( zh_xs[2]*hbb_br[2]/(zh_xs[1]*hbb_br[1])))
cb.cp().channel(['vhbb']).process(['ggZH_lep_hbb']).AddSyst(cb, 'rate_ggzhbbscal_vhbb','rateParam', ch.SystMap()( ggzh_xs[2]*hbb_br[2]/(ggzh_xs[1]*hbb_br[1])))
cb.cp().channel(['vhbb']).process(['WH_lep_hbb']).AddSyst(cb, 'rate_whbbscal_vhbb','rateParam', ch.SystMap()( wh_xs[2]*hbb_br[2]/(wh_xs[1]*hbb_br[1])))

if (len(select_chns) > 0 and 'vhbb' in select_chns) and 'vhbb' not in veto_chns:
    cb.cp().GetParameter("rate_zhbbscal_vhbb").set_frozen(True)
    cb.cp().GetParameter("rate_ggzhbbscal_vhbb").set_frozen(True)
    cb.cp().GetParameter("rate_whbbscal_vhbb").set_frozen(True)

# VBF H->bb - yields in original datacard at 125.0 GeV, scale to 125.38 GeV
# TODO: check if bias terms should be here. Is normalisation a fraction of signal process?
cb.cp().channel(['vbfhbb']).process(['ggH_hbb','ggH_hbb_bias']).AddSyst(cb, 'rate_gghbbscal_vbfhbb','rateParam', ch.SystMap()( ggh_xs[2]*hbb_br[2]/(ggh_xs[0]*hbb_br[0])))
cb.cp().channel(['vbfhbb']).process(['qqH_hbb','qqH_hbb_bias']).AddSyst(cb, 'rate_qqhbbscal_vbfhbb','rateParam', ch.SystMap()( vbf_xs[2]*hbb_br[2]/(vbf_xs[0]*hbb_br[0])))

if (len(select_chns) > 0 and 'vbfhbb' in select_chns) and 'vbfhbb' not in veto_chns:
    cb.cp().GetParameter("rate_gghbbscal_vbfhbb").set_frozen(True)
    cb.cp().GetParameter("rate_qqhbbscal_vbfhbb").set_frozen(True)


####################################################33

### larger fixes in nuisances.
if True: ## fix hzz/vhbb/hbb_boosted lumi
    # remove bogous uncertainties
    for name in ['CMS_lumi_201620172018_2016','CMS_lumi_201620172018_2017','CMS_lumi_201620172018_2018','CMS_lumi_20162017_2016','CMS_lumi_20162017_2017','CMS_lumi_20172018_2017','CMS_lumi_20172018_2018']: cb.FilterSysts(lambda x: x.channel()=='hzz' and x.name()==name)
    for name in ['lumi_13TeV_correlated','lumi_13TeV_1718']: cb.FilterSysts(lambda x: x.channel()=='tth_hbb' and x.name()==name)
    #for name in ['lumi_13TeV_20162017','lumi_13TeV_20172018','lumi_13TeV_Run2']: cb.FilterSysts(lambda x: x.channel()=='vhbb' and x.name()==name) ## LEGACY
    for name in ['lumi_13TeV_correlated','lumi_13TeV_1718','lumi_13TeV_1516']:cb.FilterSysts(lambda x: (x.channel()=='hinv') and x.name()==name)
    for name in ['lumi_13TeV_correlated','lumi_13TeV_1718','lumi_13TeV_BBD','lumi_13TeV_BCC','lumi_13TeV_DB','lumi_13TeV_GS','lumi_13TeV_LS','lumi_13TeV_XY']:cb.FilterSysts(lambda x: x.channel()=='htt_incl' and x.name()==name)
    for name in ['lumi_13TeV_correlated','lumi_13TeV_1718','lumi_13TeV_BBD','lumi_13TeV_BCC','lumi_13TeV_DB','lumi_13TeV_GS','lumi_13TeV_LS','lumi_13TeV_XY']:cb.FilterSysts(lambda x: x.channel()=='htt_stxs' and x.name()==name)
    for name in ['lumi_13TeV_correlated','lumi_13TeV_1718']:cb.FilterSysts(lambda x: x.channel()=='hww' and x.name()==name)
    for name in ['lumi_13TeV_BD_DB_GS', 'lumi_13TeV_XY','lumi_13TeV_LS_BCC']: cb.FilterSysts(lambda x: x.channel()=='vhbb' and x.name()==name)
    #no name lumi_13TeV__BD_DB_GS, lumi_13TeV_XY, lumi_13TeV_LS_BCC in vhbb_stxs
    #for name in ['lumi_13TeV_BD_DB_GS', 'lumi_13TeV_XY','lumi_13TeV_LS_BCC']: cb.FilterSysts(lambda x: x.channel()=='vhbb_stxs' and x.name()==name)
    for name in ['lumi_13TeV_BBDefl', 'lumi_13TeV_CurrCalib','lumi_13TeV_DynBeta','lumi_13TeV_Ghosts','lumi_13TeV_LSCale','lumi_13TeV_XYFact']: cb.FilterSysts(lambda x: x.channel()=='hww' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Dynamic_Beta','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='hzg' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Dynamic_Beta','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='hgg' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='hmm' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='hww' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='hww_stxs' and x.name()==name)
    for name in ['lumi_13TeV_Beam_Beam_Deflection','lumi_13TeV_Beam_Current_Calibration','lumi_13TeV_Ghosts_And_Satellites','lumi_13TeV_Length_Scale','lumi_13TeV_X_Y_Factorization']: cb.FilterSysts(lambda x: x.channel()=='tth_multilepton' and x.name()==name)
    for name in ['lumi_13TeV_20162017','lumi_13TeV_20172018','lumi_13TeV_Run2']: cb.FilterSysts(lambda x: x.channel()=='vhbb_stxs' and x.name()==name)
    for name in ['CMS_lumi_13TeV_correlated','CMS_lumi_13TeV_correlated_20172018']: cb.FilterSysts(lambda x: x.channel()=='hbb_boosted_stxs' and x.name()==name)
    for name in ['CMS_lumi_13TeV_correlated','CMS_lumi_13TeV_correlated_20172018']: cb.FilterSysts(lambda x: x.channel()=='hbb_boosted_incl' and x.name()==name)

    ## Use minimal correlation scheme
    #Uncorrelated 2016,1.0,0.0,0.0
    #Uncorrelated 2017,0.0,2.0,0.0
    #Uncorrelated 2018,0.0,0.0,1.5
    #Correlated        0.6,0.9,2.0
    #Correlated 1718   0.0,0.6,0.2

    #channels = ['hzz','hbb_boosted','vhbb','hinv','htt_incl','htt_stxs','hww','tth_hbb']
    channels = ['hzz','hbb_boosted_partial','vhbb_stxs','hinv','htt_incl','htt_stxs','hww','tth_hbb']
    cb.cp().channel(channels).syst_name(['lumi_13TeV_2016']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.010))
    cb.cp().channel(channels).syst_name(['lumi_13TeV_2017']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.020))
    cb.cp().channel(channels).syst_name(['lumi_13TeV_2018']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.015))
    ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2016' in x.name() else 1.009 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_Correlated')] )
    ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Correlated1718')] )
    #rename them to update scheme
    cb.cp().syst_name(['lumi_13TeV_2016']).channel(channels).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2016'))
    cb.cp().syst_name(['lumi_13TeV_2017']).channel(channels).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2017'))
    cb.cp().syst_name(['lumi_13TeV_2018']).channel(channels).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2018'))


    # Old scheme with full set of nuisance parameters (outdated)
    #Beam current calibration,0.2,0.3,0.2
    #Beam-beam effects (17-18),0.0,0.6,0.2
    #Ghosts and satellites,0.1,0.1,0.1
    #Length scale,0.3,0.3,0.2
    #X-Y factorization,0.5,0.8,2.0
    #channels= ['hzz','hbb_boosted','vhbb','hinv'] # LEGACY
    #ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.005 if '2016' in x.name() else 1.008 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_X_Y_Factorization')] )
    #ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.002 if '2016' in x.name() else 1.003 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Beam_Current_Calibration')] )
    #ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.003 if '2016' in x.name() else 1.003 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Length_Scale')] )
    #ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2016','lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.001) , x.set_name('lumi_13TeV_Ghosts_And_Satellites')] )
    #ch.CloneSysts(cb.cp().channel(channels).syst_name(['lumi_13TeV_2017','lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Beam_Beam_Deflection')] )

    channels_lumi = ['hzg','hgg','hmm','hww','hww_stxs','tth_multilepton'] #Already has the right names, but need to update the values just the same
    cb.cp().channel(channels_lumi).syst_name(['lumi_13TeV_Uncorrelated_2016']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.010))
    cb.cp().channel(channels_lumi).syst_name(['lumi_13TeV_Uncorrelated_2017']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.020))
    cb.cp().channel(channels_lumi).syst_name(['lumi_13TeV_Uncorrelated_2018']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.015))
    ch.CloneSysts(cb.cp().channel(channels_lumi).syst_name(['lumi_13TeV_Uncorrelated_2016','lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2016' in x.name() else 1.009 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_Correlated')] )
    ch.CloneSysts(cb.cp().channel(channels_lumi).syst_name(['lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Correlated1718')] )

    cb.cp().channel(['hbb_boosted_stxs']).syst_name(['CMS_lumi_13TeV_2016']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.010))
    cb.cp().channel(['hbb_boosted_stxs']).syst_name(['CMS_lumi_13TeV_2017']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.020))
    cb.cp().channel(['hbb_boosted_stxs']).syst_name(['CMS_lumi_13TeV_2018']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.015))
    ch.CloneSysts(cb.cp().channel(['hbb_boosted_stxs']).syst_name(['CMS_lumi_13TeV_2016','CMS_lumi_13TeV_2017','CMS_lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2016' in x.name() else 1.009 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_Correlated')] )
    ch.CloneSysts(cb.cp().channel(['hbb_boosted_stxs']).syst_name(['CMS_lumi_13TeV_2017','CMS_lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Correlated1718')] )
    cb.cp().syst_name(['CMS_lumi_13TeV_2016']).channel(['hbb_boosted_stxs']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2016'))
    cb.cp().syst_name(['CMS_lumi_13TeV_2017']).channel(['hbb_boosted_stxs']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2017'))
    cb.cp().syst_name(['CMS_lumi_13TeV_2018']).channel(['hbb_boosted_stxs']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2018'))

    cb.cp().channel(['hbb_boosted_incl']).syst_name(['CMS_lumi_13TeV_2016']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.010))
    cb.cp().channel(['hbb_boosted_incl']).syst_name(['CMS_lumi_13TeV_2017']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.020))
    cb.cp().channel(['hbb_boosted_incl']).syst_name(['CMS_lumi_13TeV_2018']).ForEachSyst(lambda x: utils.UpdateUncert(x,1.015))
    ch.CloneSysts(cb.cp().channel(['hbb_boosted_incl']).syst_name(['CMS_lumi_13TeV_2016','CMS_lumi_13TeV_2017','CMS_lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2016' in x.name() else 1.009 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_Correlated')] )
    ch.CloneSysts(cb.cp().channel(['hbb_boosted_incl']).syst_name(['CMS_lumi_13TeV_2017','CMS_lumi_13TeV_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Correlated1718')] )
    cb.cp().syst_name(['CMS_lumi_13TeV_2016']).channel(['hbb_boosted_incl']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2016'))
    cb.cp().syst_name(['CMS_lumi_13TeV_2017']).channel(['hbb_boosted_incl']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2017'))
    cb.cp().syst_name(['CMS_lumi_13TeV_2018']).channel(['hbb_boosted_incl']).ForEachSyst(lambda x: x.set_name('lumi_13TeV_Uncorrelated_2018'))

    # Old scheme with full set of nuisance parameters (outdated)
    #ch.CloneSysts(cb.cp().channel(channels_hzg).syst_name(['lumi_13TeV_Uncorrelated_2016','lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.005 if '2016' in x.name() else 1.008 if '2017' in x.name() else 1.02 ) , x.set_name('lumi_13TeV_X_Y_Factorization')] )
    #ch.CloneSysts(cb.cp().channel(channels_hzg).syst_name(['lumi_13TeV_Uncorrelated_2016','lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.002 if '2016' in x.name() else 1.003 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Beam_Current_Calibration')] )
    #ch.CloneSysts(cb.cp().channel(channels_hzg).syst_name(['lumi_13TeV_Uncorrelated_2016','lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.003 if '2016' in x.name() else 1.003 if '2017' in x.name() else 1.002 ) , x.set_name('lumi_13TeV_Length_Scale')] )
    #ch.CloneSysts(cb.cp().channel(channels_hzg).syst_name(['lumi_13TeV_Uncorrelated_2016','lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.001) , x.set_name('lumi_13TeV_Ghosts_And_Satellites')] )
    #ch.CloneSysts(cb.cp().channel(channels_hzg).syst_name(['lumi_13TeV_Uncorrelated_2017','lumi_13TeV_Uncorrelated_2018']),cb,lambda x : [ utils.UpdateUncert(x,1.006 if '2017' in x.name() else 1.002) , x.set_name('lumi_13TeV_Beam_Beam_Deflection')] )

    ### tth(bb) partial is special because it has the lumi applied as a shape to the QCD background. Need to just exclude the uncertainty for that process since we can't correct it.
    cb.FilterSysts(lambda x: x.channel()=='tth_hbb_partial' and x.name()=='lumi_13TeV_2016')
    tthbb_procs_for_lumi = set(cb.cp().channel(['tth_hbb_partial']).process_set())
    if len(tthbb_procs_for_lumi) > 0:
        tthbb_procs_for_lumi.remove('ddQCD')
    for p in tthbb_procs_for_lumi:
        cb.cp().channel(['tth_hbb_partial']).process([p]).AddSyst(cb, 'lumi_13TeV_Uncorrelated_2016', "lnN", ch.SystMap()(1.01));
    ch.CloneSysts(cb.cp().channel(['tth_hbb_partial']).syst_name(['lumi_13TeV_Uncorrelated_2016']), cb, lambda x : [ utils.UpdateUncert(x,1.006), x.set_name('lumi_13TeV_Correlated')] )
    #ch.CloneSysts(cb.cp().channel(['tth_hbb_partial']).syst_name(['lumi_13TeV_Uncorrelated_2016']), cb, lambda x: [utils.UpdateUncert(x,1.005), x.set_name('lumi_13TeV_X_Y_Factorization')])
    #ch.CloneSysts(cb.cp().channel(['tth_hbb_partial']).syst_name(['lumi_13TeV_Uncorrelated_2016']), cb, lambda x: [utils.UpdateUncert(x,1.002), x.set_name('lumi_13TeV_Beam_Current_Calibration')])
    #ch.CloneSysts(cb.cp().channel(['tth_hbb_partial']).syst_name(['lumi_13TeV_Uncorrelated_2016']), cb, lambda x: [utils.UpdateUncert(x,1.003), x.set_name('lumi_13TeV_Length_Scale')])
    #ch.CloneSysts(cb.cp().channel(['tth_hbb_partial']).syst_name(['lumi_13TeV_Uncorrelated_2016']), cb, lambda x: [utils.UpdateUncert(x,1.001), x.set_name('lumi_13TeV_Ghosts_And_Satellites')])


#Fix theory uncertainties :
#Some renaming happens later
ch.CloneSysts(cb.cp().channel(['hmm']).syst_name(['QCDscale_ggH']), cb, lambda x: [utils.UpdateUncert(x,1.021), x.set_name('THU_ggH_Res')])
cb.cp().channel(['hmm']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.046)])
cb.cp().channel(['hmm']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [x.set_name('THU_ggH_Mu')])
cb.cp().channel(['hmm']).syst_name(['QCDscale_WH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.005)])
cb.cp().channel(['hmm']).syst_name(['QCDscale_ttH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,0.908,1.058)])

cb.cp().channel(['hzg']).syst_name(['QCDscale_ttH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,0.908,1.058)])
ch.CloneSysts(cb.cp().channel(['hzg']).syst_name(['QCDscale_ggH']), cb, lambda x: [utils.UpdateUncert(x,1.021), x.set_name('THU_ggH_Res')])
cb.cp().channel(['hzg']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.046)])
cb.cp().channel(['hzg']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [x.set_name('THU_ggH_Mu')])
cb.cp().channel(['hzg']).syst_name(['QCDscale_qqH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.004)])

whprocs_hzg = ['WH_16_mu_hzg','WH_17_mu_hzg','WH_18_mu_hzg','WH_16_ele_hzg','WH_17_ele_hzg','WH_18_ele_hzg','WH_bkg_16_hmm','WH_bkg_17_hmm','WH_bkg_18_hmm']
zhprocs_hzg = ['ZH_16_mu_hzg','ZH_17_mu_hzg','ZH_18_mu_hzg','ZH_16_ele_hzg','ZH_17_ele_hzg','ZH_18_ele_hzg','ZH_bkg_16_hmm','ZH_bkg_17_hmm','ZH_bkg_18_hmm']
cb.cp().channel(['hzg']).process(whprocs_hzg).AddSyst(cb,'QCDscale_WH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['hzg']).process(zhprocs_hzg).AddSyst(cb,'QCDscale_ZH','lnN', ch.SystMap()(1.005))
cb.FilterSysts(lambda x: x.channel()=='hzg' and x.name()=='QCDscale_VH')

cb.FilterSysts(lambda x: x.channel()=='hww' and x.name()=='THU_VBF_Yield') #Duplicate but not in all categories - drop this one and rename the QCDscale_qqH uncert to THU_VBF_Yield.
cb.cp().channel(['hww']).syst_name(['QCDscale_qqH']).ForEachSyst(lambda x: [x.set_name('THU_VBF_Yield')])
cb.cp().channel(['hww']).process(['WH_hww','WH_htt']).AddSyst(cb,'QCDscale_WH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['hww']).process(['ZH_hww','ZH_htt']).AddSyst(cb,'QCDscale_ZH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['hww']).process(['ggZH_hww']).AddSyst(cb,'QCDscale_ggZH','lnN', ch.SystMap()((0.811,1.251)))
cb.FilterSysts(lambda x: x.channel()=='hww' and x.name()=='QCDscale_VH')

cb.cp().channel(['htt_incl','htt_stxs']).syst_name(['QCDScale_qqH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.004)])
cb.cp().channel(['htt_incl','htt_stxs']).syst_name(['QCDScale_ttH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,0.908,1.058)])
ch.CloneSysts(cb.cp().channel(['htt_incl','htt_stxs']).syst_name(['QCDScale_ggHWW']), cb, lambda x: [utils.UpdateUncert(x,1.021), x.set_name('THU_ggH_Res')])
cb.cp().channel(['htt_incl','htt_stxs']).syst_name(['QCDScale_ggHWW']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.046), x.set_name('THU_ggH_Mu')])
cb.FilterSysts(lambda x: x.channel()=='htt_incl' and x.name()=='QCDScale_VH')
cb.FilterSysts(lambda x: x.channel()=='htt_stxs' and x.name()=='QCDScale_VH')
cb.cp().channel(['htt_incl','htt_stxs']).process(['WH_hww','WH_lep_htt','WH_had_htt']).AddSyst(cb,'QCDscale_WH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['htt_incl','htt_stxs']).process(['ZH_hww','ZH_lep_htt','ZH_had_htt']).AddSyst(cb,'QCDscale_ZH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['htt_incl','htt_stxs']).process(['ggZH_hww','ggZH_lep_htt']).AddSyst(cb,'QCDscale_ggZH','lnN', ch.SystMap()((0.811,1.251)))

cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_WH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.005)])
cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_ZH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.005)])
cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_qqH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.004), x.set_name('THU_VBF_Yield')])
ch.CloneSysts(cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_ggH']), cb, lambda x:[utils.UpdateUncert(x,1.021), x.set_name('THU_ggH_Res')])
cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.046), x.set_name('THU_ggH_Mu')])
cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_tHq']).ForEachSyst(lambda x: [utils.UpdateUncert(x, 0.851,1.065)])
cb.cp().channel(['tth_multilepton']).syst_name(['QCDscale_tHW']).ForEachSyst(lambda x: [utils.UpdateUncert(x, 0.933,1.049)])

# TODO: this would add PDF set uncertainties to inclusive for signal procs. 
# I think we want to keep this as is (acceptance uncertainty)
#Rename specific uncertainties that are correlated between processes in the same channel where they should not have been
#cb.cp().channel(['tth_hbb']).process(['ttH_PTH_0_60_hbb','ttH_PTH_60_120_hbb','ttH_PTH_120_200_hbb','ttH_PTH_200_300_hbb','ttH_PTH_300_450_hbb','ttH_PTH_GT450_hbb']).syst_name(['CMS_ttHbb_PDF']).ForEachSyst(lambda x: x.set_name('pdf_Higgs_ttH')) ## LEGACY

# Adding inclusive theory uncertainty to tth_hbb and remove "dy" later
cb.cp().channel(['tth_hbb']).process(['ttH_PTH_0_60_hbb','ttH_PTH_60_120_hbb','ttH_PTH_120_200_hbb','ttH_PTH_200_300_hbb','ttH_PTH_300_450_hbb','ttH_PTH_GT450_hbb']).AddSyst(cb, 'THU_ttH_Yield', 'lnN', ch.SystMap()((0.908,1.058)))

cb.cp().channel(['tth_hbb_partial']).process(['tHq_hbb']).AddSyst(cb,'QCDscale_tHq', 'lnN', ch.SystMap()((0.853,1.065)))

cb.cp().channel(['vhbb']).process(['WH_lep_hbb']).AddSyst(cb,'QCDscale_WH','lnN', ch.SystMap()(1.005))
cb.cp().channel(['vhbb']).process(['ZH_lep_hbb']).AddSyst(cb,'QCDscale_ZH','lnN', ch.SystMap()(1.005))
cb.FilterSysts(lambda x: x.channel()=='vhbb' and x.name()=='QCDscale_VH')

ch.CloneSysts(cb.cp().channel(['vbfhbb']).syst_name(['QCDscale_ggH']), cb, lambda x: [utils.UpdateUncert(x,1.021), x.set_name('THU_ggH_Res')])
cb.cp().channel(['vbfhbb']).syst_name(['QCDscale_ggH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.046), x.set_name('THU_ggH_Mu')])
cb.cp().channel(['vbfhbb']).syst_name(['QCDscale_qqH']).ForEachSyst(lambda x: [utils.UpdateUncert(x,1.004), x.set_name('THU_VBF_Yield')])

#no process named WH_lep_hbb, ZH_lep_hbb in vhbb_stxs
#cb.cp().channel(['vhbb_stxs']).process(['WH_lep_hbb']).AddSyst(cb,'QCDscale_WH','lnN', ch.SystMap()(1.005))
#cb.cp().channel(['vhbb_stxs']).process(['ZH_lep_hbb']).AddSyst(cb,'QCDscale_ZH','lnN', ch.SystMap()(1.005))
#cb.FilterSysts(lambda x: x.channel()=='vhbb_stxs' and x.name()=='QCDscale_VH')

# TODO: add full sweep of STXS theory uncertainties

### rename and remove uncertainties from dictionary maps
import chtools.systs as systs
print("-> renaming")
for chn in systs.rename:
    for oldname, newname in six.iteritems(systs.rename[chn]):
        if chn=='all':
            cb.cp().syst_name([oldname]).ForEachSyst(lambda x: x.set_name(newname))
        else:
            cb.cp().syst_name([oldname]).channel([chn]).ForEachSyst(lambda x: x.set_name(newname))
            # For renaming param type nuisances: add chn to list if required
            if (chn=='hinv') | (chn=='vbfhbb'):
                if cb.GetParameter(oldname): # warning global renaming
                    print((">>>>DEBUG","WARNING","GLOBAL RENAME from",chn,"of Par",oldname,"->",newname))
                    cb.GetParameter(oldname).set_name(newname) ## does this rename also the parameters in the workspace? w.var().SetName()?
                    cb.cp().channel([chn]).renameParInWs(oldname,newname,'') ##

print("-> removing")
for chn in systs.remove:
    if chn=='all':
        cb.syst_name(systs.remove['all'], False)
    else:
        for name in systs.remove[chn]:
            cb.FilterSysts(lambda x: x.channel()==chn and x.name()==name)

print("-> flipping")
for chn in systs.flip:
    if chn=='all':
        cb.cp().syst_name(systs.flip[chn]).ForEachSyst(utils.DoSwap)
    else:
        cb.cp().channel([chn]).syst_name(systs.flip[chn]).ForEachSyst(utils.DoSwap)

if args.prune_asymm_lnN:
    print("-> pruning asymm logN, thr=",0.005)
    cb.cp().ForEachSyst(lambda x: utils.PruneAsymm(x,0.005,False) )##thr, verbose

# Drop nuisances for case when all relevant procs have been pruned
print("-> removing empties")
procs = []
cb.cp().ForEachProc(lambda x: procs.append( x.process()))
cb.FilterSysts(lambda x: x.process() not in procs if x.process() else False) # Require x.process() != None to avoid filtering params

start=Timing("Systematics handling",start)

if args.diagnostics:
    sig_procs_in_bins = defaultdict(set)
    bkg_procs_in_bins = defaultdict(set)

    print('>> Bins in channels: ')
    bins_in_channels = defaultdict(set)
    for chn in cb.cp().channel_set():
        bins_in_channels[chn] = set(cb.cp().channel([chn]).bin_set())
    pprint.pprint(dict(bins_in_channels), indent=4)

    print('>> Signal processes: ')
    pprint.pprint(cb.cp().signals().process_set(), indent=4)
    print('<< ')

    print('>> Background processes: ')
    pprint.pprint(cb.cp().backgrounds().process_set(), indent=4)
    print('<< ')


    for p in cb.cp().signals().process_set():
        for b in cb.cp().process([p]).SetFromProcs(lambda x: (x.channel(), x.bin())):
            sig_procs_in_bins[p].add(b)

    for p in cb.cp().backgrounds().process_set():
        for b in cb.cp().process([p]).SetFromProcs(lambda x: (x.channel(), x.bin())):
            bkg_procs_in_bins[p].add(b)


    print('>> Signal processes in bins: ')
    pprint.pprint(dict(sig_procs_in_bins), indent=4)
    print('<< ')

    print('>> Bkg processes in bins: ')
    pprint.pprint(dict(bkg_procs_in_bins), indent=4)
    print('<< ')


    sig_systs_in_chns = defaultdict(set)
    all_systs_in_chns = defaultdict(set)

    #for syst in cb.cp().signals().syst_name_set():
    #    sig_systs_in_chns[syst] = cb.cp().syst_name(
    #        [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

    #print '>> Signal systematics in channels: '
    #pprint.pprint(dict(sig_systs_in_chns), indent=4)
    #print '<< '

    for syst in cb.cp().syst_name_set():
        all_systs_in_chns[syst] = cb.cp().syst_name([syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

    print('>> All systematics in channels: ')
    pprint.pprint(dict(all_systs_in_chns), indent=4)
    print('<<')

    correlated_systs = defaultdict(set)
    for syst in cb.cp().syst_name_set():
        if len(cb.cp().syst_name([syst]).SetFromSysts(lambda x: x.channel())) > 1:
            correlated_systs[syst] = cb.cp().syst_name(
                [syst]).SetFromSysts(lambda x: (x.channel(), x.process()))

    print('>> Correlated systematics in channels: ')
    pprint.pprint(dict(correlated_systs), indent=4)
    print('<< ')

    start=Timing("Print summary",start)

#utils.ForEachProcAndSyst(cb.cp().channel(['tth_hbb_partial', 'tth_hbb', 'tth_multilepton', 'vhbb', 'hww_stxs','hww_incl','htt_stxs']), lambda x: x.set_mass('*'))
utils.ForEachProcAndSyst(cb.cp().channel(['tth_hbb_partial', 'tth_hbb', 'tth_multilepton', 'vhbb', 'vhbb_stxs', 'hww_stxs','hww_incl','htt_stxs']), lambda x: x.set_mass('*'))
#print "MASS SET=",cb.cp().mass_set()

start=Timing("Setting mass",start)

### Hack for tests replacing tth_hmm in multilepton analysis with tth_hww
#cb.cp().channel(['tth_multilepton']).process(['ttH_hmm']).bin(["ttH_3l_bl_neg","ttH_3l_bl_pos","ttH_3l_bt_neg","ttH_3l_bt_pos"]).ForEachProc(lambda x: utils.ReplaceProcShape(cb.cp(),x,'ttH_hww'))
#cb.cp().channel(['tth_multilepton']).process(['ttH_hmm']).bin(["ttH_3l_bl_neg","ttH_3l_bl_pos","ttH_3l_bt_neg","ttH_3l_bt_pos"]).syst_type(["shape"]).ForEachSyst(lambda x: utils.ReplaceSystShape(cb.cp(),x,'ttH_hww'))


## Sanity checks
#if not utils.CheckDoubleCounting(cb.cp()): raise ValueError('Neglecting some syst in dumping')

# Also write per-analysis cards for cross-checking
for chn in cb.channel_set():
    print('>> Writing %s card' % chn)
    cb.cp().channel([chn]).WriteDatacard(
        'comb_2021_%s%s.txt.gz' % (chn, postfix), 'comb_2021_%s%s.inputs.root' % (chn, postfix))

#fix mass for htt and hinv. if we are going to run 125.38, we need to load 125, in any case
# I didn't find the option to hard set it in ch
for chn in ['htt_incl','hinv']:
    if chn not in cb.channel_set(): continue
    cmd="zcat comb_2021_%(chn)s%(postfix)s.txt.gz | sed 's/\\$MASS/125/g' > comb_2021_%(chn)s%(postfix)s.txt && rm comb_2021_%(chn)s%(postfix)s.txt.gz && gzip comb_2021_%(chn)s%(postfix)s.txt"%{'chn':chn,'postfix':postfix}
    call(cmd,shell=True)

start=Timing("Writing datacards",start)

Timing("PrepareComb took",start_)
# print '>> Writing combined card'
#cb.WriteDatacard('comb_2021%s.txt.gz' % postfix, 'comb_2021%s.inputs.root' % postfix)
