import time
import random
import tracemalloc
from typing import TypedDict, List, Dict, Set
from collections import defaultdict
from functools import reduce

class Activity(TypedDict):
    user: str
    action: str
    duration: float

def total_time_per_user(logs: List[dict]) -> Dict[str, float]:
    def accumulator(acc, record):
        acc[record["user"]] += record["duration"]
        return acc

    totals = reduce(accumulator, logs, defaultdict(float))
    return dict(totals)

def most_active_users(logs: List[dict], k: int) -> List[str]:
    totals = total_time_per_user(logs)
    sorted_users = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return [user for user, _ in sorted_users[:k]]

def unique_actions(logs: List[dict]) -> Set[str]:
    return {record["action"] for record in logs}

def generate_activities(n: int) -> List[Activity]:
    users = [f"USER{i}" for i in range(1, max(3, n // 10))]
    actions = [
        "visit leetcode", "download movies", "visit google ai studio", 
        "access VPN", "read bcrypt docs", "compile rust code", "watch youtube"
    ]
    
    return [
        {
            "user": random.choice(users),
            "action": random.choice(actions),
            "duration": round(random.uniform(10.0, 50000.0), 2)
        }
        for _ in range(n)
    ]

def measure_performance(func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    func(*args, **kwargs)
    
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_ms = (end_time - start_time) * 1000
    peak_mem_kb = peak_mem / 1024
    
    return time_ms, peak_mem_kb

if __name__ == "__main__":
    sample_sizes = [10, 100, 1000, 10000]

    for n in sample_sizes:
        print(f"Sampling for n = {n}")
        activity_records = generate_activities(n)

        time_ms, mem_kb = measure_performance(total_time_per_user, activity_records)
        print(f"  Total Time Per User -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB")

        time_ms, mem_kb = measure_performance(most_active_users, activity_records, 5)
        print(f"  Most Active Users   -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB")

        time_ms, mem_kb = measure_performance(unique_actions, activity_records)
        print(f"  Unique Actions      -> Time: {time_ms:.4f} ms | Peak Memory: {mem_kb:.4f} KB\n")