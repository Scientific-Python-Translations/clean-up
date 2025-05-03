# 🧹 clean-up

**A GitHub Action to automate the cleanup of stale branches in your repositories.**

This action identifies and deletes local Git branches that have been removed from the remote, helping maintain a tidy and up-to-date translation repository.

---

## ⚙️ Basic example

To integrate the `clean-up` action into your workflow, add the following to your `.github/workflows/clean_up.yml` file.
Here is an example for the numpy.org translations repo.

```yaml
name: Clean Up

on:
  schedule:
    - cron: "0 3 * * 0" # Runs every Sunday at 3 AM
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Clean up
        uses: Scientific-Python-Translations/clean-up@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          # Provided by user
          translations-repo: "Scientific-Python-Translations/numpy.org-translations"
          translations-ref: "main"
          # Provided by organization secrets
          gpg-private-key: ${{ secrets.GPG_PRIVATE_KEY }}
          passphrase: ${{ secrets.PASSPHRASE }}
          token: "not-a-real-token"
          crowdin-token: ${{ secrets.CROWDIN_TOKEN }}
```

This configuration schedules the cleanup to run weekly and also allows manual triggering.

## 🛠️ Inputs

| Input               | Required | Default | Description                                                |
| ------------------- | -------- | ------- | ---------------------------------------------------------- |
| `translations-repo` | ✅       | —       | The GitHub repository to sync the translated content into. |
| `translations-ref`  | ❌       | `main`  | The branch in the translations repository to sync into.    |

## 🤖 Bot Activity

All synchronization pull requests and automated commits are performed by the dedicated bot account:
[@scientificpythontranslations](https://github.com/scientificpythontranslations)

This ensures consistent and traceable contributions from a centralized automation identity.
If you need to grant permissions or configure branch protection rules, make sure to allow actions and PRs from this bot.

## 🙌 Community & Support

- Join the [Scientific Python Discord](https://scientific-python.org/community/) and visit the `#translation` channel
- Browse the [Scientific Python Translations documentation](https://scientific-python-translations.github.io/docs/)
- Visit the [content-sync](https://github.com/Scientific-Python-Translations/content-sync) and [translations-sync](https://github.com/Scientific-Python-Translations/translations-sync) Github actions.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## 📄 License

This project is licensed under the [MIT License](LICENSE.txt).
