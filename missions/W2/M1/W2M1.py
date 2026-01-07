import time
from multiprocessing import Pool, current_process


# ---- Task Definition ----
work = [
    ("A", 3),
    ("B", 2),
    ("C", 4),
    ("D", 1),
]

# ---- Worker function ----
def work_log(task) -> None:
    try:
        name, duration = task
        print(f"Process {name} waiting {duration} seconds")
        time.sleep(duration)  # simulate work
        print(f"Process {name} Finished")
    except Exception as e:
        print(f"Error in process {name}: {e}")



def main() -> None:
    # ---- Worker Pool Setup ----
    num_workers = 2

    with Pool(processes=num_workers) as pool:
        # ---- Task Execution ----
        results = pool.map(work_log, work)


if __name__ == "__main__":
    main()
