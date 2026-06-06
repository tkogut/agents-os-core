# Tab
Source URL: https://antigravity.google/docs/tab

Editor
>
Tab
Antigravity Editor: Tab & Navigation

This guide covers the core navigation and completion tools: Supercomplete, Tab-to-Jump, and Tab-to-Import.

Supercomplete

Supercomplete provides code suggestions in a region near your current cursor position.

How it Works
File-Wide Suggestions: Suggestions can modify code throughout the document, handling tasks like changing variable names or updating separate function definitions simultaneously.
Accepting: Press Tab to accept the changes.
Tab-to-Jump

Tab-to-Jump is a fluid navigation tool that suggests the next logical place in your document to move your cursor to.

How it Works
A "Tab to jump" icon will appear offering to move your cursor to where your next logical edit will be. Pressing Tab instantly moves your cursor to that location.
Accepting: Press Tab to accept the jump.
Tab-to-Import

Tab-to-Import handles missing dependencies without breaking your flow.

How it Works
Detection: If you type a class or function that isn't imported, Antigravity suggests the import.
Action: Press Tab to complete the word and instantly add the import statement to the top of the file.
Settings

In your settings, you can customize the behavior of these features:

Enable/Disable Features: You can individually turn off Autocomplete, Tab-to-Jump, Supercomplete, or Tab-to-Import.
Tab Speed: Controls the responsiveness of suggestions.
Slow: Waits for more context before suggesting.
Default: Offers a balanced pace.
Fast: Provides rapid-fire suggestions.
Highlight Inserted Text: When enabled, text inserted via Tab is highlighted to track changes easily.
Clipboard Context: When enabled, Antigravity uses the contents of your clipboard to improve completion accuracy.
Allow Gitignored Files: Enables Tab features (suggestions and jumping) within files listed in your .gitignore file. Tab will only ignore gitignored files if git is installed.
Editor
Command