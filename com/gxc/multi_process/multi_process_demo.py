#-*- coding: UTF-8 -*-
import multiprocessing
from multiprocessing import Pool
import time
class Result:
    def func(self,msg):
      for i in xrange(3):
        print msg
        time.sleep(1)
      return "done " + msg

import math, sys, time
import pp
def IsPrime(n):

    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True
def SumPrimes(n):
    for i in xrange(15):
        sum([x for x in xrange(2,n) if IsPrime(x)])
    return sum([x for x in xrange(2,n) if IsPrime(x)])
if __name__ == "__main__":
#     pool = multiprocessing.Pool(processes=4)
#     result = []
#     for i in xrange(10):
#       msg = "hello %d" %(i)
#       _result = Result()
#       result.append(pool.apply_async(_result.func, (msg, )))
#     print "-"*40
#     pool.close()
#     pool.join()
#     print "*"*40
#     for res in result:
#       print res.get()
#     print "Sub-process(es) done."
    threadpool = Pool()
    inputs = (100000, 100100, 100200, 100300, 100400, 100500)
    start_time = time.time()
    for input in inputs:
        print SumPrimes(input)
    print '单线程执行，总耗时', time.time() - start_time, 's'
    # tuple of all parallel python servers to connect with
    ppservers = ()
    #ppservers = ("10.0.0.1",)
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers)
    print "pp 可以用的工作核心线程数", job_server.get_ncpus(), "workers"
    start_time = time.time()
#     jobs = [(input, job_server.submit(SumPrimes,(input,), (IsPrime,), ("math",))) for input in inputs]
    jobs = threadpool.map(SumPrimes, inputs)
    for job in jobs:
        print "Sum of primes below", "is", job
    print "多线程下执行耗时: ", time.time() - start_time, "s"
    job_server.print_stats()