
import time
import random

def random_task():
    """Simulates a random task that takes between 1 and 5 seconds to complete."""
    duration = random.randint(1, 5)
    print(f"Starting task that will take {duration} seconds...")
    time.sleep(duration)
    print("Task completed.")