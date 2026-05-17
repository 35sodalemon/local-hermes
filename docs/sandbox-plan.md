# 非管理员 Docker 沙盒执行方案

## 一、目标

非管理员用户执行 terminal/execute_code 时，自动创建隔离的 Docker 容器，所有操作在容器内完成。对话结束后销毁容器，释放资源。

## 二、服务器资源

- 配置：2核4G（首尔机房）
- 并发上限：2 个沙盒同时运行
- 单个沙盒资源：0.5核 / 512MB内存 / 100MB磁盘

## 三、沙盒触发条件

### DM（私信）场景
- 管理员：直接操作宿主机，不受限制
- 非管理员：执行敏感操作时自动进入沙盒，受限制

### 频道子区场景
- 默认：所有人（包括管理员）执行敏感操作都在沙盒内运行，所有人都受沙盒限制
- 管理员特权：可以主动要求在宿主机内操作（`host: true`），此时不受限制

### 触发（创建沙盒）
- 非管理员调用 terminal 工具
- 非管理员调用 execute_code 工具
- 管理员在子区中调用 terminal/execute_code（默认走沙盒）

### 不触发（复用现有机制）
- 非管理员普通对话 → LLM 直接回答
- 非管理员读写文件 → 路径检查（当前方案）
- 管理员在 DM 中所有操作 → 无限制
- 管理员在子区中使用 `host: true` → 直接宿主机执行

## 四、沙盒生命周期

```
用户调用 terminal/execute_code
  ↓
判断是否走沙盒（DM/子区 + 管理员/非管理员）
  ↓
走沙盒 → 检查当前 user_id 是否有沙盒
  ↓
没有 → 创建 Docker 容器 → 执行 → 返回结果
  ↓
有 → docker exec 复用容器 → 执行 → 返回结果
  ↓
闲置 2 分钟 → 自动销毁容器
  ↓
网关重启 → 清理所有残留容器
```

## 五、Docker 镜像设计

### 基础镜像：hermes-sandbox

```dockerfile
FROM python:3.11-slim

# 设置中文环境
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 安装系统工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make \
    gdb strace \
    nmap netcat-traditional \
    curl wget \
    vim nano \
    git \
    file \
    unzip \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 常用库（CTF + 数据分析）
RUN pip install --no-cache-dir \
    pwntools \
    requests \
    numpy \
    pandas \
    pycryptodome \
    sympy \
    gmpy2 \
    z3-solver \
    ropper \
    ROPgadget \
    capstone \
    keystone-engine \
    unicorn \
    flask \
    scapy

# 创建非 root 用户
RUN useradd -m -s /bin/bash sandbox && \
    mkdir -p /tmp/workspace && \
    chown sandbox:sandbox /tmp/workspace

USER sandbox
WORKDIR /tmp/workspace

# 默认命令
CMD ["bash"]
```

### 镜像体积：~1.67GB

## 六、核心代码改动

### 1. sandbox_manager.py

```python
class SandboxManager:
    """Docker 沙盒管理器"""
    
    SANDBOX_IMAGE = "hermes-sandbox:latest"
    MAX_CONCURRENT = 2          # 最大并发沙盒数
    IDLE_TIMEOUT = 120          # 闲置超时（秒，2分钟）
    MAX_QUEUE = 3               # 最大排队数
    EXEC_TIMEOUT = 60           # 单次执行超时（秒）
    
    def __init__(self):
        self._user_sandboxes: Dict[str, dict] = {}  # user_id -> sandbox info
        self._thread_sandboxes: Dict[str, str] = {}  # thread_id -> user_id
        self._lock = threading.RLock()
        self._queue_count = 0
        self._label_counter = 0  # 沙盒标记计数器（a-z轮回）
    
    def _next_label(self) -> str:
        """获取下一个沙盒标记（a-z轮回）"""
        label = chr(ord('a') + self._label_counter % 26)
        self._label_counter += 1
        return label
    
    def get_or_create(self, user_id: str, thread_id: str = None) -> Optional[str]:
        """获取或创建沙盒，返回容器 ID"""
        
    def execute(self, user_id: str, command: str, timeout: int = EXEC_TIMEOUT) -> dict:
        """在沙盒内执行命令"""
        
    def execute_python(self, user_id: str, code: str, timeout: int = EXEC_TIMEOUT) -> dict:
        """在沙盒内执行 Python 代码（通过 stdin 管道传递）"""
        
    def destroy_user(self, user_id: str):
        """销毁指定用户的沙盒"""
        
    def cleanup_idle(self):
        """清理所有闲置超时的沙盒"""
        
    def cleanup_all(self):
        """清理所有沙盒（网关重启时调用）"""
```

### 2. terminal_tool.py 沙盒路由

```python
def _handle_terminal(args, **kw):
    session_id = kw.get("session_id")
    if session_id:
        user_id = _get_user_id_from_session(session_id)
        admin_ids = _get_admin_user_ids()
        is_admin = user_id and str(user_id) in admin_ids
        is_thread = bool(get_session_env('HERMES_SESSION_THREAD_ID', ''))
        
        # 判断是否走沙盒
        use_sandbox = False
        if is_thread:
            # 子区内：默认走沙盒，管理员可用 host=true 跳出
            if is_admin and args.get("host", False):
                use_sandbox = False
            else:
                use_sandbox = True
        else:
            # DM 中：非管理员走沙盒，管理员直接执行
            if not is_admin:
                use_sandbox = True
        
        if use_sandbox:
            # 走沙盒逻辑
            ...
```

### 3. code_execution_tool.py 沙盒路由

与 terminal_tool.py 逻辑相同。

### 4. gateway/run.py 沙盒标记注入

```python
# 检查当前turn的工具输出是否有沙盒标记
_sandbox_prefix = ""
_history_len = agent_result.get("history_offset", len(history))
_new_messages = agent_messages[_history_len:] if len(agent_messages) > _history_len else []

for msg in _new_messages:
    if msg.get("role") == "tool":
        tool_content = msg.get("content", "")
        if isinstance(tool_content, dict):
            tool_output = tool_content.get("output", "")
        elif isinstance(tool_content, str):
            tool_data = json.loads(tool_content)
            tool_output = tool_data.get("output", "")
        else:
            continue
        
        match = re.match(r'(\[🐳[a-z]?(?: 沙盒已创建)?\])', tool_output)
        if match:
            _sandbox_prefix = match.group(1)
            break

# 如果有沙盒标记，加在回复开头
if _sandbox_prefix and response and not response.startswith("[🐳"):
    response = f"{_sandbox_prefix}\n---\n{response}"
```

## 七、沙盒标记系统

### 标记格式
- 新建沙盒：`[🐳a 沙盒已创建]`、`[🐳b 沙盒已创建]`、...
- 复用沙盒：`[🐳a]`、`[🐳b]`、...
- 标记从 a 到 z 依次轮回分配

### 标记注入
- 工具返回时在 output 前面加标记
- gateway 发送回复前检查工具输出，如果有标记就加在回复开头
- 只检查当前 turn 的消息，不检查历史消息

## 八、容器安全加固

```bash
docker run -d \
  --name hermes_sandbox_{user_id} \
  -v /tmp/hermes_sandbox_{user_id}:/tmp/workspace \
  --memory 512m \
  --cpus 0.5 \
  --network none \          # 网络隔离
  --read-only \             # 只读根文件系统
  --pids-limit 100 \        # 限制进程数
  --tmpfs /tmp:size=64m,noexec,nosuid \  # /tmp 可写但不可执行
  --tmpfs /run:size=8m \
  hermes-sandbox:latest \
  sleep infinity
```

## 九、沙盒内文件管理

### 非管理员文件目录
- 宿主机：/tmp/hermes_sandbox_{user_id}/
- 沙盒内：/tmp/workspace/（挂载点）
- write_file 写入这里 → 沙盒内可见
- terminal/execute_code 在这里执行

### 文件挂载
```bash
docker run -v /tmp/hermes_sandbox_{user_id}:/tmp/workspace ...
```

## 十、并发控制

- 最多 2 个沙盒同时运行
- 第 3 个请求排队等待（最多排队 3 个）
- 超过排队上限 → 返回错误："沙盒资源紧张，请稍后重试"

## 十一、清理机制

### 定时清理（每分钟）
- 检查所有沙盒容器的最后活跃时间
- 闲置超过 2 分钟 → 销毁

### 网关重启清理
- 启动时扫描所有 hermes_sandbox 容器
- 全部销毁

### 手动清理
```bash
docker ps -a --filter name=hermes_sandbox_ -q | xargs -r docker rm -f
```

## 十二、已知限制

### 网络隔离
- 沙盒使用 `--network none`，所有网络操作都会失败
- ping、curl、DNS 解析等网络命令无法使用
- 这是安全设计，防止沙盒访问外部网络

### 命令限制
- 沙盒内没有安装所有宿主机的命令
- 已安装：gcc, gdb, nmap, netcat, curl, wget, vim, git, ping, nslookup, dig, host
- 未安装：部分系统管理命令

## 十三、实施状态

### Phase 1：基础沙盒 ✅ 已完成
- [x] 编写 Dockerfile，构建基础镜像
- [x] 实现 SandboxManager 类
- [x] 修改 terminal 工具支持沙盒执行
- [x] 修改 execute_code 工具支持沙盒执行
- [x] 添加定时清理任务
- [x] 测试：非管理员执行命令在沙盒内

### Phase 2：高级功能 ✅ 已完成
- [x] DM/子区区分（管理员在子区也走沙盒）
- [x] 管理员跳出沙盒（host=true 参数）
- [x] 沙盒标记系统（a-z轮回）
- [x] 沙盒标记注入（gateway 层面）
- [x] 容器安全加固（--read-only, --pids-limit, --network none）

### Phase 3：优化（后续）
- [ ] 预热池：预创建空闲容器减少冷启动
- [ ] 资源监控：监控沙盒资源使用
- [ ] 日志审计：记录沙盒内所有操作
- [ ] 网络白名单：允许特定域名的网络访问

## 十四、风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| Docker 未安装 | 安装 Docker + 设置开机自启 |
| 镜像拉取慢 | 预构建并推送到本地 registry |
| 容器逃逸 | 保持 Docker 版本更新 + 非 root 用户 + --read-only |
| 资源耗尽 | 并发限制 + 超时销毁 + --pids-limit |
| 磁盘占满 | 定时清理 + 磁盘配额 |
| 网络攻击 | --network none 完全隔离 |
| 锁内阻塞 | docker 操作移到锁外 |
| TOCTOU 竞态 | 锁内字典操作 + 锁外资源清理 |

## 十五、验证清单

- [x] Docker 安装并运行
- [x] 基础镜像构建成功
- [x] 非管理员 terminal 走沙盒
- [x] 非管理员 execute_code 走沙盒
- [x] 管理员在 DM 中不走沙盒
- [x] 管理员在子区中走沙盒
- [x] 管理员在子区中可用 host=true 跳出沙盒
- [x] 沙盒内无法访问宿主机文件
- [x] 沙盒闲置 2 分钟自动销毁
- [x] 网关重启清理残留
- [x] 并发限制生效
- [x] 命令超时 60 秒
- [x] 沙盒标记系统（a-z轮回）
- [x] 沙盒标记注入（gateway 层面）
- [x] 容器安全加固（--read-only, --pids-limit, --network none）
