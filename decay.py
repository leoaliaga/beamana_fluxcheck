#!/usr/bin/env python

from ROOT import TH1F, TH2F, TFile
from math import *

hists1D = [
    ("ndecay",   16,     -0.5,  15.5),
    ("ntype",    31,    -15.5,  15.5),    
    ("ptype", 7000,   -3500.,  3500.),
    ("nimpwt",100,       0.,    50.),
    ("vz",    1000, -10000.0,  90000.0)
]
hists2D = [
    ("vx_vs_vy", 100,  -500.0,   500., 100,  -500.0,   500.0), 
    ("pdpz_vs_pdpt",100,  0, 60., 100,  0, 1.0), 
    ("pppz_vs_pppt",100,  0, 60., 100,  0, 1.0),
]
hists = hists1D + hists2D

class Decay(object):
    def __init__(self,root_file,det):
        self.idxdet = self.GetIdxDet(det)
        self.thistag = "decay_" + det
        root_file.mkdir(self.thistag)
        self.thisgroup = self.book_hists()
        return

    ##########################################
    
    def fill(self, thisentry):
        wgt = (thisentry.dk2nu.decay.nimpwt)*(thisentry.dk2nu.nuray[self.idxdet].wgt)  
        #1D:
        self.thisgroup[0].Fill(thisentry.dk2nu.decay.ndecay, wgt)
        self.thisgroup[1].Fill(thisentry.dk2nu.decay.ntype,  wgt)
        self.thisgroup[2].Fill(thisentry.dk2nu.decay.ptype,  wgt)
        self.thisgroup[3].Fill(thisentry.dk2nu.decay.nimpwt,wgt)
        self.thisgroup[4].Fill(thisentry.dk2nu.decay.vz,wgt)
        #2D:
        self.thisgroup[5].Fill(thisentry.dk2nu.decay.vx,thisentry.dk2nu.decay.vy,wgt)
        pdpt = sqrt( thisentry.dk2nu.decay.pdpx* thisentry.dk2nu.decay.pdpx + 
                     thisentry.dk2nu.decay.pdpy * thisentry.dk2nu.decay.pdpy ) 
        self.thisgroup[6].Fill(thisentry.dk2nu.decay.pdpz,pdpt, wgt)
        pppt = thisentry.dk2nu.decay.pppz * sqrt( thisentry.dk2nu.decay.ppdxdz* thisentry.dk2nu.decay.ppdxdz  + 
                                                    thisentry.dk2nu.decay.ppdydz* thisentry.dk2nu.decay.ppdydz )
        self.thisgroup[7].Fill(thisentry.dk2nu.decay.pppz,pppt, wgt)
        
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
            hist_group.append(TH1F("{}_{}".format(self.thistag, i[0]), ";{};".format(i[0]), i[1], i[2], i[3]))
        for i in hists2D:
            hist_group.append(TH2F("{}_{}".format(self.thistag, i[0]), ";{};".format(i[0]), i[1], i[2], i[3], i[4], i[5], i[6]))
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
