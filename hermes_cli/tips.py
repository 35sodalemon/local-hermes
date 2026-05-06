"""Random tips shown at CLI session start to help users discover features."""

import random


# ---------------------------------------------------------------------------
# Tip corpus — one-liners covering slash commands, CLI flags, config,
# keybindings, tools, gateway, skills, profiles, and workflow tricks.
# ---------------------------------------------------------------------------

TIPS = [
    # --- Slash Commands ---
    "/background <提示>（别名 /bg 或 /btw）在单独的会话中运行任务，当前会话不受影响。",
    "/branch 分支当前会话，让你可以探索不同方向而不丢失进度。",
    "/compress 在对话过长时手动压缩上下文。",
    "/rollback 列出文件系统检查点 — 将 agent 修改过的文件恢复到任何先前状态。",
    "/rollback diff 2 预览自检查点 2 以来的更改，不执行恢复。",
    "/rollback 2 src/file.py 从特定检查点恢复单个文件。",
    "/title \"my project\" 为会话命名 — 之后用 /resume 或 hermes -c 恢复。",
    "/resume 从之前命名的会话中继续。",
    "/queue <提示> 将消息排队到下一轮，不中断当前操作。",
    "/undo 从对话中移除最后一组用户/助手交换。",
    "/retry 重新发送你的上一条消息 — 当 agent 回复不够好时很有用。",
    "/verbose 循环工具进度显示：关闭 → 新工具 → 全部 → 详细。",
    "/reasoning high 增加模型的思考深度。/reasoning show 显示推理过程。",
    "/fast 切换优先处理模式以获得更快的 API 响应（取决于供应商）。",
    "/yolo 在当前会话剩余时间内跳过所有危险命令审批提示。",
    "/model 让你在会话中切换模型 — 试试 /model sonnet 或 /model gpt-5。",
    "/model --global 永久更改你的默认模型。",
    "/personality pirate 设置有趣的人格 — 14 个内置选项，从可爱到莎士比亚。",
    "/skin 更改 CLI 主题 — 试试 ares、mono、slate、poseidon 或 charizard。",
    "/statusbar 切换持久状态栏，显示模型、token、上下文填充%、费用和时长。",
    "/tools disable browser 临时移除当前会话的浏览器工具。",
    "/browser connect 通过 CDP 将浏览器工具连接到你运行中的 Chrome 实例。",
    "/plugins 列出已安装插件及其状态。",
    "/cron 管理定时任务 — 设置可重复执行的提示并投递到任何平台。",
    "/reload-mcp 热重载 MCP 服务器配置，无需重启。",
    "/usage 显示 token 用量、费用明细和会话时长。",
    "/insights 显示过去 30 天的使用分析。",
    "/paste 检查剪贴板中的图片并附加到你的下一条消息。",
    "/profile 显示当前活跃的配置及其主目录。",
    "/config 一览当前配置。",
    "/stop 终止 agent 生成的所有运行中的后台进程。",

    # --- @ Context References ---
    "@file:path/to/file.py 将文件内容直接注入到你的消息中。",
    "@file:main.py:10-50 只注入文件的第 10-50 行。",
    "@folder:src/ 注入目录树列表。",
    "@diff 将你未暂存的 git 更改注入消息。",
    "@staged 注入你已暂存的 git 更改（git diff --staged）。",
    "@git:5 注入最近 5 次提交及完整补丁。",
    "@url:https://example.com 获取并注入网页内容。",
    "输入 @ 触发文件系统路径补全 — 交互式导航到任何文件。",
    "组合多个引用：\"Review @file:main.py and @file:test.py for consistency.\"",

    # --- Keybindings ---
    "Alt+Enter（或 Ctrl+J）插入换行符用于多行输入。",
    "Ctrl+C 中断 agent。2 秒内双击强制退出。",
    "Ctrl+Z 将 Hermes 挂起到后台 — 在 shell 中运行 fg 恢复。",
    "Tab 接受自动建议的幽灵文本或自动补全斜杠命令。",
    "在 agent 工作时输入新消息可以中断并重定向它。",
    "Alt+V 将剪贴板中的图片粘贴到对话中。",
    "粘贴 5 行以上内容会自动保存到文件并插入简洁引用。",

    # --- CLI Flags ---
    "hermes -c 恢复最近的 CLI 会话。hermes -c \"project name\" 按标题恢复。",
    "hermes -w 创建隔离的 git worktree — 适合并行 agent 工作流。",
    "hermes -w -q \"Fix issue #42\" 结合 worktree 隔离和一次性查询。",
    "hermes chat -t web,terminal 只启用特定工具集以获得专注会话。",
    "hermes chat -s github-pr-workflow 在启动时预加载技能。",
    "hermes chat -q \"query\" 运行单次非交互查询并退出。",
    "hermes chat --max-turns 200 覆盖默认的每轮 90 次迭代限制。",
    "hermes chat --checkpoints 在每次破坏性文件更改前启用文件系统快照。",
    "hermes --yolo 在整个会话中绕过所有危险命令审批提示。",
    "hermes chat --source telegram 标记会话以便在 hermes sessions list 中过滤。",
    "hermes -p work chat 在指定配置下运行而不更改默认配置。",

    # --- CLI Subcommands ---
    "hermes doctor --fix 诊断并自动修复配置和依赖问题。",
    "hermes dump 输出精简的设置摘要 — 适合提交 bug 报告。",
    "hermes config set KEY VALUE 自动将密钥路由到 .env，其他内容路由到 config.yaml。",
    "hermes config edit 在默认编辑器中打开 config.yaml。",
    "hermes config check 扫描缺失或过时的配置项。",
    "hermes sessions browse 打开带搜索功能的交互式会话选择器。",
    "hermes sessions stats 显示各平台的会话数和数据库大小。",
    "hermes sessions prune --older-than 30 清理旧会话。",
    "hermes skills search react --source skills-sh 搜索 skills.sh 公共目录。",
    "hermes skills check 扫描已安装的 hub 技能是否有上游更新。",
    "hermes skills tap add myorg/skills-repo 添加自定义 GitHub 技能源。",
    "hermes skills snapshot export setup.json 导出技能配置用于备份或分享。",
    "hermes mcp add github --command npx 从命令行添加 MCP 服务器。",
    "hermes mcp serve 将 Hermes 自身作为 MCP 服务器运行供其他 agent 使用。",
    "hermes auth add 让你添加多个 API 密钥用于凭证池轮换。",
    "hermes completion bash >> ~/.bashrc 为所有命令和配置启用 Tab 补全。",
    "hermes logs -f 实时跟踪 agent.log。--level WARNING --since 1h 过滤输出。",
    "hermes backup 创建整个 Hermes 主目录的 zip 备份。",
    "hermes profile create coder 创建隔离配置，它会成为独立命令。",
    "hermes profile create work --clone 将当前配置和密钥复制到新配置。",
    "hermes update 自动将新的捆绑技能同步到所有配置。",
    "hermes gateway install 将 Hermes 设置为系统服务（systemd/launchd）。",
    "hermes memory setup 让你配置外部记忆提供商（Honcho、Mem0 等）。",
    "hermes webhook subscribe 创建带 HMAC 验证的事件驱动 webhook 路由。",
    "省钱技巧：hermes tools 禁用未使用的工具，hermes skills config 精简技能。",
    "/reasoning low 或 /reasoning minimal 将思考深度降至默认值以下（medium）— 更快、更便宜的响应。",
    "hermes models 将视觉、压缩和辅助任务路由到更便宜的模型 — 在不降级主聊天模型的情况下降低 85%+ 的后台 token 成本。",

    # --- Configuration ---
    "在 config.yaml 中设 display.bell_on_complete: true 可在长任务完成时听到提示音。",
    "设 display.streaming: true 可实时看到模型生成的 token。",
    "设 display.show_reasoning: true 可观看模型的思维链推理。",
    "设 display.compact: true 可减少输出中的空白以获得更密集的信息。",
    "设 display.busy_input_mode: queue 可将消息排队而非中断 agent，或设为 steer 通过 /steer 在运行中注入。",
    "设 display.resume_display: minimal 可在恢复会话时跳过完整对话回顾。",
    "设 compression.threshold: 0.50 控制自动压缩触发时机（默认：上下文的 50%）。",
    "设 agent.max_turns: 200 让 agent 每轮执行更多工具调用步骤。",
    "设 file_read_max_chars: 200000 增加每次 read_file 调用的最大内容量。",
    "设 approvals.mode: smart 让 LLM 自动批准安全命令并自动拒绝危险命令。",
    "在 config.yaml 中设 fallback_model 可自动故障转移到备用供应商。",
    "设 privacy.redact_pii: true 可在发送给 LLM 前哈希用户 ID 和电话号码。",
    "设 browser.record_sessions: true 可自动将浏览器会话录制为 WebM 视频。",
    "在 config.yaml 中设 worktree: true 可始终创建 git worktree（等同于 hermes -w）。",
    "设 security.website_blocklist.enabled: true 可阻止特定域名被 web 工具访问。",
    "设 cron.wrap_response: false 可投递原始 agent 输出，不带定时任务页头页脚。",
    "HERMES_TIMEZONE 用任何 IANA 时区字符串覆盖服务器时区。",
    "环境变量替换在 config.yaml 中有效：使用 ${VAR_NAME} 语法。",
    "config.yaml 中的快速命令可即时运行 shell 命令，零 token 消耗。",
    "自定义人格可在 config.yaml 的 agent.personalities 下定义。",
    "provider_routing 控制 OpenRouter 供应商排序、白名单和黑名单。",

    # --- Tools & Capabilities ---
    "execute_code 运行以编程方式调用 Hermes 工具的 Python 脚本 — 结果不会进入上下文。",
    "delegate_task 默认生成最多 3 个并发子 agent（delegation.max_concurrent_children），具有隔离上下文用于并行工作。",
    "web_extract 支持 PDF URL — 传入任何 PDF 链接即可转换为 markdown。",
    "search_files 基于 ripgrep，比 grep 更快 — 用它代替 terminal grep。",
    "patch 使用 9 种模糊匹配策略，微小的空白差异不会破坏编辑。",
    "patch 支持 V4A 格式，可在单次调用中批量编辑多个文件。",
    "read_file 在文件未找到时建议类似文件名。",
    "read_file 自动去重 — 重新读取未更改的文件返回轻量级存根。",
    "browser_vision 截屏并用 AI 分析 — 适用于验证码和视觉内容。",
    "browser_console 可以在页面上下文中执行 JavaScript 表达式。",
    "image_generate 使用 FLUX 2 Pro 创建图像并自动 2 倍放大。",
    "text_to_speech 将文本转换为音频 — 在 Telegram 上以语音气泡播放。",
    "send_message 可以从会话中向任何已连接的消息平台发送消息。",
    "todo 工具帮助 agent 在会话中跟踪复杂的多步骤任务。",
    "session_search 对所有过去的对话执行全文搜索。",
    "agent 自动将偏好、纠正和环境事实保存到记忆中。",
    "mixture_of_agents 将难题路由到 4 个前沿 LLM 协作处理。",
    "终端命令支持后台模式，配合 notify_on_complete 用于长时间运行的任务。",
    "终端后台进程支持 watch_patterns 以在特定输出行时发出警报。",
    "终端工具支持 6 种后端：local、Docker、SSH、Modal、Daytona 和 Singularity。",

    # --- Profiles ---
    "每个配置有自己的配置、API 密钥、记忆、会话、技能和定时任务。",
    "配置名成为 shell 命令 — 'hermes profile create coder' 创建 'coder' 命令。",
    "hermes profile export coder -o backup.tar.gz 创建可移植的配置归档。",
    "如果两个配置意外共享 bot token，第二个网关会被阻止并显示明确错误。",

    # --- Sessions ---
    "会话在第一次交换后自动生成描述性标题 — 无需手动命名。",
    "会话标题支持 lineage：\"my project\" → \"my project #2\" → \"my project #3\"。",
    "退出时，Hermes 打印包含会话 ID 和统计信息的恢复命令。",
    "hermes sessions export backup.jsonl 导出所有会话用于备份或分析。",
    "hermes -r SESSION_ID 按 ID 恢复任何特定的过去会话。",

    # --- Memory ---
    "记忆是冻结快照 — 更改只在下次会话开始时出现在系统提示中。",
    "记忆条目会自动扫描提示注入和数据泄露模式。",
    "agent 有两个记忆存储：个人笔记（约 2200 字符）和用户档案（约 1375 字符）。",
    "你给 agent 的纠正（\"no, do it this way\"）通常会自动保存到记忆。",

    # --- Skills ---
    "超过 80 个捆绑技能，涵盖 github、创意、mlops、生产力、研究等。",
    "每个已安装的技能自动成为斜杠命令 — 输入 / 查看全部。",
    "hermes skills install official/security/1password 从仓库安装可选技能。",
    "技能可以限制到特定操作系统平台 — 有些只在 macOS 或 Linux 上加载。",
    "config.yaml 中的 skills.external_dirs 让你从自定义目录加载技能。",
    "agent 可以使用 skill_manage 创建自己的技能作为过程记忆。",
    "plan 技能将 markdown 计划保存在活动工作区的 .hermes/plans/ 下。",

    # --- Cron & Scheduling ---
    "定时任务可以附加技能：hermes cron add --skill blogwatcher \"Check for new posts\"。",
    "定时任务投递目标包括 telegram、discord、slack、email、sms 等 12+ 个平台。",
    "如果定时任务响应以 [SILENT] 开头，投递会被抑制 — 适合纯监控任务。",
    "定时任务支持相对延迟（30m）、间隔（every 2h）、cron 表达式和 ISO 时间戳。",
    "定时任务在全新的 agent 会话中运行 — 提示必须自包含。",

    # --- Voice ---
    "如果安装了 faster-whisper，语音模式可以零 API 密钥运行（免费本地语音转文字）。",
    "五种 TTS 提供商可用：Edge TTS（免费）、ElevenLabs、OpenAI、NeuTTS（免费本地）、MiniMax。",
    "/voice on 在 CLI 中启用语音模式。Ctrl+B 切换按键通话录音。",
    "流式 TTS 在生成时播放句子 — 无需等待完整响应。",
    "Telegram、Discord、WhatsApp 和 Slack 上的语音消息会自动转写。",

    # --- Gateway & Messaging ---
    "Hermes 支持 21 个平台：Telegram、Discord、Slack、WhatsApp、Signal、Matrix、IRC、Microsoft Teams、email 等。",
    "hermes gateway install 将其设置为开机自启动的系统服务。",
    "钉钉使用 Stream 模式 — 无需 webhook 或公网 URL。",
    "BlueBubbles 通过本地 macOS 服务器将 iMessage 接入 Hermes。",
    "Webhook 路由支持 HMAC 验证、速率限制和事件过滤。",
    "API 服务器提供 OpenAI 兼容端点，兼容 Open WebUI 和 LibreChat。",
    "Discord 语音频道模式：bot 加入语音频道，转写语音并回复。",
    "group_sessions_per_user: true 在群聊中为每人分配独立会话。",
    "/sethome 将聊天标记为定时任务投递的主频道。",
    "网关支持基于不活跃的超时机制 — 活跃 agent 可无限运行。",

    # --- Security ---
    "危险命令审批有 4 个级别：一次、会话、始终（永久白名单）、拒绝。",
    "智能审批模式使用 LLM 自动批准安全命令并标记危险命令。",
    "SSRF 保护阻止私有网络、回环、链路本地和云元数据地址。",
    "Tirith 预执行扫描检测同形 URL 欺骗和管道到解释器模式。",
    "MCP 子进程接收过滤后的环境 — 只有安全的系统变量通过。",
    "上下文文件（.hermes.md、AGENTS.md）在加载前会进行安全扫描以检测提示注入。",
    "config.yaml 中的 command_allowlist 永久批准特定的 shell 命令模式。",

    # --- Context & Compression ---
    "上下文在达到阈值时自动压缩 — 记忆被刷新，历史被摘要。",
    "随着上下文填充，状态栏从黄色变为橙色，再变为红色。",
    "~/.hermes/SOUL.md 是 agent 的主要身份 — 自定义它来塑造行为。",
    "Hermes 从 .hermes.md、AGENTS.md、CLAUDE.md 或 .cursorrules 加载项目上下文（第一个匹配的）。",
    "子目录的 AGENTS.md 文件在 agent 导航到文件夹时逐步发现。",
    "上下文文件限制在 20,000 字符以内，采用智能头尾截断。",

    # --- Browser ---
    "五种浏览器提供商：本地 Chromium、Browserbase、Browser Use、Camofox 和 Firecrawl。",
    "Camofox 是反检测浏览器 — 带 C++ 指纹伪造的 Firefox 分支。",
    "browser_navigate 自动返回页面快照 — 无需之后调用 browser_snapshot。",
    "browser_vision 的 annotate=true 在交互元素上覆盖编号标签。",

    # --- MCP ---
    "MCP 服务器在 config.yaml 中配置 — 支持 stdio 和 HTTP 传输。",
    "每服务器工具过滤：tools.include 白名单和 tools.exclude 黑名单特定工具。",
    "MCP 服务器在运行时自动生成工具集 — hermes tools 可以按平台切换。",
    "MCP OAuth 支持：auth: oauth 启用基于浏览器的 PKCE 授权。",

    # --- Checkpoints & Rollback ---
    "检查点在未修改文件时零开销 — 默认启用。",
    "回滚前快照会自动保存，这样你可以撤销撤销。",
    "/rollback 也会撤销对话轮次，这样 agent 不会记住已回滚的更改。",
    "检查点使用 ~/.hermes/checkpoints/ 中的影子仓库 — 项目的 .git 永远不会被修改。",

    # --- Batch & Data ---
    "batch_runner.py 并行处理数百个提示以生成训练数据。",
    "hermes chat -Q 启用安静模式用于编程使用 — 抑制横幅和加载动画。",
    "轨迹保存（--save-trajectories）捕获完整的工具使用痕迹用于模型训练。",

    # --- Plugins ---
    "三种插件类型：通用（工具/钩子）、记忆提供商和上下文引擎。",
    "hermes plugins install owner/repo 直接从 GitHub 安装插件。",
    "8 种外部记忆提供商可用：Honcho、OpenViking、Mem0、Hindsight 等。",
    "插件钩子包括 pre/post_tool_call、pre/post_llm_call 和 transform_terminal_output 用于输出规范化。",

    # --- Miscellaneous ---
    "提示缓存（Anthropic）通过重用缓存的系统提示前缀来降低成本。",
    "agent 在后台线程中自动生成会话标题 — 零延迟影响。",
    "智能模型路由可以自动将简单查询路由到更便宜的模型。",
    "斜杠命令支持前缀匹配：/h 解析为 /help，/mod 解析为 /model。",
    "将文件路径拖入终端会自动附加图片或作为上下文发送。",
    "仓库根目录的 .worktreeinclude 列出要复制到 worktree 中的 gitignore 文件。",
    "hermes acp 将 Hermes 作为 ACP 服务器运行，用于 VS Code、Zed 和 JetBrains 集成。",
    "自定义供应商：在 config.yaml 的 custom_providers 下保存命名端点。",
    "HERMES_EPHEMERAL_SYSTEM_PROMPT 注入永不保存到历史的系统提示。",
    "credential_pool_strategies 支持 fill_first、round_robin、least_used 和 random 轮换。",
    "hermes login 支持 Nous 和 OpenAI Codex 供应商的 OAuth 认证。",
    "API 服务器支持 Chat Completions 和 Responses API，具有服务端状态。",
    "config 中 tool_preview_length: 0 在加载动画的活动流中显示完整文件路径。",
    "hermes status --deep 对所有组件运行更深层的诊断检查。",

    # --- Hidden Gems & Power-User Tricks ---
    "定时任务可以附加 Python 脚本（--script），其 stdout 作为上下文注入到提示中。",
    "定时脚本存放在 ~/.hermes/scripts/，在 agent 运行前执行 — 适合数据收集管道。",
    "config.yaml 中的 prefill_messages_file 将少样本示例注入每次 API 调用，永不保存到历史。",
    "SOUL.md 完全替换 agent 的默认身份 — 重写它让 Hermes 成为你的专属助手。",
    "SOUL.md 首次运行时自动播种默认人格。编辑 ~/.hermes/SOUL.md 进行自定义。",
    "/compress <关注主题> 将 60-70% 的摘要预算分配给你的主题，大幅裁剪其余内容。",
    "第二次及以后的压缩会更新之前的摘要，而不是从头开始。",
    "网关会话重置前，Hermes 在后台自动将重要信息刷入记忆。",
    "config.yaml 中设 network.force_ipv4: true 可修复 IPv6 异常服务器上的挂起 — 对 socket 做 monkey-patch。",
    "终端工具会标注常见退出码：grep 返回 1 = '未找到匹配（非错误）'。",
    "前台终端命令失败时自动重试最多 3 次，采用指数退避（2s、4s、8s）。",
    "裸 sudo 命令会被自动改写为从 .env 管道传入 SUDO_PASSWORD — 无需交互提示。",
    "execute_code 内置辅助函数：json_parse() 用于容错解析、shell_quote() 和带退避的 retry()。",
    "execute_code 的 7 个沙箱工具（web_search、terminal、read/write/search/patch）通过 RPC 调用 — 永远不进入上下文。",
    "同一文件区域读取 3 次以上会触发警告。达到 4+ 次会被硬阻止以防死循环。",
    "write_file 和 patch 检测文件自上次读取后是否被外部修改，并警告过期。",
    "V4A patch 格式支持 Add File、Delete File 和 Move File 指令 — 不仅仅是 Update。",
    "MCP 服务器可以通过采样请求 LLM 补全 — agent 成为服务器的工具。",
    "MCP 服务器发送 notifications/tools/list_changed 以触发自动工具重新注册，无需重启。",
    "delegate_task 配合 acp_command: 'claude' 可从任何平台生成 Claude Code 作为子 agent。",
    "委派有心跳线程 — 子活动传播到父进程，防止网关超时。",
    "当供应商返回 HTTP 402（需要付费）时，辅助客户端自动回退到下一个。",
    "agent.tool_use_enforcement 引导描述动作而非调用工具的模型 — 对 GPT/Codex 自动启用。",
    "agent.restart_drain_timeout（默认 60s）让运行中的 agent 在网关重启生效前完成。",
    "agent.api_max_retries（默认 3）控制 agent 在显示错误前重试失败 API 调用的次数 — 降低它以快速回退。",
    "网关按会话缓存 AIAgent 实例 — 破坏此缓存会中断 Anthropic 提示缓存。",
    "任何网站可以通过 /.well-known/skills/index.json 暴露技能 — 技能中心自动发现它们。",
    "技能审计日志 ~/.hermes/skills/.hub/audit.log 跟踪每次安装和移除操作。",
    "过期的 git worktree 会自动清理：24-72 小时且无未推送提交的会在启动时修剪。",
    "每个配置在 HERMES_HOME/home/ 有自己的子进程 HOME — 隔离的 git、ssh、npm、gh 配置。",
    "HERMES_HOME_MODE 环境变量（八进制，如 0701）设置自定义目录权限用于 web 服务器遍历。",
    "容器模式：将 .container-mode 放在 HERMES_HOME 中，主机 CLI 自动执行到容器中。",
    "Ctrl+C 有 5 个优先级：取消录音 → 取消提示 → 取消选择器 → 中断 agent → 退出。",
    "agent 运行期间的每次中断都会记录到 ~/.hermes/interrupt_debug.log 并带时间戳。",
    "BROWSER_CDP_URL 将浏览器工具连接到任何运行中的 Chrome — 接受 WebSocket、HTTP 或 host:port。",
    "BROWSERBASE_ADVANCED_STEALTH=true 使用自定义 Chromium 启用高级反检测（Scale Plan）。",
    "CLI 在窄于 80 列的终端中自动切换到紧凑模式。",
    "快速命令支持两种类型：exec（直接运行 shell 命令）和 alias（重定向到另一个命令）。",
    "每任务委派模型：config 中的 delegation.model 和 delegation.provider 将子 agent 路由到更便宜的模型。",
    "delegation.reasoning_effort 独立控制子 agent 的思考深度。",
    "config.yaml 中的 display.platforms 允许按平台显示覆盖：{telegram: {tool_progress: all}}。",
    "config 中的 human_delay.mode 模拟人类打字速度 — 可配置 min_ms/max_ms 范围。",
    "配置版本迁移在加载时自动运行 — 新配置项无需手动干预即可出现。",
    "GPT 和 Codex 模型获得特殊的系统提示指导，用于工具纪律和强制工具使用。",
    "Gemini 模型获得定制指令，用于绝对路径、并行工具调用和非交互命令。",
    "config.yaml 中的 context.engine 可以设置为插件名称以使用替代上下文管理策略。",
    "超过 8000 token 的浏览器页面在返回给 agent 前由辅助 LLM 自动摘要。",
    "压缩器执行廉价预处理：超过 200 字符的工具输出在 LLM 运行前被替换为占位符。",
    "当压缩失败时，后续尝试暂停 10 分钟以避免 API 过载。",
    "长危险命令（>70 字符）在审批提示中获得'查看'选项以先查看完整文本。",
    "音频电平可视化在语音录制期间显示 ▁▂▃▄▅▆▇ 条形图，基于麦克风电平。",
    "配置名不能与现有 PATH 二进制文件冲突 — 'hermes profile create ls' 会被拒绝。",
    "hermes profile create backup --clone-all 复制所有内容（配置、密钥、SOUL.md、记忆、技能、会话）。",
    "语音录制键可通过 config.yaml 中的 voice.record_key 配置 — 不仅仅是 Ctrl+B。",
    ".cursorrules 和 .cursor/rules/*.mdc 文件被自动检测并加载为项目上下文。",
    "上下文文件支持 10+ 种提示注入模式 — 不可见 Unicode、'忽略指令'、数据泄露尝试。",
    "GPT-5 和 Codex 在消息格式中使用 'developer' 角色而非 'system'。",
    "每任务辅助覆盖：config.yaml 中的 auxiliary.vision.provider、auxiliary.compression.model 等。",
    "辅助客户端将 'main' 视为供应商别名 — 解析为你的实际主要供应商 + 模型。",
    "hermes claw migrate --dry-run 预览 OpenClaw 迁移而不写入任何内容。",
    "带引号或转义空格粘贴的文件路径会自动处理 — 无需手动清理。",
    "斜杠命令永远不会触发大粘贴折叠 — 带大参数的 /command 正确工作。",
    "在中断模式下，agent 执行期间输入的斜杠命令绕过中断逻辑并立即运行。",
    "HERMES_DEV=1 绕过容器模式检测用于本地开发。",
    "每个 MCP 服务器获得自己的工具集（mcp-servername），可通过 hermes tools 独立切换。",
    "配置中的 MCP ${ENV_VAR} 占位符在服务器生成时解析 — 包括 ~/.hermes/.env 中的变量。",
    "来自可信仓库（NousResearch）的技能获得'可信'安全级别；社区技能获得额外扫描。",
    "技能隔离区 ~/.hermes/skills/.hub/quarantine/ 存放待安全审查的技能。",

    # --- Advanced Slash Commands ---
    '/steer <prompt> injects a note after the next tool call — nudge direction mid-task without interrupting.',
    '/goal <text> sets a standing Ralph-loop objective — Hermes auto-continues turn after turn until a judge says done.',
    '/snapshot create [label] saves a full state snapshot of Hermes config; /snapshot restore <id> reverts later.',
    '/copy [N] copies the last assistant response to your clipboard, or the Nth-from-last with a number.',
    '/redraw forces a full UI repaint, fixing terminal drift after tmux resize or mouse selection artifacts.',
    '/agents (alias /tasks) shows active agents and running background tasks across the current session.',
    '/footer toggles the gateway footer on final replies showing model, tool counts, and turn timing.',
    '/busy queue|steer|interrupt controls what pressing Enter does while Hermes is working.',
    '/topic in Telegram DMs enables user-managed multi-session topic mode — /topic <id> restores past sessions inline.',
    '/approve session|always runs a pending dangerous command with your chosen trust scope; /deny rejects it.',
    '/restart gracefully restarts the gateway after draining active runs, then pings the requester when back up.',
    '/kanban boards switch <slug> changes the active multi-project Kanban board from inside chat.',
    '/reload reloads ~/.hermes/.env into the running session — pick up new API keys without restarting.',

    # --- Cron (no-agent & scripts) ---
    'cronjob with no_agent=True runs a script on schedule and sends its stdout directly — zero tokens, zero LLM.',
    'An empty cron script stdout means silent tick — nothing is delivered, perfect for threshold watchdogs.',
    "HERMES_CRON_MAX_PARALLEL（默认 4）限制每次 tick 运行的定时任务数，防止突发饱和密钥。",

    # --- Gateway Hooks ---
    'Gateway hooks live under ~/.hermes/hooks/<name>/ with HOOK.yaml + handler.py — handler must be named `handle`.',
    'Hook events include gateway:startup, session:start, agent:step, and command:* wildcard subscriptions.',
    'Drop a ~/.hermes/BOOT.md checklist and a gateway:startup hook runs it as a one-shot agent every boot.',

    # --- Curator ---
    'hermes curator run --dry-run previews what the curator would archive or consolidate without mutating anything.',
    "hermes curator pin <skill> 硬性保护技能免受自动归档和 agent 的 skill_manage 工具影响。",
    'hermes curator rollback restores skills from a pre-run snapshot — backups live under skills/.curator_backups/.',

    # --- Credential Pools & Routing ---
    'hermes auth reset <provider> clears all cooldowns and exhaustion flags on a credential pool.',
    'credential_pool_strategies.<provider>: round_robin cycles keys evenly instead of the fill_first default.',
    'use_gateway: true per-tool routes web, image, tts, or browser through your Nous subscription — no extra keys.',
    'provider_routing.data_collection: deny excludes data-storing providers on OpenRouter.',
    'provider_routing.require_parameters: true only routes to providers that support every param in your request.',

    # --- TUI & Dashboard ---
    'HERMES_TUI_RESUME=1 auto-re-attaches to the most recent TUI session on launch — handy after SSH drops.',
    "HERMES_TUI_THEME=light|dark|<hex> 在未设置 COLORFGBG 的终端上强制 TUI 主题。",
    'Ctrl+G or Ctrl+X Ctrl+E in the TUI opens the input buffer in $EDITOR for long multi-line prompts.',
    'The TUI renders LaTeX inline — $E=mc^2$ becomes Unicode math instead of raw TeX.',
    'hermes dashboard launches a local web UI at 127.0.0.1:9119 — zero data leaves localhost.',
    'hermes dashboard --tui embeds the full Hermes TUI in your browser via xterm.js and a WebSocket PTY.',
    'Drop a YAML in ~/.hermes/dashboard-themes/ with two palette colors to reskin the entire dashboard.',
    'Dashboard plugins are drop-in: manifest.json + JS bundle in ~/.hermes/dashboard-plugins/ — no npm build required.',
    'layoutVariant: cockpit in a dashboard theme adds a 260px left rail that plugins can populate via the sidebar slot.',

    # --- Env Vars & Config Gates ---
    "display.tool_progress_command: true 在消息平台上暴露 /verbose；默认仅限 CLI。",
    'HERMES_BACKGROUND_NOTIFICATIONS=result only pings when background tasks finish (vs all/error/off).',
    'HERMES_WRITE_SAFE_ROOT restricts write_file and patch to a directory prefix; writes outside require approval.',
    'HERMES_IGNORE_RULES skips auto-injection of AGENTS.md, SOUL.md, .cursorrules, memory, and preloaded skills.',
    'HERMES_ACCEPT_HOOKS auto-approves unseen shell hooks declared in config.yaml without a TTY prompt.',
    'auxiliary.goal_judge.model routes the /goal judge to a cheap fast model to keep loop cost near zero.',
    'Checkpoints skip directories with more than 50,000 files to avoid slow git operations on massive monorepos.',

    # --- TTS ---
    'tts.provider: piper runs 44-language local TTS on CPU — voices auto-download to ~/.hermes/cache/piper-voices/.',
    'tts.providers.<name>.type: command wires any CLI TTS engine with {input_path} and {output_path} placeholders.',

    # --- API Server & Proxy ---
    'API_SERVER_ENABLED=true runs an OpenAI-compatible endpoint alongside the gateway for Open WebUI and LibreChat.',
    'GATEWAY_PROXY_URL runs a split setup: platform I/O locally, agent work delegated to a remote API server.',

    # --- Platform-specific ---
    'MATRIX_DEVICE_ID pins a stable device ID for E2EE — without it, keys rotate every start and historic decrypt breaks.',
    'TELEGRAM_WEBHOOK_SECRET is required whenever TELEGRAM_WEBHOOK_URL is set — generate with openssl rand -hex 32.',

    # --- Batch ---
    "batch_runner.py --resume 通过文本匹配已完成的提示，这样数据集重排不会重新运行已完成的工作。",

    # --- Less-Known Slash Commands ---
    '/new starts a fresh session in place (alias /reset) — fresh session ID, clean history, CLI stays open.',
    '/clear wipes the terminal screen AND starts a new session — one shortcut for a visual reset.',
    '/history prints the current conversation in-line without leaving the CLI — useful for a quick re-read.',
    '/save writes the current conversation to disk without ending the session.',
    '/status shows session info at a glance: ID, title, model, token usage, and elapsed time.',
    '/image <path> attaches a local image file for your next prompt without pasting or drag-and-drop.',
    '/platforms shows gateway and messaging-platform connection status right from inside chat.',
    '/commands paginates the full slash-command + installed-skill list — useful on platforms without tab completion.',
    '/toolsets lists every available toolset so you know what -t/--toolsets accepts.',
    '/gquota shows Google Gemini Code Assist quota usage with progress bars when that provider is active.',
    '/voice tts toggles TTS-only mode — agent replies out loud but you still type your prompts.',
    '/reload-skills re-scans ~/.hermes/skills/ so drop-in skills appear without restarting the session.',
    '/indicator kaomoji|emoji|unicode|ascii picks the TUI busy-indicator style shown during agent runs.',
    '/debug uploads a support bundle (system info + logs) and returns shareable links — works in chat too.',

    # --- CLI Subcommands & Flags ---
    'hermes -z "<prompt>" is the purest one-shot: final answer on stdout, nothing else — ideal for piping in scripts.',
    'hermes chat --pass-session-id injects the session ID into the system prompt so the agent can self-reference it.',
    'hermes chat --image path/to/pic.png attaches a local image to a single -q query without a separate upload step.',
    'hermes chat --ignore-user-config skips ~/.hermes/config.yaml — reproducible bug reports and CI runs.',
    "hermes chat --source tool 标记编程聊天，这样它们不会使 hermes sessions list 混乱。",
    'hermes dump --show-keys includes redacted API key fingerprints for deeper support debugging.',
    'hermes sessions rename <ID> "new title" renames any past session; hermes sessions delete <ID> removes one.',
    'hermes import restores a session export or profile archive produced by sessions export or profile export.',
    'hermes fallback manages the fallback_model chain interactively — no hand-editing config.yaml.',
    'hermes pairing rotates the DM pairing token — the first messager after rotation claims access to the bot.',
    'hermes setup walks first-time users through provider, keys, and platform wiring in one interactive flow.',
    'hermes status --deep runs the full health sweep across every component; plain hermes status is the quick view.',

    # --- Agent Behavior Env Vars ---
    'HERMES_AGENT_TIMEOUT=0 disables the gateway inactivity kill for a running agent — use for long research runs.',
    'HERMES_ENABLE_PROJECT_PLUGINS=1 auto-loads repo-local plugins from ./.hermes/plugins/ — trust-gated by design.',
    "HERMES_DISABLE_FILE_STATE_GUARD=1 关闭 patch 和 write_file 上的'文件自读取后已更改'保护。",
    'HERMES_ALLOW_PRIVATE_URLS=true lets web tools hit localhost and private networks — off by default in gateway mode.',
    'HERMES_OPTIONAL_SKILLS=name1,name2 auto-installs extra optional-catalog skills on first run per profile.',
    'HERMES_BUNDLED_SKILLS points at a custom bundled-skill tree — used by Homebrew and Nix packaging.',
    'HERMES_DUMP_REQUEST_STDOUT=1 dumps every API request payload to stdout instead of log files.',
    'HERMES_OAUTH_TRACE=1 logs redacted OAuth token exchange and refresh attempts for debugging provider auth.',
    'HERMES_STREAM_RETRIES (default 3) controls mid-stream reconnect attempts on transient network errors.',

    # --- Gateway Behavior Env Vars ---
    'HERMES_GATEWAY_BUSY_ACK_ENABLED=false silences the ⚡/⏳/⏩ ack messages when a user messages a busy agent.',
    'HERMES_AGENT_NOTIFY_INTERVAL (default 180s) sets how often the gateway pings with progress on long turns.',
    'HERMES_RESTART_DRAIN_TIMEOUT (default 900s) caps how long /restart waits for in-flight runs before forcing.',
    'HERMES_CHECKPOINT_TIMEOUT (default 30s) caps filesystem checkpoint creation — raise it on huge monorepos.',

    # --- Auxiliary Tasks & Image Generation ---
    'image_gen.model in config.yaml picks the FAL model: flux-2/klein, gpt-image-2, nano-banana-pro, and more.',
    'image_gen.provider routes image generation through a plugin (OpenAI Images, Codex, FAL) instead of the default.',
    'AUXILIARY_VISION_BASE_URL + AUXILIARY_VISION_API_KEY point vision analysis at any OpenAI-compatible endpoint.',
    'auxiliary.session_search.max_concurrency bounds how many matched sessions are summarized in parallel (default 3).',
    'auxiliary.session_search.extra_body forwards provider-specific OpenAI-compatible fields on summarization calls.',

    # --- Security ---
    'security.tirith_fail_open: false makes Hermes block commands when the tirith scanner itself errors out.',
    'TIRITH_FAIL_OPEN env var overrides the tirith_fail_open config — a quick toggle without editing config.yaml.',

    # --- Sessions & Source Tags ---
    '--source tool chats are excluded from hermes sessions list by default — set --source explicitly to see them.',
    'Session IDs are timestamp-prefixed (20250305_091523_abcd) so sorting works naturally in ls and jq.',

    # --- Misc ---
    'API_SERVER_MODEL_NAME customizes the model name on /v1/models — essential for multi-profile Open WebUI setups.',
    'Dashboard plugins are served from /dashboard-plugins/<name>/ — drop files into ~/.hermes/dashboard-plugins/.',
]


def get_random_tip(exclude_recent: int = 0) -> str:
    """Return a random tip string.

    Args:
        exclude_recent: not used currently; reserved for future
            deduplication across sessions.
    """
    return random.choice(TIPS)


