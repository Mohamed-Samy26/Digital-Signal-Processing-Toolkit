import numpy as np

from SignalData import SignalData


def moving_average(signal:SignalData, window_size:int):
    if window_size <= 0:
        print("Window size must be greater than 0.")
        return signal
    
    if signal.signal_type != "TIME":
        raise ValueError("Signal must be a time domain signal.")
    
    if window_size > len(signal.points):
        raise ValueError("Window size must be less than or equal to the number of samples in the signal.")
    
    points = []
    for i in range(len(signal.points) - window_size + 1):
        sum = 0
        for j in range(window_size):
            sum += signal.points[i + j][1]
        average = sum / window_size
        points.append((signal.points[i][0], average, 0))
    
    return SignalData("TIME", signal.is_periodic, points)

def sharpen(signal:SignalData):
    # returns first and second derivatives of the signal
    if signal.signal_type != "TIME":
        raise ValueError("Signal must be a time domain signal.")
    
    first_derivative = []
    # first_derivative.append((signal.points[0][0], 0))
    for i in range(1, len(signal.points)):
        first_derivative.append((signal.points[i][0], signal.points[i][1] - signal.points[i-1][1]))
    
            
    second_derivative = []
    # second_derivative.append((first_derivative[0][0], 0))
    
    for i in range(1, len(signal.points) -1):
        second_derivative.append((signal.points[i][0], (signal.points[i+1][1] - (2*signal.points[i][1]) + signal.points[i-1][1])))
        
    # second_derivative.append((signal.points[-1][0], 0))
    
    return SignalData("TIME", signal.is_periodic, first_derivative), SignalData("TIME", signal.is_periodic, second_derivative)

def fold_signal(signal:SignalData):
    if signal.signal_type != "TIME":
        raise ValueError("Signal must be a time domain signal.")
    
    points = []
    # reverse the signal points indices
    for i in range(len(signal.points)):
        points.append((signal.points[-i-1][0], signal.points[i][1]))
    
    
    return SignalData("TIME", signal.is_periodic, points)

def shift_signal(signal:SignalData, shift:int):
    if signal.signal_type != "TIME":
        raise ValueError("Signal must be a time domain signal.")
    
    points = []
    for i in range(len(signal.points)):
        points.append((signal.points[i][0] - shift, signal.points[i][1]))
    
    return SignalData("TIME", signal.is_periodic, points)

