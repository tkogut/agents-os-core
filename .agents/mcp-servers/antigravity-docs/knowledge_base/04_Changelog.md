# Changelog
Source URL: https://antigravity.google/docs/changelog

Documentation
Changelog
Markdown
Changelog
Section titled “Changelog”

Track new features, improvements, and bug fixes across Google Antigravity surfaces, including Antigravity 2.0, Antigravity CLI, the Antigravity SDK, and Antigravity IDE.

Antigravity 2.0
Antigravity CLI
IDE Extensions
Antigravity SDK
Antigravity IDE

New versions roll out gradually and may take a few days to reach all users.

Expand all
v2.22.0
LATEST
October 8, 2026
Sidebar drag-and-drop, UI Extensions, and localized conversation timestamps

Now you can drag-and-drop conversations to organize threads across the sidebar and conversation timestamps now use localized month names. This release also supports UI extensions that Antigravity shows in the side pane next to a conversation.

Improvements
(3)
v2.21.1
October 7, 2026
Advanced Search, Automations, and grouped agent actions

Use ⌘+K (or CTRL+K on Windows) to search conversations based on their contents. The Scheduled Tasks tab is now called Automations, where you can run on-demand or scheduled automations or set up with the agent's help. Antigravity now also groups the agent's file edits, terminal commands, and file reads into one collapsible row.

Improvements
(9)
Fixes
(14)
v2.19.1
September 30, 2026
Message subagents directly, export Markdown as PDF, and conversation-only undo

You can now send messages straight to a subagent from the message box, export rendered Markdown as a PDF, and revert only the conversation when you undo. You can also reopen the window from the tray icon on Windows and Linux. This release includes 5 improvements and 5 fixes.

Improvements
(5)
Fixes
(5)
v2.18.1
September 28, 2026
Manage & Install plugins in AGY

This release introduces a Customizations tab and marketplace for discovering and installing plugins and includes overall improvements to the sidebar and chat experience.

Improvements
(14)
Fixes
(15)
v2.17.0
September 22, 2026
Plan before you build

Type /plan and the agent drafts a plan you can read and edit before it writes any code. The Agent setting that governs this is now called Plan Review Policy, and you can set it to review every plan, review only when the agent judges it worthwhile, or skip review entirely.

Improvements
(11)
Fixes
(10)
v2.16.0
September 22, 2026
Windows Subsystem for Linux, Office attachments, and live subagent cards

Connect to a Windows Subsystem for Linux distribution from Application Settings, and drop Word, Excel, and PowerPoint files straight into a prompt. Subagents now appear as live cards you can follow and stop while they work. This release also adds right-click copy and save for images.

Improvements
(12)
Fixes
(15)
v2.15.1
September 19, 2026
Windows sandbox support

This release introduces file and network sandboxing on Windows.

Improvements
(1)
v2.15.0
September 18, 2026
Custom agent controls and keyboard navigation

Custom agents can now switch off the default prompts and tools, and the agent you pick sticks with you after a reload. This release also adds Page Up, Page Down, Home, End, and Escape for moving around a conversation, speeds up switching conversations in the sidebar, and fixes a batch of settings and conversation state issues.

Improvements
(7)
Fixes
(16)
v2.14.0
September 15, 2026
New Permissions System & Terminal and Git version control for Enterprise

Enterprise and Business accounts can now use the integrated terminal and Git version control in the sidebar. This release also cuts memory use in long conversations and fixes a range of stability and accessibility issues.

Improvements
(10)
Fixes
(18)
v2.13.0
September 9, 2026
Introducing new Documents section and several UX enhancements for organization and control

External files such as Google Drive links, PDFs, and Office documents now have their own Documents section in the sidebar. This release also adds a virtualized viewer for large code and data artifacts, an option to hide whitespace-only changes in diffs, and clearer warnings when a configuration file fails to parse.

Improvements
(16)
Fixes
(16)
v2.12.2
September 3, 2026
Gemini 3.8 Flash using ADC in AGY Enterprise

Enterprise users can now access Google's flagship Gemini 3.8 Flash reasoning models using ADC.

Improvements
(1)
v2.12.0
September 2, 2026
Quoting, /boost, and improved Settings

You can now highlight part of a response and quote it as context for a follow-up prompt, and paid users get the new /boost command for a deeper multi-agent reasoning pass. This release also brings UX improvements across settings, the chat panel, and sidebar navigation.

Improvements
(7)
Fixes
(9)
v2.11.0
August 26, 2026
Generative UI and UI improvements

Generative UI renders HTML artifacts inline in chat, with support for KaTeX math and Chart.js and Plotly charts. This release also adds side-by-side terminal splits, the Darcula theme, and @path/to/file references inside AGENTS.md and custom rule files.

Improvements
(10)
Fixes
(30)
v2.10.0
August 24, 2026
Embedded Terminals, Git Version Control, and Audio Attachments

An embedded terminal and Git-native version control now live directly in the sidebar. This release also adds audio file attachments, interactive image commenting, richer previews for MCP tool execution, and core performance work.

Improvements
(13)
Fixes
(8)
v2.9.1
August 20, 2026
Remote Control, faster project switching, and more

This update introduces Remote Control to drive and monitor agent sessions on your local device from any browser, alongside core performance gains, improved sidebar navigation, and cleaner error recovery.

Improvements
(11)
Fixes
(15)
v2.8.1
August 13, 2026
Chat Responsiveness Improvements

Bug fixes addressing message responsiveness when interacting with the agent.

Fixes
(1)
v2.8.0
August 12, 2026
Persistent Sidebar Folders, Crash Fixes, and UI Enhancements

Antigravity improves workspace organization by persisting your sidebar folder states. This release also ensures reliable file and artifact previews.

Improvements
(1)
Fixes
(6)
v2.7.1
August 11, 2026
Reliability, Performance Gains, and User Experience Polish

Antigravity 2.7.1 introduces visual side-by-side previews for image diffs alongside comprehensive screen-reader and keyboard accessibility enhancements. This update also delivers key performance boosts, bug fixes, and UX refinements across chat interactions and project navigation.

Improvements
(11)
Fixes
(20)
v2.6.0
August 7, 2026
Faster long conversations, more reliable hooks and subagents

Conversations with long histories now open faster, improved custom hooks and subagents behavior, and administrator policies for connected tool servers are applied correctly — plus a broad set of fixes across chat, comments and the file viewer.

Improvements
(9)
Fixes
(21)
v2.5.0
July 31, 2026
Enterprise sign-in: Gemini Enterprise accounts and Workforce Identity Federation

Added enterprise sign-in support for Gemini Enterprise user accounts (with admin controls) and Workforce Identity Federation using Advanced SSO.

Improvements
(20)
Fixes
(13)
v2.4.3
July 28, 2026
Preview tabs, MCP timeouts, file attachments, and performance fixes

Added preview tabs, attachment support for .json, .md, and .csv files, MCP timeouts, keyboard shortcuts, and various bug fixes and improvements.

Improvements
(17)
Fixes
(10)
v2.3.1
July 16, 2026
Startup stability fix

Fixes a bug where an empty or malformed configuration file caused AGY to fail to load on startup.

Patches
(1)
v2.3.0
July 13, 2026
Queued messages, plain text files support, and stability improvements

Added support for queued messages, settings to configure message execution, a send now option, plain text file attachments, and various bug fixes and improvements.

Improvements
(6)
Fixes
(5)
v2.2.1
June 25, 2026
Antigravity Guide, audio support, search improvements, and performance fixes

New built-in Antigravity Guide skill, audio file rendering, improved substring file search, performance optimizations, and critical bug fixes.

Improvements
(19)
Fixes
(17)
v2.1.4
June 11, 2026
Quota Screen Redesign and PDF Support

Quota screen redesign, PDF attachment support, new /btw slash command, and other bug fixes

Improvements
(7)
Fixes
(4)
v2.0.11
June 3, 2026
Antivirus and Open IDE fixes

Startup and Open IDE button fixes

Fixes
(2)
v2.0.10
May 28, 2026
AGY 2.0 Bug fixes

AGY 2.0 Bug fixes

Improvements
(1)
Fixes
(1)
v2.0.6
May 22, 2026
Antigravity IDE integration

Added integration with Antigravity IDE.

Improvements
(2)
v2.0.1
May 19, 2026
AGY 2.0 Bug Fixes

Antigravity 2.0 Launch bug fixes.

Fixes
(3)
About Google
Google Products
Privacy
Terms