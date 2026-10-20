# Generates the black-and-white background images with the OpenAI Images API.
# Usage: OPENAI_API_KEY=... python3 scripts/generate-images.py <output-dir>
# Then convert to grayscale JPEG (max 1600px) into assets/.
import json, os, sys, base64, urllib.request, concurrent.futures as cf
out = sys.argv[1]
STYLE = ("Black and white monochrome photograph style, pure black background, high contrast, cinematic, "
         "fine detail, subtle film grain, no color, no text, no logos, no people, plenty of dark negative space")
P = {
 "hero":   "Abstract visualization of a glowing neural network: thousands of tiny white nodes connected by thin luminous lines forming a vast 3D constellation that fades into darkness, depth of field. " + STYLE,
 "globe":  "A wireframe Earth globe made of thin white latitude and longitude lines and sparkling data points, orbit rings around it, floating in black space, data streams flowing toward it. " + STYLE,
 "circuit":"Extreme macro shot of a computer chip and circuit board traces, silver metallic lines and solder pads, shallow depth of field, dramatic side lighting. " + STYLE,
 "server": "Long symmetrical corridor of data center server racks with tiny white indicator lights receding into darkness, moody, architectural perspective. " + STYLE,
}
def gen(name):
    body = json.dumps({"model":"gpt-image-2","prompt":P[name],"size":"1536x1024","quality":"medium","n":1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
          headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        return name, "ERROR " + e.read().decode()[:400]
    open(f"{out}/{name}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"]))
    return name, "ok"
with cf.ThreadPoolExecutor(4) as ex:
    for n, r in ex.map(gen, P): print(n, r)
