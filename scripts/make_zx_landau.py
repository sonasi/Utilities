from ROOT import *
from time import sleep
import numpy as np

file = 'hzz_templates.root'
f_in = TFile(file)

# Get the Landau Distribution

mean = 140.3
sigma = 17.9

mean_7 = [
133.8,
148.0,
143.1
]
 
sigma_7 = [
15.4,
20.6,
19.9
]

mean_8 = [
140.3,
148.9,  
146.4
]

sigma_8 = [
21.7,
20.2,
19.6
]

central_7 = [
1.0,
1.9,  
3.0
]

central_8 = [
2.1,
4.5,  
7.1
]

channels = ["4mu",  "4e", "2e2mu"]
eras = ["8TeV"]

f_out = TFile("hzz_templates.root", "update")

#mvas = ["bnn", "mela"]
#for mva in mvas:    
for era in eras:
    for iter, channel in enumerate(channels):
        x = RooRealVar("x","4l mass (m4l)",100.0,600.0)

        if era == "7TeV":
            mean_ = mean_7[iter]
            sigma_ = sigma_7[iter]
            central_ = central_7[iter]
        if era == "8TeV":
            mean_ = mean_8[iter]
            sigma_ = sigma_8[iter]
            central_ = central_8[iter]
        
        # Define the calibration peak
        mean = RooRealVar("calib_mean","Landau mean of the calibration peak",mean_,101,169)
        sigma = RooRealVar("calib_sigma","Landau sigma of the calibration peak",sigma_,10,40)
        
        #calib_landau = RooLandau("calib_landau","Landau PDF for calibration peak",x,calib_mean,calib_sigma)
        zx_landau = RooLandau("zx_landau_{0}_{1}".format(channel,era), "Landau for ZX bkg",x,mean,sigma)
        
        xframe = x.frame()
        zx_landau.plotOn(xframe) 
        xframe.Draw() 
        
        xbins = 600            
                    
        bins = RooBinning(xbins, 115, 180)
        hh = zx_landau.createHistogram("x",xbins)
        hh.Draw()
        hh.Scale(central_/hh.Integral())
        print "qqzz_{0}_{1}".format(channel,era)
        print central_
        print hh.Integral(1, 35)
         
        # Now get the 2D ZZ mela ZX template
        f_in.cd();

        print "qqzz_{0}_{1}_cat1_2d".format(channel,era)

        zzbkg = gDirectory.Get("qqzz_{0}_{1}_cat1_2d".format(channel,era))
        zzbkg.SetName("qqzz_{0}_{1}_cat1_2d".format(channel,era))
#            zzbkg.Smooth()


        xbins = zzbkg.GetXaxis().GetNbins()
        ybins = zzbkg.GetYaxis().GetNbins()
        
        zzbkg_new = TH2F("zjets_{0}_{1}".format(channel,era), "zjets_{0}_{1}".format(channel,era), xbins, 115, 180, ybins, 0, 1.)
        zzbkg.Draw("colz")
        zzbkg_new.Sumw2()
        
        for binx in xrange(xbins):
            zzbkg1d = zzbkg.ProjectionY("zzbkg1d", binx+1, binx+2)
            zzbkg1d.Draw()
#                zzbkg1d.Smooth()
#            print hh.GetBinContent(binx+1)
            zzbkg1d.Scale(hh.GetBinContent(binx+1)/zzbkg1d.Integral())
            for biny in xrange(ybins):
#                print str(binx) + " " + str(biny) + " " + str(zzbkg1d.GetBinContent(biny+1) )
                zzbkg_new.SetBinContent(binx+1,biny+1, zzbkg1d.GetBinContent(biny+1) )
                zzbkg_new.SetBinError(  binx+1,biny+1, zzbkg1d.GetBinContent(biny+1)/4 )

#            print zzbkg_new.Integral(1,35)

        zzbkg_new.Draw("colz")

        f_out.cd()
        hh.Write()
        zzbkg.Write()
        zzbkg_new.Write()