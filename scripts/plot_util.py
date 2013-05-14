from ROOT import *
import array, os, sys, re

def cdf(hist):
	n = hist.GetNbinsX()
	c = []
	print n
	sum = 0
	for i in range(n):
		sum = sum + hist.GetBinContent(i)
		c.append(sum)
	return c;
	
	
#------------------------------------------------------------------------------
# Make Discriminant distributions (loop thorugh events)
#------------------------------------------------------------------------------

def loop(ifile, hbnn, mva, cmva, mvavars, type):
    print ifile
    filein = TFile(ifile)
    treein = filein.Get("HZZ4LeptonsAnalysis")
    nentry = treein.GetEntries()

    count = 0 	

	#do signal	
    for event in treein:
        count+=1

        weight = float(event.f_weight)
        if event.f_njets_pass < 2:
            continue
        inputs = []
        for var in mvavars:
            inputs.append(getattr(treein, var))

        if(type==1):
            y = mva(inputs, 50, 100)
            hbnn.Fill(y)        
        if(type==0):
            y = mva(inputs)
            hbnn.Fill(y)

        if( not (count%1000)):
            print count
            cmva.cd()
#            hbnn.Draw()
            cmva.Update()
        
    filein.Close()	
    print "Total Count: " + str(count)	



#------------------------------------------------------------------------------
# Make individual ROC plot
#------------------------------------------------------------------------------

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

        print "bins:{}, es: {}, eb: {} ".format(i, es, eb)
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





def getrate(file, process):
    in_file = open(file)
    for line in in_file:
        data = line.rsplit()
        if data:
            if data[0] == "rate" and data[1] == process:
                return data[2]
    return -1

def getefficiency(file, ratefile, dataset):
    in_file = open(ratefile)
    count = getcount(file)
    for line in in_file:
        data = line.rsplit()
        if data:
            if data[0] == dataset:
                return float(count)/float(data[1])
    return -1

def getcs(file, ratefile, dataset):
    in_file = open(ratefile)
    for line in in_file:
        data = line.rsplit()
        if data:
            if data[0] == dataset:
                return float(data[4])
    return -1
    
def getcount(file):
    in_file = open(file)
    line = in_file.readline()
    data = line.rsplit()
    columns = []
    for varname in data:
        varname = varname.lstrip(':b')
        columns.append(varname); 
    count = 0

    for line in in_file:
        data = line.rsplit()
        d = dict(zip(columns, data))
        count += 1
    return count-1
    
def getsumweight(files):
    weight_sum = 0
    for file in files:
        in_file = open(file)
        line = in_file.readline()
        data = line.rsplit()
        columns = []
        for varname in data:
            varname = varname.lstrip(':b')
            columns.append(varname)
        for line in in_file:
            data = line.rsplit()
            d = dict(zip(columns, data))
            weight_sum += float(d["weight"])
    return weight_sum
    
def getsumweight_ntuple(files):
    weight_sum = 0
    for file in files:
        print file
        f = TFile(file)
        tree = f.Get("HZZ4LeptonsAnalysis")
        # Fill Histograms with tight and loose candidates
        for event in tree:
            if 100 < event.f_mass4l < 1000:
                weight_sum += event.f_weight
    return weight_sum
