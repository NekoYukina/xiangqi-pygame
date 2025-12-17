# Xiangqi（象棋）Pygame 项目

三人组：mx、wyf、wty。目标是按照"规则内核 core + UI + AI"分层，先实现骨架、再升级到 Pygame 交互，最后引入 AI。

## 工作空间布局

```
Course/SoftEngineer/
├── .python-version         # uv 管理的 Python 版本配置
├── README.md              # 本文档
├── pyproject.toml         # uv/poetry 依赖配置
├── uv.lock                # uv 环境锁文件
├── cn_chess/              # uv 创建的虚拟环境（已在 .gitignore）
└── xiangqi/               # 象棋项目代码
```

## 项目结构

```
xiangqi/
├── main.py                # 游戏启动入口
├── app.py                 # 应用主程序（备用入口）
├── core/                  # 棋盘、走法、规则逻辑
│   ├── __init__.py
│   ├── const.py          # 常数定义（Piece, Side 枚举、棋盘尺寸）
│   ├── move.py           # Move 数据类（frm, to, moved_piece, captured）
│   ├── board.py          # Board 棋盘（squares, side_to_move, move_stack）
│   ├── movegen.py        # 走法生成（所有7种棋子的伪合法和合法着法）
│   └── rules.py          # 规则判断（in_check, is_checkmate, is_face_to_face）
│
├── ui/                    # Pygame UI 框架（Scene 模式）
│   ├── __init__.py
│   ├── game.py           # Game 主类（主循环、场景管理）
│   ├── game_config.py    # 游戏常数（800x900 窗口、80px 格子）
│   ├── theme.py          # Theme 主题（3套风格：stype_1/2/3）
│   ├── asset_manager.py  # AssetManager 资源加载（棋子图片、背景等）
│   ├── scenes.py         # Scene 基类（on_enter, on_exit, handle_event, draw）
│   ├── menuscene.py      # MenuScene 菜单（选择游戏模式）
│   └── playscene.py      # PlayScene 游戏场景（棋盘显示、选棋、移动）
│
├── ai/                    # AI 模块（Zobrist、MiniMax 搜索）
│   ├── __init__.py
│   ├── eval.py           # 局面评估函数
│   ├── search.py         # MiniMax 搜索算法
│   └── zobrist.py        # Zobrist 哈希（置换表）
│
├── assets/               # 资源文件
│   ├── fonts/
│   │   └── NotoSerifSC-Regular.otf    # 中文字体
│   └── img/
│       ├── init_bg.png          # 菜单背景框
│       ├── btn_bg.png           # 菜单按钮
│       ├── btn_fh.png           # 返回按钮
│       ├── stype_1/             # 风格 1（棋子、棋盘、点标记、选框）
│       ├── stype_2/             # 风格 2
│       └── stype_3/             # 风格 3
│
└── test/                 # 测试脚本
    ├── test_play.py      # 跳过菜单直接进游戏
    ├── test_menu.py      # 菜单测试
    └── test_ui.py        # UI 测试
```

## 快速开始

### 安装依赖

```bash
uv sync          # 安装所有依赖（包括 pygame 2.6.1）
```

### 运行游戏

```bash
# 方式 1：完整流程（菜单 → 游戏）
python -m xiangqi.main

# 方式 2：跳过菜单直接进游戏（测试用）
python xiangqi/test/test_play.py
```

## 当前进度

### ✅ 已完成

**核心游戏逻辑**
- 棋盘数据结构（10×9 一维数组）
- 所有 7 种棋子的伪合法着法生成（车、马、象、士、将、炮、兵）
- 合法着法过滤（不走进将军）
- 规则判断（检测将军、活棋判定）

**UI 框架**
- Scene 模式（便于扩展新场景）
- Game 主循环（60fps，事件处理、更新、绘制）
- 主题系统（支持 3 套视觉风格）
- 资源管理（自动加载对应主题的图片）

**MenuScene（菜单）**
- 3 种游戏模式选择
- 键盘交互（1/2/3 选择，回车确认）
- 背景铺满屏幕，菜单居中

**PlayScene（游戏）**
- 棋盘显示（动态缩放适应全屏）
- 棋子渲染（位置精确对齐网格）
- 选棋与高亮（点击棋子显示选中框）
- 显示可走位置（点标记）
- 移动执行（点击可走位置移动棋子）
- 自动切换回合

### 🔄 进行中 / 待实现

- [ ] **AI 模块**
  - 集成 [chessAI](https://github.com/yuqangy123/chessAI) 的预训练模型 或 实现简单搜索
  - 人机对战模式

- [ ] **SettingsScene**
  - 主题切换 UI
  - 难度设置

- [ ] **UI 完善**
  - 游戏状态显示（当前轮、是否将军）
  - 返回菜单按钮
  - 重新开始按钮
  - 移动历史显示

- [ ] **游戏模式**
  - 人机对战（当前只支持人人对战）
  - 挑战模式（特定局面）

## 操作说明

### 菜单界面
- 按 `1` 选择"人机对弈"
- 按 `2` 选择"换边对战"
- 按 `3` 选择"挑战棋局"
- 按 `回车` 开始游戏

### 游戏界面
1. **左键点击棋子** → 选中该棋子，显示可走位置（黄点）+ 选中框
2. **左键点击可走位置** → 执行移动，自动切换回合
3. **左键点击空位** → 取消选中

## 技术亮点

- **模块化设计**：core/ui/ai 完全解耦，便于扩展
- **Scene 模式**：易于管理多个场景（菜单、游戏、设置）
- **主题系统**：一套代码支持多套视觉风格
- **精确坐标映射**
  - `pixel_to_rc()`：鼠标坐标 → 棋盘格子（用 `round()` 四舍五入）
  - `rc_to_pixel()`：棋盘格子 → 屏幕坐标（用 `int()` 截断）

## 合作流程

1. **新功能** 从 `main` 拉新分支：`feature/<功能名>`
2. **开发完成** 后提交 PR，至少一人审查
3. **合并** 前确保：
   - 代码通过本地测试
   - 无冲突
   - 遵循现有代码风格

## 参考资源

- [JavaScript 象棋实现](https://github.com/itlwei/Chess)（菜单 UI 参考）
- [chessAI 预训练模型](https://github.com/yuqangy123/chessAI)（AI 参考）
- [Pygame 官方文档](https://www.pygame.org)

## 开发笔记

### 鼠标点击事件处理流程

**PlayScene 中的选棋与移动逻辑**：
1. `handle_event(MOUSEBUTTONDOWN)` 获取鼠标坐标
2. `pixel_to_rc()` 转换屏幕坐标 → 棋盘坐标（使用 `round()` 四舍五入）
3. 第一次点击：检测是否点击己方棋子，若是则生成该棋子的所有合法走法
4. 第二次点击：检测目标位置是否在可走列表中，若是则执行 `board.make_move()`
5. `rc_to_pixel()` 渲染时转换棋盘坐标 → 屏幕坐标（使用 `int()` 截断）

**关键方法**：
- `pixel_to_rc(pos)`：鼠标坐标 → 棋盘 (row, col)
- `rc_to_pixel(row, col)`：棋盘坐标 → 屏幕像素坐标

### 坐标系统

- **棋盘格子**：10 行 × 9 列（0-索引）
- **一维数组访问**：`index = row * 9 + col`
- **反向转换**：`row, col = divmod(index, 9)`
- **屏幕适配**：动态缩放 board_bg，通过 inset 比例（l/r/t/b）微调格子区域

### 下一步建议

1. **人机对战**（优先级高）
   - 集成 AI 模块
   - 实现 AI 回合逻辑

2. **UI 完善**（优先级中）
   - 游戏状态显示（当前轮、将军状态）
   - 场景导航（返回菜单、重新开始）
   - 移动历史显示

3. **挑战模式**（优先级低）
   - 预设局面库
   - 赢/平局判定
