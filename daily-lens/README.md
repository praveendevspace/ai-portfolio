# The Daily Lens

A personal digital newspaper that brings recent global headlines into a short, readable briefing. The site uses a newspaper-inspired layout with a midnight-blue masthead, ivory story cards, and copper accents.

**Live website:** https://the-global-edit-praveen.fairysugar4097.chatgpt.site

The website retains its original URL after being renamed from The Global Edit. Access is currently private and requires the owner's ChatGPT account.

## Features

- Highlights featuring up to seven stories, with available coverage from each topic.
- World, Business, Technology, and Science filters.
- Search across loaded headlines and descriptions.
- Saved stories stored in the current browser using local storage.
- Publication timestamps and links to original reporting.
- Responsive layouts for desktop and mobile.
- A refresh button to fetch the latest available feed results.

## News sources and selection

The server reads these RSS feeds:

| Publisher | Topic | Feed |
| --- | --- | --- |
| BBC News | World | https://feeds.bbci.co.uk/news/world/rss.xml |
| BBC News | Business | https://feeds.bbci.co.uk/news/business/rss.xml |
| BBC News | Technology | https://feeds.bbci.co.uk/news/technology/rss.xml |
| BBC News | Science & Environment | https://feeds.bbci.co.uk/news/science_and_environment/rss.xml |
| The Guardian | World | https://www.theguardian.com/world/rss |

The server takes up to 12 entries per feed, removes exact duplicate headlines, keeps stories published within the last three days, and sorts them by publication time. Highlights include the newest available story from each topic, then fill the remaining places from the recent stories.

Descriptions are publisher-provided excerpts. The website does not retrieve full articles or currently use an AI model to summarize or rank news. Selection reflects recency and topic variety rather than an editorial assessment of global importance.

## Refresh behavior

News is requested when the page opens or the reader selects **Refresh edition**. Responses allow a 15-minute cache; server caching is used only where the hosting runtime permits it. Refresh may therefore return cached results.

There is no scheduled daily edition, background update job, or automatic refresh timer while the page remains open. Saved stories persist in the same browser until removed or browser storage is cleared; they do not sync across devices.

## Technology and structure

The project uses plain HTML, CSS, and browser JavaScript, served by a JavaScript ES-module Worker. It has no third-party npm dependencies. Google Fonts supplies optional web fonts, with local font fallbacks.

```text
daily-lens/
├── README.md
├── package.json                 # Project metadata and syntax-check command
├── .openai/
│   └── hosting.json             # Existing Sites project identity
├── worker/
│   └── index.js                 # Source: server, page markup, styles, and browser code
├── scripts/
│   ├── build.sh                # Recreates dist/ from source
│   └── validate-artifact.mjs    # Checks the generated manifest and Worker export
└── dist/                       # Generated deployment output
    ├── .openai/hosting.json
    └── server/index.js
```

## Build and validate

Requirements: a modern Node.js runtime (Node.js 22 or later recommended) and Bash. No dependency installation is needed.

From this project directory, run:

```bash
node --check worker/index.js
bash scripts/build.sh
node scripts/validate-artifact.mjs
```

If npm is available, `npm run check` also performs the source syntax check.

The build deletes and recreates `dist/`, then copies the Worker source and hosting manifest. The validator confirms that the manifest is valid JSON and the generated ES module exports a `fetch` handler. These checks do not verify browser appearance, live news availability, or the complete hosted runtime.

## Editing the newspaper

- Edit `worker/index.js` for the design, branding, news sources, and interactions.
- Update the `feeds` array near the beginning of that file to change RSS sources.
- Rebuild after editing. Do not edit `dist/server/index.js` directly; a build overwrites it.
- The `global-edit-saved` browser storage key is retained to preserve existing saved stories after the rename.
- No local development server is configured. Opening the generated JavaScript file in a browser does not run the website; the `/api/news` route requires a compatible Worker runtime.

## Hosting and deployment

The website is published through **OpenAI Sites**, with server execution on **Cloudflare Workers**. Your computer does not need to stay on for the published site to work.

The tracked `.openai/hosting.json` links this source folder to the existing hosted project. Preserve its `project_id` when updating the same website. Never put credentials or API keys in this file or commit them to Git.

To publish changes through Sites:

1. Edit and validate the source.
2. Build the deployment output.
3. Use the Sites workflow to synchronize the source repository and package that exact source revision.
4. Save and deploy the packaged version to the existing Site, preserving its access settings.
5. Confirm that deployment succeeds before sharing the link.

Running `build.sh` alone does not upload or publish changes. You can ask the coding assistant to publish updates through the connected Sites tools.

## Troubleshooting

- **Site cannot be reached:** Try another browser and network, such as mobile data, to distinguish browser or network issues from hosting issues.
- **Access denied or sign-in required:** Use the ChatGPT account that owns the private Site.
- **News temporarily unavailable:** Retry later. The feeds may be unavailable; saved stories remain accessible through the Saved tab once the page loads.
- **Changes are missing:** Confirm the updated source was built and deployed, then reload the page.
- **Old IDE paths:** This folder was renamed from `global-edit` to `daily-lens`; reopen files from the new location.

## Possible next steps

AI-written summaries, explanations of why stories matter, interest-based personalization, scheduled daily editions, and additional publishers are future enhancements. They are not implemented in this version. Adding an AI service may require credentials and incur separate usage charges.
