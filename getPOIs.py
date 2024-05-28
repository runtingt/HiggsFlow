#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import print_function
import six
getPOIs = {
    # STXS to SMEFT model
    "STXStoSMEFTExpanded": {
     "POIs" : {
          "chbox" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chdd" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chgXE3" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "chwXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "chbXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "chwbXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "cbhreXE2" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cbgre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chj1XE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chq1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chj3XE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chq3" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chuXE1" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "chdXE1" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "chl3" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cll1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cg" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctgreXE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cthre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chtXEm2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "chl1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "che" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chbq" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctwreXE1" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "cqj31" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqj38" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cbwre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "chtbreXEm1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqj18" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctu8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctd8" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "cqu8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctj8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqd8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqj11" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctu1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctd1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqu1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctj1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cqd1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "ctbreXE2" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "cwXE1" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "cehre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "cuhreXEm2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.}
     },
     "POIsFix" : {},
     "cards":["hgg","hzz","hww_stxs","htt_stxs","vhbb_stxs","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg"],
     #"cards":["hgg","hzz","hww_stxs","htt_stxs","tth_hbb","vhbb_stxs"],
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },

    "STXStoSMEFTExpandedStatOnly": {
     "POIs" : {
          "chgXE3" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "chwXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
     },
     "POIsFix" : {},
     "cards":["hgg","hzz","hww_stxs","htt_stxs","vhbb_stxs","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg"],
     #"cards":["hgg","hzz","hww_stxs","htt_stxs","tth_hbb","vhbb_stxs"],
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },
    
    "STXStoSMEFTExpandedLinear": {
     "POIs" : {
          "lchbox" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchdd" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchgXE3" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "lchwXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lchbXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lchwbXE2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lcbhreXE2" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcbgre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchj1XE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchq1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchj3XE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchq3" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchuXE1" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "lchdXE1" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "lchl3" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcll1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcg" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctgreXE1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcthre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchtXEm2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lchl1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lche" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchbq" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctwreXE1" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lcqj31" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqj38" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcbwre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lchtbreXEm1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqj18" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctu8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctd8" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "lcqu8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctj8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqd8" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqj11" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctu1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctd1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqu1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctj1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcqd1" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lctbreXE2" : {"range": [-10.,10.]  , "points":20, "SMVal": 0.},
          "lcwXE1" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.},
          "lcehre" : {"range": [-5.,5.]  , "points":20, "SMVal": 0.},
          "lcuhreXEm2" : {"range": [-2.,2.]  , "points":20, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },

    "STXStoSMEFTExpandedLinearStatOnly": {
     "POIs" : {
          "lchgXE3" : {"range": [-35.,30.]  , "points":20, "SMVal": 0.},
          "lchwXE2" : {"range": [-5.,7.]  , "points":20, "SMVal": 0.},
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },
    
    "STXStoSMEFTExpandedLinearStatOnly3D": {
     "POIs" : {
          "lchgXE3" : {"range": [-35.,30.]  , "points":30, "SMVal": 0.},
          "lchwXE2" : {"range": [-6.,7.]  , "points":30, "SMVal": 0.},
          "lctgreXE1" : {"range": [-17.,10.]  , "points":30, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },

    "STXStoSMEFTExpandedLinearStatOnly4D": {
     "POIs" : {
          "lchgXE3" : {"range": [-33.,20.]  , "points":30, "SMVal": 0.},
          "lchwXE2" : {"range": [-5.,7.]  , "points":30, "SMVal": 0.},
          "lctgreXE1" : {"range": [-17.,10.]  , "points":30, "SMVal": 0.},
	      "lchj3XE1" : {"range": [-5.,5.]  , "points":30, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },
    
    "STXStoSMEFTExpandedLinearStatOnly5D": {
     "POIs" : {
          "lchgXE3" :  {"range": [-40., 20.]  , "points":30, "SMVal": 0.},
          "lchwXE2" :  {"range": [-60., 40.]  , "points":30, "SMVal": 0.},
          "lctgreXE1" :{"range": [-20., 40.]  , "points":30, "SMVal": 0.},
	      "lchj3XE1" : {"range": [-10.,  5.]  , "points":30, "SMVal": 0.},
	      "lchl3" :    {"range": [ -7., 20.]  , "points":30, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },
    
    "STXStoSMEFTExpandedLinear4D": {
     "POIs" : {
          "lchgXE3" : {"range": [-40.,20.]  , "points":30, "SMVal": 0.},
          "lchwXE2" : {"range": [-9.,5.]  , "points":30, "SMVal": 0.},
          "lctgreXE1" : {"range": [-17.,12.]  , "points":30, "SMVal": 0.},
          "lchj3XE1" : {"range": [-6.,5.]  , "points":30, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },
    
    "STXStoSMEFTExpandedStatOnly4D": {
     "POIs" : {
          "chgXE3" : {"range": [-25.,30.]  , "points":30, "SMVal": 0.},
          "chwXE2" : {"range": [-5.,7.]  , "points":30, "SMVal": 0.},
          "ctgreXE1" : {"range": [-17.,11.]  , "points":30, "SMVal": 0.},
          "chj3XE1" : {"range": [-5.,5.]  , "points":30, "SMVal": 0.}
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO expand_equations=1"
    },

    "STXStoSMEFTRotatedExpanded": {
     "POIs" : {
          "EV0XE3" : {"range":[-5.710,5.710] , "points":20, "SMVal": 0.},
          "EV1XE2" : {"range":[-1.034,1.034] , "points":20, "SMVal": 0.},
          "EV2XE1" : {"range":[-1.293,1.293] , "points":20, "SMVal": 0.},
          "EV3XE1" : {"range":[-3.576,3.576] , "points":20, "SMVal": 0.},
          "EV4XE1" : {"range":[-9.768,9.768] , "points":20, "SMVal": 0.},
          "EV5" : {"range":[-2.130,2.130] , "points":20, "SMVal": 0.},
          "EV6" : {"range":[-2.944,2.944] , "points":20, "SMVal": 0.},
          "EV7" : {"range":[-3.351,3.351] , "points":20, "SMVal": 0.},
          "EV8" : {"range":[-3.740,3.740] , "points":20, "SMVal": 0.},
          "EV9" : {"range":[-6.036,6.036] , "points":20, "SMVal": 0.},
          "EV10" : {"range":[-6.933,6.933] , "points":20, "SMVal": 0.},
          "EV11XEm1" : {"range":[-1.567,1.567] , "points":20, "SMVal": 0.},
          "EV12XEm1" : {"range":[-2.599,2.599] , "points":20, "SMVal": 0.},
          "EV13XEm1" : {"range":[-2.730,2.730] , "points":20, "SMVal": 0.},
          "EV14XEm1" : {"range":[-3.478,3.478] , "points":20, "SMVal": 0.},
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTRotatedExpanded",
     "cards":["hgg","hzz","hww_stxs","htt_stxs","vhbb_stxs","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg"],
     #"cards":["hgg","hzz","hww_stxs","htt_stxs","tth_hbb","vhbb_stxs"],
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO parametrisation=CMS-prelim-SMEFT-topU3l_22_05_05_AccCorr_rotated_231008_0p01 --PO eigenvalueThreshold=0.01 --PO expand_equations=1"
    },

    "STXStoSMEFTRotatedExpandedLinear": {
     "POIs" : {
          "lEV0XE3" : {"range":[-5.710,5.710] , "points":20, "SMVal": 0.},
          "lEV1XE2" : {"range":[-1.034,1.034] , "points":20, "SMVal": 0.},
          "lEV2XE1" : {"range":[-1.293,1.293] , "points":20, "SMVal": 0.},
          "lEV3XE1" : {"range":[-3.576,3.576] , "points":20, "SMVal": 0.},
          "lEV4XE1" : {"range":[-9.768,9.768] , "points":20, "SMVal": 0.},
          "lEV5" : {"range":[-2.130,2.130] , "points":20, "SMVal": 0.},
          "lEV6" : {"range":[-2.944,2.944] , "points":20, "SMVal": 0.},
          "lEV7" : {"range":[-3.351,3.351] , "points":20, "SMVal": 0.},
          "lEV8" : {"range":[-3.740,3.740] , "points":20, "SMVal": 0.},
          "lEV9" : {"range":[-6.036,6.036] , "points":20, "SMVal": 0.},
          "lEV10" : {"range":[-6.933,6.933] , "points":20, "SMVal": 0.},
          "lEV11XEm1" : {"range":[-1.567,1.567] , "points":20, "SMVal": 0.},
          "lEV12XEm1" : {"range":[-2.599,2.599] , "points":20, "SMVal": 0.},
          "lEV13XEm1" : {"range":[-2.730,2.730] , "points":20, "SMVal": 0.},
          "lEV14XEm1" : {"range":[-3.478,3.478] , "points":20, "SMVal": 0.},
     },
     "POIsFix" : {},
     "UseWsp": "STXStoSMEFTRotatedExpanded",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO parametrisation=CMS-prelim-SMEFT-topU3l_22_05_05_AccCorr_rotated_231008_0p01 --PO eigenvalueThreshold=0.01 --PO expand_equations=1"
    },
    
    "STXStoSMEFTRotatedExpandedLinearStatOnly5D": {
        "POIs": {
            "lEV0XE3": {"range": [-5., 5.], "points": 20, "SMVal": 0.0},
            "lEV1XE2": {"range": [-3., 2.], "points": 20, "SMVal": 0.0},
            "lEV2XE1": {"range": [-4, 5.], "points": 20, "SMVal": 0.0},
            "lEV3": {"range": [-1., 1.5], "points": 20, "SMVal": 0.0},
            "lEV4": {"range": [-6, 1], "points": 20, "SMVal": 0.0},
        },
        "POIsFix": {},
        "UseWsp": "STXStoSMEFTRotatedExpanded",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXStoSMEFTModel:STXStoSMEFT --PO parametrisation=CMS-prelim-SMEFT-topU3l_22_05_05_AccCorr_rot_hgg_statonly_STXSStage1p2XSBRRefHggStatOnly --PO eigenvalueThreshold=0.01 --PO expand_equations=1"
    },

    "TrilinearHiggsKappaVKappaFSTXS12": {
        "POIs":{
                "kappa_V":{"range":[0.,2.],"points":50},
                "kappa_F":{"range":[-2.,2.],"points":50},
                "kappa_lambda":{"range":[-20,20.],"points":50},
                },
        #"UseWsp":"",
        "POIsFix": {},
        "uncertainties":"uncertainties/brunc_kappa.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.TrilinearCouplingModels:TrilinearHiggsKappaVKappaFSTXS12 --PO BRU=true "
    },
    "TrilinearHiggsKappaVKappaF": {
        "POIs": {
           "kappa_V"          :{"range":[0. ,2.     ]   ,"points":50},
           "kappa_F"          :{"range":[-2 ,2.     ]   ,"points":50},
           "kappa_lambda"     :{"range":[-20 , 20   ]   ,"points":50}
        },
        "POIsFix": {},
        "UseWsp": "trilinearHiggskVkF"
    },
    "TrilinearHiggsKL": {
        "POIs": {
           "kappa_lambda"     :{"range":[-20 , 20   ]   ,"points":50}
        },
        "POIsFix": {"kappa_V", "kappa_F"},
        "UseWsp": "TrilinearHiggsKappaVKappaFSTXS12"
    },
    "TrilinearHiggsKLKV_2D": {
        "POIs": {
           "kappa_lambda"     :{"range":[-20 , 25   ]   ,"points":50},
           "kappa_V"          :{"range":[0. ,2.     ]   ,"points":50},
        },
        "POIsFix": {"kappa_F"},
        "UseWsp": "TrilinearHiggsKappaVKappaFSTXS12"
    },
    "TrilinearHiggsKLKF_2D": {
        "POIs": {
           "kappa_lambda"     :{"range":[-20 , 20   ]   ,"points":50},
           "kappa_F"          :{"range":[-2 ,2.     ]   ,"points":50},
        },
        "POIsFix": {"kappa_V"},
        "UseWsp": "TrilinearHiggsKappaVKappaFSTXS12"
    },
    "STXSStage1p2XSBRRefttHbb": {
      "POIs":{
          "mu_XS_ttH_PTH_0_60_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_60_120_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_120_200_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_200_300_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_GT300_BR_bb" : {"range": [-10.,10.]  , "points":30},
      },
        "POIsFix": {"THU_ttH_Yield","THU_ttH_mig60","THU_ttH_mig120","THU_ttH_mig200","THU_ttH_mig300"},
        "UseWsp": "STXS",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2XSBRRefHtt": {
      "POIs":{
          "mu_XS_ggH_0J_PTH_0_10_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_2J_PTH_LT200_BR_tautau" : {"range" : [-10.,10.], "points":30},
          "mu_XS_ggH_PTH_200_300_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT300_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_notvbftopo_BR_tautau" : {"range" : [-10.,10.], "points":30},
          "mu_XS_VBF_lowmjj_BR_tautau" : {"range" : [-10.,10.], "points":30},
          "mu_XS_VBF_highmjj_BR_tautau" : {"range" : [-10.,10.], "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_LT150_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT150_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_LT150_BR_tautau" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_tautau" : {"range": [-10.,10.]  , "points":30},
      },
        "POIsFix": {},
        "UseWsp": "STXS",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2XSBRRefHzz": {
      "POIs":{
          "mu_XS_ggH_0J_PTH_0_10_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_vbftopo_BR_ZZ" : {"range": [0.,10.] ,"points":30},
          "mu_XS_ggH_PTH_GT200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_rest_hzzdef_BR_ZZ" : {"range": [0.,10.], "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_ZZ" : {"range" : [0.,10.], "points":30},
          "mu_XS_VBF_lowmjj_lowpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highmjj_lowpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VH_lep_PTV_LT150_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VH_lep_PTV_GT150_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttHtH_BR_ZZ" : {"range": [0.,10.] ,"points":30},
          },
      "POIsFix" : {"pdf_Higgs_qqbar","pdf_As_Higgs_qqbar","pdf_Higgs_gg","pdf_As_Higgs_gg","pdf_Higgs_ttH","pdf_As_Higgs_ttH","THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j","THU_ggH_VBF3j","THU_ggH_PT10","THU_ggH_PT60","THU_ggH_PT120","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Mjj1000","THU_VBF_Mjj1500","THU_VBF_Pt25","THU_VBF_Jet01"},
      "UseWsp": "STXS",
      "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2XSBRRefHww":{
     "POIs":{
          "mu_XS_ggH_0J_BR_WW" : {"range": [-1.,3.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_GT60_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_2J_PTH_LT200_BR_WW": {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_200_300_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT300_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_lowmjj_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highmjj_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_WW"  : {"range": [-10.,10.] , "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_LT150_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT150_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_LT150_BR_WW" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_WW" : {"range": [-10.,10.]  , "points":30},
      },
     "POIsFix" : {},
     "UseWsp" : "STXS",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2XSBRRefVHbb":{
      "POIs" : {
          "mu_XS_totZH_lep_PTV_75_150_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_BR_bb" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250_BR_bb" : {"range": [-10.,10.]  , "points":30},
      },
      "POIsFix" : {},
      "UseWsp" : "STXS",
      "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
	
    "STXSStage1p2XSBRRefHggStatOnly": {
     "POIs" : {
          "mu_XS_ggH_0J_PTH_0_10_BR_gamgam" : {"range":[0,2.808] , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_BR_gamgam" : {"range":[0,2.162] , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_gamgam" : {"range":[0,2.221] , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_gamgam" : {"range":[0,2.407] , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_gamgam" : {"range":[0,3.359] , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_gamgam" : {"range":[0,5.979] , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_gamgam" : {"range":[0,3.381] , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_gamgam" : {"range":[0,3.003] , "points":30},
          "mu_XS_ggH_PTH_200_300_BR_gamgam" : {"range":[0,2.709] , "points":30},
          "mu_XS_ggH_PTH_300_450_BR_gamgam" : {"range":[0,3.458] , "points":30},
          "mu_XS_ggH_PTH_GT450_BR_gamgam" : {"range":[0,15.551] , "points":30},
          "mu_XS_simVBF_lowmjj_lowpthjj_BR_gamgam" : {"range":[0,4.546] , "points":30},
          "mu_XS_simVBF_lowmjj_highpthjj_BR_gamgam" : {"range":[0,8.227] , "points":30},
          "mu_XS_simVBF_highmjj_lowpthjj_BR_gamgam" : {"range":[0,3.510] , "points":30},
          "mu_XS_simVBF_highmjj_highpthjj_BR_gamgam" : {"range":[0,4.781] , "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_gamgam" : {"range":[0,4.564] , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_gamgam" : {"range":[0,3.622] , "points":30},
          "mu_XS_WH_lep_PTV_0_75_BR_gamgam" : {"range":[0,6.071] , "points":30},
          "mu_XS_WH_lep_PTV_75_150_BR_gamgam" : {"range":[0,5.252] , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_gamgam" : {"range":[0,4.066] , "points":30},
          "mu_XS_totZH_lep_BR_gamgam" : {"range":[0,4.188] , "points":30},
          "mu_XS_ttH_PTH_0_60_BR_gamgam" : {"range":[0,3.844] , "points":30},
          "mu_XS_ttH_PTH_60_120_BR_gamgam" : {"range":[0,3.424] , "points":30},
          "mu_XS_ttH_PTH_120_200_BR_gamgam" : {"range":[0,2.892] , "points":30},
          "mu_XS_ttH_PTH_200_300_BR_gamgam" : {"range":[0,4.057] , "points":30},
          "mu_XS_ttH_PTH_GT300_BR_gamgam" : {"range":[0,4.421] , "points":30},
          "mu_XS_tH_BR_gamgam" : {"range":[0,19.492] , "points":30},
     },
     "POIsFix" : {},
     "UseWsp": "STXS",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
 
    "STXSStage1p2XSBRRefHgg": {
     "POIs" : {
          "mu_XS_ggH_0J_PTH_0_10_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_BR_gamgam" : {"range": [-2.,4.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_PTH_200_300_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_300_450_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT450_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_lowpthjj_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_highpthjj_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_lowpthjj_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_highpthjj_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_0_60_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_60_120_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_120_200_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_200_300_BR_gamgam" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_GT300_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_tH_BR_gamgam" : {"range": [0.,20.]  , "points":30},
     },
     "POIsFix" : {"CMS_hgg_nuisance_HighR9EBPhi_13TeVsmear","CMS_hgg_nuisance_HighR9EEPhi_13TeVsmear","BR_hgg","THU_ggH_stxs_Yield","THU_ggH_stxs_Res","THU_ggH_stxs_Boosted","THU_ggH_stxs_Mig01","THU_ggH_stxs_Mig12","THU_ggH_stxs_0J_PTH10","THU_ggH_stxs_1J_PTH60","THU_ggH_stxs_1J_PTH120","THU_ggH_stxs_GE2J_PTH60","THU_ggH_stxs_GE2J_PTH120","THU_ggH_stxs_GE2J_MJJ350","THU_ggH_stxs_GE2J_MJJ700","THU_ggH_stxs_GE2J_LOWMJJ_PTHJJ25","THU_ggH_stxs_GE2J_HIGHMJJ_PTHJJ25","THU_ggH_stxs_PTH200","THU_ggH_stxs_PTH300","THU_ggH_stxs_PTH450","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_Mu","THU_ggH_PT120","THU_ggH_PT60","THU_ggH_Res","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Pt25","THU_VBF_Jet01","THU_WH_inc","THU_WH_mig75","THU_WH_mig150","THU_ZH_inc","THU_ggZH_inc","THU_ttH_Yield","THU_ttH_mig60","THU_ttH_mig120","THU_ttH_mig200","THU_ttH_mig300","rgx{QCDscale_.*}","rgx{pdf_Higgs_.*}","rgx{alphaS_.*}","CMS_hgg_tth_parton_shower","CMS_hgg_tth_gluon_splitting","CMS_hgg_tth_mc_low_stat","UnderlyingEvent_norm","PartonShower_norm"},
     "UseWsp": "STXS",
     "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2XSBRAllChannelsMu": {
        "POIs":{
          "mu_XS_ggH_0J_PTH_0_10_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_PTH_200_300_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_PTH_300_450_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT450_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_lowpthjj_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_highpthjj_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_lowpthjj_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_highpthjj_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_totZH_lep_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttH_PTH_0_60_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttH_PTH_60_120_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttH_PTH_120_200_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttH_PTH_200_300_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttH_PTH_GT300_BR_gamgam" : {"range": [0.,10.]  , "points":30},
          "mu_XS_tH_BR_gamgam" : {"range": [0.,20.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ggH_vbftopo_BR_ZZ" : {"range": [0.,10.] ,"points":30},
          "mu_XS_ggH_PTH_GT200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_other_BR_ZZ" : {"range": [0.,10.], "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_ZZ" : {"range" : [0.,10.], "points":30},
          "mu_XS_VBF_lowmjj_lowpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highmjj_lowpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highpthjj_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VH_lep_PTV_LT150_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_VH_lep_PTV_GT150_BR_ZZ" : {"range": [0.,10.]  , "points":30},
          "mu_XS_ttHtH_BR_ZZ" : {"range": [0.,10.] ,"points":30},
          "mu_XS_ggH_0J_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_GT60_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_2J_PTH_LT200_BR_WW": {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_PTH_200_300_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT300_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_VBF_lowmjj_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_VBF_highmjj_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_WW"  : {"range": [-5.,10.] , "points":30},
          "mu_XS_VBF_MJJ_60_120_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_LT150_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT150_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_LT150_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_WW" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttHtH_BR_WW" : {"range": [-5.,10.] ,"points":30},
          "mu_XS_ggH_0J_PTH_0_10_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_2J_PTH_LT200_BR_tautau" : {"range" : [-5.,10.], "points":30},
          "mu_XS_ggH_PTH_200_300_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT300_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_VBF_notvbftopo_BR_tautau" : {"range" : [-5.,10.], "points":30},
          "mu_XS_VBF_lowmjj_BR_tautau" : {"range" : [-5.,10.], "points":30},
          "mu_XS_VBF_highmjj_BR_tautau" : {"range" : [-5.,10.], "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_LT150_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT150_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_LT150_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150_BR_tautau" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttHtH_BR_tautau" : {"range": [-5.,10.] ,"points":30},
          "mu_XS_ggHbbH_BR_bb": {"range": [-5.,10.]  , "points":30},
          "mu_XS_qqH_BR_bb": {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_75_150_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttH_PTH_0_60_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttH_PTH_60_120_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttH_PTH_120_200_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttH_PTH_200_300_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ttH_PTH_GT300_BR_bb" : {"range": [-5.,10.]  , "points":30},
          "mu_XS_ggHbbHttHtH_BR_mumu" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBFVH_BR_mumu" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggHbbHttHtH_BR_Zgam" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBFVH_BR_Zgam" : {"range": [-8.,8.]  , "points":30},
         },
        "POIsFix" : {},
        "cards":["hgg","hzz","hww_stxs","htt_stxs","vhbb_stxs","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg"],
        "UseWsp": "STXSAllChannels",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json --PO addStage0=1"
    },

    "STXSStage1p2Merged": {
        "POIs":{
          "mu_XS_totZH_lep_PTV_LT150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_other" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_VBF_lowmjj" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_highmjj" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ttH_PTH_0_60" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_GT300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_300_450" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_PTH_GT450" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_vbftopo" : {"range": [-5.,5.] , "points":30},
          "mu_XS_tH" : {"range": [-10.,10.] , "points":30},
         },
        "POIsFix" : {"CMS_hgg_nuisance_HighR9EBPhi_13TeVsmear","CMS_hgg_nuisance_HighR9EEPhi_13TeVsmear","BR_hgg","THU_ggH_stxs_Yield","THU_ggH_stxs_Res","THU_ggH_stxs_Boosted","THU_ggH_stxs_Mig01","THU_ggH_stxs_Mig12","THU_ggH_stxs_0J_PTH10","THU_ggH_stxs_1J_PTH60","THU_ggH_stxs_1J_PTH120","THU_ggH_stxs_GE2J_PTH60","THU_ggH_stxs_GE2J_PTH120","THU_ggH_stxs_GE2J_MJJ350","THU_ggH_stxs_GE2J_MJJ700","THU_ggH_stxs_GE2J_LOWMJJ_PTHJJ25","THU_ggH_stxs_GE2J_HIGHMJJ_PTHJJ25","THU_ggH_stxs_PTH200","THU_ggH_stxs_PTH300","THU_ggH_stxs_PTH450","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_Mu","THU_ggH_PT120","THU_ggH_PT60","THU_ggH_Res","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Pt25","THU_VBF_Jet01","THU_WH_inc","THU_WH_mig75","THU_WH_mig150","THU_ZH_inc","THU_ggZH_inc","THU_ttH_Yield","THU_ttH_mig60","THU_ttH_mig120","THU_ttH_mig200","THU_ttH_mig300","rgx{QCDscale_.*}","rgx{pdf_Higgs_.*}","rgx{alphaS_.*}","CMS_hgg_tth_parton_shower","CMS_hgg_tth_gluon_splitting","CMS_hgg_tth_mc_low_stat","UnderlyingEvent_norm","PartonShower_norm","pdf_Higgs_qqbar","pdf_As_Higgs_qqbar","pdf_Higgs_gg","pdf_As_Higgs_gg","pdf_Higgs_ttH","pdf_As_Higgs_ttH","THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j","THU_ggH_VBF3j","THU_ggH_PT10","THU_ggH_PT60","THU_ggH_PT120","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Mjj1000","THU_VBF_Mjj1500","THU_VBF_Pt25","THU_VBF_Jet01","THU_ggH_qmtop","THU_ggH_VBF3j","THU_ggH_VBF2j"},
        "UseWsp": "STXS",
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },

    "STXSStage1p2RatioZZ": {
        "POIs":{
          "mu_XS_totZH_lep_PTV_LT150_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_other_x_BR_ZZ" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_VBF_lowmjj_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_highmjj_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200_x_BR_ZZ" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ttH_PTH_0_60_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_60_120_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_120_200_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_200_300_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_GT300_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_200_300_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_300_450_x_BR_ZZ" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_PTH_GT450_x_BR_ZZ" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10_x_BR_ZZ" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10_wbbH_x_BR_ZZ" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60_x_BR_ZZ" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120_x_BR_ZZ" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_x_BR_ZZ" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_x_BR_ZZ" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_vbftopo_x_BR_ZZ" : {"range": [-5.,5.] , "points":30},
          "mu_XS_tH_x_BR_ZZ" : {"range": [-10.,10.] , "points":30},
          "mu_BR_ZZ_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
          "mu_BR_bb_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
          "mu_BR_tautau_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
          "mu_BR_gamgam_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
         },
        "POIsFix" : {"CMS_hgg_nuisance_HighR9EBPhi_13TeVsmear","CMS_hgg_nuisance_HighR9EEPhi_13TeVsmear","BR_hgg","THU_ggH_stxs_Yield","THU_ggH_stxs_Res","THU_ggH_stxs_Boosted","THU_ggH_stxs_Mig01","THU_ggH_stxs_Mig12","THU_ggH_stxs_0J_PTH10","THU_ggH_stxs_1J_PTH60","THU_ggH_stxs_1J_PTH120","THU_ggH_stxs_GE2J_PTH60","THU_ggH_stxs_GE2J_PTH120","THU_ggH_stxs_GE2J_MJJ350","THU_ggH_stxs_GE2J_MJJ700","THU_ggH_stxs_GE2J_LOWMJJ_PTHJJ25","THU_ggH_stxs_GE2J_HIGHMJJ_PTHJJ25","THU_ggH_stxs_PTH200","THU_ggH_stxs_PTH300","THU_ggH_stxs_PTH450","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_Mu","THU_ggH_PT120","THU_ggH_PT60","THU_ggH_Res","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Pt25","THU_VBF_Jet01","THU_WH_inc","THU_WH_mig75","THU_WH_mig150","THU_ZH_inc","THU_ggZH_inc","THU_ttH_Yield","THU_ttH_mig60","THU_ttH_mig120","THU_ttH_mig200","THU_ttH_mig300","rgx{QCDscale_.*}","rgx{pdf_Higgs_.*}","rgx{alphaS_.*}","CMS_hgg_tth_parton_shower","CMS_hgg_tth_gluon_splitting","CMS_hgg_tth_mc_low_stat","UnderlyingEvent_norm","PartonShower_norm","pdf_Higgs_qqbar","pdf_As_Higgs_qqbar","pdf_Higgs_gg","pdf_As_Higgs_gg","pdf_Higgs_ttH","pdf_As_Higgs_ttH","THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j","THU_ggH_VBF3j","THU_ggH_PT10","THU_ggH_PT60","THU_ggH_PT120","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Mjj1000","THU_VBF_Mjj1500","THU_VBF_Pt25","THU_VBF_Jet01","THU_ggH_qmtop","THU_ggH_VBF3j","THU_ggH_VBF2j"},
        "UseWsp": "STXSRatio",
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12RatioZZ --PO mergejson=stxs_stage12_merge.json"
    },

    "STXSStage1p2full": {
        "POIs":{
          "mu_XS_totZH_lep_PTV_0_75" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_75_150" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_0J" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_GE1J" : {"range": [-15.,15.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          #"mu_XS_VBF_0J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_1J" : {"range": [-8.,8.]  , "points":30},
          #"mu_XS_VBF_MJJ_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_MJJ_120_350" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_VBF_lowmjj_lowpthjj" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_lowmjj_highpthjj" : {"range": [-15.,15.]  , "points":30},
          "mu_XS_VBF_highmjj_lowpthjj" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_highmjj_highpthjj" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ttH_PTH_0_60" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_GT300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_300_450" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_PTH_450_650" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggH_PTH_GT650" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_simVBF_highmjj" : {"range": [-8.,8.] , "points":30},
          "mu_XS_ggH_simVBF_lowmjj" : {"range": [-8.,8.] , "points":30},
          "mu_XS_tH" : {"range": [-10.,10.] , "points":30},
         },
        "POIsFix" : {"CMS_hgg_nuisance_HighR9EBPhi_13TeVsmear","CMS_hgg_nuisance_HighR9EEPhi_13TeVsmear","BR_hgg","THU_ggH_stxs_Yield","THU_ggH_stxs_Res","THU_ggH_stxs_Boosted","THU_ggH_stxs_Mig01","THU_ggH_stxs_Mig12","THU_ggH_stxs_0J_PTH10","THU_ggH_stxs_1J_PTH60","THU_ggH_stxs_1J_PTH120","THU_ggH_stxs_GE2J_PTH60","THU_ggH_stxs_GE2J_PTH120","THU_ggH_stxs_GE2J_MJJ350","THU_ggH_stxs_GE2J_MJJ700","THU_ggH_stxs_GE2J_LOWMJJ_PTHJJ25","THU_ggH_stxs_GE2J_HIGHMJJ_PTHJJ25","THU_ggH_stxs_PTH200","THU_ggH_stxs_PTH300","THU_ggH_stxs_PTH450","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_Mu","THU_ggH_PT120","THU_ggH_PT60","THU_ggH_Res","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Pt25","THU_VBF_Jet01","THU_WH_inc","THU_WH_mig75","THU_WH_mig150","THU_ZH_inc","THU_ggZH_inc","THU_ttH_Yield","THU_ttH_mig60","THU_ttH_mig120","THU_ttH_mig200","THU_ttH_mig300","rgx{QCDscale_.*}","rgx{pdf_Higgs_.*}","rgx{alphaS_.*}","CMS_hgg_tth_parton_shower","CMS_hgg_tth_gluon_splitting","CMS_hgg_tth_mc_low_stat","UnderlyingEvent_norm","PartonShower_norm","pdf_Higgs_qqbar","pdf_As_Higgs_qqbar","pdf_Higgs_gg","pdf_As_Higgs_gg","pdf_Higgs_ttH","pdf_As_Higgs_ttH","THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j","THU_ggH_VBF3j","THU_ggH_PT10","THU_ggH_PT60","THU_ggH_PT120","THU_ggH_qmtop","THU_VBF_Yield","THU_VBF_PTH200","THU_VBF_Mjj60","THU_VBF_Mjj120","THU_VBF_Mjj350","THU_VBF_Mjj700","THU_VBF_Mjj1000","THU_VBF_Mjj1500","THU_VBF_Pt25","THU_VBF_Jet01","THU_ggH_qmtop","THU_ggH_VBF3j","THU_ggH_VBF2j"},
        "UseWsp": "STXS",
        "cards":["hgg","hzz","hww_stxs","htt_stxs","tth_hbb","tth_multilepton","vhbb_stxs"],
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2full_mu": {
        "POIs":{
          "mu_XS_totZH_lep_PTV_0_75" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_75_150" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_0J" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_GE1J" : {"range": [-15.,15.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250" : {"range": [-3.,3.]  , "points":30},
          #"mu_XS_VBF_0J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_1J" : {"range": [-8.,8.]  , "points":30},
          #"mu_XS_VBF_MJJ_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_MJJ_120_350" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_VBF_lowmjj_lowpthjj" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_lowmjj_highpthjj" : {"range": [-15.,15.]  , "points":30},
          "mu_XS_VBF_highmjj_lowpthjj" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_VBF_highmjj_highpthjj" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ttH_PTH_0_60" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_GT300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_300_450" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_PTH_450_650" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggH_PTH_GT650" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_simVBF_highmjj" : {"range": [-8.,8.] , "points":30},
          "mu_XS_ggH_simVBF_lowmjj" : {"range": [-8.,8.] , "points":30},
          "mu_XS_tH" : {"range": [-10.,10.] , "points":30},
         },
        "POIsFix" : {},
        "UseWsp": "STXS",
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },
    "STXSStage1p2Dummy": {
        "POIs":{
          "mu_XS_totZH_lep" : {"range": [-3.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_LT150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT150" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_vbftopo" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_PTH_300_450" : {"range": [-4.,4.]  , "points":30},
          "mu_XS_ggH_PTH_GT450" : {"range": [-8.,8.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120" : {"range": [-2.,2.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60" : {"range": [-5.,5.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ggH_vbftopo" : {"range": [-8.,8.] , "points":30},
          "mu_XS_ggH_simVBF_lowmjj" : {"range": [-8.,8.] , "points":30},
          "mu_XS_tH" : {"range": [-10.,10.] , "points":30},
          "mu_XS_ttH_PTH_0_60" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_60_120" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_120_200" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_200_300" : {"range": [-3.,3.]  , "points":30},
          "mu_XS_ttH_PTH_GT300" : {"range": [-3.,3.]  , "points":30},
         },
        "POIsFix" : {},
        "UseWsp": "STXS",
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },


    "STXSStage1p2vbfmerge": {
        "POIs":{
          "mu_XS_totZH_lep_PTV_0_75" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_75_150" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_0J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_150_250_GE1J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_totZH_lep_PTV_GT250" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_0_75" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_75_150" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_0J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_150_250_GE1J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_WH_lep_PTV_GT250" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_0J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_1J" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_60_120" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_MJJ_120_350" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_VBF_highMJJ_PTHGT200" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_lowpthjj" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_lowmjj_highpthjj" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_lowpthjj" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_simVBF_highmjj_highpthjj" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_60_120" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_120_200" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_200_300" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ttH_PTH_GT300" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_200_300" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_300_450" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_PTH_GT450" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_0_10" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_0J_PTH_GT10" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_60_120" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_1J_PTH_120_200" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120" : {"range": [-10.,10.]  , "points":30},
          "mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200" : {"range": [-10.,10.]  , "points":30}
         },
        "POIsFix": {},
        "UseWsp": "STXS",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.STXSModels:stage12 --PO mergejson=stxs_stage12_merge.json"
    },


    "STXSAllStagestoEFT": {
        "POIs": {
           "cG_x05"           :{"range":[-10. ,10.  ]   ,"points":50}
          ,"cA_x04"           :{"range":[-8 , 8     ]   ,"points":50}
          ,"cWWMinuscB_x02"   :{"range":[-15 , 15   ]   ,"points":50}
          ,"cu_x01"           :{"range":[-20. , 10. ]   ,"points":50}
          ,"cHW_x02"          :{"range":[-12. , 16. ]   ,"points":50}
          ,"cHB_x01"          :{"range":[-12. , 16. ]   ,"points":50}
          ,"cd_x01"           :{"range":[-20. , 5.0 ]   ,"points":90}
          ,"cl_x01"           :{"range":[-20. , 10. ]   ,"points":90}
            },
     "POIsFix": {},
     "SMVals": {
            "cG_x05": 0,
            "cA_x04": 0,
            "cu_x01": 0,
            "cHW_x02": 0,
            "cHB_x02": 0,
            "cWWMinuscB_x02": 0,
            "cd_x01": 0,
            "cl_x01": 0
            },
     "UseWsp": "AllStagestoEFT"
        },
    "L1": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,2], "points":30},
            "lambda_Zg": {"range":[0,3], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "UseWsp": "L1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:L1"
    },
    "L1_N1": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": +1.0,
            "lambda_tg": +1.0
        },
        "UseWsp": "L1"
    },
    "L1_N2": {
        "POIs": {
            "lambda_WZ": {"range":[-2,0], "points":40},
            "lambda_tg": {"range":[0,2], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": -1.0,
            "lambda_tg": +1.0
        },
        "UseWsp": "L1"
    },
    "L1_N3": {
        "POIs": {
            "lambda_WZ": {"range":[0,2], "points":40},
            "lambda_tg": {"range":[-2,0], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": +1.0,
            "lambda_tg": -1.0
        },
        "UseWsp": "L1"
    },
    "L1_N4": {
        "POIs": {
            "lambda_WZ": {"range":[-2,0], "points":40},
            "lambda_tg": {"range":[-2,0], "points":40},
            "lambda_bZ": {"range":[0,2], "points":30},
            "lambda_tauZ": {"range":[0,2], "points":30},
            "lambda_muZ": {"range":[0,3], "points":30},
            "lambda_Zg": {"range":[0,2], "points":30},
            "lambda_gamZ": {"range":[0,2], "points":30},
            "kappa_gZ": {"range":[0.4,1.8], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "lambda_WZ": -1.0,
            "lambda_tg": -1.0
        },
        "UseWsp": "L1"
    },
    "K1": {
        "POIs": {
            "kappa_W": {"range":[0.2,2.0], "points":30},
            "kappa_Z": {"range":[0.5,1.7], "points":30},
            "kappa_tau": {"range":[0.5,1.8], "points":30},
            "kappa_t": {"range":[0.3,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30},
            "BRinv": {"range":[0,0.000000], "points":30},
            },
        "ScanPOIs": ["kappa_W","kappa_Z","kappa_tau","kappa_t","kappa_b","kappa_mu"],
        "POIsFix": {"BRinv"},
        "SMVals": { "BRinv": 0.0 },
        "cards":["hgg","hzz","hww_stxs","htt_incl","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg","vhbb_stxs"],
        "uncertainties":"uncertainties/brunc_kappa.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K1"
        },

    "K1_no_hmm": {
        "POIs": {
            "kappa_W": {"range":[0.4,1.7], "points":30},
            "kappa_Z": {"range":[0.4,1.7], "points":30},
            "kappa_tau": {"range":[0.3,1.8], "points":30},
            "kappa_t": {"range":[0.3,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,5.0], "points":30}
            },
        "POIsFix": {"BRinv","kappa_mu"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 }
    },
    "K1_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_b": +1.0
        }
    },
    "K1_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_b": +1.0
        }
    },
    "K1_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_b": +1.0
        }
    },
    "K1_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_b": +1.0
        }
    },
    "K1_N5": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_b": -1.0
        }
    },
    "K1_N6": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_b": -1.0
        }
    },
    "K1_N7": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.8], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-2.0,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_b": -1.0
        }
    },
    "K1_N8": {
        "POIs": {
            "kappa_W": {"range":[-1.8,0.0], "points":30},
            "kappa_Z": {"range":[-1.8,0.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[-1.8,0.0], "points":30},
            "kappa_mu": {"range":[0,3.0], "points":30}
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K1",
        "SMVals": { "BRinv": 0.0 },
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_b": -1.0
        }
    },
    "K2": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2 --PO dohzg=1"
        },
    "K2_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2 --PO dohzg=1"
    },
    "K2_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2 --PO dohzg=1"
    },
    "K2_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2 --PO dohzg=1"
    },
    "K2_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2 --PO dohzg=1"
    },
    "K2Width": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "UseWsp": "K2Width",
        "SMVals": {"BRinv": 0.0},
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.7], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.7], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Width_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.7,0.0], "points":30},
            "kappa_Z": {"range":[-1.7,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
        },
        "POIsFix": {"BRinv"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2Width",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },

    "K2_2D": {
        "POIs": {
            "kappa_g": {"range":[0.4,1.7], "points":30},
            "kappa_gam": {"range":[0.4,1.7], "points":30},
            },
        "POIsFix": {"kappa_W", "kappa_Z","kappa_tau","kappa_t","kappa_b","kappa_mu","BRinv"},
        "UseWsp": "K2",
        "SMVals": { "BRinv": 0.0 }
        },

    "K2Inv": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
            },
        "cards":["hgg","hzz","hww_stxs","htt_stxs","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg","vhbb_stxs","hinv"],
        "POIsFix":{},
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 },
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2Inv --PO dohzg=1",
    },
    "K2Inv_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2Inv_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Inv",
        "SMVals": { "BRinv": 0.0 }
    },
    "K2InvWidth": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0,1.8], "points":30},
            "kappa_tau": {"range":[0,1.8], "points":30},
            "kappa_g": {"range":[0,1.8], "points":30},
            "kappa_gam": {"range":[0,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2InvWidth_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2InvWidth",
        "SMVals": { "BRinv": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Inv_2D": {
        "POIs": {
            "kappa_g": {"range":[0.5,1.6], "points":30},
            "kappa_gam": {"range":[0.6,1.5], "points":30},
            "BRinv": {"range":[0,0.9], "points":30}
            },
        "POIsFix":{"kappa_W","kappa_Z","kappa_mu","kappa_tau","kappa_t","kappa_b"}
    },
    "K2Undet": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "cards":["hgg","hzz","hww_stxs","htt_incl","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg","vhbb_stxs","hinv"],
        "UseWsp": "K2Undet",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K2Undet --PO dohzg=1",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },

    "K2Undet_BRInv_BRUndet_2D": {
        "POIs": {
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },
    "K2Undet_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "kappa_Zgam": {"range":[0.,3.], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },

    "K2InvP": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },
    "K2InvP_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{"BRundet"},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0,
            "kappa_t": +1.0
        },
        "UseWsp": "K2InvP",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["BRinv"]
    },

    "K2UndetWidth": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix":{},
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N1": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N2": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": +1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N3": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": +1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2UndetWidth_N4": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "c7_Gscal_tot": {"range":[0.5,3.0], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
        },
        "POIsFix": {},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
        "UseWsp": "K2UndetWidth",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 },
        "ScanPOIs": ["c7_Gscal_tot"]
    },
    "K2Undet_N4_2D": {
        "POIs": {
            "kappa_W": {"range":[-1.0,0.0], "points":30},
            "kappa_Z": {"range":[-1.0,0.0], "points":30},
            "kappa_mu": {"range":[0.0,2.0], "points":30},
            "kappa_tau": {"range":[0.5,1.8], "points":30},
            "kappa_t": {"range":[0,2.0], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_g": {"range":[0.4,1.7], "points":30},
            "kappa_gam": {"range":[0.5,1.7], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
            },
        "POIsFix":{},
        "POIsNominal": {
            "kappa_W": -1.0,
            "kappa_Z": -1.0
        },
    },
    "K2Undet_2D": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,2.0], "points":30},
            "kappa_tau": {"range":[0.5,1.8], "points":30},
            "kappa_t": {"range":[0,2.0], "points":30},
            "kappa_b": {"range":[0.0,2.0], "points":30},
            "kappa_g": {"range":[0.4,1.7], "points":30},
            "kappa_gam": {"range":[0.5,1.7], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[0,0.6], "points":30}
            },
        "POIsFix":{}
        },
    "K2Undet_Width": {
        "POIs": {
            "kappa_W": {"range":[0.0,1.0], "points":30},
            "kappa_Z": {"range":[0.0,1.0], "points":30},
            "kappa_mu": {"range":[0.0,3.0], "points":30},
            "kappa_tau": {"range":[0.2,1.8], "points":30},
            "kappa_t": {"range":[0.2,1.8], "points":30},
            "kappa_b": {"range":[0.2,1.8], "points":30},
            "kappa_g": {"range":[0.2,1.8], "points":30},
            "kappa_gam": {"range":[0.2,1.8], "points":30},
            "BRinv": {"range":[0,0.6], "points":30},
            "BRundet": {"range":[-0.6,0.6], "points":60}
        },
        "POIsFix":{},
        "UseWsp": "K2Undet",
        "SMVals": { "BRinv": 0.0, "BRundet": 0.0 }
    },

    "K2Undet_2Dkgkgam": {
        "POIs": {
            "kappa_g": {"range":[0.5,1.6], "points":30},
            "kappa_gam": {"range":[0.6,1.5], "points":30},
            "BRinv": {"range":[0,0.9], "points":30},
            "BRundet": {"range":[0,0.9], "points":30}
            },
        "POIsFix":{"kappa_W","kappa_Z","kappa_tau","kappa_t","kappa_b","kappa_mu"}
        },

    "K3": {
        "POIs": {
            "kappa_V": {"range":[0,2], "points":30},
            "kappa_F": {"range":[0,2], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "K3",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:K3",
        },

    "K3_2D": {
        "POIs": {
            "kappa_V": {"range":[0.6,1.4], "points":30},
            "kappa_F": {"range":[0.6,1.4], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "K3"
        },

    "K3_5D": {
        "POIs": {
            "kappa_V_gamgam": {"range":[0.4,2.5], "points":30},
            "kappa_V_WW": {"range":[0.4,1.8], "points":30},
            "kappa_V_ZZ": {"range":[0.4,1.8], "points":30},
            "kappa_V_mumu": {"range":[0.0,5.0], "points":30},
            "kappa_V_tautau": {"range":[0.4,1.8], "points":30},
            "kappa_V_bb": {"range":[0.4,1.8], "points":30},
            "kappa_F_gamgam": {"range":[0,4.0], "points":30},
            "kappa_F_WW": {"range":[0,4.0], "points":30},
            "kappa_F_ZZ": {"range":[0,2.5], "points":30},
            "kappa_F_mumu": {"range":[0.0,5.0], "points":30},
            "kappa_F_tautau": {"range":[0,2.5], "points":30},
            "kappa_F_bb": {"range":[0,2.5], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"},
        "UseWsp": "K3"
        },

    "K3_5D_2D": {
        "POIs": {
            ## KF 0.6-1.2 (ZZ 1.5)  KV 0.7-1.2 ; range for the scans, large enough to include BF points
            "kappa_V_gamgam": {"range":[0.7,1.2], "points":30},
            "kappa_V_WW": {"range":[0.7,1.2], "points":30},
            "kappa_V_ZZ": {"range":[0.7,1.2], "points":30},
            "kappa_V_mumu": {"range":[0.,5.0], "points":30},
            "kappa_V_tautau": {"range":[0.7,1.2], "points":30},
            "kappa_V_bb": {"range":[0.7,1.2], "points":30},
            "kappa_F_gamgam": {"range":[0.6,1.2], "points":30},
            "kappa_F_WW": {"range":[0.6,1.2], "points":30},
            "kappa_F_ZZ": {"range":[0.6,1.5], "points":30},
            "kappa_F_mumu": {"range":[0.0,5.0], "points":30},
            "kappa_F_tautau": {"range":[0.6,1.2], "points":30},
            "kappa_F_bb": {"range":[0.6,1.2], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"},
        "UseWsp": "K3"
        },

    "K3_5D_2D_N": {
        "POIs": {
            "kappa_V_gamgam": {"range":[0.4,1.8], "points":30},
            "kappa_V_WW": {"range":[0.4,1.8], "points":30},
            "kappa_V_ZZ": {"range":[0.4,1.8], "points":30},
            "kappa_V_mumu": {"range":[0.3,2.3], "points":30},
            "kappa_V_tautau": {"range":[0.4,1.8], "points":30},
            "kappa_V_bb": {"range":[0.4,1.8], "points":30},
            "kappa_F_gamgam": {"range":[-2.5,0], "points":30},
            "kappa_F_WW": {"range":[-2.5,0], "points":30},
            "kappa_F_ZZ": {"range":[-2.5,0], "points":30},
            "kappa_F_mumu": {"range":[-2.5,0], "points":30},
            "kappa_F_tautau": {"range":[-2.5,0], "points":30},
            "kappa_F_bb": {"range":[0,2.5], "points":30}
            },
        "POIsFix": {"kappa_V","kappa_F"}
        },

    "L2_ldu": {
        "POIs": {
            "lambda_du": {"range":[-2,2], "points":40},
            "lambda_Vu": {"range":[-2,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2"
    },

    "L2_ldu_N1": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2_ldu_N2": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2_ldu_N3": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": -1.0
        }
    },
    "L2_ldu_N4": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": -1.0
        }
    },

    "L2flipped_ldu": {
        "POIs": {
            "lambda_du": {"range":[-2,2], "points":40},
            "lambda_Vu": {"range":[-2,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped"
        },

    "L2flipped_ldu_N1": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2flipped_ldu_N2": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[0,2], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": +1.0
        }
    },
    "L2flipped_ldu_N3": {
        "POIs": {
            "lambda_du": {"range":[0,2], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": +1.0,
            "lambda_Vu": -1.0
        }
    },
    "L2flipped_ldu_N4": {
        "POIs": {
            "lambda_du": {"range":[-2,0], "points":40},
            "lambda_Vu": {"range":[-2,0], "points":40},
            "kappa_uu": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_qq","lambda_lq","lambda_Vq","kappa_VV","lambda_FV"},
        "UseWsp": "L2flipped_ldu",
        "POIsNominal": {
            "lambda_du": -1.0,
            "lambda_Vu": -1.0
        }
    },


    "L2_llq": {
        "POIs": {
            "lambda_lq": {"range":[-2,2], "points":40},
            "lambda_Vq": {"range":[-2,2], "points":40},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2"
    },
    "L2_llq_N1": {
        "POIs": {
            "lambda_lq": {"range":[0,2], "points":30},
            "lambda_Vq": {"range":[0,2], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": +1.0,
            "lambda_Vq": +1.0
        }
    },
    "L2_llq_N2": {
        "POIs": {
            "lambda_lq": {"range":[-2,0], "points":30},
            "lambda_Vq": {"range":[0,2], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": -1.0,
            "lambda_Vq": +1.0
        }
    },
    "L2_llq_N3": {
        "POIs": {
            "lambda_lq": {"range":[0,2], "points":30},
            "lambda_Vq": {"range":[-2,0], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": +1.0,
            "lambda_Vq": -1.0
        }
    },
    "L2_llq_N4": {
        "POIs": {
            "lambda_lq": {"range":[-2,0], "points":30},
            "lambda_Vq": {"range":[-2,0], "points":30},
            "kappa_qq": {"range":[0,2], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"},
        "UseWsp": "L2_llq",
        "POIsNominal": {
            "lambda_lq": -1.0,
            "lambda_Vq": -1.0
        }
    },
    "L2_llq_neg": {
        "POIs": {
            "lambda_lq": {"range":[-1.8,-0.3], "points":30},
            "lambda_Vq": {"range":[0.4,1.8], "points":30},
            "kappa_qq": {"range":[0.4,1.8], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_VV","lambda_FV"}
        },

    "L2_lfv": {
        "POIs": {
            "lambda_FV": {"range":[0,3], "points":30},
            "kappa_VV": {"range":[0,3], "points":30}
            },
        "POIsFix": {"kappa_uu","lambda_du","lambda_Vu","kappa_qq","lambda_lq","lambda_Vq"}
        },

    "A1_7D": {
        "POIs": {
            "mu_BR_WW": {"range":[0,2], "points":30},
            "mu_BR_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_BR_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_BR_mumu": {"range":[-4.0,4.0], "points":30},
            "mu_BR_tautau": {"range":[0,2.0], "points":30},
            "mu_BR_bb": {"range":[0,3], "points":30},
            "mu_BR_Zgam": {"range":[-3.0,5.0], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1 --PO dohzg=1"
        },
    "A1_5P": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.6,1.4], "points":40},
            "mu_XS_VBF": {"range":[0,2], "points":40},
            "mu_XS_WH": {"range":[0,5], "points":40},
            "mu_XS_ZH": {"range":[0,3], "points":40},
            "mu_XS_ttHtH": {"range":[0.5,2.5], "points":40}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        #"cards":["hbb_boosted_partial","hww_incl","hzz","tth_hbb","tth_multilepton","vhbb","hgg","htt_incl","hmm","hzg"],
        "cards":["hbb_boosted_incl","hww_stxs","hzz","tth_hbb","tth_multilepton","vhbb_stxs","hgg","htt_incl","hmm","hzg","vbfhbb"],
        "uncertainties":"uncertainties/brunc_mu.txt",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1 --PO dohzg=1"
        },
    "A1_6P": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.6,1.4], "points":40},
            "mu_XS_VBF": {"range":[0,2], "points":40},
            "mu_XS_WH": {"range":[0,5], "points":40},
            "mu_XS_ZH": {"range":[0,3], "points":40},
            "mu_XS_ttH": {"range":[0,2.5], "points":40},
            "mu_XS_tH": {"range":[0,12], "points":40},
            },
        "POIsFix":{},
        "UseWsp": "A1",
        },
    "A1_7P": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.6,1.4], "points":40},
            "mu_XS_VBF": {"range":[0,2], "points":40},
            "mu_XS_WH": {"range":[0,5], "points":40},
            "mu_XS_qqZH": {"range":[0,3], "points":40},
            "mu_XS_ggZH": {"range":[-2,12], "points":40},
            "mu_XS_ttH": {"range":[-2,2.5], "points":40},
            "mu_XS_tH": {"range":[-2,12], "points":40},
            },
        "POIsFix":{},
        "UseWsp": "A1",
        },
    "A1_7P_2D": {
        "POIs": {
            "mu_XS_qqZH": {"range":[0,3], "points":40},
            "mu_XS_ggZH": {"range":[0,10], "points":40},
            #"mu_XS_ttH": {"range":[-2,2.5], "points":40},
            #"mu_XS_tH": {"range":[-5,5], "points":40},
            },
        "POIsFix":{},
        "UseWsp": "A1_7P",
        },
    "A1_4P": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[0.5,1.9], "points":30},
            "mu_XS_VBF": {"range":[0,3], "points":30},
            "mu_XS_VH": {"range":[0,3], "points":30},
            "mu_XS_ttHtH": {"range":[0,5], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },


    "A1_muVmuF": {
        "POIs": {
            "mu_V_ZZ": {"range":[-2,5], "points":30},
            "mu_V_gamgam": {"range":[0,3], "points":30},
            "mu_V_WW": {"range":[0,3], "points":30},
            "mu_V_tautau": {"range":[0,3], "points":30},
            "mu_V_bb": {"range":[0,3], "points":30},
            "mu_F_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_F_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_F_WW": {"range":[0.0,2.0], "points":30},
            "mu_F_tautau": {"range":[0.0,2.5], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1"
        },

    "A1_muVmuF_2D": {
        "POIs": {
            "mu_V_ZZ": {"range":[-2,4], "points":30},
            "mu_V_gamgam": {"range":[0,5], "points":30},
            "mu_V_WW": {"range":[0,5], "points":30},
            "mu_V_tautau": {"range":[0,5], "points":30},
            "mu_V_bb": {"range":[0,5], "points":30},
            "mu_F_gamgam": {"range":[0.5,1.7], "points":30},
            "mu_F_ZZ": {"range":[0.5,1.7], "points":30},
            "mu_F_WW": {"range":[0.0,2.0], "points":30},
            "mu_F_tautau": {"range":[0.0,2.5], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1"
        },

    "A1_mu": {
        "POIs": {
            "mu": {"range":[0.7,1.3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1"
        },

    "A1_mu_ggH_VBF": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[-15,10], "points":30},
            "mu_XS_VBF": {"range":[-5,10], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "A1_mu_VBFHBB": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[-15,10], "points":30},
            "mu_XS_VBF": {"range":[-2,4], "points":30},
            "rate_zj_vbfhbb": {"range":[0,2], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "A1"
        },

    "custom_VBFHBB": {
        "POIs": {
            "r_ggH": {"range":[-15,10], "points":30},
            "r_qqH": {"range":[-2,4], "points":30},
            "rate_zj_vbfhbb": {"range":[0,2], "points":30},
            },
        "POIsFix":{},
        "UseWsp": "custom_VBFHBB",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \"map=.*/qqH_hbb:r_qqH[1,-30,30]\" --PO \"map=.*/ggH_hbb:r_ggH[1,-30,30]\""
        },

    "A1_mu_WH_ZH": {
        "POIs": {
            "mu_XS_WH": {"range":[0,5], "points":40},
            "mu_XS_ZH": {"range":[0,3], "points":40}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        },

    "A1_mu_ttH": {
        "POIs": {
            "mu_XS_ttH": {"range":[-1,3], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1"
        },

    "A1_mu_ttH_tH": {
        "POIs": {
            "mu_XS_ttH": {"range":[-1,3], "points":30},
            "mu_XS_tH": {"range":[-5,10], "points":30}
            },
        "POIsFix":{},
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1"
        },

    "A1_5PD": {
        "POIs": {
            "mu_XS_ggFbbH_BR_WW": {"range":[0.5,2.5], "points":30},
            "mu_XS_VBF_BR_WW": {"range":[-2,4], "points":30},
            "mu_XS_WH_BR_WW": {"range":[-3,15], "points":30},
            "mu_XS_ZH_BR_WW": {"range":[-10,10], "points":30},
            "mu_XS_ttHtH_BR_WW": {"range":[-1,4], "points":30},
            "mu_XS_ggFbbH_BR_ZZ": {"range":[0,2], "points":30},
            "mu_XS_VBF_BR_ZZ": {"range":[0,5], "points":30},
            "mu_XS_WH_BR_ZZ": {"range":[0,15], "points":30},
            "mu_XS_ZH_BR_ZZ": {"range":[0,20], "points":30},
            "mu_XS_ttHtH_BR_ZZ": {"range":[0,15], "points":30},
            "mu_XS_ggFbbH_BR_bb": {"range":[-5,10], "points":30},
            "mu_XS_VBF_BR_bb": {"range":[-5,10], "points":30},
            "mu_XS_WH_BR_bb": {"range":[-2,4], "points":30},
            "mu_XS_ZH_BR_bb": {"range":[-3,3], "points":30},
            "mu_XS_ttHtH_BR_bb": {"range":[-1,3], "points":30},
            "mu_XS_ggFbbH_BR_gamgam": {"range":[0,2], "points":30},
            "mu_XS_VBF_BR_gamgam": {"range":[-1,3], "points":30},
            "mu_XS_WH_BR_gamgam": {"range":[-10,10], "points":30},
            "mu_XS_ZH_BR_gamgam": {"range":[0,15], "points":30},
            "mu_XS_ttHtH_BR_gamgam": {"range":[-1,6], "points":30},
            "mu_XS_ggFbbH_BR_tautau": {"range":[-1,3.5], "points":30},
            "mu_XS_VBF_BR_tautau": {"range":[0,2.5], "points":30},
            "mu_XS_WH_BR_tautau": {"range":[-2,8], "points":30},
            "mu_XS_ZH_BR_tautau": {"range":[-2,8], "points":30},
            "mu_XS_ttHtH_BR_tautau": {"range":[-2,5], "points":30},
            "mu_XS_ggFbbH_BR_mumu": {"range":[-5,5], "points":30},
            "mu_XS_VBF_BR_mumu": {"range":[-5,10], "points":30},
            "mu_XS_VH_BR_mumu": {"range":[-10,15], "points":30},
            "mu_XS_ttHtH_BR_mumu": {"range":[-5,10], "points":30},
            "mu_XS_ggFbbH_BR_Zgam": {"range":[-5,10], "points":30},
            "mu_XS_VBF_BR_Zgam": {"range":[-15,20], "points":30},
            #"mu_XS_VHttHtH_BR_Zgam": {"range":[-40,40], "points":30}
            },
        "POIsFix":{"mu_XS_VHttHtH_BR_Zgam"},
        "cards":["hgg","hzz","hww_stxs","htt_incl","tth_hbb","tth_multilepton","hbb_boosted_incl","vbfhbb","hmm","hzg","vhbb_stxs"],
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1 --PO dohzg=1",
        "uncertainties":"uncertainties/brunc_mu.txt",
        },

    "A2": {
        "POIs": {
            "mu_V_r_F": {"range":[0,3], "points":30},
            "mu_F_gamgam": {"range":[0,3], "points":30},
            "mu_F_ZZ": {"range":[0,3], "points":30},
            "mu_F_WW": {"range":[0,3], "points":30},
            "mu_F_tautau": {"range":[0,3], "points":30},
            "mu_F_bb": {"range":[0,3], "points":30}
            },
        "POIsFix": {"mu_V_r_F_WW","mu_V_r_F_ZZ","mu_V_r_F_gamgam","mu_V_r_F_bb","mu_V_r_F_tautau"},
        "UseWsp": "A2",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A2"
        },

    "A2_5D": {
        "POIs": {
            "mu_F_gamgam": {"range":[0,5], "points":30},
            "mu_F_ZZ": {"range":[0,5], "points":30},
            "mu_F_WW": {"range":[0,5], "points":30},
            "mu_F_tautau": {"range":[0,5], "points":30},
            "mu_F_bb": {"range":[0,5], "points":30},
            "mu_V_r_F_ZZ": {"range":[0,20], "points":30}
            },
        "POIsFix": {"mu_V_r_F"},
        "UseWsp": "A1"
        },

    "B1": {
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[0.0,2.0], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[0.0,5.0], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-1.0,3.0], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0.0,3.0], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_bb_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_mumu_r_BR_WW": {"range":[0.0,5.0], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[0.0,3.0], "points":30},
            "mu_XS_ggF_x_BR_WW": {"range":[0.5,2.0], "points":30}
            },
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu","mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"},
        "UseWsp": "B1"
        },

    "B1ZZ": {
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[0.0,2.0], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[0.0,5.0], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-1.0,3.0], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0.0,3.0], "points":30},
            "mu_BR_WW_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_bb_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_mumu_r_BR_ZZ": {"range":[-2.0,5.0], "points":30},
            "mu_BR_tautau_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_BR_gamgam_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
            "mu_XS_ggF_x_BR_ZZ": {"range":[0.5,2.0], "points":30}
            },
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu","mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        "POIsFix": {"mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"},
        "UseWsp": "B1ZZ"
        },

    "B1WW_P78": {
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[-5,5], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-20,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_bb_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS_ggF_x_BR_WW": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_VBF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_WH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ZH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ggF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_ttH": {"range":[-10,10], "points":30}
            },
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        },

    "B1ZZ_P78": {
        "POIs": {
            "mu_XS_VBF_r_XS_ggF": {"range":[-5,5], "points":30},
            "mu_XS_WH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_XS_ZH_r_XS_ggF": {"range":[-20,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[-10,10], "points":30},
            "mu_BR_WW_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_bb_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_tautau_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_BR_gamgam_r_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_XS_ggF_x_BR_ZZ": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_VBF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_WH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ZH": {"range":[-10,10], "points":30},
            "mu_XS7_r_XS8_ggF": {"range":[-5,5], "points":30},
            "mu_XS7_r_XS8_ttH": {"range":[-10,10], "points":30}
            },
        "POIsFix": {"mu_XS7_r_XS8_VBF","mu_XS7_r_XS8_WH","mu_XS7_r_XS8_ZH","mu_XS7_r_XS8_ggF","mu_XS7_r_XS8_ttH"}
        },

    "B2": {
        "POIs": {
            "mu_XS_ggF_x_BR_WW": {"range":[0,5], "points":30},
            "mu_XS_VBF_x_BR_tautau": {"range":[0,5], "points":30},
            "mu_XS_WH_r_XS_VBF": {"range":[0,30], "points":30},
            "mu_XS_ZH_r_XS_WH": {"range":[0,20], "points":30},
            "mu_XS_ttH_r_XS_ggF": {"range":[0,10], "points":30},
            "mu_BR_ZZ_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_gamgam_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_tautau_r_BR_WW": {"range":[0,5], "points":30},
            "mu_BR_bb_r_BR_tautau": {"range":[0,5], "points":30}
            },
        #"POIsFix": {"'rgx{.*THU.*}'","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"}
        "POIsFix": {}
        },

    "D1_general": {
        "POIs": {
            "mu_WW": {"range":[0,5], "points":30},
            "mu_ZZ": {"range":[0,5], "points":30},
            "mu_gamgam": {"range":[0,5], "points":30},
            "mu_tautau": {"range":[0,5], "points":30},
            "l_VBF_gamgam": {"range":[0,5], "points":30},
            "l_VBF_WW": {"range":[0,5], "points":30},
            "l_VBF_ZZ": {"range":[0,10], "points":30},
            "l_VBF_tautau": {"range":[0,5], "points":30},
            "l_WH_gamgam": {"range":[0,30], "points":30},
            "l_WH_WW": {"range":[0,10], "points":30},
            "l_WH_ZZ": {"range":[0,30], "points":30},
            "l_WH_tautau": {"range":[0,10], "points":30},
            "l_WH_bb": {"range":[0,10], "points":30},
            "l_ZH_gamgam": {"range":[0,10], "points":30},
            "l_ZH_WW": {"range":[0,20], "points":30},
            "l_ZH_ZZ": {"range":[0,50], "points":30},
            "l_ZH_tautau": {"range":[0,20], "points":30},
            "l_ZH_bb": {"range":[0,5], "points":30},
            "l_ttH_gamgam": {"range":[0,20], "points":30},
            "l_ttH_WW": {"range":[0,10], "points":30},
            "l_ttH_ZZ": {"range":[0,50], "points":30},
            "l_ttH_tautau": {"range":[0,30], "points":30},
            "l_ttH_bb": {"range":[0,10], "points":30}
            },
        "POIsFix": {"l_VBF","l_WH","l_ZH","l_ttH","mu_bb"}
        },

    "D1_rank1": {
        "POIs": {
            "mu_WW": {"range":[0,5], "points":30},
            "mu_ZZ": {"range":[0,5], "points":30},
            "mu_gamgam": {"range":[0,5], "points":30},
            "mu_tautau": {"range":[0,5], "points":30},
            "mu_bb": {"range":[0,5], "points":30},
            "l_VBF": {"range":[0,5], "points":30},
            "l_WH": {"range":[0,10], "points":30},
            "l_ZH": {"range":[0,10], "points":30},
            "l_ttH": {"range":[0,10], "points":30}
            },
        "POIsFix": {"l_VBF_gamgam","l_VBF_WW","l_VBF_ZZ","l_VBF_tautau","l_WH_gamgam","l_WH_WW","l_WH_ZZ","l_WH_tautau","l_WH_bb","l_ZH_gamgam","l_ZH_WW","l_ZH_ZZ","l_ZH_tautau","l_ZH_bb","l_ttH_gamgam","l_ttH_WW","l_ttH_ZZ","l_ttH_tautau","l_ttH_bb"}
        },

    "stage0": {
        "POIs": {
             "mu_XS_ggH_x_BR_WW": {"range":[0.0,2.5], "points":30},
             "mu_XS_qqH_x_BR_WW": {"range":[0.0,2.5], "points":30},
             "mu_XS_VH2HQQ_x_BR_WW": {"range":[0.0,15.0], "points":30},
             "mu_XS_QQ2HLNU_x_BR_WW": {"range":[0.0,5.0], "points":30},
             "mu_XS_QQ2HLL_x_BR_WW": {"range":[0.0,5.0], "points":30},
             "mu_XS_ttH_x_BR_WW": {"range":[-1.0,3.0], "points":30},
             "mu_BR_bb_r_BR_WW": {"range":[0.0,3.0], "points":30},
             "mu_BR_tautau_r_BR_WW": {"range":[0.0,2.0], "points":30},
             "mu_BR_ZZ_r_BR_WW": {"range":[0.0,1.5], "points":30},
             "mu_BR_gamgam_r_BR_WW": {"range":[0.3,1.8], "points":30},
             "mu_BR_mumu_r_BR_WW": {"range":[0.0,4.0], "points":30},
            },
        "POIsFix": {"mu_BR_gluglu_r_BR_WW","mu_BR_cc_r_BR_WW","THU_ggH_Mu","THU_ggH_Res","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"},
        "UseWsp": "stage0"
        },

    "stage0ZZ": {
        "POIs": {
             "mu_XS_ggH_x_BR_ZZ": {"range":[0.4,2.0], "points":30},
             "mu_XS_qqH_x_BR_ZZ": {"range":[0.0,2.5], "points":30},
             "mu_XS_VH2HQQ_x_BR_ZZ": {"range":[0.0,15.0], "points":30},
             "mu_XS_QQ2HLNU_x_BR_ZZ": {"range":[0.0,5.0], "points":30},
             "mu_XS_QQ2HLL_x_BR_ZZ": {"range":[0.0,5.0], "points":30},
             "mu_XS_ttH_x_BR_ZZ": {"range":[-1.0,3.0], "points":30},
             "mu_BR_bb_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
             "mu_BR_tautau_r_BR_ZZ": {"range":[0.0,2.0], "points":30},
             "mu_BR_WW_r_BR_ZZ": {"range":[0.0,3.0], "points":30},
             "mu_BR_gamgam_r_BR_ZZ": {"range":[0.3,1.8], "points":30},
             "mu_BR_mumu_r_BR_ZZ": {"range":[-2.0,4.0], "points":30},
            },
        "POIsFix": {"mu_BR_gluglu_r_BR_ZZ","mu_BR_cc_r_BR_ZZ","THU_ggH_Mu","THU_ggH_Res","QCDscale_qqH","QCDscale_VH","QCDscale_ggZH","QCDscale_ttH","pdf_Higgs_gg","pdf_Higgs_qqbar","pdf_Higgs_qg","CMS_vhbb_boost_EWK_13TeV","CMS_vhbb_boost_QCD_13TeV","QCDscale_VH_ggZHacceptance_highPt","param_alphaS","param_mB","param_mC","param_mt","HiggsDecayWidthTHU_hqq","HiggsDecayWidthTHU_hvv","HiggsDecayWidthTHU_hll","HiggsDecayWidthTHU_hgg","HiggsDecayWidthTHU_hzg","HiggsDecayWidthTHU_hgluglu"}
        },

    "mEpsHiggs": {
        "POIs": {
             "M": {"range":[200.0,300.0], "points":30},
             "eps": {"range":[-0.15,0.15], "points":30},
            },
        "POIsFix": {},
        "UseWsp": "mEpsHiggs",
        "SMVals": {
          "M": 246.22,
          "eps": 0.0
          }
        },
    "TwoHDM-I":{
            "POIs":{
                "cosbma":{"range":[-0.8,0.8],"points":30,},
                "tanb":{"range":[0.1,10],"points":30,},
                },
            "POIsFix":{},
            "SMVals":{
                "cosbma":0.,
                "tanb":10., ##?!? irrelevant, we usually do CLs on these.
                },
        #"UseWsp": "STXS",
        #"cards":["hbb_boosted","hww","hzz","tth_hbb","tth_multilepton","vhbb","hgg","htt_stxs"],
        #"uncertainties":"uncertainties/brunc_mu.txt",
            "T2WOpts": "-P HiggsAnalysis.CombinedLimit.AdditionalModels:twohdm --PO thdmtype=1",
    },

    "TestComb": {
        "POIs": {
            "mu_XS_ggFbbH": {"range":[-1,3], "points":30},
            "mu_XS_VBF": {"range":[-1,3], "points":30},
            },
        "POIsFix" : {},
        "cards":["hmm","hzg"],
        "UseWsp": "A1",
        "T2WOpts": "-P HiggsAnalysis.CombinedLimit.LHCHCGModels:A1 --PO dohzg=1",
    },

}

def GetWsp(model):
    if model in getPOIs and 'UseWsp' in getPOIs[model]:
        return getPOIs[model]['UseWsp']
    else:
        return model

def GetPOIsList(model, sep=',', onlyScanPOIs=False):
    POIs = list(getPOIs[model]["POIs"].keys())
    if onlyScanPOIs and 'ScanPOIs' in getPOIs[model]:
        POIs = getPOIs[model]['ScanPOIs']
    return sep.join(POIs)

def GetPOIRanges(model):
    poiRanges = ':'.join(['%s=%g,%g' % (POI, d["range"][0], d["range"][1]) for POI, d in six.iteritems(getPOIs[model]["POIs"])])
    return poiRanges
    #return poiRanges + ':qcdeff=0.0001,1.0:r0p1=0.9,1.4:r1p0=0.8,1.3:r1p1=0.4,0.6:r2p0=1.9,2.3:r2p1=-1.0,-0.3'


def SetSMVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if "SMVal" in  getPOIs[model]["POIs"][POI]:
            defVal = getPOIs[model]["POIs"][POI]['SMVal']
        elif 'SMVals' in getPOIs[model] and POI in getPOIs[model]['SMVals']:
            defVal = getPOIs[model]['SMVals'][POI]
        set_args.append('%s=%g' % (POI, defVal))
    if "SetParam" in getPOIs[model]:
        for param, val in getPOIs[model]["SetParam"].items():
            set_args.append('%s=%g' % (param, val ) )
    ## A1_5PD observed category indexes. This should avoid a v2 on the initial fits
    set_args.append("CMS_hzg_pdfindex_ele_mu_cat1_2020_13TeV=1,CMS_hzg_pdfindex_ele_mu_cat2_2020_13TeV=1,CMS_hzg_pdfindex_ele_mu_cat3_2020_13TeV=3,CMS_hzg_pdfindex_ele_mu_cat4_2020_13TeV=1,CMS_hzg_pdfindex_ele_mu_cat501_2020_13TeV=6,CMS_hzg_pdfindex_ele_mu_cat502_2020_13TeV=7,CMS_hzg_pdfindex_ele_mu_cat503_2020_13TeV=6,CMS_hzg_pdfindex_ele_mu_cat6789_2020_13TeV=1,pdf_index_ggh=2,pdfindex_RECO_0J_PTH_0_10_Tag0_13TeV=0,pdfindex_RECO_0J_PTH_0_10_Tag1_13TeV=2,pdfindex_RECO_0J_PTH_0_10_Tag2_13TeV=0,pdfindex_RECO_0J_PTH_GT10_Tag0_13TeV=1,pdfindex_RECO_0J_PTH_GT10_Tag1_13TeV=0,pdfindex_RECO_0J_PTH_GT10_Tag2_13TeV=0,pdfindex_RECO_1J_PTH_0_60_Tag0_13TeV=1,pdfindex_RECO_1J_PTH_0_60_Tag1_13TeV=1,pdfindex_RECO_1J_PTH_0_60_Tag2_13TeV=2,pdfindex_RECO_1J_PTH_120_200_Tag0_13TeV=1,pdfindex_RECO_1J_PTH_120_200_Tag1_13TeV=0,pdfindex_RECO_1J_PTH_120_200_Tag2_13TeV=0,pdfindex_RECO_1J_PTH_60_120_Tag0_13TeV=2,pdfindex_RECO_1J_PTH_60_120_Tag1_13TeV=0,pdfindex_RECO_1J_PTH_60_120_Tag2_13TeV=1,pdfindex_RECO_GE2J_PTH_0_60_Tag0_13TeV=1,pdfindex_RECO_GE2J_PTH_0_60_Tag1_13TeV=1,pdfindex_RECO_GE2J_PTH_0_60_Tag2_13TeV=0,pdfindex_RECO_GE2J_PTH_120_200_Tag0_13TeV=0,pdfindex_RECO_GE2J_PTH_120_200_Tag1_13TeV=0,pdfindex_RECO_GE2J_PTH_120_200_Tag2_13TeV=0,pdfindex_RECO_GE2J_PTH_60_120_Tag0_13TeV=0,pdfindex_RECO_GE2J_PTH_60_120_Tag1_13TeV=0,pdfindex_RECO_GE2J_PTH_60_120_Tag2_13TeV=0,pdfindex_RECO_PTH_200_300_Tag0_13TeV=0,pdfindex_RECO_PTH_200_300_Tag1_13TeV=0,pdfindex_RECO_PTH_300_450_Tag0_13TeV=1,pdfindex_RECO_PTH_300_450_Tag1_13TeV=0,pdfindex_RECO_PTH_450_650_Tag0_13TeV=0,pdfindex_RECO_PTH_GT650_Tag0_13TeV=0,pdfindex_RECO_THQ_LEP_13TeV=1,pdfindex_RECO_TTH_HAD_PTH_0_60_Tag0_13TeV=1,pdfindex_RECO_TTH_HAD_PTH_0_60_Tag1_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_0_60_Tag2_13TeV=1,pdfindex_RECO_TTH_HAD_PTH_120_200_Tag0_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_120_200_Tag1_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_120_200_Tag2_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_120_200_Tag3_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_200_300_Tag0_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_200_300_Tag1_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_200_300_Tag2_13TeV=1,pdfindex_RECO_TTH_HAD_PTH_60_120_Tag0_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_60_120_Tag1_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_60_120_Tag2_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_GT300_Tag0_13TeV=0,pdfindex_RECO_TTH_HAD_PTH_GT300_Tag1_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_0_60_Tag0_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_0_60_Tag1_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_0_60_Tag2_13TeV=2,pdfindex_RECO_TTH_LEP_PTH_120_200_Tag0_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_120_200_Tag1_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_200_300_Tag0_13TeV=0,pdfindex_RECO_TTH_LEP_PTH_60_120_Tag0_13TeV=1,pdfindex_RECO_TTH_LEP_PTH_60_120_Tag1_13TeV=2,pdfindex_RECO_TTH_LEP_PTH_60_120_Tag2_13TeV=2,pdfindex_RECO_TTH_LEP_PTH_GT300_Tag0_13TeV=0,pdfindex_RECO_VBFLIKEGGH_Tag0_13TeV=0,pdfindex_RECO_VBFLIKEGGH_Tag1_13TeV=2,pdfindex_RECO_VBFTOPO_BSM_Tag0_13TeV=2,pdfindex_RECO_VBFTOPO_BSM_Tag1_13TeV=0,pdfindex_RECO_VBFTOPO_JET3_HIGHMJJ_Tag0_13TeV=1,pdfindex_RECO_VBFTOPO_JET3_HIGHMJJ_Tag1_13TeV=0,pdfindex_RECO_VBFTOPO_JET3_LOWMJJ_Tag0_13TeV=0,pdfindex_RECO_VBFTOPO_JET3_LOWMJJ_Tag1_13TeV=0,pdfindex_RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0_13TeV=1,pdfindex_RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1_13TeV=0,pdfindex_RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0_13TeV=0,pdfindex_RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1_13TeV=1,pdfindex_RECO_VBFTOPO_VHHAD_Tag0_13TeV=1,pdfindex_RECO_VBFTOPO_VHHAD_Tag1_13TeV=0,pdfindex_RECO_VH_MET_Tag0_13TeV=0,pdfindex_RECO_VH_MET_Tag1_13TeV=0,pdfindex_RECO_VH_MET_Tag2_13TeV=0,pdfindex_RECO_WH_LEP_PTV_0_75_Tag0_13TeV=2,pdfindex_RECO_WH_LEP_PTV_0_75_Tag1_13TeV=0,pdfindex_RECO_WH_LEP_PTV_75_150_Tag0_13TeV=0,pdfindex_RECO_WH_LEP_PTV_75_150_Tag1_13TeV=0,pdfindex_RECO_WH_LEP_PTV_GT150_Tag0_13TeV=0,pdfindex_RECO_ZH_LEP_Tag0_13TeV=0,pdfindex_RECO_ZH_LEP_Tag1_13TeV=0")
    return ','.join(set_args)

def SetNominalVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if 'POIsNominal' in getPOIs[model] and POI in getPOIs[model]['POIsNominal']:
            defVal = getPOIs[model]['POIsNominal'][POI]
            set_args.append('%s=%g' % (POI, defVal))
    return ','.join(set_args)

def GetFreezeList(model):
    return ','.join(list(getPOIs[model]['POIsFix']))
    #return ','.join(list(getPOIs[model]['POIsFix']) + ['zmod_cat6_ord1_b', 'zmod_cat5_ord1_b', 'zmod_cat11_ord1_b', 'zmod_cat13_ord1_b', 'zmod_cat14_ord1_b'])

def GetGeneratePOIs(model):
    doPOIs = list(getPOIs[model]["POIs"].keys())
    if 'ScanPOIs' in getPOIs[model]:
        doPOIs = getPOIs[model]['ScanPOIs']
    ret = 'P:n::'
    ret += ':'.join(['%s,%s' % (X,X) for X in doPOIs])
    if '_2D' in model and len(doPOIs) == 2: ret=" -P " + doPOIs[0] +" -P "+doPOIs[1]
    if 'K3_5D_2D' == model:
        ## assume the following form, to pair them
        ## pois = kappa_V/F_xxx
        ret = '${P1}:${P2}:n::'
        decays = list(set([ x.split('_')[2] for x in doPOIs ]))
        ret_pairs=[] ## do the pairing
        for d in decays:
            p1 = 'kappa_V_'+d
            p2 = 'kappa_F_'+d
            if p1 not in doPOIs: raise ValueError("Expected POI: "+p1)
            if p2 not in doPOIs: raise ValueError("Expected POI: "+p2)
            ret_pairs.append(','.join([p1,p2,d]))
        ret += ':'.join(ret_pairs)
    return ret

def GetRangeGeneratePOIs(model):
    doPOIs = list(getPOIs[model]["POIs"].keys())
    for POI, d in six.iteritems(getPOIs[model]["POIs"]):
        if 'scan' not in d:
            return GetGeneratePOIs(model)
    if 'ScanPOIs' in getPOIs[model]:
        doPOIs = getPOIs[model]['ScanPOIs']
    ret = 'P:n:centeredRange::'
    ret += ':'.join(['%s,%s,%f' % (X,X, getPOIs[model]["POIs"][X]['scan']) for X in doPOIs])
    return ret

def GetMinimizerOpts(label='Default'):
    #return '--floatOtherPOIs 1 --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --cminFallbackAlgo Minuit2,Migrad,0:0.1 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_skipDiscreteIterations --X-rtd OPTIMIZE_BOUNDS=0 --X-rtd NO_INITIAL_SNAP --X-rtd SIMNLL_GROUPCONSTRAINTS=10'

    baseline_args = '--noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --cminFallbackAlgo Minuit2,Migrad,0:0.1 --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --X-rtd OPTIMIZE_BOUNDS=0 --X-rtd NO_INITIAL_SNAP --X-rtd SIMNLL_GROUPCONSTRAINTS=10 --X-rtd CACHINGPDF_NOCLONE'
    if label in ['EFT','fixed']:
        return baseline_args
    else:
        return '--floatOtherPOIs 1 %s' % baseline_args

def GetT2WOpts(model):
    opts = '--for-fits --no-wrappers --optimize-simpdf-constraints cms --X-pack-asympows --X-optimizeMHDependency=fixed -m 125.38 --use-histsum'
    if model in getPOIs and 'T2WOpts' in getPOIs[model]:
        return getPOIs[model]['T2WOpts']+' '+opts
    else:
        raise ValueError("Model has no t2w options. Probably wrong.")
        return opts

def GetCards(model,sep=' '):
    cards = getPOIs[model]["cards"][:]
    full= ['comb_2021_'+c+'.txt.gz' for c in cards]
    return sep.join(full)

def GetUncertainties(model):
    return getPOIs[model]['uncertainties'] if 'uncertainties' in getPOIs[model] else '/dev/null'

if __name__ == "__main__":
    import sys
    model = getPOIs[sys.argv[1]]

    if sys.argv[2] == '-m':
        print(GetWsp(sys.argv[1]))

    if sys.argv[2] == '-p':
        print(GetPOIsList(sys.argv[1]))

    if sys.argv[2] == '-P':
        print(GetPOIsList(sys.argv[1], sep=' ', onlyScanPOIs=True))

    if sys.argv[2] == '-r':
        print(GetPOIRanges(sys.argv[1]))

    # if sys.argv[2] == '-R':
    #     print(GetPOISpecialRanges(sys.argv[1], sys.argv[3]))

    if sys.argv[2] == '-s':
        print(SetSMVals(sys.argv[1]))

    if sys.argv[2] == '-n':
        print(SetNominalVals(sys.argv[1]))

    if sys.argv[2] == '-f':
        print(GetFreezeList(sys.argv[1]))

    if sys.argv[2] == '-g':
        print(GetGeneratePOIs(sys.argv[1]))

    if sys.argv[2] == '-G':
        print(GetRangeGeneratePOIs(sys.argv[1]))

    if sys.argv[2] == '-F':
        flist = GetFreezeList(sys.argv[1])
        if flist == '':
            print('')
        else:
            print(',' + GetFreezeList(sys.argv[1]))

    if sys.argv[2] == '-C':
        print(GetCards(sys.argv[1]))
    if sys.argv[2] == '-U':
        print(GetUncertainties(sys.argv[1]))

    if sys.argv[2] == '-O':
        if len(sys.argv) >= 4:
            print(GetMinimizerOpts(sys.argv[3]))
        else:
            print(GetMinimizerOpts())

    if sys.argv[2] == '-t':
        print(GetT2WOpts(sys.argv[1]))
