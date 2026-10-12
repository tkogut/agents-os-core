# Reviewing artifacts (CLI)
Source URL: https://antigravity.google/docs/cli/artifacts

Features
Learn
Artifacts
Reviewing artifacts (CLI)
Markdown
AVAILABLE ON:
Antigravity CLI
Reviewing artifacts
Section titled “Reviewing artifacts”

Audit generated code, review implementation proposals, attach line-level feedback comments, and verify visual media assets before applying edits to your local filesystem.

Collaboration and co-steering
Section titled “Collaboration and co-steering”

An artifact is a structured deliverable created by the agent to accomplish its task and communicate its progress and thinking to you. Artifacts include rich Markdown outlines (such as implementation plans), code diffs, architecture diagrams, and visual media files.

As agents work with higher autonomy over longer periods, artifacts enable asynchronous collaboration. You don’t need to carefully monitor every individual tool execution synchronously. Instead, you review high-level deliverables at key milestones.

Because autonomous agents can occasionally go off-course or hallucinate solutions, the artifact workflow serves as a critical interactive co-steering mechanism. Depending on your configuration, the agent pauses at intermediate milestones, allowing you to inspect proposed plans or code edits, provide inline comments, and redirect the agent before any changes are physically written to your local filesystem.

The TUI partitions these assets into two interactive layers:

Artifact picker overlay: A high-level checklist menu containing review status markers, quick preview toggles, and collapsible folders.
Artifact detail viewer: A full-screen code audit interface supporting inline commenting, syntax highlighting, and diagram scaling.
Overview of /artifact
Section titled “Overview of /artifact”

When the agent produces or modifies files, a notification updates in your TUI status bar (/artifact to review). Press ctrl+r inside the prompt box to open the full-screen Artifact Picker panel.

                                                                                                    10 artifacts · /artifact to review
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
>
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Action required (10 left)
› [ ] new release_notes.md   open  approve reject
  utils.py
  [ ] new performance_report.md
  api_client.py
  config_manager.py
  [ ] new user_guide.md
  run_tests.py
  data_processor.py
  [ ] new system_architecture.md
  [ ] new project_overview.md

Keyboard: ↑/↓ Navigate  y/n Approve/reject  shift+a Approve all  p Preview  esc Done
Interaction keybindings
Section titled “Interaction keybindings”

Audit the file checklist using the following dedicated panel controls:

Key	TUI Command	Action Behavior
↑ / ↓	nav.scroll_line	Scrolls highlighted selections up and down through the list of entries.
h / l	nav.switch_button	Focuses and toggles between inline row buttons: open, approve, and reject (Left/Right arrows also supported).
p	confirm.preview	Toggles a quick inline file preview. This opens a 12-line truncated and indented code block preview directly under the selected row.
y	confirm.approve	Instantly approves the highlighted file. The status marker updates to a green checkmark (✓ approved).
n	confirm.reject	Instantly rejects the highlighted file. The status marker updates to a red cross (✗ rejected).
Shift+A	confirm.approve_all	Bulk-approves all pending actionable files in one action.
Shift+R	confirm.reject_all	Bulk-rejects all pending actionable files in one action.
Enter	nav.confirm	Executes the active focused button. If the open button is focused, it launches the full-screen detail viewer.
Esc	nav.escape	Saves your active review state, submits approvals/rejections back to the agent thread, and returns focus to the prompt box.
Code files and visual media
Section titled “Code files and visual media”

To organize workspace assets, the picker separates files by format types:

Actionable code files: Standard programming code, configuration files, and plan Markdown files that require explicit approvals.
Collapsible media drawer: Visual asset files (such as PNG, JPG, WebP, SVG, MP4, or WebM media) are grouped into a dedicated Media drawer header. Use the following actions to interact with media items:
Highlight the Media header row and press Enter to expand or collapse the drawer list.
Highlight a specific media item and press Enter to open the file inside your operating system’s native media viewer.
Viewing an artifact
Section titled “Viewing an artifact”

To launch a close audit of a file’s code structure or proposed logic, select open (or press Enter directly on a highlighted code row) to open the Artifact Detail Viewer.

implementation_plan.md
>   1      Implementation Plan: Alpha-Centauri Telemetry Scaling Engine
    2
    3     This document provides a highly detailed, step-by-step engineering implementation plan to upgrade the Alpha-Centauri
    4     telemetry ingestion pipeline. It outlines current gaps, proposed architecture improvements, execution timelines, risks,
    5     and verification procedures.
    6     ──────
    7     ## 1. Executive Summary
    8
    9     As sensor deployments scale from 100 to 10,000 active nodes, the existing synchronous Python-based ingestion system (
   10     data_processor.py ) faces critical CPU and write latency bottlenecks.
   11
   12     This implementation plan details the migration to an asynchronous, remote-buffered pipeline utilizing distributed
   13     message
   14     queues, multi-threaded worker pools, and an optimized column-oriented storage layer.
   15     ──────
   16     ## 2. Current Architecture vs. Target Architecture
   17
   18     ### Gap Analysis
   19
   20      Feature    | Existing (v1.2)   | Target (v2.0)     | Gap to Resolve
   21     ------------|-------------------|-------------------|---------------------------
   22      Concurrency| Sync, 1-thread    | Async, concurrent | Cannot scale peak bursts
   23      Buffer     | None (direct API) | Message Queue     | Outage data loss
   24      Storage    | Flat JSON         | Columnar CNS      | Slow queries, high consumption
   25      Config     | Load on launch    | Dynamic polling   | Requires restarts to update
   26
   27     ### Architectural Schema
   28
   29         Ingestion Layer │ Buffering Layer │ Processing Layer │ Storage Layer
   30
   31         ┌────────────┐    ┌────────────┐
   32         │ "Sensor 1" │    │ "Sensor 2" │
   33         └────────────┘    └────────────┘
   34                │ HTTP POST           │ HTTP POST
   35                ▼                 ▼
   36         ┌─────────────────┐
   37         │ "Load Balancer" │
   38         └─────────────────┘
   39                  │
   40                  ▼
   41         ┌───────────────────────┐    ┌───────────────────────┐
   42         │ "Ingestion Gateway A" │    │ "Ingestion Gateway B" │
   43         └───────────────────────┘    └───────────────────────┘
   44                     │ Publish                    │ Publish
   45                     ▼                            ▼
   46         ┌─────────────────────────────┐
   47         │ "Distributed Message Queue" │
   48         └─────────────────────────────┘
   49                        │ Stream Consume
   50                        ▼
   51         ┌────────────────────┐    ┌────────────────────┐
   52         │ "Worker Process 1" │    │ "Worker Process 2" │
   53         └────────────────────┘    └────────────────────┘
   54                    │ Read Config               │ Read Config
   55                    ▼                         ▼
   56         ┌──────────────────────────┐    ┌──────────────────────────┐
   57         │ "Dynamic Config Service" │    │ "Columnar Storage (CNS)" │
  [0%  L1  1-57/135]

  ↑/↓ scroll · pgup/pgdown page · shift+g bottom · g top · c comment · m raw mermaid · ctrl+=/ctrl+- zoom 100%
  l hide lines · esc close
Auditing and navigation
Section titled “Auditing and navigation”

Use the following keyboard shortcuts to navigate the detail viewer:

Scrolling: Scroll page-by-page or line-by-line using j/k (or standard arrow keys).
Boundary jump: Press g to jump to the top of the file, and Shift+G to jump directly to the bottom.
Toggle gutter: Press l to toggle the line number gutter on and off for a cleaner presentation of the raw code.
Granular line commenting
Section titled “Granular line commenting”

If a specific block of code requires correction, follow these steps:

Navigate and position your cursor on the target line.
Press c to open an inline, multi-line text editor buffer attached directly to that line.
Draft your descriptive feedback, and press Esc to save and submit the comment. The line is updated with a visual comment indicator (💬).
To delete your active feedback, position your cursor on the commented line and press d.
Custom Mermaid diagram rendering
Section titled “Custom Mermaid diagram rendering”

If the active document contains structured system flowcharts, database relationships, or architectural layouts, use the following controls:

Cycle render modes (m): Press m to cycle through the following visual rendering modes:
Kitty graphics image: Renders diagrams natively as inline graphics within Kitty-compatible terminal emulators.
ASCII box art (default): Renders diagrams as clean, high-performance text art compatible with all shells.
Raw code: Shows the raw Markdown code block fences.
Zooming graphics: When Kitty graphics image mode is active, press ctrl+= to zoom in and scale up the image, and ctrl+- to zoom out.

Press Esc to close the detail viewer and return to the primary picker checklist.

Next steps
Section titled “Next steps”

Configure settings preferences and review agent autonomy parameters:

Managing conversations: Resume prior sessions and fork branches.
Settings, rendering, and keybindings: Customize keyboard hotkeys and visual buffers.
Permissions and sandbox: Configure security parameters and containment lists.
Previous
Visual screenshots
Next
Overview
About Google
Google Products
Privacy
Terms