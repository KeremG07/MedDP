import numpy as np
import copy


def calculate_average_error(actual_hist, noisy_hist):
    total = 0
    bins = len(actual_hist)
    for i in range(bins):
        total += abs(actual_hist[i] - noisy_hist[i])
    return total/bins


def calculate_mean_squared_error(actual_hist, noisy_hist):
    total = 0
    bins = len(actual_hist)
    for i in range(bins):
        total += (actual_hist[i] - noisy_hist[i])**2
    return total/bins

# Applying differential privacy for count queries


def laplace(counts, sensitivity, epsilon):
    noisy_counts = copy.deepcopy(counts)
    for i in range(len(counts)):
        noise = np.random.laplace(loc=0, scale=sensitivity/epsilon)
        noisy_counts[i] = round(noisy_counts[i] + noise)
    return noisy_counts


def epsilon_experiment(counts, sensitivity, eps_values: list):
    error_avg = []
    error_mse = []
    epsilon = 0
    exp_count = 10
    for eps in eps_values:
        total_e_avg = 0
        total_e_mse = 0
        for i in range(exp_count):
            dp_counts = laplace(counts, sensitivity, eps)
            total_e_avg += calculate_average_error(counts, dp_counts)
            total_e_mse += calculate_mean_squared_error(counts, dp_counts)
        error_avg.append(total_e_avg/exp_count)
        error_mse.append(total_e_mse/exp_count)

    goal_error = 0.75
    len_eps_values = len(eps_values)
    for i in range(len_eps_values):
        if (error_avg[i] < goal_error):
            epsilon = eps_values[i]
            break

    return epsilon
