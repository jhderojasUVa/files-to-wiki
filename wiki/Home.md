# Welcome to the Documentation Repository!

This Wiki serves as the living documentation for our internal architecture, systems, and standard practices. It is powered by a **Docs-as-Code** pipeline that permanently syncs this Wiki directly from the source code repository.

## How to Contribute
Because of our automated pipeline, please **do not** attempt to edit this Wiki directly via the GitHub UI. Your changes will be overwritten the next time a developer merges code!

Instead, follow this workflow:
1. Clone the main repository to your local machine.
2. Navigate to the `wiki/` directory.
3. Add, edit, or remove Markdown (`.md`) files.
4. Open a Pull Request on GitHub. 

When you open a Pull Request, our **AI Documentation Review Agent** (powered by GitHub Models / Copilot Free) will inherently scan your text. It will check grammar, structural markdown integrity, and readability, outputting automated suggestions directly on your Pull Request. 

Once your Pull Request is merged into the `main` branch, the deployment pipeline will instantly update this public Wiki and auto-generate the navigation Sidebar for easy browsing.

### Have questions?
Feel free to read through the `Architecture Overview` to understand how the inner synchronization and AI Review agent operate behind the scenes!
