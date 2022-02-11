#!/usr/bin/env python

from ROOT import TH1F, TH2F, TFile

hists1D = [
    ("nanc", 30,  0, 30)
]
hists2D = [
    ("beam_vx_vs_vy",100 , -1, 1, 100, -1, 1)
]
hists = hists1D + hists2D

class Ancestor(object):
    def __init__(self,root_file,det):
        self.idxdet = self.GetIdxDet(det)
        self.thistag = "ancestor_" + det
        root_file.mkdir(self.thistag)
        self.thisgroup = self.book_hists()
        return

    ##########################################
    
    def fill(self, thisentry):
        wgt = (thisentry.dk2nu.decay.nimpwt)*(thisentry.dk2nu.nuray[self.idxdet].wgt) 
        #1D:
        self.thisgroup[0].Fill(thisentry.dk2nu.ancestor.size(),wgt)
        #2D:
        self.thisgroup[1].Fill(thisentry.dk2nu.ancestor[0].startx,thisentry.dk2nu.ancestor[0].starty,wgt)

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
            hist_group.append(    TH2F("{}_{}".format(self.thistag, i[0]), ";{};".format(i[0]), i[1], i[2], i[3],i[4], i[5], i[6]))
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
