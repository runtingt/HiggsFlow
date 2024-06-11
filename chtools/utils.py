# import CombineHarvester.CombineTools.ch as ch
# import ROOT
# import os
from __future__ import absolute_import
from __future__ import print_function
import re
import pprint
from scipy.optimize import curve_fit
from scipy import stats
# import argparse
# from collections import defaultdict
# import sys
from subprocess import *
from six.moves import range

protected_list=['QCDScale','THU','VH_scale', 'WH_scale','ZH_scale','ggH_scale','vbf_scale','ttH_scale','pdf_Higgs','qqVH_NLOEWK','pdf_As_Higgs','CMS_ttHbb_scaleMu','CMS_LHE_weights','QCDscale','pdf_WH','pdf_ZH','pdf_ggH','pdf_qqH']


def processCmd(cmd, quiet=0):
    output = ''
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output = output + str(line)
    p.stdout.close()
    return output


def ForEachProcAndSyst(cb, func):
    cb.ForEachProc(func)
    cb.ForEachSyst(func)


def MultiReplace(proc, replacements, useRegex=False):
    for old, new in replacements:
        if useRegex:
            proc.set_process(re.sub(old, new, proc.process()))
        else:
            proc.set_process(proc.process().replace(old, new))


def GetProcess(cb, bin, process):
    procs = []
    cb.cp().bin([bin]).process([process]).ForEachProc(lambda x: procs.append(x))
    if len(procs) == 1:
        return procs[0]
    else:
        raise RuntimeError('Request for process %s in bin %s yielded %i results' % (process, bin, len(procs)))


def AdjustTemplateErrors(proc, systs, strict=True, verbosity=0,resetErrors=True):
    shape = proc.shape().Clone()
    # ShapeAsTH1F() returns a TH1 normalized to 1.0, so we scale it up:
    shape.Scale(proc.rate())
    # Clone the current TH1, and set all bin errors to zero
    new_shape = shape.Clone()
    if resetErrors:
        for ib in range(1, shape.GetNbinsX() + 1):
            new_shape.SetBinError(ib, 0.)
    successful_systs = []
    unsuccessful_systs = []
    for syst in systs:
        if verbosity > 2:
            print('>> [AdjustTemplateErrors] working on %s' % syst.name())
        # Similarly to the above, scale the Up and Down to the correct norm
        shape_u = syst.shape_u().Clone()
        shape_u.Scale(syst.value_u() * proc.rate())
        shape_d = syst.shape_d().Clone()
        shape_d.Scale(syst.value_d() * proc.rate())

        # Find the bin where this shape uncertainty has the largest variation
        # from the nominal
        max_val = 0
        max_err = 0
        max_bin = -1
        max_delta_u = 0
        max_delta_d = 0
        for ib in range(1, shape.GetNbinsX() + 1):
            err = shape.GetBinError(ib)
            delta_u = shape_u.GetBinContent(ib) - shape.GetBinContent(ib)
            delta_d = shape_d.GetBinContent(ib) - shape.GetBinContent(ib)
            this_max = max(abs(delta_d), abs(delta_u))
            if this_max > max_val:
                max_val = this_max
                max_delta_u = delta_u
                max_delta_d = delta_d
                max_bin = ib
                max_err = err
        if verbosity > 2:
            print('>> [AdjustTemplateErrors] Bin %i identified: Error %f, deltaUp %f, deltaDown %f' % (max_bin, max_err, max_delta_u, max_delta_d))
        if max_delta_u == 0 and max_delta_d == 0:
            if verbosity > 2:
                print('>> [AdjustTemplateErrors] "Syst %s has no effect at all, will be discarded.' % syst.name())
            successful_systs.append(syst.name())
            continue
        if (max_delta_u - max_delta_d) == 0:
            print('>> [AdjustTemplateErrors] ERROR: %s Bin %i : Error %f, deltaUp %r, deltaDown %r' % (syst.name(), max_bin, max_err, max_delta_u, max_delta_d))
        # Now verify the Up and Down shifts are equal in magnitude, using the
        # magnitude of (dUp - dDown)/ mean(dUp, dDown)
        rel = 2. * (max_delta_u + max_delta_d) / (max_delta_u - max_delta_d)
        if abs(rel) < 0.01:
            new_shape.SetBinError(max_bin, (abs(max_delta_u) + abs(max_delta_d)) / 2.)
            successful_systs.append(syst.name())
        else:
            if strict:
                if verbosity > 2:
                    print('>> [AdjustTemplateErrors] Bin NOT viable with rel = %f, skipping' % rel)
                unsuccessful_systs.append(syst.name())
            else:
                # new_err = max(abs(max_delta_u), abs(max_delta_d))
                new_err = (abs(max_delta_u) + abs(max_delta_d)) / 2.
                if verbosity > 2:
                    print('>> [AdjustTemplateErrors] Bin NOT viable with rel = %f, setting to %f' % (rel, new_err))
                new_shape.SetBinError(max_bin, new_err)
                successful_systs.append(syst.name())
    # Replace the TH1 in the ch::Process object
    proc.set_shape(new_shape, False)
    # Return lists of systs successfully and unsuccessfully replaced
    return successful_systs, unsuccessful_systs


def SimpleReplaceMCStats(cb_full, cb_filtered, pattern):
    autoMCStatsBins = list(cb_full.GetAutoMCStatsBins())
    drop = list(cb_filtered.cp().syst_name([pattern]).syst_name_set())
    print('>> [SimpleReplaceMCStats] dropping %i bin-by-bin parameters' % len(drop))
    cb_full.syst_name(drop, False)
    target = cb_filtered.cp().bin(autoMCStatsBins, False)
    print('>> [SimpleReplaceMCStats] Enabling autoMCStats with threshold 0 for bins:')
    pprint.pprint(target.bin_set(), indent=4)
    target.SetAutoMCStats(cb_full, 0.0)


def ReplaceMCStats(cb_full, cb_filtered, pattern, strict=True, alwaysConvert=True, verbosity=0):
    autoMCStatsBins = list(cb_full.GetAutoMCStatsBins())
    bins = [x for x in cb_filtered.bin_set() if x not in autoMCStatsBins]
    removed_systs = []
    removed_systs_failed = []
    for b in bins:
        removed_systs_bin = []
        removed_systs_failed_bin = []
        if verbosity:
            print('>> [ReplaceMCStats] working on bin %s' % b)
        cb_bin = cb_filtered.cp().bin([b])
        if alwaysConvert and len(cb_bin.cp().syst_name([pattern]).syst_name_set()) == 0:
            print('>> [ReplaceMCStats] no shape uncertainties matching pattern, setting autoMCStats to -1')
            cb_bin.SetAutoMCStats(cb_full, -1.)
            continue
        # Now go process-by-process
        procs = cb_bin.process_set()
        for p in procs:
            systs = []
            cb_bin.cp().process([p]).syst_name([pattern]).ForEachSyst(lambda x: systs.append(x))
            proc = GetProcess(cb_bin, b, p)
            done, failed = AdjustTemplateErrors(proc, systs, strict=strict, verbosity=verbosity)
            removed_systs_bin.extend(done)
            removed_systs_failed_bin.extend(failed)
        if len(removed_systs_bin) > 0:
            cb_bin.SetAutoMCStats(cb_full, 0.0)
        if verbosity > 1:
            print('>> [ReplaceMCStats] successfully removed %i shape uncertainties from bin %s' % (len(removed_systs_bin), b))
            print(removed_systs_bin)
            if len(removed_systs_failed_bin):
                print('>> [ReplaceMCStats] unable to remove %i shape uncertainties from bin %s' % (len(removed_systs_failed_bin), b))
                print(removed_systs_failed_bin)
        removed_systs.extend(removed_systs_bin)
        removed_systs_failed.extend(removed_systs_failed_bin)
    if len(removed_systs) > 0:
        cb_full.syst_name(removed_systs, False)
    if verbosity:
        print('>> [ReplaceMCStats] successfully removed total of %i shape uncertainties' % len(removed_systs))
        if len(removed_systs_failed):
            print('>> [ReplaceMCStats] unable to remove total of %i shape uncertainties' % len(removed_systs_failed))

def AddToMCStats(cb_full, cb_filtered, pattern, strict=True, alwaysConvert=True, verbosity=0):
    autoMCStatsBins = list(cb_full.GetAutoMCStatsBins())
    bins = [x for x in cb_filtered.bin_set() if x not in autoMCStatsBins]
    removed_systs = []
    removed_systs_failed = []
    for b in autoMCStatsBins: ### probably will need to run something different if this is a merge of the two
        removed_systs_bin = []
        removed_systs_failed_bin = []
        if verbosity:
            print('>> [AddToMCStats] working on bin %s' % b)
        cb_bin = cb_filtered.cp().bin([b])
        if alwaysConvert and len(cb_bin.cp().syst_name([pattern]).syst_name_set()) == 0:
            print('>> [AddToMCStats] no shape uncertainties matching pattern')
            #cb_bin.SetAutoMCStats(cb_full, -1.)
            continue
        # Now go process-by-process
        procs = cb_bin.process_set()
        for p in procs:
            systs = []
            cb_bin.cp().process([p]).syst_name([pattern]).ForEachSyst(lambda x: systs.append(x))
            proc = GetProcess(cb_bin, b, p)
            done, failed = AdjustTemplateErrors(proc, systs, strict=strict, verbosity=verbosity,resetErrors=False)
            removed_systs_bin.extend(done)
            removed_systs_failed_bin.extend(failed)
        if len(removed_systs_bin) > 0:
            cb_bin.SetAutoMCStats(cb_full, 0.0)
        if verbosity > 1:
            print('>> [AddToMCStats] successfully removed %i shape uncertainties from bin %s' % (len(removed_systs_bin), b))
            print(removed_systs_bin)
            if len(removed_systs_failed_bin):
                print('>> [AddToMCStats] unable to remove %i shape uncertainties from bin %s' % (len(removed_systs_failed_bin), b))
                print(removed_systs_failed_bin)
        removed_systs.extend(removed_systs_bin)
        removed_systs_failed.extend(removed_systs_failed_bin)
    if len(removed_systs) > 0:
        cb_full.syst_name(removed_systs, False)
    if verbosity:
        print('>> [AddToMCStats] successfully removed total of %i shape uncertainties' % len(removed_systs))
        if len(removed_systs_failed):
            print('>> [AddToMCStats] unable to remove total of %i shape uncertainties' % len(removed_systs_failed))

def DropSmallSignals(cb_obj,cb_obj_filtered, frac=0.001, printOnly=False, verbosity=0):
    print('>> [DropSmallSignals] Going to check for signal processes contributing less than ', frac ,' of the total signal in their bin')
    for chn in cb_obj_filtered.channel_set():
        removed_procs_channel = 0
        cb_obj_chn = cb_obj_filtered.cp().channel([chn])
        for binid in cb_obj_chn.bin_set():
            cb_obj_chn_bin_sig = cb_obj_chn.cp().bin([binid]).signals()
            cb_obj_chn_bin = cb_obj_chn.cp().bin([binid])
            sigrate = cb_obj_chn_bin_sig.GetRate()
            for proc in cb_obj_chn_bin_sig.process_set():
                if cb_obj_chn_bin_sig.cp().process([proc]).GetRate() < frac*sigrate:
                    if verbosity > 1 or printOnly :
                        print('>> [DropSmallSignals] Process %s bin %s channel %s can be dropped: rate is '%(proc, binid, chn), cb_obj.cp().channel([chn]).bin([binid]).process([proc]).GetRate(), ' total signal rate is ', sigrate)
                    if not printOnly:
                        cb_obj.cp().channel([chn]).bin([binid]).process([proc]).ForEachProc(lambda x: DropProcAndSysts(cb_obj,x))
                    removed_procs_channel+=1
        if verbosity and not printOnly:
            print('>> [DropSmallSignals] removed %i signal processes contributing < %.4f of the total signal in a bin of channel %s' % (removed_procs_channel,frac,chn))
        if verbosity and printOnly:
            print('>> [DropSmallSignals] there are  %i signal processes contributing < %.4f% of the total signal in a bin of channel %s' % (removed_procs_channel,frac,chn))

def DropSmallSignalsWithBounds(cb_obj, cb_obj_filtered, frac=0.001, upperBound=0.01, upperBoundForSysts=0.01,printOnly=False, verbosity=0):
    print('>> [DropSmallSignalsWithBounds] Going to check for signal processes contributing less than ', frac ,' of the total signal in their bin. Upper bound for removal is ',upperBound)
    for chn in cb_obj_filtered.channel_set():
        removed_procs_channel = 0
        removed_procs_systs_channel = 0
        total_procs =0
        cb_obj_chn = cb_obj_filtered.cp().channel([chn])
        for binid in cb_obj_chn.bin_set():
            cb_obj_chn_bin_sig = cb_obj_chn.cp().bin([binid]).signals()
            cb_obj_chn_bin = cb_obj_chn.cp().bin([binid])
            sigrate = cb_obj_chn_bin_sig.GetRate()
            drop_list = []
            drop_list_systs = []
            for proc in cb_obj_chn_bin_sig.process_set():
                procrate = cb_obj_chn_bin_sig.cp().process([proc]).GetRate()
                total_procs+=1
                if procrate < frac*sigrate:
                    drop_list.append((proc,procrate))
            drop_list.sort(key=lambda x:x[1])
            rate_todrop_systs = sum(x[1] for x in drop_list)
            while rate_todrop_systs > upperBoundForSysts*sigrate:
                #print "Would drop ", rate_todrop," events; maximum bound is ", upperBound," equivalent to ", upperBound*sigrate, " events"
                drop_list.pop()
                rate_todrop_systs = sum(x[1] for x in drop_list)
            rate_todrop = sum(x[1] for x in drop_list)
            while rate_todrop > upperBound *sigrate:
                #print "Would drop ", rate_todrop," events; maximum bound is ", upperBound," equivalent to ", upperBound*sigrate, " events"
                drop_list_systs.append(drop_list[-1])
                drop_list.pop()
                rate_todrop = sum(x[1] for x in drop_list)
            for rate_tuple in drop_list:
                proc = rate_tuple[0]
                if verbosity > 1 :
                    print('>> [DropSmallSignalsWithBounds] Process %s bin %s channel %s can be dropped: rate is '%(proc, binid, chn), cb_obj.cp().channel([chn]).bin([binid]).process([proc]).GetRate(), ' total signal rate is ', sigrate)
                if not printOnly:
                    cb_obj.cp().channel([chn]).bin([binid]).process([proc]).ForEachProc(lambda x: DropProcAndSysts(cb_obj,x))
                removed_procs_channel+=1
            for rate_tuple in drop_list_systs:
                proc = rate_tuple[0]
                if verbosity > 1 :
                    print('>> [DropSmallSignalsWithBounds] Process %s bin %s channel %s systematics can be dropped: rate is '%(proc, binid, chn), cb_obj.cp().channel([chn]).bin([binid]).process([proc]).GetRate(), ' total signal rate is ', sigrate)
                if not printOnly:
                    cb_obj.cp().channel([chn]).bin([binid]).process([proc]).ForEachProc(lambda x: DropSystsShapeUnc(cb_obj,x))
                removed_procs_systs_channel+=1
        if verbosity and not printOnly:
            print('>> [DropSmallSignalsWithBounds] removed %i signal processes (out of %i)  contributing < %.4f of the total signal in a bin of channel %s.  Maximum fraction of signal yield that is removed is %.4f. Also removed systematics for %i signal processes contributin < %.4f of the total signal in a bin of channel %s. Maximum fraction of signal yield for which systematics are removed is %.4f' % (removed_procs_channel,total_procs,frac,chn,upperBound,removed_procs_systs_channel,frac,chn,upperBoundForSysts))
        if verbosity and printOnly:
            print('>> [DropSmallSignalsWithBounds] there are %i signal processes (out of %i)  contributing < %.4f of the total signal in a bin of channel %s.  Maximum fraction of signal yield that would be removed is %.4f. Also removed systematics for %i signal processes contributin < %.4f of the total signal in a bin of channel %s. Maximum fraction of signal yield for which systematics would be removed is %.4f' % (removed_procs_channel,total_procs,frac,chn,upperBound,removed_procs_systs_channel,frac,chn,upperBoundForSysts))

def DropSmallSignalsWithBoundsFast(cb_obj, cb_obj_filtered, frac=0.001, upperBound=0.01, upperBoundForSysts=0.01,printOnly=False, verbosity=0):
    print('>> [DropSmallSignalsWithBoundsFast] Going to check for signal processes contributing less than ', frac ,' of the total signal in their bin. Upper bound for removal is ',upperBound)
    for chn in cb_obj_filtered.channel_set():
        removed_procs_channel = 0
        removed_procs_systs_channel = 0
        total_procs =0
        cb_obj_chn = cb_obj_filtered.cp().channel([chn])
        for binid in cb_obj_chn.bin_set():
            cb_obj_chn_bin_sig = cb_obj_chn.cp().bin([binid]).signals()
            cb_obj_chn_bin = cb_obj_chn.cp().bin([binid])
            sigrate = cb_obj_chn_bin_sig.GetRate()
            drop_list = []
            drop_list_systs = []
            for proc in cb_obj_chn_bin_sig.process_set():
                procrate = cb_obj_chn_bin_sig.cp().process([proc]).GetRate()
                total_procs+=1
                if procrate < frac*sigrate:
                    drop_list.append((proc,procrate))
            drop_list.sort(key=lambda x:x[1])
            rate_todrop_systs = sum(x[1] for x in drop_list)
            while rate_todrop_systs > upperBoundForSysts*sigrate:
                #print "Would drop ", rate_todrop," events; maximum bound is ", upperBound," equivalent to ", upperBound*sigrate, " events"
                drop_list.pop()
                rate_todrop_systs = sum(x[1] for x in drop_list)
            rate_todrop = sum(x[1] for x in drop_list)
            while rate_todrop > upperBound *sigrate:
                #print "Would drop ", rate_todrop," events; maximum bound is ", upperBound," equivalent to ", upperBound*sigrate, " events"
                drop_list_systs.append(drop_list[-1])
                drop_list.pop()
                rate_todrop = sum(x[1] for x in drop_list)
            for rate_tuple in drop_list:
                proc = rate_tuple[0]
                if verbosity > 1 :
                    print('>> [DropSmallSignalsWithBoundsFast] Process %s bin %s channel %s can be dropped: rate is '%(proc, binid, chn), cb_obj.cp().channel([chn]).bin([binid]).process([proc]).GetRate(), ' total signal rate is ', sigrate)
                #if not printOnly:
                #        cb_obj.cp().channel([chn]).bin([binid]).process([proc]).ForEachProc(lambda x: DropProcAndSysts(cb_obj,x))
                removed_procs_channel+=1
            if not printOnly:
                drop_proc_list=[ rate_tuple[0] for rate_tuple in drop_list]
                DropProcAndSystsList(cb_obj,cb_obj.cp().channel([chn]).bin([binid]), drop_proc_list)

            for rate_tuple in drop_list_systs:
                proc = rate_tuple[0]
                if verbosity > 1 :
                    print('>> [DropSmallSignalsWithBoundsFast] Process %s bin %s channel %s systematics can be dropped: rate is '%(proc, binid, chn), cb_obj.cp().channel([chn]).bin([binid]).process([proc]).GetRate(), ' total signal rate is ', sigrate)
                #if not printOnly:
                #        cb_obj.cp().channel([chn]).bin([binid]).process([proc]).ForEachProc(lambda x: DropSysts(cb_obj,x))
                removed_procs_systs_channel+=1

            if not printOnly:
                drop_proc_list=[rate_tuple[0] for rate_tuple in drop_list_systs]
                DropSystsList(cb_obj,cb_obj.cp().channel([chn]).bin([binid]), drop_proc_list)

        if verbosity and not printOnly:
            print('>> [DropSmallSignalsWithBoundsFast] removed %i signal processes (out of %i)  contributing < %.4f of the total signal in a bin of channel %s.  Maximum fraction of signal yield that is removed is %.4f. Also removed systematics for %i signal processes contributin < %.4f of the total signal in a bin of channel %s. Maximum fraction of signal yield for which systematics are removed is %.4f' % (removed_procs_channel,total_procs,frac,chn,upperBound,removed_procs_systs_channel,frac,chn,upperBoundForSysts))
        if verbosity and printOnly:
            print('>> [DropSmallSignalsWithBoundsFast] there are %i signal processes (out of %i)  contributing < %.4f of the total signal in a bin of channel %s.  Maximum fraction of signal yield that would be removed is %.4f. Also removed systematics for %i signal processes contributin < %.4f of the total signal in a bin of channel %s. Maximum fraction of signal yield for which systematics would be removed is %.4f' % (removed_procs_channel,total_procs,frac,chn,upperBound,removed_procs_systs_channel,frac,chn,upperBoundForSysts))



def DropProcAndSysts(cb_obj, proc):
    cb_obj.FilterSysts(lambda sys: MatchingSystAndProc(proc,sys))
    cb_obj.FilterProcs(lambda x: MatchingSystAndProc(proc,x))
    return False

def DropSysts(cb_obj, proc):
    cb_obj.FilterSysts(lambda sys: MatchingSystAndProc(proc,sys))
    return False

def DropSystsOnly(cb_obj, proc):
    cb_obj.FilterSysts(lambda sys: MatchingSystAndProcSystOnly(proc,sys))
    return False

def PrintNBins(proc,procname,dictlist,binid):
    if proc.process() == procname:
        if proc.shape().GetNbinsX()<3:
            dictlist.append(binid)



def MatchingSystAndProc(p,s):
    return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal())
           and (p.analysis()==s.analysis()) and  (p.era()==s.era())
           and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))

def MatchingSystAndProcSystOnly(p,s):
    return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal())
           and (p.analysis()==s.analysis()) and  (p.era()==s.era())
           and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()) and not any(x in s.name() for x in protected_list))


################## try to act on a list of objects
class SoftProcess:
    def __init__(self,p):
        ''' A soft clone of Process object that can be passed to MatchingSystAndProc'''
        self._bin=p.bin()
        self._process=p.process()
        self._signal=p.signal()
        self._analysis=p.analysis()
        self._era=p.era()
        self._channel=p.channel()
        self._bin_id=p.bin_id()
        self._mass=p.mass()
    def bin(self):
        return self._bin
    def process(self):
        return self._process
    def signal(self):
        return self._signal
    def analysis(self):
        return self._analysis
    def era(self):
        return self._era
    def channel(self):
        return self._channel
    def bin_id(self):
        return self._bin_id
    def mass(self):
        return self._mass

def MatchingSystAndProcListSystOnly(procs,s):
    for p in procs:
        if MatchingSystAndProcSystOnly(p,s):
            return True
    return False

def MatchingSystAndProcList(procs,s):
    for p in procs:
        if MatchingSystAndProc(p,s):
            return True
    return False


def DropProcAndSystsList(cb_obj,cb_filtered, procnames):
    #print "[DEBUG]","[DropProcAndSystsList]", procnames ,"SoftCopy"
    procs = []
    cb_filtered.cp().process(procnames).ForEachProc(lambda x: procs.append(SoftProcess(x))) ## make a soft copy

    #print "[DEBUG]","[DropProcAndSystsList]", procs ,"Systs"
    cb_obj.FilterSysts(lambda sys: MatchingSystAndProcListSystOnly(procs,sys))
    #print "[DEBUG]","[DropProcAndSystsList]","now Procs"
    cb_obj.FilterProcs(lambda x: MatchingSystAndProcList(procs,x))
    #print "[DEBUG]","[DropProcAndSystsList]","return"
    return False

def DropSystsList(cb_obj,cb_filtered, procnames):
    #print "[DEBUG]","[DropSystsList]", procnames, "SoftCopy"

    procs = []
    cb_filtered.cp().process(procnames).ForEachProc(lambda x: procs.append(SoftProcess(x))) ## make a soft copy

    cb_obj.FilterSysts(lambda sys: MatchingSystAndProcListSystOnly(procs,sys))
    return False
#######################################################33

def UpdateUncert(x, val_d, val_u=None):
    if x.type() != 'lnN':
        'Not a lnN:'
        x.PrintHeader()
        print(x)
        return
    if val_u is None:
        x.set_asymm(False)
        x.set_value_u(val_d)
    else:
        x.set_asymm(True)
        x.set_value_u(val_u)
        x.set_value_d(val_d)

def ScaleUncert(x, k):
    if x.type() != 'lnN':
        x.set_scale(x.scale()*k)
    else:
        x.set_value_u((x.value_u()-1.)*k+1)
        if x.asymm():
            x.set_value_d((x.value_d()-1)*k+1.)

def PruneAsymm(x,thr=0.01,verbose=False):
    if x.type() != 'lnN': return
    if not x.asymm(): return
    if abs(x.value_u()*x.value_d()-1)>thr: return

    if verbose: print("[INFO] Asymm. Pruning",x.name(),x.analysis(),x.channel(),x.value_d(),"/",x.value_u(),"->", x.value_u())
    UpdateUncert(x,x.value_u()) ## this will change it to a symm lnN


def DoSwap(sys):
    print(sys)
    sys.SwapUpAndDown()

def CheckDoubleCounting(cb):
    ''' Check if something went wrong with renaming and we have to nuisances assigned to the same process'''
    systs=[]
    cb.ForEachSyst(lambda x: systs.append(x) )
    d={}
    for s in systs:
        p = (s.name(),s.process(),s.bin(),s.signal(),s.analysis(),s.era(),s.channel(),s.bin_id(),s.mass())
        if p not in d: d[p]=0
        d[p] += 1

    ok=True
    for key in d :
        if d[key] >1 :
            print('WARNING' ,key, d[key])
            ok=False
    return ok


def ReplaceProcShape(cb, proc_rep, procname):
    proc_target=[]
    cb.cp().bin([proc_rep.bin()]).process([procname]).channel([proc_rep.channel()]).ForEachProc(lambda x: proc_target.append(x))
    if len(proc_target)==1:
        new_hist=proc_target[0].ShapeAsTH1F()
        new_hist.Scale(proc_rep.rate())
        proc_rep.set_shape(new_hist,False)
    else:
        print('SOMETHING WENT WRONG')


def ReplaceSystShape(cb, syst_rep, procname):
    target_syst=[]
    rep_nominal=[]
    cb.cp().syst_name([syst_rep.name()]).bin([syst_rep.bin()]).process([procname]).channel([syst_rep.channel()]).ForEachSyst(lambda x: target_syst.append(x))
    cb.cp().bin([syst_rep.bin()]).channel([syst_rep.channel()]).ForEachProc(lambda x: rep_nominal.append(x) if MatchingSystAndProc(syst_rep,x) else None)
    if len(target_syst)==1:
        hist_u_target = target_syst[0].ShapeUAsTH1F()
        hist_d_target = target_syst[0].ShapeDAsTH1F()
    else:
        print('SOMETHING WENT WRONG')
    if len(rep_nominal)==1:
        hist_u_target.Scale(rep_nominal[0].rate()*syst_rep.value_u())
        hist_d_target.Scale(rep_nominal[0].rate()*syst_rep.value_d())
        syst_rep.set_shapes(hist_u_target,hist_d_target,rep_nominal[0])
    else:
        print('SOMETHING WENT WRONG')

def flatline (x,a):
    return a

def chisqr(obs,exp,error):
    chisqr = 0
    for i in range(len(obs)):
        chisqr += ((obs[i]-exp[i])**2)/(error[i]**2)
    return chisqr

def getVar(systematic,nom,threshold={}):
    if systematic.type() in 'shape' and 'scale_j' not in systematic.name() and 'scale_t' not in systematic.name() and 'res_j' not in systematic.name():
        print("working on systematic ",systematic.name())
        hist_u = systematic.ShapeUAsTH1F()
        hist_u.Scale(nom.Integral()*systematic.value_u())
        hist_d = systematic.ShapeDAsTH1F()
        hist_d.Scale(nom.Integral()*systematic.value_d())
        ratiosup = []
        errors = []
        ratiosdown = []
        xvals =[]
        for i in range(nom.GetNbinsX()):
            if (nom.GetBinContent(i+1) > 0 ):
                ratiosup.append(hist_u.GetBinContent(i+1)/nom.GetBinContent(i+1))
                ratiosdown.append(hist_d.GetBinContent(i+1)/nom.GetBinContent(i+1))
                errors.append(0.05*nom.GetBinError(i+1)/nom.GetBinContent(i+1))
                xvals.append(i+1)
            else:
                print("nominal bin content is 0 or negative, up.down are ", hist_u.GetBinContent(i+1), " , ",hist_d.GetBinContent(i+1))
        if(not len(xvals)-1 < 1):
            poptup, pcovup = curve_fit(flatline,xvals,ratiosup,sigma=errors)
            poptdown, pcovdown = curve_fit(flatline,xvals,ratiosdown,sigma=errors)
            fitvalsup = [poptup[0] for val in xvals]
            fitvalsdown = [poptdown[0] for val in xvals]
            chiup = chisqr(ratiosup,fitvalsup,errors)
            chidown = chisqr(ratiosdown,fitvalsdown,errors)
            print(1-stats.chi2.cdf(chiup,len(xvals)-1))
            print(1-stats.chi2.cdf(chidown,len(xvals)-1))
            print("chiup ",chiup," chidown ",chidown)
            threshold2use=0.9
            for sysname in threshold.keys():
                if sysname in systematic.name():
                    threshold2use=threshold[sysname]
                    print("Use different threshold for ",systematic.name(),": ",threshold2use)
                    break
            if threshold2use>1:
                print("skip ", systematic.name())
            elif ((1-stats.chi2.cdf(chiup,len(xvals)-1)<threshold2use) or (1-stats.chi2.cdf(chidown,len(xvals)-1)<threshold2use)):
                print("this is a genuine shape uncertainty")
            else:
                print("No shape variation, convert to lognormal")
                systematic.set_type('lnN')
                return systematic.name()
                
        else:
            print("Single bin, convert shape systematic to lognormal")
            systematic.set_type('lnN')
            return systematic.name()

def CheckUncertaintyVariation(cb, thresholds={}):
    for chn in cb.channel_set():
        cb_obj_chn = cb.cp().channel([chn])
        print("CHECKING CHANNEL" ,chn)
        if chn in thresholds.keys():
            threshold=thresholds[chn]
        else:
            threshold={}
        for binid in cb_obj_chn.bin_set():
            print("CHECKING BIN" ,binid)
            for proc in cb_obj_chn.cp().bin([binid]).process_set():
                if(cb_obj_chn.cp().bin([binid]).process([proc]).GetRate()==0):continue
                print("CHECKING PROCESS" ,proc)
                systs_converted=[]
                systs_all=[]
                nominal_histos=[]
                cb_obj_chn.cp().bin([binid]).process([proc]).ForEachProc(lambda x: nominal_histos.append(x.ShapeAsTH1F()))
                nominal_histo = nominal_histos[0]
                nominal_histo.Scale(cb_obj_chn.cp().bin([binid]).process([proc]).GetRate())
                cb_obj_chn.cp().bin([binid]).process([proc]).ForEachSyst(lambda x: systs_all.append(x.type()))
                cb_obj_chn.cp().bin([binid]).process([proc]).ForEachSyst(lambda x: systs_converted.append(getVar(x,nominal_histo, threshold)))
                shape_all_systs = [x for x in systs_all if 'shape' in x]
                converted_all_systs = [x for x in systs_converted if x is not None]
                print("SYSTS CONVERTED ", len(converted_all_systs))
                print("TOTAL SYSTS ", len(shape_all_systs))
                #procrate = cb_obj_chn_bin_sig.cp().process([proc]).GetRate()
                #total_procs+=1
                #if procrate < frac*sigrate:
                #   drop_list.append((proc,procrate))


def CheckUncertaintygroupVariation(cb, groups):

    def setlnN(systematic,name):
         if name in systematic.name():
            systematic.set_type('lnN')

    def addunc(systematic,nom):
         if systematic.type() in 'shape':
             hist_u = systematic.ShapeUAsTH1F()
             hist_u.Scale(nom.Integral()*systematic.value_u())
             hist_d = systematic.ShapeDAsTH1F()
             hist_d.Scale(nom.Integral()*systematic.value_d())
             rup = []
             rdn = []
             for i in range(nom.GetNbinsX()):
                 print(nom.GetBinContent(i+1), hist_u.GetBinContent(i+1), hist_d.GetBinContent(i+1))
                 if (nom.GetBinContent(i+1) > 0 ):
                     rup.append(hist_u.GetBinContent(i+1)/nom.GetBinContent(i+1))
                     rdn.append(hist_d.GetBinContent(i+1)/nom.GetBinContent(i+1))
                 else:
                     rup.append(1)
                     rdn.append(1)
             if(len(ratiosup)==0):
                 for i in range(len(rup)):
                     ratiosup.append(rup[i])
                     ratiosdown.append(rdn[i])
             elif(len(ratiosup)!=len(rup)):
                 print("len(ratiosup)!=len(rup)")
                 exit()
             else:
                 for i in range(len(ratiosup)):
                     ratiosup[i]*=rup[i]
                     ratiosdown[i]*=rdn[i]
         else: 
             print("Not shape nuissance ")

    for chn in cb.channel_set():
        cb_obj_chn = cb.cp().channel([chn])
        print("CHECKING CHANNEL" ,chn)
        if chn not in groups.keys(): continue
        group=groups[chn]
        for binid in cb_obj_chn.bin_set():
            print("CHECKING BIN" ,binid)
            for proc in cb_obj_chn.cp().bin([binid]).process_set():
                if(cb_obj_chn.cp().bin([binid]).process([proc]).GetRate()==0):continue
                print("CHECKING PROCESS" ,proc)
                systs_converted=[]
                systs_all=[]
                nominal_histos=[]
                cb_obj_chn.cp().bin([binid]).process([proc]).ForEachProc(lambda x: nominal_histos.append(x.ShapeAsTH1F()))
                nominal_histo = nominal_histos[0]
                nominal_histo.Scale(cb_obj_chn.cp().bin([binid]).process([proc]).GetRate())
                for isyst in group[0]:
                    print("working on systematic ",isyst, " threshold is ", group[1])
                    ratiosup=[]
                    ratiosdown=[]
                    process = GetProcess(cb_obj_chn, binid, proc)
                    cb_obj_chn.cp().bin([binid]).process([proc]).ForEachSyst(lambda x: addunc(x,nominal_histo) if (isyst in x.name() and MatchingSystAndProc(process,x)) else None )
                    errors = []
                    xvals =[]
                    if len(ratiosup)==0:
                        continue
                    for i in range(nominal_histo.GetNbinsX()):
                        if (nominal_histo.GetBinContent(i+1) > 0 ):
                            errors.append(0.05*nominal_histo.GetBinError(i+1)/nominal_histo.GetBinContent(i+1))
                            xvals.append(i+1)
                        else:
                            errors.append(0)
                            xvals.append(i+1)
                    if(not len(xvals)-1 < 1):
                        poptup, pcovup = curve_fit(flatline,xvals,ratiosup,sigma=errors)
                        poptdown, pcovdown = curve_fit(flatline,xvals,ratiosdown,sigma=errors)
                        fitvalsup = [poptup[0] for val in xvals]
                        fitvalsdown = [poptdown[0] for val in xvals]
                        chiup = chisqr(ratiosup,fitvalsup,errors)
                        chidown = chisqr(ratiosdown,fitvalsdown,errors)
                        if ((1-stats.chi2.cdf(chiup,len(xvals)-1)<group[1]) or (1-stats.chi2.cdf(chidown,len(xvals)-1)<group[1])):
                            print("this is a genuine shape uncertainty")
                        else:
                            print("No shape variation, convert to lognormal")
                            systs_converted.append(isyst)
                            cb_obj_chn.cp().bin([binid]).process([proc]).ForEachSyst(lambda x: setlnN(x,isyst))
                    else:
                        print("Single bin, convert shape systematic to lognormal")
                        systs_converted.append(isyst)
                        cb_obj_chn.cp().bin([binid]).process([proc]).ForEachSyst(lambda x: setlnN(x,isyst))
                converted_all_systs = [x for x in systs_converted if x is not None]
                print("SYSTS CONVERTED ", converted_all_systs)




