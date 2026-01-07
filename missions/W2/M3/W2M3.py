from multiprocessing import Process, Queue


def main() -> None:

    # ---- List of items to push into the queue ----
    colors = ['red', 'green', 'blue', 'black']

    # ---- Queue Creation ----
    q = Queue()

    # ---- Put items into the queue ----
    print("pushing items to queue:")
    for i, color in enumerate(colors):
        # Print item number and color as it is pushed
        print(f"item no: {i+1} {color}")
        q.put(color)

    q.put(None)

    # ---- Get items from the queue ----
    print("\npopping items from queue:")
    pop_idx = 0
    while True:
        item = q.get()
        if item is None:
            break
        print(f"item no: {pop_idx} {item}")
        pop_idx += 1


if __name__ == "__main__":
    main()
