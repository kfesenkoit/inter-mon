# Meeting 03 Homework: Define And Visualize An SLI/SLO

## Scenario
You are given a small service with intentional healthy, slow, and failing requests.

The stack includes:
- `sre-demo`: lightweight service exposing Prometheus metrics (we aleradey have required metrics - no need to generate the new one)
- `loadgen`: traffic generator that creates normal, slow, and failing requests
- `alloy`: scrapes service metrics and remote-writes them to Mimir
- `mimir`: Prometheus-compatible metrics backend
- `grafana`: dashboard UI

Your task is to define one SLI, choose an SLO target, and visualize it in Grafana.

## Start The Homework Lab
```bash
cd meeting-03/homework
docker compose up -d --build
docker compose ps
```

Open:
- Grafana: `http://localhost:3000`
- Demo service: `http://localhost:8080`
- Demo service metrics: `http://localhost:8080/metrics`
- Alloy UI/metrics: `http://localhost:12347`
- Mimir API: `http://localhost:9009`

## Minimum Required Tasks
1. Pick one SLI:
   - availability
   - latency under threshold
2. Define one SLO target for that SLI.
3. Write the PromQL query that measures the SLI.
4. Build one Grafana visualization showing the SLI.
5. Add a short explanation of whether the service is meeting the SLO.

## Alternative tasks - if feels to easy
1. Use homework stack from meeting-02.
2. Generate metrics using tempo. 
3. Pick one SLI (availability, latency)
4. Define SLO target based on selected SLI. 
5. Promql query to measure SLI
6. BUild dashboard to visualize SLI. 



## Suggested Validation Steps
Check that metrics are arriving in Mimir:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=sre_demo_requests_total'
```

Check that the availability SLI query returns data:
```bash
curl 'http://localhost:9009/prometheus/api/v1/query?query=100%20*%20sum(rate(sre_demo_requests_total%7Bstatus!~%225..%22%7D%5B5m%5D))%20%2F%20sum(rate(sre_demo_requests_total%5B5m%5D))'
````

## Expected Deliverables
- SLI name and PromQL query
- SLO target and time window
- Grafana screenshot showing the SLI
- Short error-budget explanation
- Short statement: is the service meeting the SLO right now?
