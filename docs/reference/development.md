# :gear: Development

## :hammer_and_wrench: Tools

Tools used to develop this repository.

!!! note
    All commands are run from the root of the repo unless otherwise specified.

### :robot: [Google Antigravity CLI][15]

Used for AI-assisted repository management, including recipe imports and maintenance. It automates several steps of the manual workflow, such as using **LiteParse** to extract structured recipe information from local documents and images, fetching recipes from URLs, creating `.cook` files, downloading images, and updating the site configuration.

```shell title="Usage"
# Import a recipe from a GitHub issue
antigravity -i "Import recipe from issue #1333"

# Perform codebase maintenance
antigravity -i "Run zensical serve and fix any issues"
```

[15]: <https://github.com/google-gemini/antigravity-cli>
