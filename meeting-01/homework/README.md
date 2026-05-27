# Meeting 01 Homework: Alloy Metrics + Logs + Log-Based Dashboard

## Scenario
You are given a small service stack:
- `nginx` serves traffic and writes access/error logs.
- `nginx-exporter` exposes NGINX metrics.
- `loadgen` generates healthy and error traffic.
- `mimir`, `loki`, and `grafana` are running.
- `alloy` is running with an incomplete starter config.

Your task is to complete Alloy configuration and build an investigation dashboard in Grafana.

## Minimum Required Tasks
1. Configure metrics scraping in Alloy for `nginx-exporter:9113`. (hint: prometheus.scrape block)
2. Configure logs scraping in Alloy from NGINX log files. (hint: loki.file_match, loki.source.file, loki.write but can be done differently)
3. Parse NGINX access logs and add at least `status` as a log label. (hint: loki.process block)
4. Build one panel based on scraped metrics that shows request throughput or exporter availability:

Suggested scraped-metric panel queries (PromQL, datasource `Mimir`):
```promql
sum(rate(nginx_http_requests_total[1m]))
```

```promql
avg(nginx_up)
```
## Additional Tasks (More Points)
1. Build one log-based metric query in Grafana (datasource `Loki`).
2. Build a dashboard panel from that log-based metric.

Create a Grafana panel using a Loki query such as:
```logql
sum(count_over_time({job="nginx",status="500"}[1m]))
```

Error rate from logs (%):
```logql
100 *
sum(count_over_time({job="nginx",status=~"5.."}[1m]))
/
sum(count_over_time({job="nginx"}[1m]))
```


## Start The Homework Lab
```bash
cd meeting-01/homework
docker compose up -d
docker compose ps
```

Open:
- Grafana: `http://localhost:3000`
- NGINX exporter metrics: `http://localhost:9113/metrics`
- Alloy UI/metrics: `http://localhost:12347`

## Files Students Should Edit
- [alloy/config.alloy](meeting-01/homework/alloy/config.alloy)


## Suggested Validation Steps
1. Check that NGINX metrics are in Mimir: PromQL -> **nginx_up** metric is present etc. 

2. Check that NGINX logs are in Loki: Loki query -> **{job="nginx"} |= ``** etc.

3. Check that status labels exist in logs: Loki query -> **{status="200"} |= ``** etc. (label comes from loki.process block in alloy)


## Expected Deliverables
- Updated Alloy config
- Screenshot of NGINX metrics query in Grafana Explore
- Screenshot of NGINX logs query in Grafana Explore
- Screenshot of a dashboard panel showing request error rate from scraped metrics
- Optional: screenshot of a dashboard panel showing 5xx rate using Loki datasource.
