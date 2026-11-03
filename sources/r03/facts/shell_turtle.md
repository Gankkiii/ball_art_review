# 脱壳龟：代码事实初稿

状态：R03评审依据，不是候选造型已批准、不是素材接入清单。维护责任：角色与物件美术岗。

来源提交：`3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47`。用户已允许在独立设定缺失时依据代码整理事实，不编造玩法。

## 来源

- `scripts/shell_turtle.gd`
- `scripts/turtle_shell.gd`
- `scripts/battle_arena.gd`
- `scripts/fighter.gd`
- `scripts/ball.gd`

## 已存在机制

- 龟本体与独立壳是两个物理身体；本体未入壳碰到敌对Fighter时自身扣12，不是自己撞人伤12。
- HIDE IN SHELL向壳寻路最多6秒，速度240；碰到壳后hidden2.5秒，本体physics_enabled=false/visible=false、免受伤害并跟随壳。成功出壳找可用位置，速度170；CD9。
- SPIN SHELL壳spin2.5秒，CD8；start_spin将壳速度暂置0并保存，结束若仍近静止则恢复。不是“自动高速冲刺”。
- 壳radius22、不可受伤；撞敌伤18，spin时伤27并对可推动目标施加原有冲量100。
- 本体出壳若暂时无可用位置会继续隐藏等待；不把2.5秒结束画成必定出壳。

## 武器与物件

- TurtleShell独立龟壳
- 空壳/本体/入壳姿态

## 可观测状态数据

- `action: idle/seek/hidden`
- `action_left`
- `physics_enabled/visible`
- `shell.position/velocity/spin_left/spin_restore`

## 限制、容易混淆及未确定

- 壳是实际独立物体，不是全程固定背甲；不能画“龟一直穿壳”掩盖脱壳机制。
- spin的图像旋转不代表位置高速移动；不能新增冲刺/反弹规则。
- 新轮廓、服饰、装饰、候选风格差异仍未选；`_draw()`原型不是本轮新造型的批准。
- 仅A像素风/横屏/极简信息及鸭兔既有决定已确认；本轮8角色方案均待用户选择。
- 本轮仅做评审网页，不交付接入包、不修改游戏。
- 当前为只读代码核对，没有宣称新增行为/动画已在Godot或真机验证。

## 本轮基线更新核对

`bc0fdd6→3134f2b`逐文件git diff确认本角色及关联物件、BattleArena/Fighter/Ball脚本未改变。新提交已把鸭兔R02图像、场景与UI资源接入showcase，并有presentation信号；旧R02接入文档仍称代码绘制/短剑声属于过时历史，不能据此否认现代码接入。实际渲染、人工听审与真机未由本岗验证。本轮8候选仍未选择/未接入。
