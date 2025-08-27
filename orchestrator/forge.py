#!/usr/bin/env python3
import json, argparse, pathlib
from PIL import Image, ImageDraw, ImageFont
BASE = pathlib.Path.cwd().resolve()
TPL_DIR = BASE / "templates"
TEMPLATES = {
  "farm_sim": {
    "title":"AgriSim","colors":{"bg":[18,30,18],"primary":[120,200,120],"accent":[230,200,90]},
    "tick_sec":1.0,"resources":["blé","lait","bois","diesel"],
    "chains":[{"in":{"semences":1},"out":{"blé":1},"time":60},{"in":{"blé":2},"out":{"farine":1},"time":90}],
    "modules":["coop","dealership","sawmill"]
  },
  "transport_tycoon": {
    "title":"TranspoSim","colors":{"bg":[20,22,30],"primary":[120,180,255],"accent":[255,140,90]},
    "tick_sec":0.8,"resources":["passagers","colis","carburant"],
    "chains":[{"in":{"colis":1},"out":{"revenu":100},"time":45}],
    "modules":["dealership"]
  },
  "forestry_manager": {
    "title":"ForestSim","colors":{"bg":[16,24,16],"primary":[100,200,140],"accent":[200,160,80]},
    "tick_sec":1.2,"resources":["grumes","planches","copeaux"],
    "chains":[{"in":{"grumes":2},"out":{"planches":3},"time":120}],
    "modules":["sawmill","coop"]
  }
}
MODULES = {
  "coop":{"description":"Coopérative agricole: ventes groupées","fee_pct":2.0},
  "dealership":{"description":"Concession: achat/vente matériel","markup_pct":8.5},
  "sawmill":{"description":"Scierie grumes→planches","efficiency":1.2}
}
def _spr(path, w,h, bg, fg, label=None):
    img = Image.new("RGBA",(w,h),tuple(bg)+(255,))
    d = ImageDraw.Draw(img); step = max(8, w//16)
    for x in range(0,w,step): d.line((x,0,x,h), fill=tuple(fg)+(40,), width=2)
    if label:
        try:
            font = ImageFont.load_default(); tw,th = d.textsize(label, font=font)
            d.text(((w-tw)//2,(h-th)//2), label, fill=(fg[0],fg[1],fg[2],220), font=font)
        except: pass
    img.save(path)
def generate(template, prompt):
    tpl = TEMPLATES[template]; c=tpl["colors"]; bg=c["bg"]; prim=c["primary"]
    dest = TPL_DIR / template; (dest/"assets").mkdir(parents=True, exist_ok=True)
    _spr(dest/"assets/background.png", 1280,720, bg, prim, tpl["title"][:14])
    spec = {"title":tpl["title"],"tick_sec":tpl["tick_sec"],"resources":tpl["resources"],"chains":tpl["chains"],
            "modules":{k:MODULES[k] for k in tpl["modules"]},"prompt_hint":prompt}
    (dest/"game_spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Spec:", dest/"game_spec.json")
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--template", choices=["farm_sim","transport_tycoon","forestry_manager"], required=True)
    ap.add_argument("--prompt", default="Simulation économique réaliste.")
    a=ap.parse_args(); generate(a.template, a.prompt)
