# AI-Generated Wiki Documentation Repository

This repository demonstrates an automated architecture for maintaining, scaling, and reviewing technical documentation that resides within the codebase but is rendered on the GitHub Wiki. It leverages several automated GitHub Actions to streamline the developer experience.

## Features

### 1. Wiki structure auto-sync 
When a pull request introduces modifications to the `wiki/` directory and is merged to `main`, a GitHub action automatically syncs these changes to the GitHub Wiki attached to this repository.
This solves the problem of keeping the Wiki and the source-of-truth markdown files in the repository perfectly in sync.

### 2. Auto-generated sidebar structure
The sidebar of a GitHub Wiki is critical to user experience. We've introduced a Python script `scripts/generate_sidebar.py` that walks the `wiki` directory and generates a dynamic `_Sidebar.md` file.
- Automatically generates navigation based on the directory structure.
- Emits categories only for folders that contain `.md` documentation.
- Auto-resolves absolute links so that users can navigate the sidebar accurately regardless of their current depth within the Wiki.

### 3. AI Documentation Reviewer
To ensure the documentation continues to be high quality for both human developers and future AI agents, this repository leverages an automated AI reviewer mechanism running on GitHub Models (the free Copilot model access available to GitHub users).
When a user opens a pull request that modifies markdown source files, the `scripts/ai_doc_reviewer.py` script executes via GitHub Action.

**What the AI Reviewer looks for:**
*   **Tone:** Enforces a professional, direct, and developer-friendly voice.
*   **Simplicity:** Flags overly complex explanations and suggests breaking them down into readable formats like bullet points.
*   **AI-Readability:** Ensures strong, semantically correct Markdown headers (H1, H2, H3...) and proper code blocks are used for variables/paths—making the documentation easier for RAG pipelines to ingest down the road.
*   **Proofreading:** Corrects typos, grammatical errors, and awkward phrasing.

Whenever a structural or wording improvement is identified, the AI Reviewer automatically submits a Pull Request comment detailing its findings and suggesting direct copy-paste changes.

## Setup Instructions

If you intend to use this structural setup, here is what you need to configure:

1.  **Enable GitHub Wiki:** Ensure that your repository's settings have the Wiki feature enabled.
2.  **Action Write Permissions:** Ensure your GitHub Actions have `write` permission for both the repo and Pull Requests. This is mandated within the Workflow YAMLs, but your organization settings must also allow Actions to submit comments.
3.  **GitHub Models Access:** Since this utilizes GitHub Models endpoints (`https://models.inference.ai.azure.com`), the script relies on your GitHub Authentication via `GITHUB_TOKEN`. Make sure your account has access to GitHub Models. If your default `GITHUB_TOKEN` lacks Copilot/Models scope, you may need to map a Personal Access Token with the required scopes into the `GITHUB_TOKEN` environment variable in the workflow.
