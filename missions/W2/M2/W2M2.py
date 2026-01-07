from multiprocessing import Process


def print_continent(name: str = "Asia") -> None:
    print(f"The name of continent is : {name}")


def main() -> None:

    continents = ['America', 'Europe', 'Africa']
    processes = []

    # ---- Default Process (Asia) ----
    p_default = Process(target=print_continent)
    processes.append(p_default)

    # ---- Create Processes with Arguments ----
    for continent in continents:
        p = Process(target=print_continent, args=(continent,))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()

