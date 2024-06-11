import ROOT
import sys, os
from subprocess import call

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

if not hasattr(ROOT, "RooModZPdf"):
    # hmm pdfs not in this version of combine, load them ourself
    if not os.path.isfile('lib/HMuMuRooPdfs_cc.so'):
        ROOT.gROOT.ProcessLine('.L lib/HMuMuRooPdfs.cc++')
    ROOT.gSystem.Load('lib/HMuMuRooPdfs_cc.so')

dcname=sys.argv[1]
fname=sys.argv[2]

item='pdf_index_ggh'
idx=2

fin = ROOT.TFile.Open(fname,"UPDATE")
for key in fin.GetListOfKeys():
    w=fin.Get(key.GetName())
    if isinstance(w,ROOT.RooWorkspace):
        cat=w.cat(item)
        if cat != None:
            cat.setIndex(idx)
            print( "> Updating",cat.GetName(),"in",w.GetName(),"to value",idx)
            fin.cd()
            fin.WriteTObject(w,w.GetName(), 'WriteDelete')
fin.Close()

## Print
fin=ROOT.TFile.Open(fname)
for key in fin.GetListOfKeys():
    w=fin.Get(key.GetName())
    if isinstance(w,ROOT.RooWorkspace):
        cat=w.cat(item)
        if cat != None:
            print( "w:",w.GetName(),":",)
            cat.Print()
fin.Close()

cmd="cat "+ dcname + "| grep -v '^" + item +"' > "+ dcname +"_2" 
st=call(cmd,shell=True)
if st !=0 : raise RuntimeError("Grep didn't work")
cmd="mv -v " + dcname +"_2 " + dcname
st=call(cmd,shell=True)
if st !=0 : raise RuntimeError("Mv didn't work")


print( ">Done")

