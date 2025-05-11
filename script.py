import pyautogui
import time
import sys

try:
    import keyboard  # 用于键盘监听
except ImportError:
    print("请先安装keyboard库：pip install keyboard")
    sys.exit(1)

# 安全设置：设置故障保护（鼠标移到左上角会触发异常停止）
pyautogui.FAILSAFE = True
exit_flag = False


def record_positions():
    """记录多个点击位置"""
    positions = []
    print("=== 坐标记录模式 ===")
    print("移动鼠标到目标位置，按 [空格] 记录，按 [ESC] 结束记录")

    while True:
        if keyboard.is_pressed('esc'):
            print("\n结束记录")
            break
        if keyboard.is_pressed('space'):
            pos = pyautogui.position()
            positions.append(pos)
            print(f"已记录位置 {len(positions)}: {pos}")
            time.sleep(0.3)  # 防抖
    return positions


def auto_click(positions, interval=1.0, max_time=60):
    """执行自动点击"""
    print(f"\n=== 自动点击开始（{max_time}秒后停止）===")
    print("按 [ESC] 可提前终止")

    start_time = time.time()
    try:
        while (time.time() - start_time) < max_time:
            if keyboard.is_pressed('esc'):
                print("\n用户手动停止")
                break
            for i, pos in enumerate(positions):
                pyautogui.click(pos)
                print(f"点击 位置{i + 1}: {pos} | 剩余时间: {int(max_time - (time.time() - start_time))}s", end="\r")
                time.sleep(interval)
    except Exception as e:
        print(f"\n发生错误: {e}")
    finally:
        print("\n=== 点击结束 ===")


if __name__ == "__main__":
    try:
        print("准备记录点击位置...")
        time.sleep(2)
        click_positions = record_positions()

        if len(click_positions) < 1:
            print("错误：至少需要1个位置！")
            sys.exit(1)

        interval = float(input("输入点击间隔（秒，默认1.0）: ") or "1.0")
        max_time = float(input("输入运行时长（秒，默认60）: ") or "60")

        print("5秒后开始，请切换到目标窗口...")
        time.sleep(5)
        auto_click(click_positions, interval, max_time)

    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序错误: {e}")