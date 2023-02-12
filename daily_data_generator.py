import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#when run code, remember to change the following locations, becareful with "/" 
score_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/scores.csv"
control_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/control/"+"control_"
condition_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/condition/"+"condition_"
output_file_saving_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/"

delta_t = 10 #this means corsaring the data by averaging the data over this time interval
def zero_remover(daily_activity):
    counts = daily_activity.value_counts()
    werid = counts.max()
    if werid > len(daily_activity)*0.8:
        return False
    else:
        return True

def daily_data_averager(daily_data, time_interval_in_minute):
    """
    time_interval_in_minute needs to be an integer
    """
    daily = daily_data.to_numpy()
    avg_daily_data = daily.reshape(-1, time_interval_in_minute).mean(axis=1)

    return(avg_daily_data)


def daily_data_generator_condition(j, time_interval_in_minute):
    #load file and convert the timestamp from string to date
    test_file = pd.read_csv(condition_location+str(j)+".csv")
    score_file = pd.read_csv(score_location)
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])
    #normalize the activity data
    test_file["activity"] = test_file["activity"]*1000/test_file["activity"].max()

    #find all the timestamps at 0:00
    test_file["hour"] = test_file["timestamp"].dt.hour
    test_file["minute"] = test_file["timestamp"].dt.minute
    day_splitter = test_file[(test_file["hour"]==0) & (test_file["minute"]==0)].index

    #split the data by day. Here we only take days with data from 0:00-23:59. So we discard the first and last day
    extract_first_day = test_file["activity"].loc[day_splitter[0]:day_splitter[1]-1]
    daily_motion_j = pd.DataFrame()
    daily_motion_j[0] = daily_data_averager(extract_first_day, time_interval_in_minute)
    daily_motion_j.reset_index()

    for i in range(1, len(day_splitter)-1):
        start = day_splitter[i]
        end = day_splitter[i+1]
        extract_day_activity = test_file["activity"].loc[start:end-1]
        if zero_remover(extract_day_activity):
            #extract_day_time = temp[0]
            try:
                daily_motion_j[i-1] = daily_data_averager(extract_day_activity, time_interval_in_minute)
            except ValueError:
                pass
        else:
            pass
        
    daily_motion_j.reset_index()
    daily_motion_j = daily_motion_j.transpose()
    daily_motion_j.columns = [str(i) for i in range(0, daily_motion_j.shape[1])]

    #add time 
    #temp = test_file["timestamp"].iloc[day_splitter]
    #daily_motion_j["Time"] = temp.dt.date.iloc[1:-1].to_list()
    #first_column = daily_motion_j.pop('Time')
    #daily_motion_j.insert(0, "Time", first_column)

    #add other attributes from scores.csv into the daily acitivity dataframe 
    temp_row_index = score_file.index[score_file["number"] == "condition_"+str(j)]
    temp_row = score_file.iloc[temp_row_index]
    daily_motion_j["age"] = np.repeat(temp_row.iloc[0, 3], daily_motion_j.shape[0])
    daily_motion_j["gender"] = np.repeat(temp_row.iloc[0, 2], daily_motion_j.shape[0])
    daily_motion_j["mental_disorder"] = np.repeat(temp_row.iloc[0, 4], daily_motion_j.shape[0])
    daily_motion_j["melanch"] = np.repeat(temp_row.iloc[0, 5], daily_motion_j.shape[0])
    daily_motion_j["inpatient"] = np.repeat(temp_row.iloc[0, 6], daily_motion_j.shape[0])
    daily_motion_j["edu"] = np.repeat(temp_row.iloc[0, 7], daily_motion_j.shape[0])
    daily_motion_j["marriage"] = np.repeat(temp_row.iloc[0, 8], daily_motion_j.shape[0])
    daily_motion_j["work"] = np.repeat(temp_row.iloc[0, 9], daily_motion_j.shape[0])
    daily_motion_j["madrs1"] = np.repeat(temp_row.iloc[0, 10], daily_motion_j.shape[0])
    daily_motion_j["madrs2"] = np.repeat(temp_row.iloc[0, 11], daily_motion_j.shape[0])
    daily_motion_j["name"] = np.repeat("condition_"+str(j), daily_motion_j.shape[0])

    return daily_motion_j


#this function is almost exactly the same as the one above, simply change condition into control
def daily_data_generator_control(j, time_interval_in_minute):
    #load file and convert the timestamp from string to date
    test_file = pd.read_csv(control_location+str(j)+".csv")
    score_file = pd.read_csv(score_location)
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])
    #normalize the activity data
    test_file["activity"] = test_file["activity"]*1000/test_file["activity"].max()

    #find all the timestamps at 0:00
    test_file["hour"] = test_file["timestamp"].dt.hour
    test_file["minute"] = test_file["timestamp"].dt.minute
    day_splitter = test_file[(test_file["hour"]==0) & (test_file["minute"]==0)].index

    #split the data by day. Here we only take days with data from 0:00-23:59. So we discard the first and last day
    extract_first_day = test_file["activity"].loc[day_splitter[0]:day_splitter[1]-1]
    daily_motion_j = pd.DataFrame()
    daily_motion_j[0] = daily_data_averager(extract_first_day, time_interval_in_minute)
    daily_motion_j.reset_index()

    for i in range(1, len(day_splitter)-1):
        start = day_splitter[i]
        end = day_splitter[i+1]
        extract_day_activity = test_file["activity"].loc[start:end-1]
        if zero_remover(extract_day_activity):
            #extract_day_time = temp[0]
            try:
                daily_motion_j[i-1] = daily_data_averager(extract_day_activity, time_interval_in_minute)
            except ValueError:
                pass
        else:
            pass
        
    daily_motion_j.reset_index()
    daily_motion_j = daily_motion_j.transpose()
    daily_motion_j.columns = [str(i) for i in range(0, daily_motion_j.shape[1])]

    #add time 
    #temp = test_file["timestamp"].iloc[day_splitter]
    #daily_motion_j["Time"] = temp.dt.date.iloc[1:-1].to_list()
    #first_column = daily_motion_j.pop('Time')
    #daily_motion_j.insert(0, "Time", first_column)

    #add other attributes from scores.csv into the daily acitivity dataframe 
    temp_row_index = score_file.index[score_file["number"] == "control_"+str(j)]
    temp_row = score_file.iloc[temp_row_index]
    daily_motion_j["age"] = np.repeat(temp_row.iloc[0, 3], daily_motion_j.shape[0])
    daily_motion_j["gender"] = np.repeat(temp_row.iloc[0, 2], daily_motion_j.shape[0])
    daily_motion_j["mental_disorder"] = np.repeat(temp_row.iloc[0, 4], daily_motion_j.shape[0])
    daily_motion_j["melanch"] = np.repeat(temp_row.iloc[0, 5], daily_motion_j.shape[0])
    daily_motion_j["inpatient"] = np.repeat(temp_row.iloc[0, 6], daily_motion_j.shape[0])
    daily_motion_j["edu"] = np.repeat(temp_row.iloc[0, 7], daily_motion_j.shape[0])
    daily_motion_j["marriage"] = np.repeat(temp_row.iloc[0, 8], daily_motion_j.shape[0])
    daily_motion_j["work"] = np.repeat(temp_row.iloc[0, 9], daily_motion_j.shape[0])
    daily_motion_j["madrs1"] = np.repeat(temp_row.iloc[0, 10], daily_motion_j.shape[0])
    daily_motion_j["madrs2"] = np.repeat(temp_row.iloc[0, 11], daily_motion_j.shape[0])
    daily_motion_j["name"] = np.repeat("control_"+str(j), daily_motion_j.shape[0])
    return daily_motion_j




#iterate over all the files, and combine
daily_motion = daily_data_generator_condition(1, delta_t)
control_number = np.arange(1, 32+1, 1)
condition_number = np.arange(2, 23+1, 1)
for k in condition_number:
    daily_motion = pd.concat([daily_motion, daily_data_generator_condition(k, delta_t)], axis = 0)

for h in control_number:
    daily_motion = pd.concat([daily_motion, daily_data_generator_control(h, delta_t)], axis = 0)
    

#reset index, and save
#daily_motion = daily_motion.sample(frac = 1)
daily_motion = daily_motion.set_index(np.arange(0, daily_motion.shape[0], 1))
daily_motion.to_pickle(output_file_saving_location+"daily_motion.pickle") #the name of output file is daily_motion



#create train and test dataset using different group of patients
daily_motion_train = pd.DataFrame()
daily_motion_test = pd.DataFrame()
train_control_number = range(7, 32+1)
test_control_number = range(1, 9)
train_condition_number = range(7, 23+1)
test_condition_number = range(1, 7)
for k in train_condition_number:
    daily_motion_train = pd.concat([daily_motion_train, daily_data_generator_condition(k, delta_t)], axis = 0)

for h in test_condition_number:
    daily_motion_test = pd.concat([daily_motion_test, daily_data_generator_condition(h, delta_t)], axis = 0)
    
for k in train_control_number:
    daily_motion_train = pd.concat([daily_motion_train, daily_data_generator_control(k, delta_t)], axis = 0)

for h in test_control_number:
    daily_motion_test = pd.concat([daily_motion_test, daily_data_generator_control(h, delta_t)], axis = 0)
    

daily_motion_train.to_pickle(output_file_saving_location+"daily_motion_train.pickle") #the name of output file is daily_motion
daily_motion_test.to_pickle(output_file_saving_location+"daily_motion_test.pickle") #the name of output file is daily_motion

