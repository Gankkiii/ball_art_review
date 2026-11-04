from pathlib import Path
import base64,json,math,random
import cairosvg
ROOT=Path('/workspace/shared/R05-ui-review/story')
INK='#283e45'; MUT='#6d7c78'; PAPER='#fff8e8'; TEAL='#398a79'; GOLD='#e4b86d'
class Art:
 def __init__(self): self.s=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" shape-rendering="crispEdges"><style>text{font-family:"Noto Sans CJK SC",sans-serif} .pixel{image-rendering:pixelated}</style>']
 def rect(self,x,y,w,h,c,stroke=None,sw=3):
  opacity='';
  if c.startswith('#') and len(c)==9: opacity=f' fill-opacity="{int(c[7:9],16)/255}"';c=c[:7]
  self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"'+opacity+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
 def text(self,x,y,t,size=24,c=INK,weight=400): self.s.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{c}">{t}</text>')
 def path(self,d,c,stroke=None,sw=4,dash=None): self.s.append(f'<path d="{d}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,c,stroke=None,sw=3): self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
 def panel(self,x,y,w,h,c=PAPER):
  self.rect(x+6,y+7,w,h,'#263e4530');self.rect(x,y,w,h,c,INK,3); self.rect(x+6,y+6,w-12,3,'#ffffff80')
 def button(self,x,y,w,t,on=True):
  self.rect(x+2,y+5,w,84,'#3c585340'); self.rect(x,y,w,84,TEAL if on else '#e2dfd3',INK if on else '#a6aea4',3);self.text(x+w/2-len(t)*14,y+52,t,28,'#fff9e9' if on else '#89938a',600)
 def sprite(self,id,x,y,w):
  p=Path('/workspace/balls/assets/r04/characters')/id/'idle.png'; b=base64.b64encode(p.read_bytes()).decode();self.s.append(f'<image class="pixel" x="{x}" y="{y}" width="{w}" height="{w}" href="data:image/png;base64,{b}"/>')
 def tree(self,x,y,s=1):
  self.rect(x-5*s,y,10*s,30*s,'#81664d'); self.path(f'M{x-34*s},{y+8*s} V{y-15*s} H{x-23*s} V{y-34*s} H{x-11*s} V{y-48*s} H{x+9*s} V{y-34*s} H{x+24*s} V{y-15*s} H{x+34*s} V{y+8*s} Z','#598c6d');self.rect(x-18*s,y-24*s,16*s,10*s,'#8bab72')
 def rock(self,x,y,s=1):self.path(f'M{x},{y} h{30*s} v{-11*s} h{-6*s} v{-9*s} h{-17*s} v{9*s} h{-7*s} Z','#a4b4a0')
 def house(self,x,y,s=1):
  self.rect(x,y,130*s,105*s,'#e4d4ac',INK,3);self.path(f'M{x-12*s},{y} V{y-12*s} H{x+8*s} V{y-30*s} H{x+28*s} V{y-48*s} H{x+98*s} V{y-30*s} H{x+120*s} V{y-12*s} H{x+140*s} V{y} Z','#9f7354',INK,3);self.rect(x+52*s,y+45*s,28*s,60*s,'#658b7d');self.rect(x+14*s,y+24*s,25*s,26*s,'#f2c976',INK,2);self.rect(x+91*s,y+24*s,25*s,26*s,'#f2c976',INK,2)
 def footer(self,note):
  self.rect(0,804,1600,96,'#f7f1df',INK,3)
  self.text(46,865,'BALLS',28,TEAL,800)
  for i,t in enumerate(['竞技场','主线','仓库','孵蛋']):
   x=445+i*228;self.rect(x,806,208,84,TEAL if i==1 else '#fff9eb',INK,3);self.text(x+62,861,t,27,'#fff9eb' if i==1 else INK,600)
  self.text(1456,864,'?',30,INK,700)
 def header(self,crumb):
  self.rect(0,0,1600,100,PAPER,INK,3);self.button(32,8,96,'‹');self.text(162,62,'主线',34,INK,700);self.text(282,61,crumb,24,MUT);self.rect(1065,24,404,52,'#eee5cf');self.text(1088,59,'结构占位 · 玩法待定',25,'#7a6c57');self.text(1513,61,'?',28,TEAL,700)
 def save(self,path):
  source=''.join(self.s)+'</svg>';path.write_text(source);cairosvg.svg2png(bytestring=source.encode(),write_to=str(path.with_suffix('.png')))

def terrain(a,x,y,w,h,seed=4):
 rng=random.Random(seed);a.rect(x,y,w,h,'#d5e3be');
 for i in range(85):
  xx=x+rng.randrange(w//8)*8;yy=y+rng.randrange(h//8)*8;a.rect(xx,yy,8,4,rng.choice(['#c8d8aa','#b9ce9d','#e4e9ca']))

def a_map():
 a=Art();a.rect(0,0,1600,900,'#e8efdf');a.header('世界图 / 区域 A');terrain(a,28,120,1090,674)
 # Pixel river
 a.path('M170 120 h110 v96 h80 v100 h-35 v110 h90 v116 h-80 v126 h-110 v126 h-80 V648 h110 V532 h80 V414 h-80 V310 h-85 Z','#a7c9c3');a.path('M200 120 h30 v100 h80 v100 h-40 v110 h90 v100 h-85 v140 h-90 v120','none','#c8e0d6',9)
 # diffuse hills patches
 a.path('M610 150 h300 v45 h80 v115 H720 v-45 H610Z','#adc894');a.path('M685 540 h230 v34 h115 v110 H760 v-50 h-75Z','#b8cfa0')
 for x,y,s in [(75,230,1.2),(480,230,1.3),(970,320,1.3),(625,700,1.2),(1000,710,1),(110,700,1.4),(805,175,1.0),(920,205,.7)]: a.tree(x,y,s)
 a.path('M395 596 L510 474 L735 430 L873 302','none','#fff9e7',14);a.path('M395 596 L510 474 L735 430 L873 302','none','#87998c',4,'10 12')
 for i,(x,y) in enumerate([(395,596),(510,474),(735,430),(873,302)]):
  a.rect(x-27,y-27,54,54,PAPER,TEAL if i==0 else '#819583',4);a.text(x-9,y+10,chr(65+i),25,TEAL,700)
 a.house(560,285,.7);a.sprite('electric_sheep',555,503,170);a.sprite('bubble_fish',135,320,155)
 a.panel(1150,122,418,672);a.text(1181,178,'区域 A',36,INK,700);a.text(1181,218,'地点结构示意',23,MUT);a.rect(1180,252,358,208,'#d9e3c7');a.house(1250,336,.9);a.tree(1495,379,.7);a.text(1182,510,'章节 / 内容待定',26,INK,600);a.text(1182,551,'虚线仅表示候选导航',22,MUT);a.text(1182,588,'不表示既定关卡或进度',22,MUT);a.button(1180,636,358,'查看结构');a.text(1200,752,'地图点选 → 右侧抽屉',22,TEAL)
 a.panel(57,141,280,56);a.text(76,179,'拖动地图  ·  −  ＋',23);a.footer('');return a

def b_book():
 a=Art();a.rect(0,0,1600,900,'#6b8377');a.header('旅程画册 / 跨页');
 for x,y in [(60,285),(1490,230),(125,720),(1500,690)]:a.tree(x,y,1.7)
 a.rect(142,156,1316,620,'#435b51');a.rect(150,144,1300,620,'#b4966b',INK,4);a.rect(168,125,1264,616,PAPER,INK,4);a.rect(793,126,14,614,'#cabd9f');a.rect(784,127,8,612,'#e7ddc5');a.rect(807,127,8,612,'#eadfc9')
 a.text(208,181,'A  /  旅程页',24,TEAL,700);a.text(208,239,'一页，一处风景',39,INK,700);terrain(a,208,273,535,326,2);a.path('M208 480 h535 v119 H208Z','#aac8c0');a.rect(260,467,369,22,'#c9ad78');a.rect(281,480,13,70,'#a18b64');a.rect(583,480,13,70,'#a18b64');a.tree(269,390,1.1);a.tree(670,405,1.1);a.sprite('bubble_fish',350,363,230);a.text(208,651,'风景为原创结构示意',22,MUT)
 a.text(858,201,'地点 A',40,INK,700);a.text(858,246,'内容待定',26,MUT);a.path('M858 277 H1369','none','#ccbea0',3);a.text(858,330,'章节概览',28,INK,600)
 for i,t in enumerate(['地点简介占位','角色片段占位','其他内容占位']):
  y=360+i*71;a.rect(859,y,484,54,'#eee5ce' if i==0 else '#f6efdc',None);a.rect(878,y+17,18,18,TEAL if i==0 else '#c3bea8');a.text(918,y+35,t,24,INK if i==0 else MUT)
 a.button(858,598,302,'展开此页');a.button(1182,598,160,'待定',False)
 # thumb indexes/book ribbon
 for i,t in enumerate(['A','B','C']):a.rect(1432,214+i*112,66,86,TEAL if i==0 else '#d8bb84',INK,3);a.text(1452,266+i*112,t,30,'#fff8e8' if i==0 else INK,700)
 a.button(25,401,90,'‹');a.button(1502,401,90,'›');a.text(635,721,'‹  滑动翻页  /  目录  ›',23,MUT);a.footer('');return a

def c_village():
 a=Art();a.rect(0,0,1600,900,'#d6e4c0');a.header('聚落 / 地点入口');terrain(a,0,102,1600,712,18)
 # flat pixel scenery ribbon
 a.path('M0 144 H150 V127 H275 V158 H420 V138 H665 V158 H920 V127 H1100 V145 H1360 V122 H1600 V265 H0Z','#a8c397')
 a.path('M110 737 H510 V650 H669 V568 H899 V490 H1016 V615 H1380 V680 H1460 V760 H110 V737Z','#e9d5a4');a.path('M665 568 V308 H870 V490','none','#e9d5a4',90)
 a.house(245,370,1.6);a.house(1080,380,1.7);a.house(686,250,1.1)
 for x,y,s in [(100,360,1.5),(1470,325,1.8),(550,260,1.2),(980,215,1.6),(75,755,1.5),(1510,735,1.8),(520,750,.9)]: a.tree(x,y,s)
 a.sprite('electric_sheep',665,540,230);a.sprite('bubble_fish',420,580,180)
 for x,y,t in [(260,542,'地点 A'),(1090,560,'地点 B'),(674,405,'地点 C')]:
  a.panel(x,y,218,70);a.text(x+31,y+45,t,29,INK,700);a.text(x+176,y+45,'›',30,TEAL)
 a.panel(40,123,460,115);a.text(66,166,'用空间选择内容',31,INK,700);a.text(66,208,'建筑仅为导航占位',24,MUT)
 a.panel(1075,125,482,128);a.text(1101,168,'当前：地点 A',28,INK,600);a.text(1101,213,'轻触入口查看结构',24,MUT)
 a.rect(1121,690,430,93,PAPER,INK,3);a.text(1143,728,'聚落只承载页面导航',24);a.text(1143,763,'建筑功能与主线规则待定',22,MUT);a.footer('');return a

def d_archive():
 a=Art();a.rect(0,0,1600,900,'#dfe7df');a.header('档案 / 地点 A');a.panel(30,123,416,668,'#f3efdf');a.text(58,177,'旅程档案',33,INK,700);a.rect(58,203,360,62,'#e4e7dc',INK,2);a.circle(83,230,11,'none',MUT,3);a.path('M91 239 L102 250','none',MUT,3);a.text(116,244,'地点 / 章节',24,MUT)
 a.path('M87 305 V699','none','#becabe',5)
 for i,t in enumerate(['地点 A','地点 B','地点 C','地点 D']):
  y=291+i*111;a.circle(87,y+30,11,TEAL if i==0 else '#c4cdbb',INK,2);a.rect(119,y,295,84,TEAL if i==0 else '#e6e8da');a.text(140,y+37,t,27,'#fff8e8' if i==0 else INK,600);a.text(140,y+67,'结构条目',20,'#d5eadd' if i==0 else MUT)
 a.panel(474,123,1095,668);terrain(a,491,140,1060,422,21)
 a.path('M491 300 H692 V246 H970 V288 H1125 V233 H1320 V270 H1551 V562 H491Z','#b6cda3');a.path('M491 482 H880 V416 H1121 V463 H1551 V562 H491Z','#7fa891');a.rect(708,428,572,28,'#d1bb8b');a.house(1140,307,1.0);a.tree(600,350,1.4);a.tree(1425,354,1.7);a.sprite('electric_sheep',850,302,230)
 a.rect(521,168,211,53,PAPER,INK,2);a.text(542,204,'章节舞台 · 示意',22)
 a.text(513,620,'地点 A',39,INK,700);a.text(513,664,'内容与玩法待定',25,MUT);a.button(1190,601,332,'查看档案');a.rect(512,707,1005,56,'#ece7d4');a.text(534,743,'只切换信息视图，不表示已完成 / 未解锁',24,MUT);a.footer('');return a

SPECS={
'a':('世界地图 + 章节抽屉','空间总览 → 点选虚线节点 → 右抽屉 → 结构详情','地图保留全局位置，右侧预览不打断浏览','地图与命名均为占位；横屏小屏点位需控制密度'),
'b':('旅程画册 + 翻页','横向翻页 → 页签定位 → 展开跨页 → 返回画册','一次聚焦一个地点，图画叙事与低文字最自然','不适合一次比较大量条目；章节与内容尚未确定'),
'c':('聚落空间 + 地点入口','点选场景建筑 → 地点浮层 → 查看结构 → 关闭回聚落','入口嵌在场景中，最有角色生活空间感','建筑不是既定功能；需额外提示可点击区域'),
'd':('档案时间轴 + 章节舞台','列表/搜索定位 → 大图预览 → 档案详情 → 返回列表','目录检索快，可容纳后续大量内容','顺序仅信息组织，不是剧情或关卡进度；更偏工具感')}
for key,build in [('a',a_map),('b',b_book),('c',c_village),('d',d_archive)]:
 folder=ROOT/key;folder.mkdir(parents=True,exist_ok=True);art=build();art.save(folder/'page.svg')
 # separate actual modal state, retain visible navigation hierarchy behind dim overlay
 detail=build();detail.rect(0,100,1600,716,'#213c4566');detail.panel(393,232,814,420);detail.text(430,290,'地点 A · 结构预览',34,INK,700);detail.text(1136,288,'×',34,TEAL,700);detail.rect(430,321,735,132,'#e5ead5');detail.text(461,366,'结构占位',30,TEAL,600);detail.text(461,413,'玩法 / 内容 / 推进方式待定',26,MUT);detail.text(432,501,'不会开始战斗，也不显示未确定的奖励',25,MUT);detail.button(430,545,345,'返回'+('地图' if key=='a' else '画册' if key=='b' else '聚落' if key=='c' else '档案'));detail.button(800,545,365,'待定',False);detail.save(folder/'detail.svg')
 title,flow,strength,limit=SPECS[key]
 meta={'page':'story','id':key,'title':title,'image':'page.png','source':'page.svg','difference':flow,'strength':strength,'limit':limit,'detail_images':[{'image':'detail.png','title':'结构详情与返回','source':'detail.svg'}],'status':'candidate_concept_not_game_capture','resolution':[1600,900],'gameplay_status':'结构占位 / 玩法待定','navigation':['竞技场','主线','仓库','孵蛋'],'touch_targets':'主要按钮84px、底栏84px；按844px横屏等比约44px，真实手机触控未验证','assets':{'characters':'原创R04现有idle.png；已读取泡泡鱼/触电羊独立设定，不改造型','scenery':'本轮原创SVG像素块场景，不使用外部图片'},'validation':{'game_integration':'NOT_RUN','mobile_device':'NOT_RUN','real_navigation':'concept_static_only'}}
 (folder/'review.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
(ROOT/'review.json').write_text(json.dumps({'page':'story','title':'主线','options':[json.loads((ROOT/k/'review.json').read_text())|{'image':k+'/page.png','source':k+'/page.svg','detail_images':[{'image':k+'/detail.png','source':k+'/detail.svg','title':'结构详情与返回'}]} for k in SPECS]},ensure_ascii=False,indent=2))
(ROOT/'SOURCES.md').write_text('''# R05 主线页面候选\n\n本轮原创矢量像素场景；四案是完整页面概念效果，不是游戏截图。所有主线内容、命名、节点与建筑均为结构占位，玩法待定。无奖励、体力、货币、解锁或推进规则。\n\n原件：balls/assets/r04/characters/{bubble_fish,electric_sheep}/idle.png。已读取R04对应独立SETTING；角色未重制。SVG中嵌入原PNG数据，风格原件无需外链。\n\n中文：系统Noto Sans CJK SC（SIL OFL），未拷贝字体文件。SVG文本、矢量图形保持可编辑；PNG由CairoSVG渲染1600×900。source/build_story.py可重现。\n\n四个全局入口全部保留；返回、层级、提示、可用/待定按钮与弹窗均有概念表现。静态候选未绑定实际导航，未修改正式游戏；手机真机触控/游戏内适配未验证。\n''')
print('done',ROOT)
