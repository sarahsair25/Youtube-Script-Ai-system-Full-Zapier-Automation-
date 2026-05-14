"""
YouTube Script AI System — Full Automation Pipeline
Author: Sarah Sair | AI & Data Engineer
GitHub: github.com/sarahsair25
Portfolio: https://sarah-sair-ai-7044ftv.gamma.site/
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Optional
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = OpenAI(api_key=OPENAI_API_KEY)


# ─────────────────────────────────────────────
# STEP 1 — TOPIC RESEARCH AGENT
# ─────────────────────────────────────────────

def research_topic(topic: str, niche: str) -> dict:
    """
    Uses GPT-4 to research the topic and generate
    angles, hooks, and key talking points.
    """
    logger.info(f"Researching topic: {topic}")

    prompt = f"""
You are a YouTube content strategist specializing in {niche}.

Research this topic and return a structured JSON object:
Topic: {topic}

Return ONLY valid JSON with this structure:
{{
    "topic": "{topic}",
    "niche": "{niche}",
    "hook_ideas": ["hook 1", "hook 2", "hook 3"],
    "key_points": ["point 1", "point 2", "point 3", "point 4", "point 5"],
    "target_audience": "description of who this is for",
    "competitor_angle": "what makes this unique vs existing videos",
    "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "recommended_length": "X-Y minutes",
    "content_type": "tutorial/listicle/story/review/explainer"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    raw = response.choices[0].message.content.strip()

    try:
        research = json.loads(raw)
        logger.info("Topic research complete.")
        return research
    except json.JSONDecodeError:
        logger.warning("JSON parse failed — returning raw text.")
        return {"raw_research": raw, "topic": topic, "niche": niche}


# ─────────────────────────────────────────────
# STEP 2 — TITLE & THUMBNAIL TEXT GENERATOR
# ─────────────────────────────────────────────

def generate_titles(research: dict) -> dict:
    """
    Generates 5 viral YouTube titles and
    3 thumbnail text options based on research.
    """
    logger.info("Generating titles and thumbnail text...")

    prompt = f"""
You are a YouTube title optimization expert.

Based on this research data:
{json.dumps(research, indent=2)}

Generate ONLY valid JSON with this structure:
{{
    "titles": [
        "Title option 1",
        "Title option 2",
        "Title option 3",
        "Title option 4",
        "Title option 5"
    ],
    "thumbnail_text": [
        "Short text option 1 (max 5 words)",
        "Short text option 2 (max 5 words)",
        "Short text option 3 (max 5 words)"
    ],
    "best_title_recommendation": "Title option X — reason why"
}}

Rules:
- Titles must be under 60 characters
- Use numbers, power words, and curiosity gaps
- Thumbnail text must be punchy and bold
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=600
    )

    raw = response.choices[0].message.content.strip()

    try:
        titles = json.loads(raw)
        logger.info("Titles generated successfully.")
        return titles
    except json.JSONDecodeError:
        return {"raw_titles": raw}


# ─────────────────────────────────────────────
# STEP 3 — FULL SCRIPT GENERATOR
# ─────────────────────────────────────────────

def generate_script(research: dict, title: str, style: str = "engaging") -> str:
    """
    Generates a full YouTube script with:
    - Hook (first 30 seconds)
    - Intro
    - Main content sections
    - CTA (Call to Action)
    - Outro
    """
    logger.info(f"Generating full script for: {title}")

    prompt = f"""
You are a professional YouTube scriptwriter.

Write a complete, production-ready YouTube script based on:

Title: {title}
Style: {style}
Research Data: {json.dumps(research, indent=2)}

Format the script exactly like this:

=== HOOK (0:00 - 0:30) ===
[Write an attention-grabbing opening line that stops the scroll]
[Build tension or curiosity]
[Promise what they will learn]

=== INTRO (0:30 - 1:30) ===
[Introduce yourself briefly]
[Establish credibility]
[Preview the video content]
[Ask them to subscribe]

=== SECTION 1: [Title] (1:30 - 4:00) ===
[Main content — explain clearly with examples]
[Use analogies and real-world scenarios]
[Add B-roll suggestions in brackets]

=== SECTION 2: [Title] (4:00 - 7:00) ===
[Continue main content]
[Include data, stats, or stories]

=== SECTION 3: [Title] (7:00 - 10:00) ===
[Key insights and practical takeaways]
[Step-by-step instructions if applicable]

=== CALL TO ACTION (10:00 - 10:30) ===
[Strong CTA — like, comment, subscribe]
[Ask an engagement question for comments]
[Tease next video]

=== OUTRO (10:30 - 11:00) ===
[Wrap up with key message]
[Final motivational line]
[End screen instructions]

=== VIDEO DESCRIPTION (for YouTube) ===
[SEO-optimized description 150-200 words]
[Include timestamps]
[Include relevant hashtags]

Make the script conversational, energetic, and authentic.
Write exactly as it should be spoken on camera.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=2500
    )

    script = response.choices[0].message.content.strip()
    logger.info("Script generated successfully.")
    return script


# ─────────────────────────────────────────────
# STEP 4 — SEO METADATA GENERATOR
# ─────────────────────────────────────────────

def generate_seo_metadata(research: dict, title: str, script: str) -> dict:
    """
    Generates complete SEO metadata package:
    tags, description, chapters, and hashtags.
    """
    logger.info("Generating SEO metadata...")

    prompt = f"""
You are a YouTube SEO expert.

Based on:
Title: {title}
Keywords: {research.get('seo_keywords', [])}
Script excerpt: {script[:500]}

Return ONLY valid JSON:
{{
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"],
    "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5"],
    "chapters": [
        {{"time": "0:00", "title": "Intro"}},
        {{"time": "1:30", "title": "Section 1"}},
        {{"time": "4:00", "title": "Section 2"}},
        {{"time": "7:00", "title": "Section 3"}},
        {{"time": "10:00", "title": "Wrap Up"}}
    ],
    "category": "YouTube category name",
    "language": "English",
    "upload_schedule_tip": "Best day and time to upload for this niche"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600
    )

    raw = response.choices[0].message.content.strip()

    try:
        metadata = json.loads(raw)
        logger.info("SEO metadata generated.")
        return metadata
    except json.JSONDecodeError:
        return {"raw_metadata": raw}


# ─────────────────────────────────────────────
# STEP 5 — OUTPUT SAVER
# ─────────────────────────────────────────────

def save_output(topic: str, research: dict, titles: dict,
                script: str, metadata: dict) -> str:
    """
    Saves the complete output package as a structured JSON file
    and a readable markdown script file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.lower().replace(" ", "_")[:30]

    # Save JSON data package
    json_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_{timestamp}.json")
    full_package = {
        "generated_at": datetime.now().isoformat(),
        "topic": topic,
        "research": research,
        "titles": titles,
        "seo_metadata": metadata,
        "script_preview": script[:200] + "..."
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_package, f, indent=2, ensure_ascii=False)

    # Save readable script as markdown
    md_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_{timestamp}_script.md")
    best_title = titles.get("best_title_recommendation", "Generated Script")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {best_title}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y %I:%M %p')}\n\n")
        f.write(f"**Topic:** {topic}\n\n")
        f.write("---\n\n")
        f.write("## Title Options\n\n")
        for t in titles.get("titles", []):
            f.write(f"- {t}\n")
        f.write("\n---\n\n")
        f.write("## Full Script\n\n")
        f.write(script)
        f.write("\n\n---\n\n")
        f.write("## SEO Tags\n\n")
        tags = metadata.get("tags", [])
        f.write(", ".join(tags))
        f.write("\n\n## Hashtags\n\n")
        hashtags = metadata.get("hashtags", [])
        f.write(" ".join(hashtags))

    logger.info(f"Output saved:\n  JSON: {json_path}\n  Script: {md_path}")
    return md_path


# ─────────────────────────────────────────────
# MAIN PIPELINE RUNNER
# ─────────────────────────────────────────────

def run_pipeline(topic: str, niche: str,
                 style: str = "engaging",
                 preferred_title_index: int = 0) -> str:
    """
    Runs the complete YouTube Script AI Pipeline:
    1. Research topic
    2. Generate titles
    3. Generate full script
    4. Generate SEO metadata
    5. Save output package
    """
    logger.info("=" * 50)
    logger.info("YouTube Script AI System — Starting Pipeline")
    logger.info("=" * 50)

    # Step 1
    research = research_topic(topic, niche)
    time.sleep(1)

    # Step 2
    titles = generate_titles(research)
    title_list = titles.get("titles", [topic])
    chosen_title = (
        title_list[preferred_title_index]
        if preferred_title_index < len(title_list)
        else title_list[0]
    )
    time.sleep(1)

    # Step 3
    script = generate_script(research, chosen_title, style)
    time.sleep(1)

    # Step 4
    metadata = generate_seo_metadata(research, chosen_title, script)
    time.sleep(1)

    # Step 5
    output_path = save_output(topic, research, titles, script, metadata)

    logger.info("=" * 50)
    logger.info("Pipeline Complete!")
    logger.info(f"Output: {output_path}")
    logger.info("=" * 50)

    return output_path


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_pipeline(
        topic="How to Build a RAG Pipeline from Scratch",
        niche="AI and Data Engineering",
        style="educational and engaging",
        preferred_title_index=0
    )
