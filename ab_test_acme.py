'''
Created on Jul 10, 2014

@author: brun.julien@gmail.com
'''


import pandas as pd
from scipy import stats


#Constant
path = '/Users/Brun/workspace/auto_form/Data/airbnb_test/'
exp_file = 'experiment.csv'
country_file = 'country.csv'
country_list = ['CA','UK','US']

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_input(pathtofile, col_name = None):
    if col_name:
        df = pd.read_csv(pathtofile, names = col_name, header=None)
    else:
        df = pd.read_csv(pathtofile)
    return df   

def check_log(df):
    original_size = df.shape[0]
    df_clean_old = df[((df['landing_page']=='old_page') & (df['ab']=='control'))]
    df_clean_new = df[((df['landing_page']=='new_page') & (df['ab']=='treatment'))]
    cleaned_size_old = df_clean_old.shape[0]
    cleaned_size_new = df_clean_new.shape[0]
    cleaned_size_all = cleaned_size_old + cleaned_size_new
    print "original dataset size:" , original_size
    print "cleaned dataset size:" , cleaned_size_all
    print str(original_size - cleaned_size_all) + ' entries were not coherent between landing page type and a/b test category'
    return df_clean_old, df_clean_new
    
def counter(df, field_cat, value_cat, field_conv, value_conv):
    nb_entries = df.shape[0]
    converted = df[((df[field_cat] == value_cat) & (df[field_conv] == value_conv))].shape[0]
    percent = 100.0* converted/nb_entries
    print
    print value_cat + ': '+ str(converted) + ' / '+ str(nb_entries)
    print 'The conversion rate is {0:.2f} %'.format(percent)
    return percent       

def test_significance(s_old,s_new):
    '''mean_old = s_old.mean()
    sd_old = s_old.std()
    n_old = s_old.shape[0]
    mean_new = s_new.mean()
    sd_new = s_new.std()
    n_new = s_new.shape[0]
    z = (mean_new - mean_old) / (sd_old/n_old + sd_new/n_new)**(0.5)'''
    t, p = stats.ttest_ind(s_new , s_old, equal_var=False)  
    print "the t-score is " + str(t)
    
def country_count(dfc, version, country_in):
    page_type = version + '_page'
    df_country_count = dfc[dfc['landing_page']== page_type].groupby('country').count()
    dfc_converted = dfc[(dfc['converted']==1) & (dfc['landing_page']== page_type)].groupby('country').count()
    #print dfc_converted.converted[country_in], df_country_count.converted[country_in]   
    print version + ' converted {0:.2f} %'.format(100.0*dfc_converted.converted[country_in]/df_country_count.converted[country_in]) 
    return dfc[(dfc['landing_page']== page_type) & (dfc['country']==country_in)]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    
if __name__ == '__main__':

    #read input files
    df_e = read_input(path+exp_file)
    df_c_dupl = read_input(path+country_file)
    
    
    #check data quality
    df_verified_old, df_verified_new = check_log(df_e)
    df_c = df_c_dupl.drop_duplicates(cols='user_id')
    
    #Compute the percentage of change
    percent_old = counter(df_verified_old, 'landing_page', 'old_page', 'converted', 1)
    percent_new = counter(df_verified_new, 'landing_page', 'new_page', 'converted', 1)
    print
    print 'percentage of increase: {0:.2f} %'.format(100.0*(percent_new - percent_old)/percent_old)
    print

    test_significance(df_verified_old.converted,df_verified_new.converted)


    #Country
    df_country_old = pd.merge(df_verified_old, df_c, on ='user_id', how='left')
    df_country_new = pd.merge(df_verified_new, df_c, on ='user_id', how='left')
    
    for selected_country in country_list:
        print selected_country
        df_onecountry_old = country_count(df_country_old, 'old', selected_country)
        df_onecountry_new = country_count(df_country_new, 'new', selected_country)
        test_significance(df_onecountry_old.converted, df_onecountry_new.converted)


    
