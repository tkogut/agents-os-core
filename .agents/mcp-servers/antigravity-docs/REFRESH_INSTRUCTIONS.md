# How to Refresh the Knowledge Base

When new updates are released for the Antigravity IDE, you can easily pull the latest documentation into your local MCP server to keep the AI up to date.

### The Easy Way
I have created a single script that will run the whole process for you. 

Simply run this command in your Mac terminal:
```bash
./update.sh
```

### What it does:
1. Runs `scraper.py` to find any new pages on the website.
2. Runs `extractor.py` to overwrite your `knowledge_base/` folder with the newest text.
3. Your MCP server instantly starts using the new files. There is no need to restart anything!

### Google Calendar Reminder
To add a recurring monthly reminder to your Google Calendar, simply click this link:
[Add Monthly Refresh to Google Calendar](https://calendar.google.com/calendar/r/eventedit?text=Refresh+Antigravity+Docs+MCP&dates=20260323T150000Z/20260323T151500Z&details=Run+the+update.sh+script+to+fetch+the+latest+documentation+for+the+IDE.&recur=RRULE:FREQ%3DMONTHLY)
