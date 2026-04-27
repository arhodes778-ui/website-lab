#!/usr/bin/env python3
"""Weekly blog post generator for aistrion.com"""

import os
import re
import sys
from datetime import datetime
import anthropic


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def read_topics():
    with open('topics.txt', 'r', encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip() and not l.startswith('#')]


def write_topics(topics):
    with open('topics.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(topics) + '\n')


def generate_article(client, topic, slug, date_str, month_year):
    system_prompt = (
        "You are writing blog articles for Aistrion, a UK web design agency. "
        "Audience: UK small business owners who need help with their websites. "
        "Tone: direct, honest, practical, no fluff. British English spelling throughout. "
        "You must return a COMPLETE, valid HTML file and nothing else — "
        "no markdown fences, no explanation, just raw HTML starting with <!DOCTYPE html>."
    )

    existing_articles = (
        "blog-core-web-vitals.html (Performance), "
        "blog-website-checklist.html (Strategy), "
        "blog-cro-vs-redesign.html (Design), "
        "blog-website-cost.html (Pricing), "
        "blog-get-on-google.html (SEO), "
        "blog-wordpress-vs-custom.html (Strategy), "
        "blog-landing-page.html (Design), "
        "blog-website-mistakes.html (Strategy), "
        "blog-how-long-website.html (Strategy), "
        "blog-website-vs-social-media.html (Strategy), "
        "blog-website-brief.html (Strategy), "
        "blog-choose-web-designer.html (Strategy), "
        "blog-website-maintenance.html (Pricing), "
        "blog-stock-photos.html (Design), "
        "blog-local-seo.html (SEO), "
        "blog-get-more-leads.html (Strategy)"
    )

    prompt = f"""Write a complete blog article HTML file for the topic: "{topic}"

Details:
- Filename: blog-{slug}.html
- Canonical URL: https://aistrion.com/blog-{slug}.html
- Date: {date_str} | Display date: {month_year}
- Choose ONE tag from: SEO, Design, Strategy, Performance, Pricing
- Reading time: estimate accurately (4–8 min)
- Article body: minimum 800 words, British English, practical and specific
- Include at least 3 h2 sections, supporting h3s where needed
- Include at least one .callout box with a useful insight
- You may add one extra CSS component if useful (e.g. a grid, list, table)
- End the article body with a paragraph mentioning Aistrion naturally
- 4 FAQ items with real, specific answers
- 2 related article links chosen from: {existing_articles}
- CTA heading and sentence relevant to the topic

Use this EXACT HTML structure — replace [...] placeholders with your content.
CSS variables: --canvas:#F7F6F3  --surface:#FFFFFF  --ink:#111111  --secondary:#787774  --border:#EAEAEA
Fonts: Instrument Serif (headings), Geist (body), Geist Mono (labels/mono)

<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[SEO title with main keyword] | Aistrion</title>
  <meta name="description" content="[max 155 chars]" />
  <meta name="author" content="Aistrion" />
  <link rel="canonical" href="https://aistrion.com/blog-{slug}.html" />
  <link rel="icon" href="favicon.ico" sizes="any" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png" />
  <link rel="apple-touch-icon" href="favicon-192x192.png" />

  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://aistrion.com/blog-{slug}.html" />
  <meta property="og:title" content="[OG title]" />
  <meta property="og:description" content="[OG description]" />
  <meta property="og:image" content="https://aistrion.com/og-image.jpg" />
  <meta name="twitter:card" content="summary_large_image" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "[headline]",
    "author": {{ "@type": "Organization", "name": "Aistrion" }},
    "publisher": {{ "@type": "Organization", "name": "Aistrion", "url": "https://aistrion.com" }},
    "datePublished": "{date_str}",
    "dateModified": "{date_str}",
    "description": "[description]"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{ "@type": "Question", "name": "[Q1]", "acceptedAnswer": {{ "@type": "Answer", "text": "[A1]" }} }},
      {{ "@type": "Question", "name": "[Q2]", "acceptedAnswer": {{ "@type": "Answer", "text": "[A2]" }} }},
      {{ "@type": "Question", "name": "[Q3]", "acceptedAnswer": {{ "@type": "Answer", "text": "[A3]" }} }},
      {{ "@type": "Question", "name": "[Q4]", "acceptedAnswer": {{ "@type": "Answer", "text": "[A4]" }} }}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://aistrion.com" }},
      {{ "@type": "ListItem", "position": 2, "name": "Insights", "item": "https://aistrion.com/blog.html" }},
      {{ "@type": "ListItem", "position": 3, "name": "[article title]", "item": "https://aistrion.com/blog-{slug}.html" }}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" />

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --canvas: #F7F6F3; --surface: #FFFFFF; --ink: #111111;
      --secondary: #787774; --border: #EAEAEA;
      --serif: 'Instrument Serif', Georgia, serif;
      --sans: 'Geist', system-ui, sans-serif;
      --mono: 'Geist Mono', monospace;
    }}
    html {{ background: var(--canvas); color: var(--ink); font-family: var(--sans); }}
    body {{ min-height: 100vh; }}
    nav {{
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 24px 48px;
      background: rgba(247,246,243,0.9); backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
    }}
    .nav-logo {{ font-family: var(--serif); font-size: 1.2rem; color: var(--ink); text-decoration: none; }}
    .nav-back {{ font-size: 0.78rem; font-weight: 500; color: var(--secondary); text-decoration: none; letter-spacing: 0.04em; transition: color 200ms; }}
    .nav-back:hover {{ color: var(--ink); }}
    .article-wrap {{ max-width: 720px; margin: 0 auto; padding: 140px 32px 120px; }}
    .article-tag {{ font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--secondary); display: inline-flex; align-items: center; gap: 8px; margin-bottom: 32px; }}
    .article-tag::before {{ content: ''; width: 24px; height: 1px; background: var(--secondary); }}
    h1 {{ font-family: var(--serif); font-size: clamp(2.2rem, 4vw, 3.4rem); line-height: 1.1; letter-spacing: -0.025em; color: var(--ink); margin-bottom: 24px; }}
    .article-meta {{ font-size: 0.82rem; color: var(--secondary); margin-bottom: 64px; padding-bottom: 32px; border-bottom: 1px solid var(--border); }}
    .article-body h2 {{ font-family: var(--serif); font-size: 1.7rem; letter-spacing: -0.02em; color: var(--ink); margin: 56px 0 20px; line-height: 1.2; }}
    .article-body h3 {{ font-family: var(--sans); font-size: 1rem; font-weight: 600; color: var(--ink); margin: 36px 0 12px; }}
    .article-body p {{ font-size: 1.02rem; line-height: 1.85; color: #333; margin-bottom: 20px; }}
    .article-body strong {{ color: var(--ink); font-weight: 600; }}
    .article-body ul {{ margin: 0 0 20px 24px; }}
    .article-body ul li {{ font-size: 1.02rem; line-height: 1.85; color: #333; margin-bottom: 8px; }}
    .callout {{ background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--ink); border-radius: 6px; padding: 24px 28px; margin: 32px 0; }}
    .callout p {{ margin: 0; font-size: 0.95rem; color: var(--secondary); }}
    .callout strong {{ color: var(--ink); }}
    [OPTIONAL EXTRA CSS COMPONENT IF NEEDED]
    .article-cta {{ margin-top: 80px; padding: 48px; background: var(--ink); border-radius: 12px; text-align: center; }}
    .article-cta h2 {{ font-family: var(--serif); font-size: 1.8rem; color: var(--canvas); margin-bottom: 12px; }}
    .article-cta p {{ font-size: 0.92rem; color: rgba(247,246,243,0.6); margin-bottom: 28px; }}
    .article-cta a {{ display: inline-flex; align-items: center; gap: 8px; background: var(--canvas); color: var(--ink); font-size: 0.85rem; font-weight: 500; padding: 14px 28px; border-radius: 6px; text-decoration: none; }}
    .article-faq {{ margin-top: 64px; border-top: 1px solid var(--border); padding-top: 48px; }}
    .article-faq h2 {{ font-family: var(--serif); font-size: 1.7rem; color: var(--ink); margin-bottom: 32px; letter-spacing: -0.02em; }}
    .faq-item-article {{ margin-bottom: 28px; padding-bottom: 28px; border-bottom: 1px solid var(--border); }}
    .faq-item-article:last-child {{ border-bottom: none; }}
    .faq-item-article h3 {{ font-family: var(--sans); font-size: 0.95rem; font-weight: 600; color: var(--ink); margin-bottom: 8px; }}
    .faq-item-article p {{ font-size: 0.9rem; line-height: 1.75; color: var(--secondary); margin: 0; }}
    .related-articles {{ margin-top: 56px; }}
    .related-articles h2 {{ font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--secondary); margin-bottom: 20px; }}
    .related-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: var(--border); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
    .related-card {{ background: var(--surface); padding: 28px 24px; text-decoration: none; display: flex; flex-direction: column; gap: 10px; transition: background 200ms; }}
    .related-card:hover {{ background: var(--canvas); }}
    .related-tag {{ font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--secondary); }}
    .related-title {{ font-size: 0.9rem; font-weight: 500; color: var(--ink); line-height: 1.45; }}
    @media (max-width: 768px) {{
      nav {{ padding: 16px 20px; }}
      .article-wrap {{ padding: 100px 20px 80px; }}
      .related-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-8WTC2VDN44"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-8WTC2VDN44');
  </script>
</head>
<body>

  <nav>
    <a href="/" class="nav-logo">Aistrion</a>
    <a href="/blog.html" class="nav-back">← Back to blog</a>
  </nav>

  <article class="article-wrap">
    <div class="article-tag">[TAG]</div>
    <h1>[H1 title]</h1>
    <p class="article-meta">By Aistrion &nbsp;·&nbsp; {month_year} &nbsp;·&nbsp; [N] min read</p>

    <div class="article-body">
      [FULL ARTICLE BODY]
    </div>

    <div class="article-faq">
      <h2>Frequently asked questions</h2>
      <div class="faq-item-article"><h3>[Q1]</h3><p>[A1]</p></div>
      <div class="faq-item-article"><h3>[Q2]</h3><p>[A2]</p></div>
      <div class="faq-item-article"><h3>[Q3]</h3><p>[A3]</p></div>
      <div class="faq-item-article"><h3>[Q4]</h3><p>[A4]</p></div>
    </div>

    <div class="related-articles">
      <h2>More from Aistrion</h2>
      <div class="related-grid">
        <a href="[related1.html]" class="related-card"><span class="related-tag">[TAG]</span><span class="related-title">[Title]</span></a>
        <a href="[related2.html]" class="related-card"><span class="related-tag">[TAG]</span><span class="related-title">[Title]</span></a>
      </div>
    </div>

    <div class="article-cta">
      <h2>[CTA heading]</h2>
      <p>[CTA supporting sentence]</p>
      <a href="/book.html">Start a conversation →</a>
    </div>

  </article>

</body>
</html>"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def extract_tag(html):
    match = re.search(r'<div class="article-tag">(\w+)</div>', html)
    return match.group(1) if match else 'Strategy'


def extract_h1(html):
    match = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    return ''


def extract_excerpt(html):
    # First paragraph inside article-body
    match = re.search(
        r'<div class="article-body">\s*<p>(.*?)</p>',
        html, re.DOTALL
    )
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if len(text) > 160:
            text = text[:157].rsplit(' ', 1)[0] + '...'
        return text
    return ''


def update_blog_html(slug, tag, title, excerpt, month_year):
    with open('blog.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Increment article count
    count_match = re.search(r'(\d+) articles', content)
    if count_match:
        new_count = int(count_match.group(1)) + 1
        content = content.replace(
            count_match.group(0), f'{new_count} articles', 1
        )

    new_card = f"""
      <a href="blog-{slug}.html" class="article-card" data-tag="{tag}">
        <div class="card-top">
          <span class="card-tag">{tag}</span>
          <span class="card-date">{month_year}</span>
        </div>
        <div class="card-title">{title}</div>
        <div class="card-excerpt">{excerpt}</div>
        <span class="card-link">Read article →</span>
      </a>
"""

    # Insert right after the <!-- Newest first --> comment
    content = content.replace(
        '<!-- Newest first -->',
        '<!-- Newest first -->' + new_card,
        1
    )

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(content)


def update_sitemap(slug, date_str):
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    new_url = (
        f'  <url>\n'
        f'    <loc>https://aistrion.com/blog-{slug}.html</loc>\n'
        f'    <lastmod>{date_str}</lastmod>\n'
        f'    <changefreq>never</changefreq>\n'
        f'    <priority>0.7</priority>\n'
        f'  </url>\n'
    )

    content = content.replace('</urlset>', new_url + '</urlset>')

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print('Error: ANTHROPIC_API_KEY not set')
        sys.exit(1)

    topics = read_topics()
    if not topics:
        print('No topics remaining in topics.txt — add more to continue.')
        sys.exit(0)

    topic = topics[0]
    remaining = topics[1:]

    print(f'Generating: {topic}')

    now = datetime.utcnow()
    date_str = now.strftime('%Y-%m-%d')
    month_year = now.strftime('%b %Y')
    slug = slugify(topic)

    client = anthropic.Anthropic(api_key=api_key)
    html = generate_article(client, topic, slug, date_str, month_year)

    filename = f'blog-{slug}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Created: {filename}')

    tag = extract_tag(html)
    title = extract_h1(html)
    excerpt = extract_excerpt(html)

    update_blog_html(slug, tag, title, excerpt, month_year)
    update_sitemap(slug, date_str)
    write_topics(remaining)

    print(f'Done. Topics remaining: {len(remaining)}')


if __name__ == '__main__':
    main()
