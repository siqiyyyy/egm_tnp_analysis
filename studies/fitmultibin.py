import ROOT
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptFit(1111)
import numpy as np

inputFileName = {
        2017: "/home/syuan/projects/egm_tnp_analysis/results/Data2017/tnpPhoID_multibin/passingMediumV2/egammaEffi.txt_EGM2D.root",
        2018: "/home/syuan/projects/egm_tnp_analysis/results/Data2018/tnpPhoID_multibin/passingMediumV2/egammaEffi.txt_EGM2D.root",
        }
histName = "EGamma_SF2D"

def readtxt(filename):
    if "txt_EGM2D.root" in filename:
        filename = filename.replace("txt_EGM2D.root","txt")
    with open(filename) as fin:
        lines = fin.readlines()
        eta_bins = []
        pt_bins = []
        SFs = {}
        for line in lines:
            if "#" in line:
                line = line[:line.find('#')]
            line = line.replace(" ","").replace("\n","")
            if len(line) == 0: continue
            line = line.split("\t")
            eta_low = float(line[0])
            eta_high = float(line[1])
            pt_low = float(line[2])
            pt_high = float(line[3])
            eff_data = float(line[4])
            unc_data = float(line[5])
            eff_MC = float(line[6])
            unc_MC = float(line[7])
            eff_altBkg = float(line[8])
            eff_altSig = float(line[9])
            eff_altMC = float(line[10])
            eff_altSel = float(line[11])
            ### calculate SF and error
            SF = eff_data/eff_MC
            error = unc_data/eff_MC
            ### append to map
            eta_bin = (eta_low, eta_high)
            if not eta_bin in eta_bins:
                eta_bins.append(eta_bin)
            pt_bin = (pt_low, pt_high)
            if not pt_bin in pt_bins:
                pt_bins.append(pt_bin)
            SFs[(eta_bin,pt_bin)] = (SF,error)
        ### create TH2F
        eta_binning = [eta_bins[0][0]]
        for eta_bin in eta_bins:
            eta_binning.append(eta_bin[1])
        pt_binning = [pt_bins[0][0]]
        for pt_bin in pt_bins:
            pt_binning.append(pt_bin[1])
        eta_binning = np.array(eta_binning, dtype=float)
        pt_binning = np.array(pt_binning, dtype=float)
        h2d = ROOT.TH2F(histName,"SF2D with stat uncertainty", len(eta_binning)-1, eta_binning, len(pt_binning)-1, pt_binning)
        ### assign numbers to TH2F
        eta_bins = eta_bins[::-1]
        for ieta in range(1,len(eta_binning)):
            for ipt in range(1,len(pt_binning)):
                h2d.SetBinContent(ieta, ipt, SFs[(eta_bins[ieta-1],pt_bins[ipt-1])][0])
                h2d.SetBinError(ieta, ipt, SFs[(eta_bins[ieta-1],pt_bins[ipt-1])][1])
        return h2d
    return None



eta_binning = [0,0.8,1.4]

for year in [2017,2018]:
        #inputFile = ROOT.TFile.Open(inputFileName[year])
        #hist2D = inputFile.Get(histName)
        hist2D = readtxt(inputFileName[year])
        for ieta in range(1,len(eta_binning)):
                canv = ROOT.TCanvas("canv","canv",800,800)
                hist1D = hist2D.ProjectionY("h", ieta,ieta)
                f0 = ROOT.TF1("pol0","[0]")
                f1 = ROOT.TF1("pol1","[0]+[1]*(x-150)")
                hist1D.SetTitle(str(eta_binning[ieta-1])+"<#eta<"+str(eta_binning[ieta]) + " year:"+str(year))
                hist1D.Draw()
                hist1D.Fit(f0,"F")
                canv.Print("SFmultibin_statonly_"+str(year)+"_eta_"+str(eta_binning[ieta-1])+"_"+str(eta_binning[ieta])+"_fitpol0.png")
                hist1D.Fit(f1,"F")
                canv.Print("SFmultibin_statonly_"+str(year)+"_eta_"+str(eta_binning[ieta-1])+"_"+str(eta_binning[ieta])+"_fitpol1.png")
        #inputFile.Close()


