#!/usr/bin/env python

from ROOT import TH1F, TH2F, TFile
from math import *

hists1D = [
    ("tvz",      300,   -200.0,  100.0),
    ("tptype",  7000,   -3500.,  3500.)
]
hists2D = [
    ("tvx_vs_tvy",  100,    -1.5,   1.5, 100,  -8.0,   1.0),
    ("tpz_vs_tpt",  200,   -50.0,  150., 100,  -2.0,   8.0,),
]
hists = hists1D + hists2D

class Tgtexit(object):
    def __init__(self,root_file,det):
        self.idxdet = self.GetIdxDet(det)
        self.thistag = "tgtexit_" + det
        root_file.mkdir(self.thistag)
        self.thisgroup = self.book_hists()
        return

    ##########################################
    
    def fill(self, thisentry):
        wgt = (thisentry.dk2nu.decay.nimpwt)*(thisentry.dk2nu.nuray[self.idxdet].wgt)  
        self.thisgroup[0].Fill(thisentry.dk2nu.tgtexit.tvz,wgt)
        self.thisgroup[1].Fill(thisentry.dk2nu.tgtexit.tptype,wgt)
        self.thisgroup[2].Fill(thisentry.dk2nu.tgtexit.tvx,thisentry.dk2nu.tgtexit.tvy,wgt)
        tpt = sqrt(thisentry.dk2nu.tgtexit.tpx * thisentry.dk2nu.tgtexit.tpx + 
                   thisentry.dk2nu.tgtexit.tpy * thisentry.dk2nu.tgtexit.tpy )
        self.thisgroup[3].Fill(thisentry.dk2nu.tgtexit.tpz,tpt,wgt)
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

