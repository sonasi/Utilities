from ROOT import *
from time import sleep
import array, os, sys, re
import plot_util

dirin = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc/train/"
dirout = "/home/jbochenek/work/HZZ4l_2013/plots"


gROOT.Reset()
gStyle.SetOptStat(0)  # What is displayed in the stats box for each histo.
gStyle.SetPadLeftMargin(0.10)   # Left margin of the pads on the canvas.
gStyle.SetPadBottomMargin(0.10) # Bottom margin of the pads on the canvas.
gStyle.SetFrameFillStyle(4000)  # will be transparent
#gStyle.SetFrameFillStyle() # Keep the fill color of our pads white.

mvavars = []

mvavarset = [
"f_massjj",
"f_deltajj",
]
mvavars.append(mvavarset)

mvavarset2 = [
"f_massjj",
"f_deltajj"
]

mvavarset3 = [
"f_pt4l",
"f_massjj",
"f_deltajj",
]

reader1 = TMVA.Reader()
var1_ = []
for i, var1 in enumerate(mvavarset):
	var1_.append(array.array('f',[0]))
	reader1.AddVariable(var1,var1_[i])
reader1.BookMVA("MLP","/home/jbochenek/work/HZZ4l_2013/tmva/weights/TMVAClassification6_cat2_MLP.weights.xml")

def fmlp(vars):
    for i, var in enumerate(vars):
        var1_[i][0] = float(var)
    y = reader1.EvaluateMVA("MLP")
    return y
    

reader2 = TMVA.Reader()
var2_ = []
for i, var2 in enumerate(mvavarset3):
	var2_.append(array.array('f',[0]))
	reader2.AddVariable(var2,var2_[i])
reader2.BookMVA("MLP","/home/jbochenek/work/HZZ4l_2013/tmva/weights/TMVAClassification5_cat2_MLP.weights.xml")

def fmlp2(vars):
    for i, var in enumerate(vars):
        var2_[i][0] = float(var)
    y = reader2.EvaluateMVA("MLP")
    return y

    

def fvd(vars):
    y = .0941*vars[1] + .000416*vars[0]
    return y
    
def fmela(vars):
    return vars[0]
fs = "4mu"    
bins = 100
sample = "GluGluToHToZZTo4L"
bkgfile = "{}/{}_cat2_test.root".format(dirin, sample)

sample = "VBF_HToZZTo4L"
sigfile = "{}/{}_cat2_test.root".format(dirin, sample)


#Calculate VD efficiency
cmva1 = TCanvas( 'c2', 'mva output', 200, 10, 700, 500 )
cmva1.Draw()
hs1 = TH1F('hs1', 'hs1', bins, 0., 2.)
hb1 = TH1F('hb1', 'hb1', bins, 0., 2.)
plot_util.loop( sigfile, hs1, fvd, cmva1, mvavarset2, 0 )
plot_util.loop( bkgfile, hb1, fvd, cmva1, mvavarset2, 0 )

heff1 = TH2F('heff', 'heff', bins, 0, 1.0,bins, 0.0, 1)
geff1 = TGraph()
geff1.SetName("bnneff_test")
geff1.SetLineWidth(2);
geff1.SetLineColor(2);
plot_util.calceff(geff1, heff1, hs1, hb1)



#Calculate MLP Efficiency
cmva = TCanvas( 'c1', 'mva output', 200, 10, 700, 500 )
hs = TH1F('hs', 'hs', bins, 0., 1.)
hb = TH1F('hb', 'hb', bins, 0., 1.)

plot_util.loop( sigfile, hs, fmlp, cmva, mvavarset, 0 )
plot_util.loop( bkgfile, hb, fmlp, cmva, mvavarset, 0 )

c1 = TCanvas()
c1.cd()
hs.Draw()
l = TLegend(0.5, 0.5, 0.8, 0.8)
hs.SetLineColor(2)
hs.SetLineColor(3)
hb.Draw("same")
l.AddEntry(hs, "#VBF")
l.AddEntry(hb, "ggH")
l.Draw("same")
sleep(2)

heff = TH2F('heff', 'heff', bins, 0, 1.0,bins, 0.0, 1)
geff = TGraph()
geff.SetName("bnneff_test")
geff.SetLineWidth(2);
geff.SetLineColor(3);

plot_util.calceff(geff, heff, hs, hb)



#Plot both on same graph
ceff = TCanvas( 'efficiency', 'efficiency', 200, 10, 700, 500 )
ceff.cd()
l = TLegend(0.5, 0.5, 0.8, 0.8)

l.AddEntry(hs, "#VBF")
l.AddEntry(hb, "ggH")
l.Draw("same")
heff.Draw()
geff.Draw("same")
geff1.Draw("same")
ceff.SaveAs(".gif")
sleep(5)



