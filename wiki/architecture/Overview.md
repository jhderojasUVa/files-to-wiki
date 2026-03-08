# Architecture Overview

This documentation pipeline solves the age-old problem of "stale wikis" by linking the Wiki ecosystem directly to the Pull Request workflow using custom GitHub Actions.

Our architecture consists of three core components:

## 1. The Deployment Pipeline (`update-wiki.yml`)
When a developer merges a Pull Request specifically targeting files within our `wiki/` directory, GitHub Actions intercepts the event. 
- It clones both the main repository and the `.wiki.git` backing repository.
- It executes `scripts/generate_sidebar.py` to recursively crawl the new folders and dynamically update the navigation tree (`_Sidebar.md`).
- It completely overwrites the existing GitHub Wiki files with the freshly modified files.
- It force-pushes the commit back to the `.wiki` repository, instantly shifting the changes live.

## 2. Dynamic Sidebar Generation
Because the GitHub Wiki expects flat structures, organizing nested documentation can become messy. Our `generate_sidebar.py` reads our local directory structure (e.g., `wiki/architecture/`) and converts it into deeply nested dropdowns and headers inside `_Sidebar.md`. 
It ensures absolute internal links are created based on the `GITHUB_REPOSITORY` environment variable so no internal wiki links are ever broken regardless of a user's current navigational depth.

## 3. The AI Reviewer (`ai-review.yml`)
Documentation is only useful if it's readable. Whenever a Markdown file is added to a PR, our python agent (`scripts/ai_doc_reviewer.py`):
1. Captures the exact file changes.
2. Establishes a connection to the fast inference endpoint of GitHub Copilot (`gpt-4o`).
3. Acts under a static System Prompt instructing it to be a brutally honest, developer-first technical writer.
4. Generates structural suggestions and grammatical fixes and immediately posts them as a comment on the GitHub PR timeline.
