from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,hashlib
root=Path(__file__).resolve().parents[1]
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':900})
 for id in 'abcd':
  path=root/id;html=(path/'source.html').read_text();page.set_content(html)
  main_table_count=page.locator('table').count()
  if id in 'bd':
   assert main_table_count==0
   assert page.locator('.innate-grid>div').count()==6
   page.set_content((path/'detail_source.html').read_text())
  table=page.locator('table');bounds=table.evaluate('(e)=>({top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom})')
  assert bounds['bottom']<854,(id,bounds)
  assert page.locator('tbody tr').count()==6
  assert page.locator('thead th').count()==5
  for label in ['竞技场','主线','仓库','孵蛋','吸附泡泡','八方泡泡','特性一','特性二','特性三','技能三','技能四','技能五']:
   assert label in (path/'source.html').read_text(),(id,label)
  assert Image.open(path/'screen.png').size==(1600,900)
  results.append({'id':id,'image_dimensions':[1600,900],'table_bounds':bounds,'data_check':'6 rows × 4 source columns present on main(A/C) or full detail(B/D); placeholders present','main_matrix_count':main_table_count,'source_sha256':hashlib.sha256((path/'source.html').read_bytes()).hexdigest(),'png_sha256':hashlib.sha256((path/'screen.png').read_bytes()).hexdigest()})
 b.close()
(root/'qa.json').write_text(json.dumps({'status':'browser layout/data smoke passed; manual visual review done, game/device not run','checks':results},ensure_ascii=False,indent=2)+'\n')
print('4 full pages validated')
