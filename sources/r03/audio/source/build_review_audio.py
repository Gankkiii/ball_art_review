"""Original procedural R03 audition montages. No recordings or external samples.
Events are stitched for comparison, not real gameplay timers or approved sounds.
Python 3 + NumPy, PCM WAV 48 kHz / 16 bit / mono. Pass a new output directory.
"""
from pathlib import Path
import argparse, json, wave, hashlib
import numpy as np

SR=48000
RNG=np.random.default_rng(2026110303)
def tone(kind,duration,base,style):
    t=np.arange(round(SR*duration))/SR
    noise=RNG.normal(0,1,len(t))
    smooth=np.convolve(noise,np.ones(19 if style=='B' else 7)/19 if style=='B' else np.ones(7)/7,mode='same')
    attack=np.minimum(1,t/.008)
    env=attack*np.power(np.maximum(0,1-t/duration),1.7)
    f=base*(.78 if style=='B' else 1.0)
    if kind=='air':
        s=.65*smooth+.1*np.sin(2*np.pi*(f*t+35*t*t))
    elif kind=='rubber':
        s=.55*np.sin(2*np.pi*(f*t-80*t*t))+.1*noise*np.exp(-t*50)
    elif kind=='pop':
        s=.5*np.sin(2*np.pi*(f*t-140*t*t))*np.exp(-t*8)+.1*smooth
    elif kind=='electric':
        s=.27*np.sin(2*np.pi*f*t)+.16*np.sin(2*np.pi*f*1.53*t)+.22*smooth
        s*=.62+.38*np.sin(2*np.pi*42*t)**2
    elif kind=='metal':
        s=sum(.24/(i+1)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(5+i*3)) for i,k in enumerate([1,1.43,2.71,4.07]))+.14*smooth*np.exp(-t*60)
    elif kind=='thud':
        s=.55*np.sin(2*np.pi*(f*t-30*t*t))*np.exp(-t*6)+.2*smooth
    elif kind=='wood':
        s=.25*np.sin(2*np.pi*f*t)*np.exp(-t*18)+.2*np.sin(2*np.pi*f*2.47*t)*np.exp(-t*35)+.2*smooth*np.exp(-t*22)
    elif kind=='rustle':
        s=smooth*(.4+.35*np.sin(2*np.pi*17*t)**2)+.06*np.sin(2*np.pi*f*t)
    elif kind=='explosion':
        s=.65*smooth*np.exp(-t*3)+.45*np.sin(2*np.pi*(f*t-20*t*t))*np.exp(-t*5)
    else:raise ValueError(kind)
    return s*env

DATA={
 'puffer':('充气球',[('气体充入','air',.42,520),('受击吸收','rubber',.20,530),('放气喷流','air',.48,280),('放气有效碰撞','rubber',.23,210)],'A 轻弹乳胶','B 低声气囊','A更轻巧、B更饱满；都不用爆炸声冒充气体或新增气弹。'),
 'chicken':('炸弹母鸡',[('小蛋落地','wood',.14,700),('惊跑脚步','wood',.24,380),('已触发引信提示','electric',.22,1050),('真实蛋爆炸','explosion',.50,95)],'A 玩具蛋壳','B 厚壳闷爆','A便于密集物件分辨，B强调大小蛋重量；引信声不是新的伤害计时器。'),
 'bubble_fish':('泡泡鱼',[('吐出1级泡泡','pop',.19,920),('自身泡泡融合','pop',.29,640),('吸附泡泡启动','air',.44,430),('融合泡泡有效命中','pop',.28,370)],'A 清亮水泡','B 温润低泡','A融合更清楚，B较柔和；1级消失与有伤命中必须用不同强度，不能伪造1级伤害。'),
 'electric_sheep':('触电羊',[('撞墙充电','electric',.23,720),('落下一团羊毛','rustle',.28,350),('持续放电截段','electric',.46,430),('电库耗尽','electric',.22,210)],'A 干脆电跳','B 绒毛低嗡','A突出充电，B减少持续高频；放电截段仅音色试听，不意味着新增攻击间隔。'),
 'magnet_crab':('磁铁蟹',[('铁钉落地','metal',.17,1150),('磁化启动','electric',.30,260),('移动钉有效命中','metal',.26,720),('返身弹钉','metal',.20,1450)],'A 明亮小金属','B 厚重磁铁','A区分钉的阶段更鲜明，B磁化较低沉；静止钉不播放伤害声。'),
 'cactus':('仙人掌',[('散刺脱离','rustle',.24,850),('刺点有效命中','wood',.15,1050),('旧位置缩回示意','rustle',.22,250),('换位后出现','wood',.20,480)],'A 干燥轻刺','B 柔木根音','A更利落、B更温和；换位不是回血，禁用治疗提示音。'),
 'shell_turtle':('脱壳乌龟',[('本体进入壳','wood',.22,390),('原地旋壳截段','rustle',.42,460),('壳有效碰撞','thud',.25,160),('成功离壳','pop',.20,540)],'A 空心壳敲','B 厚壳闷响','A空壳易识别，B碰撞更厚；旋转声不表示高速冲刺或额外击退。'),
 'crow':('乌鸦',[('放置稻草人','wood',.25,310),('成功交换位置','rustle',.32,680),('储存羽毛','rustle',.22,950),('碰触修复自家稻草人','wood',.24,620),('稻草人真实承伤与反射','wood',.22,220)],'A 草束轻拍','B 羽翼低掠','A强调草人，B强调翅羽；没有飞羽远程攻击，修复只跟真实自家草人事件。')
}

def build(out):
    root=Path(out);root.mkdir(parents=True,exist_ok=True)
    result={'cycle':'R03','kind':'unapproved auditory direction montages','format':'PCM WAV 48000 Hz 16 bit mono','human_listening':'NOT_RUN','in_game':'NOT_RUN','characters':{}}
    for cid,(name,events,title_a,title_b,note) in DATA.items():
        variants=[]
        for style,title in [('A',title_a),('B',title_b)]:
            pieces=[];marks=[];cursor=0
            for label,kind,duration,f in events:
                sound=tone(kind,duration,f,style)
                marks.append({'event':label,'start_s':round(cursor/SR,4),'duration_s':duration,'note':'编排试听，非真实战斗时间'})
                pieces.extend([sound,np.zeros(round(.22*SR))]);cursor+=len(sound)+round(.22*SR)
            signal=np.concatenate(pieces);peak=float(np.max(np.abs(signal)))
            signal*=.70/max(peak,1e-9)
            pcm=np.round(signal*32767).astype('<i2');file=f'{cid}_{style}.wav'
            with wave.open(str(root/file),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
            variants.append({'id':style,'title':title,'file':file,'event':' → '.join(e[0] for e in events),'description':note,'events':marks,'duration_s':len(pcm)/SR,'peak_linear':float(np.max(np.abs(pcm.astype(float)))/32767),'clipped_samples':int(np.sum(np.abs(pcm.astype(np.int32))>=32767)),'sha256':hashlib.sha256((root/file).read_bytes()).hexdigest(),'status':'已制作合成试听段并检查PCM；未人工听审、未游戏验证'})
        result['characters'][cid]={'name':name,'variants':variants,'recommendation':'优先试听A的辨识度，再比较B的厚度；推荐不是已选定稿。','question':'选择A或B音色方向，或逐事件组合；试听编排不改变实际技能时点。'}
    recommendations={
      'puffer':'建议先试听A的弹性气体方向，B可用于更厚的吸收/放气；此为设计意图，听感待用户判断。',
      'chicken':'建议A保留蛋壳/脚步分辨，爆炸可比较B低频方向；不靠更响表示新增伤害。',
      'bubble_fish':'建议A水泡方向，与气球排气、电羊电流分开；B适合降低整体高频的组合。',
      'electric_sheep':'建议比较B持续低嗡与A短充电提示的组合，连续放电不变成周期攻击。',
      'magnet_crab':'建议A用于移动钉触碰，B可用于磁化启动；静止钉不加持续危险音。',
      'cactus':'建议A保留干燥刺物质感，B可用于换位出现；两者都不用治疗音暗示回血。',
      'shell_turtle':'建议A区分空壳进入/离开，B比较壳碰撞重量；不能听成新增冲刺。',
      'crow':'建议A强调草人承伤与修复，B比较换位羽响；羽毛不是远程武器。'}
    for cid,character in result['characters'].items():
        character['recommendation']=recommendations[cid]
        for v in character['variants']:
            if v['id']=='A':
                v['pros']=['设计意图：较高的瞬态与较轻的材料声，便于比较事件起点。']
                v['cons']=['潜在风险：密集事件可能争抢高频；未做扬声器听审与混音验证。']
            else:
                v['pros']=['设计意图：降低基频、增加柔和低频厚度，与A作明显音色对比。']
                v['cons']=['潜在风险：手机扬声器可能丢低频，事件辨识需实际试听。']
    (root/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Created 16 candidate audition montages; no human listening claim')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);build(parser.parse_args().output)
