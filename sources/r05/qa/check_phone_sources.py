from pathlib import Path
from playwright.sync_api import sync_playwright
import xml.etree.ElementTree as ET,json,re
r=Path('/workspace/shared/R05-ui-review');out={}
for page,filename in [('arena','b/phone.svg'),('hatch','a/phone.svg'),('story','c/phone.svg')]:
 p=r/page/filename;root=ET.parse(p).getroot();assert float(root.attrib['width'])==844 and float(root.attrib['height'])==390
 texts=[e for e in root.iter() if e.tag.endswith('text')];sizes=[float(e.attrib['font-size']) for e in texts if e.attrib.get('font-size')];assert sizes and min(sizes)>=14,(page,min(sizes))
 rects=[e for e in root.iter() if e.tag.endswith('rect')];targets=[e for e in rects if float(e.attrib.get('height',0))>=44 and float(e.attrib.get('width',0))>=44]
 out[page]={'svg':[844,390],'min_explicit_text_font_px':min(sizes),'rectangles_at_least44x44':len(targets),'scope':'Rect count includes decorative rectangles, not a count of interactive buttons; declared button regions also visually checked. Static SVG concept.'}
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True);page=b.new_page(viewport={'width':844,'height':390});page.set_content((r/'storage/b/phone_source.html').read_text(),wait_until='networkidle');buttons=page.locator('button').evaluate_all('(a)=>a.filter(e=>e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0).map(e=>({text:e.innerText,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}))');assert buttons and all(x['height']>=44 and x['width']>=44 for x in buttons),buttons
 fonts=page.evaluate('()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n,a=[];while(n=w.nextNode()){if(!n.textContent.trim())continue;const e=n.parentElement;if(["SCRIPT","STYLE"].includes(e.tagName))continue;const r=e.getBoundingClientRect(),s=getComputedStyle(e);if(r.width>0&&r.height>0&&s.visibility!=="hidden")a.push(parseFloat(s.fontSize))}return a}');assert min(fonts)>=14,min(fonts);assert page.evaluate('document.documentElement.scrollWidth')==844;page.screenshot(path=str(r/'qa/storage-phone-source-browser.png'));out['storage']={'viewport':[844,390],'min_visible_text_font_px':min(fonts),'visible_html_buttons':buttons,'no_horizontal_overflow':True,'scope':'Independent local HTML concept-prototype check; not game or real device'};b.close()
(r/'qa/phone-source-checks.json').write_text(json.dumps({'result':'PASS','pages':out,'real_device':'NOT_RUN'},ensure_ascii=False,indent=2));print('PHONE SOURCES PASS four native layouts')
