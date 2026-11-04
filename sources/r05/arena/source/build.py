from pathlib import Path
import base64,json,subprocess,html
R=Path(__file__).resolve().parents[1]; G=Path(__file__).resolve().parent/'assets'; I='#243746'; W='#815A43'; C='#F6EDD9'; B='#67AFC9'; Y='#EFC65B'
def data(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
class Page:
 def __init__(s):s.a=[]
 def rect(s,x,y,w,h,c,stroke=None,sw=3):s.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
 def text(s,x,y,t,size=22,color=I,anchor='start'):s.a.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}" font-family="Noto Sans CJK SC,sans-serif" font-weight="600">{html.escape(str(t))}</text>')
 def img(s,p,x,y,w,h):s.a.append(f'<image href="{data(p)}" x="{x}" y="{y}" width="{w}" height="{h}" style="image-rendering:pixelated"/>')
 def icon(s,k,x,y,n=28):s.img(G/'ui'/('icon_'+k+'.png'),x,y,n,n)
 def panel(s,x,y,w,h,color=C):
  s.rect(x+5,y+6,w,h,'#C9B99A');s.rect(x,y,w,h,I);s.rect(x+4,y+4,w-8,h-8,W);s.rect(x+8,y+8,w-16,h-16,color);s.rect(x+8,y+8,w-16,3,'#FFF9EA')
 def nav(s,mode='top'):
  for n,t in enumerate(['竞技场','主线','仓库','孵蛋']):
   x=48+n*137;y=28 if mode=='top' else 800
   s.rect(x,y,124,48,I);s.rect(x+3,y+3,118,42,'#A6CFC1' if n==0 else C);s.text(x+62,y+32,t,22,anchor='middle')
 def controls(s,x,y,vertical=False):
  ks=['pause','1×','2×','3×','replay','new_seed','sound_on','info']
  for j,k in enumerate(ks):
   xx=x if vertical else x+j*64; yy=y+j*64 if vertical else y
   s.panel(xx,yy,54,54,'#A6CFC1' if j==1 else C)
   if '×' in k:s.text(xx+27,yy+35,k,22,anchor='middle')
   else:s.icon(k,xx+13,yy+13,28)
 def portrait(s,n,x,y,size=72):s.img(G/'characters'/n/'idle.png',x,y,size,size)
 def skills(s,n,x,y,gap=78):
  for j,(k,cd) in enumerate(( [('vacuum','3.8'),('eight','7.8')] if n==0 else [('wall','1.8'),('wool','4.8')])):
   xx=x+j*gap;s.panel(xx,y,64,64);s.icon(k+'_28',xx+18,y+8,28);s.a.append(f'<rect x="{xx+8}" y="{y+8}" width="48" height="34" fill="#243746" opacity="0.14"/>');s.text(xx+32,y+56,cd,18,anchor='middle')
 def hp(s,n,x,y,width=180):
  s.icon('heart',x,y,24);s.text(x+34,y+23,110 if n==0 else 120,28);s.rect(x,y+35,width,10,W);s.rect(x+2,y+37,(width-4)*(110/120 if n==0 else 1),6,B if n==0 else Y)
 def resource(s,n,x,y):
  s.icon('bubble_28' if n==0 else 'bolt_28',x,y,28);s.text(x+39,y+25,'11' if n==0 else '17.5',23)
  if n:s.rect(x,y+38,128,5,W);s.rect(x,y+38,128*.175,5,Y)
 def world(s,x,y):
  s.img(G/'ui/environment/arena_wood_frame.png',x-10,y-10,720,620);s.img(G/'ui/environment/arena_floor.png',x,y,700,600)
  for bx,by,lev in [(155,130,1),(230,175,1),(330,220,3),(400,340,1),(510,430,1),(220,460,1),(120,340,1),(500,180,1),(570,300,1),(330,470,1),(420,110,1)]:
   rr=9+(lev**.5)*3; col='#9ECDD6' if lev==1 else '#708E9E';s.a.append(f'<circle cx="{x+bx}" cy="{y+by}" r="{rr}" fill="none" stroke="{col}" stroke-width="{2 if lev==1 else 4}"/>');s.text(x+bx,y+by+5,lev,13,anchor='middle')
  s.img(G/'characters/bubble_fish/idle.png',x+240-48,y+280-56,96,96);s.img(G/'characters/electric_sheep/idle.png',x+470-48,y+300-56,96,96);s.img(G/'characters/electric_sheep/objects/wool.png',x+485,y+400,64,64)
 def finish(s,p):p.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="900" viewBox="0 0 1600 900">'+''.join(s.a)+'</svg>')
SCHEMES=[('a','转播席','全部角色状态集中顶部横条，底部只留观战操作。','场边无状态卡，完整横向计分条便于连续扫读。','顶部信息较集中，注意力需在战斗与顶栏切换。',(450,220)),('b','双边卡片','左右独立角色卡，技能和资源跟随对应一方。','延续已选左右方向，归属最清楚。','两侧留白较多，双方信息需要横向扫视。',(450,180)),('c','单侧控制塔','世界靠左，双方状态与纵向操作汇入右塔。','单手右侧操作，状态可连续扫读。','右侧信息较密，战斗中心偏左。',(200,180)),('d','英雄控制坞','角色状态下沉为双卡，顶部仅保留页面导航。','技能资源集中在底部，画面顶部轻。','底部占用明显，需要上下关注技能与战斗。',(450,110))]
items=[]
for id,title,diff,strength,limit,world in SCHEMES:
 p=Page();p.rect(0,0,1600,900,'#E3DAC3');p.rect(0,0,1600,88,'#D5C5A3');p.rect(0,88,1600,4,W)
 for yy in range(112,890,32):
  for xx in range(28,1580,32):p.rect(xx,yy,2,2,'#D6CCB4')
 p.nav();p.text(26,887,'概念 · 示例数据',14,W);p.world(*world)
 if id=='a':
  for n,x in enumerate([176,836]):
   p.panel(x,98,588,108);p.portrait(['bubble_fish','electric_sheep'][n],x+12,102,96);p.hp(n,x+122,110,186);p.resource(n,x+124,160);p.skills(n,x+342,122,88);p.icon('info',x+540,139,24)
  p.panel(518,832,564,62);p.controls(545,838)
 elif id=='b':
  for n,x in enumerate([164,1200]):
   p.panel(x,180,230,600);p.portrait(['bubble_fish','electric_sheep'][n],x+67,208,96);p.hp(n,x+27,330,176);p.resource(n,x+27,418);p.skills(n,x+39,534,88);p.icon('info',x+101,705,28)
  p.controls(550,811)
 elif id=='c':
  p.panel(980,124,386,668)
  for n,y in enumerate([155,450]):
   p.portrait(['bubble_fish','electric_sheep'][n],1010,y,88);p.hp(n,1110,y+10,212);p.resource(n,1014,y+108);p.skills(n,1172,y+104,80)
  p.panel(1410,124,102,580);p.controls(1434,150,True)
 elif id=='d':
  for n,x in enumerate([304,820]):
   p.panel(x,736,476,136);p.portrait(['bubble_fish','electric_sheep'][n],x+10,748,96);p.hp(n,x+115,752,156);p.resource(n,x+115,809);p.skills(n,x+302,768,80)
  p.controls(1040,26)
 p.finish(R/id/'main.svg') if (R/id).exists() else ((R/id).mkdir(),p.finish(R/id/'main.svg'))
 subprocess.run(['inkscape',str(R/id/'main.svg'),'-o',str(R/id/'main.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 items.append({'page':'arena','id':id,'title':title,'image':f'{id}/main.png','source':f'{id}/main.svg','difference':diff,'strength':strength,'limit':limit,'detail_images':[],'world_rect':[*world,700,600],'hidden_info':'ⓘ展开种子、时间、技能说明与资源含义；概念交互待接入。','interaction':'暂停/倍率/重看/新局/音量/信息保持原功能；技能仅自动CD展示。'})
review={'page':'arena','status':'candidate_not_selected','canvas':[1600,900],'baseline':'3dd29e8','kind':'效果图，未接入；统一示例数据，非游戏实录','sample':{'hp':[110,120],'max_hp':[120,120],'cd':[[3.8,7.8],[1.8,4.8]],'charge':17.5,'bubble_count':11,'bubble_levels':[1,1,3,1,1,1,1,1,1,1,1]},'schemes':items,'limits':['实际设备触控、密集物件遮挡、动态状态变化未验证。','所有world均700×600且比例1:1，无碰撞/规则改动。','孵蛋/仓库仅导航入口，本组不新增养成机制。'],'recommendation':'优先比较B延续性和A观战层级；本轮由用户选布局。'}
(R/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
for item in items:
 folder=R/item['id'];svg=(folder/'main.svg').read_text();q=Page();q.a.append('<rect x="0" y="92" width="1600" height="808" fill="#243746" opacity="0.28"/>');q.panel(540,260,520,360)
 q.text(574,309,'信息',26);q.text(1024,308,'×',28,anchor='end');q.text(574,357,'种子 3103     时间 5.3 秒',22)
 q.text(574,409,'泡泡鱼',22);q.text(574,444,'吸附泡泡   /   八方泡泡',20)
 q.text(574,492,'触电羊',22);q.text(574,527,'转向墙壁   /   放置羊毛',20)
 q.text(574,582,'技能自动释放 · 羊毛共享电量',18,W)
 (folder/'info.svg').write_text(svg.replace('</svg>',''.join(q.a)+'</svg>'))
 subprocess.run(['inkscape',str(folder/'info.svg'),'-o',str(folder/'info.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 item['detail_images']=[{'image':f"{item['id']}/info.png",'title':'信息展开示意','source':f"{item['id']}/info.svg"}]
review['schemes']=items
(R/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
from PIL import Image
out=Image.new('RGB',(1600,900),'white')
for j,k in enumerate('abcd'):out.paste(Image.open(R/k/'main.png').convert('RGB').resize((800,450)),((j%2)*800,(j//2)*450))
out.save(R/'overview.png')
# B-only phone reflow: native CSS 844x390, not a scaled desktop screenshot.
q=Page();q.rect(0,0,844,390,'#E3DAC3')
for n,t in enumerate(['竞技场','主线','仓库','孵蛋']):
 x=6+n*102;q.rect(x,0,98,44,I);q.rect(x+3,3,92,38,'#A6CFC1' if n==0 else C);q.text(x+49,29,t,16,anchor='middle')
w=Page();w.world(0,0);q.a.append('<g transform="translate(247 44) scale(0.5)">'+''.join(a for a in w.a[1:] if not a.startswith('<text'))+'</g>')
for bx,by,lev in [(155,130,1),(230,175,1),(330,220,3),(400,340,1),(510,430,1),(220,460,1),(120,340,1),(500,180,1),(570,300,1),(330,470,1),(420,110,1)]:q.text(247+bx*.5,44+by*.5+5,lev,14,anchor='middle')
for n,x in enumerate([6,614]):
 q.panel(x,49,224,286);q.portrait(['bubble_fish','electric_sheep'][n],x+12,60,64);q.icon('heart',x+91,65,20);q.text(x+118,84,110 if n==0 else 120,20)
 q.rect(x+90,94,118,8,W);q.rect(x+92,96,114*(110/120 if n==0 else 1),4,B if n==0 else Y)
 q.resource(n,x+20,133)
 for j,(k,cd) in enumerate(([('vacuum','3.8'),('eight','7.8')] if n==0 else [('wall','1.8'),('wool','4.8')])):
  xx=x+32+j*100;q.panel(xx,217,44,44);q.icon(k+'_28',xx+8,220,28);q.text(xx+22,284,cd,18,anchor='middle')
 q.icon('info',x+98,300,24)
phone_targets=[]
for j,k in enumerate(['pause','1×','2×','3×','replay','new_seed','sound_on','info']):
 xx=224+j*50;yy=346;q.panel(xx,yy,44,44,'#A6CFC1' if j==1 else C)
 if '×' in k:q.text(xx+22,yy+29,k,17,anchor='middle')
 else:q.icon(k,xx+10,yy+10,24)
 phone_targets.append({'id':k,'rect':[xx,yy,44,44]})
q.text(8,376,'示例',14,W)
phone='<svg xmlns="http://www.w3.org/2000/svg" width="844" height="390" viewBox="0 0 844 390">'+''.join(q.a)+'</svg>'
(R/'b/phone.svg').write_text(phone);subprocess.run(['inkscape',str(R/'b/phone.svg'),'-o',str(R/'b/phone.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
review['schemes'][1]['detail_images'].append({'image':'b/phone.png','source':'b/phone.svg','title':'横屏手机布局示意'})
review['phone_demo']={'scheme':'b','viewport_css':[844,390],'world_rect':[247,44,350,300],'world_scale':0.5,'navigation_targets':[[6+n*102,0,98,44] for n in range(4)],'control_targets':phone_targets,'auto_skill_rects':[[x+32+j*100,217,44,44] for x in [6,614] for j in range(2)],'minimum_critical_numeric_font_px':14,'limitations':'仅本图重排示范；真实手机/安全区/手指操作NOT RUN。技能槽只读自动CD，不是点击施放。'}
(R/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
