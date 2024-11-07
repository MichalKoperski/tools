import time
import continuous_threading

c = 0

def count():
    global c
    c += 1
    time.sleep(1)

th = continuous_threading.ContinuousThread(target=count)
th.start()

time.sleep(5)
print('Count:', c)

# Process will automatically exit with threading._shutdown() override