import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, scrolledtext
import threading
import subprocess
import datetime

tools = {
    'curl': 'curl -v -A "Mozilla/5.0" -H "Accept: */*" -H "Connection: keep-alive" {target}',
    'nmap': 'nmap -sV -p- -T4 {target}',
    'subfinder': 'subfinder -d {target} -all | tee subdomain.txt',
    'httpx': 'httpx --list subdomain.txt -ports 80,443,8000,8080,3000 -title -tech-detect -status-code -o httpx_out.txt',
    'dirsearch': 'dirsearch -u http://{target} -e php,html,js',
    'xsstrike': 'xsstrike -u http://{target} --crawl --skip',
    'sqlmap': 'sqlmap -u http://{target} --batch --level=2',
}

class BugBountyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕷️ 漏洞赏金工具 v1.0（灵儿定制）")
        self.root.geometry("800x600")
        self.log_data = ""
        self.scanning = False
        self.current_process = None

        # "superhero"  - 夜晚超级英雄风，深色高对比，熬夜打赏金必备酷炫风
        # "flatly"     - 扁平简洁，明亮清爽，白天写代码的良伴
        # "vapor"     - 赛博朋克紫色调，神秘又未来感满满，赏金猎人的赛博战衣
        # "cyborg"     - 机械感黑色主题，冷酷且护眼，适合深夜的安全审计
        # "darkly"     - 暗黑风，柔和点的黑色调，眼睛敏感的灵儿的福音
        # "journal"   - 文艺手账风，浅色柔和，适合记录和总结漏洞笔记
        # "litera"    - 干净明亮，简约风格，清爽无负担
        # "minty"     - 清新薄荷绿，提神醒脑，赏金猎人也要养眼
        # "pulse"     - 红色热情动感，聚焦重点，关键时刻给你动力满满
        # "sandstone" - 沙石色调，温暖自然，带点复古气息
        # "simplex"   - 简单大方，浅色风格，轻量且易读
        # "sketchy"   - 手绘风趣味满满，放松时刻必备
        # "slate"     - 深灰稳重，冷峻专业，职场精英风范
        # "solar"     - 明亮温暖的阳光色系， optimistic
        # "spacelab"  - 科技蓝，未来感强，专业且冷静
        # "united"    - 统一风格，明亮且亲切，通用且适合新手
        # "yeti"      - 清新冰蓝，北极风范，极简且清爽
        self.style = ttk.Style("vapor")

        frame_top = ttk.Frame(root, padding=10)
        frame_top.pack(fill=X)

        ttk.Label(frame_top, text="🌐 目标地址：", font=("微软雅黑", 14)).pack(side=LEFT, padx=5)
        self.target_entry = ttk.Entry(frame_top, width=50)
        self.target_entry.pack(side=LEFT, padx=5)

        frame_tools = ttk.LabelFrame(root, text="🧰 工具选择", padding=(10, 5))
        frame_tools.pack(fill=X, padx=10, pady=10)

        self.tool_vars = {}
        for i, tool in enumerate(tools):
            var = ttk.BooleanVar()
            chk = ttk.Checkbutton(frame_tools, text=tool, variable=var, bootstyle="info-round-toggle")
            chk.grid(row=i//3, column=i%3, padx=10, pady=5, sticky=W)
            self.tool_vars[tool] = var

        frame_buttons = ttk.Frame(root, padding=(10, 5))
        frame_buttons.pack(fill=X)

        self.start_btn = ttk.Button(frame_buttons, text="▶️ 开始扫描", bootstyle="success", command=self.run_tools)
        self.start_btn.pack(side=LEFT, padx=5)

        self.stop_btn = ttk.Button(frame_buttons, text="⏹️ 停止扫描", bootstyle="danger", command=self.stop_scan, state="disabled")
        self.stop_btn.pack(side=LEFT, padx=5)

        self.clear_btn = ttk.Button(frame_buttons, text="🧹 清除日志", bootstyle="warning", command=self.clear_logs)
        self.clear_btn.pack(side=LEFT, padx=5)

        self.save_btn = ttk.Button(frame_buttons, text="💾 保存日志", bootstyle="primary", command=self.save_logs)
        self.save_btn.pack(side=LEFT, padx=5)

        ttk.Label(root, text="📄 实时日志输出：", font=("微软雅黑", 16)).pack(anchor=W, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, height=20, font=("Arial", 16, "bold"))
        self.log_area.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{timestamp} {msg}\n"
        self.log_area.insert("end", full_msg)
        self.log_area.yview("end")
        self.log_data += full_msg

    def run_command(self, cmd):
        try:
            self.log(f"💥 执行命令：{cmd}")
            self.current_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while self.scanning:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())
                    
            error = self.current_process.stderr.readline()
            if error:
                self.log(f"⚠️ {error.strip()}")
                
            if not self.scanning:
                self.current_process.terminate()
                self.log("🛑 扫描已停止")
                
        except Exception as e:
            self.log(f"🔥 错误：{e}")

    def run_tools(self):
        target = self.target_entry.get().strip()
        if not target:
            self.log("❌ 请输入目标地址")
            return

        selected = [tool for tool, var in self.tool_vars.items() if var.get()]
        if not selected:
            self.log("⚠️ 请至少选择一个工具")
            return

        # 处理目标地址，为 nmap 工具移除 http:// 和 https:// 前缀
        processed_target = target
        if 'nmap' in selected:
            if processed_target.startswith('http://'):
                processed_target = processed_target[7:]
            elif processed_target.startswith('https://'):
                processed_target = processed_target[8:]
            # 移除末尾的斜杠
            processed_target = processed_target.rstrip('/')

        self.scanning = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        def thread_func():
            for tool in selected:
                if not self.scanning:
                    break
                # 根据工具类型选择使用原始目标还是处理后的目标
                current_target = processed_target if tool == 'nmap' else target
                cmd = tools[tool].format(target=current_target)
                self.run_command(cmd)
            
            self.scanning = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

        threading.Thread(target=thread_func).start()

    def stop_scan(self):
        self.scanning = False
        if self.current_process:
            self.current_process.terminate()
        self.log("🛑 正在停止扫描...")

    def clear_logs(self):
        self.log_area.delete(1.0, "end")
        self.log_data = ""
        self.log("✨ 日志已清除")

    def save_logs(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            with open(filepath, "w") as f:
                f.write(self.log_data)
            self.log(f"✅ 日志已保存到：{filepath}")

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = BugBountyApp(root)
    root.mainloop()
