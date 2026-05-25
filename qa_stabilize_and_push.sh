#!/usr/bin/env bash
set -euo pipefail

echo "== Z9CoachFree QA stabilization =="

# 1) Required folders for Streamlit/assets/PDF paths.
mkdir -p assets/logos assets/icons assets/backgrounds assets/pdf scripts
for d in assets/logos assets/icons assets/backgrounds assets/pdf; do
  touch "$d/.gitkeep"
done

# 2) Assessment log expected by app logging.
if [ ! -f assessment_log.json ]; then
  echo '[]' > assessment_log.json
fi

# 3) Restore fallback question bank if master_disc_questions.json was deleted.
if [ ! -f master_disc_questions.json ] && [ -f master_disc_questions1.json ]; then
  cp master_disc_questions1.json master_disc_questions.json
fi

# 4) Remove unused ConvertKit helper from tracking if present and not needed.
if [ -f convertkit_api.py ]; then
  mkdir -p archive/unused
  git mv convertkit_api.py archive/unused/convertkit_api.py 2>/dev/null || mv convertkit_api.py archive/unused/convertkit_api.py
fi

# 5) Install/runtime check. Missing Streamlit/numpy/matplotlib/fpdf in Pylance usually means the IDE interpreter is not using this environment.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 6) Static syntax check.
python -m compileall .

# 7) Optional Streamlit smoke test command shown but not launched automatically.
echo "Smoke test manually with: streamlit run z9CoachFree.py"

# 8) Commit and push.
git status --short
git add .
git commit -m "QA stabilize Z9CoachFree snapshot rebuild" || echo "No changes to commit."
git push
