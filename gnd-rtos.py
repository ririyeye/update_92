

import os
import rtos_update

if __name__ == "__main__":
    rtos_update.update_rtos('192.168.10.101')

    os.system("pause")
