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
LISURGUT_API = "https://lisurgut.ru"

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

def _shift_entity(ent, offset_delta):
    cls = type(ent)
    kwargs = {}
    for field in ('offset', 'length', 'url', 'user_id', 'language', 'document_id', 'custom_emoji_id'):
        if hasattr(ent, field):
            val = getattr(ent, field)
            if field == 'offset':
                val += offset_delta
            kwargs[field] = val
    try:
        return cls(**kwargs)
    except Exception:
        return cls(offset=ent.offset + offset_delta, length=ent.length)


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
    elif e.text.startswith('.find '):
        query = e.text[6:].strip()
        if not query:
            await e.edit("❌ Укажи запрос: `.find artist - title`")
            return
        await e.edit("🔍 Ищу...")
        try:
            r = requests.get(f"{LISURGUT_API}/api/search", params={"q": query, "limit": 8}, timeout=8).json()
            tracks = r.get("tracks", [])
            if not tracks:
                await e.edit(f"😕 Ничего не найдено: `{query}`")
                return

            cfg_now = ld_c()
            pack_name = cfg_now['telegram']['pack_name']
            cover_ids = []
            added_docs = []
            for t in tracks:
                cover_url = t.get("cover")
                doc_id = None
                if cover_url:
                    try:
                        png = await _make_cover_png(cover_url)
                        eid, input_doc = await _cover_to_emoji_id(png, pack_name)
                        doc_id = eid
                        added_docs.append(input_doc)
                    except Exception as ce:
                        lg("FIND_COVER_ERR", str(ce))
                        doc_id = None
                cover_ids.append(doc_id)

            THUMB = "👾"
            tw = len(THUMB.encode("utf-16-le")) // 2

            header = f"🔍 {query}"
            header_t, header_ents = parse_hybrid(header)

            body_parts = []
            body_ents_manual = []
            cur_offset = 0

            for idx, (t, doc_id) in enumerate(zip(tracks, cover_ids)):
                link = f"{LISURGUT_API}/et?artist={urllib.parse.quote(t['artist'])}&title={urllib.parse.quote(t['title'])}"
                line_text, line_ents = parse_hybrid(f"**{idx+1}.** [{t['artist']} — {t['title']}]({link})")

                if doc_id:
                    prefix = THUMB + " "
                    full_line = prefix + line_text
                    body_ents_manual.append(types.MessageEntityCustomEmoji(offset=cur_offset, length=tw, document_id=doc_id))
                    for ent in line_ents:
                        body_ents_manual.append(_shift_entity(ent, cur_offset + tw + 1))
                else:
                    full_line = line_text
                    for ent in line_ents:
                        body_ents_manual.append(_shift_entity(ent, cur_offset))

                body_parts.append(full_line)
                cur_offset += len(full_line.encode("utf-16-le")) // 2
                if idx < len(tracks) - 1:
                    body_parts.append("\n")
                    cur_offset += 1

            body_t = "".join(body_parts)
            nl = "\n"
            full_text = header_t + nl + body_t
            offset_shift = len(header_t.encode("utf-16-le")) // 2 + 1

            final_ents = list(header_ents)
            for ent in body_ents_manual:
                final_ents.append(_shift_entity(ent, offset_shift))

            bq_length = len(body_t.encode("utf-16-le")) // 2
            final_ents.append(types.MessageEntityBlockquote(offset=offset_shift, length=bq_length, collapsed=True))

            await e.edit(full_text, formatting_entities=final_ents, link_preview=False)
            for input_doc in added_docs:
                try:
                    await cl(functions.stickers.RemoveStickerFromSetRequest(sticker=input_doc))
                except Exception:
                    pass
        except Exception as x:
            await e.edit(f"❌ Ошибка: {x}")
    elif e.text == '.np':
        cfg2 = ld_c()
        trk = mem.get('trk')
        cid2 = mem.get('cv_id')
        if not trk:
            await e.edit("🎵 Сейчас ничего не играет")
            return
        cover_part = f"{{emoji:{cid2}}} " if cid2 else ""
        lnk = mem.get('lnk', {})
        lis = lnk.get('lisurgut', '')
        parts = trk.split(' - ', 1)
        artist_np = parts[0] if len(parts) > 1 else trk
        title_np = parts[1] if len(parts) > 1 else trk
        link_txt = f" · [слушать]({lis})" if lis else ""
        txt = f"{cover_part}**{artist_np}** — {title_np}{link_txt}"
        t_parsed, ents = parse_hybrid(txt)
        await e.edit(t_parsed, formatting_entities=ents, link_preview=False)
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


def g_itu(artist, title):
    try:
        lg("API_COVER", f"{artist} - {title}")
        r = requests.get(
            f"{LISURGUT_API}/et/api",
            params={"artist": artist, "title": title},
            timeout=5
        ).json()
        url = r.get("track", {}).get("cover_url")
        if url:
            lg("API_COVER_OK", url)
            return url
        lg("API_COVER_EMPTY", "No cover in response")
    except Exception as e:
        lg("API_COVER_ERR", e)
    return None


def g_yam(artist, title):
    try:
        lg("API_SEARCH", f"{artist} - {title}")
        r = requests.get(
            f"{LISURGUT_API}/api/search",
            params={"q": f"{artist} - {title}", "limit": 1},
            timeout=5
        ).json()
        tracks = r.get("tracks", [])
        if tracks:
            url = tracks[0].get("cover")
            if url:
                lg("API_SEARCH_COVER_OK", url)
                return url
        lg("API_SEARCH_EMPTY", "No results")
    except Exception as e:
        lg("API_SEARCH_ERR", e)
    return None


def f_lnk(a, t):
    d = {}
    fn = f"{a} - {t}"
    lg("LINKS_GEN", f"Generating for: {fn}")
    try:
        r = requests.get(
            f"{LISURGUT_API}/api/search",
            params={"q": fn, "limit": 1},
            timeout=5
        ).json()
        tracks = r.get("tracks", [])
        if tracks:
            tid = tracks[0].get("id")
            if tid:
                detail = requests.get(f"{LISURGUT_API}/api/track/{tid}", timeout=5).json()
                mp3 = detail.get("mp3_url", "")
                if "music.yandex.ru" in mp3 or detail.get("source") == "yandex":
                    clean_id = tid.split("_")[-1] if "_" in str(tid) else tid
                    d['yandex'] = f"https://music.yandex.ru/track/{clean_id}"
                    lg("LINKS_YANDEX", d['yandex'])
    except Exception as e:
        lg("LINKS_YANDEX_ERR", str(e))
    try:
        d['lisurgut'] = f"{LISURGUT_API}/et?artist={urllib.parse.quote(a)}&title={urllib.parse.quote(t)}"
        lg("LINKS_LISURGUT", d['lisurgut'])
    except Exception as e:
        lg("LINKS_LISURGUT_ERR", str(e))
    lg("LINKS_RESULT", str(d))
    return d


def g_cld(k, cfg):
    if not cfg['telegram'].get('use_cloud', False):
        return None
    try:
        r = requests.get(f"{LISURGUT_API}/et/s", timeout=3)
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
        r = requests.post(f"{LISURGUT_API}/et/add", json={"track": k, "emoji_id": str(eid)}, timeout=5)
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
            buf_bot = io.BytesIO(png_bytes)
            buf_bot.name = "s.png"
            upl = await cl.upload_file(buf_bot, file_name="s.png")
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


async def _make_cover_png(url):
    raw = requests.get(url, timeout=10).content
    img = Image.open(io.BytesIO(raw)).convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)
    msk = Image.new('L', (100, 100), 0)
    ImageDraw.Draw(msk).rounded_rectangle((0, 0, 100, 100), radius=25, fill=255)
    img.putalpha(msk)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    return buf.getvalue()


async def _upload_sticker(png_bytes):
    buf = io.BytesIO(png_bytes)
    buf.name = 'cover.png'
    uploaded = await cl.upload_file(buf, file_name='cover.png')
    upl = await cl(functions.messages.UploadMediaRequest(
        peer=types.InputPeerSelf(),
        media=types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type='image/png',
            attributes=[types.DocumentAttributeFilename(file_name='cover.png')]
        )
    ))
    return utils.get_input_document(upl.document)


async def _cover_to_emoji_id(png_bytes, pack_name):
    buf = io.BytesIO(png_bytes)
    buf.name = 'cover.png'
    uploaded = await cl.upload_file(buf, file_name='cover.png')
    upl = await cl(functions.messages.UploadMediaRequest(
        peer=types.InputPeerSelf(),
        media=types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type='image/png',
            attributes=[types.DocumentAttributeFilename(file_name='cover.png')]
        )
    ))
    di = utils.get_input_document(upl.document)
    await cl(functions.stickers.AddStickerToSetRequest(
        stickerset=types.InputStickerSetShortName(pack_name),
        sticker=types.InputStickerSetItem(document=di, emoji='💿', keywords='cover')
    ))
    s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack_name), 0))
    return s.documents[-1].id, utils.get_input_document(s.documents[-1])


async def _ensure_pack(pack, png_bytes):
    try:
        s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
        return s, pack
    except Exception:
        pass
    lg("PACK", f"Pack not found, creating: {pack}")
    ok = await create_pack_via_bot(f"Music {pack}", pack, png_bytes)
    if not ok:
        return None, pack
    await inst_p(pack)
    await asyncio.sleep(2)
    s = await cl(functions.messages.GetStickerSetRequest(types.InputStickerSetShortName(pack), 0))
    return s, pack


async def up_cv(u, k, cfg):
    cid = g_cld(k, cfg)
    if cid:
        lg("CLD", f"Found: {cid}")
        return cid
    if cfg['telegram'].get('use_cache', False) and k in cv_c:
        lg("CV_CACHE", f"Hit: {k} -> {cv_c[k]}")
        return cv_c[k]
    lg("CV", f"Load: {u[:60]}...")
    try:
        png_bytes = await _make_cover_png(u)
        pack = cfg['telegram']['pack_name']
        s, pack = await _ensure_pack(pack, png_bytes)
        if s is None:
            return None

        for doc in list(s.documents):
            try:
                await cl(functions.stickers.RemoveStickerFromSetRequest(
                    sticker=utils.get_input_document(doc)
                ))
                lg("PACK_DEL", f"Removed old sticker {doc.id}")
            except Exception as ex:
                lg("PACK_DEL_ERR", str(ex))
        await asyncio.sleep(1)

        di = await _upload_sticker(png_bytes)
        await cl(functions.stickers.AddStickerToSetRequest(
            stickerset=types.InputStickerSetShortName(pack),
            sticker=types.InputStickerSetItem(document=di, emoji='💿', keywords='cover')
        ))
        await asyncio.sleep(1)
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
    me = await cl.get_me()
    _pack_name = f"np{me.id}"
    cfg = ld_c()
    if cfg['telegram'].get('pack_name', '') != _pack_name:
        cfg['telegram']['pack_name'] = _pack_name
        sv_c(cfg)
        lg("PACK_NAME", f"Set pack name: {_pack_name}")
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
                    im = g_itu(c['art'], c['tit']) or g_yam(c['art'], c['tit'])
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
