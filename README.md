# 🕷️ 漏洞赏金工具 v1.0

## 🌟 项目简介

漏洞赏金工具是一款专为安全研究人员和白帽子黑客设计的图形化渗透测试工具集。它集成了多个常用的安全测试工具，提供了直观的用户界面，让漏洞挖掘变得更加简单和高效。

## 🖼️ 功能演示

### 主界面

![主界面](assets/demo/1.png)

## ✨ 主要特性

- 🎨 美观的图形界面

  - 支持多种主题切换（超级英雄风、赛博朋克、暗黑模式等）
  - 实时日志输出展示
  - 简洁直观的工具选择界面

- 🛠️ 集成多种渗透测试工具

  - curl：HTTP 请求测试
  - nmap：端口扫描和服务检测
  - subfinder：子域名发现
  - httpx：HTTP 服务探测
  - dirsearch：Web 目录扫描
  - xsstrike：XSS 漏洞扫描
  - sqlmap：SQL 注入检测
  - hakrawler：Web 爬虫工具

- 🚀 便捷的操作体验

  - 一键启动多个工具
  - 实时查看扫描进度
  - 随时暂停/继续扫描
  - 日志导出功能

- 🔧 高度可定制
  - SQLMap 高级选项配置
  - 自定义工具参数
  - 灵活的主题切换

## 📦 环境要求

- Python 3.7+
- 操作系统支持：
  - macOS
  - Windows
  - Linux

## 🔨 安装步骤

1. 克隆项目代码：

```bash
git clone https://github.com/johnmelodyme/bug-bounty-tool.git
cd bug-bounty-tool
```

2. 安装依赖：

```bash
pip3 install -r requirements.txt
```

3. 安装必要的工具：

### macOS

```bash
# 使用 Homebrew 安装基础工具
brew install curl nmap subfinder httpx

# 使用 pip 安装 Python 工具
pip3 install dirsearch xsstrike sqlmap

# 使用 Go 安装其他工具
go install github.com/hakluke/hakrawler@latest
```

### Linux

```bash
# 安装基础工具
sudo apt-get install curl nmap

# 安装 Go 工具
GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/hakluke/hakrawler@latest

# 安装 Python 工具
pip3 install dirsearch xsstrike sqlmap
```

### Windows

```powershell
# 使用 winget 安装基础工具
winget install curl nmap

# 安装 Go 工具
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/hakluke/hakrawler@latest

# 安装 Python 工具
pip3 install dirsearch xsstrike sqlmap
```

## 🚀 使用指南

1. 启动程序：

```bash
python3 main.py
```

2. 基本操作流程：

   - 在目标地址栏输入要测试的网站地址
   - 在工具选择区勾选需要使用的工具
   - 点击"开始扫描"按钮开始测试
   - 可随时点击"停止扫描"终止操作

3. SQLMap 高级选项：

   - 基础模式：基本的 SQL 注入测试
   - 高风险测试：使用更激进的测试方法
   - POST 请求：测试 POST 参数注入
   - Cookie 注入：测试 Cookie 中的注入点
   - 自定义头：添加自定义 HTTP 头
   - 枚举数据库：列出所有数据库
   - 枚举表：列出指定数据库的表
   - 枚举字段：列出指定表的字段
   - Dump 数据：导出指定数据
   - 代理模式：使用代理进行测试
   - OS Shell：尝试获取系统 Shell

4. 主题切换：

   - superhero：夜晚超级英雄风，深色高对比
   - vapor：赛博朋克紫色调，未来感满满
   - darkly：暗黑风格，柔和护眼
   - cyborg：机械感黑色主题
   - solar：明亮温暖的阳光色系

5. 快捷键操作：
   - Ctrl+S：保存日志
   - Ctrl+Q：退出程序
   - F5：清除日志
   - F1：显示帮助

## 📝 注意事项

1. 使用安全：

   - 请在获得授权的情况下使用本工具
   - 遵守相关法律法规
   - 不要对未经授权的目标进行测试

2. 工具使用建议：

   - 建议先使用基础工具进行扫描
   - 根据扫描结果选择性使用高级选项
   - 重要操作前请先保存日志
   - 定期检查工具更新

3. 性能优化：
   - 避免同时运行过多工具
   - 大型目标建议分批次扫描
   - 及时清理日志避免内存占用

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

1. Fork 本仓库
2. 创建您的特性分支 (git checkout -b feature/AmazingFeature)
3. 提交您的更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 打开一个 Pull Request

## 👥 作者

- 作者：钟智强
- 邮箱：johnmelodymel@qq.com
- QQ：3072486255
- 微信：ctkqiang

## 🙏 致谢

感谢以下开源项目，没有它们就没有这个工具：

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [curl](https://curl.se/)
- [nmap](https://nmap.org/)
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [httpx](https://github.com/projectdiscovery/httpx)
- [dirsearch](https://github.com/maurosoria/dirsearch)
- [xsstrike](https://github.com/s0md3v/XSStrike)
- [sqlmap](https://sqlmap.org/)
- [hakrawler](https://github.com/hakluke/hakrawler)

## 📞 联系方式

如果您有任何问题或建议，欢迎通过以下方式联系我：

- GitHub Issues
- 邮箱：johnmelodymel@qq.com
- QQ：3072486255
- 微信：ctkqiang

## 🔄 更新日志

### v1.0 (2024-01)

- 🎉 首次发布
- 🎨 支持多种主题切换
- 🛠️ 集成多种渗透测试工具
- 📝 完善的日志记录功能
- 🔧 SQLMap 高级选项支持

## 许可证

本项目采用 **木兰宽松许可证 (Mulan PSL)** 进行许可。  
有关详细信息，请参阅 [LICENSE](LICENSE) 文件。  
（魔法契约要保管好哟~）

[![License: Mulan PSL v2](https://img.shields.io/badge/License-Mulan%20PSL%202-blue.svg)](http://license.coscl.org.cn/MulanPSL2)

## 🌟 开源项目赞助计划

### 用捐赠助力发展

感谢您使用本项目！您的支持是开源持续发展的核心动力。  
每一份捐赠都将直接用于：  
✅ 服务器与基础设施维护（魔法城堡的维修费哟~）  
✅ 新功能开发与版本迭代（魔法技能树要升级哒~）  
✅ 文档优化与社区建设（魔法图书馆要扩建呀~）

点滴支持皆能汇聚成海，让我们共同打造更强大的开源工具！  
（小仙子们在向你比心哟~）

---

### 🌐 全球捐赠通道

#### 国内用户

<div align="center" style="margin: 40px 0">

<div align="center">
<table>
<tr>
<td align="center" width="300">
<img src="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9863.jpg?raw=true" width="200" />
<br />
<strong>🔵 支付宝</strong>（小企鹅在收金币哟~）
</td>
<td align="center" width="300">
<img src="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9859.JPG?raw=true" width="200" />
<br />
<strong>🟢 微信支付</strong>（小绿龙在收金币哟~）
</td>
</tr>
</table>
</div>
</div>

#### 国际用户

<div align="center" style="margin: 40px 0">
  <a href="https://qr.alipay.com/fkx19369scgxdrkv8mxso92" target="_blank">
    <img src="https://img.shields.io/badge/Alipay-全球支付-00A1E9?style=flat-square&logo=alipay&logoColor=white&labelColor=008CD7">
  </a>
  
  <a href="https://ko-fi.com/F1F5VCZJU" target="_blank">
    <img src="https://img.shields.io/badge/Ko--fi-买杯咖啡-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white">
  </a>
  
  <a href="https://www.paypal.com/paypalme/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/PayPal-安全支付-00457C?style=flat-square&logo=paypal&logoColor=white">
  </a>
  
  <a href="https://donate.stripe.com/00gg2nefu6TK1LqeUY" target="_blank">
    <img src="https://img.shields.io/badge/Stripe-企业级支付-626CD9?style=flat-square&logo=stripe&logoColor=white">
  </a>
</div>

---

### 📌 开发者社交图谱

#### 技术交流

<div align="center" style="margin: 20px 0">
  <a href="https://github.com/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-开源仓库-181717?style=for-the-badge&logo=github">
  </a>
  
  <a href="https://stackoverflow.com/users/10758321/%e9%92%9f%e6%99%ba%e5%bc%ba" target="_blank">
    <img src="https://img.shields.io/badge/Stack_Overflow-技术问答-F58025?style=for-the-badge&logo=stackoverflow">
  </a>
  
  <a href="https://www.linkedin.com/in/ctkqiang/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-职业网络-0A66C2?style=for-the-badge&logo=linkedin">
  </a>
</div>

#### 社交互动

<div align="center" style="margin: 20px 0">
  <a href="https://www.instagram.com/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-生活瞬间-E4405F?style=for-the-badge&logo=instagram">
  </a>
  
  <a href="https://twitch.tv/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/Twitch-技术直播-9146FF?style=for-the-badge&logo=twitch">
  </a>
  
  <a href="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9245.JPG?raw=true" target="_blank">
    <img src="https://img.shields.io/badge/微信公众号-钟智强-07C160?style=for-the-badge&logo=wechat">
  </a>
</div>

---

🙌 感谢您成为开源社区的重要一员！  
💬 捐赠后欢迎通过社交平台与我联系，您的名字将出现在项目致谢列表！
