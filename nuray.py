#!/usr/bin/env python

from ROOT import TH1F, TFile

hists1D = [
    ("numu", 120,  0, 120),
    ("numubar", 120,  0, 120),
    ("nue", 120,  0, 120),
    ("nuebar", 120,  0, 120)
]

class Nuray(object):
    def __init__(self,root_file,det):
        self.idxdet = self.GetIdxDet(det)
        self.thistag = "nuray_" + det
        root_file.mkdir(self.thistag)
        self.thisgroup = self.book_hists()
        return

    ##########################################
    
    def fill(self, thisentry):
        wgt = (thisentry.dk2nu.decay.nimpwt)*(thisentry.dk2nu.nuray[self.idxdet].wgt)  
        pdg = thisentry.dk2nu.decay.ntype
        if pdg == 14:
            self.thisgroup[0].Fill(thisentry.dk2nu.nuray[self.idxdet].E,wgt)      
        if pdg == -14:
            self.thisgroup[1].Fill(thisentry.dk2nu.nuray[self.idxdet].E,wgt)      
        if pdg == 12:
            self.thisgroup[2].Fill(thisentry.dk2nu.nuray[self.idxdet].E,wgt)      
        if pdg == -12:
            self.thisgroup[3].Fill(thisentry.dk2nu.nuray[self.idxdet].E,wgt)      

        return

    ##########################################

    def save(self,root_file):
        root_file.cd(self.thistag)
        for i in self.thisgroup:
            i.Write()
        return

    ##########################################

    def book_hists(self):
        hist_group = []
        for i in hists1D:
            hist_group.append(
                TH1F("{}_{}".format(self.thistag, i[0]), ";{};".format(i[0]), i[1], i[2], i[3]))
        return hist_group

    ##########################################

    def GetIdxDet(self,detname):
        idx = -1
        if detname   == "random":
            idx = 0
        elif detname == "minosnd":
            idx = 2
        elif detname == "novand":
            idx = 3
        elif detname == "minosfd":
            idx = 8
        elif detname == "novafd":
            idx = 9
        else:
            print "Bad input, no detector found!"
            exit (1)
        return idx
