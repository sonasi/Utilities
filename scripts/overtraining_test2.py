from string import *
from ROOT import *
from time import sleep

import pyBNN
import histutil 
import os, sys, re

from ROOT import TMVA
import array

histutil.setStyle()

t = pyBNN.BayesianNNinterface()

t.setChannel("2e2mu")
era = "8TeV"
t.setEra(era)


gROOT.Reset()


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


def loop(hweights, sig, hs, c1):


    #------- sig events ---------
    stotal_ = 0
    stotal_sel = 0
    sigweight = 0
    i = 0 
    line = sig.readline()
    data = line.rsplit()
    columns = []
    for varname in data:
#        print varname
        varname = varname.lstrip(':b')
        columns.append(varname); 

    print sig

    #do signal
    for line in sig:
        data = line.rsplit()
        data_ = map(float, line.rsplit())
        d = dict(zip(columns, data))
        inputs = []


        if(float(d["mass4l"]) < 110):
            continue
        if(float(d["mass4l"]) > 150):
            continue

        channel_ = 1
        weight = float(d["weight"])
        y = t.getBNNvalue(float(d["Z1mass"]), float(d["Z2mass"]), float(d["angle_costhetastar"]), float(d["angle_costheta1"]), float(d["angle_costheta2"]), float(d["angle_phi"]), float(d["angle_phistar1"]), float(d["mass4l"]),  0.5, 0.5)



        weight = float(d["weight"])
        hweights.Fill(float(d["Z2mass"]))
        stotal_ += float(d["weight"])

        hs.Fill(y, weight)


        i+=1
        if( not (i%1000)):
            print i
            print y	
            hs.Draw()
            c1.Update()
    sig.close()
    hs.Scale(1/hs.Integral())
    print "Integral hs: " + str(hs.Integral())

def calceff(geff, heff, hs, hb):
	
	stotal=hs.Integral();
	btotal=hb.Integral();
	cs = cdf(hs);
	cb = cdf(hb);
	
	maxsig = 0;
	optmvax = 0;
	optmvay = 0;
	optcut = 0;
	
	bins = hs.GetNbinsX()
	
	for i in range(hs.GetNbinsX()):
		cs1 = stotal - cs[i-1]
		cb1 = btotal - cb[i-1]
		es = cs1 / stotal
		eb = cb1 / btotal
		sign=0
		if(cb1 > 0): 
			sign = cs1/sqrt(cs1 + cb1)
		if(sign > maxsig):
			maxsig = sign;
			optcut = i;	 
			optmvax = eb;
			optmvay = es;
		heff.Fill(eb, es);
		if(i<2):
			continue
		else:
			geff.SetPoint(geff.GetN(), eb, es);

	print "\n Maximum Significance " + str(maxsig) + ", is bin: " + str(optcut) + ", which is BNN Cut: " + str(optcut/bins)
	print "es: " + str(optmvay) + "\teb: " + str(optmvax)
	
	

def eventloop(sig_test,bkg_test, sig_train, bkg_train,channel,evtset):

	bins = 50
	
	hs_test =  TH1F('hs_test', 'hs_test', bins, 0, 1)
	hs_train = TH1F('hs_train','hs_train',bins, 0, 1)
	hb_test =  TH1F('hb_test', 'hb_test', bins, 0, 1)
	hb_train = TH1F('hb_test', 'hb_test', bins, 0, 1)

	hb_test.GetXaxis().SetTitle("BNN(x)")
	hb_test.GetYaxis().SetTitle("Normalized")
	
	hs_test.Sumw2()
	hb_test.Sumw2()
	hs_train.Sumw2()
	hb_train.Sumw2()


	hweights1 = TH1F('weights1', 'weights1', 50, 0, 100)
	hweights2 = TH1F('weights2', 'weights2', 50, 0, 100)
	hweights3 = TH1F('weights2', 'weights2', 50, 0, 100)
	hweights4 = TH1F('weights2', 'weights2', 50, 0, 100)

	hs_test.SetLineColor(2);
	hb_test.SetLineColor(1);
	hs_train.SetLineColor(2);
	hb_train.SetLineColor(1);
	
	
	legend = TLegend(0.7,0.73,0.87,0.92)
	legend.SetFillColor(kWhite);
	legend.SetShadowColor(0);
    
	legend.AddEntry(hs_test, "signal test", "l")
	legend.AddEntry(hs_train, "signal train", "lep")
	legend.AddEntry(hb_test, "bkg test", "l")
	legend.AddEntry(hb_train, "bkg train", "lep")

	
	c1 = TCanvas( 'c1', 'mva output', 200, 10, 700, 500 )
	c1.cd()
	c1.SetGridx()
	c1.SetGridy()
#	c1.SetLogy()
	c1.Draw()
	gStyle.SetOptStat(0);

	loop(hweights1, sig_test, hs_test, c1)
	loop(hweights2, sig_train, hs_train, c1)
	loop(hweights3, bkg_test, hb_test, c1)
	loop(hweights4, bkg_train, hb_train, c1)
	
 	print "Integral hb_test: " +  str(hb_test.Integral())
 	print "Integral hb_train: " + str(hb_train.Integral())
 	print "Integral hs_test: " +  str(hs_test.Integral())
 	print "Integral hs_train: " + str(hs_train.Integral())


 	print "KS test signal: {:e}".format(hs_test.KolmogorovTest(hs_train))
 	print "KS test bkg: {:e}".format(hb_test.KolmogorovTest(hb_train))
	
 	ttitle=TPaveText(0.4,0.82,0.65,0.9, "bordersize=5 NDC")
 	ttitle.SetFillStyle(4000)
 	ttitle.SetFillColor(0)
 	ttitle.AddText("KS test sig: {:.2}".format(hs_test.KolmogorovTest(hs_train)))
 	ttitle.AddText("KS test bkg: {:.2}".format(hb_test.KolmogorovTest(hb_train)))
 	ttitle.Draw("same")

	
	hb_test.Draw("hist")		
	hb_train.Draw("lep same")
	hs_test.Draw("hist same")
	hs_train.Draw("lep same")
	
	legend.Draw("same")
	ttitle.Draw("same")

	c1.Update()
	c1.SaveAs("../plots/hdist_bnn_train_vs_test_" + channel + "_" + evtset + ".pdf")
	c1.SaveAs("../plots/hdist_bnn_train_vs_test_" + channel + "_" + evtset + ".png")



	sleep(10)	


channel = "2e2mu"

sig_test = open('/home/jbochenek/data/HZZ4l_2012_Nov01/training_files/GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6_{}_bnn_test.txt'.format(channel))
bkg_test = open('/home/jbochenek/data/HZZ4l_2012_Nov01/training_files/ZZTo{0}_8TeV-powheg-pythia6_{0}_bnn_cut_110_185_test.txt'.format(channel))
sig_train = open('/home/jbochenek/data/HZZ4l_2012_Nov01/training_files/GluGluToHToZZTo4L_ensemble_8TeV_{}.txt'.format(channel))
bkg_train = open('/home/jbochenek/data/HZZ4l_2012_Nov01/training_files/ZZTo{0}_8TeV-powheg-pythia6_{0}_bnn_cut_110_185_train.txt'.format(channel))

eventloop(sig_test, bkg_test, sig_train, bkg_train, channel, "1")

