import numpy as np
import pandas as pd
import math
import data_preprocessor as dp
import copy


## Read Database

demographic = dp.process_demographic()
examination = dp.process_examination()
labs = dp.process_labs()


## Helper Functions

# Applying differential privacy for count queries
def laplace(counts, sensitivity, epsilon):
    noisy_counts = copy.deepcopy(counts)
    for i in range(len(counts)):
        noise = np.random.laplace(loc = 0, scale = sensitivity/epsilon)
        noisy_counts[i] = round(noisy_counts[i] + noise)
    return noisy_counts

# Returns the sum of multiple query outputs, can be used for range constrainted queries.
def aggregate_queries(results: list):
    result = [0]*len(results[0])
    for l in results:
        result = np.add(result, l)
    return result


## Queries

# The user asks the average values of field2 of patients grouped by field1
def avg_query(dataset_group_by, field1: str, dataset_result, field2: str):
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
    interval = 0

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
    return avg, fields_result, interval

# The user asks the distribution of field1 of ALL patients
def general_count_query(dataset_group_by, field1: str):
    seqn_list1 = dataset_group_by.iloc[:]["SEQN"].tolist()
    field_list1 = dataset_group_by.iloc[:][field1].tolist() #Show counts of this field
    
    #X Labels of the histogram / Labels for the pie chart
    fields_result = []
    for field in field_list1:
        if field not in fields_result:
            fields_result.append(field)
    num_groups = len(fields_result)
    interval = 0
    
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
        val = field_list1[i]
        j = 0
        while val >= fields_result[j]:
            j += 1
            if len(fields_result) <= j:
                break
        j -= 1
        counts[j] += 1
    """sensitivity = 2
    epsilon = 0.1
    counts = laplace(counts, sensitivity, epsilon)"""
    return counts, fields_result, interval

# The user asks the distribution of field1of patients who are aged between min_age and max_age
def age_range_query(dataset_group_by, field1: str, min_age: int, max_age: int):
    results = []
    for i in range(min_age,max_age+1):
        result, fields_result, interval = single_constraint_query(dataset_group_by, field1, demographic, "AGE",  i)
        if not result:
            print("oops")
        else:
            results.append(result)
    return aggregate_queries(results), fields_result, interval

# The user asks the distribution of field1 of patients who satisfy field2 (gender or race)
def single_constraint_query(dataset_group_by, field1: str, dataset_result, field2: str, req):
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
    interval = 0

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
    """sensitivity = 2
    epsilon = 0.1
    counts = laplace(counts, sensitivity, epsilon)"""
    return counts, fields_result, interval

# The user asks the distribution of field1 of patients who satisfy field2 and field3 (gender and race)
def double_constraint_query(dataset_group_by, field1: str, dataset_result, field2: str, field3: str, req2, req3):
    seqn_list1 = dataset_group_by.iloc[:]["SEQN"].tolist()
    seqn_list2 = dataset_result.iloc[:]["SEQN"].tolist()    #Find the SEQN here that also exist in seqn_list_1
    field_list1 = dataset_group_by.iloc[:][field1].tolist() #Show counts of this field
    field_list2 = dataset_result.iloc[:][field2].tolist()   #Check constraint "req2" here
    field_list3 = dataset_result.iloc[:][field3].tolist()   #Check constraint "req3" here
    
    #X Labels of the histogram / Labels for the pie chart
    fields_result = []
    for field in field_list1:
        if field not in fields_result:
            fields_result.append(field)
    num_groups = len(fields_result)
    interval = 0

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
            if field_list2[index_2] == req2 and field_list3[index_2] == req3: #whether the requirement is met in that field
                val = field_list1[i]
                j = 0
                while val >= fields_result[j]:
                    j += 1
                    if len(fields_result) <= j:
                        break
                j -= 1
                counts[j] += 1
    """sensitivity = 2
    epsilon = 0.1
    counts = laplace(counts, sensitivity, epsilon)"""
    return counts, fields_result, interval