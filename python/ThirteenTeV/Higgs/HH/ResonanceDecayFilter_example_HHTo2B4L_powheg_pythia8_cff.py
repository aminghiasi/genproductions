import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/afs/cern.ch/work/a/acarvalh/public/GridPacks_HH/13TeV/GF_HH_NonRes_SM_NLO/ggHH_slc6_amd64_gcc630_CMSSW_9_3_0_my_ggHH.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 2',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
                        '23:mMin = 0.05',
                        '23:onMode = off',
                        '23:onIfAny = 11 13 15', # only leptonic Z decays
                        '25:m0 = 125.0',
                        '25:onMode = off',
                        '25:onIfMatch = 5 -5',
                        '25:onIfMatch = 23 23',
                        'ResonanceDecayFilter:filter = on',
                        'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
                        'ResonanceDecayFilter:eMuAsEquivalent = off', #on: treat electrons and muons as equivalent
                        'ResonanceDecayFilter:eMuTauAsEquivalent = on', #on: treat electrons, muons , and taus as equivalent
                        'ResonanceDecayFilter:allNuAsEquivalent = off', #on: treat all three neutrino flavours as equivalent
                        'ResonanceDecayFilter:mothers = 25,23', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
                        'ResonanceDecayFilter:daughters = 5,5,11,11,11,11',
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
