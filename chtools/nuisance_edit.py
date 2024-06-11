# import CombineHarvester.CombineTools.ch as ch
# import ROOT
from __future__ import absolute_import
from __future__ import print_function
import os
import re
import pprint


def ReadNuisanceEdit(cards):
    verbose=False
    # bin, name->name
    # for freeze alternatively we can use: https://github.com/cms-analysis/CombineHarvester/compare/master...amarini:nuisance_edit_freeze?expand=1
    rename = [] #b, name, name2
    rename2= [] #b,p,name,name2
    freeze = [] # bin, name
    add = [] # proc, bin, name, value
    drop = []
    for txt in cards:
        allbins=[]
        allprocs=[]
        f = open(txt,"r")
        for l in f:
            l = l.split('#')[0]
            if l.startswith('bin') and len(allbins)==0:
                allbins=l.split()[1:]
            if l.startswith('process') and len(allbins)==0:
                allprocs=list(set(l.split()[1:]))
            #if l.startswith('nuisance edit rename'):
            if re.match('nuisance +edit +rename',l):
                parts=l.split()
                if len(parts) <= 5:
                    if '|' in parts[3] or '|' in parts[4]:
                        print("LINE is",l)
                        raise ValueError("Unimplemented")
                    for b in allbins:
                        rename.append( (b,parts[3],parts[4]) )
                else:
                    pp = parts[3]
                    bb = parts[4]
                    n1 = parts[5]
                    n2 = parts[6]
                    mybins=[bb]
                    myprocs=[pp]
                    if pp=='*': myprocs=allprocs[:]
                    elif '*' in pp: raise ValueError("Unimplemented")
                    if bb == '*': mybins=allbins[:]
                    elif '*' in bb:  #### THIS IS THE TRUE REGEX MATCHING
                        mybins=[]
                        for b in allbins:
                            if re.match(bb, b):
                                mybins.append(b)
                        #if verbose:
                        if True:
                            print(" ---- DEBUG BINS RENAME")
                            print("REGEX", bb)
                            print("ALLPROCS",allbins)
                            print("MYPROCS",mybins)
                            print(" --- ")
                        #raise ValueError("Unimplemented")# copy logic from add
                    if '|' in pp and '*' not in pp: # (|||)
                        myprocs=[]
                        if len(pp.split('(')) > 2:
                            print("LINE is",l)
                            raise ValueError("Unimplemented")
                        p0 = pp.split('(')[0]
                        p2 = pp.split(')')[1]
                        for p1 in pp.split('(')[1].split(')')[0].split('|'):
                            myprocs.append(p0+p1+p1)

                    if '|' in bb and '*' not in bb: # (|||)
                        mybins=[]
                        if len(bb.split('(')) > 2:
                            print("LINE is",l)
                            raise ValueError("Unimplemented")
                        p0 = bb.split('(')[0]
                        p2 = bb.split(')')[1]
                        for p1 in bb.split('(')[1].split(')')[0].split('|'):
                            mybins.append(p0+p1+p1)

                    for b in mybins:
                        for p in myprocs:
                            rename2.append((b,p,n1,n2) )

            #if l.startswith('nuisance edit freeze'):
            if re.match('nuisance +edit +freeze',l):
                for b in allbins:
                    freeze.append( (b,l.split()[3]) )

            #if l.startswith('nuisance edit drop'):
            if re.match('nuisance +edit +drop',l):
                parts=l.split() ## PROC BIN NAME
                drop . append( (parts[3],parts[4],parts[5] )) ## bin/proc/name

            #if l.startswith('nuisance edit add'):
            if re.match('nuisance +edit +add',l):
                parts=l.split() ## PROC CHN NAME lnN val
                if parts[6] !='lnN': raise ValueError("Only lnN nuisance adds implemented")
                myprocs=[]
                mybins=[]
                # find matching bins
                if parts[4] == '*':
                    mybins=allbins[:]
                elif '*' in parts[4]:
                    if verbose: print("->CHECK CORRECTNESS OF REGEX IMPL")
                    for b in allbins:
                        if re.match(parts[4], b):
                            mybins.append(b)
                    if verbose:
                        print(" ---- DEBUG BINS")
                        print("REGEX", parts[4])
                        print("ALLPROCS",allbins)
                        print("MYPROCS",mybins)
                        print(" --- ")
                else: mybins=[ parts[4] ]

                # find matching procs
                if parts[5] == '*':
                    myprocs=allprocs[:]
                elif '*' in parts[5]:
                    #raise ValueError("Unimplemented")
                    if verbose: print("->CHECK CORRECTNESS OF REGEX IMPL")
                    for p in allprocs:
                        if re.match(parts[5], p):
                            myprocs.append(p)
                    if verbose:
                        print(" ---- DEBUG PROCS")
                        print("REGEX", parts[5])
                        print("ALLPROCS",allprocs)
                        print("MYPROCS",myprocs)
                        print(" --- ")
                else: myprocs=[ parts[5] ]

                for p in myprocs:
                    for b in mybins:
                        add.append( (p,b,parts[5], float(parts[7])) )

        f.close()
    R={
        "rename": rename,
        "rename2": rename2,
        "freeze": freeze,
        "add": add,
        "drop":drop,
        }
    return R

def AbortOnNuisanceEdit(cards):
    for txt in cards:
        if "vhbb_stxs" in txt:
            continue #FIXME VHbb card has nuissance edits
        f = open(txt,"r")
        for l in f:
            l = l.split('#')[0]
            if l.startswith('nuisance edit'):
                raise RuntimeError("Card: "+txt+" has a nuisance edit. Please check it ")
        f.close()
