"""Test2 for 'coinmarketcap.com' API(Test1 with multithreading)"""
from multiprocessing.pool import ThreadPool
import numpy
import time
from test_task_buidl1 import ApiTest1


def multithread_test(test, threads_num=8, min_rps=5, percent=80, max_perc=450):
    results = []
    pool = ThreadPool()

    start_time = time.time()
    for i in range(threads_num):
        results.append(pool.apply_async(test.api_request))
    pool.close()
    pool.join()
    all_process_time = time.time() - start_time

    rps = round(threads_num / all_process_time)
    if rps < min_rps:
        raise AssertionError(f'rps: {rps} < {min_rps}')

    results = [r.get() for r in results]
    percentile_list = sorted([i['time_ms'] for i in results])
    percentile = numpy.percentile(percentile_list, percent)
    if percentile > max_perc:
        raise AssertionError(f'Percentile: {percentile} > {max_perc}')

    return 'Test №2 passed'


if __name__ == '__main__':
    test1 = ApiTest1()
    print(multithread_test(test1))
