from ROOT import *

dirin = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc"
dirout = "/home/jbochenek/data/HZZ4l_2013_ntuples/mc/train"


def maketrain(collection, fs):
    total = 3000
    masses = [115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,135,140,150,160,170,180]
    massrange = masses[len(masses)-1] - masses[0]
    totsofar = 0

    chaintrain1 = TChain("HZZ4LeptonsAnalysis")
    chaintest1 = TChain("HZZ4LeptonsAnalysis")
    chaintrain2 = TChain("HZZ4LeptonsAnalysis")
    chaintest2 = TChain("HZZ4LeptonsAnalysis")

    for index, mass in enumerate(masses):
        spacing = 0
        if index==0:
                spacing = float(masses[index+1] - masses[index]) / 2
        elif index == len(masses)-1:
                spacing = float(masses[index] - masses[index-1]) / 2
        else:
                spacing = float( masses[index+1] - masses[index-1] ) / 2
        number = total * spacing / massrange
        if index == len(masses)-1:
                number = total - totsofar
        totsofar += int(number)

        filein_ = "{}/output_{}_M-{}_8TeV-powheg-pythia6_{}_bnn.root".format(dirin , collection, mass, fs)
        print filein_
    
        filein = TFile(filein_)
        treein = filein.Get("HZZ4LeptonsAnalysis")
        nentry = treein.GetEntries()

        fileouttrain_ = "{}/{}_M-{}_cat2_train.root".format(dirout, collection, mass)    
        fileouttrain = TFile(fileouttrain_, "recreate")
        treeouttrain = treein.CloneTree(0)

        count = 0
        # Fill Histograms with tight and loose candidates
        for event in treein:
            if event.f_njets_pass < 2:
                continue
            if count < int(number):
                treeouttrain.Fill()
            count += 1

        print "train: {}".format(treeouttrain.GetEntries())

        treeouttrain.Write()
        fileouttrain.Close()
        chaintrain2.Add(fileouttrain_)


        fileouttrain_ = "{}/{}_M-{}_cat1_train.root".format(dirout, collection, mass)    
        fileouttrain = TFile(fileouttrain_, "recreate")
        treeouttrain = treein.CloneTree(0)

        count = 0
        # Fill Histograms with tight and loose candidates
        for event in treein:
            if event.f_njets_pass > 1:
                continue
            if count < int(number):
                treeouttrain.Fill()
            count += 1

        print "train: {}".format(treeouttrain.GetEntries())

        treeouttrain.Write()
        fileouttrain.Close()

        chaintrain1.Add(fileouttrain_)


        fileouttest_ = "{}/{}_M-{}_cat2_test.root".format(dirout, collection, mass)
        fileouttest = TFile(fileouttest_, "recreate")
        treeouttest = treein.CloneTree(1)
        count = 0

        # Fill Histograms with tight and loose candidates
        for event in treein:
            if event.f_njets_pass < 2:
                continue
            if count > int(number):
                treeouttest.Fill()
            count += 1

        treeouttest.Write()
        fileouttest.Close()

        chaintest2.Add(fileouttest_)

        fileouttest_ = "{}/{}_M-{}_cat1_test.root".format(dirout, collection, mass)
        fileouttest = TFile(fileouttest_, "recreate")
        treeouttest = treein.CloneTree(1)
        count = 0

        # Fill Histograms with tight and loose candidates
        for event in treein:
            if event.f_njets_pass > 1:
                continue
            if count > int(number):
                treeouttest.Fill()
            count += 1

        print "test: {}".format(treeouttest.GetEntries())
        filein.Close()

        treeouttest.Write()
        fileouttest.Close()

        chaintest1.Add(fileouttest_)


        print count
        filein.Close()

    mergefile = TFile("{}/{}_{}_cat1_test.root".format(dirout, collection, fs),"recreate")
    chaintest1.Merge(mergefile, 0, "fast")

    mergefiletrain = TFile("{}/{}_{}_cat1_train.root".format(dirout, collection, fs),"recreate")
    chaintrain1.Merge(mergefiletrain, 0, "fast")

    mergefile = TFile("{}/{}_{}_cat2_test.root".format(dirout, collection, fs),"recreate")
    chaintest2.Merge(mergefile, 0, "fast")

    mergefiletrain = TFile("{}/{}_{}_cat2_train.root".format(dirout, collection, fs),"recreate")
    chaintrain2.Merge(mergefiletrain, 0, "fast")

maketrain("VBF_HToZZTo4L", "2e2mu")
maketrain("GluGluToHToZZTo4L", "2e2mu")