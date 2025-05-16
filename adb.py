import subprocess
import time
import random
from datetime import datetime, timedelta

# === 配置区域 ===
ADB_PORTS = [16416, 16480, 16384, 16448,16512]
# ADB_PORTS = [16416, 16480, 16384, 16448]
# 原始点击坐标
X, Y = 1115, 3600

# 随机偏移范围（单位：像素）
OFFSET_RANGE = 50  # ±10 像素

# 点击间隔（秒）
INTERVAL_SECONDS = 0.1

# 总持续时间（秒）
DURATION_SECONDS = 600000
# =================

def run_adb_click(port: int):
    """发送带有随机偏移的点击命令"""
    offset_x = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    offset_y = random.randint(-OFFSET_RANGE, OFFSET_RANGE)
    target_x = X + offset_x
    target_y = Y + offset_y

    cmd = f'adb -s 127.0.0.1:{port} shell input tap {target_x} {target_y}'
    subprocess.run(cmd, shell=True)
    print(f"点击端口 {port} -> 坐标 ({target_x}, {target_y})")

def main():
    end_time = datetime.now() + timedelta(seconds=DURATION_SECONDS)
    print(f"启动点击任务，每 {INTERVAL_SECONDS} 秒点击一次，持续 {DURATION_SECONDS} 秒")
    print(f"设备端口：{ADB_PORTS}")

    while datetime.now() < end_time:
        for port in ADB_PORTS:
            run_adb_click(port)
        time.sleep(INTERVAL_SECONDS)

    print("点击任务完成。")

if __name__ == '__main__':
    main()
