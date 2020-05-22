import ROOT
import numpy as np
from tqdm import tqdm

ROOT.gROOT.SetBatch()

'''
from etc.inputs.tnpSampleDef import Data2017,Data2018
path_mc = {
        2017: Data2017['DY_madgraph'].path[0],
        2018: Data2018['DY_madgraph'].path[0],
        }

print("input files:")
print(path_mc[2017])
print(path_mc[2018])
'''
outdir = 'checkMCEff_output/'

def studycuts(year, treename, weight=None, ptName="ph_et", inputFileName=None, outputFileName=outdir+'histos.root'):
    ##### set up output
    outFile = ROOT.TFile.Open(outputFileName,"update")
    if not outFile:
        print("cannot open output file: "+outputFileName)
    titles = []
    binning = range(50,600,50) + [700, 800, 1000, 1200, 1500]
    binning = np.array(binning,dtype=float)
    all_cuts = ["PhoSingleTowerHadOverEmCut", "PhoFull5x5SigmaIEtaIEtaCut", "PhoAnyPFIsoWithEACut", "PhoAnyPFIsoWithEAAndQuadScalingCut", "PhoAnyPFIsoWithEACut1"]
    hEff_Single = {}
    hEff_NMinus1 = {}
    for cut in all_cuts:
        title = '_'.join([treename.split('/')[0], cut+"_Single", str(year)])
        titles.append(title)
        hEff_Single[cut] = ROOT.TEfficiency(title, cut+";p_{T};efficiency", len(binning)-1, binning)
        title = '_'.join([treename.split('/')[0], cut+"_NMinus1", str(year)])
        titles.append(title)
        hEff_NMinus1[cut] = ROOT.TEfficiency(title, cut+" N-1;efficiency;p_{T}", len(binning)-1, binning)
    ##### set up input
    if not inputFileName:
        inputFileName = path_mc[year]
    inFile = ROOT.TFile.Open(inputFileName)
    tree = inFile.Get(treename)
    Weight = np.zeros(1,dtype="float32")
    PT = np.zeros(1,dtype="float32")
    ETA = np.zeros(1,dtype="float32")
    IDs = {}
    for cut in all_cuts:
        IDs[cut] = np.zeros(1,dtype=bool)
        tree.SetBranchAddress("passingCutBasedMedium100XV2%s"%cut, IDs[cut])
    tree.SetBranchAddress(ptName, PT)
    tree.SetBranchAddress("ph_sc_eta", ETA) ## hard-coded for now TODO remove later
    if weight:
        tree.SetBranchAddress(weight, Weight)
    else:
        Weight[0]=1
    ##### loop tree
    nentries = tree.GetEntries()
    print("total entries: "+str(nentries))
    with tqdm(total=nentries) as pbar:
        for iEntry in range(nentries):
            tree.GetEvent(iEntry)
            pbar.update(1)
            if abs(ETA[0])>1.4442: continue ### only care about barrel photons
            for cut in all_cuts:
                Single_Bit = IDs[cut][0]
                NMinus1_Bit = 1
                for other_cut in all_cuts:
                    if other_cut == cut:
                        continue
                    NMinus1_Bit = NMinus1_Bit * IDs[other_cut][0]
                hEff_Single[cut].FillWeighted(Single_Bit,Weight[0],PT[0])
                hEff_NMinus1[cut].FillWeighted(NMinus1_Bit,Weight[0],PT[0])
    ##### wrap up
    inFile.Close()
    outFile.cd()
    for cut in all_cuts:
        hEff_Single[cut].Write("",ROOT.TFile.kWriteDelete)
        hEff_NMinus1[cut].Write("",ROOT.TFile.kWriteDelete)
    outFile.Close()
    print("single and N-1 histogram saved in file "+outputFileName)
    return titles

def readtree(year, treename, IDname, weight=None, ptName="ph_et", inputFileName=None, outputFileName=outdir+'histos.root'):
    ##### set up output
    outFile = ROOT.TFile.Open(outputFileName,"update")
    if not outFile:
        print("cannot open output file: "+outputFileName)
    title = '_'.join([treename.split('/')[0], IDname, str(year)])
    binning = range(50,600,50) + [700, 800, 1000, 1200, 1500]
    binning = np.array(binning,dtype=float)
    hEff = ROOT.TEfficiency(title, IDname+";p_{T};efficiency", len(binning)-1, binning)
    ##### set up input
    if not inputFileName:
        inputFileName = path_mc[year]
    inFile = ROOT.TFile.Open(inputFileName)
    tree = inFile.Get(treename)
    Weight = np.zeros(1,dtype="float32")
    PT = np.zeros(1,dtype="float32")
    ETA = np.zeros(1,dtype="float32")
    ID = np.zeros(1,dtype=bool)
    tree.SetBranchAddress(IDname, ID)
    tree.SetBranchAddress(ptName, PT)
    tree.SetBranchAddress("ph_sc_eta", ETA) ## hard-coded for now TODO remove later
    if weight:
        tree.SetBranchAddress(weight, Weight)
    else:
        Weight[0]=1
    ##### loop tree
    nentries = tree.GetEntries()
    print("total entries: "+str(nentries))
    with tqdm(total=nentries) as pbar:
        for iEntry in range(nentries):
            tree.GetEvent(iEntry)
            pbar.update(1)
            if abs(ETA[0])>1.4442: continue ### only care about barrel photons
            hEff.FillWeighted(ID[0],Weight[0],PT[0])
    ##### wrap up
    inFile.Close()
    outFile.cd()
    hEff.Write("",ROOT.TFile.kWriteDelete)
    outFile.Close()
    print("histogram "+title+" saved in file "+outputFileName)
    return title

def plot(histname, filepath=outdir+"histos.root"):
    inputFile = ROOT.TFile.Open(filepath)
    hist = inputFile.Get(histname)
    hdummy = ROOT.TH1F("hdummy",hist.GetTitle(),150,0,1500)
    hdummy.SetBinContent(0,0)
    hdummy.GetXaxis().SetTitle("p_{T}")
    hdummy.GetYaxis().SetTitle("efficiency")
    hdummy.GetYaxis().SetRangeUser(0.6,1.02)
    hdummy.Draw()
    canv = ROOT.TCanvas("canv","canv", 800, 800)
    hist.Draw("same")
    canv.Print(outdir+histname+".png")
    return 


#for year in [2017,2018]:
    #histname = readtree(year, 'tnpPhoIDs/fitter_tree', 'passingCutBasedMedium100XV2', weight='totWeight')
    #plot(histname)
    #histnames = studycuts(year, 'tnpPhoIDs/fitter_tree', weight='totWeight')
    #for histname in histnames:
    #    plot(histname)

titles = [ 'tnpPhoIDs_passingCutBasedMedium100XV2_2017','tnpPhoIDs_passingCutBasedMedium100XV2_2018', 'tnpPhoIDs_MinPtCut_Single_2017', 'tnpPhoIDs_MinPtCut_NMinus1_2017', 'tnpPhoIDs_PhoSCEtaMultiRangeCut_Single_2017', 'tnpPhoIDs_PhoSCEtaMultiRangeCut_NMinus1_2017', 'tnpPhoIDs_PhoSingleTowerHadOverEmCut_Single_2017', 'tnpPhoIDs_PhoSingleTowerHadOverEmCut_NMinus1_2017', 'tnpPhoIDs_PhoFull5x5SigmaIEtaIEtaCut_Single_2017', 'tnpPhoIDs_PhoFull5x5SigmaIEtaIEtaCut_NMinus1_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEACut_Single_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEACut_NMinus1_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEAAndQuadScalingCut_Single_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEAAndQuadScalingCut_NMinus1_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEACut1_Single_2017', 'tnpPhoIDs_PhoAnyPFIsoWithEACut1_NMinus1_2017', 'tnpPhoIDs_MinPtCut_Single_2018', 'tnpPhoIDs_MinPtCut_NMinus1_2018', 'tnpPhoIDs_PhoSCEtaMultiRangeCut_Single_2018', 'tnpPhoIDs_PhoSCEtaMultiRangeCut_NMinus1_2018', 'tnpPhoIDs_PhoSingleTowerHadOverEmCut_Single_2018', 'tnpPhoIDs_PhoSingleTowerHadOverEmCut_NMinus1_2018', 'tnpPhoIDs_PhoFull5x5SigmaIEtaIEtaCut_Single_2018', 'tnpPhoIDs_PhoFull5x5SigmaIEtaIEtaCut_NMinus1_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEACut_Single_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEACut_NMinus1_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEAAndQuadScalingCut_Single_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEAAndQuadScalingCut_NMinus1_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEACut1_Single_2018', 'tnpPhoIDs_PhoAnyPFIsoWithEACut1_NMinus1_2018']
for title in titles:
    plot(title)
