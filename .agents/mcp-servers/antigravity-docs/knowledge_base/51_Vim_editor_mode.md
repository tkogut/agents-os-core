# Vim editor mode
Source URL: https://antigravity.google/docs/cli/vim-editor-mode

Features
Learn
Settings
Vim editor mode
Markdown
AVAILABLE ON:
Antigravity CLI
Vim editor mode
Section titled “Vim editor mode”

Edit prompts with modal Vim keybindings instead of the default flat text editor.

Vim editor mode replaces the editing model in every multi-line input surface of the CLI:

Surface	What you edit there
The prompt box	Your message to the agent, including multi-line prompts and slash commands.
The comment editor in /diff	Review comments you leave on a changed file.
The comment editor in the artifact review panel	Feedback on a generated artifact before you accept it.

It also adds a vim tab to the help overlay and a mode badge to the status line.

Enable Vim editor mode
Section titled “Enable Vim editor mode”

Vim editor mode is off by default. Turn it on from the interactive settings panel or directly in settings.json.

Using the settings panel
Section titled “Using the settings panel”

To enable Vim editor mode in the settings panel, follow these steps:

Type /settings inside the prompt panel and press Enter.
Navigate to Editor Mode using ↑/↓.
Press Enter to select vim.
Set Editor Mode > Insert First to choose which mode each prompt starts in. Leave it off to start in Normal mode, or set it on to start in Insert mode with a bare Enter that submits. Refer to Start in insert mode.
Press Esc to save and close the editor.
Using settings.json
Section titled “Using settings.json”

Set editorMode in your configuration profile:

{
    "editorMode": "vim",
    "vimInsertFirst": false
}

The CLI loads this file from ~/.gemini/antigravity-cli/settings.json at startup. editorMode accepts "default" and "vim". vimInsertFirst controls which mode each new prompt starts in and applies only when editorMode is "vim"; refer to Start in insert mode.

Note: editorMode is unrelated to the editor setting. editor picks the external program that Ctrl+G launches, so setting editor to "vim" opens Vim in a separate window and does nothing to the prompt. editorMode is the one that controls modal editing inside the CLI prompt itself.

Switch between modes
Section titled “Switch between modes”

Vim editor mode starts in NORMAL. Press i to type, and Esc to return to NORMAL.

Command	Action	From mode
Esc, Ctrl+C	Enter NORMAL mode	INSERT, VISUAL
i	Insert before the cursor	NORMAL
I	Insert at the first non-blank character	NORMAL
a	Insert after the cursor	NORMAL
A	Insert at the end of the line	NORMAL
o	Open a line below and insert	NORMAL
O	Open a line above and insert	NORMAL
v	Start a character-wise selection	NORMAL
V	Start a line-wise selection	NORMAL

The status line reports the current mode:

Mode	Badge
NORMAL	none
INSERT	-- INSERT --
VISUAL	-- VISUAL --
VISUAL LINE	-- V-LINE --

An empty badge area means you’re in NORMAL mode. If you run a custom status line, it replaces this badge unless you stack it with the default.

Tip: Press ? in NORMAL mode to open the shortcuts overlay, or run /help and select the vim tab for a full cheat sheet.

Submit your prompt
Section titled “Submit your prompt”

Enter behaves differently in each mode, so you can compose multi-line prompts without accidental submits.

Context	Enter	Ctrl+S / Ctrl+Enter	ZZ
NORMAL mode	Submit	Submit	Submit
INSERT mode	Insert a newline	Submit	—
INSERT mode, insert-first on	Submit	Submit	—

ZZ submits from NORMAL and VISUAL mode, matching the muscle memory of writing and quitting a buffer.

Start in insert mode
Section titled “Start in insert mode”

Set vimInsertFirst when you want each new prompt to begin in INSERT mode with a bare Enter that submits. This keeps the default typing experience while leaving NORMAL mode one Esc away.

{
    "editorMode": "vim",
    "vimInsertFirst": true
}

The Editor Mode > Insert First option appears in /settings only when Editor Mode is set to vim. It has no effect in default mode.

Move the cursor
Section titled “Move the cursor”

All motions work on their own in NORMAL and VISUAL mode, and as targets for an operator.

Key	Motion
h l	Left, right
j k	Down, up
0 $	Start of line, end of line
^	First non-blank character on the line
w b e	Next word, previous word, end of word
W B E	Same, treating whitespace-delimited chunks as words
gg G	Start of input, end of input
f{char} F{char}	Jump onto the next or previous {char}
t{char} T{char}	Stop one character short of the next or previous {char}
; ,	Repeat the last f/F/t/T forward, backward
Edit text
Section titled “Edit text”

Editing commands fall into three groups: single keys that act immediately, operators that wait for a motion, and text objects that select a delimited region.

Single-key commands
Section titled “Single-key commands”
Key	Action
x	Delete the character under the cursor
r{char}	Replace the character under the cursor with {char}
D C	Delete or change from the cursor to the end of the line
o O	Open a new line below or above and enter INSERT mode
p P	Paste after or before the cursor
u U	Undo, redo. Ctrl+R does not redo; it opens artifact review

Commands take no count prefix, so 3dd deletes one line. To act on several lines at once, select them with V and press the operator. There is also no . to repeat the last change.

There is one unnamed register rather than the usual "a–"z set. Deletes fill it, so x, D, C, d, and c all leave text you can paste back with p.

Paste is linewise-aware. Text yanked with dd or yy pastes onto a new line below (p) or above (P). Anything else pastes inline.

Operators and motions
Section titled “Operators and motions”

Combine an operator with any motion to act on the span it covers.

Operator	Action	Word forms	Whole line
d	Delete	dw de db	dd
c	Change (delete, then enter INSERT mode)	cw ce cb	cc
y	Yank	yw ye yb	yy
dw     Delete to the start of the next word
d$     Delete to the end of the line
c^     Change back to the first non-blank character
yG     Yank to the end of the input
dfx    Delete forward through the next "x"

cw changes to the end of the current word, matching real Vim.

Text objects
Section titled “Text objects”

Pair an operator with i (inside) or a (around) and a delimiter.

Object	Selects
iw aw	A word, with or without surrounding whitespace
iW aW	A whitespace-delimited chunk
i" a" i' a'	Text in single or double quotes
i( a( i) a)	Text in parentheses
i[ a[ i] a]	Text in square brackets
i{ a{ i} a}	Text in braces

Backticks work the same way: pair i or a with a backtick to select inline code.

ci"    Change the text inside the nearest quotes
da(    Delete a parenthesized group, parentheses included
yiw    Yank the word under the cursor
Work with selections
Section titled “Work with selections”

Press v or V to select, move with any motion, then apply a command. Press v or V again, or Esc, to leave.

Key	Action on the selection
d x	Delete
c	Change
y	Yank
r{char}	Replace every selected character with {char}
~	Toggle case
u U	Lowercase, uppercase

Note: ~, u, and U change case in VISUAL mode only. In NORMAL mode, u and U are undo and redo.

Run slash and shell commands
Section titled “Run slash and shell commands”

Press / or ! in NORMAL mode. The CLI inserts the character and switches to INSERT mode, so slash commands and shell commands work without pressing i first.

/settings     Open the settings panel from NORMAL mode
!ls -la       Run a shell command from NORMAL mode
Customize the submit and newline keys
Section titled “Customize the submit and newline keys”

Three Vim actions are remappable in ~/.gemini/antigravity-cli/keybindings.json. These are the defaults:

{
    "vim.insert.insert_newline": ["alt+enter", "ctrl+j", "enter", "shift+enter"],
    "vim.insert.submit": ["ctrl+enter", "ctrl+s"],
    "vim.normal.submit": ["ctrl+enter", "ctrl+s"]
}

Motions, operators, and text objects are fixed and can’t be remapped.

Submit with Enter in NORMAL mode only
Section titled “Submit with Enter in NORMAL mode only”

This is the default. Enter submits from NORMAL mode and inserts a newline in INSERT mode, so you can type freely and submit with a single Esc Enter. No configuration is needed. Leave vimInsertFirst off:

{
    "editorMode": "vim",
    "vimInsertFirst": false
}
Submit with Enter in INSERT mode too
Section titled “Submit with Enter in INSERT mode too”

Move enter out of vim.insert.insert_newline and into vim.insert.submit. Shift+Enter, Alt+Enter, and Ctrl+J still insert newlines:

{
    "vim.insert.insert_newline": ["alt+enter", "ctrl+j", "shift+enter"],
    "vim.insert.submit": ["ctrl+enter", "ctrl+s", "enter"]
}

Setting vimInsertFirst to true achieves the same submit behavior without editing keybindings, but it also changes which mode each new prompt starts in.

Warning: Enter always submits in NORMAL mode. Remapping vim.normal.submit adds keys; it never removes Enter.

Show the mode in a custom status line
Section titled “Show the mode in a custom status line”

A custom status line replaces the built-in one, and the mode badge goes with it. You have two ways to get the mode back.

Keep the built-in line and stack your script underneath it:

{
    "statusLine": {
        "type": "command",
        "command": "~/.gemini/antigravity-cli/statusline.sh",
        "stack_with_default": true
    }
}

Or render the mode yourself. When editorMode is "vim", the JSON payload piped to your script carries a vim object:

{
    "vim": {
        "mode": "INSERT"
    }
}

mode is NORMAL, INSERT, VISUAL, or VISUAL LINE. The field is absent entirely when Vim editor mode is off, so a script can use its presence as the enablement check:

#!/bin/bash
input=$(cat)
mode=$(echo "$input" | jq -r '.vim.mode // empty')
[ -n "$mode" ] && printf -- '-- %s -- ' "$mode"
echo "$input" | jq -r '.model.display_name'

Note: vim.mode reports NORMAL, unlike the built-in badge, which renders nothing in that mode. A script that prints every mode shows a -- NORMAL -- badge the built-in line never displays.

Next steps
Section titled “Next steps”

Explore the following guides to further customize your editing experience:

Settings, rendering, and keybindings: Configure the rest of your preferences and remap keys.
Status line customization: Control what the status line reports alongside the Vim mode badge.
CLI reference: Look up every configuration key and default keybinding.
Previous
Artifact review
Next
Overview
About Google
Google Products
Privacy
Terms