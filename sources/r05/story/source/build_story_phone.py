"""R05 C phone layout concept; does not overwrite the four desktop concepts."""
from pathlib import Path
import json,hashlib
BASE=Path(__file__).resolve().parent
exec((BASE/'build_story.py').read_text().split('def a_map():')[0])
a=Art();a.s[0]=a.s[0].replace('width="1600" height="900" viewBox="0 0 1600 900"','width="844" height="390" viewBox="0 0 844 390"')
TARGETS=[]
def button(x,y,w,h,t,on=False,tid=''):
 a.rect(x,y,w,h,TEAL if on else PAPER,INK,2)
 a.text(x+w/2-len(t)*8,y+h/2+6,t,16,'#fff8e8' if on else INK,600)
 TARGETS.append({'id':tid or t,'x':x,'y':y,'width':w,'height':h})
a.rect(0,0,844,390,'#d6e4c0');terrain(a,0,54,844,278,18)
a.path('M0 96 H95 V83 H210 V105 H362 V86 H520 V108 H693 V80 H844 V159 H0Z','#b1c99e')
a.path('M38 293 H228 V235 H338 V192 H505 V164 H543 V228 H707 V265 H807 V304 H38Z','#e9d5a4')
a.path('M401 206 V120 H454 V196','none','#e9d5a4',30)
# Same visual order as C desktop: A left, C north-center, B right.
a.house(115,121,.72);a.house(407,88,.52);a.house(647,156,.64)
for x,y,s in [(47,140,.65),(316,113,.6),(533,91,.65),(788,147,.7),(547,284,.55),(811,306,.6)]:a.tree(x,y,s)
a.sprite('electric_sheep',503,202,102);a.sprite('bubble_fish',18,180,74)
# Selected A has color plus a checked square; others retain text labels, not color-only.
button(100,200,134,44,'✓ 地点 A',True,'place_a_selected')
button(387,146,126,44,'地点 C  ›',False,'place_c')
button(620,239,134,44,'地点 B  ›',False,'place_b')
a.rect(18,264,442,60,PAPER,INK,2);a.text(32,288,'地点 A',18,INK,700);a.text(32,311,'内容待定',14,MUT)
button(338,272,108,44,'查看结构',True,'details')
a.text(161,300,'小屏布局示意 · 非实机',14,MUT)
# Fixed top and bottom controls: no canvas scaling from 1600px.
a.rect(0,0,844,54,PAPER,INK,2);button(10,5,44,44,'‹',False,'back');a.text(68,34,'主线',22,INK,700);a.text(128,33,'聚落 / 地点 A',16,MUT);a.text(579,33,'结构占位 / 玩法待定',15,'#7a6c57');button(788,5,44,44,'?',False,'help')
a.rect(0,332,844,58,PAPER,INK,2)
for i,t in enumerate(['竞技场','主线','仓库','孵蛋']):button(19+i*204,339,194,44,t,i==1,'global_'+str(i))
a.save(ROOT/'c'/'phone.svg')
p=ROOT/'c'/'review.json';j=json.loads(p.read_text());d={'image':'phone.png','title':'844×390小屏重排 · 非实机','source':'phone.svg'}
j['detail_images']=[x for x in j['detail_images'] if x.get('image')!='phone.png']+[d];j['phone_layout']={'resolution':[844,390],'not_desktop_scaled':True,'minimum_text_px':14,'minimum_touch_target_px':44,'status':'static_concept_not_device_capture','targets':TARGETS};p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
p=ROOT/'review.json';j=json.loads(p.read_text())
for opt in j['options']:
 if opt['id']=='c':
  opt['detail_images']=[x for x in opt['detail_images'] if x.get('image')!='c/phone.png']+[d|{'image':'c/phone.png','source':'c/phone.svg'}];opt['phone_layout']={'resolution':[844,390],'not_desktop_scaled':True,'minimum_text_px':14,'minimum_touch_target_px':44,'status':'static_concept_not_device_capture'}
p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
assert all(t['width']>=44 and t['height']>=44 for t in TARGETS)
(ROOT/'c'/'phone-validation.json').write_text(json.dumps({'resolution':[844,390],'touch_target_count':len(TARGETS),'all_targets_at_least_44px':True,'minimum_text_px':14,'selected_location':'A','same_map_relative_landmarks':'A left / C north-center / B right','source':'source/build_story_phone.py','no_main_images_rewritten':True,'device_validation':'NOT_RUN','game_integration':'NOT_RUN'},ensure_ascii=False,indent=2))
print('phone ready',len(TARGETS),'targets')
