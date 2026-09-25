# Adi - Annotated — Personal Writing & Book Review Site

A personal website that showcases my writing (short stories and other pieces) alongside reviews of books I've read, built around an interactive graph that visualizes my reading history. Built with Django, PostgreSQL, and D3.js.

## Why I'm building this

I started writing book reviews after hearing it's a good way to improve writing skill, and I write short stories on the side. This project is both:

1. A place to actually showcase that writing instead of it sitting in random files.
2. A way to learn full-stack web development beyond what I'd covered so far (Python/Flask basics from Angela Yu's 100 Days of Python) — specifically Django, relational database design, data visualization with D3.js, and web security fundamentals (auth, hashing, content protection).

This is a learning project as much as a portfolio piece, so the README will track what I actually learned along the way, not just the finished feature list.

## Features

- **Interactive reading graph** — every book I've read, plotted with year-read on the y-axis and a switchable x-axis (publish date / rating / my difficulty rating), color-coded by genre, dots sized depending on page count, with reviewed books marked and clickable.
- **Book reviews** — full write-ups for books I've reviewed, rendered from Markdown.
- **Stories** — short fiction and other writing, also Markdown-based.
- **Comments & voting** — signed-in users can comment and upvote/downvote on reviews and stories.
- **Contact form** — sends a message straight to my inbox.
- **Admin panel** — private, 2FA-protected panel (Django Admin) for adding books and managing content.
- **Content protection** — full review/story text is gated behind sign-in to deter scraping; teasers are visible to everyone.

## Tech stack

| Layer                  | Choice                                           |
| ---------------------- | ------------------------------------------------ |
| Backend                | Django                                           |
| Database               | PostgreSQL                                       |
| Frontend interactivity | Vanilla JS, D3.js (graph), htmx (comments/votes) |
| Auth                   | Django's built-in auth system                    |
| Markdown rendering     | Python `markdown` library                        |
| Email (contact form)   | Resend                                           |
| Hosting                | Railway / Render (TBD)                           |

_(See `docs/project-guide.md` for the full build plan and reasoning behind these choices.)_

## What I'm learning

Updating this section as I go — a running log rather than a finished claim.

- [✅] Django fundamentals (models, views, templates, admin) coming from a Flask background
- [✅] Relational database design (books, reviews, stories, comments, votes)
- [✅] D3.js — scales, axes, data joins, transitions
- [✅] Building a data-driven admin workflow instead of hardcoding content
- [ ] Authentication & session handling, password hashing
- [ ] htmx for dynamic UI without a JS framework
- [ ] Basic web security: CSRF, rate limiting, 2FA, safely gating content server-side
- [ ] Deploying a Django app with a managed Postgres database

## Project status

🚧 In progress - setting up user authentication next :p

## Roadmap / ideas for later

- Search/filter across reviews and stories
- Reading stats page (pages read per year, genre breakdown, etc.)

## License / Copyright

All written content (reviews, stories, and other text) on this site is © [Adi Golos] [2026] and is not licensed for reuse or redistribution.

## Contact

Questions, feedback, or found a bug? Reach out via the contact form on the site.
