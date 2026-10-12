# Editorial publishing

The approved public article records live in `editorial-articles.json`. They are
rendered using `editorial-template.html.tmpl`, a snapshot of the current article
shell. Research notes, demand hypotheses, draft revisions and review evidence
are not stored in the public repository.

To regenerate editorial content only, without rebuilding the homepage,
services or portfolio:

```sh
python3 source/build_editorial.py
python3 tools/check_site.py .
python3 tools/check_editorial.py .
```

`build_editorial.py` writes article pages, adds their cards to Recursos, preserves
existing sitemap entries and extends the page index. Repeated runs are
idempotent. `source/build.py` invokes the editorial renderer at the end of a full
legacy rebuild so these additions are not dropped. Prefer the editorial-only
command for article updates; a full rebuild affects the whole site.

Keep `datePublished` immutable. Change `dateModified` only for a meaningful
content update. Metadata, visible dates and structured data must agree.
External requirements, pricing and platform behavior need source revalidation
before publication. Editorial recommendations and hypothetical examples must
remain distinguishable from verified provider facts and client results.

Generation does not approve articles, schedule publishing, deploy the site or
request search-engine indexing. Confirm the production commit, existing CI,
HTTPS responses and visible content after an authorized deployment.
