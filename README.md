# InstaPlus

**InstaPlus** is an advanced Instagram automation bot that mimics real user activity — liking posts, watching reels, commenting, and sharing — using smart cursor movements and keyboard inputs.  
It’s designed to behave like a human, reducing the chance of detection while improving engagement automation.

> 🚀 A lightweight and intelligent Instagram automation tool that behaves more human than bot.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## ✨ Features

- ❤️ **Auto-like posts** on the feed  
- 🎥 **Interact with Reels** (like, comment, or share)  
- 💬 **Generate AI-based comments** using GPT integration  
- 📤 **Auto-share content** to increase engagement  
- 🖱️ **Real mouse movements and keypresses** to simulate human behavior  
- 🔁 **Dynamic delays** and randomized actions  
- 🧠 **Local database storage** for action history and usage tracking  
- 📈 **Smart automation logic** that prevents repetitive behavior

---

## 📂 Project Structure

```
InstaPlus/
├─ instaplus.py       # Main entry point
├─ feed.py            # Handles feed scrolling and likes
├─ reels.py           # Controls reel interactions
├─ text_comments.py   # Handles text comment logic
├─ gpt.py             # AI-generated comments using GPT API
├─ db.py              # Local action history storage
├─ tools.py           # Utility for mouse/keyboard simulation
├─ images.py          # Image analysis or screenshot helpers
├─ util.py            # Logging, delays, and config tools
├─ carousel.py        # Handles multi-photo posts
├─ requirements.txt   # Python dependencies
├─ LICENSE
└─ README.md
```

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/InstaPlus.git
   cd InstaPlus
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your settings (like credentials, delay times, etc.) in the main file or environment variables.

---

## 🚀 Usage

### Run InstaPlus
```bash
python instaplus.py
```

### Example Actions
- Automatically like posts on your feed  
- Like and comment on Reels  
- Post or share selected content  
- Auto-type comments using generated suggestions  
- Simulate human mouse paths and typing input  

### Example Python usage
```python
from instaplus import InstaPlus
from tools import shuffle
bot = InstaPlus()

hashtags = [
    "#mahadev",
    "#triund",
    "#tree",
    "#nature",
    "#waterfall",
    "#tree",
    "#sky",
    "#northernlights",
    "#ocean",
    "#wildlife",
    "#birds",
    "#love",
    "#tracking",
    "#travel",
    "#exploring"
]

hashtags = shuffle(hashtags)
instaBot.like_by_hashtag(tags=hashtags, amount=30, do_comments=True, do_like_comments=True, randomize=False, follow=False)

# explore
bot.explore(amount=100, do_comments=True, do_like_comments=True, randomize=False, follow = False)

```

---

## 🧠 How It Works

1. **Login**  
   It uses previous logged session in browser.

2. **Feed interaction**  
   Scrolls the Instagram feed, randomly selecting posts to like or comment on.

3. **Reels & shares**  
   Opens reels and performs random actions based on user-defined frequency.

4. **Human behavior model**  
   Uses randomized delays, mouse drags, and keyboard events to mimic human timing and precision.

5. **Comment generation**  
   Uses integrated GPT module (`gpt.py`) to create context-aware comments automatically.

---

## 🔐 Security Notes

- This bot **does not hack, scrape private data, or bypass login verification**.  
- It interacts through your normal Instagram session, like a human user.  
- Avoid running it excessively — too much automation may still trigger rate limits.  
- Use responsibly and at your own risk (for learning or research purposes).

---

## 🧩 Developer Notes

- `instaplus.py` — Main orchestrator of all actions  
- `feed.py` & `reels.py` — Handle content scrolling and interaction  
- `gpt.py` — Integrates AI-generated comments  
- `tools.py` — Simulates keyboard/mouse behavior  
- `db.py` — Logs user actions for smarter repetition control  

---

## 🪄 License

This project is licensed under the **MIT License** — free to use, modify, and share.

---

## ⚡ Credits

Developed with ❤️ for automation lovers who want to **stay human while being a bot**.
