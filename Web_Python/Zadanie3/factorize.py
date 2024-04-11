import multiprocessing
import time

def factorize_sync(*numbers):
    results = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        results.append(factors)
    return results

def factorize(*numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results

def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

start_time_sync = time.time()
a, b, c, d = factorize_sync(128, 255, 99999, 10651060)
end_time_sync = time.time()

start_time_async = time.time()
a_async, b_async, c_async, d_async = factorize(128, 255, 99999, 10651060)
end_time_async = time.time()

print("Synchronous execution time:", end_time_sync - start_time_sync)
print("Asynchronous execution time:", end_time_async - start_time_async)

assert a == a_async
assert b == b_async
assert c == c_async
assert d == d_async
