#!/usr/bin/env python
"""
module with functions to enable logging
"""

import time,os,re,csv,sys,uuid,joblib
from datetime import date

LOG_DIR = os.path.join(".","logfiles")

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

def update_train_log(tag,period,rmse,runtime,MODEL_VERSION,MODEL_VERSION_NOTE,test=False):
    """
    update train log file
    """

    ## name the logfile using something that cycles with date (day, month, year)    
    today = date.today()
    if test:
        logfile = os.path.join(LOG_DIR,"train-test.log")
    else:
        logfile = os.path.join(LOG_DIR,"train-{}-{}.log".format(today.year, today.month))
        
    ## write the data to a csv file    
    header = ['unique_id','timestamp','tag','period','rmse','model_version',
              'model_version_note','runtime']
    write_header = False
    if not os.path.exists(logfile):
        write_header = True
    with open(logfile,'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(header)

        to_write = map(str,[uuid.uuid4(),time.time(),tag,period,rmse,
                            MODEL_VERSION,MODEL_VERSION_NOTE,runtime])
        writer.writerow(to_write)

def update_predict_log(country, y_pred,y_proba,target_date,runtime,MODEL_VERSION,test=False):
    """
    update predict log file
    """

    ## name the logfile using something that cycles with date (day, month, year)    
    today = date.today()
    if test:
        logfile = os.path.join(LOG_DIR,"predict-test.log")
    else:
        logfile = os.path.join(LOG_DIR,"predict-{}-{}.log".format(today.year, today.month))
        
    ## write the data to a csv file    
    header = ['unique_id','timestamp','country', 'y_pred','y_proba','target_date','model_version','runtime']
    write_header = False
    if not os.path.exists(logfile):
        write_header = True
    with open(logfile,'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(header)

        to_write = map(str,[uuid.uuid4(),time.time(),country,y_pred,y_proba,target_date,
                            MODEL_VERSION,runtime])
        writer.writerow(to_write)

        
if __name__ == "__main__":
    """
    basic test procedure for logger.py
    """
        
    print("Logger: Initializing Test Procedure")

    from model import MODEL_VERSION, MODEL_VERSION_NOTE
    
    print("Logger: Updating Train Log")
    ## train logger
    update_train_log("test_country", str((100,10)),"{'rmse':0.5}","00:00:01",
                     MODEL_VERSION, MODEL_VERSION_NOTE,test=True)
    
    print("Logger: Updating Predict Log")
    ## predict logger
    update_predict_log("test_country",[0.6,0.4],None,"2018/02/12",
                       "00:00:01",MODEL_VERSION, test=True)
    
    print("Logger: Finished Test Procedure")
        
