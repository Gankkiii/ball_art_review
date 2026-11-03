# 泡泡鱼：代码事实初稿

状态：R03评审依据，不是候选造型已批准、不是素材接入清单。维护责任：角色与物件美术岗。

来源提交：`3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47`。用户已允许在独立设定缺失时依据代码整理事实，不编造玩法。

## 来源

- `scripts/bubble_fish.gd`
- `scripts/bubble.gd`
- `scripts/battle_arena.gd`
- `scripts/fighter.gd`
- `scripts/ball.gd`

## 已存在机制

- 每1.1秒吐1级泡泡，初始bubble_timer0.5；1级直接碰敌消失无伤害。
- 同主人泡泡接触融合，level相加；等级>=2命中伤害level×8，命中后消失。
- VACUUM BUBBLE朝敌人当前方向170速度发射，飞行/吸附2.5秒，105范围吸引自己的泡泡，CD7。
- EIGHT BUBBLES八方向各1级，150速度快飞0.8秒后恢复慢漂，CD9。
- level无玩法上限；泡泡视觉/检测尺寸radius=min(54,9+sqrt(level)×3)，封顶的是尺寸不是等级。

## 武器与物件

- 独立Bubble；普通/融合/吸附/八向小泡泡

## 可观测状态数据

- `bubble_timer`
- `Bubble.level/velocity/launch_left/absorb_left/gone`

## 限制、容易混淆及未确定

- 不能给1级泡泡画成已造成伤害的爆炸。
- 气泡与充气角色的气量是不同机制；不要混为一种角色。
- 新轮廓、服饰、装饰、候选风格差异仍未选；`_draw()`原型不是本轮新造型的批准。
- 仅A像素风/横屏/极简信息及鸭兔既有决定已确认；本轮8角色方案均待用户选择。
- 本轮仅做评审网页，不交付接入包、不修改游戏。
- 当前为只读代码核对，没有宣称新增行为/动画已在Godot或真机验证。

## 本轮基线更新核对

`bc0fdd6→3134f2b`逐文件git diff确认本角色及关联物件、BattleArena/Fighter/Ball脚本未改变。新提交已把鸭兔R02图像、场景与UI资源接入showcase，并有presentation信号；旧R02接入文档仍称代码绘制/短剑声属于过时历史，不能据此否认现代码接入。实际渲染、人工听审与真机未由本岗验证。本轮8候选仍未选择/未接入。
