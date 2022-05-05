import time


def profile(func):


    def decorated(*args, **kwargs):
        print(func.__name__)
        print(f"Anzahl von argument: {len(args) + len(kwargs)}")
        start_time = time.time()

        result = func(*args, **kwargs)
        print(f"Laufzeit: {time.time() - start_time}")

        return result

    return decorated


@profile
def spam(a, b):
    time.sleep(3)
    print(3*f"{a}{b}")


spam("eggs", "Bacon")
