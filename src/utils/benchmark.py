import time
import psutil
import os
from functools import wraps
from typing import Callable, Dict, Any, Tuple
import pandas as pd

def measure_performance(func: Callable) -> Callable:
    """
    Decorator to measure the performance of an algorithm.
    Measures execution time and memory usage.
    
    Args:
        func: The function to measure
        
    Returns:
        Wrapped function that includes performance metrics
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, Dict[str, float]]:
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # Convert to MB
        
        # Measure execution time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Get final memory usage
        mem_after = process.memory_info().rss / 1024 / 1024
        mem_used = mem_after - mem_before
        
        # Calculate performance metrics
        execution_time = end_time - start_time
        
        metrics = {
            'execution_time': execution_time,
            'memory_used_mb': mem_used,
            'path_length': len(result[0]) if result and result[0] else 0,
            'path_cost': result[1] if result else float('inf')
        }
        
        return result, metrics
    
    return wrapper

class AlgorithmBenchmark:
    """
    Class for benchmarking multiple algorithms on the same graph.
    """
    def __init__(self):
        self.results = []
    
    def run_benchmark(self, algorithms: Dict[str, Callable], graph, start, end) -> pd.DataFrame:
        """
        Run benchmarks for multiple algorithms on the same graph.
        
        Args:
            algorithms: Dictionary of algorithm names to their functions
            graph: The graph to test on
            start: Starting node
            end: Target node
            
        Returns:
            DataFrame containing benchmark results
        """
        for name, algorithm in algorithms.items():
            try:
                result, metrics = measure_performance(algorithm)(graph, start, end)
                metrics['algorithm'] = name
                metrics['success'] = result is not None
                self.results.append(metrics)
            except Exception as e:
                print(f"Error running {name}: {str(e)}")
                self.results.append({
                    'algorithm': name,
                    'execution_time': float('inf'),
                    'memory_used_mb': 0,
                    'path_length': 0,
                    'path_cost': float('inf'),
                    'success': False,
                    'error': str(e)
                })
        
        return pd.DataFrame(self.results)
    
    def save_results(self, filename: str):
        """
        Save benchmark results to a CSV file.
        
        Args:
            filename: Name of the file to save results to
        """
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False) 