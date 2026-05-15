# Sales Data Quality Lab Report

## Overview

This project implements a small Apache Airflow data-quality pipeline for sales order data. The pipeline reads an input CSV file, validates the data against business rules, writes a JSON validation summary, and fails the task when invalid data is detected.

## Implemented Files

- `starter_project/dags/sales_data_quality_pipeline.py`
- `starter_project/src/config.py`
- `starter_project/src/validation.py`
- `starter_project/data/orders_passed.csv`
- `starter_project/data/orders_failed.csv`
- `docker-compose.airflow.yml`

## Pipeline Flow

1. Airflow runs the DAG `sales_data_quality_pipeline`.
2. The task `validate_orders` calls `validate_orders_task()`.
3. `validate_orders_task()` calls `run_lab_check()`.
4. `run_lab_check()` reads the CSV file, validates all rows, writes `validation_summary.json`, and sends a Discord notification if a webhook is configured.
5. If validation fails, the summary file is still preserved and the task raises an error.

## Validation Rules

The pipeline validates three data-quality rules:

- `customer_id` must not be empty.
- `amount` must be numeric and greater than `0`.
- `status` must be one of `completed`, `pending`, or `cancelled`.

## Output Summary

The generated JSON file is written to:

```text
starter_project/output/validation_summary.json
```

The summary contains:

```json
{
  "row_count": 0,
  "missing_customer_ids": 0,
  "invalid_amounts": 0,
  "invalid_statuses": 0,
  "validation_status": "passed_or_failed"
}
```

## Local Test Results

Passing dataset command:

```bash
python starter_project/scripts/run_local_check.py starter_project/data/orders_passed.csv --skip-discord
```

Result:

```text
row_count = 10
missing_customer_ids = 0
invalid_amounts = 0
invalid_statuses = 0
validation_status = passed
```

Failing dataset command:

```bash
python starter_project/scripts/run_local_check.py starter_project/data/orders_failed.csv --allow-failure --skip-discord
```

Result:

```text
row_count = 10
missing_customer_ids = 2
invalid_amounts = 2
invalid_statuses = 2
validation_status = failed
```

## Airflow Verification

The DAG was verified with Docker-based Airflow using:

```bash
docker compose -f docker-compose.airflow.yml run --rm -e DISCORD_WEBHOOK_URL= -e AIRFLOW_INPUT_FILE=/opt/airflow/data/orders_passed.csv airflow airflow dags test sales_data_quality_pipeline 2026-05-15
```

The passing dataset completed successfully.

The failing dataset was also tested:

```bash
docker compose -f docker-compose.airflow.yml run --rm -e DISCORD_WEBHOOK_URL= -e AIRFLOW_INPUT_FILE=/opt/airflow/data/orders_failed.csv airflow airflow dags test sales_data_quality_pipeline 2026-05-16
```

The task failed as expected, and the validation summary was still written before failure.

## Discord Note

The code supports Discord notifications through `DISCORD_WEBHOOK_URL`. For this submission, the webhook is intentionally left empty to avoid using a real Discord secret. If a real webhook is provided in `.env`, the pipeline can send success or failure notifications.

## Rubric Coverage

| Rubric Item | Status |
| --- | --- |
| DAG structure and execution | Completed |
| CSV ingestion and dataset handling | Completed |
| Validation logic | Completed |
| Output JSON generation | Completed |
| Failure handling | Completed |
| Discord alert | Implemented in code, not configured with a real webhook |

