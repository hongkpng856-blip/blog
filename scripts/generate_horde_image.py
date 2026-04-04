#!/usr/bin/env python3
import sys, time, json, base64, os, requests

API_KEY = "NE_YD0n8eYj84HZ5PDsPdA"
ENDPOINT = "https://aihorde.net/api/v2"

if len(sys.argv) < 4:
    print("Usage: generate_horde_image.py <title> <category> <output_dir>")
    sys.exit(1)

title = sys.argv[1]
category = sys.argv[2]
output_dir = sys.argv[3]

prompt = f"{title}, {category}, blog cover, high quality, 1024x512"
payload = {
    "prompt": prompt,
    "params": {"width": 1024, "height": 512, "steps": 30, "cfg_scale": 7, "sampler_name": "k_euler_a"}
}
headers = {"apikey": API_KEY, "Accept": "application/json", "Content-Type": "application/json"}

# submit job
resp = requests.post(f"{ENDPOINT}/generate/async", headers=headers, json=payload)
if resp.status_code != 200:
    print("Submit failed", resp.status_code, resp.text)
    sys.exit(1)
job = resp.json()
job_id = job.get("id")
if not job_id:
    print("No job id", resp.text)
    sys.exit(1)

# poll until done (max 5 min)
for _ in range(60):
    st = requests.get(f"{ENDPOINT}/generate/status/{job_id}", headers=headers)
    if st.status_code != 200:
        print("Status error", st.status_code)
        sys.exit(1)
    data = st.json()
    if data.get("done"):
        img_b64 = data.get("image")
        if not img_b64:
            print("No image data")
            sys.exit(1)
        img_bytes = base64.b64decode(img_b64)
        safe_title = "_".join(title.split())
        filename = os.path.join(output_dir, f"{safe_title}.jpg")
        os.makedirs(output_dir, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(img_bytes)
        print(f"Saved {filename}")
        sys.exit(0)
    time.sleep(5)
print("Timeout waiting for image")
sys.exit(1)
