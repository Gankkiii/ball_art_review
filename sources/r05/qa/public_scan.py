from pathlib import Path
import os,re,json,sys
root=Path('/workspace/ball_art_review');rows=[];symlinks=[];forbidden=[];count=0
patterns={'github_pat':rb'github_pat_[A-Za-z0-9_]{20,}','github_token':rb'gh[pousr]_[A-Za-z0-9]{20,}','private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----','api_key_like':rb'\bsk-[A-Za-z0-9_-]{20,}','aws_access':rb'\bAKIA[A-Z0-9]{16}\b','credential_assignment':rb'(?i)(?:password|api_key|access_token|secret_key)\s*[:=]\s*[\x22\x27][^\x22\x27\r\n]{12,}[\x22\x27]'}
for cur,dirs,files in os.walk(root,followlinks=False):
 dirs[:]=[d for d in dirs if d!='.git']
 for name in dirs+files:
  p=Path(cur)/name
  if p.is_symlink():symlinks.append(str(p.relative_to(root)))
 for name in files:
  p=Path(cur)/name
  if p.is_symlink():continue
  rel=str(p.relative_to(root));count+=1
  if any(x in p.parts for x in ['.codex','art-team','__pycache__','.godot'])or p.suffix.lower()in ['.ttf','.otf','.keystore','.jks','.p12','.pem']or p.name in ['.env','.netrc','credentials']:forbidden.append(rel)
  data=p.read_bytes()
  for key,pat in patterns.items():
   n=len(re.findall(pat,data))
   if n:rows.append({'path':rel,'pattern':key,'matches':n})
out={'result':'PASS'if not(rows or symlinks or forbidden)else'REVIEW_REQUIRED','scope':'All working-tree files in public review repository, existing history assets retained; .git metadata excluded. Finite byte patterns only, not a guarantee of finding every secret. No matched values emitted.','file_count':count,'matches':rows,'symlinks':symlinks,'private_configuration_or_font_binary_paths':forbidden};Path('/workspace/shared/R05-ui-review/qa/public-scan.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));sys.exit(bool(rows or symlinks or forbidden))
