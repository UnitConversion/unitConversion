dipoletype2draw = [
    ['Dipole', '35mm dipole magnet', 'DPL-3500'] ,
    ['Dipole G', '90mm dipole magnet', 'DPL-9000'] ,
]

quadtype2draw = [
    ['Quad A', '66mm, SNGL COIL, SHORT QUAD', 'QDP-9801'],
    ['Quad B', '66mm, SNGL COIL, SHORT QUAD', 'QDW-9802'],
    ['Quad C', '66mm, DBL COIL, LONG QUAD', 'QDP-9804'],
    ['Quad Cp', '66mm, LONG, DBL COIL KINKED QUAD', 'QDP-9807'],
    ['Quad D', '66mm, DBL COIL, SHORT QUAD', 'QDP-9809'],
    ['Quad D2', '66mm, DBL COIL, SHORT QUAD', 'QDP-9810'],
    ['Quad E', '66mm, DBL COIL, WIDE QUAD', 'QDW-9812'],
    ['Quad E2', '66mm, DBL COIL, WIDE QUAD', 'QDW-9813'],
    ['Quad F', '90mm, DBL COIL, SHORT QUAD', 'QDP-9815'],
]

sexttype2draw = [
    ['Sext A', '68mm, SHORT SEXTUPOLE', 'STP-9801'] ,
    ['Sext B', '68mm, SHORT, WIDE SEXTUPOLE', 'STP-9802'] ,
    ['Sext C', '76mm, LONG SEXTUPOLE', 'STP-9816'] ,
]

# Corr D is combined function Corrector with skew quadrupole, horizontal corrector, and vertical corrector.
cortype2draw = [
    ['Corr A', '156mm CORRECTOR', 'CRR-1560'],
    ['Corr C', '100mm CORRECTOR', 'CRR-1000'], 
    ['Corr D', '100mm SKEWED CORRECTOR', 'CRR-1001'],
    ['Corr Fast', 'FAST AIR CORE CORRECTOR', 'CRR-2000'],
]

hcortype2draw = [ 
    ['Corr A horizontal', '156mm horizontal corrector magnet sub-device', 'CRR-1560'] , # CRR-1203
    ['Corr C horizontal', '100mm horizontal corrector magnet sub-device', 'CRR-1000'] , #CRR-1201
    ['Corr D horizontal', '100mm horizontal skewed corrector magnet sub-device', 'CRR-1001'] , #CRR-1202
    ['Corr Fast horizontal', 'horizontal fast air core corrector magnet sub-device', 'CRR-2000'] ,
]

vcortype2draw = [
    ['Corr A vertical', '156mm vertical corrector magnet sub-device', 'CRR-1560'] ,
    ['Corr C vertical', '100mm vertical corrector magnet sub-device', 'CRR-1000'] ,
    ['Corr D vertical', '100mm vertical skewed corrector magnet sub-device', 'CRR-1001'] ,
    ['Corr Fast vertical', 'vertical  fast air core corrector magnet sub-device', 'CRR-2000'] ,
]

magneticleninst = {'Dipole': 2.62,
               'Dipole G': 2.62,
               'Quad A': 0.25,
               'Quad B': 0.25,
               'Quad C': 0.448,
               'Quad Cp': 0.448,
               'Quad D': 0.275,
               'Quad D2': 0.275,
               'Quad E': 0.275,
               'Quad E2': 0.275,
               'Quad F': 0.283,
               'Sext A': 0.22,
               'Sext B': 0.22,
               'Sext C': 0.25,
               'Corr A': 0.3,
               'Corr C': 0.2,
               'Corr D': 0.2,
               'Corr Fast': 0.044,
               'LN Quadrupole': 0.10,
               'LBT Dipole': 0.35,
               'LBT Quadrupole 1340': 0.25,
               'LBT Quadrupole 5200': 0.15,
               'BS Dipole BD1': 1.30,
               'BS Dipole BD2': 1.30,
               'BS Dipole BF': 1.24,
               'BS Quadrupole QF': 0.3,
               'BS Quadrupole QD': 0.3,
               'BS Quadrupole QG': 0.3,
               'BS Sextupole SF': 0.12,
               'BS Sextupole SD': 0.12,
               'BST Dipole': 1.40,
               'BST Quadrupole 5200': 0.35,
               }