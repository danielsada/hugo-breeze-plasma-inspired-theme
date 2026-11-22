# Breeze Plasma — a Hugo theme

A calm, KDE Plasma / Breeze-inspired blog theme. The wallpaper sits behind one translucent navigation panel, and everything you read is on opaque Breeze cards. It includes:

- **A Dolphin-style archive** with a *Show* pane (sections, series, tags and years, with counts), search, and URL-backed filters.
- **Posts with an "On this page" outline** in the panel. On phones it becomes a collapsible table of contents.
- **A projects page** and a **lazy YouTube player**. The player sends no requests to YouTube until you press play.
- **Automatic light/dark**, no web fonts and no external requests. Pages typically weigh under 100 KB.

Everything works without JavaScript. Sections, series and tags are real pages, and JavaScript only adds in-place filtering, search, the video player and the outline highlight.

## Requirements

**Hugo ≥ 0.158.0** (the standard edition is enough; extended isn't needed). Tested with 0.170.1.

The theme uses the template system introduced in 0.146 (`layouts/_partials`, `layouts/_markup` and so on). It also uses `hugo.Data` (0.156) and `Language.Name`/`Language.Locale` (0.158). Those versions deprecated `.Site.Data`, `languageCode` and `.Language.Lang`. On Netlify, set `HUGO_VERSION = "0.170.1"` (or newer).

The CSS relies on `light-dark()`, `color-mix()`, container queries and `:has()`. All evergreen browsers have supported these since 2024.

## Try the example site

```sh
git clone https://github.com/danielsada/hugo-breeze-plasma-inspired-theme
cd hugo-breeze-plasma-inspired-theme
hugo server -s exampleSite
# → http://localhost:1313/
```

`exampleSite/` exercises every feature:

- an English blog and a Spanish `notas` section;
- a three-part series, tags and years;
- projects, a talk and an About page;
- code, quotes, tables, figures and a table of contents.

`exampleSite/hugo.toml` lists every option with its default.

## Install

**Vendored (copy into your site):**

```sh
mkdir -p themes && cp -r path/to/hugo-breeze-plasma-inspired-theme themes/
```

Then add this to your `hugo.toml`:

```toml
theme = "hugo-breeze-plasma-inspired-theme"
```

**Hugo Module:**

```toml
[module]
  [[module.imports]]
    path = "github.com/danielsada/hugo-breeze-plasma-inspired-theme"
```

Then copy the `[markup]` block from `exampleSite/hugo.toml`. It enables class-based syntax highlighting, the table-of-contents levels and figures for titled images. Also consider `capitalizeListTitles = false`, which keeps tag and series names as you wrote them.

## Content model

| What | Where | Notes |
|---|---|---|
| Posts | Any section listed in `mainSections` (e.g. `content/blog/`, `content/notas/`) | Front matter: `title`, `date`, `description` (also the lead and the archive summary), `tags`, `series`, and `params.mark` (a small label in the archive, e.g. "Project"). |
| All posts | `content/posts/_index.md` with `params.archive: true` | Lists every post in `mainSections`. Change the path with `params.archive.path`. `params.subtitle` is shown in the title bar (HTML allowed). |
| Section metadata | The section's `_index.md` | `params.badge` (e.g. "ES"), `params.icon`, `params.lang`, `params.subtitle`, `params.backlabel`, and `params.card.{title,text,tint}` for the home section card. |
| Second-language section | Set `params.lang: es` in that section's `_index.md` | Its pages get `<html lang="es">` and Spanish UI strings, and a badge in mixed lists. "Latest posts" leaves them out (they get their own card). |
| Series | The `series` taxonomy | Needs at least `params.series.min` posts. Adds "Part n of m" and previous/next-in-series links, and its term page lists the posts oldest first. |
| Home intro | `content/_index.md` | `params.kicker`, `params.heading`, the page body, and `params.links: [{text, url \| ref \| latest: true}]`. |
| About and other pages | e.g. `content/about.md` | Shown as one card. `params.sayhi: true` appends email and social links. |
| Projects page | `content/projects.md` with `params.view: projects` | Rows come from `data/projects.yaml`. |
| Projects | `data/projects.yaml` | `name`, `status`, `since`, `summary`, `description`, `pitch` (home copy), `stack`, `icon`, `url`, `urllabel`, `writeup`, `writeuplabel`, `links`, `featured`. |
| Talks | `data/talks.yaml` | `title`, `event`, `year`, `youtube` (video id), `duration`, `poster`, `url`, `companion`, `companiontext`, `featured`. |

Videos inside posts use the `youtube-lite` shortcode:

```md
{{</* youtube-lite id="VIDEO_ID" title="What it is" duration="12:34" poster="poster.jpg" */>}}
```

Don't use Hugo's built-in `youtube` shortcode. It embeds the iframe on page load.

## Configuration

All options live under `[params]`. Every one is optional.

| Option | Default | What it does |
|---|---|---|
| `description`, `tagline` | — | Meta description; the subtitle under your name and the home kicker |
| `logo` | monogram | An `assets/` path (processed) or a `static/` path |
| `logowidth`, `logoplate`, `logoname` | `64`, `true`, `true` | Logo width in px, whether it sits on a light plate, and whether your name is shown beside it |
| `colorscheme` | `auto` | `auto`, `light` or `dark` |
| `favicon`, `ogimage`, `titlesuffix`, `crumbroot` | — | Head and breadcrumb details |
| `author.name`, `author.email`, `author.page` | — | Byline, contact and the About link |
| `colors.light.accent` / `.ink`, `colors.dark.accent` / `.ink` | Purple | Accent colours. `ink` is the text and focus-ring colour; keep it at least 4.5:1 against the card. |
| `colors.wall` | `#3d6fd6` | Wallpaper base colour |
| `wallpaper` | `breeze/wallpaper.svg` | An `assets/` path, a static path, or `"none"` |
| `fonts.sans`, `fonts.read`, `fonts.mono` | System stacks | CSS font stacks. `read` is the long-form reading face. |
| `archive.path`, `archive.taxonomy` | `/posts`, `tags` | The All-posts page and the taxonomy shown in rows |
| `archive.showtags`, `archive.rowtags`, `archive.search` | `8`, `2`, `true` | Tags in the Show pane, tags visible per row, and the search box |
| `series.taxonomy`, `series.min` | `series`, `2` | Series behaviour |
| `dates.short`, `dates.long` | `2 Jan 2006`, `2 January 2006` | Go date layouts for lists and for posts |
| `post.toc`, `post.progress`, `post.readingtime`, `post.anchors`, `post.postnav`, `post.byline` | All `true` | Post features. You can also turn the TOC off per page with `params.toc: false`. |
| `images.maxwidth`, `images.quality` | `960`, `75` | Settings for Markdown images, which are converted to WebP |
| `rss.panel` | `true` | Shows the RSS icon in the panel |
| `projects.page`, `projects.statuses` | `/projects`, `[Live, Beta, Paused, Archived]` | The projects page and the order of its status groups |
| `home.main`, `home.side` | intro, latest, recent / project, talk | The home widgets, in order (see below) |

### Navigation

`[[menus.main]]` becomes the panel's **Places** list. Each entry can set:

- `params.icon` — the name of any icon;
- `params.badge` — e.g. "ES";
- `params.count` — show the section's post count (on the All-posts entry it counts every post);
- `params.lang` — the language of the label.

`[[menus.social]]` becomes the **Elsewhere** icon row; set `params.icon` on each entry. The RSS icon is added automatically.

Without a main menu, Places lists the All-posts page and every main section. When you're on a post, the Places entry it belongs to is marked current.

### Home widgets

```toml
[[params.home.main]]
  widget = "intro"
[[params.home.main]]
  widget = "latest"   # count, sections, title
  count = 3
[[params.home.main]]
  widget = "recent"   # offset, count, sections, title, links = false
[[params.home.side]]
  widget = "project"  # title
[[params.home.side]]
  widget = "talk"     # title
[[params.home.side]]
  widget = "section"  # section (required), count, tint = "note" | "plain"
  section = "notas"
```

Add `enable = false` to hide a widget.

To add your own widget, create `layouts/_partials/home/<name>.html` in your site. It's called with `(dict "page" . "cfg" <its table>)`. The `main` widgets form the left column on wide screens. On phones they come first, followed by the `side` widgets.

### Icons

The icons are monochrome SVGs in `assets/breeze/icons/`, combined at build time into one cacheable sprite.

- **Add an icon:** drop `assets/breeze/icons/<name>.svg` into your site and use `<name>` anywhere an icon is accepted (menus, sections, projects).
- **Replace an icon:** use the same file name as the theme's icon.

The theme ships: blog, notas, series, apps, user, mail, github, linkedin, x, globe, link, rss, ext, folder, tag, cal, search, menu, close, toc, image, play, terminal, chart and box.

### Languages

UI strings live in `i18n/en.toml` and `i18n/es.toml`. To override any string for your site's language, put it in your own `i18n/<lang>.toml`. `all_posts_arrow` receives `.Count` (the number of posts), e.g. `other = "All {{ .Count }} posts →"`.

A section in a different language than the site (`params.lang` in its `_index.md`) uses that language's strings. The theme mounts its `i18n/` folder at `data/breeze/i18n/` for this. To add or override strings for such a section, create `data/breeze/i18n/<lang>.toml` in your site, using the same format.

### Styling and templates

- **Extra CSS:** create `assets/css/custom.css`. It's appended to the theme's stylesheet.
- **Head and body hooks:** override `layouts/_partials/hooks/head-end.html` and `hooks/body-end.html`.
- **Post-end hook:** override `layouts/_partials/hooks/post-end.html` to add something to the end of every post (a newsletter form, comments, a "subscribe" line). It renders inside the post card, after the tags and the series/older/newer links, with the page as context. The theme's copy is empty; when your hook outputs nothing, no wrapper or spacing is added. `exampleSite/layouts/_partials/hooks/post-end.html` shows a one-line RSS invitation.
- **Alternative page layouts:** set `params.view: <name>` on a page or section to render it with `layouts/_partials/views/<name>.html`, which receives the page as its context. The theme ships `post` and `page` (regular pages) and `projects` (any page). `archive` is used by sections and terms, and `terms` by taxonomy pages; both expect what those templates pass them, so they can't be picked with `params.view` on another kind of page.
- **Any other theme file:** copy it to the same path in your site and edit it.

## Performance and privacy

- The CSS and JavaScript are minified; they and the icon sprite are fingerprinted (cache forever). Markdown images are resized to WebP and lazy-loaded.
- Pages make no third-party requests. The YouTube iframe (youtube-nocookie) is created only after a click, and without JavaScript the player is a plain link.
- Focus is always visible, and the mobile drawer traps focus and makes the page behind it inert. The heading structure and lang attributes are correct, and contrast is at least 4.5:1 for text.

### Known limitations

- Year pages are year groups on the archive (`/posts/#y2025`), not separate pages. Hugo can't generate pages per year without front matter. Without JavaScript, a year link jumps to that year's group.
- The panel is hidden off-canvas on phones by an inline `html.js` marker. If inline scripts run but `script.js` is blocked, the drawer can't open.

## License

MIT
