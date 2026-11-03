from pathlib import Path
import json,shutil,hashlib,argparse
parser=argparse.ArgumentParser(description='Copy R04 review media and rebuild review-data / public manifest; no game or integration package changes.')
parser.add_argument('--source',default='/workspace/shared/R04-review',help='R04 input root containing DECISIONS,characters,audio,ui')
parser.add_argument('--repo',default='/workspace/ball_art_review',help='Existing review website checkout with docs/index.html and r04 app/style')
args=parser.parse_args()
SRC=Path(args.source).resolve();REPO=Path(args.repo).resolve()
if SRC==REPO or SRC in REPO.parents:raise SystemExit('Output repository must not be inside source inputs')
DOC=REPO/'docs/r04';SOURCE=REPO/'sources/r04'
IDS=['puffer','chicken','bubble_fish','electric_sheep','magnet_crab','cactus','shell_turtle','crow'];NAMES=['充气球','炸弹母鸡','泡泡鱼','触电羊','磁铁蟹','仙人掌','脱壳乌龟','乌鸦']
PUBLIC={'.png','.svg','.gif','.wav','.mp4','.json','.md','.txt'}; SOURCE_EXT=PUBLIC|{'.py','.gd','.html','.js','.css'}
def copy_dir(src,dest,allowed):
 if not src.exists():return
 for p in sorted(src.rglob('*')):
  if p.is_file() and p.suffix.lower() in allowed and not any(x.startswith('.') for x in p.relative_to(src).parts):
   assert not p.is_symlink(),p
   out=dest/p.relative_to(src);out.parent.mkdir(parents=True,exist_ok=True);
   if p.resolve()!=out.resolve():shutil.copyfile(p,out)
def norm(x,src,prefix,key=''):
 if isinstance(x,list):return [norm(v,src,prefix,key) for v in x]
 if isinstance(x,dict):return {k:norm(v,src,prefix,k) for k,v in x.items()}
 if isinstance(x,str) and x and key in {'image','animation','file','url','svg','setting_path','setting_url','poster','cover'}:
  p=Path(x);p=p if p.is_absolute() else src/p
  if p.is_file():return prefix+p.resolve().relative_to(src.resolve()).as_posix()
 return x
DOC.mkdir(parents=True,exist_ok=True);SOURCE.mkdir(parents=True,exist_ok=True)
for name in ['DECISIONS.json','DECISIONS.md']:

 for destination in [DOC/name,SOURCE/name]:
  if (SRC/name).resolve()!=destination.resolve():shutil.copyfile(SRC/name,destination)
for name in ['source','sources','web']:
 copy_dir(SRC/name,SOURCE/name,SOURCE_EXT)
audio=json.loads((SRC/'audio/review.json').read_text()) if (SRC/'audio/review.json').is_file() else {'characters':{}}
copy_dir(SRC/'audio',DOC/'audio',PUBLIC);copy_dir(SRC/'audio',SOURCE/'audio',SOURCE_EXT)
characters=[]
for id,name in zip(IDS,NAMES):
 src=SRC/'characters'/id;copy_dir(src,DOC/'characters'/id,PUBLIC);copy_dir(src,SOURCE/'characters'/id,SOURCE_EXT)
 raw=json.loads((src/'review.json').read_text()) if (src/'review.json').is_file() else {'status':'in_production','confirmed':[],'awaiting':['材料仍在制作，未视为完成。']}
 c=norm(raw,src,'r04/characters/'+id+'/');c.update(id=id,name=name)
 if (src/'SETTING.md').is_file():c['setting_path']='r04/characters/'+id+'/SETTING.md'
 elif c.get('setting_path'):c['setting_path']=None
 c['audio']=norm(audio.get('characters',{}).get(id,{}),SRC/'audio','r04/audio/')
 characters.append(c)
ui=None
if (SRC/'ui/review.json').is_file():
 copy_dir(SRC/'ui',DOC/'ui',PUBLIC);copy_dir(SRC/'ui',SOURCE/'ui',SOURCE_EXT)
 ui=norm(json.loads((SRC/'ui/review.json').read_text()),SRC/'ui','r04/ui/')
data={'version':'R04-selected-media-review-1','scope':'review webpage only; selected directions, all-new sounds awaiting audition','decisions':'r04/DECISIONS.json','characters':characters,'ui':ui,'old_R03_audio_used':False}
(DOC/'review-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
files=[]
for p in sorted(DOC.rglob('*')):
 if p.is_file() and p.name!='PUBLIC_MANIFEST.json':files.append({'path':p.relative_to(REPO/'docs').as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(DOC/'PUBLIC_MANIFEST.json').write_text(json.dumps({'scope':'R04 public media review only, no integration package','files':files},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'characters':len(characters),'selected_images':sum(bool(c.get('image')) for c in characters),'animations':sum(bool(c.get('animation')) for c in characters),'new_events':sum(len(c['audio'].get('events',[])) for c in characters),'montages':sum(bool(c['audio'].get('montage')) for c in characters),'ui':bool(ui),'public_files':len(files)}))
