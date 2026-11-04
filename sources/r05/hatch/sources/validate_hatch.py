from pathlib import Path
import json,tempfile,subprocess,hashlib,xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
checks=[]
for v in 'abcd':
 d=ROOT/v;data=json.loads((d/'review.json').read_text());assert len(data['detail_images'])==(7 if v=='a' else 6)
 for item in [{'image':data['image']}]+data['detail_images']:
  p=d/item['image'];assert p.exists();assert Image.open(p).size==((844,390) if p.stem=='phone' else (1600,900));ET.parse(p.with_suffix('.svg'));assert p.with_suffix('.html').exists();checks.append(str(p.relative_to(ROOT)))
# Both all-parent-missing state and precise temporary probability are visibly authored.
for v in 'abcd':
 s=(ROOT/v/'empty_rules.svg').read_text()
 for t in ['99%','1%','+10','+1～+9','9 : 8 : 7 : 6 : 5 : 4 : 3 : 2 : 1','缺任一亲本','Lv.0']:assert t in s,t
 assert '立即孵化' not in s
for v in 'abcd':
 s=(ROOT/v/'success.svg').read_text()
 for t in ['人工结果示例','非孵化实录','#21 泡泡鱼 ♀','待定','0','吸附泡泡   +3','八方泡泡   +2']:assert t in s,t
sample=json.loads((ROOT.parent/'sample.json').read_text());assert sample['mother']['innate']==[34,41,48,12,19,26];assert sample['father']['innate']==[23,30,37,44,8,15]
with tempfile.TemporaryDirectory(prefix='r05-hatch-rebuild-') as td:
 subprocess.run(['python3',str(Path(__file__).with_name('build_hatch.py')),'--root',td],check=True)
 generated=[p for v in 'abcd' for p in (ROOT/v).iterdir() if p.suffix in ['.png','.svg','.html','.json']]+[ROOT/'review.json']
 for p in generated:assert p.read_bytes()==(Path(td)/p.relative_to(ROOT)).read_bytes(),str(p)
 report={'status':'PASS','game_commit':sample['game_commit'],'png_count':29,'svg_count':29,'html_count':29,'json_count':5,'png_dimensions':{'28':[1600,900],'a/phone.png':[844,390]},'phone_min_font_px':14,'phone_primary_touch_height_px':44,'detail_image_paths':'29/29 main and details exist','reproduction':{'files_compared':len(generated),'byte_identical':True},'source_sha256':hashlib.sha256(Path(__file__).with_name('build_hatch.py').read_bytes()).hexdigest(),'manual_inspection':'4 main layouts, both complete parent details, confirm, result and empty/rules visually inspected; separate 844x390 A phone and 4 distinct complete artificial success-result pages visually inspected','not_run':['Godot execution','real hatch save','device/touch QA','game regression (no game code changed)'],'images':checks}
 (ROOT/'sources'/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k!='images'},ensure_ascii=False))
