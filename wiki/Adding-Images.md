# Adding Images to the Wiki

It is incredibly useful to include diagrams, screenshots, or graphs inside your Wiki documentation. Because we use a Docs-as-Code synchronization pipeline, adding images requires following standard repository structures rather than dragging and dropping into the GitHub UI.

## How to add an image

1. Inside the `wiki/` folder in your repository, look for (or create) an `images/` directory.
   - Good practice dictates keeping images organized, so feel free to make subfolders (e.g., `wiki/images/architecture/diagram.png`).
2. Add your `.png`, `.jpg`, `.gif`, or `.svg` file locally to this folder.
3. Inside your markdown document (e.g., `wiki/architecture/Overview.md`), include standard Markdown image syntax referencing the absolute path from the wiki root:

```markdown
![Architecture Diagram](images/architecture/diagram.png)
```

### Why use relative/absolute paths?
During the synchronization via our deployment pipeline (`update-wiki.yml`), the entire contents of the `wiki/` directory—including the `images/` folder you created—are seamlessly copied directly into the root of the GitHub Wiki repository. 

GitHub Wiki natively supports resolving images contained within its backend. By using standard Markdown `<img />` or `![]()` syntax, the GitHub UI will securely serve that image onto your page directly from the repository!

---
> **Pro Tip:** Try optimizing and compressing images before pushing them into the git repository to keep cloning times fast. Heavy graphics can permanently bloat git history.
