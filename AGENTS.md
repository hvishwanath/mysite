# Repository Guidelines

## Project Structure & Module Organization

- `Takeout/` holds the Google Blogger export. The key blog data is under `Takeout/Blogger/Blogs/Harish Vishwanath_s Diary/` with `feed.atom`, `theme-layouts.xml`, and `theme-classic.html`.
- Images referenced by posts live in `Takeout/Blogger/Albums/Harish Vishwanath_s Diary/`.
- Comments and settings are in `Takeout/Blogger/Comments/` and `Takeout/Blogger/Blogs/Harish Vishwanath_s Diary/settings.csv`.
- There is no application source code or tests in this repository as-is; treat it as a content archive unless you add tooling.

## Build, Test, and Development Commands

- No build or test scripts are present. If you add processing scripts later, document them here with examples, such as `python scripts/convert.py` or `npm run build`.

## Coding Style & Naming Conventions

- No code style is enforced yet. If you add scripts, keep names descriptive and lower_snake_case (e.g., `export_posts.py`).
- Prefer small, single-purpose scripts and keep output under a `dist/` or `output/` directory to avoid modifying the raw `Takeout/` data.

## Testing Guidelines

- No tests exist currently. If you add tests, name them after the script or feature (e.g., `test_export_posts.py`) and document how to run them.

## Commit & Pull Request Guidelines

- This checkout has no Git history, so there are no established commit message conventions. Use short, imperative summaries (e.g., "Add Blogger export parser").
- For PRs, include a brief description of the data touched and any scripts added, plus sample output paths if new artifacts are generated.

## Data Handling Notes

- Treat `Takeout/` as source-of-truth data; avoid editing files in place.
- When transforming data, write new files to a separate directory and record the transformation steps in the README or a script header.
