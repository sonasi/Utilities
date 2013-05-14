from string import *
from ROOT import *
from time import sleep
#import os, sys, re, hzz4mu_200_ext, hzz4e_200_ext, hzz2e2mu_200_ext, blabo
import os, sys, re
import bnn_4e_m4l_ext, bnn_4e_m125_ext, bnn_4e_2_ext, bnn_4mu_2_ext, bnn_4mu_7TeV_ext, bnn_4e_7TeV_ext, bnn_2e2mu_7TeV_ext, bnn_2e2mu_2_ext
gROOT.Reset()
#gROOT.ProcessLine(".L classes/TR130NoDY_6V_blabo.c")

def cdf(hist):
	n = hist.GetNbinsX()
	c = []
	print n
	sum = 0
	for i in range(n):
		sum = sum + hist.GetBinContent(i)
		c.append(sum)
	return c;

vdouble = vector("double")


#weight	weight	ele1_pt	ele1_eta	ele1_phi	ele1_charge	ele1_trackIso	ele1_EcalIso	ele1_HcalIso	ele1_X	ele1_SIP	ele2_pt	ele2_eta	ele2_phi	ele2_charge	ele2_trackIso	ele2_EcalIso	ele2_HcalIso	ele2_X	ele2_SIP	ele3_pt	ele3_eta	ele3_phi	ele3_charge	ele3_trackIso	ele3_EcalIso	ele3_HcalIso	ele3_X	ele3_SIP	ele4_pt	ele4_eta	ele4_phi	ele4_charge	ele4_trackIso	ele4_EcalIso	ele4_HcalIso	ele4_X	ele4_SIP	

#worst_iso_X	second_worst_iso_X	worst_vertex	second_worst_vertex	mZ	mZstar	mbestH	index	channel	sample	end

def eventloop(files, eras):
    
    
    dt = TGraph()
    dt.SetMarkerSize(1.)
    dt.SetMarkerStyle(28);
    dt.SetLineWidth(3)        

    dt2 = TGraph()
    dt2.SetMarkerSize(1.)
    dt2.SetMarkerStyle(26);
    dt2.SetLineWidth(3)        


    c1 = TCanvas( 'c1', 'mva output',600,500);
    c1.cd()


    gStyle.SetPalette(1);
    gStyle.SetOptStat(0);
    _file0 = TFile.Open("/home/jbochenek/work/HZZ4l_2012/output/hist_fullsel_7TeV.root")
    _file0.cd()
    histos_sig_130 = gDirectory.Get("histos_sig_125")
    histos_sig_130.SetTitle("Data (2011 dataset, 10.2 + 5.1 fb^{-1}) - BNN(x) vs. m_{4l}");
    histos_sig_130.GetXaxis().SetTitle("m_{4l}");
    histos_sig_130.GetYaxis().SetTitle("BNN(x)");
    histos_sig_130.SetMarkerSize(10.);
    _file1 = TFile.Open("/home/jbochenek/work/HZZ4l_2012/output/hist_fullsel.root")
    _file1.cd()

    histos_sig_8TeV = gDirectory.Get("histos_sig_125")
    histos_sig_130.Add(histos_sig_8TeV)
    histos_sig_130.Draw("colz")
    
    c2 = TCanvas( 'c2', 'mva output',600,500);
    c2.cd()
    _file0.cd()

    bkg = gDirectory.Get("bkg2d")
    bkg.SetTitle("Data (2011 dataset, 10.2 + 5.1 fb^{-1}) - BNN(x) vs. m_{4l}");
    bkg.GetXaxis().SetTitle("m_{4l}");
    bkg.GetYaxis().SetTitle("BNN(x)");
    bkg.SetMarkerSize(10.);
    _file1 = TFile.Open("/home/jbochenek/work/HZZ4l_2012/output/hist_fullsel.root")
    _file1.cd()
    bkg_8TeV = gDirectory.Get("bkg2d")
    bkg.Add(bkg_8TeV)
    bkg.Draw("colz")
    
        
    mvavars = [
    "angle_costhetastar",
    "angle_costheta1",
    "angle_costheta2",
    "angle_phi",
    "angle_phistar1",
    "Z1mass",
    "Z2mass",
    "mass4l"
    ]
    
    
    
    bins = 200
    heff = TH2F('heff_train', 'heff_train', bins, 0, 1.0,bins, 0.2, 1)
    
    hs = []
    hb = []
    index = 0
    index2 = 0

    for findex, file in enumerate(files):
        era = eras[findex]
        sig = file
        line = sig.readline()
        data = line.rsplit()
        columns = []
        for varname in data:
            print varname
            varname = varname.lstrip(':b')
            columns.append(varname); 
        
        i = 0
        #do signal
        for line in sig:
            data = line.rsplit()
            d = dict(zip(columns, data))
            inputs = []
            y = 0
            if (float(d["mass4l"])<140): 
                continue
            for var in mvavars:
                inputs.append(float(d[var]))
            if era == "7TeV":        
                index = index + 1 
                if(int(d["channel"]) == 1):
                    y = bnn_4mu_7TeV_ext.bnn_4mu_7TeV(inputs, 50, 100);
                if(int(d["channel"]) == 2):
                    y = bnn_4e_7TeV_ext.bnn_4e_7TeV(inputs, 50, 100);
                if(int(d["channel"]) == 3):
                    y = bnn_2e2mu_7TeV_ext.bnn_2e2mu_7TeV(inputs, 50, 100);
                dt.SetPoint(index, float(d["mass4l"]), y)

            if era == "8TeV":    
                index2 = index2 + 1 
                if(int(d["channel"]) == 1):
                    y = bnn_4mu_2_ext.bnn_4mu_2(inputs, 50, 100);
                if(int(d["channel"]) == 2):
                    y = bnn_4e_m4l_ext.bnn_4e_m4l(inputs, 50, 100);
                if(int(d["channel"]) == 3):
                    y = bnn_2e2mu_2_ext.bnn_2e2mu_2(inputs, 50, 100);
                dt2.SetPoint(index2, float(d["mass4l"]), y)
                
            #		hs[int(d["index"])].Fill(y, float(d["weight"]))

            c1.cd()
            dt.Draw("p same")
            dt2.Draw("p same")

            c1.Update()
            c2.cd()
            dt.Draw("p same")
            dt2.Draw("p same")

            c2.Update()
        
        sig.close()

    c1.cd()
    dt.Draw("p same")
    c1.Update()
    c2.cd()
    dt.Draw("p same")
    c2.Update()
    
    c1.Update()
    c1.SaveAs("/home/jbochenek/work/HZZ4l_2012/output/overlay_sig_data_blind.pdf")
    c2.Update()
    c2.SaveAs("/home/jbochenek/work/HZZ4l_2012/output/overlay_bkg_data_blind.pdf")
	

files = [
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_1.dat'),
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_2.dat'),
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_3.dat'),
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_7TeV_1.dat'),
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_7TeV_2.dat'),
open('/home/jbochenek/data/HZZ4l_2012_Nov01/data_7TeV_3.dat')
]

eras = [
"8TeV",
"8TeV",
"8TeV",
"7TeV",
"7TeV",
"7TeV",
]
eventloop(files, eras)


#sig = open('/home/jbochenek/data/HZZ4lNov6-2011/hzz/sigs_test_4mu.txt')
#bkg = open('/home/jbochenek/data/HZZ4lNov6-2011/hzz/bkgs_test_4mu.txt')
#eventloop(sig, bkg, "4mu_noiso_4edata", "test")