"""Gera a página de links "Jogos ZAP" (index.html + icones/) a partir de jogos.json.

Para acrescentar um jogo que ficou público: adicione uma entrada em jogos.json
({"slug": "<pasta zap-<slug>-roblox>", "nome": ..., "place": <placeId>, "desc": ...}),
rode `python gerar_site.py` e faça commit + push (GitHub Pages publica sozinho).
"""
import html
import json
import os

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
ICONES = os.path.join(BASE, "icones")
os.makedirs(ICONES, exist_ok=True)

jogos = json.load(open(os.path.join(BASE, "jogos.json"), encoding="utf-8"))

for j in jogos:
    origem = os.path.join(HOME, f"zap-{j['slug']}-roblox", "arte", "icone_jogo.png")
    destino = os.path.join(ICONES, f"{j['slug']}.webp")
    if os.path.exists(origem):
        Image.open(origem).convert("RGB").resize((256, 256), Image.LANCZOS).save(destino, "WEBP", quality=82)
    j["tem_icone"] = os.path.exists(destino)


def cartao(j):
    url = f"https://www.roblox.com/games/{j['place']}"
    img = (f'<img src="icones/{j["slug"]}.webp" alt="" width="88" height="88" loading="lazy">'
           if j["tem_icone"] else '<div class="sem">🎮</div>')
    return (f'<a class="jogo" href="{url}" target="_blank" rel="noopener">{img}'
            f'<div class="txt"><b>{html.escape(j["nome"])}</b><span>{html.escape(j["desc"])}</span></div>'
            f'<span class="jogar">Jogar</span></a>')


destaques = [j for j in jogos if j.get("destaque")]
resto = [j for j in jogos if not j.get("destaque")]

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jogos ZAP no Roblox</title>
<meta name="description" content="Todos os jogos ZAP no Roblox, feitos pelo Matheus Nerd.">
<meta property="og:title" content="Jogos ZAP no Roblox">
<meta property="og:description" content="{len(jogos)} jogos com os bichos ZAP. Toque e jogue!">
<style>
:root {{ --fundo:#160a2e; --cartao:#25124a; --borda:#3a1f6e; --texto:#fff; --sub:#c9b8ff; --rosa:#ff3caa; --ciano:#50f0ff; --amarelo:#ffe650; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--fundo); color:var(--texto); font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  background-image:repeating-linear-gradient(0deg, transparent 0 22px, rgba(255,60,170,.12) 22px 24px); }}
main {{ max-width:560px; margin:0 auto; padding:28px 16px 48px; }}
h1 {{ margin:0 0 4px; font-size:30px; line-height:1.1; color:var(--amarelo); text-align:center; text-shadow:0 3px 0 #4a1a80; }}
p.sub {{ margin:0 0 22px; text-align:center; color:var(--sub); font-size:15px; }}
h2 {{ font-size:14px; letter-spacing:.08em; text-transform:uppercase; color:var(--ciano); margin:22px 4px 10px; }}
.jogo {{ display:flex; align-items:center; gap:12px; padding:10px; margin-bottom:10px; background:var(--cartao);
  border:2px solid var(--borda); border-radius:18px; color:inherit; text-decoration:none; transition:transform .1s, border-color .1s; }}
.jogo:hover, .jogo:active {{ transform:scale(1.015); border-color:var(--rosa); }}
.jogo img, .sem {{ width:72px; height:72px; border-radius:14px; flex:none; object-fit:cover; background:#000; }}
.sem {{ display:grid; place-items:center; font-size:32px; }}
.txt {{ flex:1; min-width:0; }}
.txt b {{ display:block; font-size:16px; }}
.txt span {{ display:block; color:var(--sub); font-size:13px; margin-top:3px; }}
.jogar {{ flex:none; background:var(--rosa); color:#fff; font-weight:800; font-size:14px; padding:9px 14px; border-radius:999px; }}
footer {{ margin-top:26px; text-align:center; color:var(--sub); font-size:13px; }}
footer a {{ color:var(--ciano); }}
</style>
</head>
<body>
<main>
<h1>🎮 Jogos ZAP no Roblox</h1>
<p class="sub">{len(jogos)} jogos com os bichos ZAP • toque para jogar</p>
<h2>🔥 Em alta</h2>
{''.join(cartao(j) for j in destaques)}
<h2>Todos os jogos</h2>
{''.join(cartao(j) for j in resto)}
<footer>Novos jogos toda semana • <a href="https://www.instagram.com/matheusnerd_/">@matheusnerd_</a></footer>
</main>
</body>
</html>
"""
open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(pagina)
print("ok", len(jogos), "jogos")
