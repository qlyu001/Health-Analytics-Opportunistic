import pdb
import glob
import copy
import os
import pickle
import joblib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import sklearn.feature_selection

class FeatureColumn:
    def __init__(self, category, field, preprocessor, args=None, cost=None):
        self.category = category
        self.field = field
        self.preprocessor = preprocessor
        self.args = args
        self.data = None
        self.cost = cost

class NHANES:
    def __init__(self, db_path=None, columns=None):
        self.db_path = db_path
        self.columns = columns # Depricated
        self.dataset = None # Depricated
        self.column_data = None
        self.column_info = None
        self.df_features = None
        self.df_targets = None
        self.costs = None

    def process(self):
        df = None
        cache = {}
        # collect relevant data
        df = []
        for fe_col in self.columns:
            sheet = fe_col.category
            field = fe_col.field
            data_files = glob.glob(self.db_path+sheet+'/*.XPT')
            df_col = []
            for dfile in data_files:
                print(80*' ', end='\r')
                print('\rProcessing: ' + dfile.split('/')[-1], end='')
                # read the file
                if dfile in cache:
                    df_tmp = cache[dfile]
                else:
                    df_tmp = pd.read_sas(dfile)
                    cache[dfile] = df_tmp
                # skip of there is no SEQN
                if 'SEQN' not in df_tmp.columns:
                    continue
                #df_tmp.set_index('SEQN')
                # skip if there is nothing interseting there
                sel_cols = set(df_tmp.columns).intersection([field])
                if not sel_cols:
                    continue
                else:
                    df_tmp = df_tmp[['SEQN'] + list(sel_cols)]
                    df_tmp.set_index('SEQN', inplace=True)
                    df_col.append(df_tmp)

            try:
                df_col = pd.concat(df_col)
            except:
                #raise Error('Failed to process' + field)
                raise Exception('Failed to process' + field)
            df.append(df_col)
        df = pd.concat(df, axis=1)
        #df = pd.merge(df, df_sel, how='outer')
        # do preprocessing steps
        df_proc = []#[df['SEQN']]
        for fe_col in self.columns:
            field = fe_col.field
            fe_col.data = df[field].copy()
            # do preprocessing
            if fe_col.preprocessor is not None:
                prepr_col = fe_col.preprocessor(df[field], fe_col.args)
            else:
                prepr_col = df[field]
            # handle the 1 to many
            if (len(prepr_col.shape) > 1):
                fe_col.cost = [fe_col.cost] * prepr_col.shape[1]
            else:
                fe_col.cost = [fe_col.cost]
            df_proc.append(prepr_col)
        self.dataset = pd.concat(df_proc, axis=1)
        return self.dataset
        
# Preprocessing functions
def preproc_onehot(df_col, args=None):
    return pd.get_dummies(df_col, prefix=df_col.name, prefix_sep='#')

#Here I use mean std normalization
def preproc_real(df_col, args=None):
    if args is None:
        args={'cutoff':np.inf}
    #print(df_col)
    # other answers as nan
    df_col[df_col > args['cutoff']] = np.nan
    # nan replaced by mean
    df_col[pd.isna(df_col)] = df_col.mean()
    # statistical normalization
    df_col = (df_col-df_col.mean()) / df_col.std()
    return df_col

def preproc_impute(df_col, args=None):
    # nan replaced by mean
    df_col[pd.isna(df_col)] = df_col.mean()
    return df_col

def preproc_cut(df_col, bins):
    # limit values to the bins range
    df_col = df_col[df_col >= bins[0]]
    df_col = df_col[df_col <= bins[-1]]
    return pd.cut(df_col.iloc[:,0], bins, labels=False)

def preproc_dropna(df_col, args=None):
    df_col.dropna(axis=0, how='any', inplace=True)
    return df_col

#### Add your own preprocessing functions ####

# Dataset loader
class Dataset():
    """ 
    Dataset manager class
    """
    def  __init__(self, data_path=None):
        """
        Class intitializer.
        """
        # set database path
        if data_path == None:
            self.data_path = './run_data/'
        else:
            self.data_path = data_path
        # feature and target vecotrs
        self.features = None
        self.targets = None
        self.costs = None
        
    def load_arthritis(self, opts=None):
        columns = [
            #Demographics, Age in years at screening
            FeatureColumn('Demographics', 'RIDAGEYR',
                                            preproc_real, {'cutoff':80}),
            #Demographics, Race/Hispanic
            FeatureColumn('Demographics', 'RIDRETH3',
                                            preproc_real, {'cutoff':7}),
            #Demographics, Served active duty in the armed forces
            FeatureColumn('Demographics', 'DMQMILIZ',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Served in a foreign country
            FeatureColumn('Demographics', 'DMQADFC',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Country of birth
            FeatureColumn('Demographics', 'DMDBORN4',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Citizenship status
            FeatureColumn('Demographics', 'DMDCITZN',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Length of time in the US
            FeatureColumn('Demographics', 'DMDYRSUS',
                                            preproc_real, {'cutoff':9}),
            #Demographics, Education level, Youth 6-19
            FeatureColumn('Demographics', 'DMDEDUC3',
                                            preproc_real, {'cutoff':66}),
            #Demographics, Education level, Adults 20+
            FeatureColumn('Demographics', 'DMDEDUC2',
                                            preproc_real, {'cutoff':5}),
            #Demographics, Education level, Language at SP interview
            FeatureColumn('Demographics', 'SIALANG',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Education level, Language at Family Interview
            FeatureColumn('Demographics', 'FIALANG',
                                            preproc_onehot, {'cutoff':2}),
            #Demographics, Total number of people in household
            FeatureColumn('Demographics', 'DMDHHSIZ',
                                            preproc_real, {'cutoff':7}),
            #Demographics, Total number of children 5 years or younger in household
            FeatureColumn('Demographics', 'DMDHHSZA',
                                            preproc_real, {'cutoff':3}),
            #Demographics, Total number of adults 60+ in household
            FeatureColumn('Demographics', 'DMDHHSZE',
                                            preproc_real, {'cutoff':3}),
            #Demographics, Annual household income
            FeatureColumn('Demographics', 'INDHHIN2',
                                            preproc_real, {'cutoff':15}),
            #Demographics, Annual family income
            FeatureColumn('Demographics', 'INDFMIN2',
                                            preproc_real, {'cutoff':15}),
            #Demographics, Ratio of annual income to poverty
            FeatureColumn('Demographics', 'INDFMPIR',
                                            preproc_real, {'cutoff':5}),
            # TARGET: systolic BP average
            FeatureColumn('Questionnaire', 'MCQ220', 
                                    None, None), 
            #Laboratory, HPV Vaginal swab- high risk
            FeatureColumn('Laboratory', 'LBXHP2C',
                                            preproc_onehot, {'cutoff':2}),
            #Laboratory, HPV Vaginal swab- HPV type 16 and 18 for cervical cancer
            FeatureColumn('Laboratory', 'LBDR16',
                                            preproc_onehot, {'cutoff':2}),
            FeatureColumn('Laboratory', 'LBDR18',
                                            preproc_onehot, {'cutoff':2}),
            #Laboratory, Hepatitus B and C -liver cancer risk
            FeatureColumn('Laboratory', 'LBXHBC',
                                            preproc_onehot, {'cutoff':2}),
            FeatureColumn('Laboratory', 'LBXHCR',
                                            preproc_onehot, {'cutoff':2}),
            #Laboratory, Hemoglobin
            FeatureColumn('Laboratory', 'LBXHGB',
                                            preproc_real, {'cutoff':19.2}),
            #Laboratory, White blood cell count
            FeatureColumn('Laboratory', 'LBXWBCSI',
                                            preproc_real, {'cutoff':117.2}),
            #Laboratory, Phthalate
            FeatureColumn('Laboratory', 'URXCNP',
                                            preproc_real, {'cutoff':246}),
            #Laboratory, Platelet count
            FeatureColumn('Laboratory', 'LBXPLTSI',
                                            preproc_real, {'cutoff':777}),
            #Laboratory, Albumin, urine (ug/mL)
            FeatureColumn('Laboratory', 'URXUMA',
                                            preproc_real, {'cutoff':9730}),
            #Laboratory, Alanine aminotransferase
            FeatureColumn('Laboratory', 'LBXSATSI',
                                            preproc_real, {'cutoff':319}),
            #Laboratory, Aspartate aminotransferase
            FeatureColumn('Laboratory', 'LBXSASSI',
                                            preproc_real, {'cutoff':832}),
            #Laboratory, Alkaline phosphatase
            FeatureColumn('Laboratory', 'LBXSAPSI',
                                            preproc_real, {'cutoff':740}),
            #Laboratory, Bicarbonate
            FeatureColumn('Laboratory', 'LBXSC3SI',
                                            preproc_real, {'cutoff':34}),
            #Laboratory, Total Bilirubin
            FeatureColumn('Laboratory', 'LBXSTB',
                                            preproc_real, {'cutoff':3.5}),
            #Laboratory, Blood lead
            FeatureColumn('Laboratory', 'LBXBPB',
                                            preproc_real, {'cutoff':23.51}),
            #Laboratory, Blood mercury
            FeatureColumn('Laboratory', 'LBXIHG',
                                            preproc_real, {'cutoff':5.9}),
            #Laboratory, Blood urea nitrogen
            FeatureColumn('Laboratory', 'LBXSBU',
                                            preproc_real, {'cutoff':96}),
            #Laboratory, Chloride
            FeatureColumn('Laboratory', 'LBXSCLSI',
                                            preproc_real, {'cutoff':117}),
            #Laboratory, Chlamydia
            FeatureColumn('Laboratory', 'URXUCL',
                                            preproc_onehot, {'cutoff':2}),
            #Examination, Weight
            FeatureColumn('Examination', 'BMXWT',
                                            preproc_real, {'cutoff':198}),
            #Examination, Waist Circumference
            FeatureColumn('Examination', 'BMXWAIST',
                                            preproc_real, {'cutoff':171}),
            #Examination, BMI
            FeatureColumn('Examination', 'BMXBMI',
                                            preproc_real, {'cutoff':67.3}),
            #Examination, Pulse irregular?
            FeatureColumn('Examination', 'BPXPULS',
                                            preproc_onehot, {'cutoff':2}),
            #Examination, Systolic Blood Pressure
            FeatureColumn('Examination', 'BPXSY1',
                                            preproc_real, {'cutoff':236}),
            #Examination, Diastolic Blood Pressure
            FeatureColumn('Examination', 'BPXDI1',
                                            preproc_real, {'cutoff':120}),
            #Examination, Dental implant?
            FeatureColumn('Examination', 'OHXIMP',
                                            preproc_onehot, {'cutoff':2}),
            #Examination, Gum Disease?
            FeatureColumn('Examination', 'OHAROCGP',
                                            preproc_onehot, {'cutoff':2}),
            #Examination, Oral Hygiene
            FeatureColumn('Examination', 'OHAROCOH',
                                            preproc_onehot, {'cutoff':2}),
            #Examination, Decayed teeth
            FeatureColumn('Examination', 'OHAROCDT',
                                            preproc_onehot, {'cutoff':2}),

            #Questionnaire
            #ALQ101 - Had at least 12 alcohol drinks/1 yr?
            FeatureColumn('Questionnaire', 'ALQ101', 
                                            preproc_onehot, {'cutoff':2}),

            #ALQ110 - Had at least 12 alcohol drinks/lifetime?
            FeatureColumn('Questionnaire', 'ALQ110', 
                                            preproc_onehot, {'cutoff':2}),

            #ALQ120Q - How often drink alcohol over past 12 mos
            FeatureColumn('Questionnaire', 'ALQ120Q', 
                                            preproc_real, {'cutoff':365}),

            #ALQ120U - # days drink alcohol per wk, mo, yr
            FeatureColumn('Questionnaire', 'ALQ120U', 
                                            preproc_real, {'cutoff':3}),
            #ALQ151 - Ever have 4/5 or more drinks every day?
            FeatureColumn('Questionnaire', 'ALQ151', 
                                            preproc_onehot, {'cutoff':2}),
            #ALQ160 - # days have 4/5 or more drinks in 2 hrs
            FeatureColumn('Questionnaire', 'ALQ160', 
                                            preproc_real, {'cutoff':20}),
            #AUQ054 - General condition of hearing
            FeatureColumn('Questionnaire', 'AUQ054', 
                                            preproc_real, {'cutoff':6}),
            #AUQ060 - Hear a whisper from across a quiet room?
            FeatureColumn('Questionnaire', 'AUQ060', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ070 - Hear normal voice across a quiet room?
            FeatureColumn('Questionnaire', 'AUQ070', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ090 - Hear if spoken loudly to in better ear?
            FeatureColumn('Questionnaire', 'AUQ090', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ100 - Difficult follow conversation if noise
            FeatureColumn('Questionnaire', 'AUQ100', 
                                            preproc_real, {'cutoff':5}),
            #AUQ110 - Hearing cause frustration when talking?
            FeatureColumn('Questionnaire', 'AUQ110', 
                                            preproc_real, {'cutoff':5}),
            #AUQ136 - Ever had 3 or more ear infections?
            FeatureColumn('Questionnaire', 'AUQ136', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ138 - Ever had tube placed in ear?
            FeatureColumn('Questionnaire', 'AUQ138', 
                                            preproc_onehot, {'cutoff':2}),
            #AUD148 - Hearing aid or Cochlear implant?
            FeatureColumn('Questionnaire', 'AUD148', 
                                            preproc_onehot, {'cutoff':3}),
            #AUQ154 - Ever used assistive listening devices?
            FeatureColumn('Questionnaire', 'AUQ154', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ250 - How long bothered by ringing, roaring
            FeatureColumn('Questionnaire', 'AUQ250', 
                                            preproc_real, {'cutoff':5}),
            #AUQ260 - Bothered by ringing after loud sounds?
            FeatureColumn('Questionnaire', 'AUQ260', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ270 - Bothered by ringing when going to sleep
            FeatureColumn('Questionnaire', 'AUQ270', 
                                            preproc_onehot, {'cutoff':2}),
            #AUQ340 - How long exposed to loud noise at work?
            FeatureColumn('Questionnaire', 'AUQ340', 
                                            preproc_real, {'cutoff':7}),
            #AUQ350 - Ever exposed to very loud noise at work?
            FeatureColumn('Questionnaire', 'AUQ350', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ020 - Ever told you had high blood pressure
            FeatureColumn('Questionnaire', 'BPQ020', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ030 - Told had high blood pressure - 2+ times
            FeatureColumn('Questionnaire', 'BPQ030', 
                                            preproc_onehot, {'cutoff':2}),
            #BPD035 - Age told had hypertension
            FeatureColumn('Questionnaire', 'BPD035', 
                                            preproc_real, {'cutoff':80}),
            #BPQ040A - Taking prescription for hypertension
            FeatureColumn('Questionnaire', 'BPQ040A', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ050A - Now taking prescribed medicine for HBP
            FeatureColumn('Questionnaire', 'BPQ050A', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ080 - Doctor told you - high cholesterol level
            FeatureColumn('Questionnaire', 'BPQ080', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ090D - Told to take prescriptn for cholesterol
            FeatureColumn('Questionnaire', 'BPQ090D', 
                                            preproc_onehot, {'cutoff':2}),
            #BPQ100D - Now taking prescribed medicine
            FeatureColumn('Questionnaire', 'BPQ100D', 
                                            preproc_onehot, {'cutoff':2}),
            #CDQ001 - SP ever had pain or discomfort in chest
            FeatureColumn('Questionnaire', 'CDQ001', 
                                            preproc_onehot, {'cutoff':2}),
            #CDQ006 - How soon is the pain relieved
            FeatureColumn('Questionnaire', 'CDQ006', 
                                            preproc_onehot, {'cutoff':2}),

            #CDQ008 - Severe pain in chest more than half hour
            FeatureColumn('Questionnaire', 'CDQ008', 
                                            preproc_onehot, {'cutoff':2}),
            #CDQ010 - Shortness of breath on stairs/inclines
            FeatureColumn('Questionnaire', 'CDQ010', 
                                            preproc_onehot, {'cutoff':2}),
            #CBD121 - Money spent on eating out
            FeatureColumn('Questionnaire', 'CBD121', 
                                            preproc_real, {'cutoff':8400}),
            #HSD010 - General health condition
            FeatureColumn('Questionnaire', 'HSD010', 
                                            preproc_real, {'cutoff':5}),
            #HSQ500 - SP have head cold or chest cold
            FeatureColumn('Questionnaire', 'HSQ500', 
                                            preproc_onehot, {'cutoff':2}),
            #HSQ510 - SP have stomach or intestinal illness?
            FeatureColumn('Questionnaire', 'HSQ510', 
                                            preproc_onehot, {'cutoff':2}),
            #HSQ590 - Blood ever tested for HIV virus?
            FeatureColumn('Questionnaire', 'HSQ590', 
                                            preproc_onehot, {'cutoff':2}),
            #DED031 - Skin reaction to sun after non-exposure
            FeatureColumn('Questionnaire', 'DED031', 
                                                preproc_real, {'cutoff':5}),
            #DEQ034A - Stay in the shade?
            FeatureColumn('Questionnaire', 'DEQ034A', 
                                                preproc_real, {'cutoff':6}),
            #DEQ034D - Use sunscreen?
            FeatureColumn('Questionnaire', 'DEQ034D', 
                                                preproc_real, {'cutoff':5}),
            #DEQ038Q - # of times in past yr you had a sunburn
            FeatureColumn('Questionnaire', 'DEQ038Q', 
                                                preproc_real, {'cutoff':20}),
            #DED120 - Minutes outdoors 9am - 5pm work day
            FeatureColumn('Questionnaire', 'DED120', 
                                                preproc_real, {'cutoff':480}),
            #DED125 - Minutes outdoors 9am - 5pm not work day
            FeatureColumn('Questionnaire', 'DED125', 
                                                preproc_real, {'cutoff':480}),
            #DIQ010 - Doctor told you have diabetes
            FeatureColumn('Questionnaire', 'DIQ010', 
                                                preproc_real, {'cutoff':3}),
            #DID040 - Age when first told you had diabetes
            FeatureColumn('Questionnaire', 'DID040', 
                                                preproc_real, {'cutoff':80}),
            #DIQ160 - Ever told you have prediabetes
            FeatureColumn('Questionnaire', 'DIQ160', 
                                                preproc_onehot, {'cutoff':2}),
            #DIQ170 - Ever told have health risk for diabetes
            FeatureColumn('Questionnaire', 'DIQ170', 
                                                preproc_onehot, {'cutoff':2}),
            #DIQ172 - Feel could be at risk for diabetes
            FeatureColumn('Questionnaire', 'DIQ172', 
                                                preproc_onehot, {'cutoff':2}),



            #SLD012 - Sleep Hours
            FeatureColumn('Questionnaire', 'SLD012', 
                                            preproc_real, {'cutoff':14.5}),
            # SMQ020 - Smoking
            FeatureColumn('Questionnaire', 'SMQ020', 
                                            preproc_onehot, None),


            
        ]
        nhanes_dataset = NHANES(self.data_path, columns)
        #print(nhanes_dataset)
        df = nhanes_dataset.process()
        #print(df)
        fe_cols = df.drop(['MCQ220'], axis=1)
        features = fe_cols.values
        target = df['MCQ220'].values
        # remove nan labeled samples
        inds_valid = ~ np.isnan(target)
        features = features[inds_valid]
        target = target[inds_valid]

        # Put each person in the corresponding bin
        targets = np.zeros(target.shape[0])
        targets[target == 1] = 0 # yes cancer
        targets[target == 2] = 1 # no cancer

       # random permutation
        perm = np.random.permutation(targets.shape[0])
        self.features = features[perm]
        self.targets = targets[perm]
        self.costs = [c.cost for c in columns[1:]]
        self.costs = np.array(
            [item for sublist in self.costs for item in sublist])
        
        
    #### Add your own dataset loader ####
