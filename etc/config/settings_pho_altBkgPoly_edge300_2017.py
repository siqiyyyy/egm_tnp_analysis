#############################################################
########## General settings
#############################################################
# flag to be Tested
flags = {
    'passingMediumV2'  : '(passingCutBasedMedium100XV2 == 1)',
    }

baseOutDir = 'results/Data2017/tnpPhoID_newMC_edge300/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpPhoIDs'
samplesDef = {
    'data'   : tnpSamples.Data2017['data'].clone(),
    'mcNom'  : tnpSamples.Data2017['DY_madgraph'].clone(),
    'mcAlt'  : None,
    'tagSel' : tnpSamples.Data2017['DY_madgraph'].clone(),
}
## can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017C'] )
#samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017D'] )
#samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017E'] )
#samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017F'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 35')

## set MC weight, simple way (use tree weight) 
weightName = 'totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'ph_sc_eta' , 'type': 'float', 'bins': [-1.4442, -0.8, 0.0, 0.8, 1.4442] },
   { 'var' : 'ph_et' , 'type': 'float', 'bins': [200,300,1000] },
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.17 && event!=52007315' #cut out that one event with nan weight

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
}

#### or remove any additional cut (default)
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,90.]","betaP[0.04,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,90.]","betaF[0.04,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1.3,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1.3,0.5,5.0]",
    "acmsP[50.,40.,80.]","betaP[0.03,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0,85,95]",
    "acmsF[50.,40.,80.]","betaF[0.03,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0,85,95]",
    ]
     
tnpParAltBkgFit = [
    "meanP[1.19,-5.0,5.0]","sigmaP[0.74,0.5,5.0]",
    "meanF[1.03,-5.0,5.0]","sigmaF[2.22,0.5,5.0]",
    "linearP[1,0.001,100]","parabolicP[0,-1,1]",
    "linearF[1,0.001,100]","parabolicF[0,-50,50]",
    ]
        
