"""
Zapier Webhook Handler — YouTube Script AI Automation
Author: Sarah Sair | AI & Data Engineer

HOW IT WORKS:
─────────────────────────────────────────────────────
1. Zapier triggers this webhook (via Google Sheets, Notion, Airtable, etc.)
2. This Flask server receives the topic + niche
3. Runs the full AI pipeline
4. Returns the complete script package as JSON
5. Zapier sends results to Google Docs, Notion, Slack, Email, etc.

ZAPIER WORKFLOW SETUP:
─────────────────────────────────────────────────────
Trigger  → New row in Google Sheets (topic + niche columns)
Action 1 → Webhooks by Zapier: POST to http://your-server.com/generate
Action 2 → Google Docs: Create document with script content
Action 3 → Slack: Send notification with title options
Action 4 → Notion: Save full package to database
Action 5 → Gmail: Email you the completed script
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from youtube_script_generator import run_pipeline, research_topic, generate_titles, generate_script, generate_seo_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key-here")


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "YouTube Script AI System",
        "version": "1.0.0"
    }), 200


# ─────────────────────────────────────────────
# MAIN ZAPIER WEBHOOK ENDPOINT
# ─────────────────────────────────────────────

@app.route("/generate", methods=["POST"])
def generate():
    """
    Main endpoint called by Zapier.

    Expected JSON body from Zapier:
    {
        "secret": "your-secret-key-here",
        "topic": "How to Build a RAG Pipeline",
        "niche": "AI and Data Engineering",
        "style": "educational and engaging",
        "title_index": 0
    }

    Returns full script package for Zapier to distribute.
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    # Validate webhook secret
    if data.get("secret") != WEBHOOK_SECRET:
        logger.warning("Unauthorized webhook attempt.")
        return jsonify({"error": "Unauthorized"}), 401

    # Extract parameters
    topic = data.get("topic", "").strip()
    niche = data.get("niche", "General").strip()
    style = data.get("style", "engaging").strip()
    title_index = int(data.get("title_index", 0))

    if not topic:
        return jsonify({"error": "topic is required"}), 400

    logger.info(f"Zapier request received — Topic: {topic} | Niche: {niche}")

    try:
        # Run pipeline steps
        research = research_topic(topic, niche)
        titles = generate_titles(research)

        title_list = titles.get("titles", [topic])
        chosen_title = (
            title_list[title_index]
            if title_index < len(title_list)
            else title_list[0]
        )

        script = generate_script(research, chosen_title, style)
        metadata = generate_seo_metadata(research, chosen_title, script)

        # Build Zapier-friendly response
        response_payload = {
            "status": "success",
            "topic": topic,
            "niche": niche,

            # Titles — Zapier can use these in Google Docs / Notion
            "chosen_title": chosen_title,
            "all_titles": titles.get("titles", []),
            "best_title_recommendation": titles.get("best_title_recommendation", ""),
            "thumbnail_text_options": titles.get("thumbnail_text", []),

            # Full script — goes to Google Docs
            "full_script": script,

            # SEO metadata — goes to YouTube Studio / Notion
            "seo_tags": metadata.get("tags", []),
            "hashtags": metadata.get("hashtags", []),
            "video_chapters": metadata.get("chapters", []),
            "upload_tip": metadata.get("upload_schedule_tip", ""),

            # Research data — goes to Notion database
            "hook_ideas": research.get("hook_ideas", []),
            "key_points": research.get("key_points", []),
            "target_audience": research.get("target_audience", ""),
            "content_type": research.get("content_type", ""),
            "recommended_length": research.get("recommended_length", ""),

            # Formatted for Slack notification
            "slack_summary": f"""
🎬 *New YouTube Script Ready!*
📌 *Topic:* {topic}
🏆 *Title:* {chosen_title}
⏱ *Length:* {research.get('recommended_length', 'TBD')}
📊 *Type:* {research.get('content_type', 'TBD')}
🎯 *Audience:* {research.get('target_audience', 'TBD')}
            """.strip()
        }

        logger.info(f"Pipeline complete — returning payload for: {chosen_title}")
        return jsonify(response_payload), 200

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────────
# QUICK GENERATE ENDPOINT (no auth — for testing)
# ─────────────────────────────────────────────

@app.route("/quick-generate", methods=["POST"])
def quick_generate():
    """
    Quick test endpoint — no secret required.
    Use only in development. Disable in production.
    """
    data = request.get_json()
    topic = data.get("topic", "AI Tools for Beginners")
    niche = data.get("niche", "Technology")

    research = research_topic(topic, niche)
    titles = generate_titles(research)

    return jsonify({
        "topic": topic,
        "titles": titles.get("titles", []),
        "hook_ideas": research.get("hook_ideas", []),
        "key_points": research.get("key_points", [])
    }), 200


# ─────────────────────────────────────────────
# RUN SERVER
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    logger.info(f"Starting Zapier Webhook Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
