
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyhrv
import pyhrv.nonlinear as nl          
import neurokit2 as nk            
from scipy.stats import skew, kurtosis



def features(RR_interval, RR_interpolated):
    """features of time and frequency domain

    Args:
        RR_interval (array): rr intervals for extracting time features
        RR_interpolated (array): interpolated rr intervals for extracting frequency features

    Returns:
        pandas dataframe: a dataframe with all the features(columns) for a sample(row)
    """
      
    ## Time domain features
    # mean NN interval (muNN)
    muNN = np.mean(RR_interval)   
    # Standard deviation of a NNI series                       
    SDNN = pyhrv.time_domain.sdnn(RR_interval)
    # The root mean square of successive differences between normal heartbeats           
    RMSSD = pyhrv.time_domain.rmssd(RR_interval)   
    # The triangular index based on the NN interval histogram   
    TRindex = pyhrv.time_domain.triangular_index(nni=RR_interval, plot=False)  
    # Kurtosis
    kur = kurtosis(RR_interval) 
    # Skewness              
    skw = skew(RR_interval)                   
     # Approximate entropy(ApEn):amount of regularity and the unpredictability of fluctuations over time-series data 
    ApEn, parameters = nk.entropy_approximate(RR_interval)         
    
    # poincare(Lorenz) plot
    poincare_plot = nl.poincare(RR_interval,show=False, ellipse=False, vectors=False,legend=False)
    # Standard deviation along the minor axis
    SD1 = poincare_plot['sd1']  
    # Standard deviation along the major axis            
    SD2 = poincare_plot['sd2']  
    # Ratio between SD1 and SD2 (SD2/SD1)
    SDratio = poincare_plot['sd_ratio']     
    T  =  4 * SD1
    L = 4 * SD2
    # Cardiac sympathetic index
    CSI = L / T   
    # Modified cardiac sympathetic index               
    CSI_Modified = L ** 2 / T    
    # cardiac vagal index
    CVI = np.log10(L * T)        
    
    ## Frequency domain features(use interpolated rr for frequency features)
    fbands={'vlf': (0.01, 0.04), 'lf': (0.04, 0.2), 'hf': (0.2, 2)}
     # welch freq features
    welch_freq_features = pyhrv.frequency_domain.welch_psd(RR_interpolated,fbands, show=False, show_param=False, legend=False)       
    # Logarithmic power
    welch_log_powers=welch_freq_features['fft_log']   
    # LF/HF ratio      
    fftratio = welch_freq_features['fft_ratio']   
    # very low frequency power           
    welch_log_VLF = welch_log_powers[0] 
    # low frequency power
    welch_log_LF = welch_log_powers[1]  
    # high frequency power                     
    welch_log_HF = welch_log_powers[2]                       
    
    # Features dataframe 
    df_features_name = ['muNN', 'SDNN', 'RMSSD', 'TRindex', 'kurtosis', 'skewness', 'ApEn', 'LF/HF ratio', 'VLF power', 'LF  power', 'HF power', 'SD1','SD2', 'CSI_Modified', 'CVI', 'SD ratio']  
    df_features_value = np.column_stack((muNN, SDNN, RMSSD, TRindex, kur, skw, ApEn, fftratio, welch_log_VLF, welch_log_LF, welch_log_HF, SD1 , SD2, CSI_Modified, CVI, SDratio))    
    df_features = pd.DataFrame(data=df_features_value, columns=df_features_name )
    
    return df_features

