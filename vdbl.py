#!/usr/bin/env python

from ROOT import TH1F, TH2F, TFile

hists1D = []
hists2D = [
    ("par_enu_matH1IC",100,0,120,100,0,10),
    ("par_enu_matH2IC",100,0,120,100,0,10),
    ("par_enu_matDPIP",100,0,120,100,0,10),
    ("par_enu_matDVOL",100,0,120,100,0,10),
]

class Vdbl(object):
    def __init__(self,root_file,det):
        self.idxdet = self.GetIdxDet(det)
        self.thistag = "vdbl_" + det
        root_file.mkdir(self.thistag)
        self.thisgroup = self.book_hists()
        return

    ##########################################
    
    def fill(self, thisentry):
        wgt = (thisentry.dk2nu.decay.nimpwt)*(thisentry.dk2nu.nuray[self.idxdet].wgt)  
        enu = thisentry.dk2nu.nuray[self.idxdet].E
        self.thisgroup[0].Fill(enu,thisentry.dk2nu.vdbl[0],wgt)
        self.thisgroup[1].Fill(enu,thisentry.dk2nu.vdbl[3],wgt)
        self.thisgroup[2].Fill(enu,thisentry.dk2nu.vdbl[6],wgt)
        self.thisgroup[3].Fill(enu,thisentry.dk2nu.vdbl[9],wgt)

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
        for i in hists2D:
            hist_group.append(
                TH2F("{}_{}".format(self.thistag, i[0]), ";{};".format(i[0]), i[1], i[2], i[3], i[4], i[5], i[6]))
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
