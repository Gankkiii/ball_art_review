# R05 仓库横屏布局候选

四套完整1600×900概念页面，四入口导航一致。没有修改游戏、人物设计或玩法，不代表已经接入或真机通过。

- A：纵向列表选择，右侧形象与完整资料同屏。
- B：十种类大图陈列，每卡明确两个固定♀/♂示例；右抽屉选择具体个体，默认仅先天概览。全部来源按钮打开detail.png大幅完整矩阵，关闭返回原网格；individual_selection.png演示同种个体菜单。
- C：双页图鉴，左页形象技能、右页特性属性；缩略索引与前后翻页。
- D：横向逐个体画廊，性别与等级同屏；底部先天概览，点击展开到detail.png的完整属性矩阵，收起返回画廊。

四版同一母鱼人工评审样例：♀、Lv.0、特性一[待设计]；另外两特性待设计；吸附泡泡+3、八方泡泡+3，另外三个技能待设计。先天34/41/48/12/19/26，后天均0，种族基础与最终值均待定。+3/+3不是make_samples默认3/5。数据核对共享`../sample.json`及`../FACTS.md`。

所有精灵图使用当前仓库`assets/r04/characters/*/idle.png`与鸭兔`assets/r02/characters/*/default.png`原始透明素材，nearest显示；没有新画角色、改变武器或裁切预览。兔默认站姿保持原件，不代表本轮改刀型。

每版screen.png为概念图，source.html为可编辑独立HTML源，内嵌原PNG。A/C保留完整矩阵；B/D通过detail.png与detail_source.html展示完整来源。完整矩阵的先天/后天分列留足间距，没有“260”连读。按钮、分页、抽屉、搜索与滑动均是布局/流程提案，HTML不绑定真实存档、精灵切换或游戏逻辑；不增加培养、出战、筛选规则。'已拥有'仅浏览标签候选。真实仓库当前含20固定示例个体（10种类×♀♂）及本机实际孵出个体；未捏造任何后代。A列表逐个体、C缩略索引逐个体、D画廊逐个体；C/D的05/20+表示当前第五个固定示例，+代表本机孵出扩展，不是10种类上限。B按种类分组后同种个体菜单选择，所有个体性别/Lv可辨。其他个体只显示代码事实Lv0，不伪造先天等数值。

重建：在本云环境运行`python3 source/build_storage.py`；依赖Python3、Playwright、Chromium、Noto Sans CJK SC，源图从/workspace/balls/assets读取，PNG由HTML直接渲染。HTML单文件可离线查看。PNG与HTML是评审材料，不是组件接入素材。

本轮字体来自环境Noto Sans CJK，SIL Open Font License 1.1；未复制字体。未使用外部插画或私人资料。所有源与图片仅在shared输出，未commit/push。1600×900浏览器截图已检查数据与裁边；真实设备/游戏验证未运行。

## B 手机横屏信息组织示范

新增真正844×390重排的`b/phone.png`、`phone_source.html`，不是1600画布缩图。全局四入口、个体男女选择、页签及完整来源按钮均至少44×44 CSS px；文字最小14px。左侧种类网格内部滚动，右侧默认先天摘要，技能/特性用独立页签查看，完整6×4矩阵在同viewport浮层内展开并关闭返回。`phone_skills.png`、`phone_traits.png`、`phone_detail.png`展示这些可达状态。+3/+3仍是人工样例，未删除未知字段。手机HTML中页签与完整属性浮层可操作；精灵/性别切换仍只是候选界面，不绑定游戏数据。

重建顺序：先`python3 source/build_storage.py`，再`python3 source/build_phone.py`以生成手机预览及带短标题的B副图metadata。手机检查见`b/phone_qa.json`。此为浏览器viewport模拟，非手机真机或游戏内验证。
