import threading
import multiprocessing
import time


def calc():
    total = 0
    for _ in range(10**7):
        total += 1
        return total
    
print(calc())
start_time = time.time()

multi_thread = [multiprocessing.Process(target=calc) for _ in range(4)]

thread = [threading.Thread(target=calc) for _ in range(4)]
for t in multi_thread:
    t.start()
    
for t in multi_thread:
    t.join()
    
end_time = time.time()

print(f'Exec time:{start_time} - tread time:{end_time}')