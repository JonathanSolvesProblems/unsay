"""Static archive page for the retired Unsay demo.

The hackathon is over and the CockroachDB Cloud cluster behind the live demo
has been torn down, so the interactive app cannot run. Its URL is printed in
the README, the demo video description, the blog post and the Devpost entry,
and all of those are permanent. A dead link there would be worse than a page
that explains itself.

This handler has no dependencies and touches nothing: no database, no Bedrock,
no network. It returns one string. Lambda bills nothing while idle and the
free tier covers any traffic a retired project sees, so the links in every
public artifact keep working at zero cost, which is the whole point.

Deployed as its own zip with handler `archive_handler.handler`.
"""

from __future__ import annotations

REPO = "https://github.com/JonathanSolvesProblems/unsay"
VIDEO = "https://www.youtube.com/watch?v=UiWwvPHfN3A"
WRITEUP = ("https://jonathanandrei.com/blog/"
           "unsay-agent-memory-cockroachdb-bitemporal-fda-recalls")
DEVPOST = "https://devpost.com/software/unsay"

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Unsay: archived</title>
<style>
  :root{{
    --ink:#171512; --paper:#faf8f4; --card:#fff; --rule:#e2ddd3; --muted:#6f6a61;
    --stop:#9d1c09; --stop-bg:#fdeceb; --caution:#8a5300; --caution-bg:#fdf4e3;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--paper);color:var(--ink);
       font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Inter,sans-serif;
       display:flex;align-items:center;justify-content:center;
       min-height:100vh;padding:32px 20px}}
  .wrap{{max-width:640px;width:100%}}
  .mark{{font-size:64px;font-weight:850;letter-spacing:-.05em;line-height:1}}
  .mark .say{{position:relative;color:var(--stop)}}
  .mark .say:after{{content:"";position:absolute;left:-3%;right:-3%;top:42%;
                   height:.085em;background:var(--stop);border-radius:3px}}
  .tag{{color:var(--muted);font-size:18px;margin-top:14px}}
  .notice{{background:var(--card);border:1px solid var(--rule);
          border-left:5px solid var(--caution);border-radius:10px;
          padding:20px 22px;margin:34px 0}}
  .notice b{{display:block;margin-bottom:6px}}
  .result{{background:var(--card);border:1px solid var(--rule);
          border-left:5px solid var(--stop);border-radius:10px;
          padding:20px 22px;margin-bottom:34px}}
  ul{{list-style:none}}
  li{{padding:11px 0;border-bottom:1px solid var(--rule)}}
  li:last-child{{border-bottom:none}}
  a{{color:#1b4ed8}}
  .what{{color:var(--muted);font-size:14.5px;margin-top:3px}}
  footer{{color:var(--muted);font-size:13.5px;margin-top:30px;line-height:1.55}}
</style>
</head>
<body>
<div class="wrap">
  <div class="mark">Un<span class="say">say</span></div>
  <p class="tag">Agent memory that goes back and corrects the answers it already gave.</p>

  <div class="result">
    <b>2nd place, CockroachDB &times; AWS Hackathon: Build with Agentic Memory.</b>
    Judged across 3,700 participants. The entry is still public, and so is
    everything it was built from.
  </div>

  <div class="notice">
    <b>The live demo is retired.</b>
    It ran on a CockroachDB Cloud cluster that was torn down when judging
    closed, because leaving a paid database running past a hackathon is how you
    get a surprise bill. Everything below still works, and the repository
    rebuilds the whole thing from scratch against live openFDA data.
  </div>

  <ul>
    <li><a href="{VIDEO}">Watch the 2:34 demo</a>
      <div class="what">The full scenario against the live cluster, recorded while it ran.</div></li>
    <li><a href="{REPO}">Source on GitHub, MIT</a>
      <div class="what">Includes TESTING.md, which reproduces every claim from a clean clone.</div></li>
    <li><a href="{WRITEUP}">Long-form write-up</a>
      <div class="what">Why stale context is the failure mode retrieval quality cannot fix.</div></li>
    <li><a href="{DEVPOST}">The submission on Devpost</a>
      <div class="what">Build notes, the architecture diagram, and what I got wrong.</div></li>
  </ul>

  <footer>
    Built on CockroachDB Cloud, AWS Lambda and Amazon Bedrock, over live
    openFDA recall data. Patient records in the demo were synthetic and
    disclosed as such. This page is unmaintained.
  </footer>
</div>
</body>
</html>"""


def handler(event, context):
    """Return the archive page for every path and method."""
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html; charset=utf-8",
            # A retired page should not be re-fetched constantly, but an hour
            # keeps it editable without fighting a stale cache.
            "cache-control": "public, max-age=3600",
        },
        "body": PAGE,
    }
