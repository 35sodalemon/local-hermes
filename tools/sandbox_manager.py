"""
Docker 沙盒管理器

为非管理员用户提供隔离的代码执行环境。
- 每个用户最多一个沙盒（归属人绑定 user_id）
- 子区内共享沙盒（任何用户可使用子区内已有的沙盒）
- 归属人创建新沙盒时，旧沙盒自动销毁
- 闲置 5 分钟自动销毁
"""

import json
import logging
import os
import subprocess
import time
import threading

from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# 沙盒配置
SANDBOX_IMAGE = "hermes-sandbox:latest"
MAX_CONCURRENT = 2          # 最大并发沙盒数
IDLE_TIMEOUT = 120          # 闲置超时（秒，2分钟）
MAX_QUEUE = 3               # 最大排队数
EXEC_TIMEOUT = 60           # 单次执行超时（秒）
CONTAINER_PREFIX = "hermes_sandbox_"


class SandboxManager:
    """Docker 沙盒管理器"""

    def __init__(self):
        # user_id -> {container_id, container_name, workspace, created_at, last_active, thread_id, label}
        self._user_sandboxes: Dict[str, dict] = {}
        # thread_id -> user_id（子区归属人）
        self._thread_sandboxes: Dict[str, str] = {}
        self._lock = threading.RLock()
        self._queue_count = 0
        # 沙盒标记计数器（a-z轮回）
        self._label_counter = 0

    def _next_label(self) -> str:
        """获取下一个沙盒标记（a-z轮回）"""
        label = chr(ord('a') + self._label_counter % 26)
        self._label_counter += 1
        return label

    def _run_docker(self, args: list, timeout: int = 30) -> dict:
        """执行 docker 命令"""
        cmd = ["docker"] + args
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            return {
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Docker 命令超时", "returncode": -1}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": -1}

    def _container_name(self, user_id: str) -> str:
        """生成容器名称"""
        safe_id = (user_id or "unknown").replace("/", "_").replace(".", "_")[-30:]
        return f"{CONTAINER_PREFIX}{safe_id}"

    def _get_active_count(self) -> int:
        """获取当前活跃沙盒数"""
        result = self._run_docker([
            "ps", "--filter", f"name={CONTAINER_PREFIX}", "-q"
        ])
        if result["returncode"] == 0 and result["stdout"]:
            return len(result["stdout"].split("\n"))
        return 0

    def _create_workspace(self, user_id: str) -> str:
        """创建沙盒工作目录"""
        workspace = f"/tmp/hermes_sandbox_{user_id}"
        os.makedirs(workspace, exist_ok=True)
        return workspace

    def _is_container_running(self, container_id: str) -> bool:
        """检查容器是否在运行（不持锁调用）"""
        result = self._run_docker(["inspect", "-f", "{{.State.Running}}", container_id])
        return result["returncode"] == 0 and "true" in result["stdout"].lower()

    def _destroy_user_sandbox(self, user_id: str) -> dict:
        """销毁指定用户的沙盒（内部方法，调用者需持锁）
        返回需要在锁外执行的清理信息"""
        if user_id not in self._user_sandboxes:
            return {}

        info = self._user_sandboxes.pop(user_id)
        container_name = info["container_name"]

        # 从子区映射中移除
        thread_id = info.get("thread_id")
        if thread_id and self._thread_sandboxes.get(thread_id) == user_id:
            del self._thread_sandboxes[thread_id]

        # 返回需要在锁外执行的清理信息
        return {
            "container_name": container_name,
            "workspace": info.get("workspace", ""),
        }

    def _cleanup_sandbox_resources(self, cleanup_info: dict):
        """在锁外清理沙盒资源（docker rm + 目录清理）"""
        if not cleanup_info:
            return
        container_name = cleanup_info.get("container_name", "")
        workspace = cleanup_info.get("workspace", "")
        
        # 停止并删除容器
        if container_name:
            self._run_docker(["rm", "-f", container_name])
        
        # 清理工作目录
        if workspace and os.path.exists(workspace):
            import shutil
            shutil.rmtree(workspace, ignore_errors=True)
        
        if container_name:
            logger.info("Sandbox destroyed: %s", container_name)

    def get_or_create(self, user_id: str, thread_id: str = None) -> Optional[str]:
        """
        获取或创建沙盒，返回容器 ID

        逻辑：
        1. 检查当前子区是否有沙盒 → 有则复用
        2. 没有 → 检查用户是否已有沙盒 → 有则复用或重建
        3. 创建新沙盒
        """
        # 1. 检查子区是否已有沙盒（任何用户创建的）
        if thread_id:
            with self._lock:
                owner_id = self._thread_sandboxes.get(thread_id)
                if owner_id and owner_id in self._user_sandboxes:
                    container_id = self._user_sandboxes[owner_id]["container_id"]
                else:
                    owner_id = None
                    container_id = None

            # 锁外检查容器状态
            if owner_id and container_id:
                if self._is_container_running(container_id):
                    with self._lock:
                        if owner_id in self._user_sandboxes:
                            self._user_sandboxes[owner_id]["last_active"] = time.time()
                    return container_id
                else:
                    # 容器已销毁，清理映射
                    with self._lock:
                        if thread_id in self._thread_sandboxes:
                            del self._thread_sandboxes[thread_id]

        # 2. 检查用户是否已有沙盒
        with self._lock:
            if user_id in self._user_sandboxes:
                container_id = self._user_sandboxes[user_id]["container_id"]
            else:
                container_id = None

        # 锁外检查容器状态
        if container_id:
            if self._is_container_running(container_id):
                with self._lock:
                    if user_id in self._user_sandboxes:
                        self._user_sandboxes[user_id]["last_active"] = time.time()
                return container_id
            else:
                # 容器已销毁，清理记录
                with self._lock:
                    if user_id in self._user_sandboxes:
                        self._destroy_user_sandbox(user_id)

        # 3. 检查并发限制（锁外查询 docker）
        active_count = self._get_active_count()
        if active_count >= MAX_CONCURRENT:
            with self._lock:
                if self._queue_count >= MAX_QUEUE:
                    return None
                self._queue_count += 1

            # 等待空闲沙盒
            try:
                for _ in range(30):
                    time.sleep(1)
                    if self._get_active_count() < MAX_CONCURRENT:
                        break
                else:
                    return None
            finally:
                with self._lock:
                    self._queue_count -= 1

        # 4. 如果用户已有沙盒，销毁旧的
        with self._lock:
            cleanup_info = {}
            if user_id in self._user_sandboxes:
                cleanup_info = self._destroy_user_sandbox(user_id)
        self._cleanup_sandbox_resources(cleanup_info)

        # 5. 创建新沙盒
        return self._create(user_id, thread_id)

    def _create(self, user_id: str, thread_id: str = None) -> Optional[str]:
        """创建新的沙盒容器"""
        container_name = self._container_name(user_id)
        workspace = self._create_workspace(user_id)

        # 先清理同名容器（如果存在）
        self._run_docker(["rm", "-f", container_name])

        # 创建容器（安全加固）
        result = self._run_docker([
            "run", "-d",
            "--name", container_name,
            "-v", f"{workspace}:/tmp/workspace",
            "--memory", "512m",
            "--cpus", "0.5",
            "--network", "none",
            "--read-only",
            "--pids-limit", "100",
            "--tmpfs", "/tmp:size=64m,noexec,nosuid",
            "--tmpfs", "/run:size=8m",
            SANDBOX_IMAGE,
            "sleep", "infinity",
        ], timeout=60)

        if result["returncode"] != 0:
            logger.error("Failed to create sandbox: %s", result["stderr"])
            return None

        container_id = result["stdout"]
        
        # 分配沙盒标记
        label = self._next_label()

        with self._lock:
            self._user_sandboxes[user_id] = {
                "container_id": container_id,
                "container_name": container_name,
                "workspace": workspace,
                "created_at": time.time(),
                "last_active": time.time(),
                "thread_id": thread_id,
                "label": label,
            }
            # 如果有 thread_id，记录子区归属
            if thread_id:
                self._thread_sandboxes[thread_id] = user_id

        logger.info("Sandbox created for user %s: %s (thread: %s, label: %s)", user_id, container_name, thread_id, label)
        return container_id

    def execute(self, user_id: str, command: str, timeout: int = EXEC_TIMEOUT) -> dict:
        """在沙盒内执行命令"""
        container_name = self._container_name(user_id)

        # 检查容器是否存在
        result = self._run_docker(["inspect", "-f", "{{.State.Running}}", container_name])
        if result["returncode"] != 0 or "true" not in result["stdout"].lower():
            return {"success": False, "error": "沙盒容器不存在", "exit_code": -1}

        # 更新活跃时间
        label = ""
        with self._lock:
            if user_id in self._user_sandboxes:
                self._user_sandboxes[user_id]["last_active"] = time.time()
                label = self._user_sandboxes[user_id].get("label", "")

        # 在容器内执行命令
        result = self._run_docker([
            "exec", container_name,
            "bash", "-c", command,
        ], timeout=timeout)

        return {
            "success": result["returncode"] == 0,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "exit_code": result["returncode"],
            "label": label,
        }

    def execute_python(self, user_id: str, code: str, timeout: int = EXEC_TIMEOUT) -> dict:
        """在沙盒内执行 Python 代码（通过 stdin 管道传递，避免命令行注入）"""
        container_name = self._container_name(user_id)

        # 检查容器是否存在
        result = self._run_docker(["inspect", "-f", "{{.State.Running}}", container_name])
        if result["returncode"] != 0 or "true" not in result["stdout"].lower():
            return {"success": False, "error": "沙盒容器不存在", "exit_code": -1}

        # 更新活跃时间
        label = ""
        with self._lock:
            if user_id in self._user_sandboxes:
                self._user_sandboxes[user_id]["last_active"] = time.time()
                label = self._user_sandboxes[user_id].get("label", "")

        # 通过 stdin 管道传递代码（避免命令行注入 + 兼容 read-only 容器）
        cmd = ["docker", "exec", "-i", container_name, "python3", "-"]
        try:
            proc = subprocess.run(
                cmd, input=code, capture_output=True, text=True, timeout=timeout
            )
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "exit_code": proc.returncode,
                "label": label,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "执行超时", "exit_code": -1}
        except Exception as e:
            return {"success": False, "error": str(e), "exit_code": -1}

    def destroy_user(self, user_id: str):
        """销毁指定用户的沙盒"""
        with self._lock:
            cleanup_info = self._destroy_user_sandbox(user_id)
        self._cleanup_sandbox_resources(cleanup_info)

    def cleanup_idle(self):
        """清理所有闲置超时的沙盒"""
        now = time.time()
        idle_users = []

        with self._lock:
            for user_id, info in self._user_sandboxes.items():
                if now - info["last_active"] > IDLE_TIMEOUT:
                    idle_users.append(user_id)

        for user_id in idle_users:
            logger.info("Cleaning up idle sandbox for user: %s", user_id)
            with self._lock:
                cleanup_info = self._destroy_user_sandbox(user_id)
            self._cleanup_sandbox_resources(cleanup_info)

    def cleanup_all(self):
        """清理所有沙盒（网关重启时调用）"""
        with self._lock:
            user_ids = list(self._user_sandboxes.keys())

        cleanup_infos = []
        for user_id in user_ids:
            with self._lock:
                cleanup_info = self._destroy_user_sandbox(user_id)
            cleanup_infos.append(cleanup_info)
        
        for cleanup_info in cleanup_infos:
            self._cleanup_sandbox_resources(cleanup_info)

        # 额外清理：删除所有 hermes_sandbox_ 开头的容器
        result = self._run_docker([
            "ps", "-a", "--filter", f"name={CONTAINER_PREFIX}", "-q"
        ])
        if result["returncode"] == 0 and result["stdout"]:
            for container_id in result["stdout"].split("\n"):
                if container_id.strip():
                    self._run_docker(["rm", "-f", container_id.strip()])

        logger.info("All sandboxes cleaned up")

    def get_status(self) -> dict:
        """获取沙盒状态"""
        with self._lock:
            active = len(self._user_sandboxes)
            sandboxes = {}
            for uid, info in self._user_sandboxes.items():
                sandboxes[uid] = {
                    "container_name": info["container_name"],
                    "thread_id": info.get("thread_id"),
                    "created_at": info["created_at"],
                    "last_active": info["last_active"],
                    "idle_seconds": time.time() - info["last_active"],
                }

        return {
            "active_count": active,
            "max_concurrent": MAX_CONCURRENT,
            "idle_timeout": IDLE_TIMEOUT,
            "sandboxes": sandboxes,
            "thread_map": dict(self._thread_sandboxes),
        }


# 全局单例
sandbox_manager = SandboxManager()

# 启动自动清理线程
def _start_cleanup_thread():
    """启动后台清理线程，每分钟检查一次闲置沙盒"""
    import atexit
    def _cleanup_loop():
        while True:
            time.sleep(60)
            try:
                sandbox_manager.cleanup_idle()
            except Exception as e:
                logger.debug("Sandbox cleanup error: %s", e)
    t = threading.Thread(target=_cleanup_loop, daemon=True)
    t.start()
    # 网关退出时清理所有沙盒
    atexit.register(sandbox_manager.cleanup_all)

_start_cleanup_thread()
