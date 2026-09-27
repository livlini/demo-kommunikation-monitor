import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import html


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Communication Monitor — Demo",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# ORIGINAL DEMO DATA
#
# These values are fictional prototype data.
# They are NOT collected live.
# ============================================================

DATA = [
    {
        "trend": "AI governance & AI Act",
        "category": "AI & Technology",
        "signals": 18,
        "previous_signals": 13,
        "sources": 5,
        "relevance": 9.0,
    },
    {
        "trend": "AI in the finance function",
        "category": "Finance & CFO",
        "signals": 16,
        "previous_signals": 12,
        "sources": 4,
        "relevance": 8.8,
    },
    {
        "trend": "Audit standards & assurance",
        "category": "Audit",
        "signals": 12,
        "previous_signals": 11,
        "sources": 3,
        "relevance": 7.8,
    },
    {
        "trend": "Digital tax & e-invoicing",
        "category": "Tax",
        "signals": 10,
        "previous_signals": 9,
        "sources": 4,
        "relevance": 8.2,
    },
]


# ============================================================
# ORIGINAL TREND STRENGTH MODEL
# ============================================================

def calculate_trend_score(
    signals,
    previous_signals,
    sources,
    relevance,
):

    # Volume — max 30
    volume_points = min(
        signals,
        30,
    )

    # Growth — max 30
    if previous_signals > 0:

        growth_pct = (
            (
                signals
                - previous_signals
            )
            / previous_signals
        ) * 100

    else:

        growth_pct = (
            100
            if signals > 0
            else 0
        )

    growth_points = min(
        max(
            growth_pct,
            0,
        )
        / 100
        * 30,
        30,
    )

    # Source breadth — max 20
    source_points = min(
        sources * 2,
        20,
    )

    # Relevance — max 20
    relevance_points = (
        min(
            max(
                relevance,
                0,
            ),
            10,
        )
        * 2
    )

    total = (
        volume_points
        + growth_points
        + source_points
        + relevance_points
    )

    return {
        "trend_strength":
            round(total, 1),

        "volume_points":
            round(volume_points, 1),

        "growth_points":
            round(growth_points, 1),

        "source_points":
            round(source_points, 1),

        "relevance_points":
            round(relevance_points, 1),

        "wow_growth_pct":
            round(growth_pct, 1),
    }


# ============================================================
# PREPARE DEMO DATA
# ============================================================

rows = []

for item in DATA:

    score = calculate_trend_score(
        item["signals"],
        item["previous_signals"],
        item["sources"],
        item["relevance"],
    )

    rows.append({
        **item,
        **score,
    })


df = pd.DataFrame(rows)

df = df.sort_values(
    "trend_strength",
    ascending=False,
)


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fa;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 750;
        color: #163d73;
        margin-bottom: 0;
    }

    .subtitle {
        color: #667085;
        font-size: 17px;
        margin-top: 4px;
        margin-bottom: 14px;
    }

    .demo-label {
        display: inline-block;
        background: #e7eef8;
        color: #163d73;
        border-radius: 100px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 650;
        margin-bottom: 20px;
    }

    .section-title {
        color: #163d73;
        font-size: 25px;
        font-weight: 700;
        margin-top: 32px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #667085;
        font-size: 14px;
        margin-bottom: 20px;
    }

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #e3eaf3;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Communication Monitor</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        A weekly signal monitor tracking communication-relevant
        developments across Finance & CFO, Audit, Tax and AI & Technology.
    </div>

    <div class="demo-label">
        PROTOTYPE · DEMO DATA
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW CHART
# ============================================================

st.markdown(
    '<div class="section-title">Trend Strength Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Trendscore is the combined trend strength
        based on four different factors.
    </div>
    """,
    unsafe_allow_html=True,
)


chart = (
    alt.Chart(df)
    .mark_bar(
        cornerRadiusTopRight=6,
        cornerRadiusBottomRight=6,
        color="#7ea6d8",
    )
    .encode(

        y=alt.Y(
            "trend:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelLimit=350,
                labelFontSize=13,
            ),
        ),

        x=alt.X(
            "trend_strength:Q",
            title="Trend Strength",
            scale=alt.Scale(
                domain=[0, 100]
            ),
        ),

        tooltip=[
            alt.Tooltip(
                "trend:N",
                title="Trend",
            ),

            alt.Tooltip(
                "trend_strength:Q",
                title="Trend Strength",
                format=".1f",
            ),

            alt.Tooltip(
                "signals:Q",
                title="Signals",
            ),

            alt.Tooltip(
                "wow_growth_pct:Q",
                title="WoW",
                format=".1f",
            ),

            alt.Tooltip(
                "sources:Q",
                title="Sources",
            ),

            alt.Tooltip(
                "relevance:Q",
                title="Relevance",
                format=".1f",
            ),
        ],
    )
    .properties(
        height=300,
    )
)


st.altair_chart(
    chart,
    use_container_width=True,
)


# ============================================================
# SCORE EXPLANATION
# ============================================================

with st.expander(
    "How is Trend Strength calculated?"
):

    st.markdown(
        """
**Trend Strength is an internal indicator from 0–100.**

- **Volume — max 30 points:** 1 point per relevant signal.
- **Week-over-week growth — max 30 points:** +100% or more gives 30 points.
- **Source breadth — max 20 points:** 2 points per unique source.
- **Relevance — max 20 points:** relevance from 0–10 multiplied by 2.

The Trend Strength model is an internal prototype indicator and is
**not an external industry benchmark**.
        """
    )


# ============================================================
# CURRENT TRENDS
# ============================================================

st.markdown(
    '<div class="section-title">Current Trends</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Hover over a card to see the calculation
        behind its Trend Strength.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def format_wow(value):

    if value > 0:
        return f"+{value:.1f}%"

    if value < 0:
        return f"{value:.1f}%"

    return "0.0%"


# ============================================================
# FLIP CARDS
# ============================================================

def render_flip_card(row):

    category = html.escape(
        str(row["category"])
    )

    trend = html.escape(
        str(row["trend"])
    )

    wow = format_wow(
        row["wow_growth_pct"]
    )

    card_html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            * {{
                box-sizing: border-box;
            }}

            html,
            body {{
                margin: 0;
                padding: 0;
                background: transparent;

                font-family:
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    Roboto,
                    Helvetica,
                    Arial,
                    sans-serif;
            }}


            .flip-card {{
                background: transparent;
                width: 100%;
                height: 300px;
                perspective: 1200px;
                cursor: pointer;
            }}


            .flip-card-inner {{
                position: relative;
                width: 100%;
                height: 100%;

                transition:
                    transform 0.65s
                    cubic-bezier(
                        0.4,
                        0.2,
                        0.2,
                        1
                    );

                transform-style:
                    preserve-3d;
            }}


            .flip-card:hover
            .flip-card-inner {{

                transform:
                    rotateY(180deg);
            }}


            .front,
            .back {{

                position: absolute;

                width: 100%;
                height: 100%;

                padding: 28px;

                border-radius: 18px;

                backface-visibility: hidden;
                -webkit-backface-visibility: hidden;

                box-shadow:
                    0 6px 18px
                    rgba(
                        22,
                        61,
                        115,
                        0.08
                    );
            }}


            .front {{

                background: white;

                border:
                    1px solid
                    #e3eaf3;
            }}


            .back {{

                background:
                    #163d73;

                color: white;

                transform:
                    rotateY(180deg);
            }}


            .category {{

                color:
                    #6282ad;

                font-size:
                    12px;

                font-weight:
                    700;

                text-transform:
                    uppercase;

                letter-spacing:
                    0.8px;

                margin-bottom:
                    12px;
            }}


            .trend {{

                color:
                    #163d73;

                font-size:
                    23px;

                line-height:
                    1.25;

                font-weight:
                    700;

                min-height:
                    60px;
            }}


            .label {{

                color:
                    #7a8797;

                font-size:
                    12px;

                font-weight:
                    600;

                letter-spacing:
                    0.5px;

                margin-top:
                    22px;
            }}


            .strength {{

                color:
                    #163d73;

                font-size:
                    52px;

                line-height:
                    1;

                font-weight:
                    750;

                margin-top:
                    5px;
            }}


            .out-of {{

                color:
                    #98a2b3;

                font-size:
                    16px;
            }}


            .metrics {{

                color:
                    #667085;

                font-size:
                    14px;

                margin-top:
                    17px;
            }}


            .back-title {{

                font-size:
                    21px;

                font-weight:
                    700;

                margin-bottom:
                    18px;
            }}


            .score-row {{

                display:
                    flex;

                justify-content:
                    space-between;

                padding:
                    8px 0;

                font-size:
                    14px;

                border-bottom:
                    1px solid
                    rgba(
                        255,
                        255,
                        255,
                        0.12
                    );
            }}


            .score-value {{

                font-weight:
                    700;
            }}


            .detail {{

                margin-top:
                    14px;

                font-size:
                    12px;

                line-height:
                    1.55;

                color:
                    rgba(
                        255,
                        255,
                        255,
                        0.76
                    );
            }}


            .total {{

                display:
                    flex;

                justify-content:
                    space-between;

                margin-top:
                    14px;

                padding-top:
                    12px;

                border-top:
                    1px solid
                    rgba(
                        255,
                        255,
                        255,
                        0.35
                    );

                font-size:
                    15px;

                font-weight:
                    700;
            }}

        </style>

    </head>


    <body>

        <div class="flip-card">

            <div class="flip-card-inner">


                <!-- FRONT -->

                <div class="front">

                    <div class="category">
                        {category}
                    </div>

                    <div class="trend">
                        {trend}
                    </div>

                    <div class="label">
                        TREND STRENGTH
                    </div>

                    <div class="strength">

                        {row["trend_strength"]:.1f}

                        <span class="out-of">
                            / 100
                        </span>

                    </div>

                    <div class="metrics">

                        WoW:
                        {wow}

                        &nbsp; · &nbsp;

                        {int(row["signals"])}
                        signals

                        &nbsp; · &nbsp;

                        {int(row["sources"])}
                        sources

                    </div>

                </div>


                <!-- BACK -->

                <div class="back">

                    <div class="back-title">
                        Score calculation
                    </div>


                    <div class="score-row">

                        <span>
                            Volume
                        </span>

                        <span class="score-value">
                            {row["volume_points"]:.1f} / 30
                        </span>

                    </div>


                    <div class="score-row">

                        <span>
                            Growth
                        </span>

                        <span class="score-value">
                            {row["growth_points"]:.1f} / 30
                        </span>

                    </div>


                    <div class="score-row">

                        <span>
                            Source breadth
                        </span>

                        <span class="score-value">
                            {row["source_points"]:.1f} / 20
                        </span>

                    </div>


                    <div class="score-row">

                        <span>
                            Relevance
                        </span>

                        <span class="score-value">
                            {row["relevance_points"]:.1f} / 20
                        </span>

                    </div>


                    <div class="detail">

                        {int(row["signals"])}
                        signals

                        ·

                        {int(row["sources"])}
                        sources

                        <br>

                        Relevance:
                        {row["relevance"]:.1f} / 10

                        <br>

                        Week-over-week:
                        {wow}

                    </div>


                    <div class="total">

                        <span>
                            Trend Strength
                        </span>

                        <span>
                            {row["trend_strength"]:.1f} / 100
                        </span>

                    </div>


                </div>


            </div>

        </div>

    </body>

    </html>
    """


    components.html(
        card_html,
        height=320,
        scrolling=False,
    )


# ============================================================
# 2 x 2 GRID
# ============================================================

for i in range(
    0,
    len(df),
    2,
):

    col1, col2 = st.columns(
        2,
        gap="large",
    )


    with col1:

        render_flip_card(
            df.iloc[i]
        )


    if i + 1 < len(df):

        with col2:

            render_flip_card(
                df.iloc[i + 1]
            )


# ============================================================
# DEMO SOURCES
# ============================================================

st.markdown(
    '<div class="section-title">Example Sources</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-description">
        Example source types used when designing the prototype.
    </div>
    """,
    unsafe_allow_html=True,
)


source_col1, source_col2 = st.columns(2)


with source_col1:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Regulatory & public authorities**"
        )

        st.caption(
            "EU institutions and Danish authorities"
        )


    with st.container(
        border=True
    ):

        st.markdown(
            "**Professional organisations**"
        )

        st.caption(
            "Accounting, audit and finance organisations"
        )


with source_col2:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Industry insights**"
        )

        st.caption(
            "Reports, analysis and professional publications"
        )


    with st.container(
        border=True
    ):

        st.markdown(
            "**Market signals**"
        )

        st.caption(
            "Selected communication-relevant developments"
        )


# ============================================================
# ABOUT
# ============================================================

with st.expander(
    "About this prototype"
):

    st.markdown(
        """
This is the original **Communication Monitor prototype**.

The values shown in this version are **fictional demonstration data** created to illustrate the dashboard concept and Trend Strength methodology.

Unlike the live Communication Monitor, this demo does **not** use the automated Collector → Analyzer → Trend Engine pipeline.
        """
    )
