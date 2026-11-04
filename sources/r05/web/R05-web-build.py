#!/usr/bin/env python3
"""Build public R05 review data; never publishes, deletes history, or modifies game."""
import argparse,json,hashlib,shutil,struct
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--source',default='/workspace/shared/R05-ui-review');ap.add_argument('--repo',default='/workspace/ball_art_review');a=ap.parse_args();src=Path(a.source).resolve();repo=Path(a.repo).resolve();out=repo/'docs/r05';sources=repo/'sources/r05';out.mkdir(parents=True,exist_ok=True);sources.mkdir(parents=True,exist_ok=True)
public={'.png','.svg','.gif','.jpg','.jpeg','.webp','.json','.md','.txt'};source=public|{'.py','.gd','.html','.js','.css'}
def cp(s,d):
 if s.resolve()!=d.resolve():d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,d)
def asset(base,value):
 p=(base/value).resolve()
 if not p.is_relative_to(src) or not p.is_file():raise ValueError(f'missing/outside asset {p}')
 return 'r05/'+p.relative_to(src).as_posix()
pages=[]
for pid,name in [('arena','竞技场'),('storage','仓库'),('hatch','孵蛋'),('story','主线')]:
 root=src/pid;schemes=[];master=root/'review.json'
 entries=[]
 if master.exists():
  raw=json.loads(master.read_text());raw=raw.get('schemes',raw.get('variants',raw.get('options',raw))) if isinstance(raw,dict) else raw
  if isinstance(raw,list):entries=[(root,x)for x in raw]
 if not entries:
  for sid in 'abcd':
   p=root/sid/'review.json'
   if p.exists():entries.append((p.parent,json.loads(p.read_text())))
 for base,s in entries:
  s=dict(s);s['id']=str(s['id']).lower();s['image']=asset(base,s['image']);details=[]
  for i,v in enumerate(s.get('detail_images',[])):
   if isinstance(v,str):details.append({'image':asset(base,v),'title':'副状态 '+str(i+1)})
   else:
    v=dict(v);v['image']=asset(base,v.get('image',v.get('file')));details.append(v)

  for v in details:
   ip=src/v['image'].removeprefix('r05/')
   if ip.suffix.lower()=='.png':
    w,h=struct.unpack('>II',ip.read_bytes()[16:24]);v['dimensions']={'width':w,'height':h}
  s['detail_images']=details;schemes.append(s)
 pages.append({'id':pid,'name':name,'schemes':schemes})
for p in src.rglob('*'):
 if not p.is_file() or p.is_symlink() or any(x.startswith('.') for x in p.relative_to(src).parts):continue
 rel=p.relative_to(src)
 if p.suffix.lower() in source:cp(p,sources/rel)
 # HTML/generation/source never copied into public website media directory
 if p.suffix.lower() in public and not any(x in {'source','sources','web'} for x in rel.parts):cp(p,out/rel)
(out/'review-data.json').write_text(json.dumps({'version':'R05','status':'candidates_not_selected','pages':pages},ensure_ascii=False,indent=2)+'\n')
(out/'PUBLIC_SCOPE.md').write_text('# R05 公开范围\n\n四页候选主图与副图均为原创 UI 效果图，非实际游戏实录；统一人工示例数据不代表已接入。qa/current_*.png 仅为既有 3dd29e8 游戏在隔离空 save 下的虚拟桌面基线截图，不含玩家存档，不是真机，也不证明 R05 接入。未修改游戏与玩法，所有候选待用户选择。旧轮文件保留历史，不进入本轮导航。生成源码保留仓库 sources/r05；不含字体二进制、团队内部配置、私密资料或接入压缩包。\n')
manifest=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name!='PUBLIC_MANIFEST.json':
  b=p.read_bytes();manifest.append({'path':p.relative_to(repo/'docs').as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(out/'PUBLIC_MANIFEST.json').write_text(json.dumps({'version':'R05','files':manifest},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pages':[{p['id']:len(p['schemes'])}for p in pages],'public_files':len(manifest)}))
