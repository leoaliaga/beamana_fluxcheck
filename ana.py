#!/bin/env python

import sys
from decay import Decay
from ancestor import Ancestor
from tgtexit import Tgtexit
from nuray import Nuray
from vdbl import Vdbl
from ROOT import TChain, TFile

def load_Dk2Nu():
    from ROOT import gSystem, gInterpreter
    gSystem.Load("libCintex.so")
    from ROOT import Cintex
    Cintex.Enable()
    gSystem.Load("$DK2NU_LIB/libdk2nuTree.so")
    return

def process_list(fname, root_name):
    print "=> inputs to process_list: ", fname, root_name
    root_file = TFile(root_name, "RECREATE")
    load_Dk2Nu()
    detector = ["random", "minosnd", "novand", "minosfd", "novafd"]
    hist_decay = []
    hist_ancestor = []
    hist_tgtexit = []
    hist_nuray = []
    hist_vdbl = []
    for idet in range(len(detector)):
        hist_decay.append(Decay(root_file, detector[idet]))
        hist_ancestor.append(Ancestor(root_file, detector[idet]))
        hist_tgtexit.append(Tgtexit( root_file, detector[idet]))
        hist_nuray.append(Nuray( root_file, detector[idet]))
        hist_vdbl.append(Vdbl( root_file, detector[idet]))
        
    with open(fname, 'r') as flist:
        tchain = TChain('dk2nuTree')
        i = 0
        for iline in flist:
            ifile = iline.strip()
            print "=> fileIn : ",ifile
            tchain.Add(ifile)
            tn = tchain.GetEntries()
            tn_0_1 = tn/20
        print "=> entries: ",tn
        for entry in tchain:
            for idet in range(len(detector)):
                hist_decay[idet].fill(entry)
                hist_ancestor[idet].fill(entry)
                hist_tgtexit[idet].fill(entry)             
                hist_nuray[idet].fill(entry)             
                hist_vdbl[idet].fill(entry)             
            i += 1
            if i % tn_0_1==0:
                print round(100 * float(i) /float(tn)),"% of total events"
    for idet in range(len(detector)):
        hist_decay[idet].save(root_file)
        hist_ancestor[idet].save(root_file)
        hist_tgtexit[idet].save(root_file)
        hist_nuray[idet].save(root_file)
        hist_vdbl[idet].save(root_file)
    root_file.Close()
    return

