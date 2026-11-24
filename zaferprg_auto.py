import io
import math
import re
import unicodedata
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zaferopta Quant Pro V36.1",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #05080f;
        color: #f3f4f6;
    }
    .z-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid #ffd700;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 14px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
    }
    .z-header h1 {
        color: #ffd700;
        font-size: 20px;
        letter-spacing: 1.5px;
        margin: 0 0 4px 0;
    }
    .z-header p {
        color: #00f3ff;
        font-size: 11px;
        text-transform: uppercase;
        font-weight: bold;
        margin: 0;
    }
    .engine-card {
        background-color: #0b1120;
        border-left: 4px solid #00f3ff;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        font-size: 13px;
        line-height: 1.6;
    }
    .engine-card h4 {
        margin: 0 0 8px 0;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .score-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        margin-top: 8px;
    }
    .score-item {
        background: #131b2e;
        border: 1px solid #1e293b;
        padding: 7px;
        text-align: center;
        border-radius: 6px;
    }
    .score-item .sc {
        font-weight: bold;
        color: #00f3ff;
        font-size: 14px;
    }
    .score-item .pr {
        font-size: 11px;
        color: #9ca3af;
    }
    .consensus-box {
        background: linear-gradient(135deg, #064e3b, #022c22);
        border: 2px solid #ffd700;
        padding: 16px;
        border-radius: 10px;
        margin-top: 14px;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.25);
        color: #ffffff;
        font-size: 13px;
        line-height: 1.85;
    }
    .consensus-title {
        color: #ffd700;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .seal-badge {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        margin-left: 4px;
    }
    .seal-triple { background: #ffd700; color: #000000; }
    .seal-ok { background: #00ff66; color: #000000; }
    .seal-diff { background: #ff9900; color: #000000; }
    .seal-pass { background: #ff3366; color: #ffffff; }
    .alert-def {
        margin-top: 8px;
        padding: 8px;
        border-radius: 6px;
        background: rgba(0, 243, 255, 0.12);
        border: 1px solid #00f3ff;
        color: #e0f2fe;
        font-size: 12px;
    }
    .alert-backbone {
        margin-top: 8px;
        padding: 8px;
        border-radius: 6px;
        background: rgba(168, 85, 247, 0.16);
        border: 1px solid #a855f7;
        color: #f3e8ff;
        font-size: 12px;
    }
    .alert-caution {
        margin-top: 8px;
        padding: 8px;
        border-radius: 6px;
        background: rgba(255, 153, 0, 0.16);
        border: 1px solid #ff9900;
        color: #fef3c7;
        font-size: 12px;
    }
    .alert-radar {
        margin-top: 8px;
        padding: 9px;
        border-radius: 6px;
        background: rgba(255, 215, 0, 0.15);
        border: 1px solid #ffd700;
        color: #fef08a;
        font-size: 12px;
    }
    .seal-footer {
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 215, 0, 0.35);
        text-align: center;
        font-size: 13px;
        color: #ffd700;
        font-weight: bold;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

STOP_WORDS = {
    "fc", "fk", "sk", "sc", "cf", "ac", "as", "afc", "bc", "wba",
    "club", "clube", "sport", "spor", "kulubu", "calcio", "olympique", "de"
}


def norm_text(val) -> str:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return ""
    s = str(val)
    tr_map = {
        "İ": "i", "I": "i", "ı": "i",
        "Ş": "s", "ş": "s",
        "Ğ": "g", "ğ": "g",
        "Ü": "u", "ü": "u",
        "Ö": "o", "ö": "o",
        "Ç": "c", "ç": "c",
    }
    for k, v in tr_map.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_generic_words(norm_str: str) -> str:
    tokens = [t for t in norm_str.split(" ") if len(t) > 1 and t not in STOP_WORDS]
    return " ".join(tokens).strip()


def match_team_in_cell(cell_norm: str, q_norm: str, q_core: str, strict_only: bool) -> bool:
    if not cell_norm or not q_norm:
        return False
    if cell_norm == q_norm or q_norm in cell_norm:
        return True
    if cell_norm in q_norm and len(cell_norm) >= 4:
        return True
    if strict_only:
        return False
    cell_core = strip_generic_words(cell_norm)
    if q_core and cell_core:
        if cell_core == q_core or q_core in cell_core:
            return True
        if cell_core in q_core and len(cell_core) >= 4:
            return True
    return False


def parse_score(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    s = str(val).strip()
    if not s:
        return None
    m = re.match(r"^(\d{1,2})\s*[-:–—]\s*(\d{1,2})$", s)
    if not m:
        return None
    h, a = int(m.group(1)), int(m.group(2))
    if h > 15 or a > 15:
        return None
    return (h, a)


def detect_columns(df: pd.DataFrame) -> dict:
    headers = list(df.columns)
    norm_headers = [(h, norm_text(h)) for h in headers]

    home_col = next(
        (h for h, n in norm_headers if n == "ev sahibi" or "ev sahibi" in n),
        next((h for h, n in norm_headers if n in {"ev", "home"} or "home team" in n), ""),
    )
    away_col = next(
        (h for h, n in norm_headers if n == "deplasman" or "deplasman" in n),
        next((h for h, n in norm_headers if n in {"dep", "away"} or "away team" in n), ""),
    )

    score_candidates = []
    sample_df = df.head(60)
    for h, hn in norm_headers:
        if not h or h in {home_col, away_col}:
            continue
        if "iy ms" in hn or hn == "iyms" or "tarih" in hn or "saat" in hn:
            continue
        hits = 0
        goal_sum = 0
        for val in sample_df[h]:
            sc = parse_score(val)
            if sc is not None:
                hits += 1
                goal_sum += sc[0] + sc[1]
        if hits >= 5:
            score_candidates.append((h, hn, hits, goal_sum / hits))

    ht_col = next(
        (h for h, hn, _, _ in score_candidates if hn in {"skor iy", "iy skor", "ilk yari skor", "ht score"}),
        next(
            (
                h for h, hn, _, _ in score_candidates
                if ("iy" in hn or "ht" in hn or "ilk yari" in hn) and "ms" not in hn and "ft" not in hn
            ),
            next((h for h, n in norm_headers if n in {"skor iy", "iy skor"}), ""),
        ),
    )

    ms_col = next(
        (
            h for h, hn, _, _ in score_candidates
            if h != ht_col and hn in {"skor ms", "ms skor", "mac sonu skor", "ft score"}
        ),
        next(
            (
                h for h, hn, _, _ in score_candidates
                if h != ht_col and ("ms" in hn or "ft" in hn) and "iy" not in hn and "ht" not in hn
            ),
            next(
                (
                    h for h, hn, _, _ in score_candidates
                    if h != ht_col and "skor" in hn and "iy" not in hn and "ht" not in hn
                ),
                "",
            ),
        ),
    )
    if not ms_col:
        rem = [x for x in score_candidates if x[0] != ht_col and "iy" not in x[1] and "ht" not in x[1]]
        if rem:
            rem.sort(key=lambda x: x[3], reverse=True)
            ms_col = rem[0][0]
        else:
            ms_col = next((h for h, n in norm_headers if n in {"skor ms", "ms skor"}), "")

    home_goal_col = next((h for h, n in norm_headers if n in {"ev gol", "ms ev", "ev skor"}), "")
    away_goal_col = next((h for h, n in norm_headers if n in {"dep gol", "ms dep", "dep skor"}), "")

    return {
        "home": home_col,
        "away": away_col,
        "ms_score": ms_col,
        "ht_score": ht_col,
        "home_goal": home_goal_col,
        "away_goal": away_goal_col,
    }


@st.cache_data(show_spinner=False)
def load_excel_archive(file_bytes: bytes):
    raw_df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0, header=None, dtype=str)
    header_idx = -1
    for r in range(min(16, len(raw_df))):
        row_vals = [norm_text(c) for c in raw_df.iloc[r].tolist()]
        joined = "|".join(row_vals)
        if (
            "ev sahibi" in joined
            or ("ev" in row_vals and "deplasman" in row_vals)
            or ("home" in row_vals and "away" in row_vals)
        ):
            header_idx = r
            break
    if header_idx == -1 and len(raw_df) > 7:
        header_idx = 7

    if header_idx == -1 or len(raw_df) <= header_idx + 1:
        return None, None

    raw_headers = raw_df.iloc[header_idx].tolist()
    headers = []
    seen_cols = {}
    for i, h in enumerate(raw_headers):
        base = str(h).strip() if (h is not None and str(h).strip() != "" and str(h).lower() != "nan") else f"COL_{i}"
        if base in seen_cols:
            seen_cols[base] += 1
            base = f"{base}_{seen_cols[base]}"
        else:
            seen_cols[base] = 0
        headers.append(base)

    df = raw_df.iloc[header_idx + 1:].copy().reset_index(drop=True)
    df.columns = headers
    col_map = detect_columns(df)

    if col_map["home"] or col_map["away"]:
        mask = pd.Series(False, index=df.index)
        if col_map["home"]:
            mask = mask | (df[col_map["home"]].notna() & (df[col_map["home"]].astype(str).str.strip() != ""))
        if col_map["away"]:
            mask = mask | (df[col_map["away"]].notna() & (df[col_map["away"]].astype(str).str.strip() != ""))
        df = df[mask].reset_index(drop=True)

    return df, col_map


def get_row_ms_score(row: pd.Series, col_map: dict):
    if col_map["ms_score"]:
        sc = parse_score(row.get(col_map["ms_score"]))
        if sc is not None:
            return sc
    if col_map["home_goal"] and col_map["away_goal"]:
        try:
            h = int(float(str(row.get(col_map["home_goal"])).strip()))
            a = int(float(str(row.get(col_map["away_goal"])).strip()))
            return (h, a)
        except (ValueError, TypeError):
            pass
    return None


def get_row_ht_score(row: pd.Series, col_map: dict):
    if col_map["ht_score"]:
        return parse_score(row.get(col_map["ht_score"]))
    return None


def find_team_rows(df: pd.DataFrame, col_map: dict, team_name: str):
    q_norm = norm_text(team_name)
    q_core = strip_generic_words(q_norm)
    if df is None or df.empty or not q_norm:
        return [], "", True, q_norm, q_core

    home_col = col_map["home"]
    away_col = col_map["away"]

    matched_indices = []
    strict_mode = True
    for idx, row in df.iterrows():
        ev = norm_text(row.get(home_col, ""))
        dep = norm_text(row.get(away_col, ""))
        if match_team_in_cell(ev, q_norm, q_core, True) or match_team_in_cell(dep, q_norm, q_core, True):
            matched_indices.append(idx)

    if not matched_indices:
        strict_mode = False
        for idx, row in df.iterrows():
            ev = norm_text(row.get(home_col, ""))
            dep = norm_text(row.get(away_col, ""))
            if match_team_in_cell(ev, q_norm, q_core, False) or match_team_in_cell(dep, q_norm, q_core, False):
                matched_indices.append(idx)

    matched_label = ""
    if matched_indices:
        r0 = df.loc[matched_indices[0]]
        ev0 = norm_text(r0.get(home_col, ""))
        matched_label = r0.get(home_col, "") if match_team_in_cell(ev0, q_norm, q_core, strict_mode) else r0.get(away_col, "")

    return matched_indices, str(matched_label).strip(), strict_mode, q_norm, q_core


def calc_team_stats(df: pd.DataFrame, col_map: dict, indices: list, strict_mode: bool, q_norm: str, q_core: str):
    if not indices:
        return None

    played = scored = conceded = wins = draws = losses = 0
    home_played = home_wins = home_scored = home_conceded = 0
    away_played = away_wins = away_scored = away_conceded = 0
    ewma_points = 0.0
    ewma_weight_sum = 0.0
    total_recent = len(indices)

    for pos, idx in enumerate(indices):
        row = df.loc[idx]
        ev = norm_text(row.get(col_map["home"], ""))
        dep = norm_text(row.get(col_map["away"], ""))
        sc = get_row_ms_score(row, col_map)
        if sc is None:
            continue

        is_home = match_team_in_cell(ev, q_norm, q_core, strict_mode)
        is_away = (not is_home) and match_team_in_cell(dep, q_norm, q_core, strict_mode)
        if not is_home and not is_away:
            continue

        gf = sc[0] if is_home else sc[1]
        ga = sc[1] if is_home else sc[0]
        played += 1
        scored += gf
        conceded += ga

        if gf > ga:
            wins += 1
            pts = 3
            if is_home:
                home_wins += 1
            else:
                away_wins += 1
        elif gf == ga:
            draws += 1
            pts = 1
        else:
            losses += 1
            pts = 0

        if is_home:
            home_played += 1
            home_scored += gf
            home_conceded += ga
        else:
            away_played += 1
            away_scored += gf
            away_conceded += ga

        w = 0.85 ** max(0, total_recent - 1 - pos)
        ewma_points += (pts / 3.0) * w
        ewma_weight_sum += w

    if played == 0:
        return None

    return {
        "played": played,
        "avg_scored": scored / played,
        "avg_conceded": conceded / played,
        "home_played": home_played,
        "home_avg_scored": (home_scored / home_played) if home_played >= 3 else (scored / played),
        "home_avg_conceded": (home_conceded / home_played) if home_played >= 3 else (conceded / played),
        "away_played": away_played,
        "away_avg_scored": (away_scored / away_played) if away_played >= 3 else (scored / played),
        "away_avg_conceded": (away_conceded / away_played) if away_played >= 3 else (conceded / played),
        "win_rate": round((wins / played) * 100),
        "home_win_rate": round((home_wins / home_played) * 100) if home_played > 0 else round((wins / played) * 100),
        "away_win_rate": round((away_wins / away_played) * 100) if away_played > 0 else round((wins / played) * 100),
        "ewma_form": round((ewma_points / ewma_weight_sum) * 100) if ewma_weight_sum > 0 else 50,
    }


def poisson_prob(lam: float, k: int) -> float:
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def dixon_coles_tau(h: int, a: int, lam: float, mu: float, rho: float) -> float:
    if h == 0 and a == 0:
        return max(0.25, 1.0 - lam * mu * rho)
    if h == 0 and a == 1:
        return max(0.25, 1.0 + lam * rho)
    if h == 1 and a == 0:
        return max(0.25, 1.0 + mu * rho)
    if h == 1 and a == 1:
        return max(0.25, 1.0 - rho)
    return 1.0


def poisson_over_total_prob(total_lambda: float, line: float) -> float:
    max_under = int(math.floor(line))
    under_sum = sum(poisson_prob(total_lambda, k) for k in range(max_under + 1))
    return max(0.01, min(0.99, 1.0 - under_sum))


def analyze_injury_text(text: str) -> dict:
    if not text or len(text.strip()) < 2 or text.strip().lower() == "yok":
        return {
            "att_pen": 0.0,
            "def_pen": 0.0,
            "gk_pen": 0.0,
            "count": 0,
            "starter_count": 0,
            "key_count": 0,
            "def_starter_count": 0,
            "gk_starter_count": 0,
            "att_mid_starter_count": 0,
            "bench_count": 0,
            "def_collapse": False,
            "weak_subs": [],
            "note": "Tam kadro (etkili eksik yok)",
        }

    items = [x.strip() for x in re.split(r",|;| ve |\/|\+", text) if len(x.strip()) > 1]
    att_pen = def_pen = gk_pen = 0.0
    starter_count = key_count = bench_count = 0
    def_starter_count = gk_starter_count = att_mid_starter_count = 0
    weak_subs = []

    for item in items:
        t = norm_text(item)
        if re.search(r"\b(yedek|uzun|rotasyon|genc|bench|sub)\b", t):
            bench_count += 1
            continue

        rating_match = re.search(r"\b([4-9][.,]\d{1,2})\b", item)
        sub_mult = 1.0
        if rating_match:
            r_val = float(rating_match.group(1).replace(",", "."))
            if r_val < 6.20:
                sub_mult = 1.35
                weak_subs.append(f"{item.split(' ')[0]} ({r_val:.1f})")
            elif r_val < 6.50:
                sub_mult = 1.20
                weak_subs.append(f"{item.split(' ')[0]} ({r_val:.1f})")
            elif r_val >= 6.80:
                sub_mult = 0.80

        is_key = bool(
            re.search(r"\b(kilit|yildiz|kaptan|as|star|key)\b", t)
            or "golcu" in t
            or "oyun kurucu" in t
            or "10 numara" in t
        )
        mult = (1.35 if is_key else 1.0) * sub_mult
        starter_count += 1
        if is_key:
            key_count += 1

        is_gk = "kaleci" in t or bool(re.search(r"\bgk\b", t))
        is_def = (not is_gk) and any(k in t for k in ("stoper", "defans", "bek", "savunma"))
        is_att = (not is_gk) and any(k in t for k in ("forvet", "santrafor", "golcu", "kanat", "hucum"))
        is_playmaker = (not is_gk) and (not is_def) and (
            "oyun kurucu" in t or "10 numara" in t or ("orta saha" in t and is_key)
        )
        is_mid = (not is_gk) and (not is_def) and (not is_att) and (not is_playmaker) and any(
            k in t for k in ("orta saha", "libero", "merkez")
        )

        b_att = b_def = b_gk = 0.0
        if is_gk:
            gk_starter_count += 1
            b_gk += 0.05
        elif is_def:
            def_starter_count += 1
            b_def += 0.11
            b_att += 0.01
        elif is_playmaker:
            att_mid_starter_count += 1
            b_att += 0.065
            b_def += 0.035
        elif is_att:
            att_mid_starter_count += 1
            b_att += 0.05
            b_def += 0.005
        elif is_mid:
            att_mid_starter_count += 1
            b_att += 0.03
            b_def += 0.035
        else:
            att_mid_starter_count += 1
            b_att += 0.03
            b_def += 0.03

        att_pen += b_att * mult
        def_pen += b_def * mult
        gk_pen += b_gk * mult

    def_collapse = def_starter_count >= 2
    if def_collapse:
        def_pen += 0.12 + max(0, def_starter_count - 2) * 0.06

    att_pen = min(0.28, att_pen)
    def_pen = min(0.55, def_pen)
    gk_pen = min(0.12, gk_pen)

    tier_summary = f"{starter_count} ilk 11"
    role_parts = []
    if def_starter_count > 0:
        role_parts.append(f"{def_starter_count} savunma")
    if gk_starter_count > 0:
        role_parts.append(f"{gk_starter_count} kaleci")
    if role_parts:
        tier_summary += f" ({', '.join(role_parts)})"
    if bench_count > 0:
        tier_summary += f", {bench_count} yedek/uzun (%0)"

    tags = ""
    if def_collapse:
        tags += " [🚨 SAVUNMA ÇÖKÜŞÜ]"
    if weak_subs:
        tags += f" [⚠️ Zayıf İkame: {', '.join(weak_subs)}]"

    gk_note = f", Kaleci -%{round(gk_pen * 100)}" if gk_pen > 0 else ""
    note = (
        f"{tier_summary} ➔ Savunma Zafiyeti -%{round(def_pen * 100)}"
        f"{gk_note}, Hücum/OS -%{round(att_pen * 100)}{tags}"
    )

    return {
        "att_pen": att_pen,
        "def_pen": def_pen,
        "gk_pen": gk_pen,
        "count": len(items),
        "starter_count": starter_count,
        "key_count": key_count,
        "def_starter_count": def_starter_count,
        "gk_starter_count": gk_starter_count,
        "att_mid_starter_count": att_mid_starter_count,
        "bench_count": bench_count,
        "def_collapse": def_collapse,
        "weak_subs": weak_subs,
        "note": note,
    }


def normalize_weights(raw_dict: dict) -> dict:
    keys = list(raw_dict.keys())
    total_raw = sum(max(0.0, raw_dict[k]) for k in keys)
    if total_raw <= 0:
        return {"w1": 35, "w2": 20, "w3": 15, "w4": 10, "w5": 20}
    res = {}
    total_int = 0
    for k in keys:
        res[k] = round((max(0.0, raw_dict[k]) / total_raw) * 100)
        total_int += res[k]
    diff = 100 - total_int
    if diff != 0:
        max_key = max(keys, key=lambda k: res[k])
        res[max_key] += diff
    return res


def fetch_injuries_via_gemini(api_key: str, match_name: str):
    prompt = (
        f"{match_name} futbol maçı için her iki takımın bugünkü güncel sakat ve cezalı İLK 11 oyuncularını "
        "internetten araştır. Uzun süreli veya yedek oyuncuları yazma. Stoper, bek, kaleci ve kilit oyun kurucu "
        "mevkilerini ayrı ve net belirt. Eğer yerine ilk 11'de geçecek yedek oyuncunun güncel SofaScore/WhoScored "
        "sezon puanını gerçek kaynakta bulabiliyorsan ve 6.50 altındaysa oyuncunun yanına puanı ekle "
        "(örn: Lacroix stoper 6.3); gerçek puan bulamazsan kesinlikle tahmin etme ve sayı yazma. "
        "Sadece şu 2 satır formatında kısa cevap ver:\n"
        "EV: [eksik oyuncular ve mevkileri, yoksa Yok]\n"
        "DEP: [eksik oyuncular ve mevkileri, yoksa Yok]"
    )

    def call_model(model_name: str, use_search: bool):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key.strip()}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if use_search:
            payload["tools"] = [{"google_search": {}}]
        return requests.post(url, json=payload, timeout=25)

    candidates = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.0-flash"]
    tried = []
    resp = None
    used_model = ""

    for m in candidates:
        tried.append(m)
        resp = call_model(m, True)
        if resp.status_code == 400:
            resp = call_model(m, False)
        if resp.ok:
            used_model = m
            break
        if resp.status_code != 404:
            break

    if resp is None or resp.status_code == 404:
        list_resp = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key.strip()}",
            timeout=15,
        )
        if list_resp.ok:
            models = list_resp.json().get("models", [])
            valid = [
                m["name"].replace("models/", "")
                for m in models
                if "generateContent" in m.get("supportedGenerationMethods", [])
                and m["name"].replace("models/", "") not in tried
            ]
            detected = next((n for n in valid if "flash" in n), valid[0] if valid else None)
            if detected:
                used_model = detected
                resp = call_model(detected, True)
                if resp.status_code == 400:
                    resp = call_model(detected, False)

    if resp is None or not resp.ok:
        code = resp.status_code if resp is not None else "Bağlantı"
        raise RuntimeError(f"API Hatası (HTTP {code})")

    data = resp.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts)

    ev_match = re.search(r"EV:\s*(.+)", text, re.IGNORECASE)
    dep_match = re.search(r"DEP:\s*(.+)", text, re.IGNORECASE)
    ev_txt = ev_match.group(1).replace("*", "").strip() if ev_match else ""
    dep_txt = dep_match.group(1).replace("*", "").strip() if dep_match else ""

    if ev_txt.lower() == "yok":
        ev_txt = ""
    if dep_txt.lower() == "yok":
        dep_txt = ""

    return ev_txt, dep_txt, used_model


st.markdown(
    """
    <div class="z-header">
        <h1>ZAFEROPTA QUANT PRO</h1>
        <p>V36.1 // Omurga Çöküşü + Kilit Oyun Kurucu + +EV Radarı (Python)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "home_inj_val" not in st.session_state:
    st.session_state["home_inj_val"] = ""
if "away_inj_val" not in st.session_state:
    st.session_state["away_inj_val"] = ""

uploaded_file = st.file_uploader("1. 75 SÜTUNLU ARŞİV EXCEL (.XLSX)", type=["xlsx", "xls"])
df_archive = None
col_map = None

if uploaded_file is not None:
    df_archive, col_map = load_excel_archive(uploaded_file.getvalue())
    if df_archive is not None:
        ms_lbl = col_map["ms_score"] or (
            f"{col_map['home_goal']}/{col_map['away_goal']}" if col_map["home_goal"] else "YOK"
        )
        st.success(
            f"✔ {len(df_archive)} satırlık arşiv yüklendi | "
            f"Ev: [{col_map['home'] or 'YOK'}] | Dep: [{col_map['away'] or 'YOK'}] | "
            f"MS: [{ms_lbl}] | İY: [{col_map['ht_score'] or 'YOK'}]"
        )
    else:
        st.error("Excel başlık satırı algılanamadı.")

match_input = st.text_input("2. MAÇ ANALİZİ (EV SAHİBİ - DEPLASMAN)", placeholder="Örn: Galatasaray - Aston Villa")

with st.expander("🤖 CANLI SAKAT & CEZALI TARAMA (GEMINI API)", expanded=False):
    api_key_input = st.text_input("Google AI Studio API Anahtarı", type="password")
    if st.button("🔍 SAKAT / CEZALILARI İNTERNETTEN TARA", use_container_width=True):
        if not api_key_input.strip():
            st.warning("Önce API anahtarını girin.")
        elif "-" not in match_input:
            st.warning("Maç adını 'Ev Sahibi - Deplasman' formatında yazın.")
        else:
            try:
                with st.spinner("İlk 11 sakat/cezalıları taranıyor..."):
                    ev_res, dep_res, model_used = fetch_injuries_via_gemini(api_key_input, match_input)
                    st.session_state["home_inj_val"] = ev_res
                    st.session_state["away_inj_val"] = dep_res
                    st.success(f"✔ Tarama tamamlandı ({model_used}) ve kutulara işlendi.")
            except Exception as exc:
                st.error(f"❌ {exc}")

home_injuries = st.text_input(
    "3. EV SAHİBİ SAKAT / CEZALI OYUNCULAR",
    key="home_inj_val",
    placeholder="Örn: Victor Osimhen kilit forvet, Rafael Leao kilit kanat, Ismail Jakobs bek",
)
away_injuries = st.text_input(
    "4. DEPLASMAN SAKAT / CEZALI OYUNCULAR",
    key="away_inj_val",
    placeholder="Örn: Matty Cash bek, Matteo Ruggeri bek",
)

st.markdown("**5. GOALOO XG & XGA MANUEL GİRİŞİ (OPSİYONEL)**")
c_g1, c_g2 = st.columns(2)
with c_g1:
    g_home_xg = st.number_input("Ev Attack xG", min_value=0.0, max_value=10.0, value=0.0, step=0.01)
    g_away_xg = st.number_input("Dep Attack xG", min_value=0.0, max_value=10.0, value=0.0, step=0.01)
with c_g2:
    g_home_xga = st.number_input("Ev Defence xGA", min_value=0.0, max_value=10.0, value=0.0, step=0.01)
    g_away_xga = st.number_input("Dep Defence xGA", min_value=0.0, max_value=10.0, value=0.0, step=0.01)

st.markdown("**6. GÜNCEL PİYASA ORANLARI & GOL BAREMİ (+EV & KELLY)**")
c_o1, c_o2, c_o3 = st.columns(3)
with c_o1:
    odd_ms1 = st.number_input("MS 1", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
with c_o2:
    odd_ms0 = st.number_input("MS 0", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
with c_o3:
    odd_ms2 = st.number_input("MS 2", min_value=0.0, max_value=100.0, value=0.0, step=0.01)

c_b1, c_b2, c_b3 = st.columns(3)
with c_b1:
    goal_line = st.selectbox("Gol Baremi", [1.5, 2.5, 3.5, 4.5], index=1)
with c_b2:
    odd_over = st.number_input(f"{goal_line:.1f} ÜST", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
with c_b3:
    odd_under = st.number_input(f"{goal_line:.1f} ALT", min_value=0.0, max_value=100.0, value=0.0, step=0.01)

if st.button("👑 TÜM MOTORLARI VE MÜHRÜ ÇALIŞTIR", type="primary", use_container_width=True):
    if "-" not in match_input:
        st.error("Lütfen maç adını araya tire (-) koyarak girin! (Örn: Galatasaray - Aston Villa)")
        st.stop()

    has_goaloo = (g_home_xg > 0 and g_home_xga > 0 and g_away_xg > 0 and g_away_xga > 0)
    if (df_archive is None or df_archive.empty) and not has_goaloo:
        st.error("Lütfen 1. bölümden Excel arşivini yükleyin VEYA 5. bölümden Goaloo xG/xGA değerlerini girin!")
        st.stop()

    parts = match_input.split("-", 1)
    home_team = parts[0].strip()
    away_team = parts[1].strip()
    gl_str = f"{goal_line:.1f}"

    home_indices, home_label, h_strict, h_qnorm, h_qcore = find_team_rows(df_archive, col_map, home_team)
    away_indices, away_label, a_strict, a_qnorm, a_qcore = find_team_rows(df_archive, col_map, away_team)

    combined_indices = list(dict.fromkeys(home_indices + away_indices))
    home_stats = calc_team_stats(df_archive, col_map, home_indices, h_strict, h_qnorm, h_qcore)
    away_stats = calc_team_stats(df_archive, col_map, away_indices, a_strict, a_qnorm, a_qcore)

    if not home_stats and not away_stats and not has_goaloo:
        st.warning(f"'{home_team}' ve '{away_team}' Excel arşivinde bulunamadı ve Goaloo xG girilmedi.")
        st.stop()

    h_inj = analyze_injury_text(home_injuries)
    a_inj = analyze_injury_text(away_injuries)

    h_excel_att = (home_stats["home_avg_scored"] * 0.65 + home_stats["avg_scored"] * 0.35) if home_stats else None
    h_excel_def = (home_stats["home_avg_conceded"] * 0.65 + home_stats["avg_conceded"] * 0.35) if home_stats else None
    a_excel_att = (away_stats["away_avg_scored"] * 0.65 + away_stats["avg_scored"] * 0.35) if away_stats else None
    a_excel_def = (away_stats["away_avg_conceded"] * 0.65 + away_stats["avg_conceded"] * 0.35) if away_stats else None

    excel_home_xg = ((h_excel_att + a_excel_def) / 2.0) * 1.06 if (h_excel_att is not None and a_excel_def is not None) else h_excel_att
    excel_away_xg = ((a_excel_att + h_excel_def) / 2.0) * 0.94 if (a_excel_att is not None and h_excel_def is not None) else a_excel_att

    goaloo_home_xg = (g_home_xg + g_away_xga) / 2.0 if has_goaloo else None
    goaloo_away_xg = (g_away_xg + g_home_xga) / 2.0 if has_goaloo else None

    if excel_home_xg is not None and goaloo_home_xg is not None:
        base_home_xg = (excel_home_xg * 0.5) + (goaloo_home_xg * 0.5)
        base_away_xg = (excel_away_xg * 0.5) + (goaloo_away_xg * 0.5)
    elif goaloo_home_xg is not None:
        base_home_xg = goaloo_home_xg
        base_away_xg = goaloo_away_xg
    else:
        base_home_xg = excel_home_xg if excel_home_xg is not None else 1.35
        base_away_xg = excel_away_xg if excel_away_xg is not None else 1.05

    h_net_missing = h_inj["starter_count"] - a_inj["starter_count"]
    a_net_missing = a_inj["starter_count"] - h_inj["starter_count"]

    h_backbone_collapse = (not h_inj["def_collapse"]) and (
        (h_inj["def_starter_count"] >= 1 and h_inj["gk_starter_count"] >= 1 and h_net_missing >= 1)
        or (h_inj["starter_count"] >= 3 and h_net_missing >= 2)
    )
    a_backbone_collapse = (not a_inj["def_collapse"]) and (
        (a_inj["def_starter_count"] >= 1 and a_inj["gk_starter_count"] >= 1 and a_net_missing >= 1)
        or (a_inj["starter_count"] >= 3 and a_net_missing >= 2)
    )

    single_home_collapse = h_inj["def_collapse"] and not a_inj["def_collapse"]
    single_away_collapse = a_inj["def_collapse"] and not h_inj["def_collapse"]
    both_def_collapse = h_inj["def_collapse"] and a_inj["def_collapse"]

    single_home_backbone = h_backbone_collapse and not a_inj["def_collapse"] and not a_backbone_collapse
    single_away_backbone = a_backbone_collapse and not h_inj["def_collapse"] and not h_backbone_collapse

    home_def_adv_rate = 0.65 if single_away_collapse else (0.55 if single_away_backbone else (0.25 if both_def_collapse else 0.32))
    away_def_adv_rate = 0.65 if single_home_collapse else (0.55 if single_home_backbone else (0.25 if both_def_collapse else 0.32))
    caution_factor = 0.94 if both_def_collapse else 1.0

    home_gap_boost = (1.0 + min(0.12, (a_net_missing - 1) * 0.05)) if (not both_def_collapse and a_net_missing >= 2) else 1.0
    away_gap_boost = (1.0 + min(0.12, (h_net_missing - 1) * 0.05)) if (not both_def_collapse and h_net_missing >= 2) else 1.0
    home_gap_drag = (1.0 - min(0.10, (h_net_missing - 1) * 0.04)) if (not both_def_collapse and h_net_missing >= 2) else 1.0
    away_gap_drag = (1.0 - min(0.10, (a_net_missing - 1) * 0.04)) if (not both_def_collapse and a_net_missing >= 2) else 1.0

    home_att_health = max(0.70, 1.0 - h_inj["att_pen"])
    away_att_health = max(0.70, 1.0 - a_inj["att_pen"])

    home_boost_mult = (1.0 + ((a_inj["def_pen"] * home_def_adv_rate) + a_inj["gk_pen"]) * home_att_health) * home_gap_boost
    away_boost_mult = (1.0 + ((h_inj["def_pen"] * away_def_adv_rate) + h_inj["gk_pen"]) * away_att_health) * away_gap_boost

    home_boost_pct = round((home_boost_mult * caution_factor - 1.0) * 100)
    away_boost_pct = round((away_boost_mult * caution_factor - 1.0) * 100)

    base_home_xg = max(0.30, base_home_xg * (1.0 - h_inj["att_pen"]) * home_gap_drag * home_boost_mult * caution_factor)
    base_away_xg = max(0.25, base_away_xg * (1.0 - a_inj["att_pen"]) * away_gap_drag * away_boost_mult * caution_factor)

    rho = -0.13
    score_matrix = []
    total_prob = 0.0
    for h in range(9):
        for a in range(9):
            tau = dixon_coles_tau(h, a, base_home_xg, base_away_xg, rho)
            p = poisson_prob(base_home_xg, h) * poisson_prob(base_away_xg, a) * tau
            score_matrix.append({"home": h, "away": a, "prob": p})
            total_prob += p

    p_home_win = p_draw = p_away_win = m1_btts_prob = 0.0
    m1_over15 = m1_over25 = m1_over35 = m1_over45 = m1_sel_over = 0.0

    for item in score_matrix:
        item["prob"] /= total_prob
        tot = item["home"] + item["away"]
        if item["home"] > item["away"]:
            p_home_win += item["prob"]
        elif item["home"] == item["away"]:
            p_draw += item["prob"]
        else:
            p_away_win += item["prob"]
        if tot > 1.5:
            m1_over15 += item["prob"]
        if tot > 2.5:
            m1_over25 += item["prob"]
        if tot > 3.5:
            m1_over35 += item["prob"]
        if tot > 4.5:
            m1_over45 += item["prob"]
        if tot > goal_line:
            m1_sel_over += item["prob"]
        if item["home"] > 0 and item["away"] > 0:
            m1_btts_prob += item["prob"]

    score_matrix.sort(key=lambda x: x["prob"], reverse=True)
    m1_sel_under = max(0.0, 1.0 - m1_sel_over)
    m1_sel_over_pct = round(m1_sel_over * 100)
    m1_over25_pct = round(m1_over25 * 100)
    m1_over35_pct = round(m1_over35 * 100)
    m1_over45_pct = round(m1_over45 * 100)

    ht_home_xg = base_home_xg * 0.44
    ht_away_xg = base_away_xg * 0.44
    p_ht1 = p_htx = p_ht2 = p_ht_over05 = ht_tot_prob = 0.0
    for h in range(6):
        for a in range(6):
            tau_ht = dixon_coles_tau(h, a, ht_home_xg, ht_away_xg, -0.10)
            p = poisson_prob(ht_home_xg, h) * poisson_prob(ht_away_xg, a) * tau_ht
            ht_tot_prob += p
            if h > a:
                p_ht1 += p
            elif h == a:
                p_htx += p
            else:
                p_ht2 += p
            if (h + a) > 0.5:
                p_ht_over05 += p

    m1_ht1_pct = round((p_ht1 / ht_tot_prob) * 100)
    m1_htx_pct = round((p_htx / ht_tot_prob) * 100)
    m1_ht2_pct = max(0, 100 - m1_ht1_pct - m1_htx_pct)
    m1_ht05_pct = round((p_ht_over05 / ht_tot_prob) * 100)
    m1_ht_taraf = "İY 1" if (m1_ht1_pct >= m1_htx_pct and m1_ht1_pct >= m1_ht2_pct) else (
        "İY 2" if (m1_ht2_pct >= m1_htx_pct and m1_ht2_pct > m1_ht1_pct) else "İY X"
    )

    m1_btts_pct = round(m1_btts_prob * 100)
    m1_taraf_pick = "MS 1" if (p_home_win >= p_away_win and p_home_win >= p_draw) else (
        "MS 2" if (p_away_win > p_home_win and p_away_win >= p_draw) else "MS 0"
    )
    m1_taraf_prob = max(p_home_win, p_draw, p_away_win)
    m1_taraf_conf = round(m1_taraf_prob * 100)

    over_sel_cnt = over25_cnt = over35_cnt = over45_cnt = btts_cnt = valid_rows = 0
    ht05_cnt = ht1_cnt = htx_cnt = ht2_cnt = valid_ht_rows = 0

    for idx in combined_indices:
        row = df_archive.loc[idx]
        sc = get_row_ms_score(row, col_map)
        if sc is not None:
            valid_rows += 1
            tot = sc[0] + sc[1]
            if tot > goal_line:
                over_sel_cnt += 1
            if tot > 2.5:
                over25_cnt += 1
            if tot > 3.5:
                over35_cnt += 1
            if tot > 4.5:
                over45_cnt += 1
            if sc[0] > 0 and sc[1] > 0:
                btts_cnt += 1
        sc_iy = get_row_ht_score(row, col_map)
        if sc_iy is not None:
            valid_ht_rows += 1
            if (sc_iy[0] + sc_iy[1]) > 0.5:
                ht05_cnt += 1
            if sc_iy[0] > sc_iy[1]:
                ht1_cnt += 1
            elif sc_iy[0] == sc_iy[1]:
                htx_cnt += 1
            else:
                ht2_cnt += 1

    m2_has_data = valid_rows > 0
    m2_sel_over_pct = round((over_sel_cnt / valid_rows) * 100) if m2_has_data else m1_sel_over_pct
    m2_over25_pct = round((over25_cnt / valid_rows) * 100) if m2_has_data else m1_over25_pct
    m2_over35_pct = round((over35_cnt / valid_rows) * 100) if m2_has_data else m1_over35_pct
    m2_over45_pct = round((over45_cnt / valid_rows) * 100) if m2_has_data else m1_over45_pct
    m2_btts_pct = round((btts_cnt / valid_rows) * 100) if m2_has_data else m1_btts_pct
    m2_ht05_pct = round((ht05_cnt / valid_ht_rows) * 100) if valid_ht_rows > 0 else m1_ht05_pct
    m2_ht1_pct = round((ht1_cnt / valid_ht_rows) * 100) if valid_ht_rows > 0 else m1_ht1_pct
    m2_htx_pct = round((htx_cnt / valid_ht_rows) * 100) if valid_ht_rows > 0 else m1_htx_pct
    m2_ht2_pct = max(0, 100 - m2_ht1_pct - m2_htx_pct) if valid_ht_rows > 0 else m1_ht2_pct
    m2_ht_taraf = "İY 1" if (m2_ht1_pct >= m2_htx_pct and m2_ht1_pct >= m2_ht2_pct) else (
        "İY 2" if (m2_ht2_pct >= m2_htx_pct and m2_ht2_pct > m2_ht1_pct) else "İY X"
    )

    KELLY_CAP = 5.0

    def check_ev(label: str, prob: float, mkt_odd: float):
        if mkt_odd <= 1.01:
            return None
        ev = (prob * mkt_odd) - 1.0
        ev_pct = f"{ev * 100:.1f}"
        raw_kelly = (((mkt_odd - 1.0) * prob - (1.0 - prob)) / (mkt_odd - 1.0)) * 0.25 * 100.0 if ev > 0 else 0.0
        raw_kelly = max(0.0, raw_kelly)
        return {
            "label": label,
            "prob": prob,
            "mkt_odd": mkt_odd,
            "ev": ev,
            "ev_pct": ev_pct,
            "raw_kelly": raw_kelly,
            "kelly": min(KELLY_CAP, raw_kelly),
            "is_capped": raw_kelly > KELLY_CAP,
        }

    ev1 = check_ev("MS 1", p_home_win, odd_ms1)
    ev0 = check_ev("MS 0", p_draw, odd_ms0)
    ev2 = check_ev("MS 2", p_away_win, odd_ms2)
    ev_over = check_ev(f"{gl_str} ÜST", m1_sel_over, odd_over)
    ev_under = check_ev(f"{gl_str} ALT", m1_sel_under, odd_under)
    ev_list = [x for x in (ev1, ev0, ev2, ev_over, ev_under) if x is not None]

    p_ah_hm05 = sum(s["prob"] for s in score_matrix if (s["home"] - s["away"]) >= 1)
    p_ah_am05 = sum(s["prob"] for s in score_matrix if (s["home"] - s["away"]) <= -1)
    p_ah_ap05 = sum(s["prob"] for s in score_matrix if (s["home"] - s["away"]) <= 0)

    if p_ah_hm05 >= 0.55:
        best_ah_prob = p_ah_hm05
        best_ah = f"{home_team} -0.5 AH (%{round(p_ah_hm05 * 100)})"
    elif p_ah_am05 >= 0.52:
        best_ah_prob = p_ah_am05
        best_ah = f"{away_team} -0.5 AH (%{round(p_ah_am05 * 100)})"
    else:
        best_ah_prob = p_ah_ap05
        best_ah = f"{away_team} +0.5 AH (%{round(p_ah_ap05 * 100)})"

    h_xg_val = g_home_xg if has_goaloo else (home_stats["avg_scored"] if home_stats else 1.40)
    h_xga_val = g_home_xga if has_goaloo else (home_stats["avg_conceded"] if home_stats else 1.15)
    a_xg_val = g_away_xg if has_goaloo else (away_stats["avg_scored"] if away_stats else 1.20)
    a_xga_val = g_away_xga if has_goaloo else (away_stats["avg_conceded"] if away_stats else 1.25)

    raw_ev_gol = (h_xg_val + a_xga_val) / 2.0
    raw_dep_gol = (a_xg_val + h_xga_val) / 2.0
    adj_ev_gol = max(0.30, raw_ev_gol * (1.0 - h_inj["att_pen"] * 0.85) * home_gap_drag * home_boost_mult * caution_factor)
    adj_dep_gol = max(0.25, raw_dep_gol * (1.0 - a_inj["att_pen"] * 0.85) * away_gap_drag * away_boost_mult * caution_factor)
    beklenen_gol = adj_ev_gol + adj_dep_gol
    raw_beklenen_gol = raw_ev_gol + raw_dep_gol

    f_state_h = home_stats["ewma_form"] if home_stats else min(95, max(30, round(50 + (h_xg_val - h_xga_val) * 20)))
    f_attack_h = min(98, max(20, round((45 + h_xg_val * 24) * (1.0 - h_inj["att_pen"] * 0.5) * home_gap_drag * min(1.20, home_boost_mult * caution_factor))))
    f_def_h = min(98, max(12, round((92 - h_xga_val * 26) * (1.0 - (h_inj["def_pen"] * 0.85 + h_inj["gk_pen"] * 0.5)))))

    f_state_a = away_stats["ewma_form"] if away_stats else min(95, max(30, round(50 + (a_xg_val - a_xga_val) * 20)))
    f_attack_a = min(98, max(20, round((45 + a_xg_val * 24) * (1.0 - a_inj["att_pen"] * 0.5) * away_gap_drag * min(1.20, away_boost_mult * caution_factor))))
    f_def_a = min(98, max(12, round((92 - a_xga_val * 26) * (1.0 - (a_inj["def_pen"] * 0.85 + a_inj["gk_pen"] * 0.5)))))

    h_power = f_state_h * 0.40 + f_attack_h * 0.30 + f_def_h * 0.30
    a_power = f_state_a * 0.40 + f_attack_a * 0.30 + f_def_a * 0.30
    m12_taraf = "MS 1" if h_power > a_power + 6 else ("MS 2" if a_power > h_power + 6 else "MS 0 (Beraberlik)")

    m5_sel_over_pct = round(poisson_over_total_prob(beklenen_gol, goal_line) * 100)
    m12_goal_res = f"{gl_str} ÜST" if m5_sel_over_pct >= 50 else f"{gl_str} ALT"
    m12_btts_res = "KG VAR" if (adj_ev_gol >= 0.95 and adj_dep_gol >= 0.85) else "KG YOK"

    form_gap = abs(f_state_h - f_state_a)
    def_inj_imp = (h_inj["def_starter_count"] + a_inj["def_starter_count"]) * 4.5 + (5 if h_inj["def_collapse"] else 0) + (5 if a_inj["def_collapse"] else 0)
    bb_imp = (6 if h_backbone_collapse else 0) + (6 if a_backbone_collapse else 0)
    gk_imp = (h_inj["gk_starter_count"] + a_inj["gk_starter_count"]) * 1.5
    other_imp = (h_inj["att_mid_starter_count"] + a_inj["att_mid_starter_count"]) * 1.2

    raw_w1 = (38 if not m2_has_data else 30) + (8 if not has_goaloo else 0)
    raw_w2 = 0 if valid_rows == 0 else (12 if valid_rows < 10 else (19 if valid_rows < 20 else (27 if valid_rows >= 35 else 23)))
    raw_w3 = 10 + min(20, def_inj_imp + bb_imp + gk_imp + other_imp) + (4 if form_gap >= 25 else (2 if form_gap >= 15 else 0))
    raw_w4 = 12 if (len(ev_list) > 0 or best_ah_prob >= 0.62) else 9
    raw_w5 = 5 if not has_goaloo else (24 if valid_rows < 10 else 20)

    dyn_w = normalize_weights({"w1": raw_w1, "w2": raw_w2, "w3": raw_w3, "w4": raw_w4, "w5": raw_w5})

    m3_goal_sig = m1_sel_over_pct
    if single_home_collapse or single_away_collapse:
        m3_goal_sig = min(90, m1_sel_over_pct + 8)
    elif single_home_backbone or single_away_backbone:
        m3_goal_sig = min(88, m1_sel_over_pct + 5)
    elif both_def_collapse:
        m3_goal_sig = max(20, m1_sel_over_pct - 4)

    final_sel_over_pct = round(
        (
            dyn_w["w1"] * m1_sel_over_pct
            + dyn_w["w2"] * m2_sel_over_pct
            + dyn_w["w3"] * m3_goal_sig
            + dyn_w["w4"] * m1_sel_over_pct
            + dyn_w["w5"] * m5_sel_over_pct
        )
        / 100.0
    )
    final_goal_pick = f"{gl_str} ÜST" if final_sel_over_pct >= 50 else f"{gl_str} ALT"
    final_goal_conf = final_sel_over_pct if final_sel_over_pct >= 50 else (100 - final_sel_over_pct)
    goal_agree = (m1_sel_over_pct >= 50 and m2_sel_over_pct >= 50) or (m1_sel_over_pct < 50 and m2_sel_over_pct < 50)

    picked_taraf_ev = ev1 if m1_taraf_pick == "MS 1" else (ev2 if m1_taraf_pick == "MS 2" else ev0)
    if picked_taraf_ev:
        kelly_taraf = picked_taraf_ev["kelly"]
    else:
        kelly_taraf = min(KELLY_CAP, (m1_taraf_conf - 48) * 0.18) if m1_taraf_conf > 52 else 0.0

    goal_pick_is_over = final_goal_pick == f"{gl_str} ÜST"
    target_goal_ev = ev_over if goal_pick_is_over else ev_under

    if final_goal_conf < 55:
        goal_kelly_cap = 0.0
    elif final_goal_conf < 60 or not goal_agree:
        goal_kelly_cap = 1.5
    else:
        goal_kelly_cap = KELLY_CAP

    if target_goal_ev:
        kelly_goal = min(goal_kelly_cap, target_goal_ev["raw_kelly"])
    elif not ev_over and not ev_under:
        raw_g = min(4.5, (final_goal_conf - 50) * 0.18) if final_goal_conf >= 55 else 0.0
        kelly_goal = min(goal_kelly_cap, raw_g)
    else:
        kelly_goal = 0.0

    total_kelly = kelly_taraf + kelly_goal

    btts_w1 = (dyn_w["w1"] + dyn_w["w3"] + dyn_w["w5"]) if m2_has_data else 100
    btts_w2 = (dyn_w["w2"] + dyn_w["w4"]) if m2_has_data else 0
    final_btts_pct = round((m1_btts_pct * btts_w1 + m2_btts_pct * btts_w2) / (btts_w1 + btts_w2))
    final_btts_pick = "KG VAR" if final_btts_pct >= 50 else "KG YOK"
    final_btts_conf = final_btts_pct if final_btts_pct >= 50 else (100 - final_btts_pct)
    btts_agree = (m1_btts_pct >= 50 and m2_btts_pct >= 50) or (m1_btts_pct < 50 and m2_btts_pct < 50)

    final_ht05_pct = round((m1_ht05_pct * btts_w1 + m2_ht05_pct * btts_w2) / (btts_w1 + btts_w2))
    final_ht05_pick = "İY 0.5 ÜST" if final_ht05_pct >= 50 else "İY 0.5 ALT"
    final_ht05_conf = final_ht05_pct if final_ht05_pct >= 50 else (100 - final_ht05_pct)

    final_ht1 = round((m1_ht1_pct * btts_w1 + m2_ht1_pct * btts_w2) / (btts_w1 + btts_w2))
    final_htx = round((m1_htx_pct * btts_w1 + m2_htx_pct * btts_w2) / (btts_w1 + btts_w2))
    final_ht2 = max(0, 100 - final_ht1 - final_htx)
    final_ht_pick = "İY 1" if (final_ht1 >= final_htx and final_ht1 >= final_ht2) else (
        "İY 2" if (final_ht2 >= final_htx and final_ht2 > final_ht1) else "İY X"
    )
    final_ht_conf = max(final_ht1, final_htx, final_ht2)

    top_scores_html = "".join(
        f'<div class="score-item"><div class="sc">{s["home"]}-{s["away"]}</div><div class="pr">%{s["prob"]*100:.1f}</div></div>'
        for s in score_matrix[:6]
    )
    st.markdown(
        f"""
        <div class="engine-card" style="border-left-color:#00f3ff;">
            <h4>Motor 1: Dixon-Coles (ρ=-0.13), xG & Pazarlar</h4>
            Ev: <b>{base_home_xg:.2f}</b> | Dep: <b>{base_away_xg:.2f}</b> (Toplam: <b>{base_home_xg + base_away_xg:.2f}</b>)
            <div class="score-grid">{top_scores_html}</div>
            <div style="margin-top:8px;">
                🎯 <b>Taraf:</b> {m1_taraf_pick} (MS1:%{round(p_home_win*100)} | MS0:%{round(p_draw*100)} | MS2:%{round(p_away_win*100)})<br>
                • <b>Barem ({gl_str}):</b> {"ÜST" if m1_sel_over_pct >= 50 else "ALT"} (%{m1_sel_over_pct if m1_sel_over_pct >= 50 else 100-m1_sel_over_pct}) |
                <b>2.5Ü:</b> %{m1_over25_pct} | <b>3.5Ü:</b> %{m1_over35_pct} | <b>KG:</b> {"VAR" if m1_btts_pct >= 50 else "YOK"} (%{m1_btts_pct if m1_btts_pct >= 50 else 100-m1_btts_pct})
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="engine-card" style="border-left-color:#00ff66;">
            <h4>Motor 2: Excel Arşiv & İç/Dış Saha Sonuçları</h4>
            <b>{home_label or home_team}</b> ({len(home_indices)} maç) & <b>{away_label or away_team}</b> ({len(away_indices)} maç) ➔ <b>{valid_rows}</b> gerçek MS skoru<br>
            • <b>{gl_str} Üst:</b> %{m2_sel_over_pct} | <b>2.5 Üst:</b> %{m2_over25_pct} | <b>KG Var:</b> %{m2_btts_pct} | <b>İY 0.5 Üst:</b> %{m2_ht05_pct}
        </div>
        """,
        unsafe_allow_html=True,
    )

    fair_ms1 = f"{1.0 / max(0.02, p_home_win):.2f}"
    fair_ms0 = f"{1.0 / max(0.02, p_draw):.2f}"
    fair_ms2 = f"{1.0 / max(0.02, p_away_win):.2f}"
    fair_over = f"{1.0 / max(0.02, m1_sel_over):.2f}"
    fair_under = f"{1.0 / max(0.02, m1_sel_under):.2f}"

    ev_lines_html = "".join(
        f"• <b>{x['label']}</b> (Oran: {x['mkt_odd']:.2f} | İhtimal: %{x['prob']*100:.1f}): "
        f"<span style='color:{'#00ff66' if x['ev'] > 0 else '#ff3366'}; font-weight:bold;'>"
        f"{'+' if x['ev'] > 0 else ''}%{x['ev_pct']} {'✅ +EV' if x['ev'] > 0 else '❌ -EV'}</span><br>"
        for x in ev_list
    ) or "Oran girilmediği için +EV taraması pasif."

    st.markdown(
        f"""
        <div class="engine-card" style="border-left-color:#ff9900;">
            <h4>Motor 3 & 4: Adil Oranlar & +EV Değer Tespiti</h4>
            <b>Adil Oranlar:</b> MS1: <b>{fair_ms1}</b> | MS0: <b>{fair_ms0}</b> | MS2: <b>{fair_ms2}</b> | {gl_str} Üst: <b>{fair_over}</b> | {gl_str} Alt: <b>{fair_under}</b><br>
            {ev_lines_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="engine-card" style="border-left-color:#a855f7;">
            <h4>Motor 5, 6, 7, 8, 9 & 12: Kadro, Handikap & Goaloo Özeti</h4>
            🏥 <b>{home_team}:</b> {h_inj['note']} | EWMA: %{f_state_h}<br>
            🏥 <b>{away_team}:</b> {a_inj['note']} | EWMA: %{f_state_a}<br>
            ⚖️ <b>Asya Handikap:</b> {best_ah} | <b>Goaloo Düzeltilmiş Gol:</b> {beklenen_gol:.2f} (Ham: {raw_beklenen_gol:.2f}) | <b>M12:</b> {m12_taraf} / {m12_goal_res} / {m12_btts_res}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if goal_agree and kelly_goal > 0:
        goal_badge = '<span class="seal-badge seal-triple">👑 M1+M2+KELLY ONAMLI</span>'
    elif goal_agree and kelly_goal <= 0:
        goal_badge = '<span class="seal-badge seal-diff">⚠️ M1+M2 UYUMLU (PAS)</span>'
    elif (not goal_agree) and kelly_goal > 0:
        goal_badge = '<span class="seal-badge seal-ok">⚖️ KARMA SENTEZ (SINIRLI +EV)</span>'
    else:
        goal_badge = '<span class="seal-badge seal-pass">⛔ KARMA SENTEZ (PAS GEÇ)</span>'

    btts_badge = (
        '<span class="seal-badge seal-triple">👑 M1+M2 TAM UYUMLU</span>'
        if btts_agree
        else '<span class="seal-badge seal-diff">⚖️ KARMA SENTEZ</span>'
    )

    alert_blocks = ""
    if single_home_collapse:
        alert_blocks += f'<div class="alert-def">🚨 <b>SAVUNMA ÇÖKÜŞÜ AVANTAJI:</b> {home_team} savunmasında {h_inj["def_starter_count"]} ilk 11 eksiği var ➔ <b>{away_team}</b> hücumuna <b>+%{away_boost_pct} xG avantajı</b> işlendi.</div>'
    elif single_away_collapse:
        alert_blocks += f'<div class="alert-def">🚨 <b>SAVUNMA ÇÖKÜŞÜ AVANTAJI:</b> {away_team} savunmasında {a_inj["def_starter_count"]} ilk 11 eksiği var ➔ <b>{home_team}</b> hücumuna <b>+%{home_boost_pct} xG avantajı</b> işlendi.</div>'
    elif single_home_backbone:
        alert_blocks += f'<div class="alert-backbone">⚡ <b>OMURGA ÇÖKÜŞÜ AVANTAJI:</b> {home_team} kadrosunda {h_inj["starter_count"]} kritik ilk 11 eksiği var ➔ <b>{away_team}</b> hücumuna <b>+%{away_boost_pct} xG avantajı</b> işlendi.</div>'
    elif single_away_backbone:
        alert_blocks += f'<div class="alert-backbone">⚡ <b>OMURGA ÇÖKÜŞÜ AVANTAJI:</b> {away_team} kadrosunda {a_inj["starter_count"]} kritik ilk 11 eksiği var ➔ <b>{home_team}</b> hücumuna <b>+%{home_boost_pct} xG avantajı</b> işlendi.</div>'
    elif both_def_collapse:
        alert_blocks += '<div class="alert-caution">⚠️ <b>ÇİFT SAVUNMA ÇÖKÜŞÜ (TEMKİNLİ OYUN FRENİ):</b> Her iki takımda da 2+ savunma eksiği var ➔ Karşılıklı xG şişirmesi kısıldı.</div>'

    active_labels = set()
    if kelly_taraf > 0:
        active_labels.add(m1_taraf_pick)
    if kelly_goal > 0:
        active_labels.add(final_goal_pick)

    radar_candidates = sorted(
        [x for x in ev_list if x["ev"] >= 0.05 and x["label"] not in active_labels],
        key=lambda x: x["ev"],
        reverse=True,
    )
    if radar_candidates and (kelly_taraf == 0 or kelly_goal == 0):
        top_r = radar_candidates[0]
        radar_k = min(2.5, top_r["kelly"])
        alert_blocks += (
            f'<div class="alert-radar">💎 <b>SÜRPRİZ / DEĞER (+EV) RADARI:</b> Ana tercihler pas geçilirken Motor 4, '
            f'<b>{top_r["label"]}</b> (Oran: <b>{top_r["mkt_odd"]:.2f}</b> | İhtimal: %{top_r["prob"]*100:.1f}) '
            f'seçeneğinde <b>+%{top_r["ev_pct"]} +EV</b> tespit etti (Sürpriz Kasa: <b>%{radar_k:.1f}</b>).</div>'
        )

    true_conf = min(96, round((m1_taraf_conf + final_goal_conf + final_btts_conf) / 3))
    taraf_k_str = f"<b>Kelly Kasa: %{kelly_taraf:.1f}</b>" if kelly_taraf > 0 else '<span style="color:#fbbf24;">Kelly Kasa: %0.0 (Pas Geç)</span>'
    goal_k_str = f"<b>Kelly Kasa: %{kelly_goal:.1f}</b>" if kelly_goal > 0 else '<span style="color:#fbbf24;">Kelly Kasa: %0.0 (Pas Geç)</span>'
    total_k_str = f"%{total_kelly:.1f}" if total_kelly > 0 else "%0.0 (PAS GEÇ - DEĞER ORANI YOK)"

    st.markdown(
        f"""
        <div class="consensus-box">
            <div class="consensus-title">👑 {home_team.upper()} - {away_team.upper()} 👑<br>
            <span style="font-size:11px; color:#fff; font-weight:normal;">ÜÇLÜ SENTEZ MÜHRÜ (M1 + M2 + KELLY // BAREM {gl_str})</span></div>
            📌 <b>1. Taraf Mührü:</b> {m1_taraf_pick} (Güven: %{m1_taraf_conf}) ➔ {taraf_k_str}<br>
            ⚽ <b>2. Gol Mührü:</b> {final_goal_pick} (Net Güven: %{final_goal_conf}) ➔ {goal_k_str} {goal_badge}<br>
            🔥 <b>3. KG Mührü:</b> {final_btts_pick} (Net Güven: %{final_btts_conf}) {btts_badge}<br>
            ⏱️ <b>4. İlk Yarı Gol Mührü:</b> {final_ht05_pick} (Net Güven: %{final_ht05_conf})<br>
            ⏳ <b>5. İlk Yarı Taraf Mührü:</b> {final_ht_pick} (Net Güven: %{final_ht_conf})<br>
            🏆 <b>6. Nihai Skor Çifti:</b> {score_matrix[0]['home']}-{score_matrix[0]['away']} veya {score_matrix[1]['home']}-{score_matrix[1]['away']}
            {alert_blocks}
            <div class="seal-footer">
                🔒 ÜÇLÜ KANTİTATİF GÜVEN MÜHRÜ: %{true_conf}<br>
                💼 ÖNERİLEN TOPLAM OPTİMAL KASA RİSKİ (KELLY): {total_k_str}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
