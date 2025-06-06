import subprocess
import time
import random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# === 配置区域 ===
ADB_PORTS = [16416, 16480, 16384, 16448, 16576, 16544, 16608, 16640]

X, Y = 1115, 3600
OFFSET_RANGE = 50
INTERVAL_SECONDS = 0.2
DURATION_SECONDS = 600000
# =================

def run_adb_click(port: int):
    offset_x = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    offset_y = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    target_x = X + offset_x
    target_y = Y + offset_y

    cmd = f'adb -s 127.0.0.1:{port} shell input tap {target_x} {target_y}'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[{port}] Tap at ({target_x}, {target_y})")

def main():
    end_time = datetime.now() + timedelta(seconds=DURATION_SECONDS)
    print(f"启动点击任务，每 {INTERVAL_SECONDS} 秒点击一次，持续 {DURATION_SECONDS} 秒")
    print(f"设备端口：{ADB_PORTS}")

    with ThreadPoolExecutor(max_workers=len(ADB_PORTS)) as executor:
        while datetime.now() < end_time:
            futures = [executor.submit(run_adb_click, port) for port in ADB_PORTS]
            # 等待所有点击完成（也可省略等待以追求极限速率）
            for f in futures:
                f.result()
            time.sleep(INTERVAL_SECONDS)

    print("点击任务完成。")

if __name__ == '__main__':
    main()
