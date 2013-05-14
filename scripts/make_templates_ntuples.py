#!/usr/bin/env python

#------------------------------------------------------------------------------
# File: make_templates_ntuples.py
# Created: 24-April-2013 Joe Bochenek
# $Revision$
# Description: Apply all the corrections and reproduce ntuples with correct 
#              weight.  The combined weight is stored in f_weight.
#               Also I make input histograms
#------------------------------------------------------------------------------



from ROOT import *
import numpy as np
import pyBNN
import sys
from time import sleep
import array, os, sys, re

import plot_util


#Library
ROOT.gSystem.AddIncludePath("-I $ROOFITSYS/include/")
ROOT.gSystem.AddIncludePath("-I /home/jbochenek/work/Limits/CreateDatacards/include/")
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("/home/jbochenek/work/Limits/CreateDatacards/include/HiggsCSandWidth_cc.so")
ROOT.gSystem.Load("/home/jbochenek/work/Limits/CreateDatacards/include/HiggsCSandWidthSM4_cc.so")


#Declare BNN
myCSW = HiggsCSandWidth("/home/jbochenek/work/Limits/CreateDatacards/include/txtFiles")
t = pyBNN.BayesianNNinterface()

print myCSW.HiggsCS(1, 125, 8)


#Declare VBF MLP
mvavarset = [
"f_massjj",
"f_deltajj",
]
reader1 = TMVA.Reader()
var1_ = []
for i, var1 in enumerate(mvavarset):
	var1_.append(array.array('f',[0]))
	reader1.AddVariable(var1,var1_[i])
reader1.BookMVA("MLP","/home/jbochenek/work/HZZ4l_2013/tmva/weights/TMVAClassification6_cat2_MLP.weights.xml")



def checkoverlap(thisevent, overlaplist):
    bool_overlap = 0
    for ievent in overlaplist:
        if ievent == thisevent:
            bool_overlap = 1
    return bool_overlap


def makeplot3d_data(files, name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, overlap):
    t.setChannel(channel)    
    
    # Declare Histograms
    bnn3d_cat1 = TH3F(name+"_cat1_3d", name+"_cat1_3d", xbins, xmin, xmax, ybins, ymin, ymax, zbins, zmin, zmax)
    bnn2d_cat1 = TH2F(name+"_cat1_2d", name+"_cat1_2d", xbins, xmin, xmax, ybins, ymin, ymax)
    bnn2dvbf_cat1 = TH2F(name+"_cat1_3dvbf", name+"_cat1_3dvbf", ybins, ymin,ymax, zbins, zmin, zmax)

    bnn3d_cat2 = TH3F(name+"cat2_3d", name+"_cat2_3d", xbins, xmin, xmax, ybins, ymin, ymax, zbins, zmin, zmax)
    bnn2d_cat2 = TH2F(name+"_cat2_2d", name+"_cat2_2d", xbins, xmin, xmax, ybins, ymin, ymax)
    bnn2dvbf_cat2 = TH2F(name+"_cat2_3dvbf", name+"_cat2_3dvbf", ybins, ymin,ymax, zbins, zmin, zmax)

    bnn2d = TH2F(name+"_2d", name+"_2d", xbins, xmin, xmax, ybins, ymin, ymax)


    nbinsX=21
    nbinsYps=25
    nbinsYgrav=29
    
    binsX = [0.000, 0.030, 0.060, 0.100, 0.200, 0.300, 0.400, 0.500, 0.550, 0.600, 0.633, 0.666, 0.700, 0.733, 0.766, 0.800, 0.833, 0.866, 0.900, 0.933, 0.966, 1.000]
    binsYps = [0.000, 0.100, 0.150, 0.200, 0.233, 0.266, 0.300, 0.333, 0.366, 0.400, 0.433, 0.466, 0.500, 0.533, 0.566, 0.600, 0.633, 0.666, 0.700, 0.733, 0.766, 0.800, 0.850, 0.900, 0.950, 1.000]
    binsYgrav = [0.000, 0.100, 0.150, 0.175 , 0.200, 0.225, 0.250, 0.275, 0.300, 0.325, 0.350, 0.375, 0.400, 0.425 , 0.450, 0.475, 0.500, 0.525, 0.575, 0.600, 0.633, 0.666, 0.700, 0.733 , 0.766, 0.800, 0.850, 0.900, 0.950, 1.000]

    abinsX = array.array('d',binsX)
    abinsYps = array.array('d',binsYps)
    abinsYgrav = array.array('d',binsYgrav)
    
    bnn_jcp_2PM = TH2F(name+"_2PM", name+"_2PM", nbinsX, abinsX, nbinsYgrav, abinsYgrav)
    bnn_jcp_0M  = TH2F(name+"_0M", name+"_0M", nbinsX, abinsX, nbinsYps, abinsYps)

    bnn3d_cat1.Sumw2()
    bnn2d_cat1.Sumw2()
    bnn2dvbf_cat1.Sumw2()
    bnn3d_cat2.Sumw2()
    bnn2d_cat2.Sumw2()
    bnn2dvbf_cat2.Sumw2()
    bnn2d.Sumw2()

    display = 0

    if display:
        c1 = TCanvas()
        c1.Divide(2,2)

    for file in files:
        f= TFile(file)
        tree = f.Get("HZZ4LeptonsAnalysis")
        nentry = tree.GetEntries()

        # Make ntuple files for training with correct weights

        parts = file.split("/")
        fileouttrain_ = "{}/{}".format(dirout, parts[-1])    
        fileouttrain = TFile(fileouttrain_, "recreate")
        treeouttrain = tree.CloneTree(0)
    
        print file    
        count = 0
        
        # Fill Histograms with tight and loose candidates
        for event in tree:


            bnnval = t.getBNNvalue(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l,  -1, -1)
            bnnvalps = t.getBNNvalueSPS(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l)
            bnnvalgrav = t.getBNNvalueGrav(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l)

            # Check for redundant events
            if checkoverlap(event.f_mass4l, overlap):
                print "OVERLAPPING EVENT (event mass {}) SKIPPED".format(event.f_mass4l)
                continue
            print "Checking with mass {}, bnn {}".format(event.f_mass4l, bnnval)
                
            weight = 1. 

            treeouttrain.Fill()
            
            count+=1

            overlap.append(event.f_mass4l)


            if (((event.f_mass4l) > 120) & ((event.f_mass4l) > 130)):
                bnn_jcp_2PM.Fill(bnnval, bnnvalgrav)
                bnn_jcp_0M.Fill(bnnval, bnnvalps)


            #  Fill the various histograms.  Slice the data.
            #      cat 1     cat 2
            #   --------------------
            #   |         |         |  int. reweight
            #   |         |         |
            #   --------------------
            #   |         |         |  no int. reweight
            #   |         |         |
            #   --------------------
            #    
            #   Global reweight = PU * scale * etc

            mlpval = 0
            
            bnn2d.Fill(event.f_mass4l, bnnval)

            if(event.f_njets_pass > 1):
                var1_[0][0] = float(event.f_massjj)
                var1_[1][0] = float(event.f_deltajj)            
                mlpval = reader1.EvaluateMVA("MLP")
                
                bnn3d_cat2.Fill(event.f_mass4l, bnnval, mlpval)
                bnn2d_cat2.Fill(event.f_mass4l, bnnval)
                bnn2dvbf_cat2.Fill(bnnval, mlpval)

            else:
                bnnval = t.getBNNvalue(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l,  -1, -1)
                bnn3d_cat1.Fill(event.f_mass4l, bnnval, event.f_pt4l)
                bnn2d_cat1.Fill(event.f_mass4l, bnnval)
                bnn2dvbf_cat1.Fill(bnnval, event.f_pt4l/event.f_mass4l)

            if display:
                if (not(count%1000)):
                    print "mass: {}, bnn: {}, bnngrav: {}, bnnps: {}, mlp: {}, weight: {}".format(event.f_mass4l, bnnval, bnnvalps, bnnvalgrav, mlpval, weight)
                    c1.cd(1)
                    bnn2d_cat1.Draw("colz")
                    c1.cd(2)
                    bnn2d_cat2.Draw("colz")
                    c1.cd(3)
                    bnn2dvbf_cat1.Draw("colz")
                    c1.cd(4)
                    bnn_jcp_0M.Draw("colz")
                    c1.Update()

        treeouttrain.Write()
        fileouttrain.Close()

    out_file.cd()

    print "Data Events: {}/{}".format(count, nentry)
        
    bnn3d_cat1.Write(name+"_cat1_3d")
    bnn2d_cat1.Write(name+"_cat1_2d")
    bnn2dvbf_cat1.Write(name+"_cat1_2dvbf")

    bnn3d_cat2.Write(name+"_cat2_3d")
    bnn2d_cat2.Write(name+"_cat2_2d")
    bnn2dvbf_cat2.Write(name+"_cat2_2dvbf")

    bnn2d.Write(name+"_2d")
    bnn_jcp_2PM.Write(name+"_jcp_2PM")
    bnn_jcp_0M.Write(name+"_jcp_0M")

    


def makeplot3d(files, name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, bool_reweight, global_reweight, isdata=false):
    t.setChannel(channel)    
    
    # Declare Histograms
    bnn3d_cat1 = TH3F(name+"_cat1_3d", name+"_cat1_3d", xbins, xmin, xmax, ybins, ymin, ymax, zbins, zmin, zmax)
    bnn2d_cat1 = TH2F(name+"_cat1_2d", name+"_cat1_2d", xbins, xmin, xmax, ybins, ymin, ymax)
    bnn2dvbf_cat1 = TH2F(name+"_cat1_3dvbf", name+"_cat1_3dvbf", ybins, ymin,ymax, zbins, zmin, zmax)

    bnn3d_cat2 = TH3F(name+"cat2_3d", name+"_cat2_3d", xbins, xmin, xmax, ybins, ymin, ymax, zbins, zmin, zmax)
    bnn2d_cat2 = TH2F(name+"_cat2_2d", name+"_cat2_2d", xbins, xmin, xmax, ybins, ymin, ymax)
    bnn2dvbf_cat2 = TH2F(name+"_cat2_3dvbf", name+"_cat2_3dvbf", ybins, ymin,ymax, zbins, zmin, zmax)

    bnn2d = TH2F(name+"_2d", name+"_2d", xbins, xmin, xmax, ybins, ymin, ymax)

    nbinsX=21
    nbinsYps=25
    nbinsYgrav=29
    
    binsX = [0.000, 0.030, 0.060, 0.100, 0.200, 0.300, 0.400, 0.500, 0.550, 0.600, 0.633, 0.666, 0.700, 0.733, 0.766, 0.800, 0.833, 0.866, 0.900, 0.933, 0.966, 1.000]
    binsYps = [0.000, 0.100, 0.150, 0.200, 0.233, 0.266, 0.300, 0.333, 0.366, 0.400, 0.433, 0.466, 0.500, 0.533, 0.566, 0.600, 0.633, 0.666, 0.700, 0.733, 0.766, 0.800, 0.850, 0.900, 0.950, 1.000]
    binsYgrav = [0.000, 0.100, 0.150, 0.175 , 0.200, 0.225, 0.250, 0.275, 0.300, 0.325, 0.350, 0.375, 0.400, 0.425 , 0.450, 0.475, 0.500, 0.525, 0.575, 0.600, 0.633, 0.666, 0.700, 0.733 , 0.766, 0.800, 0.850, 0.900, 0.950, 1.000]

    abinsX = array.array('d',binsX)
    abinsYps = array.array('d',binsYps)
    abinsYgrav = array.array('d',binsYgrav)
    
    bnn_jcp_2PM = TH2F(name+"_2PM", name+"_2PM", nbinsX, abinsX, nbinsYgrav, abinsYgrav)
    bnn_jcp_0M  = TH2F(name+"_0M", name+"_0M", nbinsX, abinsX, nbinsYps, abinsYps)
#    bnn_jcp_1m  = TH2F(name+"_2d", name+"_2d", xbins, xmin, xmax, ybins, ymin, ymax)


    bnn3d_cat1.Sumw2()
    bnn2d_cat1.Sumw2()
    bnn2dvbf_cat1.Sumw2()
    bnn3d_cat2.Sumw2()
    bnn2d_cat2.Sumw2()
    bnn2dvbf_cat2.Sumw2()
    bnn2d.Sumw2()

    int_weight_sum = 0
    int_weight_sum_cat1 = 0
    int_weight_sum_cat2 = 0
    count = 0
    cat1_count = 0
    cat2_count = 0
    weight_sum = 0

    display = 1
    if display:
        c1 = TCanvas()
        c1.Divide(2,2)

    for file in files:
        f= TFile(file)
        tree = f.Get("HZZ4LeptonsAnalysis")
        nentry = tree.GetEntries()
    
        
        # Fill Histograms with tight and loose candidates
        for event in tree:
            count += 1
            if(event.f_mass4l) < 100:
                continue
            weight = 1.
                
            if not(isdata):
                if bool_reweight==1:
                    weight = event.f_pu_weight * event.f_eff_weight * event.f_int_weight
                else: 
                    weight = event.f_pu_weight * event.f_eff_weight
                weight_sum += weight

            if(event.f_mass4l) > 180:
                continue
                


            #  Fill the various histograms.  Slice the data.
            #      cat 1     cat 2
            #   --------------------
            #   |         |         |  int. reweight
            #   |         |         |
            #   --------------------
            #   |         |         |  no int. reweight
            #   |         |         |
            #   --------------------
            #    
            #   Global reweight = PU * scale * etc
            bnnvalps = t.getBNNvalueSPS(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l)
            bnnvalgrav = t.getBNNvalueGrav(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l)

            bnnval = t.getBNNvalue(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l,  -1, -1)
            mlpval = 0
            bnn2d.Fill(event.f_mass4l, bnnval, weight)

            if (((event.f_mass4l) > 120) & ((event.f_mass4l) < 130)):
                bnn_jcp_2PM.Fill(bnnval, bnnvalgrav)
                bnn_jcp_0M.Fill(bnnval, bnnvalps)


            if(event.f_njets_pass > 1):
                var1_[0][0] = float(event.f_massjj)
                var1_[1][0] = float(event.f_deltajj)            
                mlpval = reader1.EvaluateMVA("MLP")
                
                bnn3d_cat2.Fill(event.f_mass4l, bnnval, mlpval, weight)
                bnn2d_cat2.Fill(event.f_mass4l, bnnval, weight)
                bnn2dvbf_cat2.Fill(bnnval, mlpval, weight)

            else:
                bnnval = t.getBNNvalue(event.f_Z1mass, event.f_Z2mass, event.f_angle_costhetastar, event.f_angle_costheta1, event.f_angle_costheta2, event.f_angle_phi, event.f_angle_phistar1, event.f_mass4l,  -1, -1)
                bnn3d_cat1.Fill(event.f_mass4l, bnnval, event.f_pt4l, weight)
                bnn2d_cat1.Fill(event.f_mass4l, bnnval, weight)
                bnn2dvbf_cat1.Fill(bnnval, event.f_pt4l/event.f_mass4l, weight)

            if display:
                if (not(count%1000)):
                    print "{} - mass: {}, bnn: {}, bnngrav: {}, bnnps: {}, mlp: {}, weight: {}".format(count, event.f_mass4l, bnnval, bnnvalps, bnnvalgrav, mlpval, weight)
                    c1.cd(1)
                    bnn2d_cat1.Draw("colz")
                    c1.cd(2)
                    bnn2d_cat2.Draw("colz")
                    c1.cd(3)
                    bnn_jcp_2PM.Draw("colz")
                    c1.cd(4)
                    bnn_jcp_0M.Draw("colz")
                    c1.Update()




        # Make ntuple files for training with correct weights

        parts = file.split("/")
        fileouttrain_ = "{}/{}".format(dirout, parts[-1])    
        fileouttrain = TFile(fileouttrain_, "recreate")
        treeouttrain = tree.CloneTree(0)


        evt_sum = 0            
        for event in tree:
            weight = 1.              
            if event.f_eff_weight == 0:
                event.f_eff_weight = 1.
                          
            if bool_reweight==1:
                weight =  event.f_pu_weight * event.f_eff_weight * event.f_int_weight * global_reweight / weight_sum 
            else: 
                weight =  event.f_pu_weight * event.f_eff_weight * global_reweight / weight_sum

#            print "rw: {}, weight: {},  event.f_pu_weight: {},  event.f_eff_weight: {} ".format(bool_reweight, weight,  event.f_pu_weight,  event.f_eff_weight )

            newweight = array.array('f',[0.])
            treeouttrain.SetBranchAddress( 'f_weight', newweight )    
            newweight[0] = weight
#            print "weight: {},  event.f_weight: {},  event.f_pu_weight: {},  event.f_eff_weight: {},  event.f_int_weight: {},  global_reweight: {},  weight_sum, {} ".format(weight, event.f_weight, event.f_pu_weight,  event.f_eff_weight, event.f_int_weight,  global_reweight,  weight_sum )
            treeouttrain.Fill()
            evt_sum += weight

        treeouttrain.Write()
        fileouttrain.Close()



    bnn2d.Scale(global_reweight/weight_sum)

    print "histogram integral {},\n global_reweight {}".format(bnn2d.Integral(), global_reweight)


    bnn2d_cat1.Scale(global_reweight/weight_sum)
    bnn3d_cat1.Scale(global_reweight/weight_sum)
    bnn2dvbf_cat1.Scale(global_reweight/weight_sum)

    bnn2d_cat2.Scale(global_reweight/weight_sum)
    bnn3d_cat2.Scale(global_reweight/weight_sum)
    bnn2dvbf_cat2.Scale(global_reweight/weight_sum)

    out_file.cd()

        
    bnn3d_cat1.Write(name+"_cat1_3d")
    bnn2d_cat1.Write(name+"_cat1_2d")
    bnn2dvbf_cat1.Write(name+"_cat1_2dvbf")

    bnn3d_cat2.Write(name+"_cat2_3d")
    bnn2d_cat2.Write(name+"_cat2_2d")
    bnn2dvbf_cat2.Write(name+"_cat2_2dvbf")

    bnn2d.Write(name+"_2d")

    bnn_jcp_2PM.Write(name+"_jcp_2PM")
    bnn_jcp_0M.Write(name+"_jcp_0M")



masses_8TeV =  [115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,135,140,145,150,160,170,180]
masses_7TeV =  [115,120,125,130,140,150,160,170, 180]


channels = ["2e2mu", "4mu", "4e"]
reweight = [1, 1, 0]
eras = ["7TeV", "8TeV"]
xmin = 115
xmax = 180
xbins = 65
ymin = 0.
zmin = 0.
ymax = 1.
zmax = 1.
ybins = 20
zbins = 20

out_file = TFile("hzz_templates_test.root", "recreate")
limits_dir = "/home/jbochenek/work/Limits/CreateDatacards/"
dirin = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc/"
dirout = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc/train/"

dirindata = "/home/jbochenek/data/HZZ4l_2013_ntuples/data/"
Z2lBR = 0.03365
lumi7TeV = 5.051
lumi8TeV = 19.21



#We're only doing 8TeV for now
sqrts = 8
era = str(sqrts) + "TeV"




#Data Frist
overlap = []




for ichannel, channel in enumerate(channels):

    #    for channel in channels:
    t.setChannel(channel)
    print "reweight? " + str(reweight[ichannel])


    # Background gg -> ZZ 
    files = [
    "{0}output_GluGluToZZTo2L2L_TuneZ2star_{1}-gg2zz-pythia6_{2}_bnn.root".format(dirin, era, channel),
    "{0}output_GluGluToZZTo4L_{1}-gg2zz-pythia6_{2}_bnn.root".format(dirin, era, channel)
    ]
    print ""
    name = "ggzz_{0}_{1}".format(channel,era)
    print name
    datacard = "{0}SM_inputs_{1}/inputs_{2}.txt".format(limits_dir, era, channel) 
    rate = float(plot_util.getrate(datacard, "ggZZ"))
    evtcountfile = plot_util.getsumweight_ntuple(files)
    print "rate = {0}".format(rate)
    doreweight = 0
    makeplot3d(files, name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, doreweight, rate)



    # signal gg -> H -> ZZ -> 4l
    for thismass in masses_8TeV:
        print ""
        name = "ggH_{0}_{1}_{2}".format(thismass,channel,era)
        print name

        dataset = 'GluGluToHToZZTo4L_M-{0}_{1}-powheg-pythia6'.format(thismass, era)
        thisfile = '{0}output_{1}_{2}_bnn.root'.format(dirin, dataset, channel)
        eff = plot_util.getefficiency(thisfile, "sig_input_Summer12_Moriond.txt", dataset)

        CS_ggH = myCSW.HiggsCS(1, float(thismass), sqrts)
        BR_HZZ = myCSW.HiggsBR(11, float(thismass))
        evtcountfile = plot_util.getsumweight_ntuple([thisfile])


#        print "New weight: " + str(CS_ggH*myCSW.HiggsBR(13, float(thismass))*eff*1000.*lumi8TeV)

        evtcount = 2*CS_ggH*BR_HZZ*(9*Z2lBR*Z2lBR)*eff*1000*lumi8TeV
        print "CS_ggH ({0}) * BR_HZZ ({1}) * 9*Z2lBR({3})*Z2lBR({3}) * eff({2}) * (1000) * lumi7TeV({4}) = {5}".format(CS_ggH, BR_HZZ, eff, Z2lBR, lumi8TeV, evtcount)
        print "evt count file = {0}".format(evtcount / evtcountfile)
        print ""

        doreweight = reweight[ichannel]

        if thismass > 170:
            doreweight = 0
        makeplot3d([thisfile], name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, doreweight, evtcount)




    # signal VBF, qq -> H -> ZZ -> 4l
    for thismass in masses_8TeV:
        print ""
        name = "qqH_{0}_{1}_{2}".format(thismass, channel, era)
        print name
        dataset = 'VBF_HToZZTo4L_M-{0}_{1}-powheg-pythia6'.format(thismass, era)
        thisfile = '{0}output_{1}_{2}_bnn.root'.format(dirin, dataset, channel)
        eff = plot_util.getefficiency(thisfile, "sig_input_Summer12_Moriond.txt", dataset)
        evtcountfile = plot_util.getsumweight_ntuple([thisfile])
        CS_ggH = myCSW.HiggsCS(2, float(thismass), sqrts)
        BR_HZZ = myCSW.HiggsBR(11, float(thismass))
        evtcount = CS_ggH*BR_HZZ*(9*Z2lBR*Z2lBR)*eff*1000*lumi8TeV

        print "CS_ggH ({0}) * BR_HZZ ({1}) * 9*Z2lBR({3})*Z2lBR({3}) * eff({2}) * (1000) * lumi7TeV({4}) = {5}".format(CS_ggH, BR_HZZ, eff, Z2lBR, lumi8TeV, evtcount)
        print "evt count / evt count file = {0}".format(evtcount / evtcountfile)
        doreweight = reweight[ichannel]
        if thismass > 170:
            doreweight = 0
        makeplot3d([thisfile], name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, doreweight, evtcount)
        print ""


      




# MC Samples Now
for ichannel, channel in enumerate(channels):
    # Background ( qq -> ZZ )
    print ""
    name = "qqzz_{0}_{1}".format(channel,era)
    print name  
    thisfile = '{0}output_ZZTo{1}_{2}-powheg-pythia6_{1}_bnn.root'.format(dirin, channel, era)
    datacard = "{0}SM_inputs_{1}/inputs_{2}.txt".format(limits_dir, era, channel) 
    sumweight = plot_util.getsumweight_ntuple([thisfile])
    rate = float(plot_util.getrate(datacard, "qqZZ"))
    print "rate = {0}".format(rate)
    print "sumwegiht = {0}".format(sumweight)
    makeplot3d([thisfile], name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, 0, rate)




for ichannel, channel in enumerate(channels):
    sqrts = 8
    era = str(sqrts) + "TeV"

    t.setChannel(channel)
    t.setEra(era)

    print ""
    name = "data_{0}_{1}".format(channel,era)
    print name  
    thisfile = '{0}ntuple_Run2012_{1}_bnn.root'.format(dirindata, channel)
    print thisfile
    makeplot3d_data([thisfile], name, xmin, ymin, zmin, xmax, ymax, zmax, xbins, ybins, zbins, out_file, overlap)
