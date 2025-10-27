import reflex as rx
from app.states.dashboard_state import DashboardState


def _metric_row(metric: dict[str, str]) -> rx.Component:
    metric_name = metric["metric"]
    return rx.el.tr(
        rx.el.td(
            metric_name, class_name="px-4 py-3 font-semibold text-gray-800 text-left"
        ),
        rx.foreach(
            DashboardState.week_labels,
            lambda week_label: rx.el.td(
                metric[week_label], class_name="px-4 py-3 text-gray-700 text-center"
            ),
        ),
        class_name=rx.cond(
            metric_name == "Time to Value in s (p50)",
            "bg-red-600 text-white font-bold",
            "border-b border-gray-200 hover:bg-gray-50 transition-colors",
        ),
    )


def _html_legend(legend_items: list[dict[str, str]]) -> rx.Component:
    def legend_item(item: dict) -> rx.Component:
        return rx.el.div(
            rx.el.div(class_name=f"w-3 h-3 rounded-full {item['color']}"),
            rx.el.span(item["name"], class_name="text-sm text-gray-600"),
            class_name="flex items-center gap-2",
        )

    return rx.el.div(
        rx.foreach(legend_items, legend_item),
        class_name="flex justify-center items-center gap-4 mt-4",
    )


def user_activity_chart() -> rx.Component:
    legend_items = [
        {"name": "DAU (Avg)", "color": "bg-blue-500"},
        {"name": "WAU", "color": "bg-green-500"},
        {"name": "MAU", "color": "bg-purple-500"},
    ]
    return rx.el.div(
        rx.el.h2(
            "User Activity Trends", class_name="text-2xl font-bold text-gray-800 mb-4"
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(
                content_style={"backgroundColor": "white", "border": "1px solid #ccc"}
            ),
            rx.recharts.x_axis(data_key="week_label", stroke="#888888"),
            rx.recharts.y_axis(stroke="#888888"),
            rx.recharts.line(
                type="monotone",
                data_key="DAU",
                stroke="#3b82f6",
                name="DAU (Avg)",
                dot=False,
            ),
            rx.recharts.line(
                type="monotone", data_key="WAU", stroke="#16a34a", name="WAU", dot=False
            ),
            rx.recharts.line(
                type="monotone", data_key="MAU", stroke="#9333ea", name="MAU", dot=False
            ),
            data=DashboardState.chart_data,
            height=300,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 5},
        ),
        _html_legend(legend_items),
        class_name="mt-8 p-6 bg-white rounded-xl shadow-md border border-gray-200",
    )


def session_metrics_chart() -> rx.Component:
    legend_items = [
        {"name": "Avg. Session Count", "color": "bg-orange-500"},
        {"name": "Avg. Usage Duration (mins)", "color": "bg-teal-500"},
    ]
    return rx.el.div(
        rx.el.h2("Session Metrics", class_name="text-2xl font-bold text-gray-800 mb-4"),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(
                content_style={"backgroundColor": "white", "border": "1px solid #ccc"}
            ),
            rx.recharts.x_axis(data_key="week_label", stroke="#888888"),
            rx.recharts.y_axis(stroke="#888888"),
            rx.recharts.line(
                type="monotone",
                data_key="SessionCount",
                stroke="#f97316",
                name="Avg. Session Count",
                dot=False,
            ),
            rx.recharts.line(
                type="monotone",
                data_key="UsageDuration",
                stroke="#14b8a6",
                name="Avg. Usage Duration (mins)",
                dot=False,
            ),
            data=DashboardState.chart_data,
            height=300,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 5},
        ),
        _html_legend(legend_items),
        class_name="mt-8 p-6 bg-white rounded-xl shadow-md border border-gray-200",
    )


def news_engagement_chart() -> rx.Component:
    legend_items = [
        {"name": "News Items Viewed (p50)", "color": "bg-cyan-500"},
        {"name": "News Items Viewed (p95)", "color": "bg-red-500"},
    ]
    return rx.el.div(
        rx.el.h2(
            "News Items Engagement", class_name="text-2xl font-bold text-gray-800 mb-4"
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(
                content_style={"backgroundColor": "white", "border": "1px solid #ccc"}
            ),
            rx.recharts.x_axis(data_key="week_label", stroke="#888888"),
            rx.recharts.y_axis(stroke="#888888"),
            rx.recharts.line(
                type="monotone",
                data_key="NewsItemsP50",
                stroke="#06b6d4",
                name="News Items Viewed (p50)",
                dot=False,
            ),
            rx.recharts.line(
                type="monotone",
                data_key="NewsItemsP95",
                stroke="#ef4444",
                name="News Items Viewed (p95)",
                dot=False,
            ),
            data=DashboardState.chart_data,
            height=300,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 5},
        ),
        _html_legend(legend_items),
        class_name="mt-8 p-6 bg-white rounded-xl shadow-md border border-gray-200",
    )


def stickiness_chart() -> rx.Component:
    legend_items = [{"name": "Stickiness (%)", "color": "bg-indigo-500"}]
    return rx.el.div(
        rx.el.h2(
            "Stickiness Trend", class_name="text-2xl font-bold text-gray-800 mb-4"
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(
                content_style={"backgroundColor": "white", "border": "1px solid #ccc"}
            ),
            rx.recharts.x_axis(data_key="week_label", stroke="#888888"),
            rx.recharts.y_axis(stroke="#888888", domain=[0, 100]),
            rx.recharts.line(
                type="monotone",
                data_key="Stickiness",
                stroke="#6366f1",
                name="Stickiness (%)",
                dot=False,
            ),
            data=DashboardState.chart_data,
            height=300,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 5},
        ),
        _html_legend(legend_items),
        class_name="mt-8 p-6 bg-white rounded-xl shadow-md border border-gray-200",
    )


def analytics_charts() -> rx.Component:
    return rx.el.div(
        user_activity_chart(),
        session_metrics_chart(),
        news_engagement_chart(),
        stickiness_chart(),
        class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
    )


def dashboard_component() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "User Engagement Analytics",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Start Date", class_name="text-sm font-medium text-gray-700"
                ),
                rx.el.input(
                    type="date",
                    default_value=DashboardState.start_date,
                    on_change=DashboardState.set_start_date,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="w-full md:w-auto",
            ),
            rx.el.div(
                rx.el.label("End Date", class_name="text-sm font-medium text-gray-700"),
                rx.el.input(
                    type="date",
                    default_value=DashboardState.end_date,
                    on_change=DashboardState.set_end_date,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="w-full md:w-auto",
            ),
            rx.el.button(
                rx.icon("search", class_name="mr-2 h-4 w-4"),
                "Get Metrics",
                on_click=DashboardState.fetch_metrics,
                is_loading=DashboardState.is_loading,
                class_name="flex items-center justify-center w-full md:w-auto mt-4 md:mt-0 md:self-end px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 p-6 bg-gray-50 rounded-lg border border-gray-200",
        ),
        rx.cond(
            DashboardState.error_message != "",
            rx.el.div(
                rx.icon("flag_triangle_right", class_name="h-5 w-5 text-red-500 mr-3"),
                rx.el.span(DashboardState.error_message),
                class_name="flex items-center p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg",
            ),
            None,
        ),
        rx.el.div(
            rx.cond(
                DashboardState.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-indigo-500 h-8 w-8"),
                    class_name="flex justify-center items-center h-64",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Metric",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-orange-100",
                                ),
                                rx.foreach(
                                    DashboardState.week_labels,
                                    lambda week: rx.el.th(
                                        week,
                                        class_name="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider bg-orange-100",
                                    ),
                                ),
                                class_name="border-b-2 border-gray-300",
                            )
                        ),
                        rx.el.tbody(rx.foreach(DashboardState.metrics, _metric_row)),
                        class_name="min-w-full bg-white divide-y divide-gray-200",
                    ),
                    class_name="overflow-x-auto",
                ),
            ),
            class_name="shadow-lg rounded-lg border border-gray-200 overflow-hidden",
        ),
        rx.cond(DashboardState.chart_data.length() > 0, analytics_charts(), None),
        class_name="p-8 bg-white rounded-xl shadow-md space-y-8",
    )