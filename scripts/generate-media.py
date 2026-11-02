# Generates the sample marketing images in assets/media with the OpenAI Images API.
# Usage: OPENAI_API_KEY=... python3 scripts/generate-media.py <output-dir> [names...]
import json, os, sys, base64, urllib.request, concurrent.futures as cf
out = sys.argv[1]
BRAND = ("Brand: LeadAIO, an AI Optimization company. Visual style: pure black background, bold white sans-serif type "
         "(geometric grotesque), signature gold #D6AE4B highlight, small accents of electric blue #3D6BFF, mint #00E59B and hot pink #FF2E7E. "
         "The wordmark is 'LeadAIO' with 'Lead' in white and 'AIO' in yellow. Subtle black-and-white tech texture (neural network lines or circuit traces). "
         "Premium enterprise B2B look, clean grid, generous spacing. All text must be spelled exactly as given; no other text.")
P = {
 "logo-concepts": ("1536x1024", "A brand identity presentation board showing three logo concepts for 'LeadAIO' on black, arranged in three columns, each labeled small 'Concept A', 'Concept B', 'Concept C'. A: clean wordmark. B: wordmark with a minimal answer-bubble icon. C: monogram 'L' with a cursor/spark. Below, a row of color swatches: black, white, yellow #FFD60A, blue #3D6BFF, mint #00E59B, pink #FF2E7E. " + BRAND),
 "linkedin-ad-1": ("1024x1024", "Square LinkedIn sponsored ad. Big headline: 'Is AI recommending your competitors?' Subline: 'Get found, cited and recommended by ChatGPT, Gemini and Perplexity.' Yellow button: 'Get your AI visibility audit'. LeadAIO wordmark at the bottom left. Background: dark neural network texture. " + BRAND),
 "linkedin-ad-2": ("1024x1024", "Square LinkedIn sponsored ad. Huge headline in two lines: 'Be the answer.' with 'answer' in yellow. Below a mock AI chat answer card citing 'LeadAIO [1]'. Small line: 'AI Optimization for enterprise brands'. LeadAIO wordmark at bottom. " + BRAND),
 "facebook-ad": ("1024x1536", "Vertical 4:5 Facebook feed ad. Headline: 'Search changed. Has your brand?' Three stacked labeled tiles: 'AIO', 'GEO', 'AEO' in blue, mint and pink outlines. Yellow button: 'Book a demo'. LeadAIO wordmark at top. " + BRAND),
 "webinar": ("1536x1024", "Webinar promo banner. Small label 'LIVE WEBINAR'. Title: 'Winning the AI Answer'. Subtitle: 'How enterprise brands get cited by ChatGPT, Gemini and Perplexity'. A yellow 'Register now' button. Right side: wireframe globe with data streams in white lines. LeadAIO wordmark top left. " + BRAND),
 "deck-cover": ("1536x1024", "Title slide of a sales presentation, 16:9. Large title: 'AI Optimization for the Enterprise'. Subtitle: 'Product overview'. LeadAIO wordmark bottom left. Right half: abstract glowing neural network in white. Thin yellow rule under the title. " + BRAND),
 "report-cover": ("1024x1536", "Cover of a research report, portrait. Small label 'LEADAIO RESEARCH'. Title: 'The State of AI Search Visibility'. Subtitle: 'How AI platforms choose which brands to recommend'. A bold abstract bar chart in yellow, blue, mint and pink rising from the bottom. LeadAIO wordmark at the bottom. " + BRAND),
 "website-mockup": ("1536x1024", "Photorealistic laptop on a dark desk showing a website homepage. On screen: black website with nav, big headline 'Make your brand the answer AI gives.' with 'the answer' in yellow, a yellow button 'Get your AI visibility audit', and a mock AI answer card. Moody studio lighting, black and white environment so only the screen has color. " + BRAND),
 "launch-graphic": ("1536x1024", "Social media launch announcement graphic. Small label 'INTRODUCING'. Giant LeadAIO wordmark centered. Below: 'The AI Optimization company for enterprise brands.' Abstract circuit traces radiating outward in white with a few yellow sparks. " + BRAND),
 "one-pager": ("1024x1536", "A printed one-page product sheet lying on a black surface, portrait. Header with LeadAIO wordmark. Title: 'AIO, GEO and AEO in one program'. Three columns with headings 'Measure', 'Optimize', 'Prove' and short gray placeholder text lines. A yellow highlight box at the bottom: 'Book your AI visibility audit'. " + BRAND),
}
def gen(name):
    size, prompt = P[name]
    body = json.dumps({"model":"gpt-image-2","prompt":prompt,"size":size,"quality":"high","n":1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
          headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    try: d = json.load(urllib.request.urlopen(req, timeout=500))
    except urllib.error.HTTPError as e: return name, "ERROR " + e.read().decode()[:300]
    except Exception as e: return name, "ERROR " + str(e)
    open(f"{out}/{name}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"]))
    return name, "ok"
names = sys.argv[2:] or list(P)
with cf.ThreadPoolExecutor(5) as ex:
    for n, r in ex.map(gen, names): print(n, r, flush=True)
