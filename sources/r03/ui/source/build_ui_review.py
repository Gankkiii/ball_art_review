#!/usr/bin/env python3
"""R03 concept UI comparison only. No game file is read or changed by this renderer.
Inputs are frozen actual-simulation JSON and copied original candidate images.
SVGs embed images, so each SVG can be viewed independently. Fonts are not bundled.
"""
from pathlib import Path
from html import escape
import json,math,base64,subprocess,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];(R/'images').mkdir(parents=True,exist_ok=True)
INK='#243746';PAPER='#FFF7E4';CREAM='#F7EBCD';WOOD='#D9BA8C';BLUE='#67AFC9';GOLD='#EFC65B';PURPLE='#B89ACF';CORAL='#E77D65';MINT='#8FBDB1'
PRIMARY=json.loads((R/'data/shared_sample.json').read_text());STRESS=json.loads((R/'data/stress_sample.json').read_text())
class Page:
 def __init__(self):self.svg=[];self.texts=[]
 def add(self,s):self.svg.append(s)
 def rect(self,x,y,w,h,c,opacity=1):self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{c}" opacity="{opacity:g}"/>')
 def line(self,x1,y1,x2,y2,c=INK,w=2,dash=None):self.add(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w:g}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,fill,stroke=None,width=2,opacity=1):self.add(f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" opacity="{opacity:g}"'+(f' stroke="{stroke}" stroke-width="{width:g}"' if stroke else '')+'/>')
 def poly(self,ps,fill,stroke=None,width=2,opacity=1):self.add('<polygon points="'+' '.join(f'{x:g},{y:g}' for x,y in ps)+f'" fill="{fill}" opacity="{opacity:g}"'+(f' stroke="{stroke}" stroke-width="{width:g}"' if stroke else '')+'/>')
 def frame(self,x,y,w,h,fill=CREAM,edge=INK):
  self.poly([(x+4,y),(x+w-4,y),(x+w-4,y+4),(x+w,y+4),(x+w,y+h-4),(x+w-4,y+h-4),(x+w-4,y+h),(x+4,y+h),(x+4,y+h-4),(x,y+h-4),(x,y+4),(x+4,y+4)],edge)
  self.rect(x+3,y+4,w-6,h-8,fill);self.rect(x+4,y+4,w-8,2,PAPER);self.rect(x+4,y+h-6,w-8,2,WOOD)
 def text(self,value,x,y,size=18,color=INK,kind='hud',anchor='start'):
  self.add(f'<text id="hud_{len(self.texts)}" x="{x:g}" y="{y:g}" font-family="Noto Sans CJK SC, DejaVu Sans, sans-serif" font-size="{size:g}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>')
  if kind=='hud':self.texts.append({'value':str(value),'position':[x,y],'element_id':'hud_'+str(len(self.texts))})
 def image(self,name,x,y,w=None,h=None,flip=False):
  path=R/'assets'/name;im=Image.open(path);w=w or im.width;h=h or im.height;uri='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
  self.add((f'<g transform="translate({x+w:g} {y:g}) scale(-1 1)">' if flip else '')+f'<image x="{0 if flip else x:g}" y="{0 if flip else y:g}" width="{w:g}" height="{h:g}" href="{uri}" style="image-rendering:pixelated"/>'+('</g>' if flip else ''))
 def save(self,name,caption):
  content=''.join(self.svg)
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="828" viewBox="0 0 1100 828"><title>{escape(caption)}</title><rect width="1100" height="48" fill="{INK}"/><text x="16" y="30" font-family="Noto Sans CJK SC, sans-serif" font-size="16" fill="{PAPER}">{escape(caption)}</text><g transform="translate(0 48)">{content}</g></svg>\n'
  dst=R/'images'/f'{name}.svg';dst.write_text(svg)
  subprocess.run(['inkscape',str(dst),'--export-type=png',f'--export-filename={dst.with_suffix(".png")}','--export-background-opacity=0'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  return {'image':'images/'+dst.with_suffix('.png').name,'svg':'images/'+dst.name,'default_text':{'strings':[x['value'] for x in self.texts],'non_whitespace_characters':sum(sum(not c.isspace() for c in x['value']) for x in self.texts),'count_method':'Exact rendered HUD strings in source, including numeric object levels; outside concept caption excluded; not OCR.','elements':self.texts}}
def glyph(p,kind,x,y,size=24,color=INK):
 # Distinct review glyphs; descriptions live in review text, not permanent labels.
 sc=size/24;p.add(f'<g transform="translate({x:g} {y:g}) scale({sc:g})">')
 if kind in ['heart','pause','speed','replay','new_seed','sound_on','roster','info']:
  p.image('icon_'+kind+'.png',0,0,24,24)
 elif kind=='bubble':
  for cx,cy,r in [(7,15,5),(16,8,5),(18,19,3)]:p.circle(cx,cy,r,'none',color,2)
 elif kind=='vacuum':
  p.circle(12,12,9,'none',color,2);p.poly([(0,9),(6,9),(6,5),(12,12),(6,19),(6,15),(0,15)],color)
 elif kind=='eight':
  for i in range(8):
   t=i*math.tau/8;p.circle(12+9*math.cos(t),12+9*math.sin(t),2,color)
 elif kind=='wall':
  p.rect(18,1,4,22,color);p.line(0,12,15,12,color,3);p.poly([(10,5),(17,12),(10,19)],color)
 elif kind=='wool':
  for cx,cy in [(7,11),(12,7),(17,11)]:p.circle(cx,cy,5,CREAM,color,1.5)
  p.line(12,15,12,22,color,2);p.poly([(8,19),(12,24),(16,19)],color)
 elif kind=='bolt':p.poly([(12,0),(21,0),(15,9),(23,9),(5,24),(9,14),(2,14)],color)
 elif kind=='shell':
  p.poly([(1,18),(3,10),(8,4),(16,4),(21,10),(23,18)],MINT,color,2);p.line(2,20,22,20,color,2)
 elif kind=='spin':
  p.circle(12,12,8,'none',color,2);p.poly([(16,0),(24,5),(15,8)],color)
 elif kind=='dummy':
  p.circle(12,6,4,GOLD,color,1.5);p.line(12,10,12,23,color,3);p.line(2,13,22,13,color,3)
 elif kind=='feather':
  p.poly([(3,23),(7,8),(16,1),(22,3),(20,11),(9,20)],PAPER,color,2);p.line(4,22,19,4,color,1.5)
 elif kind=='swap':
  p.line(1,7,21,7,color,2);p.poly([(17,3),(23,7),(17,11)],color);p.line(23,17,3,17,color,2);p.poly([(7,13),(1,17),(7,21)],color)
 p.add('</g>')
def num(v,dec=1):
 if dec==0:return str(math.ceil(v-1e-7))
 v=math.ceil(max(0,v)*10-1e-7)/10
 return f'{v:.1f}'
def worldxy(v):return 200+v[0],90+v[1]
def actor(p,name,pos,flip=False):
 x,y=worldxy(pos);p.image(name+'_a.png',x-48,y-56,96,96,flip)
def hp(p,x,y,width,health,maxhp,color):
 glyph(p,'heart',x,y-20,20);p.text(num(health,0),x+28,y-3,20)
 p.rect(x,y+7,width,9,WOOD);p.rect(x+2,y+9,(width-4)*min(1,max(0,health/maxhp)),5,color)
def skill(p,kind,x,y,cd,compact=False,color=BLUE):
 size=28 if compact else 56
 if compact:
  glyph(p,kind,x,y,20,color);p.text(num(cd),x+26,y+17,16)
 else:
  p.frame(x,y,size,size,PAPER);glyph(p,kind,x+14,y+9,28,color)
  ratio=min(1,max(0,cd/{'vacuum':7,'eight':9,'wall':5,'wool':7,'shell':9,'spin':8,'swap':7,'feather':6}[kind]))
  if ratio:p.rect(x+4,y+4,size-8,(size-8)*ratio,INK,0.24)
  if cd>0:p.text(num(cd),x+size/2,y+size+19,16,anchor='middle')
  else:p.rect(x+4,y+size-8,size-8,3,MINT)
def controls(p,scheme):
 if scheme=='B':start=320;step=52;size=44;p.frame(308,706,484,58,WOOD)
 else:start=488;step=None;size=48;p.frame(480,706,600,58,WOOD)
 specs=[('pause',None),('speed','1×'),('speed','2×'),('speed','3×'),('replay',None),('new_seed',None),('sound_on',None),('roster',None),('info',None)]
 offsets=[0,56,112,168,236,292,360,416,480]
 for i,(icon,label) in enumerate(specs):
  x=start+(i*step if step else offsets[i]);p.frame(x,711,size,size,PAPER);icon_size=20 if label else 24
  p.image('icon_'+icon+'.png',x+(size-icon_size)/2,715 if label else 723,icon_size,icon_size)
  if label:p.text(label,x+size/2,746 if scheme=='B' else 748,12,anchor='middle')
def floor(p):
 p.image('screen_surround.png',0,0,1100,780);p.image('arena_floor.png',200,90,700,600);p.image('arena_wood_frame.png',190,80,720,620)
def world(p,s,stress):
 if not stress:
  if s['wool_active']:
   x,y=worldxy(s['wool_position']);p.circle(x,y,110,'none',GOLD,1,0.2)
   for ox,oy in [(-7,0),(0,-5),(7,0)]:p.circle(x+ox,y+oy,7,CREAM,WOOD,1)
  for b in s['bubbles']:
   x,y=worldxy(b['position']);p.circle(x,y,b['radius'],'#C6E8EC' if b['level']>=2 else 'none',BLUE,2,0.9 if b['level']>=2 else 0.65)
   if b['level']>=2:p.text(str(b['level']),x,y+5,14,anchor='middle')
  if s['zapping']:
   x1,y1=worldxy(s['sheep']['position']);x2,y2=worldxy(s['fish']['position'])
   p.line(x1,y1,(x1+x2)/2+8,(y1+y2)/2-4,GOLD,3);p.line((x1+x2)/2+8,(y1+y2)/2-4,x2,y2,GOLD,3)
  actor(p,'bubble_fish',s['fish']['position']);actor(p,'electric_sheep',s['sheep']['position'],True)
 else:
  for dummy in s['dummies']:
   x,y=worldxy(dummy['position']);p.image('object_dummy.png',x-48,y-56,96,96);p.rect(x-22,y+30,44,5,WOOD);p.rect(x-21,y+31,42*dummy['health']/dummy['max_health'],3,CORAL)
  x,y=worldxy(s['shell_position']);p.circle(x,y,30,'none',MINT,3);p.image('object_shell.png',x-48,y-56,96,96)
  if not s['turtle_hidden']:actor(p,'shell_turtle',s['turtle']['position'])
  actor(p,'crow',s['crow']['position'],True)
  if s['feather']:
   x,y=worldxy(s['crow']['position']);glyph(p,'feather',x-9,y-55,18)
def stats(s,stress):
 if not stress:return [dict(name='bubble_fish',actor=s['fish'],resource_kind='bubble',resource=str(len(s['bubbles'])),skills=['vacuum','eight'],color=BLUE),dict(name='electric_sheep',actor=s['sheep'],resource_kind='bolt',resource=num(s['charge']),skills=['wall','wool'],color=GOLD)]
 return [dict(name='shell_turtle',actor=s['turtle'],resource_kind='shell',resource=num(s['turtle_action_left']),skills=['shell','spin'],color=MINT),dict(name='crow',actor=s['crow'],resource_kind='dummy',resource=str(len(s['dummies'])),skills=['swap','feather'],color=PURPLE)]
def sidebars(p,s,stress):
 for i,a in enumerate(stats(s,stress)):
  x=10 if i==0 else 930;p.frame(x,90,160,600);p.image(a['name']+'_a.png',x+56,110,48,48)
  hp(p,x+14,215,132,a['actor']['health'],a['actor']['max_health'],a['color'])
  glyph(p,a['resource_kind'],x+14,279,28,a['color']);p.text(a['resource'],x+54,303,22)
  if not stress and i==1:p.rect(x+14,322,132,5,WOOD);p.rect(x+14,322,132*s['charge']/100,5,GOLD)
  if stress and i==1 and s['feather']:glyph(p,'feather',x+18,330,24)
  skill(p,a['skills'][0],x+12,420,a['actor']['cd_one'],color=a['color']);skill(p,a['skills'][1],x+88,420,a['actor']['cd_two'],color=a['color'])
def top_bottom(p,s,stress):
 for i,a in enumerate(stats(s,stress)):
  x=16 if i==0 else 574;p.frame(x,10,510,64);p.image(a['name']+'_a.png',x+10,16,48,48)
  hp(p,x+70,40,210,a['actor']['health'],a['actor']['max_health'],a['color'])
  glyph(p,a['resource_kind'],x+314,24,28,a['color']);p.text(a['resource'],x+354,46,20)
  if not stress and i==1:p.rect(x+354,55,130,4,WOOD);p.rect(x+354,55,130*s['charge']/100,4,GOLD)
  sx=18 if i==0 else 938
  for j,k in enumerate(a['skills']):
   # Bottom state slots, not clickable skill controls.
   p.frame(sx+j*74,708,66,60,PAPER);glyph(p,k,sx+j*74+6,717,24,a['color']);p.text(num(a['actor']['cd_one' if j==0 else 'cd_two']),sx+j*74+35,754,14,anchor='middle')
def close_hud(p,s,stress):
 aa=stats(s,stress)
 for i,a in enumerate(aa):
  x=16 if i==0 else 884;p.image(a['name']+'_a.png',x,10,48,48);hp(p,x+58,40,136,a['actor']['health'],a['actor']['max_health'],a['color'])
 positions=[(338,423),(676,501)] if not stress else [(746,169),(318,287)]
 for i,a in enumerate(aa):
  x,y=positions[i];p.frame(x,y,154,60,PAPER)
  glyph(p,a['resource_kind'],x+8,y+5,22,a['color']);p.text(a['resource'],x+38,y+23,18)
  if not stress and i==1:p.rect(x+82,y+15,60,4,WOOD);p.rect(x+82,y+15,60*s['charge']/100,4,GOLD)
  skill(p,a['skills'][0],x+8,y+32,a['actor']['cd_one'],True,a['color']);skill(p,a['skills'][1],x+82,y+32,a['actor']['cd_two'],True,a['color'])
  cx,cy=worldxy((s['shell_position'] if i==0 and stress and s['turtle_hidden'] else a['actor']['position']))
  left_of_actor=x+77<cx;edge=x+154 if left_of_actor else x;target_x=cx-44 if left_of_actor else cx+44;p.line(edge,y+30,target_x,cy,a['color'],1,'3 3')
SCHEMES=[{'id':'A','title':'左右侧栏 · 原方向延续','summary':'状态固定在两侧，视线知道去哪找；延续已选左右侧栏，泡泡和独立物件不背额外文字。','advantages':['与已选鸭兔左右状态区一致，换随机角色只替换状态图标。','状态不跟着角色漂，密集物件中仍可定位HP与CD。','羊电量可用100上限细条；无上限泡泡等级只在泡泡上显示数字。'],'tradeoffs':['两侧常驻面板占视觉宽度，空闲时仍有较大底板。','玩家要在角色和侧栏之间移动视线。'],'questions':['随机角色战斗继续沿用左右侧栏，还是想选另两种更轻的布局？']},
{'id':'B','title':'上下窄条 · 两侧留白','summary':'HP与资源放顶端，四技能冷却靠底边；物理场地不变，两侧取消高面板。','advantages':['中央和侧边更透气，泡泡/铁钉等物件不被高侧栏包围。','HP始终固定，资源与CD分层清楚。'],'tradeoffs':['HP/资源在上、CD在下，视线跨度更大。','底部自动技能与公共操作接近，需用样式区分，避免误认为点击施法。'],'questions':['是否接受HP与冷却分上下两层，而不延续已选左右侧栏？']},
{'id':'C','title':'近身状态 · 边缘摘要','summary':'HP留在上角，资源和两技能CD靠近本体；独立壳/稻草人密集时需要自动避让。','advantages':['资源和动作接近，少看远处面板。','无高侧栏，常驻框体最轻。'],'tradeoffs':['泡泡围身、乌鸦换位或龟隐藏时HUD容易挡路或跳动。','图中只选了静态不遮挡位置；实际需要避让/迟滞逻辑，尚未实现。','移动端小屏必须验证字体、跟随抖动与触控，不可仅凭静图称通过。'],'questions':['愿意接受更高的动态避让实现和验证成本，换取近身读数吗？']}]
results=[]
for scheme in SCHEMES:
 for stress in [False,True]:
  s=STRESS if stress else PRIMARY;p=Page();floor(p);world(p,s,stress)
  {'A':sidebars,'B':top_bottom,'C':close_hud}[scheme['id']](p,s,stress);controls(p,scheme['id'])
  name=scheme['id'].lower()+('_stress' if stress else '_primary')
  pair='脱壳龟入壳＋乌鸦两稻草人' if stress else '泡泡鱼＋触电羊'
  meta=p.save(name,f'方案{scheme["id"]}｜{scheme["title"]}｜{pair}｜概念合成，非游戏实录')
  if not stress:entry=dict(scheme,**meta);results.append(entry)
  else:results[-1]['stress_image']=meta['image'];results[-1]['stress_svg']=meta['svg'];results[-1]['stress_text']=meta['default_text']
review={'version':'R03-UI-review-1','review_only':True,'status':'candidates_not_selected','baseline':'3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47','canvas':{'game':[1100,780],'image':[1100,828],'outside_caption_height':48},'shared_sample':{'data':'data/shared_sample.json','source':'actual Godot fixed-step capture; pair deliberately fixed for fair UI comparison, not a randomized-roll screenshot','characters':['bubble_fish','electric_sheep'],'seed':PRIMARY['seed'],'time':PRIMARY['simulation_time'],'health':[PRIMARY['fish']['health'],PRIMARY['sheep']['health']],'bubbles':len(PRIMARY['bubbles']),'max_bubble_level':max(x['level'] for x in PRIMARY['bubbles']),'sheep_charge':PRIMARY['charge'],'charge_cap':100,'world_positions_unchanged_across_schemes':True},'stress_sample':{'data':'data/stress_sample.json','characters':['shell_turtle','crow'],'turtle_hidden':True,'shell_separate':True,'dummy_count':2,'time':STRESS['simulation_time']},'schemes':results,'recommendation':{'id':'A','reason':'先保留已选左右侧栏，八随机角色仅替换图标/状态读数，拥挤物件下读数稳定；B适合更重视空旷感时选择，C应等动态避让验证。','not_user_selection':True},'shared_rules':['A像素风、浅色场地、横屏和极简作为共同基线；A/B/C是本轮待选布局，不代表用户已放弃原左右侧栏。','所有方案同一角色候选A和相同实际模拟状态；角色造型A不是用户已选。','物理场地700×600、位置/伤害/CD/随机/结算不改；画面世界矩形均[200,90,700,600]。','每个角色两技能为自动状态，只显示冷却，不是点击施法按钮。','底部保留暂停、1×/2×/3×、重看同种子、新随机(10角色池)、声音、全部角色、信息；图标仅概念，未绑定游戏。','无上限泡泡level不画封顶条；羊charge是代码真实0..100，可画细条。','泡泡等级1仍是无伤害小泡泡；只有融合等级>=2显示等级数字，未画1级命中爆炸。','羊本体/羊毛共享一电库，仅画当前实际的一条放电路径，不暗示双倍伤。','龟hidden不画本体，只画独立壳；两个稻草人不是额外英雄，不加主动攻击。'], 'limits':['概念SVG/PNG不是实机截图、不是完整动态UI或接入素材包。','新8角色的造型、动作、音色仍待用户选择；本轮未重设计已交付鸭兔。','性能、真机安全区、触控、长数值和HUD动态避让尚未验证。','养成/挂机等未确定系统不加入战斗UI。'],'sources':['../facts/bubble_fish.md','../facts/electric_sheep.md','../facts/shell_turtle.md','../facts/crow.md','data/asset_sources.json','source/capture_state.gd','source/build_ui_review.py']}
review['eight_role_adapters']=[
 {'id':'puffer','visible_state':'gas0..100；吸收仅活动时用免伤图标/剩余秒','meter':'只有气量可100上限；视觉膨胀不扩大物理圆'},
 {'id':'chicken','visible_state':'存活蛋数量；仅已触发引信/大蛋落地时在对应蛋旁显示临爆提示','meter':'不把下蛋时间/蹲蛋做成必定命中条；小蛋接触引信0.8秒与大蛋落地1.5秒不同'},
 {'id':'bubble_fish','visible_state':'本鱼泡泡数量；融合泡泡在物件上显示level；吸附仅激活时标记','meter':'level无上限，不画百分比满槽；尺寸54上限不是等级上限'},
 {'id':'electric_sheep','visible_state':'charge数值/细条；一处羊毛图标与正在放电状态','meter':'charge有真实100上限；本体和羊毛共享这一条电量'},
 {'id':'magnet_crab','visible_state':'铁钉数；repel_ready图标；当前磁墙仅激活时提示','meter':'静止铁钉无伤害、仅移动时危险；总钉数无已知上限，不画满槽'},
 {'id':'cactus','visible_state':'场上刺数；移动不画速度/奔跑条','meter':'每次散5但存留数量可累积，不假设总量5封顶；REGROW是换位置不是回血'},
 {'id':'shell_turtle','visible_state':'seek/hidden图标；hidden剩余时间；独立壳是否spin','meter':'hidden结束若无可站位置可继续等，不能承诺数字归零必出壳；壳不可伤不画假HP'},
 {'id':'crow','visible_state':'两个稻草人数和实际HP小条；feather单根储存图标','meter':'稻草人各60HP、最多2；羽毛不是弹药条或远程飞羽武器'}
]
review['current_code_routing']='main.gd调用arena.setup(match_seed)从10角色池不重复抽2；showcase.gd当前固定[5,6]鸭兔。这里是随机对战UI候选，未把任何候选接入或改写现默认入口。固定鱼羊与龟鸦是公平比较样例，不称seed已随机抽到它们。'
review['world_view']={'origin':[200,90],'size':[700,600],'scale':1,'same_across_all_schemes':True}
(R/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
thumbs=[]
for e in results:
 im=Image.open(R/e['image']).convert('RGB').resize((550,414),Image.Resampling.LANCZOS);thumbs.append(im)
board=Image.new('RGB',(1650,414),CREAM)
for i,im in enumerate(thumbs):board.paste(im,(i*550,0))
board.save(R/'images/comparison_overview.png')
print('UI review built:3 primary+3 stress self-contained SVG/PNG; exact HUD character counts',[(x['id'],x['default_text']['non_whitespace_characters']) for x in results])
