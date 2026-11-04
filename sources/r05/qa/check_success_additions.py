from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import json,hashlib,datetime
R=Path('/workspace/shared/R05-ui-review');D=Path('/workspace/ball_art_review/docs');BASE='http://127.0.0.1:8033/'
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True);page=b.new_page(viewport={'width':1280,'height':900});errors=[];bad=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append([r.url,r.status])if r.status>=400 else None);page.goto(BASE,wait_until='networkidle');page.wait_for_function("document.documentElement.dataset.reviewReady==='true'");data=page.request.get(BASE+'r05/review-data.json').json();media_total=sum(1+len(s.get('detail_images',[]))for pg in data['pages']for s in pg['schemes']);assert media_total==58,media_total;h=next(pg for pg in data['pages']if pg['id']=='hatch');records=[];sec=page.locator('#hatch')
 for s in h['schemes']:
  sec.locator('[data-scheme="'+s['id']+'"]').click();details=s['detail_images'];indexes=[i+1 for i,m in enumerate(details)if m['image'].endswith('/success.png')];assert len(indexes)==1,(s['id'],details);sec.locator('.substates button').nth(indexes[0]).click();im=sec.locator('[role=tabpanel] .viewer img');page.wait_for_function('(e)=>e.complete&&e.naturalWidth===1600&&e.naturalHeight===900',arg=im.element_handle());src=im.get_attribute('src');assert src.endswith('/success.png');res=page.request.get(BASE+src);assert res.ok;local=D/src;assert hashlib.sha256(res.body()).hexdigest()==hashlib.sha256(local.read_bytes()).hexdigest();records.append({'scheme':s['id'],'url':src,'status':res.status,'size':[1600,900],'sha256':hashlib.sha256(res.body()).hexdigest()})
 # Revisit all currently visible links, plus previously visited base media targets.
 old=json.load(open(R/'qa/browser-checks.json'));urls=set(old['static_targets'])|{BASE+x['url']for x in records};checked=[]
 for url in sorted(urls):
  res=page.request.get(url);assert res.ok,(url,res.status);checked.append(url)
 for w,h in [(390,844),(844,390)]:
  page.set_viewport_size({'width':w,'height':h});assert page.evaluate('document.documentElement.scrollWidth')<=w
 assert not errors and not bad,(errors,bad)
 oldhash=old['hashes'];current={x:hashlib.sha256((D/x).read_bytes()).hexdigest()for x in oldhash};assert all(current[k]==oldhash[k]for k in oldhash if k!='r05/review-data.json'),current
 out={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Targeted new-media verification after completed54-media full browser suite; unchanged frontend code verified by hashes. Existing interaction tests not rerun.','new_success_images':records,'final_total_media':58,'current_static_targets_rechecked':checked,'final_hashes':current,'javascript_errors':errors,'http_errors':bad,'real_device':'NOT_RUN','game_binding':'NOT_RUN'};(R/'qa/browser-additions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));b.close();print('ADDITIONS PASS4; total58; targets',len(checked))
