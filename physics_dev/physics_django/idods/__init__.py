from django.core.signals import request_started
from django.core.signals import request_finished
import time

startedd = 0

def started(sender, **kwargs):
    global startedd
    startedd = time.time()

def finished(sender, **kwargs):
    total = time.time() - startedd
    total = total*1000
    print '=> elapsed time request/response: %f ms' % total

try:
    request_started.connect(started)
    request_finished.connect(finished)

except Exception as e:
    print e
