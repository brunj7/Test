'''
Created on Jul 10, 2014

@author: Brun
'''


import pandas as pd
from scipy import stats


def read_input(pathtofile, col_name = None):
    if col_name:
        df = pd.read_csv(pathtofile, names = col_name, header=None)
    else:
        df = pd.read_csv(pathtofile)
    return df   

def check_log(df):
    original_size = df.shape[0]
    df_clean = df[((df['landing_page']=='old_page') & (df['ab']=='control')) | ((df['landing_page']=='new_page') & (df['ab']=='treatment'))]
    cleaned_size = df_clean.shape[0]
    print "original dataset size:" , original_size
    print "cleaned dataset size:" , cleaned_size
    print str(original_size - cleaned_size) + ' entries were not coherent between landing page type and a/b test category'
    return df_clean
    
def counter(df, field_cat, value_cat, field_conv, value_conv):
    nb_entries = df.shape[0]
    converted = df[((df[field_cat] == value_cat) & (df[field_conv] == value_conv))].shape[0]
    percent = 100.0* converted/nb_entries
    
    print value_cat + ': '+ str(converted) + ' / '+ str(nb_entries)
    print '{0:.2f} %'.format(percent)
    return converted, percent

def country_count(country):
    print country
    print 'old converted {0:.2f} %'.format(100.0*df_converted_old.converted[country]/df_country_count.converted[country])
    print 'new converted {0:.2f} %'.format(100.0*df_converted_new.converted[country]/df_country_count.converted[country])                                                         
    
if __name__ == '__main__':
    path = '/Users/Brun/workspace/auto_form/Data/airbnb_test/'
    exp_file = 'experiment.csv'
    country_file = 'country.csv'
    
    #read input files
    df_e = read_input(path+exp_file)
    df_c = read_input(path+country_file)
    
    df_verified = check_log(df_e)
    
    nb_converted_old, percent_old = counter(df_verified, 'landing_page', 'old_page', 'converted', 1)
    nb_converted_new, percent_new = counter(df_verified, 'landing_page', 'new_page', 'converted', 1)
    
    print 'percentage of increase: {0:.2f} %'.format(100.0*(percent_new - percent_old)/percent_old)

    df_country = pd.merge(df_verified, df_c, on ='user_id')
    
    df_country_count = df_country.groupby('country').count()
    df_converted = df_country[df_country['converted']==1].groupby('country').count()
    df_converted_old = df_country[(df_country['converted']==1) & (df_country['landing_page']=='old_page')].groupby('country').count()
    df_converted_new = df_country[(df_country['converted']==1) & (df_country['landing_page']=='new_page')].groupby('country').count()
    
    country_count('CA')
    country_count('US')
    country_count('UK')
    

    
