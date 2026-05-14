# 🎬 YouTube Script AI System — Full Zapier Automation

> **"Stop writing scripts manually. Let AI do it in 60 seconds."**

A production-ready AI pipeline that automatically generates complete YouTube scripts, SEO metadata, titles, and thumbnail text — fully integrated with Zapier for end-to-end automation.

**Built by [Sarah Sair](https://sarah-sair-ai-7044ftv.gamma.site/) | Generative AI & Data Engineer**

---

## 🚀 What This System Does

| Step | What Happens | Tool |
|------|-------------|------|
| 1 | You add a topic to Google Sheets | Google Sheets |
| 2 | Zapier detects new row | Zapier Trigger |
| 3 | Webhook fires the AI pipeline | Flask + GPT-4 |
| 4 | AI researches topic & angles | GPT-4 |
| 5 | AI generates 5 viral title options | GPT-4 |
| 6 | AI writes full production script | GPT-4 |
| 7 | AI generates SEO tags & metadata | GPT-4 |
| 8 | Script saved to Google Docs | Zapier Action |
| 9 | Summary sent to Slack | Zapier Action |
| 10 | Full package saved to Notion | Zapier Action |

---

## 📁 Project Structure

```
youtube-ai-system/
├── src/
│   ├── youtube_script_generator.py   # Core AI pipeline
│   └── zapier_webhook.py             # Flask webhook server
├── outputs/                          # Generated scripts saved here
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
└── README.md                         # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sarahsair25/Youtube-Script-Ai-system-Full-Zapier-Automation-.git
cd youtube-script-ai-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
OPENAI_API_KEY=your-openai-api-key-here
WEBHOOK_SECRET=your-secret-key-here
PORT=5000
```

### 4. Run the Pipeline Locally

```bash
python src/youtube_script_generator.py
```

### 5. Start the Webhook Server

```bash
python src/zapier_webhook.py
```

Server runs at: `http://localhost:5000`

---

## 🔗 Zapier Integration Setup

### Step 1 — Create a Zapier Zap

Go to [zapier.com](https://zapier.com) → **Create Zap**

---

### Step 2 — Set Your Trigger

**App:** Google Sheets
**Event:** New Spreadsheet Row

Your Google Sheet should have these columns:

| topic | niche | style | title_index |
|-------|-------|-------|-------------|
| How to Build a RAG Pipeline | AI Engineering | educational | 0 |
| 10 Python Tips for Beginners | Programming | entertaining | 1 |

---

### Step 3 — Add Webhook Action

**App:** Webhooks by Zapier
**Event:** POST

**URL:**
```
http://your-server-url.com/generate
```

**Payload Type:** JSON

**Data:**
```json
{
  "secret": "your-secret-key-here",
  "topic": "{{topic}}",
  "niche": "{{niche}}",
  "style": "{{style}}",
  "title_index": "{{title_index}}"
}
```

---

### Step 4 — Send Script to Google Docs

**App:** Google Docs
**Event:** Create Document from Text

**Document Name:**
```
{{chosen_title}} — {{today}}
```

**Content:**
```
{{full_script}}
```

---

### Step 5 — Send Notification to Slack

**App:** Slack
**Event:** Send Channel Message

**Message:**
```
{{slack_summary}}
```

---

### Step 6 — Save to Notion Database

**App:** Notion
**Event:** Create Database Item

Map these fields:

| Notion Field | Zapier Value |
|-------------|-------------|
| Title | `{{chosen_title}}` |
| Topic | `{{topic}}` |
| Script | `{{full_script}}` |
| Tags | `{{seo_tags}}` |
| Hashtags | `{{hashtags}}` |
| Upload Tip | `{{upload_tip}}` |

---

## 📡 API Reference

### `POST /generate`

Main Zapier webhook endpoint.

**Request Body:**
```json
{
  "secret": "your-secret-key",
  "topic": "How to Build a RAG Pipeline",
  "niche": "AI and Data Engineering",
  "style": "educational and engaging",
  "title_index": 0
}
```

**Response:**
```json
{
  "status": "success",
  "topic": "How to Build a RAG Pipeline",
  "chosen_title": "Build a RAG Pipeline in 10 Minutes (Step by Step)",
  "all_titles": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"],
  "thumbnail_text_options": ["RAG in 10 MIN", "Build This NOW", "Copy This Setup"],
  "full_script": "=== HOOK (0:00 - 0:30) ===\n...",
  "seo_tags": ["rag pipeline", "ai engineering", "gpt-4", "..."],
  "hashtags": ["#AIEngineering", "#RAG", "#Python", "..."],
  "video_chapters": [{"time": "0:00", "title": "Intro"}, "..."],
  "hook_ideas": ["Hook 1", "Hook 2", "Hook 3"],
  "key_points": ["Point 1", "Point 2", "..."],
  "target_audience": "Developers learning AI engineering",
  "recommended_length": "10-12 minutes",
  "upload_tip": "Tuesday at 9am EST for tech content",
  "slack_summary": "🎬 New YouTube Script Ready!..."
}
```

### `GET /health`

Health check endpoint.

```json
{
  "status": "running",
  "service": "YouTube Script AI System",
  "version": "1.0.0"
}
```

---

## 📊 Pipeline Results

| Metric | Result |
|--------|--------|
| Script generation time | ~60 seconds |
| Titles generated per run | 5 options |
| SEO tags per video | 10 tags |
| Script sections | Hook + Intro + 3 Sections + CTA + Outro |
| Output formats | JSON + Markdown |

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![GPT-4](https://img.shields.io/badge/GPT--4-412991?style=flat&logo=openai&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Zapier](https://img.shields.io/badge/Zapier-FF4A00?style=flat&logo=zapier&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=flat&logo=googlesheets&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=flat&logo=notion&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white)

---

## 🎯 Use Cases

- 🎬 **YouTube creators** automating content pipelines
- 📊 **Content agencies** scaling script production
- 🤖 **AI engineers** building LLM automation workflows
- 🚀 **Solo founders** creating content without a team

---

## 📬 Connect With Me

[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=flat&logo=google-chrome&logoColor=white)](https://sarah-sair-ai-7044ftv.gamma.site/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sarahsair)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:sarahsair@gmail.com)

---

*Built with GPT-4, Flask, and Zapier by Sarah Sair — AI & Data Engineer*
