---
name: cron-date-context-enforcement
description: Enforce accurate date/weekday context in cron-generated reports to prevent LLM hallucination.
---

# Cron Date Context Enforcement

## Problem
LLMs frequently miscalculate weekdays or holiday offsets when generating daily reports (e.g., labeling a Tuesday as Monday). This leads to incorrect trading schedules and confusing user-facing content.

## Solution
Use a deterministic Python helper script (`~/.hermes/helpers/date_context.py`) to generate the exact date, weekday, and next trading day before the LLM starts writing.

## Implementation Steps

1.  **Create Helper Script**:
    ```python
    # ~/.hermes/helpers/date_context.py
    import datetime, json
    
    def get_date_context():
        now = datetime.datetime.now()
        today = now.date()
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        # Logic for specific holidays (e.g., Labor Day 2026: May 1-5)
        labor_day_start = datetime.date(2026, 5, 1)
        labor_day_end = datetime.date(2026, 5, 5)
        is_holiday = labor_day_start <= today <= labor_day_end
        
        # Calculate next trading day (skip weekends)
        next_day = today + datetime.timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += datetime.timedelta(days=1)
            
        return {
            "today_iso": today.isoformat(),
            "today_weekday": weekday_names[today.weekday()],
            "next_trading_day": next_day.isoformat(),
            "report_title": f"## {today.isoformat()} ({weekday_names[today.weekday()]})"
        }

    if __name__ == '__main__':
        print(json.dumps(get_date_context(), ensure_ascii=False))
    ```

2.  **Update Program/Instruction**:
    In your cron program file (e.g., `stock-daily-research-program.md`), add a mandatory step:
    > "**Date Confirmation**: Before writing any dates, run `python3 ~/.hermes/helpers/date_context.py`. Use the output for all headers and references. Do NOT calculate weekdays manually."

3.  **Cron Job Integration**:
    Ensure the cron job's prompt or initial script execution includes this helper call.

## Why This Matters
-   **Accuracy**: Eliminates "Monday/Tuesday" confusion during holidays.
-   **Consistency**: Ensures "Next Trading Day" logic handles weekend skips correctly.
-   **Trust**: Users rely on precise timing for trading decisions.