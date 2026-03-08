import os
import sys
import requests
from openai import OpenAI

def main():
    # Use the GitHub token to authenticate with GitHub Models (Free tier for Copilot users)
    github_token = os.environ.get('GITHUB_TOKEN')
    pr_number = os.environ.get('PR_NUMBER')
    repo = os.environ.get('REPOSITORY')
    
    # Get the list of changed files from the environment variable set by the GitHub Action
    changed_files_raw = os.environ.get('CHANGED_FILES', '').strip()
    changed_files = [f.strip() for f in changed_files_raw.split('\n') if f.strip()]
    
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment. The AI review cannot run.")
        sys.exit(0) # Exit cleanly so we don't block the PR, just skip the review.
        
    if not changed_files:
        print("No wiki markdown files changed. Skipping AI review.")
        sys.exit(0)
        
    # Initialize the OpenAI compatible client pointing to GitHub Models endpoint
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=github_token,
    )
    
    system_instruction = """
You are an expert Technical Documentation Agent. 
Your task is to evaluate markdown documentation updates in a Pull Request.
Your audience consists of both human software engineers and other AI coding assistants.

**Rules for your review:**
1. Determine if the tone is professional, direct, and developer-friendly. Point out areas that are too colloquial or overly complex.
2. Check if complex concepts are broken down into easy-to-read bullet points or clear paragraphs. Suggest improvements.
3. Check if the structure is AI-friendly: well-defined section headers (H1, H2, H3), and code blocks used correctly for specific variables, paths, or code snippets.
4. Catch any grammatical errors, typos, or awkward phrasing and suggest the exact corrected text.
5. Provide actionable feedback. Output your review as a clean markdown response. Do not provide a general summary if everything is perfect, but rather specific suggestions.
    """
    
    all_reviews = []
    
    for file_path in changed_files:
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. It might have been deleted. Skipping.")
            continue
            
        print(f"Reviewing {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        prompt = f"Please review the following documentation file `{file_path}`:\n\n```markdown\n{content}\n```"
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2 # Keep it focused and analytical
            )
            
            review = f"### 🤖 AI Review for `{file_path}`\n\n{response.choices[0].message.content}"
            all_reviews.append(review)
            print(f"Finished reviewing {file_path}")
        except Exception as e:
            print(f"Error calling GitHub Models API for {file_path}: {e}")
            all_reviews.append(f"### 🤖 AI Review for `{file_path}`\n\n*Failed to generate review due to an API error.*")
        
    # Combine reviews and post as a PR comment
    if all_reviews and github_token and pr_number and repo:
        print("Posting review comment to PR...")
        final_body = "## 📝 AI Documentation Review\n\n" + "\n\n---\n\n".join(all_reviews)
        post_pr_comment(github_token, repo, pr_number, final_body)
    else:
        print("Could not post to PR. Missing GitHub token, PR number, or repo name.")
        print("\nReview Output:\n")
        print("\n\n---\n\n".join(all_reviews))

def post_pr_comment(token, repo, pr_number, body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": body}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Successfully posted comment to PR.")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    main()
