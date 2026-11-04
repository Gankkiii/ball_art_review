#!/usr/bin/env python3
"""Original R05 review UI. No game writes or image capture input. Run --root output-dir."""
from pathlib import Path
import base64,json,html,argparse,subprocess,cairosvg
P=argparse.ArgumentParser();P.add_argument('--root',required=True);args=P.parse_args();ROOT=Path(args.root);ROOT.mkdir(parents=True,exist_ok=True)
ASSET=Path(__file__).parent/'assets'
INK='#243746';BG='#F7EBCD';PAPER='#FFF9EB';WOOD='#D9BA8C';GOLD='#EFC65B';TEAL='#A9D8C9';CORAL='#E77D65';MUTED='#687A7D';LILAC='#D5C6E5'
class Art:
 def __init__(self): self.s=[]
 def rect(self,x,y,w,h,fill=PAPER,stroke=INK,sw=3):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
 def text(self,x,y,t,size=24,weight=500,color=INK):self.s.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(t))}</text>')
 def line(self,x,y,x2,y2,color=INK,width=3,dash=''):self.s.append(f'<path d="M{x} {y} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>')
 def image(self,x,y,w,name):
  data=base64.b64encode((ASSET/f'{name}.png').read_bytes()).decode();self.s.append(f'<image x="{x}" y="{y}" width="{w}" height="{w}" href="data:image/png;base64,{data}" style="image-rendering:pixelated"/>')
 def button(self,x,y,w,t,active=False):self.rect(x,y,w,54,TEAL if active else PAPER);self.text(x+20,y+36,t,23,700)
 def pill(self,x,y,w,t,fill=TEAL):self.rect(x,y,w,36,fill,INK,2);self.text(x+12,y+26,t,19,700)
 def egg(self,x,y,scale=1):
  self.s.append(f'<g transform="translate({x} {y}) scale({scale})"><path d="M48 0 H72 V12 H84 V28 H96 V48 H104 V92 H96 V108 H80 V120 H40 V108 H24 V92 H16 V48 H24 V28 H36 V12 H48 Z" fill="{PAPER}" stroke="{INK}" stroke-width="4"/><path d="M44 24H56V36H44ZM76 62H88V74H76ZM36 82H48V94H36Z" fill="{GOLD}"/><path d="M46 8H64" stroke="white" stroke-width="6"/></g>')
 def head(self,variant,title):
  self.rect(0,0,1600,900,BG,BG,0);self.rect(0,0,1600,88,INK,INK,0);self.text(32,56,'BALLS',34,800,BG)
  for i,n in enumerate(['竞技场','主线','仓库','孵蛋']):
   x=888+i*170;self.rect(x,18,150,52,GOLD if i==3 else INK,BG if i!=3 else GOLD,2);self.text(x+38,54,n,24,700,INK if i==3 else BG)
  self.text(42,140,'孵蛋',36,800);self.text(154,138,title,26,600);self.pill(1290,111,264,'概念UI · 人工样例',WOOD)
  self.line(40,161,1560,161,WOOD,2);self.text(40,877,'精灵等级 Lv.0 与技能阶级 +3 分开显示；预览不提前生成随机结果。',19,500,MUTED);self.text(1370,877,f'方案 {variant.upper()}',20,700)
 def parent(self,x,y,w,role,compact=False):
  mother=role=='母亲';self.rect(x,y,w,200 if compact else 310);self.pill(x+16,y+16,100,role,LILAC if mother else TEAL);self.image(x+14,y+57,116,'fish' if mother else 'sheep')
  self.text(x+139,y+90,'泡泡鱼 ♀' if mother else '触电羊 ♂',26,800);self.pill(x+142,y+105,110,'精灵 Lv.0',BG)
  self.text(x+18,y+190,'吸附泡泡 +3  /  八方泡泡 +3' if mother else '转向墙壁 +3  /  放置羊毛 +3',21)
  if not compact:self.text(x+18,y+231,'特性一（待设计）',21);self.button(x+18,y+247,w-36,'查看详情 / 更换')
 def choice(self,x,y,w):
  self.text(x,y,'母亲最高技能并列：由你选择技能 1',26,800)
  self.rect(x,y+22,w,66,TEAL);self.text(x+20,y+64,'●  吸附泡泡',25,800);self.pill(x+w-100,y+37,78,'+3',PAPER)
  self.rect(x,y+102,w,66);self.text(x+20,y+144,'○  八方泡泡',25,700);self.pill(x+w-100,y+117,78,'+3',BG)
 def ranges(self,x,y,w):
  self.text(x,y,'先天范围 · 每项独立随机',23,700)
  names=['生命','攻击','防御','速度','重量','大小'];vals=['23–34','30–41','37–48','12–44','8–19','15–26']
  for i,(n,v) in enumerate(zip(names,vals)):
   cols=2 if w<500 else 3; yy=y+42+(i//cols)*35;xx=x+(i%cols)*(w//cols);
   if cols==2:self.rect(xx-3,yy-26,w//cols-17,32,BG,BG,0)
   self.text(xx,yy,n,20);self.text(xx+55,yy,v,21,700)
 def preview(self,x,y,w):
  self.text(x,y,'后代预览',28,800);self.pill(x+w-132,y-29,130,'精灵 Lv.0',TEAL)
  self.text(x,y+44,'泡泡鱼 · 特性随母亲',25,700);self.text(x,y+83,'技能 1：吸附泡泡 · 阶级待随机',22)
  self.text(x,y+121,'技能 2：母种族其余 4 项随机',22);self.text(x,y+155,'其中 3 项待设计，不提前确定',20,500,MUTED)
 def save(self,path,width=1600,height=900):
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><g font-family="Noto Sans CJK SC, sans-serif">'+''.join(self.s)+'</g></svg>';path.with_suffix('.svg').write_text(svg)
  path.with_suffix('.html').write_text(f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden}}svg{{display:block}}</style>'+svg)
  cairosvg.svg2png(bytestring=svg.encode(),write_to=str(path.with_suffix('.png')))

def main(v):
 a=Art();titles={'a':'四步向导','b':'遗传工作台','c':'亲本连图','d':'母亲档案与确认票据'};a.head(v,titles[v])
 if v=='a':
  for i,t in enumerate(['01 亲本','02 继承','03 确认','04 结果']):a.pill(45+i*386,185,350,t,TEAL if i==1 else PAPER)
  a.rect(45,247,365,574,WOOD);a.image(115,273,200,'fish');a.text(75,520,'泡泡鱼 ♀ · 精灵 Lv.0',27,800);a.text(75,563,'母亲决定种族与特性',22);a.line(75,587,379,587);a.text(75,630,'父亲：触电羊 ♂',24,700);a.text(75,669,'精灵 Lv.0 · 技能 +3 / +3',20);a.button(75,738,304,'返回亲本')
  a.rect(438,247,1117,574);a.choice(477,296,585);a.egg(1188,320,1.45);a.text(1162,548,'泡泡鱼 · 未孵化',23,700);a.ranges(477,555,990);a.text(477,705,'后代精灵 Lv.0；后天全 0；基础与最终数值待定',23);a.button(1180,741,330,'下一步：确认',True)
 elif v=='b':
  a.parent(45,190,430,'母亲');a.parent(1125,190,430,'父亲');a.rect(500,190,600,449,WOOD);a.preview(530,237,540);a.choice(530,438,540);a.line(475,330,500,330);a.line(1100,330,1125,330)
  a.rect(45,514,430,307);a.text(70,558,'母种族技能池',26,800);a.text(70,608,'已设计：吸附 / 八方',23);a.text(70,650,'其余 3 项：待设计',23);a.text(70,710,'仅列候选，不锁定技能 2',21);a.button(70,746,380,'规则说明')
  a.rect(1125,514,430,307);a.ranges(1150,550,390);a.text(1150,724,'后天全 0',22);a.text(1150,766,'种族基础 / 最终：待定',22)
  a.rect(500,664,600,157);a.egg(514,681,.8);a.text(626,705,'亲本已选 · 技能 1 已选',25,800);a.text(626,744,'尚未执行，不显示随机结果',21);a.button(810,761,260,'确认并孵蛋',True)
 elif v=='c':
  a.parent(45,190,415,'母亲');a.parent(1140,190,415,'父亲');a.line(460,343,665,343,INK,4);a.line(935,343,1140,343,INK,4);a.pill(490,285,160,'种族 / 特性',LILAC);a.pill(957,285,155,'先天范围',TEAL)
  a.egg(687,199,1.9);a.pill(698,454,205,'后代精灵 Lv.0',TEAL);a.text(630,521,'泡泡鱼 · 尚未生成',27,800)
  a.rect(45,552,1510,269);a.choice(75,598,610);a.preview(765,599,740);a.button(1185,747,330,'查看确认单',True)
 else:
  a.rect(45,190,720,631,WOOD);a.rect(72,212,658,377,LILAC);a.rect(85,225,630,351);a.pill(105,245,140,'母亲档案',LILAC);a.image(97,290,240,'fish');a.text(351,330,'泡泡鱼 ♀',36,800);a.pill(354,353,168,'精灵 Lv.0',TEAL);a.text(353,429,'吸附泡泡 +3',25);a.text(353,476,'八方泡泡 +3',25);a.text(353,533,'特性一（待设计）',23);a.button(105,606,300,'查看母亲详情');a.button(425,606,300,'更换母亲');a.image(98,663,125,'sheep');a.text(248,700,'父亲  触电羊 ♂',27,700);a.text(248,742,'精灵 Lv.0 · 技能 +3 / +3',22);a.text(248,786,'查看详情 / 更换父亲 →',22,700)
  a.rect(800,190,755,421);a.text(830,237,'继承清单',30,800);a.text(830,281,'✓ 泡泡鱼    ✓ 特性随母    ✓ 后代 Lv.0',23);a.choice(830,334,695);a.text(830,548,'技能 2：母种族其余 4 项随机',23);a.text(830,585,'其中 3 项待设计；先天范围详见确认',21,500,MUTED)
  a.rect(800,636,755,185,PAPER,INK,3);a.line(832,651,1525,651,WOOD,3,'10 7');a.egg(824,669,.9);a.text(959,689,'确认票据 · 尚未执行',27,800);a.text(959,732,'随机项待揭晓；后天全 0',22);a.button(1215,754,300,'检查并孵蛋',True)
 return a

def selection(v,father=False):
 a=main(v);a.rect(0,164,1600,683,BG,BG,0);a.text(45,210,'选择亲本 / 查看详情',32,800);a.pill(1180,181,370,'先选性别对应亲本，再返回预览',BG)
 # Two visible areas: filtered picker and full details, real data no invented creatures.
 a.rect(45,239,480,576);a.pill(66,260,203,'母亲 ♀',PAPER if father else LILAC);a.pill(288,260,212,'父亲 ♂',TEAL if father else PAPER);a.text(66,333,'可选亲本 · 示例列表',24,700)
 a.rect(66,358,438,146,PAPER if father else TEAL);a.image(75,365,115,'fish');a.text(209,407,'泡泡鱼 ♀',28,800);a.text(209,447,'精灵 Lv.0',23);a.text(209,482,'母亲已选' if father else '当前选中',20,700)
 a.rect(66,524,438,142,TEAL if father else PAPER);a.image(75,535,105,'sheep');a.text(209,573,'触电羊 ♂',26,700);a.text(209,614,'当前选中' if father else '父亲页签可选',21);a.text(66,721,'按性别切换；列表仅显示示例',21);a.button(66,746,438,'返回预览')
 a.rect(550,239,1005,576);a.image(575,249,128,'sheep' if father else 'fish');a.text(760,289,'触电羊 ♂' if father else '泡泡鱼 ♀',32,800);a.pill(761,310,156,'精灵 Lv.0',TEAL)
 a.text(760,372,'当前：特性一（待设计）',23)
 a.text(580,412,'其他特性：特性二 / 特性三（均待设计）',22)
 a.text(580,454,'技能 1：转向墙壁 +3' if father else '技能 1：吸附泡泡 +3',24,700);a.text(1060,454,'技能 2：放置羊毛 +3' if father else '技能 2：八方泡泡 +3',24,700)
 a.text(580,492,'其余技能：技能 3 / 4 / 5（均待设计，无已定效果）',22)
 for xx,t in [(580,'属性'),(735,'种族基础'),(955,'先天'),(1140,'后天'),(1330,'最终')]:a.text(xx,535,t,23,700)
 for i,(n,val) in enumerate(zip(['生命','攻击','防御','速度','重量','大小'],[23,30,37,44,8,15] if father else [34,41,48,12,19,26])):
  yy=573+i*31
  for xx,t in [(580,n),(735,'待定'),(955,str(val)),(1140,'0'),(1330,'待定')]:a.text(xx,yy,t,22)
 a.text(580,782,'父亲技能身份不继承给后代。' if father else '种族与特性随母亲。',21)
 a.button(1165,746,355,'使用此父亲 →' if father else '使用此母亲 →',True);return a

def father_details(v):return selection(v,True)

def execute(v):
 a=main(v);a.rect(230,218,1140,581,PAPER,INK,5);a.pill(263,245,310,'确认 · 执行前最后检查',GOLD);a.text(263,336,'泡泡鱼 ♀  ×  触电羊 ♂',34,800);a.pill(263,364,390,'双方精灵等级均为 Lv.0',TEAL)
 a.text(263,438,'后代：泡泡鱼 · 精灵 Lv.0 · 特性随母亲',27,700);a.text(263,480,'技能 1：吸附泡泡（并列由你选）· 阶级待随机',24);a.text(263,520,'技能 2：母种族其余 4 项随机，其中 3 项待设计',23)
 a.ranges(263,562,1040)
 a.text(263,703,'基础 / 最终待定；后天全 0',20,500,MUTED)
 a.text(263,673,'立即孵化并保存本机；失败不入仓。无新增计时或消耗。',22,700);a.button(263,724,300,'返回修改');a.button(1005,724,330,'立即孵化',True);a.egg(1143,280,1.4);return a

def outcome(v):
 a=Art();a.head(v,'执行后的两种去向');a.pill(45,185,1510,'状态示意 · 本轮未实际孵化，随机字段只在读取真实返回后显示',WOOD)
 a.rect(45,245,730,568);a.pill(73,273,232,'✓ 保存成功',TEAL);a.image(92,315,165,'fish');a.text(294,356,'泡泡鱼 · 精灵 Lv.0',29,800);a.text(294,403,'已保存到本机仓库',25,700);a.text(73,516,'真实结果读取区',27,800);a.text(73,563,'编号 / 性别 / 技能阶级 / 先天值',23);a.text(73,604,'由本次实际孵化返回，不预填随机结果',22,500,MUTED);a.text(73,656,'特性随母；基础 / 最终待定；后天 0',22);a.button(73,727,320,'到仓库查看',True);a.button(418,727,325,'返回亲本选择')
 a.rect(805,245,750,568);a.pill(834,273,250,'! 本机保存失败',CORAL);a.text(834,368,'未加入仓库',34,800);a.text(834,425,'请检查设备存储空间。',26);a.text(834,493,'保留亲本选择与预览，返回后再执行。',23);a.text(834,545,'再次执行会重新随机，不能承诺同一结果。',22);a.text(834,613,'此处不显示“已入仓”或虚构编号。',22,500,MUTED);a.button(834,727,690,'返回预览 / 检查后重新孵化',True);return a

def empty_rules(v):
 a=Art();a.head(v,'选择亲本与规则说明');a.rect(45,190,655,632);a.text(75,244,'先选择一母一父',32,800)
 for yy,role,col in [(285,'母亲 ♀',LILAC),(469,'父亲 ♂',TEAL)]:
  a.rect(75,yy,595,151,BG,INK,2);a.pill(95,yy+18,160,role,col);a.text(95,yy+98,'尚未选择',26,700);a.button(398,yy+69,244,'选择亲本 →')
 a.text(75,683,'缺任一亲本，不显示孵化操作。',25,700);a.text(75,728,'选择后查看后代预览，再选择并列技能。',23);a.text(75,777,'无成本、倒计时或亲本消耗。',23)
 a.rect(730,190,825,632);a.pill(760,214,760,'当前代码临时规则 · 不代表长期平衡已确认',WOOD)
 lines=[(293,'技能 1：母亲最高阶技能；并列才由你二选一。'),(341,'强化阶级：父母各自最高阶之间随机，含两端。'),(389,'较高值未到 +10 时，另有 1% 覆盖为较高值 +1。'),(437,'本人工 +3 / +3 样例：99% 为 +3，1% 为 +4。'),(500,'技能 2：母种族 5 池排除技能 1，余 4 项随机。'),(548,'其中 3 项待设计，不提前确定身份或战斗效果。'),(596,'技能 2 阶级 +1～+9，概率随阶级递减：'),(644,'权重依次 9 : 8 : 7 : 6 : 5 : 4 : 3 : 2 : 1。'),(707,'后代精灵始终 Lv.0，技能 +n 不是精灵等级。'),(755,'种族 / 特性随母；先天六项分别在双亲范围随机。'),(791,'后天全 0；种族基础 / 最终仍待定。')]
 for yy,t in lines:a.text(760,yy,t,22,700 if yy in [293,500,707] else 500)
 return a

def result_table(a,x,y,w,row=35):
 cols=[0,.23,.48,.67,.84]
 for c,t in zip(cols,['属性','种族基础','先天','后天','最终']):a.text(x+w*c,y,t,20,700)
 for i,(n,value) in enumerate(zip(['生命','攻击','防御','速度','重量','大小'],[23,30,37,12,8,15])):
  yy=y+35+i*row;a.line(x,yy+10,x+w-8,yy+10,WOOD,1)
  for c,t in zip(cols,[n,'待定',str(value),'0','待定']):a.text(x+w*c,yy,t,21,700 if c==.48 else 500)

def result_skills(a,x,y,w):
 a.rect(x,y,w,58,TEAL,INK,2);a.text(x+15,y+38,'吸附泡泡   +3',25,800)
 a.rect(x,y+72,w,58,PAPER,INK,2);a.text(x+15,y+110,'八方泡泡   +2',25,800)

def success(v):
 a=Art();a.head(v,{'a':'四步向导 · 完整结果','b':'遗传工作台 · 完整结果','c':'亲本连图 · 完整结果','d':'结果票据 · 完整结果'}[v])
 if v=='a':
  for i,t in enumerate(['01 亲本','02 继承','03 确认','04 结果']):a.pill(45+i*386,185,350,t,TEAL if i==3 else PAPER)
  a.rect(45,245,365,577,WOOD);a.image(125,267,192,'fish');a.text(75,504,'#21 泡泡鱼 ♀',31,800);a.pill(75,526,170,'精灵 Lv.0',TEAL);a.text(75,615,'母亲：泡泡鱼 ♀',23,700);a.text(75,662,'父亲：触电羊 ♂',23);a.button(75,741,304,'返回亲本选择')
  a.rect(438,245,1117,577);a.pill(468,267,1055,'人工结果示例 · 非孵化实录 / 非真实写盘',WOOD);a.text(470,348,'特性一（待设计） · 随母亲',26,700)
  result_skills(a,470,378,395);result_table(a,915,350,604,46);a.text(470,577,'技能 +n 与精灵 Lv.0 独立显示',21);a.text(470,624,'先天示例均在父母对应范围内',21);a.text(470,667,'本页演示结果阅读，不代表实际拥有',21,500,MUTED);a.button(470,741,395,'到仓库查看',True);a.button(1100,741,415,'再次孵化 → 返回确认')
 elif v=='b':
  a.parent(45,190,390,'母亲');a.parent(1165,190,390,'父亲');a.rect(45,530,390,292,WOOD);a.text(70,579,'本次继承选择',27,800);a.text(70,635,'母亲并列：吸附泡泡',24);a.text(70,684,'父亲技能身份不继承',22);a.button(70,740,340,'返回修改亲本')
  a.rect(1165,530,390,292);a.text(1190,576,'后续去向',27,800);a.text(1190,629,'仅本机保存，无云同步',22);a.button(1190,664,340,'到仓库查看',True);a.button(1190,740,340,'再次孵化 → 返回确认')
  a.rect(460,190,680,632,WOOD);a.pill(482,211,636,'人工结果示例 · 非孵化实录 / 非真实写盘',PAPER);a.image(482,250,116,'fish');a.text(625,285,'#21 泡泡鱼 ♀',30,800);a.pill(627,306,170,'精灵 Lv.0',TEAL);a.text(485,404,'特性一（待设计） · 随母',24,700);result_skills(a,485,425,630);result_table(a,485,595,630,29)
 elif v=='c':
  a.parent(45,190,415,'母亲',True);a.parent(1140,190,415,'父亲',True);a.line(460,280,665,280,INK,4);a.line(935,280,1140,280,INK,4);a.image(700,184,192,'fish');a.pill(664,368,270,'#21 泡泡鱼 ♀ · Lv.0',TEAL)
  a.pill(45,422,1510,'人工结果示例 · 非孵化实录 / 非真实写盘 · 亲本连线只说明来源',WOOD)
  a.rect(45,483,895,339);result_table(a,75,530,835,35);a.rect(965,483,590,339);a.text(991,528,'特性一（待设计） · 随母亲',25,700);result_skills(a,991,553,538);a.button(991,740,238,'到仓库查看',True);a.button(1245,740,284,'返回确认 / 再孵化')
 else:
  a.rect(45,190,525,632,WOOD);a.rect(64,210,483,465,LILAC);a.rect(77,223,457,438);a.pill(97,242,180,'母亲档案',LILAC);a.image(210,279,192,'fish');a.text(105,501,'泡泡鱼 ♀ · 精灵 Lv.0',27,800);a.text(105,548,'吸附泡泡 +3 / 八方泡泡 +3',22);a.text(105,596,'种族与特性来源',23,700);a.image(75,693,96,'sheep');a.text(178,735,'父亲：触电羊 ♂',24,700);a.text(178,777,'精灵 Lv.0 · +3 / +3',21)
  a.rect(605,190,950,632);a.line(627,210,1532,210,WOOD,3,'12 8');a.pill(632,227,894,'人工结果示例 · 非孵化实录 / 非真实写盘',WOOD);a.image(630,278,144,'fish');a.text(803,315,'#21 泡泡鱼 ♀',33,800);a.pill(805,337,170,'精灵 Lv.0',TEAL);a.text(803,412,'特性一（待设计） · 随母',24,700)
  result_skills(a,632,456,320);result_table(a,991,455,530,35);a.button(632,741,320,'到仓库查看',True);a.button(991,741,530,'返回亲本 / 再次孵化确认')
 return a

def phone():
 a=Art();a.rect(0,0,844,390,BG,BG,0);a.rect(0,0,844,56,INK,INK,0);a.text(12,35,'BALLS / 孵蛋',21,800,BG)
 for i,t in enumerate(['竞技场','主线','仓库','孵蛋']):
  x=424+i*103;a.rect(x,6,96,44,GOLD if i==3 else INK,GOLD if i==3 else BG,2);a.text(x+20,35,t,17,700,INK if i==3 else BG)
 a.text(12,83,'A 四步向导 · 选择继承',21,800);a.text(600,81,'844×390 · 概念布局',15,500,MUTED)
 for i,t in enumerate(['01 亲本','02 继承','03 确认','04 结果']):
  x=12+i*208;a.rect(x,96,196,28,TEAL if i==1 else PAPER,INK,1);a.text(x+12,116,t,14,700)
 a.rect(12,136,244,188,WOOD,INK,2);a.image(18,145,64,'fish');a.text(86,164,'母亲 泡泡鱼 ♀',17,700);a.text(86,191,'精灵 Lv.0',16,700);a.text(27,222,'技能强化 +3 / +3',16,700);a.line(26,235,242,235,INK,1);a.text(27,262,'父亲 触电羊 ♂ · Lv.0',16);a.text(27,291,'已选双亲 · 摘要可收起',14)
 a.rect(270,136,562,188,PAPER,INK,2);a.text(286,162,'母亲最高技能并列：你来选择技能 1',18,800)
 for yy,t,sel in [(174,'●  吸附泡泡',True),(226,'○  八方泡泡',False)]:
  a.rect(286,yy,530,44,TEAL if sel else PAPER,INK,2);a.text(300,yy+29,t,18,700);a.text(745,yy+29,'+3',18,800)
 a.text(286,299,'+3 是技能强化；后代精灵仍为 Lv.0，阶级执行时随机。',15)
 for x,w,t,active in [(12,244,'查看双亲详情',False),(270,170,'上一步',False),(452,170,'规则说明',False),(634,198,'下一步：确认',True)]:
  a.rect(x,336,w,44,TEAL if active else PAPER,INK,2);a.text(x+15,365,t,17,700)
 return a

meta=[('a','四步向导','按亲本→继承→确认→结果串行推进，摘要栏保留父母信息。','第一次操作容易理解，每步只有一个主要决定。','查看另一亲本需返回一步，信息对比速度较慢。'),('b','遗传工作台','父母分列两侧，中央固定继承选择，底部直接执行。','同时比对亲本与后代，修改最快。','信息密度最高；小屏需缩放或进一步收起规则。'),('c','亲本连图','父母通过静态关联线汇向中央蛋，继承选择位于下方。','种族与先天来源关系直观，中心视觉最强。','下方规则空间较少，需要详情页承接完整范围。'),('d','母亲档案与确认票据','母亲大卡为起点，父亲为附选卡，右侧继承清单和执行票据。','突出母亲决定种族与特性，确认路径清晰。','父亲属性不常驻；需要详情抽屉才可完整对照。')]
for v,title,diff,strength,limit in meta:
 folder=ROOT/v;folder.mkdir(exist_ok=True)
 for stem,fn in [('main',main),('parents',selection),('father_details',father_details),('execute',execute),('result',outcome),('success',success),('empty_rules',empty_rules)]:fn(v).save(folder/stem)
 data={'page':'hatch','id':v,'title':title,'image':'main.png','difference':diff,'strength':strength,'limit':limit,'detail_images':[{'title':'亲本选择与母亲详情','image':'parents.png'},{'title':'父亲完整详情','image':'father_details.png'},{'title':'执行前确认','image':'execute.png'},{'title':'成功 / 失败状态对照','image':'result.png'},{'title':'完整结果页 · 人工例','image':'success.png'},{'title':'缺亲本与临时规则','image':'empty_rules.png'}],'status':'候选概念UI · 人工样例，未接入/未实际孵化','dimensions':[1600,900],'source':'main.svg / main.html；生成器 ../sources/build_hatch.py','sample':'../../sample.json','notes':['主图展示母亲技能+3/+3并列，玩家选择吸附泡泡；只有并列才出现二选一。','精灵恒Lv.0；+3是技能阶级，临时概率不代表精灵升级。','技能2来自母种族剩余4项，3项尚待设计；不假定抽到具体项。','种族与特性随母，先天按父母对应维度范围随机，后天0。','SVG/HTML为原始设计源码，PNG为该源码渲染的概念稿，不是游戏实录。']}
 if v=='a':
  phone().save(folder/'phone',844,390);data['detail_images'].append({'title':'844×390横屏手机布局','image':'phone.png'})
 (folder/'review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
variants=[]
for v,*_ in meta:
 data=json.loads((ROOT/v/'review.json').read_text());data['image']=v+'/'+data['image'];data['detail_images']=[dict(item,image=v+'/'+item['image']) for item in data['detail_images']];variants.append(data)
(ROOT/'review.json').write_text(json.dumps({'page':'hatch','title':'孵蛋 · 四种布局','variants':variants,'recommendation':'A 易上手；频繁操作可选 B。四案均待用户确认。'},ensure_ascii=False,indent=2))
