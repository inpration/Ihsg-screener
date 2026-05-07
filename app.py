# =============================================================================
# IHSG SWING TRADING SCREENER — app.py
# Jalankan dengan: streamlit run app.py
# Dependensi: pip install streamlit yfinance pandas numpy
# =============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IHSG Swing Trading Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark Trading Terminal Aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

    /* Root & Background */
    .stApp {
        background: #0a0e1a;
        color: #c8d8e8;
        font-family: 'Exo 2', sans-serif;
    }
    .stApp > header { background: transparent !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d1220;
        border-right: 1px solid #1e3a5f;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCheckbox span {
        color: #8ab4d4 !important;
        font-family: 'Exo 2', sans-serif;
        font-size: 0.85rem;
    }

    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #0d1b2e 0%, #0a2540 50%, #0d1b2e 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 28px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, #0088ff, transparent);
    }
    .hero-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2.1rem;
        font-weight: 700;
        color: #00d4ff;
        margin: 0;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    .hero-sub {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.95rem;
        color: #5a8aaa;
        margin-top: 6px;
        letter-spacing: 1px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        color: #00d4ff;
        margin-left: 12px;
        vertical-align: middle;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Metric Cards */
    .metric-grid { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
    .metric-card {
        flex: 1; min-width: 150px;
        background: #0d1b2e;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: #00d4ff44; }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0066cc, transparent);
    }
    .metric-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #4a7090;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .metric-card.green .metric-value { color: #00e676; }
    .metric-card.yellow .metric-value { color: #ffd600; }
    .metric-card.red .metric-value { color: #ff5252; }

    /* Section Title */
    .section-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        color: #00d4ff;
        text-transform: uppercase;
        letter-spacing: 3px;
        border-left: 3px solid #00d4ff;
        padding-left: 12px;
        margin: 28px 0 16px;
    }

    /* Dataframe override */
    .stDataFrame {
        border: 1px solid #1e3a5f !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    .stDataFrame table { font-family: 'Share Tech Mono', monospace !important; font-size: 0.82rem !important; }
    .stDataFrame thead tr th {
        background: #0d1b2e !important;
        color: #00d4ff !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border-bottom: 1px solid #1e3a5f !important;
    }
    .stDataFrame tbody tr td { border-bottom: 1px solid #0e1e30 !important; }
    .stDataFrame tbody tr:hover td { background: #0e2035 !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #003d6b, #0055a0);
        color: #00d4ff;
        border: 1px solid #0077cc;
        border-radius: 8px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        letter-spacing: 1px;
        padding: 10px 28px;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0055a0, #007acc);
        border-color: #00d4ff;
        box-shadow: 0 0 16px rgba(0, 212, 255, 0.25);
        color: #ffffff;
    }

    /* Progress / Spinner */
    .stProgress > div > div { background: linear-gradient(90deg, #0055a0, #00d4ff) !important; }

    /* Info / Warning / Success boxes */
    .stAlert { border-radius: 8px !important; border-left-width: 4px !important; font-family: 'Exo 2', sans-serif !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #0d1b2e !important;
        color: #00d4ff !important;
        font-family: 'Share Tech Mono', monospace !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: #0a1220 !important;
        border: 1px solid #1e3a5f !important;
        border-top: none !important;
    }

    /* Divider */
    hr { border-color: #1a2e45 !important; }

    /* Ticker pill */
    .ticker-pill {
        display: inline-block;
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.25);
        border-radius: 5px;
        padding: 2px 8px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #00d4ff;
        margin: 2px;
    }

    /* Log area */
    .log-box {
        background: #060c14;
        border: 1px solid #1a2e45;
        border-radius: 8px;
        padding: 14px 18px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.78rem;
        color: #3d7a9e;
        max-height: 200px;
        overflow-y: auto;
        line-height: 1.7;
    }
    .log-box .ok { color: #00e676; }
    .log-box .warn { color: #ffd600; }
    .log-box .err { color: #ff5252; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #060c14; }
    ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #0055a0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# KONSTANTA & DEFAULT WATCHLIST
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_WATCHLIST = ["BUMI.JK", "MBMA.JK", "BUVA.JK", "BBCA.JK", "BMRI.JK"]

BROKER_POOL = {
    "BK": "BRI Danareksa Sekuritas",
    "AK": "UBS Sekuritas",
    "CC": "Mandiri Sekuritas",
    "YU": "CIMB Sekuritas",
    "ZP": "Kim Eng Sekuritas",
    "RX": "Macquarie Sekuritas",
    "HD": "HD Capital",
    "LG": "Lautandhana Securindo",
}

# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: AMBIL DATA HISTORIS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900, show_spinner=False)
def fetch_ohlcv(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """Download data OHLCV dari yfinance, kembalikan DataFrame atau None jika gagal."""
    try:
        df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        if df.empty or len(df) < 30:
            return None
        # Flatten MultiIndex kolom (jika ada)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: HITUNG INDIKATOR TEKNIKAL
# ─────────────────────────────────────────────────────────────────────────────
def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Tambahkan kolom MA, MACD, Signal, RSI, Volume SMA ke DataFrame."""
    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    # Moving Averages
    df["MA5"]  = close.rolling(5).mean()
    df["MA10"] = close.rolling(10).mean()
    df["MA20"] = close.rolling(20).mean()

    # MACD (EMA12 - EMA26) & Signal (EMA9 of MACD)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["MACD"]   = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["Hist"]   = df["MACD"] - df["Signal"]

    # RSI (periode 14)
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    # Volume SMA 20
    df["Vol_SMA20"] = volume.rolling(20).mean()

    return df


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: CEK GOLDEN CROSS (MACD x Signal)
# ─────────────────────────────────────────────────────────────────────────────
def macd_golden_cross_days_ago(df: pd.DataFrame) -> int | None:
    """
    Kembalikan berapa hari lalu terjadinya Golden Cross MACD.
    Golden Cross = MACD bersilang naik di atas Signal (sebelumnya di bawah).
    Kembalikan None jika tidak ditemukan dalam 10 hari terakhir.
    """
    hist = df["Hist"].dropna().values
    if len(hist) < 2:
        return None
    for i in range(len(hist) - 1, max(len(hist) - 11, 0), -1):
        if hist[i] > 0 and hist[i - 1] <= 0:
            return len(hist) - 1 - i  # 0 = hari ini
    return None


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: SCREENING UTAMA
# ─────────────────────────────────────────────────────────────────────────────
def run_screening(df: pd.DataFrame, ticker: str) -> dict | None:
    """
    Terapkan semua filter swing trading.
    Kembalikan dict hasil jika lolos, None jika tidak.
    """
    last = df.iloc[-1]

    close      = float(last["Close"])
    ma5        = float(last["MA5"])
    ma10       = float(last["MA10"])
    ma20       = float(last["MA20"])
    macd_val   = float(last["MACD"])
    signal_val = float(last["Signal"])
    rsi_val    = float(last["RSI"])
    vol_last   = float(last["Volume"])
    vol_sma20  = float(last["Vol_SMA20"])

    # ── Filter 1: Trend (MA Stack)
    trend_ok = (close > ma5) and (ma5 > ma10) and (ma10 > ma20)
    if not trend_ok:
        return None

    # ── Filter 2: MACD di atas Signal
    macd_above = macd_val > signal_val
    if not macd_above:
        return None

    # ── Filter 3: Golden Cross maksimal 3 hari lalu
    gc_days = macd_golden_cross_days_ago(df)
    if gc_days is None or gc_days > 3:
        return None

    # ── Filter 4: RSI 40–65
    rsi_ok = 40.0 <= rsi_val <= 65.0
    if not rsi_ok:
        return None

    # ── Filter 5: Volume Breakout (> 1.5x Vol SMA20)
    vol_ratio = vol_last / vol_sma20 if vol_sma20 > 0 else 0
    vol_breakout = vol_ratio >= 1.5
    if not vol_breakout:
        return None

    return {
        "Ticker":          ticker,
        "Close Price":     close,
        "MA5":             ma5,
        "MA10":            ma10,
        "MA20":            ma20,
        "MACD":            macd_val,
        "Signal":          signal_val,
        "RSI":             round(rsi_val, 2),
        "MACD Status":     f"✅ GC {gc_days}d ago",
        "Volume Breakout": "✅ YES",
        "Vol Ratio":       round(vol_ratio, 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: MOCK DATA BANDARMOLOGI
# ─────────────────────────────────────────────────────────────────────────────
def get_broker_data(ticker: str, close_price: float) -> pd.DataFrame:
    """
    Hasilkan mock data Broker Summary untuk hari ini.
    Broker BK atau AK selalu menjadi Top Buyer (net beli terbesar).
    """
    # Seed berdasarkan ticker + tanggal agar konsisten dalam satu hari
    seed = hash(ticker + datetime.now().strftime("%Y%m%d")) % (2**32)
    rng  = random.Random(seed)

    top_buyer_code = rng.choice(["BK", "AK"])
    brokers_used   = [top_buyer_code] + rng.sample(
        [b for b in BROKER_POOL if b != top_buyer_code], 4
    )

    rows = []
    for i, code in enumerate(brokers_used):
        if code == top_buyer_code:
            # Top buyer: akumulasi besar, net positif
            net_lot   = rng.randint(5_000, 20_000)
            net_value = net_lot * 100 * close_price * rng.uniform(0.96, 1.02)
        elif i <= 2:
            # Broker lain dengan net positif kecil
            net_lot   = rng.randint(500, 3_000)
            net_value = net_lot * 100 * close_price * rng.uniform(0.95, 1.03)
        else:
            # Net negatif (seller)
            net_lot   = -rng.randint(1_000, 8_000)
            net_value = net_lot * 100 * close_price * rng.uniform(0.95, 1.03)

        rows.append({
            "Broker_Code":    code,
            "Broker_Name":    BROKER_POOL.get(code, code),
            "Net_Volume_Lot": int(net_lot),
            "Net_Value_IDR":  round(net_value, 0),
        })

    return pd.DataFrame(rows).sort_values("Net_Volume_Lot", ascending=False)


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI: KALKULASI RISIKO ENTRY (BANDAR AVERAGE PRICE)
# ─────────────────────────────────────────────────────────────────────────────
def compute_risk_level(broker_df: pd.DataFrame, close_price: float) -> dict:
    """
    Hitung harga rata-rata Top Buyer dan tentukan Risk Level.
    Rumus: Net_Value_IDR / (Net_Volume_Lot * 100)
    """
    top = broker_df[broker_df["Net_Volume_Lot"] > 0].iloc[0]

    top_buyer_code = top["Broker_Code"]
    net_vol  = top["Net_Volume_Lot"]
    net_val  = top["Net_Value_IDR"]

    # Harga rata-rata akuisisi bandar
    if net_vol > 0:
        bandar_avg_price = net_val / (net_vol * 100)
    else:
        bandar_avg_price = close_price

    # Selisih % antara Current Price vs Bandar Avg
    if bandar_avg_price > 0:
        diff_pct = ((close_price - bandar_avg_price) / bandar_avg_price) * 100
    else:
        diff_pct = 0.0

    # Risk Level
    if diff_pct <= 3.0:
        risk = "🟢 LOW RISK (Strong Buy)"
    elif diff_pct <= 7.0:
        risk = "🟡 MEDIUM RISK (Hold)"
    else:
        risk = "🔴 HIGH RISK (Rawan Guyur)"

    return {
        "Top_Buyer_Code":    top_buyer_code,
        "Bandar_Avg_Price":  round(bandar_avg_price, 2),
        "Diff_Pct":          round(diff_pct, 2),
        "Risk_Level":        risk,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Konfigurasi
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi Screener")
    st.markdown("---")

    watchlist_input = st.text_area(
        "📋 Watchlist (satu ticker per baris)",
        value="\n".join(DEFAULT_WATCHLIST),
        height=160,
        help="Format: BBCA.JK, BMRI.JK, dll."
    )

    st.markdown("---")
    st.markdown("**🔧 Parameter Filter**")

    rsi_min = st.slider("RSI Min", 20, 60, 40)
    rsi_max = st.slider("RSI Max", 50, 80, 65)
    gc_max_days = st.slider("Golden Cross Maks (hari)", 1, 7, 3)
    vol_multiplier = st.slider("Volume Multiplier (x)", 1.0, 3.0, 1.5, 0.1)

    st.markdown("---")
    show_broker = st.checkbox("🏦 Tampilkan Detail Broker", value=True)
    show_log    = st.checkbox("📜 Tampilkan Scan Log", value=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#3a6080; line-height:1.8;'>
    ⚠️ <b>Disclaimer</b><br>
    Aplikasi ini hanya untuk tujuan edukasi dan riset.<br>
    Data Bandarmologi adalah <b>simulasi (mock data)</b>.<br>
    Bukan merupakan rekomendasi investasi.<br><br>
    Selalu lakukan analisis mandiri sebelum berinvestasi.
    </div>
    """, unsafe_allow_html=True)

    run_btn = st.button("🚀 JALANKAN SCREENING")


# ─────────────────────────────────────────────────────────────────────────────
# HEADER UTAMA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='hero-title'>
        📈 IHSG SWING TRADING SCREENER
        <span class='hero-badge'>BETA v1.0</span>
    </div>
    <div class='hero-sub'>
        Bursa Efek Indonesia · Technical Analysis + Bandarmologi (Mock Data)
    </div>
</div>
""", unsafe_allow_html=True)

col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.info("**📊 Sumber Data:** yfinance (Yahoo Finance) — 6 bulan historis")
with col_info2:
    st.info("**🕐 Update:** Cache 15 menit · Data T-1 (closing kemarin)")
with col_info3:
    st.info("**🏦 Bandarmologi:** Simulasi Mock Data (Broker Summary BEI tidak tersedia di API publik)")


# ─────────────────────────────────────────────────────────────────────────────
# LOGIKA UTAMA: JALANKAN SAAT TOMBOL DITEKAN
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    # Parse watchlist
    tickers = [t.strip().upper() for t in watchlist_input.splitlines() if t.strip()]
    if not tickers:
        st.error("❌ Watchlist kosong. Tambahkan minimal satu ticker.")
        st.stop()

    # ── Header ticker yang akan di-scan
    st.markdown("<div class='section-title'>🔍 Ticker yang Dipindai</div>", unsafe_allow_html=True)
    st.markdown("".join([f"<span class='ticker-pill'>{t}</span>" for t in tickers]), unsafe_allow_html=True)
    st.markdown("")

    # ── Progress Bar
    progress_bar  = st.progress(0, text="Memulai scan...")
    log_lines     = []
    passed_list   = []
    failed_list   = []

    # ── Scan setiap ticker
    for idx, ticker in enumerate(tickers):
        progress_pct = (idx + 1) / len(tickers)
        progress_bar.progress(progress_pct, text=f"📡 Mengambil data: **{ticker}** ({idx+1}/{len(tickers)})")

        # 1. Download data
        df_raw = fetch_ohlcv(ticker, period="6mo")
        if df_raw is None:
            log_lines.append(f"<span class='err'>✗ {ticker} — Gagal mengambil data / data tidak cukup</span>")
            failed_list.append({"Ticker": ticker, "Alasan": "Data tidak tersedia"})
            continue

        # 2. Hitung indikator
        df_ind = compute_indicators(df_raw.copy())
        df_ind  = df_ind.dropna(subset=["MA20", "RSI", "Vol_SMA20"])
        if df_ind.empty:
            log_lines.append(f"<span class='err'>✗ {ticker} — Indikator tidak dapat dihitung</span>")
            failed_list.append({"Ticker": ticker, "Alasan": "Indikator NaN"})
            continue

        # Override parameter dari sidebar
        last = df_ind.iloc[-1]
        rsi_cur = float(last["RSI"])
        vol_cur = float(last["Volume"])
        vol_sma = float(last["Vol_SMA20"])
        vol_ratio = vol_cur / vol_sma if vol_sma > 0 else 0

        # Gunakan parameter dari sidebar
        rsi_ok   = rsi_min <= rsi_cur <= rsi_max
        vol_ok   = vol_ratio >= vol_multiplier

        gc_days = macd_golden_cross_days_ago(df_ind)
        gc_ok   = (gc_days is not None) and (gc_days <= gc_max_days)

        close  = float(last["Close"])
        ma5    = float(last["MA5"])
        ma10   = float(last["MA10"])
        ma20   = float(last["MA20"])
        macd_v = float(last["MACD"])
        sig_v  = float(last["Signal"])

        trend_ok = (close > ma5) and (ma5 > ma10) and (ma10 > ma20)
        macd_ok  = macd_v > sig_v

        all_pass = trend_ok and macd_ok and gc_ok and rsi_ok and vol_ok

        if not all_pass:
            reasons = []
            if not trend_ok: reasons.append("Trend❌")
            if not macd_ok:  reasons.append("MACD❌")
            if not gc_ok:    reasons.append(f"GC={gc_days}d❌" if gc_days is not None else "GC=None❌")
            if not rsi_ok:   reasons.append(f"RSI={rsi_cur:.1f}❌")
            if not vol_ok:   reasons.append(f"Vol={vol_ratio:.1f}x❌")
            log_lines.append(f"<span class='warn'>⊘ {ticker} — Tidak lolos: {', '.join(reasons)}</span>")
            failed_list.append({"Ticker": ticker, "Alasan": " | ".join(reasons)})
            continue

        # 3. Bandarmologi (mock data)
        broker_df = get_broker_data(ticker, close)
        risk_data = compute_risk_level(broker_df, close)

        passed_list.append({
            "Ticker":              ticker,
            "Close Price (IDR)":   f"Rp {close:,.0f}",
            "RSI (14)":            f"{rsi_cur:.1f}",
            "Status MACD":         f"✅ GC {gc_days}d lalu",
            "Volume Breakout":     f"✅ YES ({vol_ratio:.1f}x)",
            "Top Buyer Code":      risk_data["Top_Buyer_Code"],
            "Top Buyer Name":      BROKER_POOL.get(risk_data["Top_Buyer_Code"], "-"),
            "Bandar Avg Price":    f"Rp {risk_data['Bandar_Avg_Price']:,.2f}",
            "Selisih (%)":         f"{risk_data['Diff_Pct']:+.2f}%",
            "Risk Level":          risk_data["Risk_Level"],
            # Simpan data mentah untuk detail
            "_broker_df":          broker_df,
            "_close":              close,
            "_rsi":                rsi_cur,
        })

        log_lines.append(
            f"<span class='ok'>✔ {ticker} — LOLOS semua filter · "
            f"RSI={rsi_cur:.1f} · GC={gc_days}d · Vol={vol_ratio:.1f}x · "
            f"{risk_data['Risk_Level'][:2]}</span>"
        )

    progress_bar.empty()

    # ─────────────────────────────────────────────────────────────────────────
    # RINGKASAN METRIK
    # ─────────────────────────────────────────────────────────────────────────
    n_total  = len(tickers)
    n_passed = len(passed_list)
    n_failed = len(failed_list)

    low_risk   = sum(1 for r in passed_list if "LOW"    in r["Risk Level"])
    med_risk   = sum(1 for r in passed_list if "MEDIUM" in r["Risk Level"])
    high_risk  = sum(1 for r in passed_list if "HIGH"   in r["Risk Level"])

    st.markdown("<div class='section-title'>📊 Ringkasan Scan</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='metric-grid'>
        <div class='metric-card'>
            <div class='metric-value'>{n_total}</div>
            <div class='metric-label'>Total Ticker</div>
        </div>
        <div class='metric-card green'>
            <div class='metric-value'>{n_passed}</div>
            <div class='metric-label'>Lolos Filter</div>
        </div>
        <div class='metric-card red'>
            <div class='metric-value'>{n_failed}</div>
            <div class='metric-label'>Tidak Lolos</div>
        </div>
        <div class='metric-card green'>
            <div class='metric-value'>{low_risk}</div>
            <div class='metric-label'>🟢 Low Risk</div>
        </div>
        <div class='metric-card yellow'>
            <div class='metric-value'>{med_risk}</div>
            <div class='metric-label'>🟡 Medium Risk</div>
        </div>
        <div class='metric-card red'>
            <div class='metric-value'>{high_risk}</div>
            <div class='metric-label'>🔴 High Risk</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # HASIL SCREENING — TABEL UTAMA
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>✅ Saham yang Lolos Screening</div>", unsafe_allow_html=True)

    if not passed_list:
        st.warning("⚠️ Tidak ada saham yang memenuhi semua kriteria swing trading pada watchlist ini saat ini. Coba tambah ticker atau sesuaikan parameter.")
    else:
        # Kolom yang ditampilkan di tabel utama (exclude kolom internal)
        display_cols = [
            "Ticker", "Close Price (IDR)", "RSI (14)", "Status MACD",
            "Volume Breakout", "Top Buyer Code", "Top Buyer Name",
            "Bandar Avg Price", "Selisih (%)", "Risk Level"
        ]
        display_df = pd.DataFrame([
            {c: r[c] for c in display_cols} for r in passed_list
        ])

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ── Detail per saham (Expander + Broker Table)
        if show_broker:
            st.markdown("<div class='section-title'>🏦 Detail Broker Summary (Mock Data)</div>", unsafe_allow_html=True)
            for result in passed_list:
                ticker = result["Ticker"]
                broker_df_show = result["_broker_df"][
                    ["Broker_Code", "Broker_Name", "Net_Volume_Lot", "Net_Value_IDR"]
                ].copy()
                broker_df_show["Net_Value_IDR"] = broker_df_show["Net_Value_IDR"].apply(
                    lambda x: f"Rp {x:,.0f}"
                )
                broker_df_show.columns = ["Kode", "Nama Broker", "Net Volume (Lot)", "Net Value (IDR)"]

                with st.expander(f"📋 {ticker} — Broker Flow Summary"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.dataframe(broker_df_show, use_container_width=True, hide_index=True)
                    with col_b:
                        st.metric("Close Price",   result["Close Price (IDR)"])
                        st.metric("Bandar Avg",    result["Bandar Avg Price"])
                        st.metric("Selisih Harga", result["Selisih (%)"])
                        st.metric("Risk Level",    result["Risk Level"])

    # ─────────────────────────────────────────────────────────────────────────
    # TABEL YANG TIDAK LOLOS
    # ─────────────────────────────────────────────────────────────────────────
    if failed_list:
        with st.expander(f"❌ Saham Tidak Lolos ({len(failed_list)} ticker)"):
            st.dataframe(pd.DataFrame(failed_list), use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────────────────────────────────
    # SCAN LOG
    # ─────────────────────────────────────────────────────────────────────────
    if show_log and log_lines:
        st.markdown("<div class='section-title'>📜 Scan Log</div>", unsafe_allow_html=True)
        log_content = "<br>".join(log_lines)
        st.markdown(f"""
        <div class='log-box'>
            [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scan selesai — {n_passed}/{n_total} lolos<br>
            {'<br>'.join(log_lines)}
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # LEGENDA & PENJELASAN FILTER
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📖 Legenda & Kriteria Filter</div>", unsafe_allow_html=True)
    with st.expander("Tampilkan penjelasan lengkap kriteria screening"):
        st.markdown(f"""
        | Filter | Kriteria | Keterangan |
        |--------|----------|------------|
        | 📈 **Trend** | Close > MA5 > MA10 > MA20 | MA Stack Bullish — konfirmasi tren naik bertahap |
        | ⚡ **MACD** | MACD > Signal | Momentum bullish aktif |
        | 🎯 **Golden Cross** | GC ≤ {gc_max_days} hari lalu | Entry dini sebelum momentum habis |
        | 📊 **RSI** | {rsi_min} ≤ RSI ≤ {rsi_max} | Tidak overbought, tidak oversold ekstrem |
        | 🔊 **Volume** | Volume > {vol_multiplier}x Vol SMA20 | Konfirmasi minat pasar / akumulasi bandar |

        **Risk Level (Bandarmologi Mock):**
        - 🟢 **LOW RISK (Strong Buy)** — Current Price ≤ Bandar Avg + 3% → Bandar masih "mengamankan" posisi
        - 🟡 **MEDIUM RISK (Hold)** — Selisih 3%–7% → Harga mulai jauh dari basis bandar, perlu cautious
        - 🔴 **HIGH RISK (Rawan Guyur)** — Selisih > 7% → Bandar bisa melepas posisi sewaktu-waktu

        > ⚠️ **Catatan Penting:** Data Broker Summary adalah **simulasi mock data** karena API publik
        > (yfinance) tidak menyediakan data Broker Summary BEI secara langsung.
        > Untuk data real, gunakan platform seperti RTI Business, Stockbit Pro, atau Mirae HOTS.
        """)

# ─────────────────────────────────────────────────────────────────────────────
# STATE AWAL — Sebelum tombol ditekan
# ─────────────────────────────────────────────────────────────────────────────
else:
    st.markdown("<div class='section-title'>🚀 Cara Penggunaan</div>", unsafe_allow_html=True)
    st.markdown("""
    1. **Edit Watchlist** di sidebar — tambah/hapus ticker BEI (format: `BBCA.JK`)
    2. **Sesuaikan Parameter** filter RSI, Golden Cross, dan Volume Multiplier
    3. Klik tombol **🚀 JALANKAN SCREENING** di sidebar
    4. Analisis hasil di tabel dan detail broker flow
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📋 Kriteria Teknikal yang Digunakan:**")
        st.markdown("""
        - ✅ **MA Stack Bullish**: Close > MA5 > MA10 > MA20
        - ✅ **MACD Golden Cross**: Terjadi ≤ 3 hari lalu
        - ✅ **RSI**: 40–65 (momentum tanpa overbought)
        - ✅ **Volume Breakout**: > 1.5x rata-rata 20 hari
        """)
    with col2:
        st.markdown("**🏦 Fitur Bandarmologi (Mock):**")
        st.markdown("""
        - 🔍 Simulasi Net Flow per Broker
        - 💰 Kalkulasi Harga Rata-rata Top Buyer
        - 🎯 Risk Level: LOW / MEDIUM / HIGH
        - 📊 Perbandingan Bandar Avg vs Current Price
        """)

    st.markdown("---")
    st.caption(f"⏱️ Last refresh: {datetime.now().strftime('%d %B %Y, %H:%M WIB')} · Data: yfinance (T-1 closing)")
