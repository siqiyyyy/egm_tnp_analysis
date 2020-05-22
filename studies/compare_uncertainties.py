import numpy as np
from matplotlib import pyplot as plt

inputFileName = {
        2017: "/home/syuan/projects/egm_tnp_analysis/results/Data2017/tnpPhoID_multibin/passingMediumV2/egammaEffi.txt_EGM2D.root",
        2018: "/home/syuan/projects/egm_tnp_analysis/results/Data2018/tnpPhoID_multibin/passingMediumV2/egammaEffi.txt_EGM2D.root",
        }
histName = "EGamma_SF2D"

def get_raw_pt_SF_unc(_eta_bin, year):
    filename = inputFileName[year]
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
            error = np.sqrt(unc_data**2 + unc_MC**2 + (eff_altBkg-eff_data)**2 + (eff_altSig-eff_data)**2 )/eff_MC
            ### append to map
            eta_bin = (eta_low, eta_high)
            if not eta_bin in eta_bins:
                eta_bins.append(eta_bin)
            pt_bin = (pt_low, pt_high)
            if not pt_bin in pt_bins:
                pt_bins.append(pt_bin)
            SFs[(eta_bin,pt_bin)] = (SF,error)
        ### create arrays
        x = []
        y = []
        xunc = []
        yunc = []
        if _eta_bin[0]==0:
            _eta_bin=eta_bins[0]
        else:
            _eta_bin=eta_bins[1]
        for pt_bin in pt_bins:
            x.append((pt_bin[0]+pt_bin[1])/2)
            y.append(SFs[(_eta_bin,pt_bin)][0])
            xunc.append((pt_bin[1]-pt_bin[0])/2)
            yunc.append(SFs[(_eta_bin,pt_bin)][1])
        return x,y,xunc,yunc

def get_SF_uncertainty(pt, eta, year, version):

    pt = np.array(pt, dtype=float)

    eta_bins = [(0.0,0.8), (0.8,1.4)]
    if not hasattr(eta, '__iter__'):
        if abs(eta)<0.8:
            eta = eta_bins[0]
        elif abs(eta)<1.4:
            eta = eta_bins[1]
        else:
            print("warning: eta out of measurement coverage")
            return (np.ones_like(pt),np.zeros_like(pt))
    else:
        if eta == (-0.8, 0.0):
            eta = eta_bins[0]
        elif eta == (-1.4, -0.8):
            eta = eta_bins[1]
        elif not eta in eta_bins:
            print("warning: invalid eta range")
            return (np.ones_like(pt),np.zeros_like(pt))

    if "new" in version:
        SF,unc={
            ((0.0,0.8),2017):   (1.019, 0.015),
            ((0.8,1.4),2017):   (1.015, 0.014),
            ((0.0,0.8),2018):   (1.017, 0.016),
            ((0.8,1.4),2018):   (1.013, 0.020)
            }[eta,year]
        SF = np.full_like(pt,SF)
        unc = np.full_like(pt,unc)

        if "extrapolation" in version and "systematics" in version:
            unc_gr = {
            ((0.0,0.8),2017):   7.767e-5,
            ((0.8,1.4),2017):   7.488e-5,
            ((0.0,0.8),2018):   6.354e-5,
            ((0.8,1.4),2018):   4.783e-5
            }[eta,year] * abs(pt-150)
            unc = np.sqrt(unc*unc + unc_gr*unc_gr)
            return (SF,unc)

        if "extrapolation" in version and not ("systematics" in version):
            unc_gr = {
            ((0.0,0.8),2017):   5.074e-5,
            ((0.8,1.4),2017):   6.976e-5,
            ((0.0,0.8),2018):   3.620e-5,
            ((0.8,1.4),2018):   4.470e-5
            }[eta,year] * abs(pt-150)
            unc = np.sqrt(unc*unc + unc_gr*unc_gr)
            return (SF,unc)
        
        unc = np.where(pt>300, 0.03, unc)
        return (SF,unc)

    if "EGamma" in version:
        SF,unc={
            ((0.0,0.8),2017):   (0.967, 0.080),
            ((0.8,1.4),2017):   (0.983, 0.150),
            ((0.0,0.8),2018):   (1.035, 0.060),
            ((0.8,1.4),2018):   (1.027, 0.075)
            }[eta,year]
        SF = np.full_like(pt,SF)
        unc = np.full_like(pt,unc)
        return (SF,unc)
    
    else:
        print("warning: invalid version name")
        return (np.ones_like(pt),np.zeros_like(pt))


'''
for year in [2017,2018]:
    for eta_bin in [(0.0,0.8),(0.8,1.4)]:
        fig, ax = plt.subplots(1,1)
        pt = np.linspace(200.,1400.,200)
        for version in ["EGamma", "new", "new with extrapolation"]:
            SF,unc = get_SF_uncertainty(pt,eta_bin,year,version)
            p = ax.plot(pt,SF, label=version)
            color = p[0].get_color()
            plt.fill_between(pt, SF-unc, SF+unc, alpha=0.2, facecolor=color, antialiased=True)
        ax.set_ylabel("scale factor")
        ax.set_xlabel("photon p_{T}")
        ax.set_ylim(0.9,1.15)
        ax.legend()
        ax.set_title("eta:"+str(eta_bin[0])+"~"+str(eta_bin[1])+" year:"+str(year))
        fig.savefig("output/compare_uncertainty_"+str(eta_bin[0])+"_"+str(eta_bin[1])+"_"+str(year)+".png")
'''

# same plot but plot also the SFs in the multibin measurement
for year in [2017,2018]:
    for eta_bin in [(0.0,0.8),(0.8,1.4)]:
        fig, ax = plt.subplots(1,1)
        pt = np.linspace(200.,1400.,200)
        for version in ["new with extrapolation"]:
            SF,unc = get_SF_uncertainty(pt,eta_bin,year,version)
            p = ax.plot(pt,SF, label="extrapolated SF&uncertainty")
            color = p[0].get_color()
            plt.fill_between(pt, SF-unc, SF+unc, alpha=0.2, facecolor=color, antialiased=True)
        # plot the scale factors
        x,y,xunc,yunc = get_raw_pt_SF_unc(eta_bin, year)
        ax.errorbar(x,y,xerr=xunc,yerr=yunc,label="measured SF",fmt='o')
        ax.set_ylabel("SF")
        ax.set_xlabel("photon $p_{T}$")
        ax.set_ylim(0.9,1.15)
        ax.legend()
        ax.set_title("eta:"+str(eta_bin[0])+"~"+str(eta_bin[1])+" year:"+str(year))
        fig.savefig("output/compare_uncertainty_withmultibinSF_"+str(eta_bin[0])+"_"+str(eta_bin[1])+"_"+str(year)+".png")

'''
# same plots but keep SF=1
for year in [2017,2018]:
    for eta_bin in [(0.0,0.8),(0.8,1.4)]:
        fig, ax = plt.subplots(1,1)
        pt = np.linspace(200.,1400.,200)
        for version in ["EGamma", "new", "new with extrapolation"]:
            SF,unc = get_SF_uncertainty(pt,eta_bin,year,version)
            SF = np.ones_like(SF)
            p = ax.plot(pt,SF, label=version)
            color = p[0].get_color()
            plt.fill_between(pt, SF-unc, SF+unc, alpha=0.2, facecolor=color, antialiased=True)
        ax.set_ylabel("scale factor")
        ax.set_xlabel("photon p_{T}")
        ax.set_ylim(0.9,1.15)
        ax.legend()
        ax.set_title("eta:"+str(eta_bin[0])+"~"+str(eta_bin[1])+" year:"+str(year))
        fig.savefig("output/compare_uncertainty_SF1_"+str(eta_bin[0])+"_"+str(eta_bin[1])+"_"+str(year)+".png")
'''
