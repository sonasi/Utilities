from ROOT import *
from time import sleep
import numpy as np
import pyBNN

dirin = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc"
dirout = "/home/jbochenek/work/HZZ4l_2013/plots"

t = pyBNN.BayesianNNinterface()

gROOT.Reset()
gStyle.SetOptStat(0)  # What is displayed in the stats box for each histo.
gStyle.SetPadLeftMargin(0.10)   # Left margin of the pads on the canvas.
gStyle.SetPadBottomMargin(0.10) # Bottom margin of the pads on the canvas.
gStyle.SetFrameFillStyle(4000)  # will be transparent
gStyle.SetFrameFillColor(0) # Keep the fill color of our pads white.

#First make basic distribution plots vs samples (pt1, pt4l, angles, etc)

samples = [
["ZZTo2e2mu_8TeV-powheg-pythia6", "qq#rightarrow ZZ"],
["GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6", "gg#rightarrow H #rightarrow 4l"],
["VBF_HToZZTo4L_M-125_8TeV-powheg-pythia6", "qq#rightarrow H #rightarrow 4l"]
]

distribution = ["bnnval_njets2_comparison", 25, 0, 1, "BNN(x)", 1]

fs = "2e2mu"
t.setChannel(fs)    
t.setEra("8TeV")

histogram = []

c = TCanvas(distribution[0], distribution[0], 400, 400)
c.Draw()
legend = TLegend(0.5,0.7,0.9,0.9)
legend.SetFillColor(0)

for iter, sample in enumerate(samples):
    histogram.append(TH1F(distribution[0], distribution[0], int(distribution[1]), float(distribution[2]), float(distribution[3])))
    histogram[iter].SetDirectory(0)
    
for iter, sample in enumerate(samples):
    filein_ = "{}/output_{}_{}_bnn.root".format(dirin, sample[0], fs)

    filein = TFile(filein_)
    treein = filein.Get("HZZ4LeptonsAnalysis")
    nentry = treein.GetEntries()
    
    histogram[iter].SetDirectory(0)
    print "{}/{}".format(iter, len(histogram))
    histogram[iter].SetLineColor(int(iter)+1)
    histogram[iter].SetFillColor(int(iter)+1)
    histogram[iter].SetFillStyle(3004)

    histogram[iter].SetLineWidth(2)
    histogram[iter].GetXaxis().SetTitle( distribution[4] )
    histogram[iter].GetYaxis().SetTitle("# events/bin")
    h = histogram[iter]
    legend.AddEntry(h, sample[1], "f")


    # Book and Fill Histograms
    count = 0
    print "count, event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l"
    for event in treein:
        if event.f_mass4l < 100:
            continue
        if event.f_mass4l > 175:
            continue
        if event.f_njets_pass < 2:
            continue
            
        bnnval = t.getBNNvalue(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l,  -1, -1)
        histogram[iter].Fill(bnnval, event.f_weight)
        count += 1
        if not(count%1000):
            print "{}: bnn: {} - {}, {}, {}, {}, {}, {}, {}, {}".format(count, bnnval, event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l)
            histogram[iter].Draw()
            c.Update()
    
    if distribution[5] == 1:
        histogram[iter].Scale(1./histogram[iter].Integral())

    print "{} {}: {}".format(iter, sample[0], count)
    print iter
    if iter == 0:
        c.cd()
        print histogram[iter].Integral()

    else:
        c.cd()
        print histogram[iter].Integral()
        print "same"
    c.Update()

hs = THStack("stack","")
for iter, sample in enumerate(samples):
    hs.Add(histogram[iter], "h")

hs.Draw("nostack")
hs.GetXaxis().SetTitle( distribution[4] )
if distribution[5] == 1:
    hs.GetYaxis().SetTitle("normalized")
if distribution[5] == 0:
    hs.GetYaxis().SetTitle("")

legend.Draw("same")
c.Update()
sleep(1)
c.SaveAs("{}/{}.gif".format(dirout, distribution[0]))