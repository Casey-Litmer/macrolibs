from time import perf_counter


def timer(print_time = True):
    def time_function(f):
        def wrapper(*args, **kwargs):
            t0 = perf_counter()
            result = f(*args, **kwargs)
            time = perf_counter() - t0

            if print_time:
                print("time (ms):", time)
                return result
            else:
                return (result, time)

        return wrapper
    return time_function
