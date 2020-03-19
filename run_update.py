import time
import compute_cases

while(1):
    print(time.ctime())
    compute_cases.main()
    print('------------------------------------\n')
    time.sleep(1*60*60)
