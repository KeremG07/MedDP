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
    for eps in eps_values:
        total_e_avg = 0
        total_e_mse = 0
        for i in range(40):
            dp_counts = laplace(counts, sensitivity, eps)
            total_e_avg += calculate_average_error(counts, dp_counts)
            total_e_mse += calculate_mean_squared_error(counts, dp_counts)
        error_avg.append(total_e_avg/40)
        error_mse.append(total_e_mse/40)

    # TODO: choose the best epsilon value here by looking at error values and return that as well

    # FOR EXAMPLE CHOOSE THE SMALLEST EPSILON VALUE THAT GIVES LESS THAN 5% ERROR FOR BOTH ERROR MEASUREMENTS
    goal_error = 0.30
    len_eps_values = len(eps_values)
    for i in range(len_eps_values):
        if (error_avg[i] < goal_error):  # and error_mse[i] < goal_error):
            epsilon = eps_values[i]
            break

    return error_avg, error_mse, epsilon
