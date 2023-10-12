import pandas as pd
import plotly.graph_objects as go


def antall_med_glidende_gjennomsnitt(
    tittel, timestamp_felt, tabell, client, predikat=""
):
    # SQL query to count number of rows per day and calculate moving averages
    QUERY = f"""
    SELECT 
    date, 
    count,
    AVG(count) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_7_day_avg,
    AVG(count) OVER (
        ORDER BY date
        ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
    ) AS moving_28_day_avg
    FROM (
        SELECT date_range.date AS date, IFNULL(original_table.count, 0) AS count
            FROM (
                SELECT *
                FROM UNNEST(GENERATE_DATE_ARRAY('2023-03-01', CURRENT_DATE())) AS date
            ) AS date_range
        LEFT JOIN (
        SELECT
            DATE({timestamp_felt}) AS date,
            COUNT(*) AS count
        FROM
            `{tabell}`
        {predikat}
        GROUP BY
            DATE({timestamp_felt})
            ) AS original_table
        ON date_range.date = original_table.date
    )
    WHERE date > '2023-03-01'
    ORDER BY 
    date
    """

    query_job = client.query(QUERY)

    df: pd.DataFrame = query_job.to_dataframe()

    fig = go.Figure()

    # Add bar chart for daily counts
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["count"],
            name="Antall per dag",
            marker_color="#3380A5",
        )
    )

    # Add lines for moving averages
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["moving_7_day_avg"],
            name="Snitt over 7 dager",
            line=dict(color="#FF9100"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["moving_28_day_avg"],
            name="Snitt over 28 dager",
            line=dict(color="#C30000"),
        )
    )

    # Set x and y axis labels
    fig.update_layout(
        title=dict(
            text="7- og 28 dagers glidende gjennomsnitt",
            x=0,
            y=0.95,
            font=dict(family="Source Sans 3", size=20, color="#23262A"),
        ),
        plot_bgcolor="#FFFFFF",
        yaxis=dict(
            gridcolor="#CCCCCC",
        ),
    )

    return fig
