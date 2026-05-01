# SALS — Command Reference

## Table of Contents

- [Setup](#setup)
- [Development](#development)
- [Database](#database)
- [Translation (i18n)](#translation-i18n)
- [File Storage](#file-storage)
- [Deployment](#deployment)
- [Useful Scripts](#useful-scripts)

---

## Setup

```bash
# Clone and enter project
cd SALS/

# Activate virtual environment
source .venv/bin/activate
# or
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install django-rosetta deep-translator

# Install system dependency for translations
sudo apt install gettext

# Create .env file (copy from example and fill in values)
cp .env.example .env
```

### Required `.env` variables

```
SECRET_KEY=
DEBUG=True
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
RENDER_EXTERNAL_HOSTNAME=   # production only
```

---

## Development

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Check for errors without running
python manage.py check

# Create superuser (admin)
python manage.py createsuperuser

# Open Django shell (interactive Python with Django loaded)
python manage.py shell
```

---

## Database

```bash
# Create migration files after changing models.py
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show all migrations and their status
python manage.py showmigrations

# Rollback a specific migration
python manage.py migrate loan_app 0014

# View raw SQL for a migration
python manage.py sqlmigrate loan_app 0001
```

---

## Translation (i18n)

### Workflow — adding new translations

```bash
# Step 1: Scan all files and update .po file
python manage.py makemessages -l bn --ignore=.venv --ignore=venv

# Step 2: Manually edit translations in .po file
nano locale/bn/LC_MESSAGES/django.po

# Step 3: Compile translations (must run after every edit)
python manage.py compilemessages
```

### Rules for developers

- In Python (views.py): wrap strings with `_("your string")`
- In templates: add `{% load i18n %}` at top, then `{% trans "your string" %}`
- F-strings: use `_("Hello %s") % variable` instead of `_(f"Hello {variable}")`
- After adding any new string: run `makemessages` → edit `.po` → `compilemessages`

### Auto-mark strings in views.py

```bash
python3 - << 'EOF'
import re

with open('loan_app/views.py', 'r') as f:
    content = f.read()

if 'from django.utils.translation import gettext' not in content:
    content = content.replace(
        'from django.shortcuts import',
        'from django.utils.translation import gettext as _\nfrom django.shortcuts import'
    )

content = re.sub(
    r'(messages\.\w+\(request,\s*)"([^"]*)"',
    r'\1_("\2")',
    content
)

with open('loan_app/views.py', 'w') as f:
    f.write(content)

print("Done")
EOF
```

### Auto-wrap strings in templates

```bash
# Backup templates first
cp -r templates/ templates_backup/

python3 - << 'EOF'
import os
import re

template_dir = 'templates'

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if not file.endswith('.html'):
            continue

        path = os.path.join(root, file)
        with open(path, 'r') as f:
            content = f.read()

        if '{% load i18n %}' in content:
            continue

        content = '{% load i18n %}\n' + content

        content = re.sub(
            r'>([A-Z][^<>{%}]+?)<',
            lambda m: '>{% trans "' + m.group(1).strip() + '" %}<' if m.group(1).strip() else m.group(0),
            content
        )

        with open(path, 'w') as f:
            f.write(content)

        print(f"✓ {path}")

print("Done")
EOF

# Restore if something breaks
# rm -rf templates/ && cp -r templates_backup/ templates/
```

### Auto-translate .po file using Google Translate

```bash
pip install deep-translator

python3 - << 'EOF'
from deep_translator import GoogleTranslator
import time

translator = GoogleTranslator(source='en', target='bn')

with open('locale/bn/LC_MESSAGES/django.po', 'r') as f:
    lines = f.readlines()

result = []
i = 0
while i < len(lines):
    line = lines[i]
    result.append(line)
    if line.startswith('msgid "') and line.strip() != 'msgid ""':
        text = line[7:-2]
        i += 1
        next_line = lines[i]
        if next_line.strip() == 'msgstr ""':
            try:
                translated = translator.translate(text)
                result.append(f'msgstr "{translated}"\n')
                print(f"✓ {text[:40]}")
                time.sleep(0.3)
            except Exception as e:
                print(f"✗ failed: {text[:40]} — {e}")
                result.append(next_line)
        else:
            result.append(next_line)
    i += 1

with open('locale/bn/LC_MESSAGES/django.po', 'w') as f:
    f.writelines(result)

print("Done")
EOF
```

### Check translation stats

```bash
# Total strings
grep -c "msgid" locale/bn/LC_MESSAGES/django.po

# Untranslated strings
grep -c 'msgstr ""' locale/bn/LC_MESSAGES/django.po

# View all translations
grep -A1 "msgid" locale/bn/LC_MESSAGES/django.po
```

---

## File Storage

- Locally: files go to `SALS/media/` (requires `MEDIA_ROOT = BASE_DIR / 'media'` in settings)
- Production: files go to Cloudinary automatically
- Accepted formats: PNG, JPG, PDF (for NID and land documents)

### Fix PDF not showing in templates

Use URL-based detection instead of filename:

```django
{% with profile.nid_card_front.url as url %}
    {% if '.pdf' in url or '/raw/' in url %}
        <a href="{{ url }}" target="_blank">View PDF</a>
    {% else %}
        <img src="{{ url }}">
    {% endif %}
{% endwith %}
```

---

## Deployment (Render)

### build.sh

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
##apt-get install -y gettext
##python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py migrate
```

### Before deploying

```bash
# Collect static files locally to test
python manage.py collectstatic

# Make sure locale/ is committed
git add locale/
git add build.sh
git commit -m "Add Bengali translation"
git push
```

### Environment variables to set on Render

```
SECRET_KEY
DEBUG=False
CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
RENDER_EXTERNAL_HOSTNAME
DATABASE_URL

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Useful Scripts

### Check which venv is active

```bash
which python
```

### Install all dependencies fresh

```bash
pip install -r requirements.txt
pip install django-rosetta deep-translator
```

### Update requirements.txt after installing new packages

```bash
pip freeze > requirements.txt
```

### Find all untranslated strings in templates

```bash
grep -rn "{% trans" templates/ | wc -l
```

### Find all message strings in views

```bash
grep -n "messages\." loan_app/views.py
```

### Find all hardcoded strings not yet wrapped

```bash
grep -rn 'messages\..*"' loan_app/views.py | grep -v "_("
```

---


**Debugging section:**



```bash
# Check active venv
which python

# Check Django version
python manage.py version

# Check all installed packages
pip list

# Find untranslated strings in .po file
grep -B1 'msgstr ""' locale/bn/LC_MESSAGES/django.po | grep "msgid"

# Find strings not yet wrapped in templates
grep -rn "[A-Z][a-z]" templates/registration/ | grep -v "{%"

# Check for fuzzy translations (wrong auto-matches)
grep -n "fuzzy" locale/bn/LC_MESSAGES/django.po
```

**Git section:**



```bash
# Before committing translations always
python manage.py compilemessages
git add locale/
git add templates/
git add loan_app/views.py
git commit -m "Update translations"
git push
```

**Testing section:**



```bash
# Test Bengali version
http://127.0.0.1:8000/bn/

# Test English version  
http://127.0.0.1:8000/en/

# Test admin panel
http://127.0.0.1:8000/admin/

# Test rosetta translation UI
http://127.0.0.1:8000/rosetta/
```

---

### Removing fuzzy from .po file
This is still fuzzy because the `msgid` spans multiple lines in the `.po` file. The translation exists but Django won't use it while it's marked fuzzy.

Fix — remove the `#, fuzzy` and `#|` lines manually:

bash

```bash
nano locale/bn/LC_MESSAGES/django.po
```

Find every block with `#, fuzzy` and delete those lines, keeping only:

```
msgid "..."
msgstr "..."
```

Or do it automatically:

bash

```bash
python3 - << 'EOF'
with open('locale/bn/LC_MESSAGES/django.po', 'r') as f:
    lines = f.readlines()

result = []
for line in lines:
    if line.startswith('#, fuzzy') or line.startswith('#| '):
        continue
    result.append(line)

with open('locale/bn/LC_MESSAGES/django.po', 'w') as f:
    f.writelines(result)

print("Done")
EOF
```

Then compile:



```bash
python manage.py compilemessages
```
---

##### This finds all `{% trans` tags that don't have a closing `%}` on the same line.

```bash
grep -rn "{% trans" templates/ | grep -v "%}"
```
