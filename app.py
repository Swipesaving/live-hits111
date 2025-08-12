from flask import Flask, request, jsonify
import os, requests, time

app = Flask(__name__)

# Basic health check
@app.get("/")
def home():
    return "Live Hits is running. Try /hits?q=your+keywords"

@app.get("/hits")
def hits():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"ok": False, "error": "Missing ?q=keywords"}), 400

    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        return jsonify({"ok": False, "error": "SERPAPI_KEY not set"}), 500

    # Simple SerpAPI Google News search (last 24h)
    # NOTE: Free trial has limits; this is just a starter.
    params = {
        "engine": "google_news",
        "q": q,
        "api_key": serpapi_key,
        "when": "24h",            # last 24 hours
        "hl": "en",
    }
    r = requests.get("https://serpapi.com/search", params=params, timeout=20)
    data = r.json()

    results = []
    for item in data.get("news_results", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "source": item.get("source"),
            "date": item.get("date"),
        })

    return jsonify({
        "ok": True,
        "query": q,
        "count": len(results),
        "results": results
    })

if __name__ == "__main__":
    # Render will run via gunicorn, but this helps local runs
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
