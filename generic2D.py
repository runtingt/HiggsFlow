#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path

import sys
sys.setrecursionlimit(10000)

remin=False

def read(scan, param_x, param_y, file):
    global remin
    # print files
    goodfiles = [f for f in [file] if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    if remin:
        mymin=limit.GetMinimum("deltaNLL")
        print(">> Remin deltaNLL=",mymin)

    if (param_x=="M"):
      print("M eps model")
      graph = plot.TGraph2DFromTree(limit, param_x, param_y, '2*(deltaNLL-%f)'%mymin, 'quantileExpected > -0.5 && (deltaNLL-%f) > 0 && 2.0*(deltaNLL-%f)<10.0'%(mymin,mymin))
    else:
      graph = plot.TGraph2DFromTree(limit, param_x, param_y, '2*(deltaNLL-%f)'%mymin, 'quantileExpected > -0.5 && (deltaNLL-%f) > 0 && 2.0*(deltaNLL-%f)<20.0'%(mymin,mymin))
    best = plot.TGraphFromTree(limit, param_x, param_y, 'deltaNLL == 0')
    plot.RemoveGraphXDuplicates(best)
    assert(best.GetN() == 1)
    graph.SetName(scan)
    best.SetName(scan+'_best')
    # graph.Print()
    return (graph, best)

def fillTH2(hist2d, graph):

    param = 0
    ordpoly = 7
    fstring = "("
    for o1 in range(ordpoly+1):
      if (o1==0):
        fstring += "["+str(param)+"]"
        param+=1
        continue
      else:
        fstring += "+["+str(param)+"]*pow(x,"+str(o1)+")"
        param+=1
        fstring += "+["+str(param)+"]*pow(y,"+str(o1)+")"
        param+=1

        o2=1
        while o2<(o1+1):
          fstring += "+["+str(param)+"]*pow(x,"+str(o1)+")*pow(y,"+str(o2)+")"
          param+=1
          if (not o1==o2):
            fstring += "+["+str(param)+"]*pow(x,"+str(o2)+")*pow(y,"+str(o1)+")"
            param+=1
          o2+=1

    fstring+=")"
    print(fstring)

    f2D = ROOT.TF2("f2D",fstring, \
                  hist2d.GetXaxis().GetBinCenter(1),hist2d.GetXaxis().GetBinCenter(hist2d.GetNbinsX()),
                  hist2d.GetYaxis().GetBinCenter(1),hist2d.GetYaxis().GetBinCenter(hist2d.GetNbinsY()))
    graph.Fit("f2D")

    for x in range(1, hist2d.GetNbinsX()+1):
        for y in range(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            #val = graph.Interpolate(xc, yc)
            val = f2D.Eval(xc, yc)
            hist2d.SetBinContent(x, y, val)

def fixZeros(hist2d):
    for x in range(1, hist2d.GetNbinsX()+1):
        for y in range(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            if hist2d.GetBinContent(x, y) == 0:
                # print 'Bin at (%f,%f) is zero!' % (xc, yc)
                hist2d.SetBinContent(x, y, 1000)

def makeHist(name, bins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(bins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(bins) - 1.)) - 1E-5
    hist = ROOT.TH2F(name, '', bins, graph2d.GetXmin()-binw_x, graph2d.GetXmax()+binw_x, bins, graph2d.GetYmin()-binw_y, graph2d.GetYmax()+binw_y)
    return hist

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#plot.ModTDRStyle(l=0.13, b=0.10, r=0.19)
plot.ModTDRStyle(l=0.13, b=0.10)
ROOT.gStyle.SetNdivisions(506, "Y")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
plot.SetBirdPalette()

# ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetNdivisions(506, "Y")
ROOT.gStyle.SetMarkerSize(1.0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', help='output name')
parser.add_argument('--file', '-f', help='named input scans')
parser.add_argument('--multi', type=int, default=1, help='scale number of bins')
parser.add_argument('--thin', type=int, default=1, help='thin graph points')
parser.add_argument('--order', default='b,tau,Z,gam,W,comb')
parser.add_argument('--x-range', default='-5,5')
parser.add_argument('--y-range', default='-5,5')
parser.add_argument('--x-axis', default='#kappa_{V}')
parser.add_argument('--y-axis', default='#kappa_{F}')
parser.add_argument('--axis-hist', default=None)
parser.add_argument('--layout', type=int, default=1)
parser.add_argument('--remin', action='store_true', default=False)
parser.add_argument('--sm-point', default='1,1')
parser.add_argument('--translate', help='json file with POI name translation')
parser.add_argument('--title-right', default='', help='title text')
parser.add_argument('--suppl', action='store_true', default=False)



args = parser.parse_args()

if args.remin: remin=True

if args.translate is not None:
    with open(args.translate) as jsonfile:
        name_translate = json.load(jsonfile)

infile = args.file

order = args.order.split(',')

graph_test = read('test', args.x_axis, args.y_axis, infile)[0]


if ("eps" in args.output):
  axis = ROOT.TH2F('hist2d', '', 100, 200.0, 260.0, 100, -0.149, 0.149)
elif args.axis_hist is not None:
  hargs = args.axis_hist.split(',')
  axis = ROOT.TH2F('hist2d', '', int(hargs[0]), float(hargs[1]), float(hargs[2]), int(hargs[3]), float(hargs[4]), float(hargs[5]))
else:
  axis = makeHist('hist2d', 40 * args.multi, graph_test)

# axis = None
x_axis = args.x_axis
if x_axis in name_translate:
    x_axis = name_translate[x_axis]
y_axis = args.y_axis
if y_axis in name_translate:
    y_axis = name_translate[y_axis]
if (x_axis=="M"):
  axis.GetXaxis().SetTitle(x_axis+" [GeV]")
else:
  axis.GetXaxis().SetTitle(x_axis)
axis.GetYaxis().SetTitle(y_axis)


canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].SetGridx(False)
pads[0].SetGridy(False)
pads[0].Draw()
axis.Draw()
if args.x_range is not None:
    xranges = args.x_range.split(',')
    axis.GetXaxis().SetLimits(float(xranges[0]), float(xranges[1]))
    axis.GetXaxis().SetRangeUser(float(xranges[0]), float(xranges[1]))
if args.y_range is not None:
    yranges = args.y_range.split(',')
    axis.GetYaxis().SetLimits(float(yranges[0]), float(yranges[1]))
    axis.GetYaxis().SetRangeUser(float(yranges[0]), float(yranges[1]))

if args.layout == 1:
    legend = ROOT.TLegend(0.14, 0.53, 0.35, 0.74, '', 'NBNDC')
if args.layout == 2:
    legend = ROOT.TLegend(0.15, 0.11, 0.46, 0.27, '', 'NBNDC')
    legend.SetNColumns(2)
if args.layout == 3:
    legend = ROOT.TLegend(0.14, 0.53, 0.35, 0.74, '', 'NBNDC')


graphs = {}
bestfits = {}
hists = {}
conts68 = {}
conts95 = {}

outfile = ROOT.TFile(args.output+'.root', 'RECREATE')
order = ['default']
for scan in order:
    graphs[scan], bestfits[scan] = read(scan, args.x_axis, args.y_axis, infile)
    outfile.WriteTObject(graphs[scan], scan+'_graph')
    outfile.WriteTObject(bestfits[scan])
    hists[scan] = makeHist(scan+'_hist', 40 * args.multi, graph_test)
    fillTH2(hists[scan], graphs[scan])
    outfile.WriteTObject(hists[scan], hists[scan].GetName()+'_input')
    fixZeros(hists[scan])
    hists[scan].GetZaxis().SetTitle('-2 #Delta ln #Lambda(%s,%s)' %( x_axis, y_axis))
    # hists[scan].GetZaxis().SetTitleOffset(0)
    #hists[scan].Draw('COLZSAME')
    hists[scan].SetMinimum(0)
    hists[scan].SetMaximum(10)
    outfile.WriteTObject(hists[scan], hists[scan].GetName()+'_processed')
    conts68[scan] = plot.contourFromTH2(hists[scan], ROOT.Math.chisquared_quantile_c(1-0.683, 2))
    conts95[scan] = plot.contourFromTH2(hists[scan], ROOT.Math.chisquared_quantile_c(1-0.9545, 2))
    for i, c in enumerate(conts68[scan]):
        if args.thin > 1:
            newgr = ROOT.TGraph(c.GetN() / args.thin)
            needLast = True
            for a,p in enumerate(range(0, c.GetN(), args.thin)):
                if p == c.GetN()-1: needLast = False
                newgr.SetPoint(a, c.GetX()[p], c.GetY()[p])
            if needLast: newgr.SetPoint(newgr.GetN(), c.GetX()[c.GetN()-1], c.GetY()[c.GetN()-1])
            conts68[scan][i] = newgr
            c = conts68[scan][i]
        c.SetFillColor(ROOT.TColor.GetColor(200, 200, 200))
        c.SetLineColor(ROOT.TColor.GetColor(0, 0, 0))
        c.SetLineWidth(3)
        pads[0].cd()
        #c.Draw('L SAME')
        c.Draw('LF SAME')
        outfile.WriteTObject(c, 'graph68_%s_%i' % (scan, i))
    if scan in conts95:
        for i, c in enumerate(conts95[scan]):
            c.SetLineWidth(3)
            c.SetLineStyle(7)
            pads[0].cd()
            outfile.WriteTObject(c, 'graph95_%s_%i' % (scan, i))
    try:
      legend.AddEntry(conts68[scan][0], 'Scan', 'F')
    except IndexError:
      print(f"Warning: no 68% CL contour found to add to legend for scan {scan}")
for scan in order:
    for i, c in enumerate(conts68[scan]):
        c.Draw('L SAME')
    if scan in conts95:
        for i, c in enumerate(conts95[scan]):
            c.Draw('L SAME')
            #c.Draw('C SAME')

for scan in order:
    bestfits[scan].SetMarkerStyle(34)
    bestfits[scan].SetMarkerSize(1.2)
    if scan == 'comb': bestfits[scan].SetMarkerSize(1.5)
    bestfits[scan].Draw('PSAME')

sm_point = ROOT.TGraph()
sm_point.SetPoint(0, *[float(x) for x in args.sm_point.split(',')])
# sm_point.SetMarkerColor(ROOT.TColor.GetColor(249, 71, 1))
#sm_point.SetMarkerColor(ROOT.kRed)
#sm_point.SetMarkerStyle(33)
#sm_point.SetMarkerSize(2)
sm_point.SetMarkerColor(ROOT.kBlack)
sm_point.SetMarkerStyle(29)
sm_point.SetMarkerSize(2)
sm_point.Draw('PSAME')
# sm_point.SetFillColor(ROOT.TColor.GetColor(248, 255, 1))

# legend.Draw()

if (args.layout==1):
  legend2 = ROOT.TLegend(0.2, 0.13, 0.9, 0.19, '', 'NBNDC')
  legend2.SetNColumns(4)
if (args.layout==2):
  legend2 = ROOT.TLegend(0.6, 0.7, 0.9, 0.9, '', 'NBNDC')
  legend2.SetNColumns(2)
try:
  legend2.AddEntry(conts68['default'][0], '1#sigma region', 'F')
  legend2.AddEntry(conts95['default'][0], '2#sigma region', 'L')
except IndexError:
  print(f"Warning: Missing at least one CL contour to add to legend2")
legend2.AddEntry(bestfits['default'], 'Best fit', 'P')
legend2.AddEntry(sm_point, 'SM expected', 'P')
legend2.SetMargin(0.4)
legend2.Draw()

latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.6*canv.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31)
latex2.DrawLatex(0.9, 0.95,"36.3#minus138 fb^{-1} (13 TeV)")
latex2.SetTextAlign(11)
latex2.SetTextSize(0.06)#0.7*canv.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.17, 0.87, "CMS")
latex2.SetTextSize(0.7*canv.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
#latex2.DrawLatex(0.25, 0.95, "Preliminary")
if args.suppl: latex2.DrawLatex(0.17, 0.83, "Supplementary")

#box = ROOT.TPave(0.15, 0.82, 0.41, 0.92, 0, 'NBNDC')
## box.Draw()
#plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{ and }CMS', '#it{LHC Run 1}', 11, 0.025, 0.035, 1.1, extraText2='#it{Internal}')
#plot.DrawTitle(pads[0], args.title_right, 3)

axis.SetMinimum(0)
axis.SetMaximum(6)

axis.GetZaxis().SetTitleOffset(0)

pads[0].RedrawAxis()
# plot.DrawCMSLogo(pads[0], '#it{ATLAS}#bf{+}CMS', '#it{LHC Run 1}', 11, 0.02, 0.035, 1.1, extraText2='#it{Internal}')
# pads[0].RedrawAxis()
canv.Print('.pdf')
canv.Print('.png')
outfile.Close()

