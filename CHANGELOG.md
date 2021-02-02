- 12.15.2020 (marii)
  + [x] Removed `mkl-random` package from `requirements.txt`
    - Why: It requires Cython via Condas to install; wasn't being used
  + [x] Added Spacy model to `requirements.txt` / `Pipfile`
    - Why: now the English model will be versioned + automatically installed with `pipenv install` instead of installed manually / globally
  + [x] Moved files (e.g., scripts, notebooks, results) into directories to organize repo root
  + [x] Used `pipenv` for more modular + granular dependency management
  + [x] Used `pyenv` and locked `.python-version` to `3.8` to reduce vectors for error
  + [x] .gitignored caches
