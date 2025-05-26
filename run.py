# 导入所需的库
import time  # 用于实现延时功能
import subprocess  # 用于创建和管理子进程
from watchdog.observers import Observer  # 用于监控文件系统变化
from watchdog.events import FileSystemEventHandler  # 用于处理文件系统事件

class ReloadHandler(FileSystemEventHandler):
    """文件变更处理器，继承自FileSystemEventHandler
    用于监控main.py文件的变化并自动重启程序
    """
    def __init__(self, command):
        self.command = command  # 要执行的命令
        self.process = None  # 存储子进程对象
        self.run_script()  # 初始化时运行脚本

    def run_script(self):
        """运行Python脚本
        如果已有进程在运行，先终止它再启动新进程
        """
        if self.process:
            self.process.kill()  # 终止现有进程
        print("🚀 Running script...\n")
        self.process = subprocess.Popen(self.command, shell=True)  # 创建新进程

    def on_modified(self, event):
        """文件修改事件处理函数
        当main.py文件发生变化时自动重启程序
        """
        if event.src_path.endswith("main.py"):
            print(f"📁 Detected change in: {event.src_path}")
            self.run_script()

if __name__ == "__main__":
    path = "."  # 监控当前目录
    event_handler = ReloadHandler("python3 main.py")  # 创建事件处理器
    observer = Observer()  # 创建观察者对象
    observer.schedule(event_handler, path=path, recursive=False)  # 设置监控
    observer.start()  # 启动监控
    print("🧿 Watching for changes in main.py...")

    try:
        while True:
            time.sleep(1)  # 主循环，每秒检查一次
    except KeyboardInterrupt:
        observer.stop()  # 处理Ctrl+C中断
    observer.join()  # 等待观察者线程结束
