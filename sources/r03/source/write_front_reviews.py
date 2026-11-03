#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
D={
'puffer':{
 'name':'充气球',
 'variants':[
  ('软刺气团','圆润气团、短软凸点与小圆口；充满时保持圆形体积变化。不是已经确定的河豚物种。',['小尺寸识别快；充气前后对比直接','与鸭兔轮廓区分明显，无手持武器'],['圆身在密集碰撞中容易与泡泡混淆，需保留实心身体和脸']),
  ('折瓣气囊','高菱形、折瓣体块和纵向分区；膨胀表现为折瓣展开，而非只换色。',['折瓣可表达气量变化；轮廓比圆泡更独特'],['小尺寸下体块分区容易丢失；不能画成新护甲或新增蓄气器官规则'])],
 'recommendation':'推荐A软刺气团：气量膨胀更直观。B适合希望与圆形泡泡强区分的方向；均未选定。',
 'questions':['造型选A圆软气团还是B折瓣气囊？Puffer物种外观尚未确定，不默认它一定是河豚。','免伤表现选A完整细环还是B分段罩？二者都应可与放气状态叠加，不能表示碰撞体或新增护盾值。','放气动画更偏圆团挤压回弹还是折瓣逐段回缩？音色选A轻弹乳胶还是B低声气囊，可与造型独立组合。'],
 'objects':[
  ('A免伤细环','objects/absorb_a.png','连续单环候选，不定义碰撞或伤害范围。'),('B免伤分段罩','objects/absorb_b.png','结构分段而非新增护盾层数。'),('免伤与放气共存','objects/absorb_and_burst.png','immune_left可在start_burst后仍>0；这幅是并存示例，不意味着所有burst都有免伤。')],
 'states':[
  ('idle','原形','action idle；普通接触无额外伤害。'),('inflate','充气','仅外观半径随gas变化，物理radius保持24。'),('immune','免伤吸收','只读immune_left；受击伤害×1.8转气，视觉不另加毒刺伤害。'),('burst','放气碰撞','真实burst状态才有36接触伤害；角色共享0.35计时器，不能按每目标重复结算。')],
 'information':['必须分清gas和immune_left；可以同时膨胀、放气、免伤。','视觉最大2倍不是攻击范围扩大；参考动作GIF没有真实碰撞数据。','无手持武器；气体、免伤环和尾迹是身体/状态表现，不是气弹。'],
 'audio':['轻弹乳胶','低声气囊']},
'chicken':{
 'name':'炸弹母鸡',
 'variants':[
  ('圆身红冠','低重心圆身、短尾、圆冠、短脚；强调蹲蛋的压低体态。',['与A玩具街机一致；母鸡身份与蛋清晰'],['密集状态时可能显笨重；需与黄鸭的帽/嘴/尾明显区分']),
  ('长颈扇尾','长颈、尖冠、展开三片尾羽和显眼双腿；更强调惊跑。',['轮廓高挑，冲刺方向更容易读；与鸭形象差异大'],['头尾占画布更大；腿摆动不能误导实际碰撞或步行规则'])],
 'recommendation':'推荐A圆身红冠配斑点蛋：本体/蛋/蹲蛋语义直接。偏重喜剧惊跑可选B；均待确认。',
 'questions':['母鸡造型选圆身红冠还是长颈扇尾？与已定鸭子保留不同冠、尾和身体比例。','蛋壳选A离散斑点还是B宽带纹？小蛋/大蛋都沿同一方案，并靠大小和已点燃引信区分，不能做手持炮弹。','惊跑更强调身体弹跳还是腿和尾的摆动？爆炸音色选A玩具蛋壳还是B厚壳闷爆，不能用落雷声冒充炸蛋。'],
 'objects':[
  ('A斑点蛋','objects/egg_a.png','与B同尺寸概念比较，天然蛋壳/斑点造型，不增加机械武器。'),('B宽带蛋','objects/egg_b.png','与A同尺寸比较；带纹是图案，不是新增属性。'),('大小蛋关系','objects/egg_patterns.png','小/大蛋外观比例示意，不是爆炸范围刻度。'),('大蛋引信示意','objects/armed_big_egg.png','大蛋落地即1.5秒引信；小蛋则敌触后0.8秒，不可混同。')],
 'states':[
  ('idle','待机','被动每1.7秒产小蛋，非普通碰撞伤害。'),('run','惊跑','持续1模拟秒，每0.18秒随机改向；GIF只是姿态展示，不能定义路径。'),('lay','蹲蛋','实际蹲3秒后产大蛋，不能按GIF时长提前落蛋。'),('big_egg','大蛋落地','大蛋立即引信，不是等接触；爆炸发生时才按当时位置判定。')],
 'information':['需要小蛋/大蛋、armed/fuse和爆炸事件的不同表现。','鸡不是鸭，不复用雷云/避雷针；没有枪炮或新投掷技能。','自身爆炸只受20%伤害；爆炸图形不应额外扩大实际半径。'],
 'audio':['玩具蛋壳','厚壳闷爆']},
'bubble_fish':{
 'name':'泡泡鱼',
 'variants':[
  ('流线叉尾','横向鱼身、背鳍、分叉尾与前端小口；用身体呼气而非武器射击。',['方向清晰；与真实吐泡事件容易关联'],['身体和八向泡泡都偏圆，需靠尾鳍/实心轮廓区分']),
  ('方身管口','短方身、平直尾和突出嘴管，体表斑块；方形剪影与圆泡强区分。',['小尺寸下与泡泡区别更强；轮廓有辨识度'],['嘴管容易被误读成枪；必须作为生物嘴部，不新增射程/弹丸'])],
 'recommendation':'推荐A流线叉尾，鱼身份更直接；若最重视鱼与泡泡区分可选B方身管口。造型、泡泡描边和音色可以独立组合。',
 'questions':['本体选A流线叉尾还是B方身管口？B突出部分仅嘴，不是鱼枪。','融合泡泡选单层加粗边缘还是双层内部光纹？一级仍应轻薄，不能给一级画成造成伤害的爆炸。','八向泡泡更强调八个分离小泡，还是短促八向出现光点？音色选A清亮水泡还是B温润低泡，保持吸附和命中可区分。'],
 'objects':[
  ('1级与融合泡泡','objects/bubble_levels.png','左侧1级薄环，右侧融合双层纹理候选。数字等级无上限，封顶的是尺寸；这些图不是完整等级资产。')],
 'states':[
  ('idle','待机','独立鱼体，没有枪杖。'),('level1','1级吐泡','每1.1秒产生1级；1级接触敌人消失但无伤害。'),('fusion','融合','同主泡泡等级相加，>=2才造成level×8伤害；合成示意不是额外生成两个命中。'),('eight','八向吐泡','图内确有八个1级小泡；0.8秒后恢复慢漂，非爆炸AOE。')],
 'information':['等级/是否融合比体积更重要；尺寸达到上限仍可继续增长等级。','吸附泡泡需要独立状态，目标是吸自己的泡泡；示意不改变105吸附范围或2.5秒。','GIF是四状态编排，不是从待机到融合必然执行的技能连招。'],
 'audio':['清亮水泡','温润低泡']},
'electric_sheep':{
 'name':'触电羊',
 'variants':[
  ('圆团云绒','大团簇羊毛、右侧深色脸、小耳与短蹄，脱落羊毛保持同一团簇语言。',['羊身份清晰；暖绒毛与蓝金电效对比容易读'],['与雷云都偏团状，羊毛点必须无脸无腿避免第二只羊误读']),
  ('叠卷块绒','低平身体、叠卷毛锁、前伸脸和上挑耳；羊毛以折卷堆呈现。',['低宽剪影与云团不同；毛的方向可强调脱落'],['块状羊毛容易像地垫或机械装置，需保留自然纤维感'])],
 'recommendation':'推荐A圆团云绒，羊与羊毛关系更直观；若想避开云团轮廓，可选B叠卷块绒。电效都应局部、只画单一实际路径。',
 'questions':['羊体选A圆团云绒还是B叠卷块绒？两者都无枪杖、无新增角冲撞技能。','脱落羊毛选圆绒团还是折卷堆？必须无脸无腿，只有一个羊毛点，与本体共享电库。','持续电流更偏短促跳弧还是连贯细丝？音色选A干脆电跳还是B绒毛低嗡，不做本体和羊毛各一条双伤害光束。'],
 'objects':[
  ('A圆绒团','objects/wool_patch.png','单一脱落羊毛，无脸无腿，无独立电库。'),('B折卷堆','objects/wool_folded.png','结构不同的羊毛候选，新羊毛替换旧位置，不新增第二处持续点。')],
 'states':[
  ('idle','无电','无电不能因演出而持续造成伤害。'),('wall','撞墙补电','实际撞墙每次+30，满库100；闪光是事件反馈，不是额外攻击。'),('wool','留羊毛','只留下一个羊毛点，本体和羊毛共享charge。'),('zap','放电','单一路径持续伤害；两处覆盖仍算一份消耗与攻击路径，不画双倍伤。')],
 'information':['charge、wool_active/wool_position和zapping是必要状态，不只是装饰灯。','WALL TURN实际max(140,当前速度)，不承诺严格保持低速。','放电origin可能来自羊毛；真实first_target路径可被物件截住，不保证光束永远直达英雄。'],
 'audio':['干脆电跳','绒毛低嗡']}}

APPEARANCE={
 'puffer':[
  {'palette':'薄荷绿主体、浅薄荷高光、深青阴影、蓝灰轮廓。','material':'软乳胶气团的玩具材质意向；短凸点为柔软轮廓，不代表毒刺。','expression':'点状双眼与小张口，脸集中在圆体中央。','personality':'候选性格感：好奇、轻弹、略呆萌；不是已定背景或行为规则。'},
  {'palette':'金黄主体、珊瑚折瓣、奶油细高光、蓝灰轮廓。','material':'折叠气囊的玩具材质意向，用纵向分面表现撑开；不表示机械护甲。','expression':'细点眼配较扁的横口，脸与折瓣形成紧绷对比。','personality':'候选性格感：紧张、憋气、倔强；不改变吸收或放气机制。'}],
 'chicken':[
  {'palette':'金黄圆身、奶油头胸、暖橙翼区、珊瑚圆冠。','material':'哑光搪胶与软羽块面的玩具意向；大色块便于像素尺寸读取。','expression':'小眼前视、短喙、圆冠压低，脸与圆身连成低重心轮廓。','personality':'候选性格感：憨厚但容易慌张，蹲蛋喜剧感强；非新增角色背景。'},
  {'palette':'奶油长颈与躯体、金黄颈部、珊瑚尖冠和扇尾、暖橙脚。','material':'薄片尾羽与修长软胶玩具意向；不是新增盔甲或武器。','expression':'小眼向前、尖冠上扬、窄长颈显得更警觉。','personality':'候选性格感：机灵、急躁、跑跑停停；实际改向仍由现有技能决定。'}],
 'bubble_fish':[
  {'palette':'浅青蓝身体、浅薄荷高光、深蓝鳍面、珊瑚叉尾。','material':'柔软半光泽水玩具意向，实心色块高光；并非本体半透明泡泡。','expression':'前侧小眼和轻开的吐泡口，视线清楚朝前。','personality':'候选性格感：灵动、轻松、爱吐泡；不新增主动操作或连招。'},
  {'palette':'金黄方身、暖橙边面、珊瑚斑块和尾、浅青嘴管。','material':'圆角积木玩具的块面意向，不表示防御装甲；突出部分仍是生物嘴。','expression':'小眼与平直嘴管显得专注、略木讷。','personality':'候选性格感：憨直、执着、稳稳吐泡；不是固定物种或背景设定。'}],
 'electric_sheep':[
  {'palette':'奶油大团羊毛、米色暗面、深紫灰脸、蓝灰蹄与轮廓。','material':'软绒团加哑光脸部的玩具意向；团簇不等于雷云或第二只羊。','expression':'大白眼、细黑瞳与右侧圆脸，带一点发愣的表情。','personality':'候选性格感：温吞、蓬松、突然来电的反差；无新增性格玩法。'},
  {'palette':'奶油折卷毛、灰米卷纹、深紫灰前伸脸、蓝灰轮廓。','material':'叠卷毛束的布绒玩具意向，避免画成机械电池盒。','expression':'侧眼配前伸脸和上挑耳，显得谨慎且专注。','personality':'候选性格感：稳重、警觉、有收束感；不意味着更硬或更高防御。'}]}

def main():
 for ident,data in D.items():
  out=R/'characters'/ident
  variants=[]
  for i,(title,desc,pros,cons) in enumerate(data['variants']):
   letter='ab'[i]
   appearance=APPEARANCE[ident][i]
   full_description=desc+' 配色：'+appearance['palette']+' 材质意向：'+appearance['material']+' 表情：'+appearance['expression']+' '+appearance['personality']
   variants.append({'id':letter,'title':('A ' if i==0 else 'B ')+title,'image':f'variant_{letter}.png','display':f'{letter}_display.png','motion':f'{letter}_states.gif','description':full_description,'palette':appearance['palette'],'material':appearance['material'],'expression':appearance['expression'],'personality':appearance['personality'],'pros':pros,'cons':cons,'status':'unselected concept candidate'})
  states=[]
  for i,(sid,title,desc) in enumerate(data['states']):
   states.append({'id':sid,'title':title,'image':f'states/a_{i}.png','alternative_image':f'states/b_{i}.png','animation':'motion_compare.gif','event':sid,'description':desc})
  if ident=='bubble_fish':
   states.append({'id':'vacuum','title':'吸附泡泡','image':'states/vacuum.png','animation':'','event':'VACUUM_BUBBLE','description':'朝敌人当时方向发射的吸附泡泡；吸引自己的泡泡，持续2.5秒、105范围。仅静态语义示意，箭头和泡泡位置不是实际世界距离，四格GIF不含此独立图。'})
  states.append({'id':'hit_feedback','title':'受击反馈两方向','image':'states/hit_feedback.png','animation':'','event':'actual_HP_loss','description':'同一A造型公平比较A眨眼反馈与B局部碎光。仅真实HP下降触发普通受击；不加击退、无敌、硬直或hitstop。Puffer在immune_left>0免伤时应改吸收反馈，不画假掉血。'})
  states.append({'id':'movement','title':'移动朝向示意','image':'states/movement_direction.png','animation':'','event':'existing_velocity_direction','description':'箭头只说明当前已有速度方向，轻摆/朝向可随之表现；不新增跑步、转向、加速或物理规则。母鸡惊跑仍是已有run技能，和普通移动区分。'})
  if ident=='puffer':
   states.append({'id':'immune_absorb','title':'免伤时的受击吸收','image':'states/immune_absorb.png','animation':'','event':'hit_while_immune_left_positive','description':'immune_left>0时用蓝色吸收反馈并转气，不播放普通HP下降反馈；即使action已转burst，免伤仍可能继续。'})
  data['questions'].append('普通受击反馈选眨眼反馈还是局部碎光？移动朝向箭头仅用于本评审说明，不是新增游戏常驻UI或运动规则。')
  review={'id':ident,'name':data['name'],'cycle':'R03','status':'待用户逐项选择；仅概念评审，非游戏实录、非完整接入帧、非接入包','variants':variants,'comparison':'comparison.png','animation':'motion_compare.gif','recommendation':data['recommendation'],'questions':data['questions'],'states':states,'weapons_objects':[{'name':n,'image':im,'description':desc} for n,im,desc in data['objects']],'information':data['information'],'source_facts':{'document':'SETTING.md','repository':'Gankkiii/balls','commit':'3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47','scope':'代码事实不等于新造型已批准；不修改玩法、数值、物理或随机行为'},'audio_questions':{'options':data['audio'],'source':'../../audio/review.json','scope':'程序合成音色方向；编排试听不代表真实技能时序，未人工听审'},'validation':{'png_svg':'本轮原创整数像素几何，透明96×96候选图；已检查可打开。','concept_animation':'4格、650ms/格、总2.6秒循环；独立状态展示，不是真实战斗时序或完整连续动作。','human_listening':'NOT_RUN','in_game':'NOT_RUN','device':'NOT_RUN'},'missing':['未制作正式接入用完整动作帧、Godot资源或接入清单；这是本轮范围限制，不将概念伪称完成。','候选造型、物件图案、重要动作和音色仍未由用户选定。','未做真实战斗、设备显示或扬声器听感验证。']}
  (out/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
  p=out/'SETTING.md';s=p.read_text().split('\n## 本轮造型候选（未选）')[0]
  if ident=='puffer' and '免伤与放气可并存' not in s:s+='\n补充核对：`start_burst()`不清空`immune_left`，所以免伤与放气可并存；免伤表现应读`immune_left>0`，不能只看`action==immune`。\n'
  s+='\n## 本轮造型候选（未选）\n\n'+ '\n'.join('- '+v['title']+'：'+v['description'] for v in variants)+'\n\n推荐只作建议，不等于用户选择。动作、物件与音色问题见 `review.json`，可独立组合。\n'
  p.write_text(s)
 print('4 role review JSON and independent setting candidate entries written')
if __name__=='__main__':main()
