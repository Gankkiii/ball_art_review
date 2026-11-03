"""R03 original review-only pixel candidates. No image inputs; not game assets or gameplay simulation."""
from pathlib import Path
import json, math, hashlib, argparse
from PIL import Image, ImageDraw, ImageFont

INK='#243746';CREAM='#FFF3DA';CORAL='#EA7E65';METAL='#B1D2D3';GOLD='#EFC65B';PURPLE='#B89ACF'
GREEN='#83B77D';DARKGREEN='#427863';LEAF='#B5D49A';WOOD='#B58C65';STRAW='#E7C77D';CYAN='#86C8C0';MUTED='#657880'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ROOT=None
def rgba(c,a=255):return tuple(int(c[i:i+2],16) for i in [1,3,5])+(a,)
class Art:
 def __init__(self):self.ops=[]
 def box(self,x,y,w,h,c,a=255):self.ops.append(('r',[x,y,w,h],c,a))
 def poly(self,p,c,a=255):self.ops.append(('p',p,c,a))
 def line(self,p,c,w=1,a=255):self.ops.append(('l',p,c,a,w))
 def image(self):
  im=Image.new('RGBA',(48,48));d=ImageDraw.Draw(im)
  for typ,g,c,a,*v in self.ops:
   if typ=='r':x,y,w,h=g;d.rectangle((x,y,x+w-1,y+h-1),fill=rgba(c,a))
   elif typ=='p':d.polygon(g,fill=rgba(c,a))
   else:d.line(g,fill=rgba(c,a),width=v[0])
  return im.resize((96,96),Image.Resampling.NEAREST)
 def svg(self):
  out=['<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 48 48" shape-rendering="crispEdges">']
  for t,g,c,a,*v in self.ops:
   op=f' opacity="{a/255:.6f}"' if a<255 else ''
   if t=='r':x,y,w,h=g;out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"{op}/>')
   elif t=='p':out.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in g)+f'" fill="{c}"{op}/>')
   else:out.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in g)+f'" fill="none" stroke="{c}" stroke-width="{v[0]}"{op}/>')
  return '\n'.join(out+['</svg>'])
 def save(self,folder,name):
  folder.mkdir(parents=True,exist_ok=True);self.image().save(folder/(name+'.png'));(folder/(name+'.svg')).write_text(self.svg())
def octa(a,x,y,w,h,c):
 k=min(3,w//4,h//4);a.poly([(x+k,y),(x+w-k-1,y),(x+w-1,y+k),(x+w-1,y+h-k-1),(x+w-k-1,y+h-1),(x+k,y+h-1),(x,y+h-k-1),(x,y+k)],c)
def eye(a,x,y,blink=False):
 a.box(x,y,3,1 if blink else 4,INK)
 if not blink:a.box(x,y,1,1,CREAM)
def star(a,x,y,c=GOLD):a.poly([(x,y-3),(x+1,y-1),(x+3,y),(x+1,y+1),(x,y+3),(x-1,y+1),(x-3,y),(x-1,y-1)],c)
def cactus(v='a',state='idle',phase=0):
 a=Art();a.box(15,39,22,2,INK,35)
 if v=='a':
  octa(a,17,9,15,31,INK);octa(a,19,11,11,27,GREEN);a.box(20,14,2,20,LEAF);a.box(27,14,2,22,DARKGREEN)
  a.poly([(10,17),(15,17),(15,26),(19,26),(19,32),(9,32),(7,30),(7,20),(10,20)],INK)
  a.poly([(10,20),(13,20),(13,28),(18,28),(18,30),(10,30)],GREEN)
  a.poly([(31,23),(35,23),(35,14),(39,14),(41,17),(41,29),(38,32),(30,32)],INK)
  a.poly([(32,26),(37,26),(37,17),(39,17),(39,28),(37,30),(32,30)],GREEN)
  for x,y in [(17,15),(32,17),(8,22),(15,34),(30,33),(37,13)]:a.line([(x,y),(x-2,y-2)],CREAM)
  a.box(21,6,3,5,CORAL);a.box(18,8,9,2,CORAL);a.box(22,8,2,2,GOLD)
  eye(a,24,21,state=='blink');a.box(25,28,3,1,INK)
 else:
  for x,y,w,h in [(6,15,13,16),(29,9,13,19),(13,22,24,18)]:octa(a,x,y,w,h,INK);octa(a,x+2,y+2,w-4,h-4,GREEN)
  a.box(9,18,2,8,LEAF);a.box(32,12,2,10,LEAF);a.box(17,26,3,10,LEAF);a.box(30,28,3,8,DARKGREEN)
  for x,y in [(5,20),(12,14),(36,8),(42,17),(13,34),(36,34)]:a.line([(x,y),(x+2,y-2)],CREAM)
  a.box(23,19,3,5,CORAL);a.box(20,21,9,2,CORAL);a.box(24,21,2,2,GOLD)
  eye(a,25,28,state=='blink');a.box(25,35,4,1,INK)
 if state=='thorns':
  for x,y in [(6,38),(11,9),(37,38),(42,31),(34,5)]:a.poly([(x,y-3),(x+2,y+2),(x-2,y+2)],STRAW);a.box(x,y-2,1,4,INK)
 if state=='regrow':
  for x in [10,37]:a.line([(x-2,42),(x,39),(x+2,42)],LEAF,1)
 return a
def turtle(v='a',state='idle',phase=0):
 a=Art();a.box(9,37,33,3,INK,30)
 if state=='hidden':return shell(v,phase if phase else 0)
 if v=='a':
  for x in [12,26]:octa(a,x,31,7,9,INK);a.box(x+2,33,3,5,GREEN)
  octa(a,9,21,26,15,INK);octa(a,11,23,22,11,GREEN);a.box(14,25,16,3,LEAF)
  a.box(29,18,8,12,INK);a.box(31,20,5,8,GREEN);octa(a,33,12,12,13,INK);octa(a,35,14,8,9,LEAF)
  eye(a,40,16,state=='blink');a.box(40,22,4,1,INK);a.poly([(9,27),(3,31),(9,32)],GREEN)
 else:
  for x,y in [(5,29),(27,31),(8,16),(28,18)]:a.poly([(x,y),(x+12,y+1),(x+9,y+6),(x,y+5)],INK);a.box(x+2,y+2,6,2,GREEN)
  octa(a,10,17,25,20,INK);octa(a,12,19,21,16,GREEN);a.box(15,21,15,3,LEAF);a.box(14,32,16,2,DARKGREEN)
  octa(a,32,21,13,11,INK);octa(a,34,23,9,7,LEAF);eye(a,39,23,state=='blink');a.box(40,29,4,1,INK)
  a.poly([(11,24),(4,25),(9,29)],LEAF)
 return a
def shell(v='a',phase=0):
 a=Art()
 if v=='a':
  octa(a,7,12,34,27,INK);octa(a,9,14,30,23,DARKGREEN);octa(a,11,15,26,18,GREEN)
  a.poly([(24,15),(32,21),(30,30),(19,31),(14,22)],LEAF)
  for x,y in [(11,18),(34,18),(12,31),(35,31)]:a.line([(24,23),(x,y)],DARKGREEN,1)
  a.box(10,34,28,2,METAL)
 else:
  a.poly([(12,16),(34,16),(43,24),(39,36),(10,36),(5,25)],INK)
  a.poly([(13,18),(33,18),(40,25),(37,33),(12,33),(8,25)],GREEN)
  a.poly([(18,20),(29,20),(34,25),(30,31),(17,31),(13,25)],DARKGREEN)
  a.poly([(20,22),(27,22),(30,25),(27,29),(20,29),(17,25)],LEAF)
  for x in [10,33]:a.box(x,24,4,4,STRAW)
  a.box(11,34,26,1,METAL)
 if phase:
  for j in range(4):
   t=j*math.pi/2+phase*.65;x=int(24+math.cos(t)*12);y=int(25+math.sin(t)*9);a.box(x,y,3,2,GOLD)
 return a
def crab(v='a',state='idle',phase=0):
 a=Art();a.box(7,39,34,2,INK,30)
 for side in [-1,1]:
  for i in range(3):
   x=24+side*13;y=29+i*3;a.line([(x,y),(x+side*7,y+3),(x+side*9,y+1)],INK,2);a.line([(x,y-1),(x+side*7,y+2)],CORAL)
 if v=='a':
  octa(a,10,23,28,15,INK);octa(a,12,25,24,11,CORAL);a.box(14,26,19,3,'#F7AA88');a.box(15,34,18,2,'#C76860')
  for x in [16,29]:a.box(x,15,2,11,INK);a.box(x-1,15,5,5,CREAM);a.box(x+1,16,2,1 if state=='blink' else 3,INK)
  for x in [3,34]:
   a.poly([(x,11),(x+4,11),(x+4,19),(x+7,19),(x+7,11),(x+11,11),(x+11,23),(x+8,26),(x+3,26),(x,23)],INK)
   a.poly([(x+2,13),(x+3,13),(x+3,21),(x+8,21),(x+8,13),(x+9,13),(x+9,22),(x+7,24),(x+4,24),(x+2,22)],CORAL)
   a.box(x+1,12,3,4,METAL);a.box(x+7,12,3,4,METAL)
 else:
  octa(a,15,14,19,25,INK);octa(a,17,16,15,21,CORAL);a.box(19,18,11,3,'#F7AA88');a.box(19,34,11,2,'#C76860')
  a.box(14,12,22,5,INK);a.box(16,13,18,3,METAL)
  for x in [17,21,25,29]:a.box(x,6,2,10,INK);a.box(x,7,1,7,STRAW)
  a.box(14,5,21,3,INK);a.box(16,6,17,1,CORAL)
  for x in [7,34]:octa(a,x,22,9,10,INK);octa(a,x+1,24,7,6,CORAL);a.box(x+3,22,2,4,CREAM)
  for x in [20,28]:a.box(x,23,3,4,CREAM);a.box(x+1,24,2,1 if state=='blink' else 3,INK)
 if state=='ready':star(a,24,11 if v=='a' else 3,CYAN)
 return a
def nail(moving=False):
 a=Art();c=GOLD if moving else METAL
 a.poly([(16,13),(21,10),(29,18),(27,22),(20,16),(15,21),(12,18)],INK)
 a.poly([(17,14),(21,12),(27,18),(26,20),(20,15),(15,19),(14,18)],c)
 a.poly([(23,20),(27,22),(15,38),(12,39),(13,35)],INK);a.poly([(24,22),(25,23),(14,37),(14,35)],c)
 return a
def crow(v='a',state='idle',phase=0):
 a=Art();a.box(11,39,27,2,INK,30)
 for x in [19,30]:a.box(x,34,2,6,INK);a.box(x-2,39,6,1,GOLD)
 if v=='a':
  a.poly([(19,11),(29,9),(36,13),(36,23),(31,26),(31,36),(16,36),(12,29),(14,19)],INK)
  a.poly([(21,13),(28,11),(33,14),(33,22),(29,25),(29,33),(18,34),(15,28),(17,20)],PURPLE)
  a.poly([(18,20),(8,18),(6,22),(11,33),(20,30),(24,24)],'#5B587D')
  a.line([(11,22),(16,27),(14,30)],METAL)
  a.poly([(34,16),(45,20),(34,24)],INK);a.poly([(35,18),(42,20),(35,22)],GOLD)
  eye(a,29,15,state=='blink');a.box(24,29,3,3,'#D8C8DC')
 else:
  octa(a,12,14,26,24,INK);octa(a,14,16,22,20,PURPLE)
  a.poly([(13,21),(5,27),(9,36),(21,31),(24,22)],'#5B587D');a.poly([(30,22),(41,27),(39,35),(27,31)],'#5B587D')
  for x,y in [(9,29),(12,32),(34,30)]:a.line([(x,y),(x+3,y+1)],METAL)
  a.poly([(31,15),(42,18),(41,22),(32,25)],INK);a.poly([(33,17),(39,19),(33,22)],GOLD)
  a.box(19,10,4,6,INK);a.box(24,11,4,5,INK);eye(a,28,16,state=='blink');a.box(20,32,9,2,'#D8C8DC')
 if state=='feather':
  a.poly([(20,5),(27,2),(29,4),(24,11),(21,11)],CREAM);a.line([(22,12),(26,5)],INK)
 return a
def dummy(v='a',damaged=False):
 a=Art();a.box(22,23,3,19,INK);a.box(10,23,28,3,INK);a.box(12,24,24,1,WOOD)
 if v=='a':
  octa(a,17,13,14,13,INK);octa(a,19,15,10,9,STRAW);a.box(14,11,20,4,INK);a.box(19,7,10,5,STRAW)
  a.poly([(18,27),(29,27),(31,34),(16,34)],CORAL);a.box(20,19,2,2,INK);a.box(26,19,2,2,INK)
 else:
  octa(a,15,13,18,13,INK);octa(a,17,15,14,9,STRAW);a.box(19,9,12,4,INK);a.box(16,12,21,3,INK)
  a.poly([(16,26),(31,26),(33,35),(14,35)],METAL);a.box(18,28,5,4,CORAL);a.box(26,29,4,4,PURPLE)
  a.line([(20,18),(23,21),(20,21)],INK);a.box(28,18,2,2,INK)
 for x,y in [(9,22),(36,22),(17,34),(29,35)]:a.line([(x,y),(x-2,y+3)],STRAW)
 if damaged:a.line([(27,14),(23,19),(27,24),(23,29)],INK,2)
 return a
def feather():
 a=Art();a.poly([(16,35),(15,25),(22,14),(31,9),(35,12),(32,22),(24,31)],INK);a.poly([(18,31),(18,25),(24,16),(31,12),(32,14),(29,22),(23,28)],CREAM);a.line([(15,38),(29,17)],METAL,1);return a
def font(size):return ImageFont.truetype(FONT,size,index=2)
def text(im,xy,s,size=16,c=INK):ImageDraw.Draw(im).text(xy,s,font=font(size),fill=rgba(c))
def place(im,art,x,y,scale=2):
 p=art.image();p=p.resize((96*scale,96*scale),Image.Resampling.NEAREST);im.alpha_composite(p,(int(x),int(y)))
def scene():
 im=Image.new('RGBA',(384,256),rgba(CREAM));d=ImageDraw.Draw(im)
 d.rectangle((12,42,371,231),fill=rgba('#F1E5C9'),outline=rgba('#D2B58A'),width=2)
 for x in range(20,372,32):d.line((x,44,x,230),fill=rgba('#EBDFC2'))
 d.line((14,211,369,211),fill=rgba('#DFCEAD'),width=2);return im
def candidate_preview(a,title,id='',v='a'):
 im=Image.new('RGBA',(384,420),rgba(CREAM))
 if id=='shell_turtle':
  place(im,a,12,106,2);place(im,shell(v),196,106,2)
  text(im,(38,70),'裸身本体',17);text(im,(230,70),'独立空壳',17)
  text(im,(30,289),'并列展示，不是一直穿壳',16,MUTED)
  title=title.split('＋')[0]
 else:place(im,a,48,40,3)
 text(im,(20,332),title,21);text(im,(20,384),'R03 候选 · 非游戏实录',13,MUTED);return im
def state_preview(id,v,kind,title):
 im=scene();draw={'cactus':cactus,'shell_turtle':turtle,'magnet_crab':crab,'crow':crow}[id]
 if id=='crow' and kind=='repair':
  place(im,crow(v,'idle'),132,90,1);place(im,dummy(v,False),172,90,1)
  text(im,(22,190),'碰到受伤的自家草人后，消耗羽毛补25HP',13)
 else:
  place(im,draw(v,kind),80,44,2)
  if id=='shell_turtle' and kind!='hidden':
   place(im,shell(v),246,120,1);text(im,(110,185),'裸身本体',12);text(im,(266,185),'独立壳',12)
  if id=='crow':place(im,dummy(v,True),252,119,1)
 if id=='magnet_crab' and kind in ['idle','moving']:
  place(im,nail(kind=='moving'),256,124,1)
  if kind=='moving':ImageDraw.Draw(im).line([(263,174),(253,180)],fill=rgba(GOLD),width=3)
 text(im,(18,10),title,18);text(im,(18,235),'状态示意，不是实际战斗时序',12,MUTED);return im
def ring_draw(d,x,y,r,c,width=2):
 p=[(x-r//2,y-r),(x+r//2,y-r),(x+r,y-r//2),(x+r,y+r//2),(x+r//2,y+r),(x-r//2,y+r),(x-r,y+r//2),(x-r,y-r//2),(x-r//2,y-r)];d.line(p,fill=rgba(c),width=width)
def squash_art(art,amount):
 # New vector pose deformation around the same foot baseline; never a position/physics change.
 result=Art();factor=1-amount
 def yy(y):return round(40+(y-40)*factor)
 for typ,g,c,a,*extra in art.ops:
  if typ=='r':
   x,y,w,h=g;result.box(x,yy(y),w,max(1,yy(y+h)-yy(y)),c,a)
  elif typ=='p':result.poly([(x,yy(y)) for x,y in g],c,a)
  else:result.line([(x,yy(y)) for x,y in g],c,extra[0],a)
 return result
def hurt_frame(id,style,i):
 im=scene();draw={'cactus':cactus,'shell_turtle':turtle,'magnet_crab':crab,'crow':crow}[id]
 strength=[0,.08,.12,.12,.07,.03,0,0][i] if style==0 else 0
 pose=draw('a','blink' if style==0 and i in [1,2,3] else 'idle')
 place(im,squash_art(pose,strength),98,49,2)
 d=ImageDraw.Draw(im)
 if style==1 and 1<=i<=5:
  for j in range(6):
   ang=j*math.pi/3;radius=28+i*5;x=int(194+math.cos(ang)*radius);y=int(150+math.sin(ang)*radius*.65)
   d.line([(x,y),(x+int(math.cos(ang)*5),y+int(math.sin(ang)*5))],fill=rgba(CORAL if j%2 else GOLD),width=3)
 text(im,(18,10),['受击A：局部压低／眨眼','受击B：局部碎光'][style],17)
 note='仅裸身真实受伤；hidden与独立壳不播受伤' if id=='shell_turtle' else '只有真实掉血才触发；不新增击退、无敌或停顿'
 text(im,(18,211),note,11);text(im,(18,235),'同一位置的候选表现，无声概念，非游戏实录',11,MUTED)
 return im
def motion_frame(id,style,i):
 im=scene();d=ImageDraw.Draw(im);a='a';step=i/11
 title=['局部符号反馈','短轨迹／碎光反馈'][style]
 if id=='cactus':
  place(im,cactus(a,'idle'),114,56,2)
  pts=[(76,188),(112,208),(278,201),(308,166),(272,100)]
  for j,(x,y) in enumerate(pts):
   d.polygon([(x,y-9),(x+6,y+5),(x-6,y+5)],fill=rgba(STRAW),outline=rgba(INK))
   if style==0:ring_draw(d,x,y+2,10+((i+j)%4)*2,LEAF,2)
   elif i%4<2:d.line([(x-9,y-11),(x-3,y-4)],fill=rgba(CORAL),width=3)
  text(im,(18,211),'本体不走路；刺原地出现，REGROW不是回血',11)
 elif id=='shell_turtle':
  place(im,turtle(a),24,89,1);place(im,shell(a,i),160,56,2)
  if style==0:ring_draw(d,256,171,32+(i%4)*2,CYAN,3)
  else:
   for j in range(4):
    ang=j*math.pi/2+i*.55;x=int(255+math.cos(ang)*45);y=int(169+math.sin(ang)*32);d.line([(x,y),(x+int(math.sin(ang)*10),y-int(math.cos(ang)*8))],fill=rgba(GOLD),width=4)
  text(im,(18,211),'独立壳原地旋转；不是高速冲刺',12)
 elif id=='magnet_crab':
  place(im,crab(a,'ready' if i<7 else 'idle'),116,65,2)
  # Concept mode timeline. Grey resting nail never gets danger feedback.
  moving=2<=i<=9
  xs=[110,110,190,270,340,300,252,212,260,310,310,310]
  ys=[190,190,190,190,190,190,190,190,166,145,145,145]
  x=xs[i];y=ys[i]
  small=nail(moving).image().resize((48,48),Image.Resampling.NEAREST);im.alpha_composite(small,(x-24,y-24))
  if moving:
   if style==0:ring_draw(d,x,y,14,CYAN,2)
   else:
    dx=x-xs[max(0,i-1)];dy=y-ys[max(0,i-1)];norm=max(1,math.hypot(dx,dy))
    for j in range(3):
     tail=12+j*7;tx=x-dx/norm*tail;ty=y-dy/norm*tail
     d.line([(tx,ty),(tx-dx/norm*5,ty-dy/norm*5)],fill=rgba(GOLD),width=2)
  d.line((344,76,344,204),fill=rgba(CORAL if moving else '#D2B58A'),width=4)
  text(im,(18,211),'静钉无害；移动钉才有暖色反馈',12)
 elif id=='crow':
  # Teleport on the midpoint. There is no travel or projectile between endpoints.
  left,right=(30,235) if i<6 else (235,30)
  place(im,crow(a,'feather'),left,91,1);place(im,dummy(a,True),right,91,1)
  if style==0:
   for x in [left+48,right+48]:ring_draw(d,x,183,18+(i%4)*3,PURPLE,2)
  else:
   for x in [left+48,right+48]:
    for j in range(3):
     length=3+(i%3)*3
     d.line([(x-12+j*8,171-j*8),(x-12+j*8+length,171-j*8-length)],fill=rgba(CREAM if j%2 else PURPLE),width=3)
  text(im,(18,211),'只换位置不消耗储羽；未画远程修复或飞羽攻击',10)
 text(im,(18,10),title,17);text(im,(18,235),'概念编排 · 无声 · 不代表实际游戏时序',11,MUTED)
 return im

META={
'cactus':{'name':'仙人掌','titles':['A 高柱花冠','B 圆掌丛簇'],'desc':['高柱主干配不对称双臂与小花，扎根轮廓清楚。','宽低圆掌与两片侧掌形成簇状轮廓，不画行走腿。'],'pros':[['静止身份直观','高柱与刺点容易区分'],['横向轮廓稳定','小尺寸下分枝更醒目']],'cons':[['高柱需检查HUD遮挡'],['低身容易与场上刺混淆，需清楚描边']],'recommend':'推荐A：高柱双臂能更快读成固定本体，仍待用户选择。','questions':['选择高柱花冠还是圆掌丛簇？','散刺反馈选局部根部符号还是短碎光？两者都不表示移动或回血。'],'states':[('idle','固定本体'),('thorns','附近散刺'),('regrow','换位提示，不回血')],'objects':[('thorn','独立刺点','静止刺点在现有逻辑位置生成；不是手持武器，命中后移除。')],'information':['本体静止、敌方碰撞受伤18','附近散5刺；刺命中伤12后消失','REGROW仅瞬移换位，不回血'],'missing':['未制作可直接接入的完整角色动作与游戏事件接口','候选外形与动效尚未由用户选择']},
'shell_turtle':{'name':'脱壳龟','titles':['A 长颈短足＋圆拱壳','B 低身宽足＋六角矮壳'],'desc':['轻长颈和四短足，独立圆壳另画，突出龟与壳是两物体。','宽低躯体与侧展足，搭配矮六角壳；不是一直穿背甲。'],'pros':[['脱壳后的身体易读','圆拱壳旋转形态直接'],['身体与壳轮廓差异大','矮壳不遮挡附近角色']],'cons':[['本体小尺寸需保留头部对比'],['六角外观不能被误认六边形碰撞']],'recommend':'推荐A：身体和独立圆壳关系较直观，仍待用户选择。','questions':['选择长颈短足与圆拱壳，还是低身宽足与六角矮壳？','旋壳用局部环形符号还是短边缘轨迹？都不增加冲刺。'],'states':[('idle','本体与壳分离'),('hidden','入壳后本体不可见'),('seek','寻壳状态概念')],'objects':[('shell','独立龟壳','不可受伤的独立物体；spin开始速度置0，并非新增冲刺。')],'information':['本体未隐藏撞敌时自己扣12','寻壳接触后隐藏2.5秒；无合法位置可继续等待','独立壳碰撞伤18，旋转时27，原有冲量不改'],'missing':['完整寻壳/出壳连续动画待用户选型后制作','隐藏/出壳与真实物理同步未验证']},
'magnet_crab':{'name':'磁铁蟹','titles':['A 横向马蹄钳','B 高背线圈蟹'],'desc':['横宽蟹身与马蹄形钳端，磁铁主题集中在双钳轮廓。','较高背部线圈与普通小钳，身体纵向识别明显；线圈是候选装饰，不增加技能。'],'pros':[['磁铁主题一眼可读','宽低身体适合贴地铁钉'],['与其他圆身角色区分大','钳和磁力主题分层清楚']],'cons':[['大钳不能暗示新增近战范围'],['背部装置较多，小尺寸需降细节']],'recommend':'推荐A：马蹄轮廓比线圈更直接传达磁铁主题；仍待选择。','questions':['选择马蹄钳还是高背线圈造型？','移动钉用局部状态环还是短暖色轨迹？静止钉始终不显示伤害反馈。'],'states':[('idle','铁钉静止无害'),('ready','下一枚回钉弹飞准备'),('moving','移动钉才可伤敌')],'objects':[('nail_rest','静止铁钉','rest为无害静止物，不能画成危险地刺。'),('nail_moving','移动铁钉','wall/return/out时只有实际移动才伤16，单钉命中间隔0.3秒。')],'information':['每1秒落钉；静钉无踩踏伤害','随机磁化一墙，铁钉到墙后回身','准备态弹下一枚回钉，向敌当时位置外飞0.8秒后停'],'missing':['磁墙/回收/弹飞完整事件绑定未实现','候选装置不代表可独立导入或扩大伤害范围']},
'crow':{'name':'乌鸦','titles':['A 瘦长折翼侧影','B 宽身披翼轮廓'],'desc':['瘦长身体、折叠单翼和长金喙，稻草人采用简洁草帽T架。','宽身与双侧披翼、短粗金喙，搭配拼布草人；只改外形，不增护甲或法术。'],'pros':[['乌鸦与稻草人对照清楚','储羽标记不易和武器混淆'],['大轮廓更适合小尺寸','拼布草人易显示受损/修复']],'cons':[['单翼侧影需检查左右翻转'],['披翼需避免看成护盾/无敌状态']],'recommend':'推荐A：瘦长侧影与木草人关系更清楚，仍待用户选择。','questions':['选择瘦长折翼还是宽身披翼？','换位用两端局部环，还是不连线的短羽光？羽毛不得成为远程攻击。'],'states':[('idle','本体与受伤稻草人'),('feather','储羽准备'),('repair','近身修复概念')],'objects':[('dummy','独立稻草人','最多2个，固定60HP，承伤实际值反到敌方英雄，不主动攻击。'),('dummy_damaged','受伤稻草人','存活且受伤时才能由乌鸦碰触消耗羽毛补25HP。'),('feather','储存羽毛','状态道具；不是羽毛弹、法杖或远程伤害技能。')],'information':['稻草人最多2个，固定站位','与首个稻草人换位置须两边合法','带羽碰自己受伤稻草人补25HP，消耗羽毛'],'missing':['完整换位/受损/修复游戏动画尚未接入','新稻草人外形和储羽图标仍待用户选择']}}

def object_art(id,key,v='a'):
 if key=='thorn':
  a=Art();a.poly([(22,12),(31,35),(17,35)],INK);a.poly([(23,17),(28,32),(20,32)],STRAW);a.box(23,22,2,10,CREAM);return a
 if key=='shell':return shell(v)
 if key=='nail_rest':return nail(False)
 if key=='nail_moving':return nail(True)
 if key=='dummy':return dummy(v,False)
 if key=='dummy_damaged':return dummy(v,True)
 if key=='feather':return feather()

DETAIL_DESCRIPTIONS={
 'cactus':[
  '高柱主干、不对称双臂和小花冠形成竖向轮廓；柔绿蜡皮、奶黄色刺与珊瑚花配深蓝灰描边。单眼平口偏沉着，候选气质稳重扎根，不增加背景设定或行走能力。',
  '宽低圆掌配两片高低侧掌，轮廓更像丛簇；浅绿蜡质高光、深绿边面和珊瑚小花保持A暖色。小黑眼和平口偏呆萌钝感，气质只是视觉意向，不代表新机制。'],
 'shell_turtle':[
  '裸身为长颈短足、侧向小眼和平口，和独立圆拱壳并列展示；柔绿皮肤、浅绿高光与分片硬甲形成材质对照。意向是谨慎轻巧，壳不是一直穿在背上，气质不是已定故事设定。',
  '低身宽足与短颈粗头搭配独立六角矮壳；柔绿皮肤、深绿甲片和浅金角片均是候选外观。直视黑眼与厚实轮廓偏稳健憨实，六角外观不改变圆形碰撞或壳规则。'],
 'magnet_crab':[
  '横宽珊瑚蟹身、双眼柄与马蹄形大钳，金属浅青钳端和壳面亮条区分玩具金属与光滑甲壳。小黑眼显机灵忙碌，这是候选气质；大钳不增加近战伤害或射程。',
  '高背线圈、较窄竖身和普通小钳形成另一种轮廓；珊瑚壳、浅金线圈和浅青横梁表达工具材质。前置双眼更专注朴拙，背部装置只作候选造型，不新增装甲或技能。'],
 'crow':[
  '瘦长侧身、折翼和长金喙，淡紫身体配深紫哑光羽片、浅青羽缘与浅腹部。单侧黑眼和收拢姿态偏谨慎沉着；这是候选视觉气质，不编造角色身世或飞羽攻击。',
  '宽身、两侧披翼和短粗金喙，深紫羽片包住淡紫胸腹，额顶小羽角强化体块；直视小黑眼更显机敏倔强。披翼只表达蓬松羽质与轮廓，不能被当成护盾或无敌状态。']}

def build():
 draw={'cactus':cactus,'shell_turtle':turtle,'magnet_crab':crab,'crow':crow}
 for id,m in META.items():
  folder=ROOT/'characters'/id;folder.mkdir(parents=True,exist_ok=True);variants=[]
  facts=ROOT/'facts'/(id+'.md');assert facts.is_file(),f'Missing required facts: {facts}'
  facts_text=facts.read_text();assert len(facts_text)>100
  for j,v in enumerate(['a','b']):
   a=draw[id](v);a.save(folder,'variant_'+v+'_sprite');candidate_preview(a,m['titles'][j],id,v).save(folder/('variant_'+v+'.png'))
   variants.append({'id':v,'title':m['titles'][j],'image':'variant_'+v+'.png','source_image':'variant_'+v+'_sprite.png','source_svg':'variant_'+v+'_sprite.svg','description':DETAIL_DESCRIPTIONS[id][j],'pros':m['pros'][j],'cons':m['cons'][j]})
  board=Image.new('RGBA',(768,530),rgba(CREAM))
  for j,v in enumerate(['a','b']):board.alpha_composite(Image.open(folder/('variant_'+v+'.png')),(j*384,34))
  text(board,(18,8),m['name']+' · 两个候选方向',21);text(board,(18,482),'A像素风已定；具体候选待选择。概念，不是实机。',17);board.save(folder/'comparison.png')
  states=[]
  for kind,title in m['states']:
   im=state_preview(id,'a',kind,title);name='state_'+kind+'.png';im.save(folder/name)
   states.append({'id':kind,'title':title,'image':name,'description':'按现有代码语义绘制的候选状态示意；未接入游戏。','event':kind})
  motion=[]
  for style in [0,1]:
   ims=[motion_frame(id,style,i) for i in range(12)];name=f'motion_{style+1}.gif'
   ims[0].save(folder/name,save_all=True,append_images=ims[1:],duration=120,loop=0,disposal=2)
   ims[0].save(folder/f'motion_{style+1}_cover.png')
   with Image.open(folder/name) as encoded:
    encoded_frames=encoded.n_frames;total_ms=0
    for fi in range(encoded_frames):encoded.seek(fi);total_ms+=encoded.info.get('duration',0)
   motion.append({'id':f'motion_{style+1}','title':['方向1：局部符号反馈','方向2：短轨迹／碎光反馈'][style],'image':f'motion_{style+1}_cover.png','animation':name,'logical_frames':12,'gif_encoded_frames':encoded_frames,'loop_duration_ms':total_ms,'description':f'本轮新制无声概念编排；12逻辑帧×120ms循环，GIF合并重复画面后{encoded_frames}编码帧。仅比较反馈语法，不是技能时间或游戏录像。'})
   states.append({'id':f'motion_{style+1}','title':motion[-1]['title'],'image':f'motion_{style+1}_cover.png','animation':name,'description':motion[-1]['description'],'event':'concept_only'})
  for style in [0,1]:
   ims=[hurt_frame(id,style,i) for i in range(8)];name=f'hurt_{style+1}.gif'
   ims[0].save(folder/name,save_all=True,append_images=ims[1:],duration=80,loop=0,disposal=2);ims[2].save(folder/f'hurt_{style+1}_cover.png')
   with Image.open(folder/name) as encoded:
    encoded_frames=encoded.n_frames;total_ms=0
    for fi in range(encoded_frames):encoded.seek(fi);total_ms+=encoded.info.get('duration',0)
   record={'id':f'hurt_{style+1}','title':['受击A：局部压低／眨眼','受击B：局部碎光'][style],'image':f'hurt_{style+1}_cover.png','animation':name,'logical_frames':8,'gif_encoded_frames':encoded_frames,'loop_duration_ms':total_ms,'description':'统一用A候选示意的纯表现对比；只有真实掉血才触发，不增加击退/无敌/hitstop，循环仅供评审。'+('龟壳不可受伤，hidden不播受伤。' if id=='shell_turtle' else '')}
   motion.append(record);states.append({**record,'event':'actual_health_loss_only'})
  mobility={'cactus':'本体固定原位、不走路；REGROW仅合法位置瞬移，不回血。','shell_turtle':'裸身可移动/寻壳；hidden不可见并跟壳；旋壳视觉是原地转，不增冲刺。','magnet_crab':'蟹按原运动滑行；铁钉区分静止、向墙、回身、弹出，不另加近战钳攻击。','crow':'本体按原运动；换位是合法条件下瞬换，不画飞行法术或远程羽攻击。'}[id]
  states.append({'id':'mobility','title':'移动／站桩方向','image':'state_idle.png','description':mobility,'event':'existing_position_and_velocity'})
  objs=[]
  for key,title,desc in m['objects']:
   a=object_art(id,key);a.save(folder,'object_'+key);objs.append({'id':key,'name':title,'image':'object_'+key+'.png','source_svg':'object_'+key+'.svg','description':desc})
  if id in ['shell_turtle','crow']:
   key='shell' if id=='shell_turtle' else 'dummy';a=object_art(id,key,'b');a.save(folder,'object_'+key+'_b');objs.append({'id':key+'_b','name':'B方向配套'+('独立壳' if key=='shell' else '稻草人'),'image':'object_'+key+'_b.png','source_svg':'object_'+key+'_b.svg','description':'B候选的物件轮廓，不改变实际物体规则。'})
  data={'id':id,'name':m['name'],'status':'R03 review candidates; none selected; not integration assets','variants':variants,'recommendation':m['recommend'],'questions':m['questions'],'states':states,'motion':motion,'weapons_objects':objs,'information':m['information'],'validation':['已根据独立代码事实稿核对角色/物件语义','本轮原创程序几何绘图，RGBA/SVG新源，无截图或视频抽帧输入','PNG/GIF文件可读性由交付前检查；未完成Godot接入、真机、触控或人工听审'],'missing':m['missing'],'source_facts':'../../facts/'+id+'.md','setting_document':'SETTING.md','source_facts_sha256':hashlib.sha256(facts.read_bytes()).hexdigest(),'source_code':'../../sources/build_last_four_review.py','technical':{'native_size':[96,96],'logical_grid':[48,48],'sampling':'nearest','format':'RGBA PNG and editable SVG; review GIF','orientation':'candidate facing right; mirroring not game-validated','anchor_note':'Review poses only, no approved gameplay anchor/hitbox','scope':'Review webpage only; no integration package/game changes'},'provenance':{'new_original_creation':True,'external_image_inputs':False,'font':'system Noto Sans CJK SC (OFL1.1), rendered preview text only; font binary not redistributed','license_note':'Original task graphics for project review, not claim of exclusivity'}}
  data['review_scope_note']='为控制变量，状态与动效统一采用A候选示意；不代表A已选。B完整动作、实际移动动画及游戏事件绑定尚未制作/验证。'
  data['questions'].append('受击表现选择局部压低/眨眼还是局部碎光？两者都不新增击退、无敌或停顿。')
  data['recommendation']+=' 重点动效建议局部符号反馈，受击建议局部碎光以少改轮廓；均只是评审推荐，不代表已选。'
  data['missing'].append('B候选完整动作与移动连续帧未制作；当前仅关键状态/反馈语法评审，不称全套动画完成。')
  (folder/'review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
  print(id,'written')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);args=p.parse_args();ROOT=args.root.resolve();build()
