# DevJournal Blog

A production-ready, multi-author blogging platform built with Django. It includes tags, comments, search, RSS, sitemap, and a modern admin UI.

## ✨ Features

- Published/draft workflow for posts
- Tags with counts and tag-based filtering
- Comment moderation (approved only)
- Search with highlighted results
- Pagination (8 posts per page)
- Related posts by shared tags
- RSS feed and sitemap
- Login-required post creation
- Responsive UI + Jazzmin admin theme

## 🧱 Tech Stack

- Django 5.2
- SQLite (default)
- Pillow (images)
- Jazzmin (admin UI)

## ✅ Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations:

```powershell
python manage.py migrate
```

4. Start the dev server:

```powershell
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## 🔑 Admin Login

If you’ve seeded the database, use:

- **Username:** `editor`
- **Password:** `Editor123!`

Admin panel: http://127.0.0.1:8000/admin/

## 🌐 URLs

- `/` — Home
- `/posts/` — All posts
- `/posts/<slug>/` — Post detail
- `/tag/<slug>/` — Tag filter
- `/search/?q=...` — Search
- `/author/<username>/` — Author posts
- `/rss/` — RSS feed
- `/sitemap.xml` — Sitemap

## 📦 Optional Docker Run

```powershell
docker build -t devjournal .
```

```powershell
docker run -p 8000:8000 devjournal
```

## 🗂 Project Structure

```
blog_project/
	manage.py
	blog_project/
		settings/
		urls.py
	blog/
		models.py
		views.py
		admin.py
	templates/
	static/
```

## ✅ Notes

- Public pages show **only published posts**.
- Draft posts are visible only in admin.
- Tags must exist before selecting them in the post form.

---

