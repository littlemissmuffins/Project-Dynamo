There is an Apache-style access log at `/app/access.log`. Parse it and write a
summary report to `/app/report.json`.

Write a JSON object to `/app/report.json` with exactly these three keys:

1. `total_requests` (integer) — the total number of non-blank log lines in
   `/app/access.log`.
2. `unique_ips` (integer) — the number of distinct client IP addresses (the
   first whitespace-separated token on each line).
3. `top_path` (string) — the request path (e.g. `/index.html`) that appears
   most often across the `"METHOD path HTTP/x.x"` portion of each line. If
   there is a tie, any one of the tied paths is acceptable.

Success criteria:

1. `/app/report.json` exists and contains valid JSON.
2. The JSON object has exactly the keys `total_requests`, `unique_ips`, and
   `top_path` — no extra keys, none missing.
3. `total_requests` and `unique_ips` exactly match the true counts computed
   from `/app/access.log`.
4. `top_path` is a path whose request count in the log equals the maximum
   request count of any path (i.e. it is a correct mode, ties permitted).
