from libPython.tnpClassUtils import tnpSample

eosDir = 'root://cmseos.fnal.gov//store/user/syuan/TnP/2020-03-23/'
Data2017 = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph'          : tnpSample('DY_madgraph',
                                       eosDir + 'merged_2017MC.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_madgraph_oldMC'          : tnpSample('DY_madgraph',
                                       'root://cmseos.fnal.gov//store/user/syuan/TnP/2020-04-23_oldMC/2017/merged_oldMC_filtered.root',
                                       isMC = True, nEvts =  -1 ),
    'data' : tnpSample('data_Run2017' , eosDir + 'merged_2017data.root' , lumi = 41.5 ),

    }

Data2018 = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph'          : tnpSample('DY_madgraph',
                                       eosDir + 'merged_2018MC.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_madgraph_oldMC'          : tnpSample('DY_madgraph',
                                       'root://cmseos.fnal.gov//store/user/syuan/TnP/2020-04-23_oldMC/2018/merged_oldMC.root',
                                       isMC = True, nEvts =  -1 ),
    'data' : tnpSample('data_Run2018' , eosDir + 'merged_2018data.root' , lumi = 59.7 ),

    }
