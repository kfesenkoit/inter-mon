# Meeting 03 Incident Lab

## Scenario
The service begins failing because a dependency becomes unavailable. The team must detect the issue, assess impact, mitigate it, and write a blameless postmortem.

## Roles
- Incident Commander
- Investigator
- Communications Lead
- Scribe

## Start Or Reuse The Lab
```bash
cd meeting-03/lab
docker compose up -d
docker compose ps
```

## Fault Injection
Primary scenario:
```bash
cd meeting-03/lab
docker compose stop mythical-database
```

Recovery:
```bash
cd meeting-03/lab
docker compose start mythical-database
```

Optional alternate scenario:
```bash
cd meeting-03/lab
docker compose stop mythical-queue
docker compose start mythical-queue
```

## Student Tasks
1. Detect the issue from the SLI/SLO dashboard, a logs query, or a trace search.
2. State which user-visible behavior is affected.
3. Define the impacted SLI.
4. Estimate impact using duration, error rate, or affected endpoints.
5. Restore the failed dependency.
6. Write a postmortem using the provided template.

## Inspect Incident Signals
Check service status:
```bash
docker compose ps
```

Check the API directly:
```bash
curl -i http://localhost:4000/unicorn
```

Query recent server logs:
```bash
curl -G 'http://localhost:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={service_name="mythical-server"}' \
  --data-urlencode 'limit=10'
```

Query error-related logs:
```bash
curl -G 'http://localhost:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={service_name="mythical-server"} |= "FAILURE"' \
  --data-urlencode 'limit=10'
```

Query stored request metrics:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=traces_spanmetrics_calls_total'
```

Check whether the incident appears as HTTP errors:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=sum(rate(traces_spanmetrics_calls_total{http_status_code=~"5.."}[5m]))'
```

Check whether the incident appears as latency degradation:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=sum(rate(traces_spanmetrics_latency_sum{span_kind="SPAN_KIND_SERVER",http_target!~"/debug/pprof.*"}[5m]))%20/%20sum(rate(traces_spanmetrics_latency_count{span_kind="SPAN_KIND_SERVER",http_target!~"/debug/pprof.*"}[5m]))'
```

Use Grafana Explore during the exercise for readable results. The `curl` commands are mainly useful for proving which backend holds each signal.

## Suggested SLI Candidates
Primary SLI for the database-stop incident: p95 server latency:
```promql
histogram_quantile(
  0.95,
  sum(rate(traces_spanmetrics_latency_bucket{
    span_kind="SPAN_KIND_SERVER",
    http_target!~"/debug/pprof.*"
  }[5m])) by (le)
)
```

Simple latency SLI: average server latency:
```promql
sum(rate(traces_spanmetrics_latency_sum{
  span_kind="SPAN_KIND_SERVER",
  http_target!~"/debug/pprof.*"
}[5m]))
/
sum(rate(traces_spanmetrics_latency_count{
  span_kind="SPAN_KIND_SERVER",
  http_target!~"/debug/pprof.*"
}[5m]))
```

Optional SLI when the fault produces HTTP 5xx: availability of API requests:
```promql
1 - (
  sum(
    rate(traces_spanmetrics_calls_total{
      span_kind="SPAN_KIND_SERVER",
      http_status_code=~"5..",
      http_target!~"/debug/pprof.*"
    }[5m])
  )
  /
  sum(
    rate(traces_spanmetrics_calls_total{
      span_kind="SPAN_KIND_SERVER",
      http_status_code=~"[0-9]+",
      http_target!~"/debug/pprof.*"
    }[5m])
  )
)
```

Optional bucket-based latency success ratio:
```promql
sum(
  rate(traces_spanmetrics_latency_bucket{
    span_kind="SPAN_KIND_SERVER",
    http_target!~"/debug/pprof.*",
    le="<existing bucket value>"
  }[5m])
)
/
sum(
  rate(traces_spanmetrics_latency_count{
    span_kind="SPAN_KIND_SERVER",
    http_target!~"/debug/pprof.*"
  }[5m])
)
```

