from typing import List


class SignalData:
    
    def __init__(self, signal_type: str, is_periodic: bool, points: List[tuple]):        
        if signal_type not in ["FREQ", "TIME"]:
            raise ValueError("Signal type must be either FREQ or TIME")
        
        self.signal_type = signal_type
        self.is_periodic = is_periodic
        self.points = points
        self.num_samples = len(points)
    
    def __str__(self):
        return f"Signal Type: {self.signal_type}\nIs Periodic: {self.is_periodic}\nNumber of Samples: {self.num_samples}\nPoints: {self.points}"
    