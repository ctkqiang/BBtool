# -*- coding: utf-8 -*-

import sys
import subprocess
from pathlib import Path

def clean(paths):
    for path in paths:
        if path.exists():
            print(f"🧹 清理旧文件: {path}")
            if path.is_file():
                path.unlink()
            else:
                subprocess.run(["rm", "-rf", str(path)])

def build_mac(script_name, icon_path, app_name):
    print("🍎 macOS 平台，开始打包 .app...")
    cmd = [
        "pyinstaller", "--windowed", "--noconsole",
        f"--icon={icon_path}",
        f"--name={app_name}",
        script_name
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("❌ 打包失败：\n", result.stderr)
        return

    app_path = Path("dist") / f"{app_name}.app"
    if app_path.exists():
        print(f"✅ .app 打包完成：{app_path.resolve()}")
        subprocess.run(["touch", str(app_path)])
        subprocess.run(["killall", "Finder"])

        create_dmg(app_path, app_name)
    else:
        print("⚠️ 未找到 .app 文件")

def create_dmg(app_path: Path, app_name: str):
    dmg_path = Path("dist") / f"{app_name}.dmg"
    temp_dir = Path("dist/dmg_temp")
    app_link = temp_dir / app_path.name
    apps_link = temp_dir / "Applications"

    print("📦 正在创建 .dmg 安装包...")

    # 创建临时目录并链接 .app 和系统 Applications 文件夹
    temp_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-R", str(app_path), str(app_link)])
    subprocess.run(["ln", "-s", "/Applications", str(apps_link)])

    # 使用 hdiutil 创建 dmg
    subprocess.run([
        "hdiutil", "create", "-volname", app_name,
        "-srcfolder", str(temp_dir),
        "-ov", "-format", "UDZO",
        str(dmg_path)
    ])

    # 清理临时目录
    subprocess.run(["rm", "-rf", str(temp_dir)])
    print(f"✅ .dmg 创建完成：{dmg_path.resolve()}")

    subprocess.run(["open", "dist"])

def build_windows(script_name, icon_path, app_name):
    print("🔧 Windows 平台，开始打包 EXE...")
    cmd = [
        "pyinstaller", "--windowed", "--noconsole",
        f"--icon={icon_path}",
        f"--name={app_name}",
        script_name
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("✅ Windows EXE 打包完成")
    else:
        print("❌ 打包失败：\n", result.stderr)

def build():
    script_name = "main.py"
    icon_win = "./assets/logo.ico"
    icon_mac = "./assets/logo.icns"
    app_name = "漏洞赏金工具"

    clean([
        Path("dist"),
        Path("build"),
        Path(f"{app_name}.spec")
    ])

    if sys.platform == "darwin":
        build_mac(script_name, icon_mac, app_name)
    elif sys.platform == "win32":
        build_windows(script_name, icon_win, app_name)
    else:
        print(f"❌ 当前平台 {sys.platform} 暂不支持打包")

if __name__ == "__main__":
    build()
