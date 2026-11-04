from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import json,hashlib,datetime
BASE='http://127.0.0.1:8033/';OUT=Path('/workspace/shared/R05-ui-review/qa');DOCS=Path('/workspace/ball_art_review/docs')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True);ctx=b.new_context(viewport={'width':1280,'height':900},permissions=['clipboard-read','clipboard-write']);page=ctx.new_page();errors=[];bad=[];mut=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append([r.url,r.status])if r.status>=400 else None);page.on('request',lambda r:mut.append([r.url,r.method])if r.method not in ['GET','HEAD']else None)
 page.goto(BASE,wait_until='networkidle');page.wait_for_function("document.documentElement.dataset.reviewReady==='true'");data=page.request.get(BASE+'r05/review-data.json').json();assert len(data['pages'])==4 and all(len(x['schemes'])==4 for x in data['pages']);assert page.locator('[role=tab]').count()==16;assert page.locator('select[data-choice]').evaluate_all('(a)=>a.every(x=>x.value==="")')
 media=[];schemes=[];targets=set()
 for pg in data['pages']:
  sec=page.locator('#'+pg['id']);tabs=sec.locator('[role=tab]')
  for s in pg['schemes']:
   sec.locator('[data-scheme="'+s['id']+'"]').click();assert sec.locator('[aria-selected=true]').count()==1;assert sec.locator('[role=tabpanel]>.substates button').count()==len(s.get('detail_images',[]))+1
   for mb in sec.locator('.substates button').all():
    mb.click();im=sec.locator('[role=tabpanel] .viewer img');page.wait_for_function('(e)=>e.complete&&e.naturalWidth>0',arg=im.element_handle());size=im.evaluate('(e)=>[e.naturalWidth,e.naturalHeight]');assert size in [[1600,900],[844,390]],(pg['id'],s['id'],size);rect=im.bounding_box();assert abs(rect['width']/rect['height']-size[0]/size[1])<0.005,(size,rect);src=im.get_attribute('src');targets.add(BASE+src);media.append({'page':pg['id'],'scheme':s['id'],'url':src,'natural_size':size,'display_aspect_correct':True})
   # Browsing never silently chooses a candidate.
   assert page.locator('#choice-'+pg['id']).input_value()==''
   sec.locator('.actions button').click();assert page.locator('#choice-'+pg['id']).input_value()==s['id'];schemes.append([pg['id'],s['id']])
   # Reset via explicit feedback choice for independence checks below.
   page.locator('#choice-'+pg['id']).select_option('')
  tabs.first.click();tabs.first.press('End');assert tabs.last.get_attribute('aria-selected')=='true';tabs.last.press('ArrowRight');assert tabs.first.get_attribute('aria-selected')=='true';tabs.first.press('Home');assert tabs.first.get_attribute('aria-selected')=='true'
 ids=['arena','storage','hatch','story'];wanted=['a','b','c','d'];manual='人工QA临时手改段落：须完整保留，不代表用户决定。'
 page.locator('#template').fill(manual)
 for id,v in zip(ids,wanted):
  page.locator('#choice-'+id).select_option(v);page.locator('input[aria-label="'+dict(arena='竞技场',storage='仓库',hatch='孵蛋',story='主线')[id]+'补充意见"]').fill('QA '+id)
 assert page.locator('#template').input_value()==manual;page.locator('#generate').click();text=page.locator('#template').input_value();assert text.startswith(manual+'\n\n') and 'R05 UI 评审草稿' in text
 for id,v in zip(ids,wanted):assert page.locator('#choice-'+id).input_value()==v
 page.reload();page.wait_for_function("document.documentElement.dataset.reviewReady==='true'");assert page.locator('#template').input_value()==text
 for id,v in zip(ids,wanted):assert page.locator('#choice-'+id).input_value()==v
 page.locator('#copy').click();page.wait_for_function('document.querySelector("#live").textContent.includes("已复制")');assert page.evaluate('navigator.clipboard.readText()')==text
 # True original-pixel zoom on phone, not another fit-to-screen thumbnail.
 page.set_viewport_size({'width':390,'height':844});trigger=page.locator('#arena [role=tabpanel] .viewer button');trigger.click();assert page.locator('#zoom').evaluate('(e)=>e.open');page.locator('#native-zoom').click();z=page.locator('#zoom .zoom-scroll').evaluate('(e)=>({cw:e.clientWidth,ch:e.clientHeight,sw:e.scrollWidth,sh:e.scrollHeight,iw:e.querySelector("img").getBoundingClientRect().width,ih:e.querySelector("img").getBoundingClientRect().height})');assert z['iw']==1600 and z['ih']==900 and z['sw']>z['cw'] and z['sh']>z['ch'];page.locator('#zoom .zoom-scroll').evaluate('(e)=>{e.scrollLeft=400;e.scrollTop=150}');assert page.locator('#zoom .zoom-scroll').evaluate('(e)=>e.scrollLeft>0&&e.scrollTop>0');page.screenshot(path=str(OUT/'phone-native-zoom.png'));page.keyboard.press('Escape');assert not page.locator('#zoom').evaluate('(e)=>e.open');assert trigger.evaluate('(e)=>e===document.activeElement')
 widths=[]
 for w,h in [(360,844),(390,844),(768,1024),(1280,900),(844,390)]:
  page.set_viewport_size({'width':w,'height':h});page.locator('details').evaluate_all('(a)=>a.forEach(d=>d.open=true)');page.locator('img').evaluate_all('(a)=>a.forEach(i=>i.loading="eager")');page.wait_for_timeout(100);bounds=page.evaluate('({doc:document.documentElement.scrollWidth,body:document.body.scrollWidth})');assert bounds['doc']<=w and bounds['body']<=w,(w,bounds);widths.append({'width':w,'height':h,'expanded':True,**bounds});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/f'viewport-{w}x{h}.png'))
 for url in page.locator('[src],a[href],link[href]').evaluate_all('(a)=>a.map(e=>e.src||e.href).filter(Boolean)'):targets.add(url if url.startswith('http')else BASE+url)
 checked=[]
 for url in sorted(targets):
  u=urlparse(url)
  if u.netloc!='127.0.0.1:8033' or (u.fragment and u.path in ['/','/index.html']):continue
  r=page.request.get(url);assert r.ok,(url,r.status);checked.append(url)
 assert not errors,errors;assert not bad,bad;assert not mut,mut
 # Deliberately denied clipboard, separate browser context; no fake success.
 fallback=b.new_context();fallback.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('QA denied clipboard'))}})");fp=fallback.new_page();fp.goto(BASE);fp.wait_for_function("document.documentElement.dataset.reviewReady==='true'");fp.locator('#template').fill('fallback test');fp.locator('#copy').click();fp.wait_for_function('document.querySelector("#live").textContent.includes("系统复制")');assert fp.locator('#template').evaluate('(e)=>e.selectionStart===0&&e.selectionEnd===e.value.length');fallback.close()
 report={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':4,'candidates':16,'schemes_browsed_and_chosen':schemes,'media_loaded':media,'independent_choices_notes_reload':True,'manual_template_not_overwritten':True,'explicit_generate_appends':True,'clipboard_write_and_read_equal':True,'denied_clipboard_select_fallback':True,'keyboard_tabs':True,'phone_native_zoom':z,'escape_returns_focus':True,'viewports':widths,'static_targets':checked,'javascript_errors':errors,'http_errors':bad,'mutating_requests':mut,'hashes':{x:hashlib.sha256((DOCS/x).read_bytes()).hexdigest()for x in ['index.html','r05/app.js','r05/style.css','r05/review-data.json']},'real_device':'NOT_RUN','game_binding':'NOT_RUN','public_site':'NOT_RUN'}
 (OUT/'browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));b.close();print('BROWSER PASS',len(media),'media',len(checked),'targets')
