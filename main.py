import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, scrolledtext
import threading
import subprocess
import datetime
import sys
import glob
import tkinter as tk
import os
import time 
import ctypes

tools = {
    'curl': 'curl -v -A "Mozilla/5.0" -H "Accept: */*" -H "Connection: keep-alive" {target}' if sys.platform != 'win32' else 'curl -v -A "Mozilla/5.0" -H "Accept: */*" -H "Connection: keep-alive" "{target}"',
    'nmap': 'nmap -sV -p- -T4 {target}',
    'subfinder': 'subfinder -d {target} -all | tee subdomain.txt',
    'httpx': 'httpx --list subdomain.txt -ports 80,443,8000,8080,3000 -title -tech-detect -status-code -o httpx_out.txt',
    'dirsearch': 'dirsearch -u http://{target} -e php,html,js',
    'xsstrike': 'xsstrike -u http://{target} --crawl --skip',
    # sqlmap 基础模式
    'sqlmap_basic': 'sqlmap -u "{target}" --batch',
    'sqlmap_aggressive': 'sqlmap -u "{target}" --level=5 --risk=3 --batch',
    'sqlmap_post': 'sqlmap -u "{target}" --data="username=admin&password=1" --batch',
    'sqlmap_cookie': 'sqlmap -u "{target}" --cookie="PHPSESSID=12345" --batch',
    'sqlmap_headers': 'sqlmap -u "{target}" --headers="X-Forwarded-For: 127.0.0.1" --batch',
    'sqlmap_dbs': 'sqlmap -u "{target}" --dbs --batch',
    'sqlmap_tables': 'sqlmap -u "{target}" -D <数据库名> --tables --batch',
    'sqlmap_columns': 'sqlmap -u "{target}" -D <数据库名> -T <表名> --columns --batch',
    'sqlmap_dump': 'sqlmap -u "{target}" -D <数据库名> -T <表名> -C <字段1>,<字段2> --dump --batch',
    'sqlmap_proxy': 'sqlmap -u "{target}" --proxy="http://127.0.0.1:8080" --batch',
    'sqlmap_os_shell': 'sqlmap -u "{target}" --os-shell --batch',
    'hakrawler': 'echo {target} | hakrawler',
}

# 添加工具安装命令
tool_install_commands = {
    'macos': {
        'curl': 'brew install curl',
        'nmap': 'brew install nmap',
        'subfinder': 'brew install subfinder',
        'httpx': 'brew install httpx',
        'dirsearch': 'pip3 install dirsearch',
        'xsstrike': 'pip3 install xsstrike',
        'sqlmap': 'pip3 install sqlmap',
        'hakrawler': 'go install github.com/hakluke/hakrawler@latest'
    },
    'windows': {
        'curl': 'winget install curl',
        'nmap': 'winget install nmap',
        'subfinder': 'go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
        'httpx': 'go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest',
        'dirsearch': 'pip3 install dirsearch',
        'xsstrike': 'pip3 install xsstrike',
        'sqlmap': 'pip3 install sqlmap',
        'hakrawler': 'go install github.com/hakluke/hakrawler@latest'
    },
    'linux': {
        'curl': 'sudo apt-get install curl',
        'nmap': 'sudo apt-get install nmap',
        'subfinder': 'GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
        'httpx': 'GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest',
        'dirsearch': 'pip3 install dirsearch',
        'xsstrike': 'pip3 install xsstrike',
        'sqlmap': 'pip3 install sqlmap',
        'hakrawler': 'go install github.com/hakluke/hakrawler@latest'
    }
}

class BugBountyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕷️ 漏洞赏金工具 v1.0.2（灵儿定制）")
        self.root.geometry("800x600")
        self.log_data = ""
        self.scanning = False
        self.current_process = None

        # 创建菜单栏
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)

        # 文件菜单
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存日志", command=self.save_logs)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=root.quit)

        # 主题菜单
        theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="主题", menu=theme_menu)
        themes = {
            "superhero": "超级英雄风",
            "vapor": "赛博朋克",
            "darkly": "暗黑模式",
            "cyborg": "机械风格",
            "solar": "阳光模式"
        }
        
        for theme_id, theme_name in themes.items():
            theme_menu.add_command(
                label=theme_name,
                command=lambda t=theme_id: self.change_theme(t)
            )

        # 帮助菜单
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用指南", command=self.show_guide)
        help_menu.add_command(label="工具说明", command=self.show_tools_info)
        help_menu.add_command(label="检查更新", command=self.check_update)
        help_menu.add_command(label="安装工具", command=self.check_tools_installation)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)

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
        self.style = ttk.Style("superhero")

        frame_top = ttk.Frame(root, padding=10)
        frame_top.pack(fill=X)

        ttk.Label(frame_top, text="🌐 目标地址：", font=("微软雅黑", 14)).pack(side=LEFT, padx=5)
        self.target_entry = ttk.Entry(frame_top, width=50)
        self.target_entry.pack(side=LEFT, padx=5)

        # Store frame_tools as instance variable
        self.frame_tools = ttk.LabelFrame(root, text="🧰 工具选择", padding=(10, 5))
        self.frame_tools.pack(fill=X, padx=10, pady=10)

        # Main tools selection
        self.tool_vars = {}
        main_tools = ['curl', 'nmap', 'subfinder', 'httpx', 'dirsearch', 'xsstrike', 'sqlmap']
        for i, tool in enumerate(main_tools):
            var = ttk.BooleanVar()
            chk = ttk.Checkbutton(self.frame_tools, text=tool, variable=var, bootstyle="info-round-toggle")
            chk.grid(row=i//3, column=i%3, padx=10, pady=5, sticky=W)
            self.tool_vars[tool] = var
            if tool == 'sqlmap':
                var.trace_add('write', self.toggle_sqlmap_options)

        # SQLMap advanced options frame (initially hidden)
        self.sqlmap_options_frame = ttk.LabelFrame(root, text="SQLMap 高级选项", padding=(10, 5))
        self.sqlmap_option_vars = {}
        
        # SQLMap advanced options
        self.sqlmap_options = [
            ('基础模式', 'sqlmap_basic'),
            ('高风险测试', 'sqlmap_aggressive'),
            ('POST请求', 'sqlmap_post'),
            ('Cookie注入', 'sqlmap_cookie'),
            ('自定义头', 'sqlmap_headers'),
            ('枚举数据库', 'sqlmap_dbs'),
            ('枚举表', 'sqlmap_tables'),
            ('枚举字段', 'sqlmap_columns'),
            ('Dump数据', 'sqlmap_dump'),
            ('代理模式', 'sqlmap_proxy'),
            ('OS Shell', 'sqlmap_os_shell')
        ]
        
        for i, (label, key) in enumerate(self.sqlmap_options):
            var = ttk.BooleanVar()
            chk = ttk.Checkbutton(
                self.sqlmap_options_frame, 
                text=label, 
                variable=var, 
                bootstyle="secondary-round-toggle"
            )
            chk.grid(row=i//3, column=i%3, padx=10, pady=5, sticky=W)
            self.sqlmap_option_vars[key] = var
        
        # Initially hide the SQLMap options
        self.sqlmap_options_frame.pack_forget()
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

        ttk.Label(root, text="实时日志输出：", font=("微软雅黑", 13)).pack(anchor=W, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, height=20, font=("Arial", 14, "bold"))
        self.log_area.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def show_guide(self):
        """显示使用指南"""
        guide_text = """
        🎯 使用指南

        1. 基本操作
        • 在目标地址栏输入要测试的网站地址
        • 在工具选择区勾选需要使用的工具
        • 点击"开始扫描"按钮开始测试
        • 可随时点击"停止扫描"终止操作

        2. 注意事项
        • 使用前请确保已安装所需工具
        • 建议先使用基础工具进行扫描
        • 扫描过程中请遵守相关法律法规
        • 建议在授权情况下使用本工具

        3. 快捷操作
        • Ctrl+S：保存日志
        • Ctrl+Q：退出程序
        • F5：清除日志
        • F1：显示帮助

        4. 主题切换
        • 可根据使用场景选择不同主题
        • 夜间模式更护眼
        • 支持自定义主题色彩"""

        self._show_help_window("使用指南", guide_text)

    def show_tools_info(self):
        """显示工具说明"""
        tools_text = """
        🛠️ 工具说明

        1. curl
        • 功能：HTTP请求测试工具
        • 用途：测试网站响应和HTTP头信息
        • 特点：轻量级、易用、标准输出

        2. nmap
        • 功能：网络扫描和端口检测
        • 用途：发现开放端口和服务版本
        • 特点：功能强大、可定制性高

        3. subfinder
        • 功能：子域名发现工具
        • 用途：收集目标的所有子域名
        • 特点：速度快、准确率高

        4. httpx
        • 功能：HTTP探测工具
        • 用途：批量探测HTTP服务
        • 特点：支持多端口、识别技术栈

        5. dirsearch
        • 功能：目录扫描工具
        • 用途：发现网站隐藏目录
        • 特点：内置字典、支持多线程

        6. xsstrike
        • 功能：XSS漏洞扫描
        • 用途：检测跨站脚本漏洞
        • 特点：智能检测、支持DOM XSS

        7. sqlmap
        • 功能：SQL注入检测
        • 用途：自动化SQL注入测试
        • 特点：支持多种数据库、自动绕过"""

        self._show_help_window("工具说明", tools_text)

    def check_update(self):
        update_text = """
        ✨ 版本信息

        当前版本：v1.0
        发布日期：2024-01
        最新版本：v1.0

        您的软件已经是最新版本！

        如需获取最新版本信息，请关注：
        • GitHub: github.com/johnmelodyme
        • 邮箱: johnmelodymel@qq.com
        • QQ: 3072486255"""

        self._show_help_window("检查更新", update_text)

    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{timestamp} {msg}\n"
        self.log_area.insert("end", full_msg)
        self.log_area.yview("end")
        self.log_data += full_msg

    def run_command(self, cmd):
        try:
            self.log(f"💥 执行命令：{cmd}")
            # 根据操作系统选择shell路径
            shell_path = '/bin/zsh' if sys.platform == 'darwin' else '/bin/sh'
            self.current_process = subprocess.Popen(
                cmd, 
                shell=True,
                executable=shell_path,  # 添加executable参数指定shell路径
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
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

    def toggle_sqlmap_options(self, *args):
        """Toggle visibility of SQLMap advanced options"""
        if self.tool_vars['sqlmap'].get():
            # Show SQLMap options after the tools frame
            self.sqlmap_options_frame.pack(fill=X, padx=10, pady=5, after=self.frame_tools)
        else:
            # Hide SQLMap options and reset all checkboxes
            self.sqlmap_options_frame.pack_forget()
            for var in self.sqlmap_option_vars.values():
                var.set(False)

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
            processed_target = processed_target.rstrip('/')

        # 处理 sqlmap 选项
        sqlmap_selected = []
        if 'sqlmap' in selected:
            for key, var in self.sqlmap_option_vars.items():
                if var.get():
                    sqlmap_selected.append(key)
            if not sqlmap_selected:
                sqlmap_selected = ['sqlmap_basic']
            selected.remove('sqlmap')
            selected += sqlmap_selected

        self.scanning = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        def thread_func():
            for tool in selected:
                if not self.scanning:
                    break
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
        try:
            # 设置默认文件名（包含时间戳）
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"bug_bounty_log_{timestamp}.txt"
            
            # 根据操作系统设置保存对话框的参数
            if sys.platform == 'win32':
                filetypes = [("文本文件", "*.txt"), ("所有文件", "*.*")]
                defaultextension = ".txt"
                initialdir = os.path.expanduser("~\\Documents")
            else:
                filetypes = [("文本文件", ".txt"), ("所有文件", ".*")]
                defaultextension = ".txt"
                initialdir = os.path.expanduser("~/Documents")
        
            filepath = filedialog.asksaveasfilename(
                initialfile=default_filename,
                initialdir=initialdir,
                defaultextension=defaultextension,
                filetypes=filetypes,
                title="保存扫描日志"
            )
        
            if filepath:
                # 使用utf-8编码保存，确保中文正常显示
                with open(filepath, "w", encoding="utf-8") as f:
                    # 添加日志头部信息
                    header = f"漏洞赏金扫描日志\n时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n\n"
                    f.write(header + self.log_data)
                
                self.log(f"✅ 日志已保存到：{filepath}")
                
                # 如果是Windows，自动打开保存目录
                if sys.platform == 'win32':
                    os.startfile(os.path.dirname(filepath))
                
        except Exception as e:
            self.log(f"❌ 保存日志失败：{str(e)}")
            if sys.platform == 'win32':
                self.log("请检查文件路径是否包含特殊字符，或尝试使用管理员权限运行程序。")

    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)
        self.log(f"✨ 已切换到{theme_name}主题")

    def show_about(self):
        about_text = """🕷️ 漏洞赏金工具 v1.0.2
        
集成多种安全测试工具的漏洞赏金猎人助手：

• curl - HTTP请求测试
• nmap - 端口扫描和服务检测
• subfinder - 子域名发现
• httpx - HTTP探测和分析
• dirsearch - Web路径扫描
• xsstrike - XSS漏洞扫描
• sqlmap - SQL注入测试

作者： 钟智强
电邮： johnmelodymel@qq.com
QQ：  3072486255
微信： ctkqiang

版权所有 © 2025 钟智强定制
保留所有权利

本工具仅供安全研究和授权测试使用，
禁止用于非法用途。
"""
        about_window = ttk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x400")
        
        # 添加图标
        try:
            icon_path = os.path.join("assets", "logo.png")
            if os.path.exists(icon_path):
                img = tk.PhotoImage(file=icon_path)
                about_window.iconphoto(True, img)
        except Exception:
            pass
            
        # 创建内容框架
        content_frame = ttk.Frame(about_window, padding=20)
        content_frame.pack(fill=BOTH, expand=True)
        
        # 添加标题
        title_label = ttk.Label(
            content_frame, 
            text="漏洞赏金工具", 
            font=("微软雅黑", 18, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 添加版本号
        version_label = ttk.Label(
            content_frame,
            text="Version 1.0",
            font=("微软雅黑", 10)
        )
        version_label.pack(pady=(0, 20))
        
        # 添加主要内容
        text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD, 
            height=15,
            font=("微软雅黑", 10)
        )
        text.pack(expand=True, fill=BOTH)
        text.insert("1.0", about_text)
        text.configure(state="disabled")
        
        # 添加确定按钮
        ttk.Button(
            content_frame,
            text="确定",
            command=about_window.destroy,
            style="primary.TButton"
        ).pack(pady=(20, 0))

        # 检查工具安装状态
        self.check_tools_installation()

    def check_tools_installation(self):
        missing_tools = []
        for tool in tools.keys():
            if not self.is_tool_installed(tool):
                missing_tools.append(tool)
        
        if missing_tools:
            self.show_installation_dialog(missing_tools)

    def is_tool_installed(self, tool_name):
        try:
            if tool_name.startswith('sqlmap_'):
                tool_name = 'sqlmap'
                
                # Windows系统特殊处理
                if sys.platform == 'win32':
                    # 检查系统PATH中的所有目录
                    paths = os.environ['PATH'].split(';')
                    # 检查常见的工具安装路径
                    additional_paths = [
                        os.path.expanduser('~\\go\\bin'),
                        os.path.expanduser('~\\AppData\\Local\\Programs\\Python\\Python3*\\Scripts'),
                        os.path.expanduser('~\\AppData\\Local\\Programs\\Python\\Python3*'),
                        'C:\\Program Files\\Go\\bin',
                        'C:\\Program Files (x86)\\Nmap'
                    ]
                    paths.extend(additional_paths)
                    
                    # 检查可执行文件是否存在
                    for path in paths:
                        if '*' in path:  # 处理通配符路径
                            
                            matching_paths = glob.glob(path)
                            for match_path in matching_paths:
                                exe_path = os.path.join(match_path, tool_name + '.exe')
                                if os.path.exists(exe_path):
                                    return True
                        else:
                            exe_path = os.path.join(path, tool_name + '.exe')
                            if os.path.exists(exe_path):
                                return True
                    return False
                else:
                    # Unix系统使用which命令
                    result = subprocess.run(['which', tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return result.returncode == 0
        except Exception as e:
            print(f"检查工具路径时出错：{e}")
            return False

    def show_installation_dialog(self, missing_tools):
        dialog = ttk.Toplevel(self.root)
        dialog.title("🛠️ 工具状态检查")
        dialog.geometry("800x500")
        
        content_frame = ttk.Frame(dialog, padding=20)
        content_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(
            content_frame,
            text="工具安装状态：",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=(0, 10))
        
        # 创建工具列表框架
        tools_frame = ttk.Frame(content_frame)
        tools_frame.pack(fill=X, pady=10)
        
        # 为所有工具创建状态指示器
        self.progress_bars = {}
        
        all_tools = [tool for tool in tools.keys() if not tool.startswith('sqlmap_') or tool == 'sqlmap']
        
        for tool in all_tools:
            tool_frame = ttk.Frame(tools_frame)
            tool_frame.pack(fill=X, pady=5)
            
            # 创建状态指示器
            status_indicator = ttk.Label(
                tool_frame,
                text="●",
                font=("微软雅黑", 12),
                foreground="green" if tool not in missing_tools else "red"
            )
            status_indicator.pack(side=LEFT, padx=(0, 5))
            
            # 工具名称
            ttk.Label(
                tool_frame,
                text=f"{tool}",
                font=("微软雅黑", 12)
            ).pack(side=LEFT)
            
            # 状态文本
            status_text = "已安装" if tool not in missing_tools else "未安装"
            ttk.Label(
                tool_frame,
                text=f"({status_text})",
                font=("微软雅黑", 10),
                foreground="green" if tool not in missing_tools else "red"
            ).pack(side=LEFT, padx=5)
            
            # 只为未安装的工具添加进度条
            if tool in missing_tools:
                progress = ttk.Progressbar(
                    tool_frame,
                    length=200,
                    mode='determinate',
                    bootstyle="success"
                )
                progress.pack(side=LEFT, padx=10)
                self.progress_bars[tool] = progress
        
        # 只在有未安装工具时显示安装按钮
        if missing_tools:
            ttk.Button(
                content_frame,
                text="一键安装缺失工具",
                command=lambda: self.install_tools(missing_tools, dialog),
                bootstyle="success"
            ).pack(pady=20)
            
            # 添加说明文本
            note_text = """注意：
            • 工具安装需要管理员权限
            • 安装过程可能需要几分钟
            • 请确保网络连接正常
            • macOS用户需要先安装Homebrew
            • 安装完成后需要重启应用"""
            
            note = scrolledtext.ScrolledText(
                content_frame,
                wrap=tk.WORD,
                height=6,
                font=("微软雅黑", 10)
            )
            note.pack(fill=X)
            note.insert("1.0", note_text)
            note.configure(state="disabled")
        else:
            ttk.Label(
                content_frame,
                text="✅ 所有工具已安装完成！",
                font=("微软雅黑", 12, "bold"),
                foreground="green"
            ).pack(pady=20)

    def install_tools(self, missing_tools, dialog):
        def install_thread():
            if sys.platform == "win32":
                # 检查是否以管理员权限运行
                
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    self.log("⚠️ 请以管理员权限运行程序进行工具安装")
                    return
                    
                # 确保Go环境已安装
                if any(tool in missing_tools for tool in ['subfinder', 'httpx', 'hakrawler']):
                    if not self.check_tool_path('go'):
                        self.log("⚠️ 请先安装Go语言环境：https://golang.org/dl/")
                        return
                        
                # 确保Python环境已安装
                if any(tool in missing_tools for tool in ['dirsearch', 'xsstrike', 'sqlmap']):
                    if not self.check_tool_path('python3') and not self.check_tool_path('python'):
                        self.log("⚠️ 请先安装Python环境：https://www.python.org/downloads/")
                        return
                
            failed_tools = []
            path_setup_needed = []
        
            for tool in missing_tools:
                try:
                    self.progress_bars[tool]['value'] = 0
                    dialog.update()
                    
                    # Get OS-specific install command
                    cmd = tool_install_commands[os_type][tool]
                    process = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    while process.poll() is None:
                        if self.progress_bars[tool]['value'] < 90:
                            self.progress_bars[tool]['value'] += 1
                        dialog.update()
                        time.sleep(0.1)
                    
                    if process.returncode == 0:
                        self.progress_bars[tool]['value'] = 100
                        
                        # Check if tool needs PATH setup
                        if not self.check_tool_path(tool):
                            path_setup_needed.append(tool)
                    else:
                        self.progress_bars[tool]['bootstyle'] = "danger"
                        failed_tools.append(tool)
                        
                except Exception as e:
                    self.progress_bars[tool]['bootstyle'] = "danger"
                    failed_tools.append(tool)
                    print(f"安装 {tool} 时出错：{e}")
                
                dialog.update()
            
            # Show installation results
            result_frame = ttk.Frame(dialog, padding=20)
            result_frame.pack(fill=X)
            
            if failed_tools:
                fail_msg = f"⚠️ 以下工具安装失败：\n{', '.join(failed_tools)}"
                ttk.Label(
                    result_frame,
                    text=fail_msg,
                    font=("微软雅黑", 12),
                    foreground="red"
                ).pack(pady=5)
            
            if path_setup_needed:
                if os_type == 'macos':
                    path_msg = "需要将以下工具添加到环境变量，请在终端执行：\n"
                    path_msg += "echo 'export PATH=\"$PATH:/usr/local/bin:/usr/local/go/bin:$HOME/go/bin\"' >> ~/.zshrc\n"
                    path_msg += "source ~/.zshrc"
                elif os_type == 'linux':
                    path_msg = "需要将以下工具添加到环境变量，请在终端执行：\n"
                    path_msg += "echo 'export PATH=\"$PATH:/usr/local/go/bin:$HOME/go/bin\"' >> ~/.bashrc\n"
                    path_msg += "source ~/.bashrc"
                else:
                    path_msg = "请将以下路径添加到系统环境变量Path中：\n"
                    path_msg += "1. %USERPROFILE%\\go\\bin\n"
                    path_msg += "2. %LOCALAPPDATA%\\Programs\\Python\\Python3*\\Scripts\n"
                    path_msg += "\n添加方法：\n"
                    path_msg += "1. 按Win+X，选择'系统'\n"
                    path_msg += "2. 点击'高级系统设置'\n"
                    path_msg += "3. 点击'环境变量'\n"
                    path_msg += "4. 在'用户变量'中找到'Path'\n"
                    path_msg += "5. 点击'编辑'并添加上述路径\n"
                    path_msg += "6. 重启终端和应用程序"
                    
                    self.log(path_msg)
            
            if not failed_tools and not path_setup_needed:
                ttk.Label(
                    result_frame,
                    text="✅ 所有工具安装成功！",
                    font=("微软雅黑", 12, "bold")
                ).pack(pady=5)
            
            ttk.Button(
                result_frame,
                text="重启应用",
                command=self.restart_app,
                bootstyle="success"
            ).pack(pady=10)
        
        threading.Thread(target=install_thread).start()

    def restart_app(self):
        """重启应用"""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def show_guide(self):
        """显示使用指南"""
        guide_text = """🎯 使用指南

1. 基本操作
• 在目标地址栏输入要测试的网站地址
• 在工具选择区勾选需要使用的工具
• 点击"开始扫描"按钮开始测试
• 可随时点击"停止扫描"终止操作

2. 注意事项
• 使用前请确保已安装所需工具
• 建议先使用基础工具进行扫描
• 扫描过程中请遵守相关法律法规
• 建议在授权情况下使用本工具

3. 快捷操作
• Ctrl+S：保存日志
• Ctrl+Q：退出程序
• F5：清除日志
• F1：显示帮助

4. 主题切换
• 可根据使用场景选择不同主题
• 夜间模式更护眼
• 支持自定义主题色彩"""

        self._show_help_window("使用指南", guide_text)

    def show_tools_info(self):
        """显示工具说明"""
        tools_text = """
        🛠️ 工具说明

1. curl
• 功能：HTTP请求测试工具
• 用途：测试网站响应和HTTP头信息
• 特点：轻量级、易用、标准输出

2. nmap
• 功能：网络扫描和端口检测
• 用途：发现开放端口和服务版本
• 特点：功能强大、可定制性高

3. subfinder
• 功能：子域名发现工具
• 用途：收集目标的所有子域名
• 特点：速度快、准确率高

4. httpx
• 功能：HTTP探测工具
• 用途：批量探测HTTP服务
• 特点：支持多端口、识别技术栈

5. dirsearch
• 功能：目录扫描工具
• 用途：发现网站隐藏目录
• 特点：内置字典、支持多线程

6. xsstrike
• 功能：XSS漏洞扫描
• 用途：检测跨站脚本漏洞
• 特点：智能检测、支持DOM XSS

7. sqlmap
• 功能：SQL注入检测
• 用途：自动化SQL注入测试
• 特点：支持多种数据库、自动绕过"""

        self._show_help_window("工具说明", tools_text)

    def check_update(self):
        """检查更新"""
        update_text = """
        ✨ 版本信息

当前版本：v1.0
发布日期：2024-01
最新版本：v1.0

您的软件已经是最新版本！

如需获取最新版本信息，请关注：
• GitHub: github.com/johnmelodyme
• 邮箱: johnmelodymel@qq.com
• QQ: 3072486255"""

        self._show_help_window("检查更新", update_text)

    def _show_help_window(self, title, content):
        """通用帮助窗口显示函数"""
        help_window = ttk.Toplevel(self.root)
        help_window.title(title)
        help_window.geometry("500x600")
        
        # 创建内容框架
        content_frame = ttk.Frame(help_window, padding=20)
        content_frame.pack(fill=BOTH, expand=True)
        
        # 添加标题
        ttk.Label(
            content_frame,
            text=title,
            font=("微软雅黑", 18, "bold")
        ).pack(pady=(0, 20))
        
        # 添加内容
        text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            height=20,
            font=("微软雅黑", 11)
        )
        text.pack(expand=True, fill=BOTH)
        text.insert("1.0", content)
        text.configure(state="disabled")
        
        # 添加确定按钮
        ttk.Button(
            content_frame,
            text="确定",
            command=help_window.destroy,
            style="primary.TButton"
        ).pack(pady=(20, 0))

if __name__ == "__main__":
    root = ttk.Window(themename="vapor")
    try:
        icon_path = os.path.join("assets", "logo.png")
        if os.path.exists(icon_path):
            img = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, img)
        else:
            if sys.platform == "darwin":
                icon_path = os.path.join("assets", "logo.png")  
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    root.iconphoto(True, img)
            elif sys.platform == "win32":
                icon_path = os.path.join("assets", "logo.ico")
                if os.path.exists(icon_path):
                    root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Warning: Could not load application icon: {e}")
    
    app = BugBountyApp(root)
    root.mainloop()
