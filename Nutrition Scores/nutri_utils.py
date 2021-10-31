## The puprpose of this python file is to store functions related to nutrition score (SAIN LIM_original and modified)

#import libraries
import numpy as np
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
from wordcloud import WordCloud ,STOPWORDS
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def compute_sain(row, rv_dict):
    cal        = row['calories']
    ro_protein = (row['Protein (g)']/rv_dict['Protein'])*(100/cal)
    ro_fiber   = (row['Fiber (g)']/rv_dict['Fiber'])*(100/cal)
    ro_vitc    = (row['Vitamin C (mg)']/rv_dict['Vitamin C'])*(100/cal)
    ro_calcm   = (row['Calcium (mg)']/rv_dict['Calcium'])*(100/cal)
    ro_iron    = (row['Iron, Fe (mg)']/rv_dict['Iron'])*(100/cal)
    ro_vitd    = (row['Vitamin D (mcg)']/rv_dict['Vitamin D'])*(100/cal)
    
    ro_arr     = np.array([ro_protein, ro_fiber, ro_vitc, ro_calcm, ro_iron, ro_vitd])
    ro_arr[ro_arr==np.inf] = 0
    ro_arr       = ro_arr[~np.isnan(ro_arr)]
    ro_arr_sort  = np.sort(ro_arr)[::-1]
    ro_mean      = np.sum(ro_arr_sort[0:5])/5.0
    if pd.notnull(ro_mean):
        sain_mean    = ro_mean*100
        return (sain_mean)
    else:
        return(0)
    
def compute_lim(row, rv_dict):
    aisle       = row['aisle']
    ro_sugar    = (row['Sugars (g)']/rv_dict['Sugars'])*(100)
    ro_sodium   = (row['Sodium (mg)']/rv_dict['Sodium'])*(100)
    ro_satf     = (row['Saturated Fats (g)']/rv_dict['Saturated fatty acids'])*(100)
    ro_arr      = np.array([ro_sugar, ro_sodium, ro_satf])
    ro_arr[ro_arr==np.inf] = np.nan
    ro_arr       = ro_arr[~np.isnan(ro_arr)]
    ro_mean = np.sum(ro_arr)/3.0
    
    if pd.notnull(ro_mean):
        if aisle == 'soft drinks':
            ro_mean = ro_mean*2.5
        lim_mean    = ro_mean*100
        return (lim_mean)
    else:
        return(0)
    
def create_food_classes(score, thresholds):
    sain = score[0]#['SAIN log score']
    lim  = score[1]#['LIM log score']
    
    if sain >= thresholds[0] and lim < thresholds[1]:
        return 'class 1'
    elif sain < thresholds[0] and lim < thresholds[1]:
        return 'class 2'
    elif sain >= thresholds[0] and lim >= thresholds[1]:
        return 'class 3'
    elif sain < thresholds[0] and lim >= thresholds[1]:
        return 'class 4'
    else:
        return 'no class'
    
def compute_weighted_sain(row, rv_dict):
    cal        = row['calories']
    ro_protein = (row['Protein (g)']/rv_dict['Protein'])*(100/cal)
    ro_fiber   = (row['Fiber (g)']/rv_dict['Fiber'])*(100/cal)
    ro_vitc    = (row['Vitamin C (mg)']/rv_dict['Vitamin C'])*(100/cal)
    ro_calcm   = (row['Calcium (mg)']/rv_dict['Calcium'])*(100/cal)
    ro_iron    = (row['Iron, Fe (mg)']/rv_dict['Iron'])*(100/cal)
    ro_mn_fa   = (row['Fatty acids, total monounsaturated (mg)']/rv_dict['Monounsaturated fatty acids'])*(100/cal)
    ro_vitd    = (row['Vitamin D (mcg)']/rv_dict['Vitamin D'])*(100/cal)
    ro_vite    = (row['Vitamin E (Alpha-Tocopherol) (mg)']/rv_dict['Vitamin E'])*(100/cal)
    ro_thiam   = (row['Thiamin (B1) (mg)']/rv_dict['Thiamine'])*(100/cal)
    ro_ribo    = (row['Riboflavin (B2) (mg)']/rv_dict['Riboflavin'])*(100/cal)
    ro_niac    = (row['Niacin (B3) (mg)']/rv_dict['Niacin'])*(100/cal)
    ro_panto   = (row['Pantothenic acid (B5) (mg)']/rv_dict['Pantothenic acid'])*(100/cal)
    ro_vitb6   = (row['Vitamin B6 (mg)']/rv_dict['Vitamin B6'])*(100/cal)
    ro_fola    = (row['Folate (B9) (mcg)']/rv_dict['Folates'])*(100/cal)
    ro_reti    = (row['Retinol (mcg)']/rv_dict['Retinol'])*(100/cal)
    ro_bcar    = (row['Carotene, beta (mcg)']/rv_dict['Beta Carotene'])*(100/cal)
    ro_pota    = (row['Potassium, K (mg)']/rv_dict['Potassium'])*(100/cal)
    ro_magn    = (row['Magnesium (mg)']/rv_dict['Magnesium'])*(100/cal)
    ro_vitb12  = (row['Vitamin B-12 (mcg)']/rv_dict['Vitamin B12'])*(100/cal)
    ro_copr    = (row['Copper, Cu (mg)']/rv_dict['Copper'])*(100/cal)
    ro_zinc    = (row['Zinc, Zn (mg)']/rv_dict['Zinc'])*(100/cal)
    ro_sele    = (row['Selenium, Se (mcg)']/rv_dict['Selenium'])*(100/cal)
    ro_carb    = (row['Carbohydrates percent energy']/rv_dict['Carbohydrates'])*(100/cal)
    ro_vita    = (row['Vitamin A, IU (IU)']/rv_dict['Vitamin A'])*(100)

    ro_arr     = np.array([ro_protein, ro_fiber, ro_vitc, ro_calcm, ro_iron, ro_mn_fa, ro_vitd, ro_vite, ro_thiam, 
                           ro_ribo, ro_niac, ro_panto, ro_vitb6, ro_fola, ro_reti, ro_bcar, ro_pota, 
                            ro_magn, ro_vitb12, ro_copr, ro_zinc, ro_sele, ro_carb, ro_vita])
    ro_arr[ro_arr==np.inf] = np.nan
    ro_mean = np.nanmean(ro_arr)
    if pd.notnull(ro_mean):
        sain_mean    = ro_mean*100
        return (sain_mean)
    else:
        return(0)

def compute_weighted_lim(row, rv_dict):
    aisle       = row['aisle']
    ro_sugar    = (row['Sugars (g)']/rv_dict['Sugars'])*(100)
    ro_sodium   = (row['Sodium (mg)']/rv_dict['Sodium'])*(100)
    ro_satf     = (row['Saturated Fats (g)']/rv_dict['Saturated fatty acids'])*(100)
    ro_chole    = (row['Cholesterol (mg)']/rv_dict['Cholesterol'])*(100)
    ro_arr      = np.array([ro_sugar, ro_sodium, ro_satf, ro_chole])
    ro_arr[ro_arr==np.inf] = np.nan
    ro_mean = np.nanmean(ro_arr)
    if pd.notnull(ro_mean):
        if aisle == 'soft drinks':
            ro_mean = ro_mean*2.5
        lim_mean    = ro_mean*100
        return (lim_mean)
    else:
        return(0)

def plot_barplot(df, name, col_name, x_name):
    df = df[df.aisle == name]
    score_count = df[col_name].value_counts()
    plt.figure(figsize=(10,5))
    sns.barplot(score_count.index, score_count.values, alpha=0.8)
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.xlabel(x_name, fontsize=12)
    plt.xticks(rotation='vertical')
    plt.title(name)
    plt.show()
    
#missing value computation
def cal_missing_val(df):
    data_dict = {}
    for col in df.columns:
        data_dict[col] = (df[col].isnull().sum()/df.shape[0])*100
    return pd.DataFrame.from_dict(data_dict, orient='index', columns=['MissingValueInPercentage'])
