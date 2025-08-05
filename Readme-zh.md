# FilebackUp - 文件备份工具

## 项目概述

FilebackUp 是一个功能强大的文件备份工具，支持完整备份、增量备份和差异备份三种备份策略。该工具可以根据文件重要性将待备份文件分为高、中、低三个优先级，并针对不同级别的文件采用不同的备份策略，从而提高备份效率并节省存储空间。

## 功能特点

- **多级备份策略**：支持将文件分为高、中、低三个优先级，实现差异化备份
- **完整备份**：一次性备份所有文件，适合首次备份
- **增量备份**：仅备份新增文件，适合中级优先级文件的定期备份
- **差异备份**：备份已修改的文件，适合高级优先级文件的实时保护
- **数据库支持**：使用SQLite数据库记录备份历史和文件信息
- **文件哈希校验**：通过MD5哈希值检测文件变化
- **邮件通知**：备份完成后自动发送通知邮件
- **日志记录**：详细记录备份过程和可能的错误

## 安装要求

- Python 3.6+
- SQLAlchemy
- PyYAML

## 安装步骤

1. 克隆仓库到本地：

```sh
git clone https://github.com/yourusername/FilebackUp.git
cd FilebackUp
```

2. 安装依赖：

```sh
pip install -r requirements.txt
```



## 配置说明

在使用前，需要在 `config/config.yaml` 文件中配置以下信息：

```yaml
# 邮箱配置
email: your-email@qq.com
# 邮箱授权码, 请注意授权码不等于密码
PassCode: your-email-auth-code
port: 587
SendTo: recipient-email@example.com

# 文件分级配置
HighLevelFiles:
  - high_priority_dir: "/path/to/important/files"

MidLevelFiles:
  - HighInMid: 
    - high_dir1: "/path/to/important/files/in/mid"
  - mid_dir1: "/path/to/mid/priority/files"
  - mid_dir2: "/path/to/another/mid/files"

LowLevelFiles:
  - low_dir1: "/path/to/low/priority/files"
```

## 使用方法

基本用法：

```sh
python file_backup.py -o /path/to/backup/destination
```

强制执行完整备份：

```sh
python file_backup.py -o /path/to/backup/destination -f
```

参数说明：

- `-o, --output`: 指定备份文件存放的目标目录
- `-f, --force`: 强制执行完整备份，不考虑之前的备份状态

## 工作原理

1. **完整备份**：
   - 首次备份或使用 `-f` 参数时执行
   - 备份所有级别的文件
   - 记录文件哈希值和路径到数据库
2. **增量备份**：
   - 对中级优先级文件执行
   - 只备份数据库中不存在的新文件
   - 更新数据库记录
3. **差异备份**：
   - 对高级优先级文件执行
   - 通过比较文件哈希值检测变化
   - 备份已修改的文件并更新数据库

## 项目结构

```
FilebackUp/
├── config/
│   └── config.yaml          # 配置文件
├── core/
│   ├── cal_file_hash.py     # 计算文件哈希值
│   ├── check_is_backuped.py # 检查是否已备份
│   ├── db.py                # 数据库操作
│   ├── decorators.py        # 装饰器函数
│   ├── differential_backup.py # 差异备份
│   ├── full_backup.py       # 完整备份
│   ├── get_config.py        # 获取配置
│   ├── get_file_size.py     # 获取文件大小
│   ├── get_parm.py          # 获取命令行参数
│   ├── global_vars.py       # 全局变量管理
│   ├── incremental_backup.py # 增量备份
│   ├── logger.py            # 日志管理
│   ├── send_message.py      # 发送邮件通知
│   └── setting.py           # 数据库设置
├── file_backup.py           # 主程序
└── Readme-zh.md             # 中文说明文档
└── Readme.md								 # 英文说明文档
```

## 数据库结构

工具使用SQLite数据库存储以下信息：

1. **HIGH_LEVEL_FILES**：高优先级文件表
   - 文件名、路径、大小、哈希值、是否新增、是否修改
2. **MID_LEVEL_FILES**：中优先级文件表
   - 文件名、路径、大小、是否新增
3. **LOW_LEVEL_FILES**：低优先级文件表
   - 文件名、路径、大小
4. **IS_BACKUPED**：备份状态表
   - 目标路径信息

## 性能优化

- 使用多级备份策略减少重复备份
- 通过文件哈希值快速检测变化
- 装饰器实现备份性能统计

## 常见问题

1. **备份失败**
   - 检查目标路径权限
   - 确保配置文件正确
   - 查看日志文件了解详细错误
2. **邮件发送失败**
   - 确认邮箱授权码正确
   - 检查网络连接
3. **数据库错误**
   - 检查数据库文件权限
   - 在首次运行时会自动创建数据库

## 贡献指南

欢迎贡献代码或提出建议，请通过以下步骤参与：

1. Fork 项目仓库
2. 创建功能分支
3. 提交变更
4. 创建 Pull Request

## 许可证

Apache-2.0 License
