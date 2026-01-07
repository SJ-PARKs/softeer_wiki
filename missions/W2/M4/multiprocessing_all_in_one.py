import time
from multiprocessing import Process, Queue, current_process
from queue import Empty 

def worker(
    tasks_to_accomplish: Queue,
    tasks_that_are_done: Queue
) -> None:
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
            # ---- Execute the task ----
            time.sleep(0.5)
            process_name = current_process().name
            result = f"{task} is done by {process_name}"
            tasks_that_are_done.put(result)
        except Empty:
            # No more tasks available in the queue
            break

def main() -> None:
    tasks_to_accomplish: Queue = Queue()
    tasks_that_are_done: Queue = Queue()

    # Distribute 10 tasks
    for task_no in range(10):
        tasks_to_accomplish.put(f"Task no {task_no}")
        print(f"Task no {task_no}")

    processes = []

    # Create 4 worker processes
    for process_no in range(4):
        process = Process(
            target=worker,
            args=(tasks_to_accomplish, tasks_that_are_done),
            name=f"Worker-{process_no+1}"
        )
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Print completed task results
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())


if __name__ == "__main__":
    main()
