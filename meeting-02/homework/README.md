# Meeting 02 Homework: Generate RED Metrics From Traces In Alloy

## Scenario
You are given a tracing-focused stack:
- `tracegen` continuously emits synthetic OTLP traces.
- `alloy` receives traces and should generate RED metrics from spans.
- `tempo` stores traces.
- `mimir` stores Prometheus-compatible metrics.
- `grafana` is used to query traces and metrics.

Your task is to implement the Alloy pipeline so RED metrics are generated from traces at Alloy level and pushed to Mimir.

## Minimum Required Tasks
1. Configure Alloy to receive OTLP traces.
2. Forward traces to Tempo.
3. Configure Alloy span-to-metrics generation (RED metrics).
4. Push generated RED metrics to Mimir.
5. Build one Grafana panel using generated RED metrics from Mimir.

## Additional Tasks (More Points)
1. Add extra RED dimensions (for example endpoint/route and HTTP status code).
2. Build two panels:
   - request rate
   - error rate
3. Build a latency panel using RED histogram metrics (p95 or average).
4. Add recording rules in Grafana for RED metrics.

## Start The Homework Lab
```bash
cd meeting-02/homework
docker compose up -d --build
docker compose ps
```

Open:
- Grafana: `http://localhost:3000`
- Alloy UI/metrics: `http://localhost:12347`
- Tempo API: `http://localhost:3200`
- Mimir API: `http://localhost:9009`

## Files Students Should Edit
- [alloy/config.alloy](meeting-02/homework/alloy/config.alloy)

After editing Alloy config:
```bash
cd meeting-02/homework
docker compose restart alloy
```

## Suggested Validation Steps
1. Verify traces exist in Tempo:
```bash
curl 'http://localhost:3200/api/search?limit=5'
```
Or using grafana and tempo datasource.

2. Verify RED call metric exists in Mimir:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=traces_spanmetrics_calls_total'
```
Or using grafana and mimir datasource.

3. Verify RED latency metric exists in Mimir:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=traces_spanmetrics_latency_count'
```
Or using grafana and mimir datasource.

4. Verify error signals exist:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=sum(rate(traces_spanmetrics_calls_total{status_code="STATUS_CODE_ERROR"}[1m]))'
```
Or using grafana and mimir datasource.

## RED Metric Panel Hints (Mimir PromQL)
Request rate:
```promql
sum(rate(traces_spanmetrics_calls_total[1m]))
```

Error rate (%):
```promql
100 *
sum(rate(traces_spanmetrics_calls_total{http_status_code=~"4..|5.."}[1m]))
/
sum(rate(traces_spanmetrics_calls_total[1m]))
```

Average latency (ms):
```promql
sum(rate(traces_spanmetrics_latency_sum[1m]))
/
sum(rate(traces_spanmetrics_latency_count[1m]))
```

## Expected Deliverables
- Updated Alloy config
- Screenshot showing traces in Tempo
- Screenshot showing RED metrics in Mimir/Prometheus query
- Screenshot of at least one RED dashboard panel in Grafana
