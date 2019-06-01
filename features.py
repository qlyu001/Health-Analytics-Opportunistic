#adding lab
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
            #Laboratory, Arsenic in urine
            #FeatureColumn('Laboratory', 'URXUAS5',
                                            #preproc_real, {'cutoff':4.54}),
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

            #adding examination
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

            #Question
            FeatureColumn('Questionnaire', 'DIQ175T', 
                                   preproc_real, None),
            
            #DIQ175Q - Doctor warning
            FeatureColumn('Questionnaire', 'DIQ175Q', 
                                   preproc_real, None),
            #DIQ175O - Increased fatigue
            FeatureColumn('Questionnaire', 'DIQ175O', 
                                   preproc_real, None),
            #DIQ175N - Blurred vision
            FeatureColumn('Questionnaire', 'DIQ175N', 
                                   preproc_real, None),
            #DIQ175M - Tingling/numbness in hands or feet
            FeatureColumn('Questionnaire', 'DIQ175M', 
                                   preproc_real, None),

            #DIQ175D - Poor diet
            FeatureColumn('Questionnaire', 'DIQ175D', 
                                            preproc_real, None),
            #DIQ175E - Race
            FeatureColumn('Questionnaire', 'DIQ175E', 
                                            preproc_real, None),
            #DIQ175G - Lack of physical activity
            FeatureColumn('Questionnaire', 'DIQ175G', 
                                            preproc_real, None),
            #DIQ175H - High blood pressure
            FeatureColumn('Questionnaire', 'DIQ175H', 
                                            preproc_real, None),
            #DIQ175I - High blood sugar
            FeatureColumn('Questionnaire', 'DIQ175I', 
                                            preproc_real, None),
            #DIQ175J - High cholesterol
            FeatureColumn('Questionnaire', 'DIQ175J', 
                                            preproc_real, None),

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
            #DIQ175B - Overweight
            FeatureColumn('Questionnaire', 'DIQ175B', 
                                            preproc_real, None),
