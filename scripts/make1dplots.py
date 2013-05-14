from ROOT import *
from time import sleep
from histutil import *

setStyle()

dirin = "/home/jbochenek/data/HZZ4l_2013_ntuples/"
dirout = "/home/jbochenek/work/HZZ4l_2013/plots"


#Make basic distribution plots vs samples (pt1, pt4l, angles, etc)
dists_cat1 = [
["f_mass4l", 37, 70, 181, "m_{4l}", 0],
["f_Z2mass", 30, 0, 110, "m_{Z2}", 0],
["f_Z1mass", 25, 50, 105, "m_{Z1}", 0],
["f_angle_phi", 25, -1, 1., "#phi", 1, 0.1],
["f_angle_phistar1", 25, -1, 1., "#phi*", 1, 0.10],
["f_angle_costhetastar", 20, -1, 1, "cos(#theta*)", 1, 0.15],
["f_angle_costheta1", 25, -1, 1., "cos(#theta_{1})", 1, 0.1],
["f_angle_costheta2", 25, -1, 1., "cos(#theta_{2})", 1, 0.11],
["f_lept1_pt", 30, 0, 130, "pt_{l1}", 0],
["f_pt4l", 25, 0, 180, "p_{T,4l}", 0],
["f_njets_pass", 14, 0, 6, "n_{jets}", 0],
]

dists_cat2 = [
"f_jet1_pt",
"f_jet2_pt",
"f_jet2_e"   
]

samples = [
["ZZTo{}_8TeV-powheg-pythia6", "qq#rightarrow ZZ"],
["GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6", "gg #rightarrow H #rightarrow ZZ"],
["VBF_HToZZTo4L_M-126_8TeV-powheg-pythia6", "VBF"],
]

datafile = "ntuple_Run2012"

channels = ["2e2mu", "4mu", "4e"]

fs = "2e2mu"

for distribution in dists_cat1:


    legend = TLegend(0.6,0.6,0.88,0.92)
#    legend = TLegend(0.25,0.7,0.52,0.92)
    legend.SetFillColor(kWhite);
    legend.SetShadowColor(0);

    hdata = TH1F(distribution[0], distribution[0], int(distribution[1]), float(distribution[2]), float(distribution[3]))
    hdata.GetXaxis().SetTitle( distribution[4] )
    hdata.GetYaxis().SetTitle("events/bin")


    for fs in channels:    
        filein_ = "{}/mc/train/{}_{}_bnn.root".format(dirin, datafile, fs)
        print filein_
        filein = TFile(filein_)
        treein = filein.Get("HZZ4LeptonsAnalysis")
        nentry = treein.GetEntries()
    
        print "Data n = " + str(nentry)
    
        for event in treein:
            hdata.Fill(getattr(treein, distribution[0]), event.f_weight)
        if distribution[5] == 1:
            hdata.Scale(1./hdata.Integral())

    histogram = []

    c = TCanvas(distribution[0], distribution[0], 400, 400)
    c.Draw()
    for iter, sample in enumerate(samples):
        histogram.append(TH1F(distribution[0], distribution[0], int(distribution[1]), float(distribution[2]), float(distribution[3])))
        histogram[iter].SetDirectory(0)
        
    for iter, sample in enumerate(samples):
        
        histogram[iter].SetDirectory(0)
        print "{}/{}".format(iter, len(histogram))
        histogram[iter].SetLineColor(int(iter)+1)
        histogram[iter].SetFillColor(int(iter)+1)
        histogram[iter].SetFillStyle(3004)
        histogram[iter].GetXaxis().SetTitle( distribution[4] )
        histogram[iter].GetYaxis().SetTitle( "events/bin" )
        legend.AddEntry(histogram[iter], sample[1], "f")

        for fs in channels:
            filein_ = "{}/mc/train/output_{}_{}_bnn.root".format(dirin, sample[0], fs)
            filein_ = filein_.format(fs)
            print filein_
            filein = TFile(filein_)
            treein = filein.Get("HZZ4LeptonsAnalysis")
            nentry = treein.GetEntries()

            # Book and Fill Histograms
            count = 0
            for event in treein:
                histogram[iter].Fill(getattr(treein, distribution[0]), event.f_weight)
                count += event.f_weight

        if distribution[5] == 1:
            histogram[iter].Scale(1./histogram[iter].Integral())
        else: 
            print "{} Integral {}".format(sample[1],  histogram[iter].Integral())

#        print "{} {}: {}".format(iter, sample[0], count)
#        print iter
        if iter == 0:
            c.cd()
#            histogram[iter].Draw()
            print histogram[iter].Integral()

        else:
            c.cd()
#            histogram[iter].Draw("same")
            print histogram[iter].Integral()
            print "same"
        c.Update()
        


    hs = THStack("stack","")
    hdata.GetXaxis().SetTitle( distribution[4] )
    hdata.GetYaxis().SetTitle( "events/bin" )
#    hs.SetMaximum( distribution[6] )

    for iter, sample in enumerate(samples):
        hs.Add(histogram[iter], "h")

    if distribution[5] == 1:
        hs.Draw("nostack")
    else:
        hs.Draw()
        
    hs.GetHistogram().GetXaxis().SetTitle( distribution[4] )
    hs.GetHistogram().GetYaxis().SetTitle( "events/bin" )

#    if distribution[5] == 0:
#        legend.AddEntry(hdata, "Data: 19.2 fb^{-1}", "lep")
#        hdata.Draw("e1 p same")



    ttitle=TPaveText(0.2,0.95,0.6,1.0, "bordersize=5 NDC")
    ttitle.SetFillStyle(4000)
    ttitle.SetFillColor(0)
    ttitle.SetTextSize(0.035); 
    ttitle.SetTextAlign(12);
    ttitle.SetShadowColor(0);
    ttitle.AddText("CMS Preliminary");
    ttitle.Draw("same")


    legend.Draw("same")
    c.Update()
        

    sleep(1)
    c.SaveAs("{}/{}.png".format(dirout, distribution[0]))
    c.SaveAs("{}/{}.pdf".format(dirout, distribution[0]))