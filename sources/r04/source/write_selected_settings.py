#!/usr/bin/env python3
"""Maintain eight standalone R04 setting entries without touching team rules."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parent.parent
CHOICES={
'puffer':['A圆薄荷软刺气团；不因此认定为已批准的河豚物种。','B分段吸收罩；无额外护盾层数，可与放气同时显示。','普通实际掉HP只眨眼；免伤受击改蓝色吸收反馈，不假掉血。'],
'chicken':['B长颈扇尾母鸡；不是鸭，不加枪炮。','A斑点蛋；小蛋敌触引信、大蛋落地引信的差别保留。','B腿/尾摆惊跑；不另加跳跃、位移或速度规则。','普通实际掉HP只眨眼。'],
'bubble_fish':['A流线叉尾鱼；没有枪杖或新增嘴部武器。','A单层加粗泡泡边缘，level增加时颜色由浅至深，数字继续保留。','颜色达到最深不代表等级封顶，尺寸封顶也不代表等级封顶；1级无伤害。','八向技能画八个分离1级小泡，不用一张AOE爆炸替代。','普通实际掉HP只眨眼。'],
'electric_sheep':['A圆团云绒羊，补两条清晰可见的小短腿与深色蹄，保持圆团造型。','A圆团羊毛无脸、无腿；只有一处羊毛点，共享本体电量，不是第二只羊。','普通实际掉HP只眨眼；持续电只显示真实单一路径，不额外双倍伤害。'],
'magnet_crab':['A横向马蹄磁钳造型；钳仍是肢体，不新增近战判定。','B仅在实际移动的铁钉后画短轨迹，静止钉无伤害/危险地刺视觉。','普通实际掉HP只眨眼。'],
'cactus':['A高柱花冠并补两只眼睛；无行走腿、无奔跑。','A落刺时短暂发亮；不是持续范围伤害或新刺点寿命。','REGROW实际换位时花冠短亮，不恢复生命、不增加无敌。','普通实际掉HP只眨眼。'],
'shell_turtle':['A长颈短足本体，加独立圆拱空壳；不是全程穿背甲。','A只有壳纹旋转，不增加光效/冲刺或运动规则。','仅易受伤本体实际掉HP才眨眼；隐藏本体和不可受伤空壳不画受击。'],
'crow':['B宽身披翼乌鸦，B拼布稻草人；不新增护甲或稻草人主动攻击。','B真实换位两端出现短羽光，不连接飞羽弹道。','换位仍固定第一个稻草人且双方位置合法才成功，不变成自由选点。','普通实际掉HP只眨眼；羽毛储存/近身修复语义保持，不当远程攻击。']}
def main():
 decisions=json.loads((ROOT/'DECISIONS.json').read_text());commit=subprocess.check_output(['git','-C','/workspace/balls','rev-parse','HEAD'],text=True).strip()
 for ident,approved in CHOICES.items():
  old=(ROOT.parent/'R03-review/facts'/f'{ident}.md').read_text()
  facts='## 来源\n'+old.split('## 来源\n',1)[1].split('## 限制、容易混淆及未确定',1)[0]
  limits=old.split('## 限制、容易混淆及未确定',1)[1].split('- 新轮廓',1)[0].strip()
  limits=limits.replace('本轮造型仅候选','本轮已选圆薄荷气团，但物种并未另行确定')
  name=decisions['characters'][ident]['name']
  out=f'# {name}：R04已确认视觉与代码事实\n\n状态：本页记录用户明确选择的视觉方向，不代表已经接入游戏或完成真机/听感验收。仅更新评审网页，不制作接入包，不修改游戏与受保护团队配置。\n\n代码检查基线：`{commit}`。本轮已重新读取本角色与关联代码；下列机制事实与造型选择分开记录。\n\n'
  out+=facts+'## 机制边界\n\n'+limits+'\n\n## R04已确认视觉\n\n'+'\n'.join('- '+a for a in approved)+'\n\n'
  out+='## 声音状态\n\n全部R03试听音色已经被用户否决，早先A/B音色选择不再有效；本轮禁止复用或链接旧试听。当前确认的是角色材质/发声方向，新音效由音效岗重新制作并等待用户试听确认。母鸡惊跑明确为急促“咯咯咯”，不是公鸡打鸣。\n\n'
  out+='## 当前交付与验证边界\n\n同目录 `review.json` 指向本轮选定造型、关键动作和物件概念预览。没有重新开放造型A/B选择；网页中的短标签只帮助查看，详细规则收在本页。GIF播放时长不是技能CD/真实战斗时序，造型大小不是新碰撞体。普通眨眼只是受击反馈，不额外加无敌、击退、硬直或hitstop。\n\n当前鸭兔已有R02资源接入代码，不在本轮重新设计。这里不将概念动画当作Godot实录，不宣称真实渲染、音画同步、人工听审或设备验收通过。\n'
  if ident=='puffer':out+='\n免伤补充：`start_burst()`不清`immune_left`，所以免伤可能与burst并存。接触伤害0.35秒为角色共享计时器，非每目标独立。\n'
  if ident=='bubble_fish':out+='\n等级对照图为同尺寸的色深示意，便于直接比较；不是按世界空间复现所有等级大小。实机尺寸仍按`min(54,9+sqrt(level)*3)`，level没有玩法上限；深色和尺寸上限不能代替实时数字。\n'
  p=ROOT/'characters'/ident/'SETTING.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(out)
 print('Eight R04 standalone confirmed setting entries written')
if __name__=='__main__':main()
