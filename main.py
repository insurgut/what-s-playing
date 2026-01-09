#              ▓███                  
#            ░█████                  Привет брат, я рад что ты зашёл сюда, данный код был сделан на коленке под двумя
#            ██████                  банками хмельного, пусть и так, но ты же этим заинтересовался, и я очень благодарен тебе! )
#            ██████                  
#            ▒█████                  Контакт для связи и предложений: Telegram @lisurgut.
#             ▒████                  
#                ░░█▓░               Если используешь информацию из данного кода, будь добр - не выставляй за лично своё,
#                  █████░            буду рад если укажешь моё соавторство или хотя бы где то сможешь упомянуть меня как разработчика <3
#                  █████▓            
#                  ██████            ██ █ ███████ ██ █ ██ █████ █ ██████ ██████ █ █████ █ █ ████████ █ ███ █ ██ ██ █████ █ █ ████████ ██
#                  █████▓            █ █ ███ █ █████ ██ ███ █ ███████ ███ █████ █ █████ ██ ███████ ████ █ ██ █ █ █ ████ █ ███ █████ ██ █
#                  █████░            █ █████ ███ ███████ ██ ███ █ █████ █████ ███ █ █████ █ ██ █████ ██████ ██ ███ ████ ███ ███ ██████ █
#                  ██▓░               


import configparser,asyncio,sys,requests,re,io,urllib.parse,json,os,time,threading,logging,random,string
from flask import Flask,request,jsonify
import telethon
from telethon import TelegramClient,functions,types,errors,events,utils
from telethon.extensions import html
from PIL import Image, ImageDraw
from yandex_music import Client as YMClient

CFG='config.json';CV='covers_cache.json'
app=Flask(__name__);logging.getLogger('werkzeug').setLevel(logging.ERROR)

# === DEFAULT CONFIG STRUCTURE ===
DEF_CFG = {
    "telegram": {
        "api_id": 0, "api_hash": "", "cid": 0, "mid": 0,
        "pack_name": "music_covers_v1", "cmd": ".mul",
        "set_status": True, "off_status_emoji": "0",
        "use_cache": True, "use_cloud": True
    },
    "messages": {
        "false_mes": "<blockquote>{emoji=5890937586544807413} <b>Музыка на паузе</b></blockquote>",
        "true_mes": "<blockquote>{emoji=5915480455603295660} <b>Играет:</b></blockquote>\n\n<blockquote>{cover} {name} • {title}</blockquote>\n\n<blockquote>{emoji=5346296430166293639} <a href=\"{link_to=yandexmusic}\">Яндекс</a></blockquote>"
    },
    "lastfm": { "api_key": "", "username": "" },
    "yandex": { "token": "" }
}

def ld_c():
 if not os.path.exists(CFG):
  print("⚠️ Config not found. Creating new...")
  json.dump(DEF_CFG,open(CFG,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
  return DEF_CFG
 try:return json.load(open(CFG,encoding='utf-8'))
 except:return DEF_CFG

def sv_c(d):json.dump(d,open(CFG,'w',encoding='utf-8'),ensure_ascii=False,indent=4)

HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
body{background:#0d0d0d;color:#ccc;font-family:'Consolas',monospace;padding:20px;display:flex;flex-direction:column;align-items:center}
.box{width:100%;max-width:700px}
.sec{color:#555;font-size:10px;text-transform:uppercase;margin:25px 0 5px 0;letter-spacing:1px;border-bottom:1px solid #222}
.row{display:flex;align-items:center;background:#161616;padding:8px;border-radius:6px;margin-bottom:2px}
.tag{background:#252525;color:#888;padding:4px 8px;border-radius:4px;font-size:12px;margin-right:10px;white-space:nowrap;min-width:120px}
.val{background:none;border:none;color:#ddd;font-family:inherit;font-size:13px;width:100%;outline:none}
.val:focus{color:#fff}
.masked{cursor:pointer;color:#666;font-style:italic}
.masked:hover{color:#888}
.desc{font-size:11px;color:#444;margin-bottom:8px;margin-left:5px;font-style:italic}
.sw{position:relative;width:34px;height:18px}
.sw input{opacity:0;width:0;height:0}
.sl{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#333;border-radius:18px;transition:.3s}
.sl:before{position:absolute;content:"";height:14px;width:14px;left:2px;bottom:2px;background:#777;border-radius:50%;transition:.3s}
input:checked+.sl{background:#2ea043}
input:checked+.sl:before{transform:translateX(16px);background:#fff}
</style></head><body><div class="box" id="c"></div>
<script>
let d={};const S=['api_hash','token','api_key'];
const DESCS = {
 'api_id': 'Telegram APP ID (my.telegram.org)',
 'cid': 'Target Channel/Group ID (-100...)',
 'mid': 'Message ID to edit (Integer)',
 'cmd': 'Command to forward status',
 'set_status': 'Update User Profile Emoji Status?',
 'off_status_emoji': 'Emoji ID when paused (0 to clear)',
 'true_mes': 'Vars: {name}, {title}, {cover}, {link_to=yandex}',
 'token': 'Yandex Music Token (y0_...)'
};
async function L(){d=await(await fetch('/g')).json();R()}
function R(){
 let h=document.getElementById('c');h.innerHTML='';
 for(let s in d){
  let sh=document.createElement('div');sh.className='sec';sh.innerText=s;h.appendChild(sh);
  for(let k in d[s]){
   let r=document.createElement('div');r.className='row';
   let t=document.createElement('div');t.className='tag';t.innerText=k;r.appendChild(t);
   let v=d[s][k];
   if(typeof v==='boolean'){
    let l=document.createElement('label');l.className='sw';
    let cb=document.createElement('input');cb.type='checkbox';cb.checked=v;
    cb.onchange=(e)=>{d[s][k]=e.target.checked;Szv()};
    let sl=document.createElement('span');sl.className='sl';l.append(cb,sl);r.appendChild(l);
   }else if(S.includes(k) && String(v).length>10){
    let sp=document.createElement('span');sp.className='masked';sp.innerText=String(v).substr(0,5)+'...'+String(v).substr(-5);
    sp.onclick=()=>{
     let i=document.createElement('input');i.className='val';i.value=v;
     i.onblur=()=>{d[s][k]=i.value;Szv();R()};
     sp.replaceWith(i);i.focus();
    };r.appendChild(sp);
   }else{
    let i=document.createElement('input');i.className='val';i.value=v;
    i.oninput=(e)=>{d[s][k]=isNaN(e.target.value)?e.target.value:Number(e.target.value)};
    if(typeof v==='string')i.oninput=(e)=>{d[s][k]=e.target.value};
    i.onblur=()=>Szv();r.appendChild(i);
   }
   h.appendChild(r);
   if(DESCS[k]){
    let ds=document.createElement('div');ds.className='desc';ds.innerText=DESCS[k];h.appendChild(ds);
   }
  }
 }
}
async function Szv(){await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})}
L();
</script></body></html>"""

@app.route('/g')
def g():return jsonify(ld_c())
@app.route('/',methods=['GET','POST'])
def i():
 if request.method=='POST':sv_c(request.json);return 'OK'
 return HTML
def rf():app.run(host='0.0.0.0',port=41720,use_reloader=False)
threading.Thread(target=rf,daemon=True).start()
print("🔗 UI: http://127.0.0.1:41720")

# === WAIT FOR CONFIG ===
while True:
 c = ld_c()
 try:
  if c['telegram']['api_id'] and c['telegram']['api_hash']: break
 except: pass
 print("⏳ Waiting for config... Fill it at http://127.0.0.1:41720")
 time.sleep(5)

# === START ===
AID,AHS=c['telegram']['api_id'],c['telegram']['api_hash']
cl=TelegramClient('session',AID,AHS);ym=YMClient(token=c['yandex']['token']) if c['yandex']['token'] else YMClient()
mem={'trk':None,'lnk':{},'cv_id':None,'last_msg':'','stop_ticks':0,'last_st':None,'fw':0,'last_st_fail':0}
cv_c=json.load(open(CV,encoding='utf-8')) if os.path.exists(CV) else {}
def sv_cache():json.dump(cv_c,open(CV,'w',encoding='utf-8'),ensure_ascii=False)
def lg(t,m):print(f"[{time.strftime('%H:%M:%S')}] {t} {m}")
def u16(s):return len(s.encode('utf-16-le'))//2

def parse_hybrid(txt):
 t,ents=html.parse(txt);ms=list(re.finditer(r'\{emoji=(\d+)\}',t))
 for m in reversed(ms):
  s,e=m.span();eid=int(m.group(1));rep="👾"
  s16=u16(t[:s]);l_old=u16(t[s:e]);l_new=u16(rep);dt=l_new-l_old
  t=t[:s]+rep+t[e:]
  for en in ents:
   if en.offset>=s16+l_old:en.offset+=dt
   elif en.offset+en.length>=s16+l_old:en.length+=dt
  ents.append(types.MessageEntityCustomEmoji(s16,l_new,eid))
 return t,ents

@cl.on(events.NewMessage(outgoing=True))
async def h_cmd(e):
 cfg=ld_c()
 if e.text==cfg['telegram']['cmd']:
  await e.delete()
  try:await cl.forward_messages(e.chat_id,cfg['telegram']['mid'],cfg['telegram']['cid'])
  except Exception as x:lg("CMD",x)
 elif e.text=='.test':
  await e.edit("🔄 <b>Check...</b>",parse_mode='html');p=cfg['telegram']['pack_name']
  try:
   s=await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(p),0))
   if not s.documents:await e.edit(f"❌ Empty: {p}");return
   m=f"📦 <a href='https://t.me/addemoji/{p}'>{p}</a>\n"
   for d in s.documents[-3:]:m+=f"🆔 <code>{d.id}</code>: {{emoji={d.id}}}\n"
   t,en=parse_hybrid(m);await e.edit(t,formatting_entities=en,link_preview=True)
  except Exception as x:await e.edit(f"Err: {x}")
 elif e.text.startswith('.em '):
  try:await e.delete();t="👾";i=int(e.text.split()[1]);await cl.send_message(e.chat_id,t,formatting_entities=[types.MessageEntityCustomEmoji(0,u16(t),i)])
  except:pass

def g_trk(cfg):
 try:
  r=requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={cfg['lastfm']['username']}&api_key={cfg['lastfm']['api_key']}&format=json&limit=1",timeout=2).json()
  t=r['recenttracks']['track'][0]
  return {'play':t.get('@attr',{}).get('nowplaying')=='true','art':t['artist']['#text'],'tit':t['name'],'img':None}
 except:return None
def g_itu(q):
 try:
  r=requests.get(f"https://itunes.apple.com/search?term={urllib.parse.quote(q)}&entity=song&limit=1",timeout=2).json()
  if r['resultCount']>0:return r['results'][0]['artworkUrl100'].replace('100x100','600x600')
 except:pass;return None
def g_yam(q):
 try:
  s=ym.search(q);
  if s.best and s.best.type=='track':return "https://"+s.best.result.cover_uri.replace('%%','400x400')
 except:pass;return None
def f_lnk(a,t):
 q=f"{a} {t}";d={}
 try:
  r=requests.get(f"https://api.song.link/v1-alpha.1/links?userCountry=RU&songIfNoneFound=true&q={urllib.parse.quote(q)}",timeout=3,headers={'User-Agent':'Mozilla/5.0'}).json()
  for k,v in r.get('linksByPlatform',{}).items():d[k]=v['url']
 except:pass
 if 'yandex' not in d:
  try:
   s=ym.search(q);t=s.best.result if s.best and s.best.type=='track' else None
   if t:d['yandex']=f"https://music.yandex.ru/album/{t.albums[0].id}/track/{t.id}"
  except:pass
 return d

def g_cld(k,cfg):
 if not cfg['telegram'].get('use_cloud',False):return None
 try:
  r=requests.get("https://api.lisurgut.ru/et/s",timeout=3)
  if r.status_code==200:
   data=r.json()
   for item in data:
    if item.get('track')==k:
     eid=item.get('emoji_id');lg("SCL",f"Found: {eid}");return eid
  return None
 except Exception as e:lg("SCL",f"ERR: {e}");return None

def s_cld(k,eid,cfg):
 if not cfg['telegram'].get('use_cloud',False):return
 try:
  r=requests.post("https://api.lisurgut.ru/et/add",json={"track":k,"emoji_id":str(eid)},timeout=5)
  lg("SCL",f"Add: {r.status_code}")
 except Exception as e:lg("SCL",f"Add ERR: {e}")

async def inst_p(p):
 try:await cl(functions.messages.InstallStickerSetRequest(types.InputStickerSetShortName(p),False))
 except:pass

async def create_pack_via_bot(title, name, png_bytes):
 lg("BOT_CHAT","Starting pack creation via @Stickers...")
 try:
  async with cl.conversation("@Stickers",timeout=30) as conv:
   await conv.send_message("/cancel");await asyncio.sleep(0.5)
   await conv.send_message("/newemojipack")
   r = await conv.get_response()
   if r.buttons:
    for row in r.buttons:
     for btn in row:
      if "Static" in btn.text: await btn.click();break
   await conv.get_response()
   await conv.send_message(name)
   await conv.get_response()
   upl = await cl.upload_file(png_bytes, file_name="s.png")
   await conv.send_file(upl, force_document=True)
   await conv.get_response()
   await conv.send_message("💿")
   await conv.get_response()
   await conv.send_message("/publish")
   await conv.get_response()
   await conv.send_message("/skip")
   await conv.get_response()
   await conv.send_message(name)
   r = await conv.get_response()
   await cl.delete_dialog("@Stickers")
   return "Kaboom" in r.text
 except Exception as e:
  lg("BOT_CHAT",f"Err: {e}")
  try:await cl.delete_dialog("@Stickers")
  except:pass
  return False

async def up_cv(u,k,cfg):
 cid=g_cld(k,cfg)
 if cid:lg("CLD",f"Found: {cid}");return cid
 if cfg['telegram'].get('use_cache',False) and k in cv_c:return cv_c[k]
 
 lg("CV",f"Load: {u[:30]}...");b=io.BytesIO()
 try:
  i=Image.open(io.BytesIO(requests.get(u).content)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
  msk=Image.new('L',(100,100),0);ImageDraw.Draw(msk).rounded_rectangle((0,0,100,100),radius=25,fill=255)
  i.putalpha(msk);i.save(b,'PNG');b.seek(0);b.name="c.png"
  png_bytes = b.getvalue()
  
  pack=cfg['telegram']['pack_name']
  try:
   s=await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack),0))
   if len(s.documents)>=100:
    me=await cl.get_me()
    rnd=''.join(random.choices(string.ascii_letters,k=6))
    np=f"em{me.id}_{rnd}"
    lg("PACK",f"Full! Creating via Bot: {np}")
    ok = await create_pack_via_bot(f"Music {np}", np, png_bytes)
    if ok:
     c=ld_c();c['telegram']['pack_name']=np;sv_c(c);pack=np
     await inst_p(pack)
     s=await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack),0))
     nid=s.documents[0].id
     s_cld(k,nid,cfg)
     if cfg['telegram'].get('use_cache'):cv_c[k]=nid;sv_cache()
     return nid
    else: return None
  except: pass

  tm=await cl.send_file('me',b,force_document=True,attributes=[types.DocumentAttributeFilename('c.png')])
  di=utils.get_input_document(tm.media.document)
  try:
   await cl(functions.stickers.AddStickerToSetRequest(types.InputStickerSetShortName(pack),types.InputStickerSetItem(di,'💿',keywords='c')))
  except errors.StickersetInvalidError:
   me=await cl.get_me()
   rnd=''.join(random.choices(string.ascii_letters,k=6))
   np=f"em{me.id}_{rnd}"
   lg("PACK",f"Invalid! Creating via Bot: {np}")
   ok = await create_pack_via_bot(f"Music {np}", np, png_bytes)
   if ok:
    c=ld_c();c['telegram']['pack_name']=np;sv_c(c);pack=np
    await inst_p(pack)
    s=await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack),0))
    nid=s.documents[0].id
    s_cld(k,nid,cfg)
    if cfg['telegram'].get('use_cache'):cv_c[k]=nid;sv_cache()
    await tm.delete()
    return nid
   await tm.delete(); return None

  await tm.delete()
  await inst_p(pack)
  await asyncio.sleep(2)
  s=await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack),0))
  nid=s.documents[-1].id
  
  s_cld(k,nid,cfg)
  if cfg['telegram'].get('use_cache'):cv_c[k]=nid;sv_cache()
  lg("OK",f"ID: {nid}");return nid
 except Exception as e:lg("ERR",e);return None

async def set_st(eid,cfg):
 if not cfg['telegram'].get('set_status',False):return
 if time.time() < mem['fw']: return
 if not eid:eid=cfg['telegram'].get('off_status_emoji')
 if eid and str(eid).strip() in ['','0']:eid=None
 if mem['last_st']==eid:return
 if mem['last_st_fail'] and time.time() < mem['last_st_fail']: return

 try:
  if eid:await cl(functions.account.UpdateEmojiStatusRequest(types.EmojiStatus(document_id=int(eid))));lg("ST","Set")
  else:await cl(functions.account.UpdateEmojiStatusRequest(types.EmojiStatusEmpty()));lg("ST","Cls")
  mem['last_st']=eid
 except errors.FloodWaitError as e:
  lg("FLOOD",f"Wait {e.seconds}s");mem['fw']=time.time()+e.seconds+5
 except errors.DocumentInvalidError:
  lg("ST_ERR","Doc Invalid (wait sync)");mem['last_st_fail']=time.time()+15
 except Exception as e:lg("ST_ERR",f"{type(e).__name__}: {e}")

async def main():
 try:await cl.start()
 except:sys.exit("❌ Auth")
 lg("BOT",f"Ready (Lib v{telethon.__version__})");last_valid=None
 while 1:
  try:
   cfg=ld_c();curr=g_trk(cfg)
   
   if curr and curr['play']:
    mem['stop_ticks'] = 0
    last_valid = curr
   else:
    mem['stop_ticks'] += 1
   
   final_track = None
   if mem['stop_ticks'] < 4:
    final_track = last_valid
   else:
    final_track = None
   
   tx=""
   if final_track:
    c = final_track
    fn=f"{c['art']} - {c['tit']}"
    if mem['trk']!=fn:
     lg("NP",fn);mem['trk']=fn;im=c['img']
     if not im:im=g_itu(fn)
     if not im:im=g_yam(fn)
     if im:mem['cv_id']=await up_cv(im,fn,cfg)
     else:lg("WARN","No cover");mem['cv_id']=None
     mem['lnk']=f_lnk(c['art'],c['tit'])
    await set_st(mem['cv_id'],cfg)
    tx=cfg['messages']['true_mes'].replace('{name}',c['art']).replace('{title}',c['tit'])
    if '{cover}' in tx:tx=tx.replace('{cover}',f"{{emoji={mem['cv_id']}}}" if mem['cv_id'] else "")
    for s in re.findall(r'\{link_to=(.*?)\}',tx):
     k='yandex' if 'yandex' in s else 'spotify' if 'spotify' in s else 'soundcloud' if 'soundcloud' in s else 'appleMusic' if 'apple' in s else 'youtube' if 'youtube' in s else s
     tx=tx.replace(f'{{link_to={s}}}',mem['lnk'].get(k,"#"))
   else:
    tx=cfg['messages']['false_mes'];mem['trk']=None
    await set_st(None,cfg)
   
   f_txt,ents=parse_hybrid(tx.strip())
   if f_txt!=mem['last_msg']:
    try:await cl.edit_message(cfg['telegram']['cid'],cfg['telegram']['mid'],text=f_txt,formatting_entities=ents,link_preview=False);mem['last_msg']=f_txt;lg("UP","Updated")
    except errors.MessageNotModifiedError:mem['last_msg']=f_txt
    except errors.FloodWaitError as e:lg("MSG_FLOOD",f"{e.seconds}s");await asyncio.sleep(e.seconds)
    except Exception as e:lg("TG_ERR",e)
  except Exception as e:lg("ERR",e)
  await asyncio.sleep(1.2)

with cl:cl.loop.run_until_complete(main())



#              ▓███                  
#            ░█████                  Привет брат, я рад что ты зашёл сюда, данный код был сделан на коленке под двумя
#            ██████                  банками хмельного, пусть и так, но ты же этим заинтересовался, и я очень благодарен тебе! )
#            ██████                  
#            ▒█████                  Контакт для связи и предложений: Telegram @lisurgut.
#             ▒████                  
#                ░░█▓░               Если используешь информацию из данного кода, будь добр - не выставляй за лично своё,
#                  █████░            буду рад если укажешь моё соавторство или хотя бы где то сможешь упомянуть меня как разработчика <3
#                  █████▓            
#                  ██████            ██ █ ███████ ██ █ ██ █████ █ ██████ ██████ █ █████ █ █ ████████ █ ███ █ ██ ██ █████ █ █ ████████ ██
#                  █████▓            █ █ ███ █ █████ ██ ███ █ ███████ ███ █████ █ █████ ██ ███████ ████ █ ██ █ █ █ ████ █ ███ █████ ██ █
#                  █████░            █ █████ ███ ███████ ██ ███ █ █████ █████ ███ █ █████ █ ██ █████ ██████ ██ ███ ████ ███ ███ ██████ █

#                  ██▓░               
