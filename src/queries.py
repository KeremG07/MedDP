import numpy as np
import pandas as pd
import math
import data_preprocessor as dp


## Read Database
demographic = dp.process_demographic()
examination = dp.process_examination()
labs = dp.process_labs()

## Helper Functions

#Returns the sum of multiple query outputs, can be used for range constrainted queries.
def aggregate_queries(results: list):
    result = [0]*len(results[0])
    for l in results:
        result = np.add(result, l)
    return result


## The user asks the average values of field2 of patients grouped by field1
def query_type1(dataset_group_by, field1: str, dataset_result, field2: str):
    seqn_list1 = dataset_group_by.iloc[:]["SEQN"].tolist()
    seqn_list2 = dataset_result.iloc[:]["SEQN"].tolist()    #Find the SEQN here that also exist in seqn_list_1
    field_list1 = dataset_group_by.iloc[:][field1].tolist() #Show the aggregate result of these values
    field_list2 = dataset_result.iloc[:][field2].tolist()   #Calculate the averages of these values
    
    #X Labels of the histogram / Labels for the pie chart
    fields_result = []
    for field in field_list1:
        if field not in fields_result:
            fields_result.append(field)
    num_groups = len(fields_result)
    
    #If number of groups are too large, create intervals for better representation
    if num_groups > 10:
        num_groups = 10
        interval = (max(fields_result)-min(fields_result))/num_groups
        fields_result = [0]*num_groups
        fields_result[0] = min(fields_result)
        for k in range(1,10):
            fields_result[k] = interval + fields_result[k-1]
                    
    counts = [0]*num_groups             #number of data points
    sums = [0]*num_groups               #sum of data points
    for i in range(len(seqn_list1)):
        seqn = seqn_list1[i]
        if seqn in seqn_list2:
            index_2 = seqn_list2.index(seqn)
            val = field_list2[index_2]
            if pd.notna(val):                   #skipping over NaN data
                cat = field_list1[i]
                j = 0
                while cat >= fields_result[j]:  #which category the data point falls into
                    j += 1
                    if len(fields_result) <= j:
                        break
                j -= 1
                counts[j] += 1
                sums[j] += val
    avg = [0]*num_groups
    for i in range(num_groups):
        if not counts[i] == 0:          #preventing divbyzero exception
            avg[i] = sums[i]/counts[i]
    return avg
    

#The user asks the distribution of field1 of patients who satisfy field2
def query_type2(dataset_group_by, field1: str, dataset_result, field2: str, req: int):
    seqn_list1 = dataset_group_by.iloc[:]["SEQN"].tolist()
    seqn_list2 = dataset_result.iloc[:]["SEQN"].tolist()    #Find the SEQN here that also exist in seqn_list_1
    field_list1 = dataset_group_by.iloc[:][field1].tolist() #Show counts of this field
    field_list2 = dataset_result.iloc[:][field2].tolist()   #Check constraint "req" here
    
    #X Labels of the histogram / Labels for the pie chart
    fields_result = []
    for field in field_list1:
        if field not in fields_result:
            fields_result.append(field)
    num_groups = len(fields_result)
    
    #If number of groups are too large, create intervals for better representation
    if num_groups > 10:
        num_groups = 10
        interval = (max(fields_result)-min(fields_result))/num_groups
        fields_result = [0]*num_groups
        fields_result[0] = min(fields_result)
        for k in range(1,10):
            fields_result[k] = interval + fields_result[k-1]
                   
    counts = [0]*num_groups #final list
    for i in range(len(seqn_list1)):
        seqn = seqn_list1[i]
        if seqn in seqn_list2:
            index_2 = seqn_list2.index(seqn)
            if field_list2[index_2] == req: #whether the requirement is met in that field
                val = field_list1[i]
                j = 0
                while val >= fields_result[j]:
                    j += 1
                    if len(fields_result) <= j:
                        break
                j -= 1
                counts[j] += 1
    return counts