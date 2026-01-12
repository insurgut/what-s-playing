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


import configparser, asyncio, sys, requests, re, io, urllib.parse, json, os, time, threading, logging, random, string
from flask import Flask, request, jsonify
import telethon
from telethon import TelegramClient, functions, types, errors, events, utils
from telethon.extensions import html
from PIL import Image, ImageDraw
from yandex_music import Client as YMClient

CFG = 'config.json'
CV = 'covers_cache.json'

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

DEF_CFG = {
    "telegram": {
        "api_id": 0,
        "api_hash": "",
        "cid": 0,
        "mid": 0,
        "cocid": 0,
        "comid": 0,
        "pack_name": "music_covers_v1",
        "cmd": ".mul",
        "set_status": True,
        "off_status_emoji": "0",
        "use_cache": True,
        "use_cloud": True,
        "link_preview": True
    },
    "messages": {
        "false_mes": "{emoji:5890937586544807413} Музыка на паузе",
        # Vars: {name}, {title}, {cover}, {link_to:yandex}, {link_to:lisurgut}
        "true_mes": (
            "<blockquote>{emoji:5915480455603295660} Сейчас играет:</blockquote>\n"
            "<blockquote>{cover} {name} • {title}</blockquote>\n"
            "<blockquote>{emoji:5346296430166293639} <a href=\"{link_to:lisurgut}\">О треке</a></blockquote>\n"
            "<blockquote>{link_to:lisurgut}</blockquote>"
        )
    },
    "lastfm": {
        "api_key": "",
        "username": ""
    },
    "yandex": {
        "token": ""
    }
}


def ld_c():
    if not os.path.exists(CFG):
        print("⚠️ Config not found. Creating new...")
        json.dump(DEF_CFG, open(CFG, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        return DEF_CFG
    try:
        return json.load(open(CFG, encoding='utf-8'))
    except:
        return DEF_CFG


def sv_c(d):
    json.dump(d, open(CFG, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


HTML = """body{background:#0d0d0d;color:#ccc;font-family:'Consolas',monospace;padding:20px;display:flex;flex-direction:column;align-items:center}.box{width:100%;max-width:700px}.sec{color:#555;font-size:10px;text-transform:uppercase;margin:25px 0 5px 0;letter-spacing:1px;border-bottom:1px solid #222}.row{display:flex;align-items:center;background:#161616;padding:8px;border-radius:6px;margin-bottom:2px}.tag{background:#252525;color:#888;padding:4px 8px;border-radius:4px;font-size:12px;margin-right:10px;white-space:nowrap;min-width:120px}.val{background:none;border:none;color:#ddd;font-family:inherit;font-size:13px;width:100%;outline:none}.val:focus{color:#fff}.masked{cursor:pointer;color:#666;font-style:italic}.masked:hover{color:#888}.desc{font-size:11px;color:#444;margin-bottom:8px;margin-left:5px;font-style:italic}.sw{position:relative;width:34px;height:18px}.sw input{opacity:0;width:0;height:0}.sl{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#333;border-radius:18px;transition:.3s}.sl:before{position:absolute;content:"";height:14px;width:14px;left:2px;bottom:2px;background:#777;border-radius:50%;transition:.3s}input:checked+.sl{background:#2ea043}input:checked+.sl:before{transform:translateX(16px);background:#fff}let d={};const S=['api_hash','token','api_key'];const DESCS={'api_id':'Telegram APP ID (my.telegram.org)','cid':'Target Channel/Group ID (-100...)','mid':'Message ID to edit (Integer)','cocid':'Config Channel ID','comid':'Config Message ID','cmd':'Command to forward status','set_status':'Update User Profile Emoji Status?','off_status_emoji':'Emoji ID when paused (0 to clear)','true_mes':'Vars: {name}, {title}, {cover}, {link_to:yandex}, {link_to:lisurgut}','token':'Yandex Music Token (y0\\_...)','link_preview':'Enable link previews (OG)?'};async function L(){d=await(await fetch('/g')).json();R()}function R(){let h=document.getElementById('c');h.innerHTML='';for(let s in d){let sh=document.createElement('div');sh.className='sec';sh.innerText=s;h.appendChild(sh);for(let k in d[s]){let r=document.createElement('div');r.className='row';let t=document.createElement('div');t.className='tag';t.innerText=k;r.appendChild(t);let v=d[s][k];if(typeof v==='boolean'){let l=document.createElement('label');l.className='sw';let cb=document.createElement('input');cb.type='checkbox';cb.checked=v;cb.onchange=(e)=>{d[s][k]=e.target.checked;Szv()};let sl=document.createElement('span');sl.className='sl';l.append(cb,sl);r.appendChild(l)}else if(S.includes(k)&&String(v).length>10){let sp=document.createElement('span');sp.className='masked';sp.innerText=String(v).substr(0,5)+'...'+String(v).substr(-5);sp.onclick=()=>{let i=document.createElement('input');i.className='val';i.value=v;i.onblur=()=>{d[s][k]=i.value;Szv();R()};sp.replaceWith(i);i.focus()};r.appendChild(sp)}else{let i=document.createElement('input');i.className='val';i.value=v;i.oninput=(e)=>{d[s][k]=isNaN(e.target.value)?e.target.value:Number(e.target.value)};if(typeof v==='string')i.oninput=(e)=>{d[s][k]=e.target.value};i.onblur=()=>Szv();r.appendChild(i)}h.appendChild(r);if(DESCS[k]){let ds=document.createElement('div');ds.className='desc';ds.innerText=DESCS[k];h.appendChild(ds)}}}}async function Szv(){await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})}L();"""


@app.route('/g')
def g():
    return jsonify(ld_c())


@app.route('/', methods=['GET', 'POST'])
def i():
    if request.method == 'POST':
        sv_c(request.json)
        return 'OK'
    return HTML


def rf():
    app.run(host='0.0.0.0', port=41720, use_reloader=False)


def lg(t, m):
    print(f"[{time.strftime('%H:%M:%S')}] {t} {m}")


threading.Thread(target=rf, daemon=True).start()
print("🔗 UI: http://127.0.0.1:41720")

try:
    cfg = ld_c()
    if re.search(r'{.+=.+?}', str(cfg['messages'])):
        lg("CONFIG", "Old config format detected. Auto-updating...")
        for key, value in cfg['messages'].items():
            if isinstance(value, str):
                cfg['messages'][key] = re.sub(r'{(.*?)=(.*?)}', r'{\1:\2}', value)
        sv_c(cfg)
        lg("CONFIG", "Config updated to new format!")
except Exception as e:
    lg("MIGRATION_ERR", e)

while True:
    c = ld_c()
    try:
        if c['telegram']['api_id'] and c['telegram']['api_hash']:
            break
    except:
        pass
    print("⏳ Waiting for config... Fill it at http://127.0.0.1:41720")
    time.sleep(5)

AID, AHS = c['telegram']['api_id'], c['telegram']['api_hash']
cl = TelegramClient('session', AID, AHS)
ym = YMClient(token=c['yandex']['token']) if c['yandex']['token'] else YMClient()

mem = {
    'trk': None,
    'lnk': {},
    'cv_id': None,
    'last_msg': '',
    'stop_ticks': 0,
    'last_st': None,
    'fw': 0,
    'last_st_fail': 0
}

cv_c = json.load(open(CV, encoding='utf-8')) if os.path.exists(CV) else {}


def sv_cache():
    json.dump(cv_c, open(CV, 'w', encoding='utf-8'), ensure_ascii=False)


def u16(s):
    return len(s.encode('utf-16-le')) // 2

from telethon.extensions import markdown

def parse_hybrid(txt: str):
    lg("PARSE_IN", f"Input text: {repr(txt)}")
    
    if not txt:
        return txt, []

    def repl_triple_quote(m):
        return f"<blockquote>{m.group(1)}</blockquote>"
    txt = re.sub(r'"""(.*?)"""', repl_triple_quote, txt, flags=re.DOTALL)

    txt = re.sub(r'(?<!")\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', txt)
    txt = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', txt)
    txt = re.sub(r'__([^_]+)__', r'<i>\1</i>', txt)
    txt = re.sub(r'(?m)^>\s+(.*)$', r'<blockquote>\1</blockquote>', txt)

    def repl_emoji(m):
        eid = m.group(1)
        return f'<a href="emoji/{eid}">👾</a>'
    txt = re.sub(r'{emoji:(\d+)}', repl_emoji, txt)

    text, entities = html.parse(txt)
    
    for i, e in enumerate(entities):
        if isinstance(e, types.MessageEntityTextUrl):
            url = getattr(e, 'url', '')
            if url.startswith("emoji/"):
                try:
                    eid = int(url.split("/", 1)[1])
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, eid)
                except Exception:
                    continue

    return text, entities

@cl.on(events.NewMessage(outgoing=True))
async def h_cmd(e):
    cfg = ld_c()
    if not e.text:
        return
    if e.text == cfg['telegram']['cmd']:
        await e.delete()
        try:
            await cl.forward_messages(e.chat_id, cfg['telegram']['mid'], cfg['telegram']['cid'])
        except Exception as x:
            lg("CMD", x)
    elif e.text == '.test':
        await e.edit("🔄 Check...", parse_mode='html')
        p = cfg['telegram']['pack_name']
        try:
            s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(p), 0))
            if not s.documents:
                await e.edit(f"❌ Empty: {p}")
                return
            m = f"📦 {p}\n"
            for d in s.documents[-3:]:
                m += f"🆔 {d.id}: {{emoji:{d.id}}}\n"
            t, en = parse_hybrid(m)
            await e.edit(t, formatting_entities=en, link_preview=True)
        except Exception as x:
            await e.edit(f"Err: {x}")
    elif e.text.startswith('.em '):
        try:
            await e.delete()
            t = "👾"
            i = int(e.text.split()[1])
            await cl.send_message(e.chat_id, t, formatting_entities=[types.MessageEntityCustomEmoji(0, u16(t), i)])
        except:
            pass
    elif e.text == '.id':
        await e.edit(f"✅ Chat ID for config: `{e.chat_id}`")


def g_trk(cfg):
    try:
        if not cfg.get('lastfm', {}).get('username') or not cfg.get('lastfm', {}).get('api_key'):
            return None
        r = requests.get(
            f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={cfg['lastfm']['username']}&api_key={cfg['lastfm']['api_key']}&format=json&limit=1",
            timeout=2
        ).json()
        track_data = r.get('recenttracks', {}).get('track')
        if not track_data:
            return None
        t = track_data[0] if isinstance(track_data, list) else track_data
        is_playing = t.get('@attr', {}).get('nowplaying') == 'true'
        artist = t.get('artist', {}).get('#text', 'Unknown Artist')
        title = t.get('name', 'Unknown Track')
        lg("LASTFM", f"Got track: play={is_playing}, art={artist}, tit={title}")
        return {'play': is_playing, 'art': artist, 'tit': title, 'img': None}
    except Exception as e:
        lg("LASTFM_ERR", f"An error occurred in g_trk: {e}")
        return None


def g_itu(q):
    try:
        lg("ITUNES_Q", q)
        r = requests.get(
            f"https://itunes.apple.com/search?term={urllib.parse.quote(q)}&entity=song&limit=1",
            timeout=2
        ).json()
        if r.get('resultCount', 0) > 0 and r.get('results'):
            url = r['results'][0]['artworkUrl100'].replace('100x100', '600x600')
            lg("ITUNES_OK", url)
            return url
        lg("ITUNES_EMPTY", "No results")
    except Exception as e:
        lg("ITUNES_ERR", e)
    return None


def g_yam(q):
    try:
        lg("YAM_Q", q)
        s = ym.search(q)
        if s.best and s.best.type == 'track' and s.best.result:
            url = "https://" + s.best.result.cover_uri.replace('%%', '400x400')
            lg("YAM_OK", url)
            return url
        lg("YAM_EMPTY", "No best track")
    except Exception as e:
        lg("YAM_ERR", e)
    return None


def f_lnk(a, t):
    d = {}
    fn = f"{a} - {t}"
    lg("LINKS_GEN", f"Generating for: {fn}")
    try:
        s = ym.search(fn)
        track = s.best.result if s.best and s.best.type == 'track' else None
        if track and track.albums:
            try:
                album_id = track.albums[0].id
                url = f"https://music.yandex.ru/album/{album_id}/track/{track.id}"
                d['yandex'] = url
                lg("LINKS_YANDEX", f"Found: {url}")
            except Exception as e:
                lg("LINKS_YANDEX_ID_ERR", str(e))
        else:
            lg("LINKS_YANDEX", "No track/albums found")
    except Exception as e:
        lg("LINKS_YANDEX_ERR", str(e))
    try:
        url = (
            "https://lisurgut.ru/et"
            f"?artist={urllib.parse.quote(a)}"
            f"&title={urllib.parse.quote(t)}"
        )
        d['lisurgut'] = url
        lg("LINKS_LISURGUT", f"Generated: {url}")
    except Exception as e:
        lg("LINKS_LISURGUT_ERR", str(e))
    lg("LINKS_RESULT", str(d))
    return d


def g_cld(k, cfg):
    if not cfg['telegram'].get('use_cloud', False):
        return None
    try:
        r = requests.get("https://api.lisurgut.ru/et/s", timeout=3)
        if r.status_code == 200:
            data = r.json()
            for item in data:
                if item.get('track') == k:
                    eid = item.get('emoji_id')
                    lg("SCL", f"Found: {eid}")
                    return eid
        return None
    except Exception as e:
        lg("SCL", f"ERR: {e}")
        return None


def s_cld(k, eid, cfg):
    if not cfg['telegram'].get('use_cloud', False):
        return
    try:
        r = requests.post("https://api.lisurgut.ru/et/add", json={"track": k, "emoji_id": str(eid)}, timeout=5)
        lg("SCL", f"Add: {r.status_code}")
    except Exception as e:
        lg("SCL", f"Add ERR: {e}")


async def inst_p(p):
    try:
        await cl(functions.messages.InstallStickerSetRequest(types.InputStickerSetShortName(p), False))
        lg("PACK_INST", p)
    except Exception as e:
        lg("PACK_INST_ERR", str(e))


async def create_pack_via_bot(title, name, png_bytes):
    lg("BOT_CHAT", "Starting pack creation via @Stickers...")
    try:
        async with cl.conversation("@Stickers", timeout=30) as conv:
            await conv.send_message("/cancel")
            await asyncio.sleep(0.5)
            await conv.send_message("/newemojipack")
            r = await conv.get_response()
            if r.buttons:
                done = False
                for row in r.buttons:
                    for btn in row:
                        if "Static" in btn.text:
                            await btn.click()
                            done = True
                            break
                    if done:
                        break
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
            lg("BOT_CHAT_DONE", r.text)
            return "Kaboom" in r.text
    except Exception as e:
        lg("BOT_CHAT_ERR", f"Err: {e}")
        try:
            await cl.delete_dialog("@Stickers")
        except:
            pass
        return False


async def up_cv(u, k, cfg):
    cid = g_cld(k, cfg)
    if cid:
        lg("CLD", f"Found: {cid}")
        return cid
    if cfg['telegram'].get('use_cache', False) and k in cv_c:
        lg("CV_CACHE", f"Hit: {k} -> {cv_c[k]}")
        return cv_c[k]
    lg("CV", f"Load: {u[:60]}...")
    b = io.BytesIO()
    try:
        i = Image.open(io.BytesIO(requests.get(u).content)).convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)
        msk = Image.new('L', (100, 100), 0)
        ImageDraw.Draw(msk).rounded_rectangle((0, 0, 100, 100), radius=25, fill=255)
        i.putalpha(msk)
        i.save(b, 'PNG')
        b.seek(0)
        b.name = "c.png"
        png_bytes = b.getvalue()
        if not os.path.exists('local_covers'):
            os.makedirs('local_covers')
        safe_k = "".join([c for c in k if c.isalpha() or c.isdigit() or c in (' ', '-')]).rstrip()
        with open(os.path.join('local_covers', f'{safe_k}.png'), 'wb') as f:
            f.write(png_bytes)
        b.seek(0)
        pack = cfg['telegram']['pack_name']
        try:
            s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
            lg("PACK_INFO", f"{pack}: {len(s.documents)} docs")
            if len(s.documents) >= 100:
                me = await cl.get_me()
                rnd = ''.join(random.choices(string.ascii_letters, k=6))
                np = f"em{me.id}_{rnd}"
                lg("PACK", f"Full! Creating via Bot: {np}")
                ok = await create_pack_via_bot(f"Music {np}", np, png_bytes)
                if ok:
                    c = ld_c()
                    c['telegram']['pack_name'] = np
                    sv_c(c)
                    pack = np
                    await inst_p(pack)
                    s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
                    nid = s.documents[0].id
                    s_cld(k, nid, cfg)
                    if cfg['telegram'].get('use_cache'):
                        cv_c[k] = nid
                        sv_cache()
                    return nid
                else:
                    return None
        except Exception as e:
            lg("PACK_INFO_ERR", str(e))
        tm = await cl.send_file('me', b, force_document=True,
                                attributes=[types.DocumentAttributeFilename('c.png')])
        di = utils.get_input_document(tm.media.document)
        try:
            await cl(functions.stickers.AddStickerToSetRequest(
                types.InputStickerSetShortName(pack),
                types.InputStickerSetItem(di, '💿', keywords='c')
            ))
        except errors.StickersetInvalidError:
            me = await cl.get_me()
            rnd = ''.join(random.choices(string.ascii_letters, k=6))
            np = f"em{me.id}_{rnd}"
            lg("PACK", f"Invalid! Creating via Bot: {np}")
            ok = await create_pack_via_bot(f"Music {np}", np, png_bytes)
            if ok:
                c = ld_c()
                c['telegram']['pack_name'] = np
                sv_c(c)
                pack = np
                await inst_p(pack)
                s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
                nid = s.documents[0].id
                s_cld(k, nid, cfg)
                if cfg['telegram'].get('use_cache'):
                    cv_c[k] = nid
                    sv_cache()
                await tm.delete()
                return nid
            await tm.delete()
            return None
        await tm.delete()
        await inst_p(pack)
        await asyncio.sleep(2)
        s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
        nid = s.documents[-1].id
        s_cld(k, nid, cfg)
        if cfg['telegram'].get('use_cache'):
            cv_c[k] = nid
            sv_cache()
        lg("CV_OK", f"ID: {nid}")
        return nid
    except Exception as e:
        lg("CV_ERR", e)
        return None


async def set_st(eid, cfg):
    if not cfg['telegram'].get('set_status', False):
        return
    if time.time() < mem['fw']:
        return
    if not eid:
        eid = cfg['telegram'].get('off_status_emoji')
    if eid and str(eid).strip() in ['', '0']:
        eid = None
    if mem['last_st'] == eid:
        return
    if mem['last_st_fail'] and time.time() < mem['last_st_fail']:
        return
    try:
        if eid:
            await cl(functions.account.UpdateEmojiStatusRequest(types.EmojiStatus(document_id=int(eid))))
            lg("ST", f"Set {eid}")
        else:
            await cl(functions.account.UpdateEmojiStatusRequest(types.EmojiStatusEmpty()))
            lg("ST", "Cleared")
        mem['last_st'] = eid
    except errors.FloodWaitError as e:
        lg("FLOOD", f"Wait {e.seconds}s")
        mem['fw'] = time.time() + e.seconds + 5
    except errors.DocumentInvalidError:
        lg("ST_ERR", "Doc Invalid (wait sync)")
        mem['last_st_fail'] = time.time() + 15
    except Exception as e:
        lg("ST_ERR", f"{type(e).__name__}: {e}")


async def config_watcher(last_known_text):
    cfg = ld_c()
    cocid, comid = cfg['telegram'].get('cocid', 0), cfg['telegram'].get('comid', 0)
    if not (cocid and comid):
        return last_known_text
    try:
        msg = await cl.get_messages(cocid, ids=comid)
        if not msg or not msg.text or msg.text == last_known_text['text']:
            return last_known_text
        lg("CONFIG", "Change detected, verifying...")
        lg("CONFIG_WAS", f"\n{last_known_text['text']}")
        lg("CONFIG_GOT", f"\n{msg.text}")
        match = re.search(r"```(?:json)?\n(.+?)\s*```", msg.text, re.DOTALL)
        if not match:
            lg("CONFIG_ERR", "Could not find JSON block, reverting.")
            try:
                await msg.edit(last_known_text['text'])
            except errors.MessageNotModifiedError:
                pass
            try:
                await msg.react('👎')
            except Exception:
                pass
            return last_known_text
        try:
            new_data = json.loads(match.group(1))
            sv_c(new_data)
            lg("CONFIG", "Successfully saved via polling!")
            try:
                await msg.react('👍')
            except Exception:
                pass
            return {'text': msg.text}
        except Exception as x:
            lg("CONFIG_ERR", f"Failed to parse JSON, reverting! Err: {x}")
            try:
                await msg.edit(last_known_text['text'])
            except errors.MessageNotModifiedError:
                pass
            try:
                await msg.react('👎')
            except Exception:
                pass
            return last_known_text
    except Exception as e:
        lg("CONFIG_POLL_ERR", f"Error checking config message: {e}")
        return last_known_text


async def main():
    try:
        await cl.start()
    except:
        sys.exit("❌ Auth")
    cfg = ld_c()
    cocid, comid = cfg['telegram'].get('cocid', 0), cfg['telegram'].get('comid', 0)
    initial_text = ""
    if cocid and comid:
        lg("CONFIG", f"Starting config sync for message {comid} in chat {cocid}")
        initial_text = f"```json\n{json.dumps(cfg, indent=4, ensure_ascii=False)}\n```"
        try:
            await cl.edit_message(cocid, comid, initial_text)
        except Exception as e:
            lg("CONFIG_SYNC_ERR", f"Initial sync failed: {e}")
    last_known_text = {'text': initial_text}
    lg("BOT", f"Ready (Lib v{telethon.__version__})")
    last_valid = None
    while 1:
        last_known_text = await config_watcher(last_known_text)
        try:
            cfg = ld_c()
            curr = g_trk(cfg)
            if curr and curr['play']:
                mem['stop_ticks'] = 0
                last_valid = curr
            else:
                mem['stop_ticks'] += 1
            final_track = last_valid if mem['stop_ticks'] < 4 else None

            if final_track:
                c = final_track
                fn = f"{c['art']} - {c['tit']}"
                if mem['trk'] != fn:
                    lg("NP", fn)
                    mem['trk'] = fn
                    im = g_itu(fn) or g_yam(fn)
                    mem['cv_id'] = await up_cv(im, fn, cfg) if im else None
                    if not im:
                        lg("WARN", "No cover")
                    mem['lnk'] = f_lnk(c['art'], c['tit'])

                await set_st(mem['cv_id'], cfg)

                tx = cfg['messages']['true_mes']
                lg("TX_TEMPLATE", repr(tx))
                lg("TX_LINKS_DICT", str(mem['lnk']))

                # ссылки
                for s in re.findall(r'{link_to:(.*?)}', tx):
                    k = 'yandex' if s == 'yandex' else 'lisurgut' if s == 'lisurgut' else None
                    if k and k in mem['lnk']:
                        replacement = mem['lnk'][k]
                        tx = tx.replace(f'{{link_to:{s}}}', replacement)
                        lg("TX_REPLACE_LINK", f"{s} -> {replacement}")
                    else:
                        lg("TX_REPLACE_LINK_MISSING", f"{s} not in links: {mem['lnk']}")

                lg("TX_AFTER_LINKS", repr(tx))

                # текст
                tx = tx.replace('{name}', c['art']).replace('{title}', c['tit'])
                lg("TX_AFTER_TEXT", repr(tx))

                # обложка
                if '{cover}' in tx:
                    cover_emoji = f"{{emoji:{mem['cv_id']}}}" if mem['cv_id'] else ""
                    tx = tx.replace('{cover}', cover_emoji)
                    lg("TX_AFTER_COVER", repr(tx))
                else:
                    lg("TX_NO_COVER_PLACEHOLDER", "No {cover} in template")
            else:
                tx = cfg['messages']['false_mes']
                lg("TX_FALSE", repr(tx))
                mem['trk'] = None
                await set_st(None, cfg)

            tx = tx.strip()
            lg("TX_BEFORE_PARSE", repr(tx))
            f_txt, ents = parse_hybrid(tx)
            lg("TX_PARSED", f"text={repr(f_txt[:200])}..., ents={len(ents)}")

            if f_txt != mem['last_msg']:
                try:
                    lg("EDIT_ATTEMPT", f"cid={cfg['telegram']['cid']}, mid={cfg['telegram']['mid']}, preview={cfg['telegram'].get('link_preview', True)}")
                    await cl.edit_message(
                        cfg['telegram']['cid'],
                        cfg['telegram']['mid'],
                        text=f_txt,
                        formatting_entities=ents,
                        link_preview=cfg['telegram'].get('link_preview', True)
                    )
                    mem['last_msg'] = f_txt
                    lg("UP", "Updated")
                except errors.MessageNotModifiedError:
                    mem['last_msg'] = f_txt
                    lg("UP_SKIPPED", "MessageNotModified")
                except errors.FloodWaitError as e:
                    lg("MSG_FLOOD", f"{e.seconds}s")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    lg("TG_ERR", e)
        except Exception as e:
            lg("ERR", e)
        await asyncio.sleep(1)


with cl:
    cl.loop.run_until_complete(main())




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

