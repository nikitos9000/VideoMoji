import time


def timer(fn):
    def _perform(*args, **kwargs):
        start_time = time.time()

        result = fn(*args, **kwargs)

        end_time = time.time() - start_time
        print 'Elapsed time for "%s.%s": %f' % (fn.__module__, fn.__name__, end_time)

        return result

    return _perform
