# Developer's Guide

## Things to do if JSON schema for metadata changes

* Update the markdown files for doc by running following command from the root of the repo.

    ```bash
    python docs/doc.py
    ```

* Also make update to python models by running bash-script `codegen.sh`.
* Refactor where updates classes are used through out the code base.

## Testing markdown linting locally

To test linting errors for markdown files locally, you need to install following npm package.

```bash
npm install -g markdownlint-cli
```

After this you can run the following command to check for markdown linting errors. Make sure you are at the root of the repo.

```bash
markdownlint docs/**/*.md --config .markdownlint.yaml -i docs/schemas/**/*.md
markdownlint README.md --config .markdownlint.yaml
markdownlint CHANGELOG.md --config .markdownlint.yaml
```

## Testing spell check locally

To test spell check locally  for markdown and python files, you need to install following npm package.

```bash
npm install -g cspell
```

After you install `cspell` you can run following command to test the spell check.

```bash
cspell --config .cspell.json "src/**/*.py" "docs/**/*.md" "README.md" "CHANGELOG.md"
```
