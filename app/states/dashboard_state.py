import reflex as rx
from typing import TypedDict, Any
import datetime
import httpx
import logging


class WeekData(TypedDict):
    week_label: str
    DAU_avg: float
    WAU: int
    MAU: int
    Stickiness: float
    Avg_session_count_per_DAU_day: float
    Avg_Usage_Duration_p50_in_mins_day: float
    No_of_news_items_viewed_day_p50: float
    No_of_news_items_viewed_day_p95: float
    time_to_value_in_s_p50: float | None


class MetricsResponse(TypedDict):
    start_date: str
    end_date: str
    weeks: list[WeekData]


class DashboardState(rx.State):
    start_date: str = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    end_date: str = datetime.date.today().isoformat()
    metrics: list[dict[str, str | float | int | None]] = []
    week_labels: list[str] = []
    is_loading: bool = False
    error_message: str = ""
    METRIC_DISPLAY_NAMES: dict[str, str] = {
        "DAU(avg)": "DAU(avg)",
        "WAU": "WAU",
        "MAU": "MAU",
        "Stickiness(%)": "Stickiness percentage",
        "Avg. session count per DAU/day": "Avg. session count per DAU/day",
        "Avg. Usage Duration (p50) in mins/day": "Avg. Usage Duration (p50) in mins/day",
        "time_to_value_in_s_p50": "Time to Value in s (p50)",
        "No. of news items viewed/day (p50)": "No. of news items viewed/day (p50)",
        "No. of news items viewed/day (p95)": "No. of news items viewed/day (p95)",
    }

    @rx.var
    def chart_data(self) -> list[dict[str, str | float]]:
        data_map: dict[str, dict[str, str | float]] = {
            wl: {"week_label": wl} for wl in self.week_labels
        }
        metric_keys_to_process = {
            "DAU(avg)": "DAU",
            "WAU": "WAU",
            "MAU": "MAU",
            "Stickiness percentage": "Stickiness",
            "Avg. session count per DAU/day": "SessionCount",
            "Avg. Usage Duration (p50) in mins/day": "UsageDuration",
            "No. of news items viewed/day (p50)": "NewsItemsP50",
            "No. of news items viewed/day (p95)": "NewsItemsP95",
        }
        for display_name, data_key in metric_keys_to_process.items():
            metric_data = next(
                (m for m in self.metrics if m["metric"] == display_name), None
            )
            if metric_data:
                for wl in self.week_labels:
                    try:
                        value = metric_data.get(wl, 0)
                        if isinstance(value, str):
                            value = value.replace("%", "")
                        data_map[wl][data_key] = float(value)
                    except (ValueError, TypeError) as e:
                        logging.exception(f"Error converting {data_key} value: {e}")
                        data_map[wl][data_key] = 0
        return list(data_map.values())

    @rx.var
    def ordered_metric_keys(self) -> list[str]:
        return list(self.METRIC_DISPLAY_NAMES.keys())

    @rx.event(background=True)
    async def fetch_metrics(self):
        async with self:
            if not self.start_date or not self.end_date:
                self.error_message = "Please select both a start and end date."
                return
            if self.start_date > self.end_date:
                self.error_message = "Start date cannot be after end date."
                return
            self.is_loading = True
            self.error_message = ""
            self.metrics = []
            self.week_labels = []
            yield
        try:
            api_url = (
                f"https://api.chunavo.com/api/v1/analytics/user_engagement_metrics"
            )
            params = {"start_date": self.start_date, "end_date": self.end_date}
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
            async with self:
                self.week_labels = [
                    week["week_label"] for week in data.get("weeks", [])
                ]
                transformed_metrics = []
                for api_key, display_name in self.METRIC_DISPLAY_NAMES.items():
                    row = {"metric": display_name}
                    for week in data.get("weeks", []):
                        value = week.get(api_key)
                        if value is not None and isinstance(value, (int, float)):
                            if display_name == "Stickiness percentage":
                                row[week["week_label"]] = f"{value:.2f}%"
                            else:
                                row[week["week_label"]] = f"{value:.2f}"
                        elif (
                            display_name == "Time to Value in s (p50)" and value is None
                        ):
                            row[week["week_label"]] = ""
                        else:
                            row[week["week_label"]] = (
                                str(value) if value is not None else "-"
                            )
                    transformed_metrics.append(row)
                self.metrics = transformed_metrics
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP Error fetching metrics: {e}")
            async with self:
                self.error_message = f"Failed to fetch data: {e.response.status_code}"
        except Exception as e:
            logging.exception(f"Error fetching metrics: {e}")
            async with self:
                self.error_message = "An unexpected error occurred."
        finally:
            async with self:
                self.is_loading = False