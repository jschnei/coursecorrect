import numpy as np
import matplotlib.pyplot as plt

from math import sqrt
import random

TEST_CURVE = [(0, 0), (10, 0), (10, 10), (20, 10)]

def l2dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return sqrt((x1-x2)**2 + (y1-y2)**2)

def interpolate_segment(p1, p2, dist):
    x1, y1 = p1
    x2, y2 = p2

    total_dist = l2dist(p1, p2)
    ratio = dist / total_dist

    return (x1 + (x2-x1)*ratio, y1 + (y2-y1)*ratio)

def total_dist(curve):
    total_distance = 0
    for i in range(1, len(curve)):
        total_distance += l2dist(curve[i-1], curve[i])
    return total_distance

def interpolate_curve(curve, dist):
    total_distance = total_dist(curve)

    cur_ind = 1
    cur_dist = dist
    while (cur_dist > l2dist(curve[cur_ind-1], curve[cur_ind]) and
           cur_ind + 1 < len(curve)):
        cur_ind += 1
        cur_dist -= l2dist(curve[cur_ind-1], curve[cur_ind])
    
    return interpolate_segment(curve[cur_ind-1], curve[cur_ind], cur_dist)



def interpolate(curve, num_points):
    total_distance = total_dist(curve)

    interpolated_points = []
    segment_dist = total_distance/(num_points - 1)

    cur_ind = 1
    cur_dist = 0

    for i in range(num_points):
        interpolated_points.append(
            interpolate_segment(curve[cur_ind-1], curve[cur_ind], cur_dist)
        )
        
        cur_dist += segment_dist

        while (cur_dist > l2dist(curve[cur_ind-1], curve[cur_ind])
               and cur_ind + 1 < len(curve)):
            cur_dist -= l2dist(curve[cur_ind-1], curve[cur_ind])
            cur_ind += 1
    
    return interpolated_points


def add_noise(point, noise):
    x, y = point
    nx, ny = random.gauss(0, noise), random.gauss(0, noise)

    return (x + nx, y + ny)


def generate_test_data(curve, num_points=1000, noise = 0.5):
    points = interpolate(curve, num_points)
    times = np.linspace(0, 1, num_points)

    return [add_noise(point, noise) for point in points], times

def plot_curve(curve):
    points = generate_test_data(TEST_CURVE)

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    plt.plot(xs, ys)
    plt.show()
