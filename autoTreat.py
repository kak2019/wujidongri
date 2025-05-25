import subprocess
import time
import random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# === 配置区域 ===
ADB_PORTS = [16384]

X, Y = 650, 1150
OFFSET_RANGE = 50
SHORT_INTERVAL_SECONDS = 0.5  # 两次点击之间的短暂间隔
LONG_INTERVAL_SECONDS = 2.0   # 每轮点击后的长暂停
DURATION_SECONDS = 300  # 设置为 300 秒以便调试
# =================

def run_adb_click(port: int):
    offset_x = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    offset_y = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    target_x = X + offset_x
    target_y = Y + offset_y

    adb_path = r'C:\Program Files\Netease\MuMu Player 12\shell\adb'  # 确保这是 ADB 的正确路径
    cmd = f'"{adb_path}" -s 127.0.0.1:{port} shell input tap {target_x} {target_y}'  # 使用完整路径

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"[{port}] Tap at ({target_x}, {target_y})")
    print(result.stdout.decode(errors='ignore'))  # 使用 'ignore' 来处理编码问题
    print(result.stderr.decode(errors='ignore'))
def main():
    end_time = datetime.now() + timedelta(seconds=DURATION_SECONDS)
    print(f"启动点击任务，第一个点击后间隔 {SHORT_INTERVAL_SECONDS} 秒，再点击一次，然后间隔 {LONG_INTERVAL_SECONDS} 秒，持续 {DURATION_SECONDS} 秒")
    print(f"设备端口：{ADB_PORTS}")

    with ThreadPoolExecutor(max_workers=len(ADB_PORTS)) as executor:
        while datetime.now() < end_time:
            # 第一次点击
            futures1 = [executor.submit(run_adb_click, port) for port in ADB_PORTS]
            for f in futures1:
                f.result()

            time.sleep(SHORT_INTERVAL_SECONDS)  # 等待0.5秒

            # 第二次点击
            futures2 = [executor.submit(run_adb_click, port) for port in ADB_PORTS]
            for f in futures2:
                f.result()

            time.sleep(LONG_INTERVAL_SECONDS)  # 等待2秒

    print("点击任务完成。")

if __name__ == '__main__':
    main()