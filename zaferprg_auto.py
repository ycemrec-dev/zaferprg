<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zaferopta Quant Pro V36.1</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <style>
        :root {
            --bg-color: #05080f;
            --card-bg: #0f172a;
            --accent-cyan: #00f3ff;
            --accent-green: #00ff66;
            --accent-orange: #ff9900;
            --accent-red: #ff3366;
            --accent-purple: #a855f7;
            --accent-yellow: #eab308;
            --accent-blue: #3b82f6;
            --accent-pink: #ec4899;
            --accent-teal: #14b8a6;
            --accent-gold: #ffd700;
            --accent-rose: #f43f5e;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: #1e293b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); padding: 12px; }
        .container { max-width: 650px; margin: 0 auto; }
        
        .header {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border: 1px solid var(--accent-gold);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
        }
        .header h1 { color: var(--accent-gold); font-size: 20px; letter-spacing: 1.5px; margin-bottom: 4px; }
        .header p { color: var(--accent-cyan); font-size: 11px; text-transform: uppercase; font-weight: bold; }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .card label { display: block; font-size: 12px; color: var(--accent-cyan); margin-bottom: 6px; font-weight: 600; text-transform: uppercase; }
        .hint-txt { font-size: 10px; color: var(--text-muted); margin-top: -4px; margin-bottom: 8px; line-height: 1.35; }
        
        input[type="text"], input[type="password"], input[type="file"], input[type="number"], select {
            width: 100%;
            padding: 11px;
            background-color: #080e1a;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            font-size: 14px;
            margin-bottom: 8px;
        }
        input[type="file"] { padding: 7px; cursor: pointer; }
        select {
            border-color: var(--accent-cyan);
            color: var(--accent-gold);
            font-weight: bold;
            text-align: center;
            cursor: pointer;
        }
        .status-msg { font-size: 12px; font-weight: bold; margin-bottom: 8px; line-height: 1.4; }
        
        .api-box {
            background: rgba(168, 85, 247, 0.07);
            border: 1px dashed rgba(168, 85, 247, 0.45);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .api-box label { color: var(--accent-purple); font-size: 11px; margin-bottom: 6px; text-align: center; font-weight: bold; }
        .btn-api {
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #a855f7, #6366f1);
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            margin-bottom: 6px;
            box-shadow: 0 3px 12px rgba(168, 85, 247, 0.3);
        }
        .api-status { font-size: 11px; text-align: center; color: var(--text-muted); min-height: 16px; line-height: 1.4; }

        .manual-input-box {
            background: rgba(244, 63, 94, 0.05);
            border: 1px dashed rgba(244, 63, 94, 0.4);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .odds-input-box {
            background: rgba(0, 243, 255, 0.04);
            border: 1px dashed rgba(0, 243, 255, 0.35);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .manual-input-box label, .odds-input-box label { font-size: 11px; margin-bottom: 6px; display: block; text-align: center; font-weight: bold; }
        .input-row { display: flex; gap: 6px; margin-bottom: 6px; }
        .input-row input, .input-row select { margin-bottom: 0; padding: 8px 4px; font-size: 12px; text-align: center; flex: 1; }
        .input-row select { flex: 1.25; }

        button.btn-main {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #ffd700, #ff9900);
            color: #000;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.35);
        }
        button:active { transform: scale(0.98); }

        .warn-banner {
            background: rgba(255, 153, 0, 0.12);
            border: 1px solid var(--accent-orange);
            color: var(--accent-orange);
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            margin-bottom: 12px;
            display: none;
            line-height: 1.5;
        }

        .loading { text-align: center; color: var(--accent-gold); font-weight: bold; margin: 15px 0; display: none; font-size: 14px; }
        .results { display: none; }
        
        .engine-box {
            background-color: #0b1120;
            border-left: 4px solid var(--accent-cyan);
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            font-size: 13px;
            line-height: 1.6;
        }
        .engine-box.m1 { border-left-color: var(--accent-cyan); }
        .engine-box.m2 { border-left-color: var(--accent-green); }
        .engine-box.m3 { border-left-color: var(--accent-orange); }
        .engine-box.m4 { border-left-color: var(--accent-red); }
        .engine-box.m5 { border-left-color: var(--accent-purple); }
        .engine-box.m6 { border-left-color: var(--accent-yellow); }
        .engine-box.m7 { border-left-color: var(--accent-blue); }
        .engine-box.m8 { border-left-color: var(--accent-pink); }
        .engine-box.m9 { border-left-color: var(--accent-teal); }
        .engine-box.m10 { border-left-color: var(--accent-gold); }
        .engine-box.m11 { border-left-color: var(--accent-teal); background: linear-gradient(180deg, #0b1120, #041219); border: 1px solid rgba(20, 184, 166, 0.3); }
        .engine-box.m12 { border-left-color: var(--accent-red); background: linear-gradient(90deg, #0b1120, #1a0808); border: 1px solid rgba(255, 51, 102, 0.3); }
        
        .engine-box h3 { font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
        .engine-box.m11 h3 { color: var(--accent-teal); text-align: center; border-bottom: 1px solid rgba(20, 184, 166, 0.3); padding-bottom: 8px; margin-bottom: 10px; }
        .engine-box.m12 h3 { color: var(--accent-red); font-weight: bold; letter-spacing: 0.8px; }

        .opta-table { width: 100%; border-collapse: collapse; font-size: 11px; line-height: 1.4; }
        .opta-table th { background-color: rgba(19, 27, 46, 0.8); padding: 8px 6px; text-align: left; color: var(--accent-teal); border-bottom: 1px solid var(--border-color); font-size: 10px; }
        .opta-table td { padding: 8px 6px; border-bottom: 1px solid rgba(30, 41, 59, 0.6); color: var(--text-main); vertical-align: middle; }
        .opta-table tr:last-child td { border-bottom: none; }
        .opta-badge { background: #064e3b; color: var(--accent-green); padding: 3px 6px; border-radius: 4px; font-weight: bold; border: 1px solid var(--accent-green); display: inline-block; text-align: center; font-size: 10px; }
        .opta-weight { color: var(--accent-gold); font-weight: bold; text-align: center; font-size: 11px; }
        .opta-final-row td { background-color: rgba(0, 255, 102, 0.08); font-weight: bold; border-top: 2px solid var(--accent-green); }
        .opta-final-title { color: var(--accent-green); font-size: 11px; }

        .score-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 8px; }
        .score-item { background: #131b2e; border: 1px solid var(--border-color); padding: 7px; text-align: center; border-radius: 5px; }
        .score-item .sc { font-weight: bold; color: var(--accent-cyan); font-size: 14px; }
        .score-item .pr { font-size: 11px; color: var(--text-muted); }

        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-top: 6px; }
        .stat-card { background: #131b2e; padding: 7px; border-radius: 5px; text-align: center; border: 1px solid var(--border-color); }
        .stat-card .val { font-size: 13px; font-weight: bold; color: var(--accent-green); }
        .stat-card .lbl { font-size: 10px; color: var(--text-muted); text-transform: uppercase; }

        .m1-predictions { margin-top: 10px; background: #080e1a; border: 1px solid var(--border-color); padding: 10px; border-radius: 6px; font-size: 12px; line-height: 1.6; }

        .m12-content { background: #080e1a; border: 1px solid rgba(255, 51, 102, 0.2); padding: 10px; border-radius: 6px; font-size: 12px; line-height: 1.8; }
        .m12-subtit { color: var(--accent-cyan); font-weight: bold; margin-top: 4px; display: block; }

        .consensus {
            background: linear-gradient(135deg, #064e3b, #022c22);
            border: 2px solid var(--accent-gold);
            padding: 16px;
            border-radius: 10px;
            margin-top: 16px;
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.25);
        }
        .consensus h2 { color: var(--accent-gold); font-size: 16px; margin-bottom: 12px; text-align: center; letter-spacing: 0.5px; line-height: 1.4; }
        .consensus-list { font-size: 13px; color: #fff; line-height: 1.9; text-align: left; }
        .seal-badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-left: 4px; vertical-align: middle; }
        .seal-triple { background: var(--accent-gold); color: #000; }
        .seal-ok { background: var(--accent-green); color: #000; }
        .seal-diff { background: var(--accent-orange); color: #000; }
        .seal-pass { background: var(--accent-red); color: #fff; }
        .pas-text { color: #fbbf24; font-weight: bold; }
        .def-alert {
            margin-top: 10px;
            padding: 8px;
            border-radius: 6px;
            background: rgba(0, 243, 255, 0.12);
            border: 1px solid var(--accent-cyan);
            color: #e0f2fe;
            font-size: 12px;
            line-height: 1.45;
        }
        .backbone-alert {
            margin-top: 10px;
            padding: 8px;
            border-radius: 6px;
            background: rgba(168, 85, 247, 0.16);
            border: 1px solid var(--accent-purple);
            color: #f3e8ff;
            font-size: 12px;
            line-height: 1.45;
        }
        .caution-alert {
            margin-top: 10px;
            padding: 8px;
            border-radius: 6px;
            background: rgba(255, 153, 0, 0.16);
            border: 1px solid var(--accent-orange);
            color: #fef3c7;
            font-size: 12px;
            line-height: 1.45;
        }
        .radar-alert {
            margin-top: 10px;
            padding: 9px;
            border-radius: 6px;
            background: rgba(255, 215, 0, 0.15);
            border: 1px solid var(--accent-gold);
            color: #fef08a;
            font-size: 12px;
            line-height: 1.5;
        }
        .seal-footer { margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255, 215, 0, 0.35); text-align: center; font-size: 13px; color: var(--accent-gold); font-weight: bold; line-height: 1.6; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>ZAFEROPTA QUANT PRO</h1>
        <p>V36.1 // Omurga Çöküşü + Kilit Oyun Kurucu + +EV Radarı</p>
    </div>

    <div class="card">
        <label>1. 75 SÜTUNLU ARŞİV EXCEL (.XLSX)</label>
        <input type="file" id="excelFile" accept=".xlsx, .xls">
        <div id="fileStatus" class="status-msg" style="color: var(--accent-orange);">⚠️ Arşiv dosyası bekleniyor...</div>
        
        <label>2. MAÇ ANALİZİ (EV SAHİBİ - DEPLASMAN)</label>
        <input type="text" id="matchInput" placeholder="Örn: Chelsea - Leeds United">

        <!-- CANLI GEMINI API SAKAT / CEZALI TARAMA -->
        <div class="api-box">
            <label>🤖 CANLI SAKAT & CEZALI TARAMA (GEMINI API)</label>
            <input type="password" id="geminiApiKey" placeholder="Google AI Studio API Anahtarını yapıştır">
            <button type="button" class="btn-api" onclick="fetchInjuriesViaAPI()">🔍 SAKAT / CEZALILARI İNTERNETTEN TARA</button>
            <div id="apiStatus" class="api-status">Anahtar bir kez girildiğinde cihazda saklanır.</div>
        </div>

        <label>3. EV SAHİBİ SAKAT / CEZALI OYUNCULAR</label>
        <input type="text" id="homeInjuries" placeholder="Örn: Alan Patrick kilit orta saha, Bernabei bek, Rochet kaleci">

        <label>4. DEPLASMAN SAKAT / CEZALI OYUNCULAR</label>
        <input type="text" id="awayInjuries" placeholder="Örn: Matty Cash bek, Matteo Ruggeri bek">
        <div class="hint-txt">💡 2+ stoper/bek <b>Savunma Çöküşü</b>; 1 savunma + 1 kaleci veya 3+ ilk 11 farkı <b>Omurga Çöküşü</b> tetikler. Ana tercih Pas Geç olursa <b>+EV Radarı</b> sürpriz değeri gösterir.</div>

        <!-- GOALOO XG / XGA GİRİŞ KUTULARI -->
        <div class="manual-input-box">
            <label style="color: var(--accent-rose);">5. GOALOO XG & XGA MANUEL GİRİŞİ (GOL PAZARLARI & POISSON)</label>
            <div class="input-row">
                <input type="number" step="0.01" id="gHomeXg" placeholder="Ev Attack xG">
                <input type="number" step="0.01" id="gHomeXga" placeholder="Ev Defence xGA">
            </div>
            <div class="input-row">
                <input type="number" step="0.01" id="gAwayXg" placeholder="Dep Attack xG">
                <input type="number" step="0.01" id="gAwayXga" placeholder="Dep Defence xGA">
            </div>
        </div>

        <!-- PİYASA ORANLARI VE ÇOKLU GOL BAREMİ -->
        <div class="odds-input-box">
            <label style="color: var(--accent-cyan);">6. GÜNCEL PİYASA ORANLARI & GOL BAREMİ (+EV & KELLY)</label>
            <div class="input-row">
                <input type="number" step="0.01" id="oddMs1" placeholder="MS 1">
                <input type="number" step="0.01" id="oddMs0" placeholder="MS 0">
                <input type="number" step="0.01" id="oddMs2" placeholder="MS 2">
            </div>
            <div class="input-row">
                <select id="goalLineSelect" onchange="updateGoalOddPlaceholder()">
                    <option value="2.5" selected>Barem: 2.5</option>
                    <option value="3.5">Barem: 3.5</option>
                    <option value="4.5">Barem: 4.5</option>
                    <option value="1.5">Barem: 1.5</option>
                </select>
                <input type="number" step="0.01" id="oddGoalOver" placeholder="2.5 ÜST Oranı">
                <input type="number" step="0.01" id="oddGoalUnder" placeholder="2.5 ALT (Ops.)">
            </div>
        </div>
        
        <button type="button" class="btn-main" onclick="runAllEngines()">TÜM MOTORLARI VE MÜHRÜ ÇALIŞTIR</button>
    </div>

    <div class="loading" id="loadingText">12 Aktif Motor V36.1 omurga & +EV radarıyla hesaplanıyor...</div>
    <div class="warn-banner" id="warnBanner"></div>

    <div class="results" id="resultsArea">
        <div class="engine-box m1">
            <h3>Motor 1: Gerçek Dixon-Coles (ρ=-0.13), xG & Pazarlar</h3>
            <p id="m1Text">-</p>
            <div class="score-grid" id="scoreGrid"></div>
            <div class="m1-predictions" id="m1PredictionsText">-</div>
        </div>

        <div class="engine-box m2">
            <h3>Motor 2: Excel Arşiv & İç/Dış Saha Sonuçları</h3>
            <p id="m2Text">-</p>
            <div class="stats-grid" id="statsGrid"></div>
            <div class="m1-predictions" id="m2HtText" style="margin-top: 8px; text-align: center;">-</div>
        </div>

        <div class="engine-box m3">
            <h3 style="color: var(--accent-orange);">Motor 3: Adil Oran vs Piyasa Sapması</h3>
            <p id="m3Text">-</p>
        </div>

        <div class="engine-box m4">
            <h3 style="color: var(--accent-red);">Motor 4: +EV Değer Oran (Value Bet) Tespiti</h3>
            <p id="m4Text">-</p>
        </div>

        <div class="engine-box m5">
            <h3 style="color: var(--accent-purple);">Motor 5: Savunma & Omurga Kadro Analizi + EWMA</h3>
            <p id="m5Text">-</p>
        </div>

        <div class="engine-box m6">
            <h3 style="color: var(--accent-yellow);">Motor 6: Asya Handikap Olasılık Matrisi</h3>
            <p id="m6Text">-</p>
        </div>

        <div class="engine-box m7">
            <h3 style="color: var(--accent-blue);">Motor 7: Maç Temposu & Disiplin/Kart Riski</h3>
            <p id="m7Text">-</p>
        </div>

        <div class="engine-box m8">
            <h3 style="color: var(--accent-pink);">Motor 8: Ev/Deplasman Saha Üstünlüğü & İstikrar</h3>
            <p id="m8Text">-</p>
        </div>

        <div class="engine-box m9">
            <h3 style="color: var(--accent-teal);">Motor 9: Poisson Canlı Bahis (In-Play) Senaryoları</h3>
            <p id="m9Text">-</p>
        </div>

        <div class="engine-box m10">
            <h3 style="color: var(--accent-gold);">Motor 10: Kelly Criterion Kasa & Risk Yönetimi</h3>
            <p id="m10Text">-</p>
        </div>

        <div class="engine-box m11">
            <h3>Motor 11: Dinamik 5 Katmanlı Opta Sentez Matrisi</h3>
            <table class="opta-table">
                <thead>
                    <tr>
                        <th style="width: 28%;">Modül & Katman</th>
                        <th style="width: 44%;">Gerçek Saha / Arşiv Bulgusu</th>
                        <th style="width: 18%; text-align: center;">Yönelim</th>
                        <th style="width: 10%; text-align: center;">Dinamik Ağırlık</th>
                    </tr>
                </thead>
                <tbody id="optaTableBody"></tbody>
            </table>
        </div>

        <div class="engine-box m12">
            <h3>MOTOR 12: GOALOO ANALİZİ (FORM, HÜCUM, SAVUNMA)</h3>
            <div class="m12-content" id="m12Text">-</div>
        </div>

        <div class="consensus">
            <h2 id="consensusTitle">👑 ÜÇLÜ SENTEZ MÜHRÜ (M1 + M2 + KELLY)</h2>
            <div class="consensus-list" id="consensusText">-</div>
            <div class="seal-footer" id="sealFooter">-</div>
        </div>
    </div>
</div>

<script>
let excelData = null;
let colMap = { home: '', away: '', msScore: '', htScore: '', homeGoal: '', awayGoal: '' };

function updateGoalOddPlaceholder() {
    let gl = document.getElementById('goalLineSelect').value;
    document.getElementById('oddGoalOver').placeholder = `${gl} ÜST Oranı`;
    document.getElementById('oddGoalUnder').placeholder = `${gl} ALT (Ops.)`;
}

window.addEventListener('DOMContentLoaded', () => {
    updateGoalOddPlaceholder();
    try {
        let savedKey = localStorage.getItem('zaferopta_gemini_key');
        if (savedKey) {
            document.getElementById('geminiApiKey').value = savedKey;
            document.getElementById('apiStatus').style.color = 'var(--accent-green)';
            document.getElementById('apiStatus').innerText = '✔ Kayıtlı API anahtarı hazır.';
        }
    } catch (e) {}
});

document.getElementById('geminiApiKey').addEventListener('change', function() {
    try { localStorage.setItem('zaferopta_gemini_key', this.value.trim()); } catch (e) {}
});

function normText(str) {
    if (str === undefined || str === null) return '';
    return str.toString()
        .replace(/İ/g, 'i').replace(/I/g, 'i').replace(/ı/g, 'i')
        .replace(/Ş/g, 's').replace(/ş/g, 's')
        .replace(/Ğ/g, 'g').replace(/ğ/g, 'g')
        .replace(/Ü/g, 'u').replace(/ü/g, 'u')
        .replace(/Ö/g, 'o').replace(/ö/g, 'o')
        .replace(/Ç/g, 'c').replace(/ç/g, 'c')
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

function stripGenericWords(normStr) {
    const stop = new Set(['fc', 'fk', 'sk', 'sc', 'cf', 'ac', 'as', 'afc', 'bc', 'wba', 'club', 'clube', 'sport', 'spor', 'kulubu', 'calcio', 'olympique', 'de']);
    return normStr.split(' ').filter(t => t.length > 1 && !stop.has(t)).join(' ').trim();
}

function matchTeamInCell(cellNorm, qNorm, qCore, strictOnly) {
    if (!cellNorm || !qNorm) return false;
    if (cellNorm === qNorm || cellNorm.includes(qNorm)) return true;
    if (qNorm.includes(cellNorm) && cellNorm.length >= 4) return true;
    if (strictOnly) return false;
    let cellCore = stripGenericWords(cellNorm);
    if (qCore && cellCore) {
        if (cellCore === qCore || cellCore.includes(qCore)) return true;
        if (qCore.includes(cellCore) && cellCore.length >= 4) return true;
    }
    return false;
}

function parseScore(val) {
    if (val === undefined || val === null) return null;
    let s = val.toString().trim();
    if (!s) return null;
    let m = s.match(/^(\d{1,2})\s*[-:–—]\s*(\d{1,2})$/);
    if (!m) return null;
    let h = parseInt(m[1], 10), a = parseInt(m[2], 10);
    if (isNaN(h) || isNaN(a) || h > 15 || a > 15) return null;
    return { h, a };
}

function getRowMsScore(r) {
    if (colMap.msScore && r[colMap.msScore] !== undefined) {
        let sc = parseScore(r[colMap.msScore]);
        if (sc) return sc;
    }
    if (colMap.homeGoal && colMap.awayGoal) {
        let h = parseInt(r[colMap.homeGoal], 10);
        let a = parseInt(r[colMap.awayGoal], 10);
        if (!isNaN(h) && !isNaN(a)) return { h, a };
    }
    return null;
}

function getRowHtScore(r) {
    if (colMap.htScore && r[colMap.htScore] !== undefined) {
        return parseScore(r[colMap.htScore]);
    }
    return null;
}

function detectColumns(headers, sampleRows) {
    let normHeaders = headers.map(h => ({ raw: h, norm: normText(h) }));

    let homeCol = (normHeaders.find(x => x.norm === 'ev sahibi' || x.norm.includes('ev sahibi')) ||
                   normHeaders.find(x => x.norm === 'ev' || x.norm === 'home' || x.norm.includes('home team')) || {}).raw || '';

    let awayCol = (normHeaders.find(x => x.norm === 'deplasman' || x.norm.includes('deplasman')) ||
                   normHeaders.find(x => x.norm === 'dep' || x.norm === 'away' || x.norm.includes('away team')) || {}).raw || '';

    let scoreCandidates = [];
    headers.forEach(h => {
        if (!h || h === homeCol || h === awayCol) return;
        let hn = normText(h);
        if (hn.includes('iy ms') || hn === 'iyms' || hn.includes('tarih') || hn.includes('saat')) return;
        let hits = 0, goalSum = 0;
        for (let i = 0; i < Math.min(60, sampleRows.length); i++) {
            let sc = parseScore(sampleRows[i][h]);
            if (sc) {
                hits++;
                goalSum += (sc.h + sc.a);
            }
        }
        if (hits >= 5) {
            scoreCandidates.push({ raw: h, norm: hn, hits, avgGoals: goalSum / hits });
        }
    });

    let htScoreCol = (
        scoreCandidates.find(x => x.norm === 'skor iy' || x.norm === 'iy skor' || x.norm === 'ilk yari skor' || x.norm === 'ht score') ||
        scoreCandidates.find(x => (x.norm.includes('iy') || x.norm.includes('ht') || x.norm.includes('ilk yari')) && !x.norm.includes('ms') && !x.norm.includes('ft')) ||
        normHeaders.find(x => x.norm === 'skor iy' || x.norm === 'iy skor') ||
        {}
    ).raw || '';

    let msScoreCol = (
        scoreCandidates.find(x => x.raw !== htScoreCol && (x.norm === 'skor ms' || x.norm === 'ms skor' || x.norm === 'mac sonu skor' || x.norm === 'ft score')) ||
        scoreCandidates.find(x => x.raw !== htScoreCol && (x.norm.includes('ms') || x.norm.includes('ft')) && !x.norm.includes('iy') && !x.norm.includes('ht')) ||
        scoreCandidates.find(x => x.raw !== htScoreCol && x.norm.includes('skor') && !x.norm.includes('iy') && !x.norm.includes('ht')) ||
        scoreCandidates.filter(x => x.raw !== htScoreCol && !x.norm.includes('iy') && !x.norm.includes('ht')).sort((a, b) => b.avgGoals - a.avgGoals)[0] ||
        normHeaders.find(x => x.norm === 'skor ms' || x.norm === 'ms skor') ||
        {}
    ).raw || '';

    let homeGoalCol = (normHeaders.find(x => x.norm === 'ev gol' || x.norm === 'ms ev' || x.norm === 'ev skor') || {}).raw || '';
    let awayGoalCol = (normHeaders.find(x => x.norm === 'dep gol' || x.norm === 'ms dep' || x.norm === 'dep skor') || {}).raw || '';

    colMap = { home: homeCol, away: awayCol, msScore: msScoreCol, htScore: htScoreCol, homeGoal: homeGoalCol, awayGoal: awayGoalCol };
}

document.getElementById('excelFile').addEventListener('change', function(e) {
    let file = e.target.files[0];
    if (!file) return;
    
    let reader = new FileReader();
    reader.onload = function(e) {
        try {
            let data = new Uint8Array(e.target.result);
            let workbook = XLSX.read(data, {type: 'array'});
            let worksheet = workbook.Sheets[workbook.SheetNames[0]];
            let rawJson = XLSX.utils.sheet_to_json(worksheet, {header: 1, raw: false});
            
            let headerIdx = -1;
            for (let r = 0; r < Math.min(16, rawJson.length); r++) {
                let row = rawJson[r] || [];
                let joined = row.map(c => normText(c)).join('|');
                if (joined.includes('ev sahibi') || (joined.includes('ev') && joined.includes('deplasman')) || (joined.includes('home') && joined.includes('away'))) {
                    headerIdx = r;
                    break;
                }
            }
            if (headerIdx === -1 && rawJson.length > 7) headerIdx = 7;

            if (headerIdx !== -1 && rawJson.length > headerIdx + 1) {
                let headers = rawJson[headerIdx].map((h, i) => (h !== undefined && h !== null && h.toString().trim() !== '') ? h.toString().trim() : `COL_${i}`);
                let rows = rawJson.slice(headerIdx + 1);
                let parsed = rows.map(row => {
                    let obj = {};
                    headers.forEach((h, i) => { obj[h] = row[i] !== undefined ? row[i] : ""; });
                    return obj;
                });

                detectColumns(headers, parsed);

                excelData = parsed.filter(r => (colMap.home && r[colMap.home]) || (colMap.away && r[colMap.away]));
                document.getElementById('fileStatus').style.color = 'var(--accent-green)';
                document.getElementById('fileStatus').innerHTML = `✔ Başarılı! <b>${excelData.length}</b> satırlık arşiv yüklendi.<br><span style="font-size:10px; color:var(--text-muted);">Algılanan Sütunlar ➔ Ev: [${colMap.home || 'YOK'}] | Dep: [${colMap.away || 'YOK'}] | MS: [${colMap.msScore || (colMap.homeGoal ? colMap.homeGoal+'/'+colMap.awayGoal : 'YOK')}] | İY: [${colMap.htScore || 'YOK'}]</span>`;
            } else {
                alert("Excel formatı uygun değil! Başlık satırı bulunamadı.");
            }
        } catch (err) { alert("Excel okuma hatası: " + err.message); }
    };
    reader.readAsArrayBuffer(file);
});

async function callGeminiModel(apiKey, modelName, prompt, useSearch) {
    let bodyObj = { contents: [{ parts: [{ text: prompt }] }] };
    if (useSearch) bodyObj.tools = [{ google_search: {} }];
    return await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${encodeURIComponent(apiKey)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyObj)
    });
}

async function findActiveModel(apiKey, skipList) {
    let resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${encodeURIComponent(apiKey)}`);
    if (!resp.ok) return null;
    let data = await resp.json();
    let models = data.models || [];
    let valid = models
        .filter(m => m.supportedGenerationMethods && m.supportedGenerationMethods.includes('generateContent'))
        .map(m => m.name.replace('models/', ''))
        .filter(name => !skipList.includes(name));
    return valid.find(n => n.includes('3.8-flash')) || valid.find(n => n.includes('flash')) || valid[0] || null;
}

async function fetchInjuriesViaAPI() {
    let apiKey = document.getElementById('geminiApiKey').value.trim();
    let matchName = document.getElementById('matchInput').value.trim();
    let statusEl = document.getElementById('apiStatus');

    if (!apiKey) { statusEl.style.color = 'var(--accent-red)'; statusEl.innerText = '⚠️ Önce API anahtarını gir.'; return; }
    if (!matchName || !matchName.includes('-')) { statusEl.style.color = 'var(--accent-orange)'; statusEl.innerText = '⚠️ 2. kutuya "Ev Sahibi - Deplasman" yaz.'; return; }

    try { localStorage.setItem('zaferopta_gemini_key', apiKey); } catch (e) {}
    statusEl.style.color = 'var(--accent-gold)';
    statusEl.innerText = '⏳ İlk 11 sakat/cezalılar ve yerine girenler taranıyor...';

    let prompt = `${matchName} futbol maçı için her iki takımın bugünkü güncel sakat ve cezalı İLK 11 oyuncularını internetten araştır. Uzun süreli veya yedek oyuncuları yazma. Stoper, bek, kaleci ve kilit oyun kurucu mevkilerini ayrı ve net belirt. Eğer yerine ilk 11'de geçecek yedek oyuncunun güncel SofaScore/WhoScored sezon puanını gerçek kaynakta bulabiliyorsan ve 6.50 altındaysa oyuncunun yanına puanı ekle (örn: Lacroix stoper 6.3); gerçek puan bulamazsan kesinlikle tahmin etme ve sayı yazma. Sadece şu 2 satır formatında kısa cevap ver:\nEV: [eksik oyuncular ve mevkileri, yoksa Yok]\nDEP: [eksik oyuncular ve mevkileri, yoksa Yok]`;

    try {
        let candidates = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.0-flash'];
        let tried = [], resp = null, usedModel = '';

        for (let m of candidates) {
            tried.push(m);
            resp = await callGeminiModel(apiKey, m, prompt, true);
            if (resp.status === 400) resp = await callGeminiModel(apiKey, m, prompt, false);
            if (resp.ok) { usedModel = m; break; }
            if (resp.status !== 404) break;
        }
        if (!resp || resp.status === 404) {
            let detected = await findActiveModel(apiKey, tried);
            if (detected) {
                usedModel = detected;
                resp = await callGeminiModel(apiKey, detected, prompt, true);
                if (resp.status === 400) resp = await callGeminiModel(apiKey, detected, prompt, false);
            }
        }
        if (!resp || !resp.ok) {
            if (resp && resp.status === 429) throw new Error("Kota doldu (HTTP 429).");
            throw new Error(resp ? `HTTP ${resp.status}` : 'Bağlantı hatası');
        }

        let data = await resp.json();
        let text = data?.candidates?.[0]?.content?.parts?.map(p => p.text || '').join('\n') || '';
        let evMatch = text.match(/EV:\s*(.+)/i);
        let depMatch = text.match(/DEP:\s*(.+)/i);
        let evText = evMatch ? evMatch[1].replace(/\*/g, '').trim() : "Bilgi bulunamadı";
        let depText = depMatch ? depMatch[1].replace(/\*/g, '').trim() : "Bilgi bulunamadı";

        document.getElementById('homeInjuries').value = evText.toLowerCase() === 'yok' ? '' : evText;
        document.getElementById('awayInjuries').value = depText.toLowerCase() === 'yok' ? '' : depText;
        statusEl.style.color = 'var(--accent-green)';
        statusEl.innerText = `✔ Tarama tamamlandı (${usedModel}) ve 3-4. kutulara işlendi!`;
    } catch (err) {
        statusEl.style.color = 'var(--accent-red)';
        statusEl.innerText = '❌ Hata: ' + err.message;
    }
}

function factorial(n) {
    if (n === 0 || n === 1) return 1;
    let res = 1;
    for (let i = 2; i <= n; i++) res *= i;
    return res;
}

function poissonProb(lambda, k) {
    return (Math.exp(-lambda) * Math.pow(lambda, k)) / factorial(k);
}

function dixonColesTau(h, a, lam, mu, rho) {
    if (h === 0 && a === 0) return Math.max(0.25, 1 - lam * mu * rho);
    if (h === 0 && a === 1) return Math.max(0.25, 1 + lam * rho);
    if (h === 1 && a === 0) return Math.max(0.25, 1 + mu * rho);
    if (h === 1 && a === 1) return Math.max(0.25, 1 - rho);
    return 1.0;
}

function poissonOverTotalProb(totalLambda, line) {
    let maxUnder = Math.floor(line);
    let underSum = 0;
    for (let k = 0; k <= maxUnder; k++) underSum += poissonProb(totalLambda, k);
    return Math.max(0.01, Math.min(0.99, 1 - underSum));
}

function parseNum(id) {
    let raw = document.getElementById(id).value;
    if (!raw) return NaN;
    return parseFloat(raw.toString().replace(',', '.'));
}

// V36.1: SAVUNMA, KALECİ VE KİLİT OYUN KURUCU AYRIMI
function analyzeInjuryText(text) {
    if (!text || text.trim().length < 2 || text.trim().toLowerCase() === 'yok') {
        return {
            attPen: 0, defPen: 0, gkPen: 0, count: 0, starterCount: 0, keyCount: 0,
            defStarterCount: 0, gkStarterCount: 0, attMidStarterCount: 0, benchCount: 0,
            defCollapse: false, weakSubs: [],
            note: "Tam kadro (etkili eksik yok)"
        };
    }
    let items = text.split(/,|;| ve |\/|\+/).map(x => x.trim()).filter(x => x.length > 1);
    let attPen = 0, defPen = 0, gkPen = 0, starterCount = 0, keyCount = 0, benchCount = 0;
    let defStarterCount = 0, gkStarterCount = 0, attMidStarterCount = 0;
    let weakSubs = [];

    items.forEach(item => {
        let t = normText(item);
        if (/\byedek\b/.test(t) || /\buzun\b/.test(t) || /\brotasyon\b/.test(t) || /\bgenc\b/.test(t) || /\bbench\b/.test(t) || /\bsub\b/.test(t)) {
            benchCount++;
            return;
        }

        let ratingMatch = item.match(/\b([4-9][.,]\d{1,2})\b/);
        let subMult = 1.0;
        if (ratingMatch) {
            let rVal = parseFloat(ratingMatch[1].replace(',', '.'));
            if (rVal < 6.20) { subMult = 1.35; weakSubs.push(`${item.split(' ')[0]} (${rVal.toFixed(1)})`); }
            else if (rVal < 6.50) { subMult = 1.20; weakSubs.push(`${item.split(' ')[0]} (${rVal.toFixed(1)})`); }
            else if (rVal >= 6.80) { subMult = 0.80; }
        }

        let isKey = /\bkilit\b/.test(t) || /\byildiz\b/.test(t) || /\bkaptan\b/.test(t) || /\bas\b/.test(t) || /\bstar\b/.test(t) || /\bkey\b/.test(t) || t.includes('golcu') || t.includes('oyun kurucu') || t.includes('10 numara');
        let mult = (isKey ? 1.35 : 1.0) * subMult;
        starterCount++;
        if (isKey) keyCount++;

        let isGk = t.includes('kaleci') || /\bgk\b/.test(t);
        let isDef = !isGk && (t.includes('stoper') || t.includes('defans') || t.includes('bek') || t.includes('savunma'));
        let isAtt = !isGk && (t.includes('forvet') || t.includes('santrafor') || t.includes('golcu') || t.includes('kanat') || t.includes('hucum'));
        let isPlaymaker = !isGk && !isDef && (t.includes('oyun kurucu') || t.includes('10 numara') || (t.includes('orta saha') && isKey));
        let isMid = !isGk && !isDef && !isAtt && !isPlaymaker && (t.includes('orta saha') || t.includes('libero') || t.includes('merkez'));

        let bAtt = 0, bDef = 0, bGk = 0;
        if (isGk) {
            gkStarterCount++;
            bGk += 0.05;
        } else if (isDef) {
            defStarterCount++;
            bDef += 0.11;
            bAtt += 0.01;
        } else if (isPlaymaker) {
            attMidStarterCount++;
            bAtt += 0.065; // Kilit oyun kurucu / 10 numara yüksek hücum etkisi
            bDef += 0.035;
        } else if (isAtt) {
            attMidStarterCount++;
            bAtt += 0.05;
            bDef += 0.005;
        } else if (isMid) {
            attMidStarterCount++;
            bAtt += 0.03;
            bDef += 0.035;
        } else {
            attMidStarterCount++;
            bAtt += 0.03;
            bDef += 0.03;
        }

        attPen += bAtt * mult;
        defPen += bDef * mult;
        gkPen += bGk * mult;
    });

    let defCollapse = defStarterCount >= 2;
    if (defCollapse) {
        defPen += 0.12 + Math.max(0, defStarterCount - 2) * 0.06;
    }

    attPen = Math.min(0.28, attPen);
    defPen = Math.min(0.55, defPen);
    gkPen = Math.min(0.12, gkPen);

    let tierSummary = `${starterCount} ilk 11`;
    let roleParts = [];
    if (defStarterCount > 0) roleParts.push(`${defStarterCount} savunma`);
    if (gkStarterCount > 0) roleParts.push(`${gkStarterCount} kaleci`);
    if (roleParts.length > 0) tierSummary += ` (${roleParts.join(', ')})`;
    if (benchCount > 0) tierSummary += `, ${benchCount} yedek/uzun (%0)`;

    let tags = '';
    if (defCollapse) tags += ` <span style="color:var(--accent-red); font-weight:bold;">[🚨 SAVUNMA ÇÖKÜŞÜ]</span>`;
    if (weakSubs.length > 0) tags += ` <span style="color:var(--accent-yellow); font-weight:bold;">[⚠️ Zayıf İkame: ${weakSubs.join(', ')}]</span>`;

    let gkNoteStr = gkPen > 0 ? `, Kaleci -%${Math.round(gkPen*100)}` : '';

    return {
        attPen, defPen, gkPen, count: items.length, starterCount, keyCount,
        defStarterCount, gkStarterCount, attMidStarterCount, benchCount,
        defCollapse, weakSubs,
        note: `${tierSummary} ➔ Savunma Zafiyeti -%${Math.round(defPen*100)}${gkNoteStr}, Hücum/OS -%${Math.round(attPen*100)}${tags}`
    };
}

function normalizeWeights(rawObj) {
    let keys = Object.keys(rawObj);
    let sum = keys.reduce((acc, k) => acc + Math.max(0, rawObj[k]), 0);
    if (sum <= 0) return { w1: 35, w2: 20, w3: 15, w4: 10, w5: 20 };
    let res = {};
    let total = 0;
    keys.forEach(k => {
        res[k] = Math.round((Math.max(0, rawObj[k]) / sum) * 100);
        total += res[k];
    });
    let diff = 100 - total;
    if (diff !== 0) {
        let maxKey = keys.reduce((a, b) => res[a] >= res[b] ? a : b);
        res[maxKey] += diff;
    }
    return res;
}

function findTeamRows(data, teamName) {
    let qNorm = normText(teamName);
    let qCore = stripGenericWords(qNorm);
    if (!data || !data.length || !qNorm) return { rows: [], matchedLabel: '' };

    let rows = data.filter(r => {
        let ev = normText(r[colMap.home]);
        let dep = normText(r[colMap.away]);
        return matchTeamInCell(ev, qNorm, qCore, true) || matchTeamInCell(dep, qNorm, qCore, true);
    });
    let strictMode = true;

    if (rows.length === 0) {
        strictMode = false;
        rows = data.filter(r => {
            let ev = normText(r[colMap.home]);
            let dep = normText(r[colMap.away]);
            return matchTeamInCell(ev, qNorm, qCore, false) || matchTeamInCell(dep, qNorm, qCore, false);
        });
    }

    let matchedLabel = '';
    if (rows.length > 0) {
        let r0 = rows[0];
        let ev = normText(r0[colMap.home]);
        matchedLabel = matchTeamInCell(ev, qNorm, qCore, strictMode) ? r0[colMap.home] : r0[colMap.away];
    }

    return { rows, matchedLabel, strictMode, qNorm, qCore };
}

function calcTeamStats(foundObj) {
    let rows = foundObj.rows;
    if (!rows || rows.length === 0) return null;

    let played = 0, scored = 0, conceded = 0, wins = 0, draws = 0, losses = 0;
    let homePlayed = 0, homeWins = 0, homeScored = 0, homeConceded = 0;
    let awayPlayed = 0, awayWins = 0, awayScored = 0, awayConceded = 0;
    let ewmaPoints = 0, ewmaWeightSum = 0;
    let totalRecent = rows.length;

    rows.forEach((r, idx) => {
        let ev = normText(r[colMap.home]);
        let dep = normText(r[colMap.away]);
        let sc = getRowMsScore(r);
        if (!sc) return;

        let isHome = matchTeamInCell(ev, foundObj.qNorm, foundObj.qCore, foundObj.strictMode);
        let isAway = !isHome && matchTeamInCell(dep, foundObj.qNorm, foundObj.qCore, foundObj.strictMode);
        if (!isHome && !isAway) return;

        let gf = isHome ? sc.h : sc.a;
        let ga = isHome ? sc.a : sc.h;
        played++;
        scored += gf;
        conceded += ga;

        let pts = 0;
        if (gf > ga) { wins++; pts = 3; if (isHome) homeWins++; else awayWins++; }
        else if (gf === ga) { draws++; pts = 1; }
        else { losses++; pts = 0; }

        if (isHome) { homePlayed++; homeScored += gf; homeConceded += ga; }
        else { awayPlayed++; awayScored += gf; awayConceded += ga; }

        let w = Math.pow(0.85, Math.max(0, totalRecent - 1 - idx));
        ewmaPoints += (pts / 3) * w;
        ewmaWeightSum += w;
    });

    if (played === 0) return null;
    return {
        played,
        avgScored: scored / played,
        avgConceded: conceded / played,
        homePlayed,
        homeAvgScored: homePlayed >= 3 ? (homeScored / homePlayed) : (scored / played),
        homeAvgConceded: homePlayed >= 3 ? (homeConceded / homePlayed) : (conceded / played),
        awayPlayed,
        awayAvgScored: awayPlayed >= 3 ? (awayScored / awayPlayed) : (scored / played),
        awayAvgConceded: awayPlayed >= 3 ? (awayConceded / awayPlayed) : (conceded / played),
        winRate: Math.round((wins / played) * 100),
        homeWinRate: homePlayed > 0 ? Math.round((homeWins / homePlayed) * 100) : Math.round((wins / played) * 100),
        awayWinRate: awayPlayed > 0 ? Math.round((awayWins / awayPlayed) * 100) : Math.round((wins / played) * 100),
        ewmaForm: ewmaWeightSum > 0 ? Math.round((ewmaPoints / ewmaWeightSum) * 100) : 50
    };
}

function runAllEngines() {
    let matchName = document.getElementById('matchInput').value.trim();
    if (!matchName || !matchName.includes('-')) {
        alert("Lütfen maç adını araya tire (-) koyarak girin! (Örn: Chelsea - Leeds United)");
        return;
    }

    let inHxG = parseNum('gHomeXg');
    let inHxGA = parseNum('gHomeXga');
    let inAxG = parseNum('gAwayXg');
    let inAxGA = parseNum('gAwayXga');
    let hasGoaloo = !isNaN(inHxG) && !isNaN(inHxGA) && !isNaN(inAxG) && !isNaN(inAxGA);

    if ((!excelData || excelData.length === 0) && !hasGoaloo) {
        alert("Lütfen 1. bölümden Excel arşiv dosyasını yükleyin VEYA 5. bölümden Goaloo xG/xGA verilerini girin!");
        return;
    }

    let goalLine = parseFloat(document.getElementById('goalLineSelect').value) || 2.5;
    let glStr = goalLine.toFixed(1);

    document.getElementById('loadingText').style.display = 'block';
    document.getElementById('resultsArea').style.display = 'none';
    document.getElementById('warnBanner').style.display = 'none';

    setTimeout(() => {
        try {
            let parts = matchName.split('-');
            let homeTeam = parts[0].trim();
            let awayTeam = parts[1].trim();
            let homeTeamUpper = homeTeam.toUpperCase();
            let awayTeamUpper = awayTeam.toUpperCase();

            let homeFound = findTeamRows(excelData, homeTeam);
            let awayFound = findTeamRows(excelData, awayTeam);

            let seen = new Set();
            let combinedRows = [];
            [...homeFound.rows, ...awayFound.rows].forEach(r => {
                if (!seen.has(r)) { seen.add(r); combinedRows.push(r); }
            });

            let homeStats = calcTeamStats(homeFound);
            let awayStats = calcTeamStats(awayFound);
            let scoreReadIssue = (homeFound.rows.length > 0 && !homeStats) || (awayFound.rows.length > 0 && !awayStats);

            if (!homeStats && !awayStats && !hasGoaloo) {
                document.getElementById('loadingText').style.display = 'none';
                document.getElementById('warnBanner').style.display = 'block';
                if (scoreReadIssue) {
                    let sampleVal = colMap.msScore ? (combinedRows[0][colMap.msScore] || 'Boş') : 'Sütun bulunamadı';
                    document.getElementById('warnBanner').innerHTML = `⚠️ Takımlar Excel'de bulundu (<b>${homeFound.rows.length + awayFound.rows.length}</b> satır), ancak <b>MS Skor</b> sütunu okunamadı! (Algılanan sütun: <b>${colMap.msScore || 'YOK'}</b>, Örnek değer: <b>${sampleVal}</b>).`;
                } else {
                    document.getElementById('warnBanner').innerHTML = `⚠️ <b>"${homeTeam}"</b> ve <b>"${awayTeam}"</b> Excel arşivinde bulunamadı ve Goaloo xG verisi girilmedi. Excel'deki takım adını kontrol edin veya 5. bölümden Goaloo xG/xGA değerlerini girin.`;
                }
                return;
            }

            if (!homeStats || !awayStats) {
                document.getElementById('warnBanner').style.display = 'block';
                if (scoreReadIssue) {
                    document.getElementById('warnBanner').innerHTML = `ℹ️ <b>Bilgi:</b> Arşivdeki bazı satırlarda MS Skor okunamadı, eksik kısım Goaloo xG/xGA değerlerinden telafi edildi.`;
                } else {
                    document.getElementById('warnBanner').innerHTML = `ℹ️ <b>Bilgi:</b> ${!homeStats ? homeTeam : ''} ${(!homeStats && !awayStats) ? 've ' : ''}${!awayStats ? awayTeam : ''} Excel arşivinde bulunamadı. Eksik takım verisi girdiğiniz Goaloo xG/xGA değerlerinden telafi edildi.`;
                }
            }

            let hInj = analyzeInjuryText(document.getElementById('homeInjuries').value);
            let aInj = analyzeInjuryText(document.getElementById('awayInjuries').value);

            // İç/Dış Saha Ağırlıklı Excel xG (%65 Saha Özel + %35 Genel)
            let hExcelAtt = homeStats ? (homeStats.homeAvgScored * 0.65 + homeStats.avgScored * 0.35) : null;
            let hExcelDef = homeStats ? (homeStats.homeAvgConceded * 0.65 + homeStats.avgConceded * 0.35) : null;
            let aExcelAtt = awayStats ? (awayStats.awayAvgScored * 0.65 + awayStats.avgScored * 0.35) : null;
            let aExcelDef = awayStats ? (awayStats.awayAvgConceded * 0.65 + awayStats.avgConceded * 0.35) : null;

            let excelHomeXg = (hExcelAtt !== null && aExcelDef !== null) ? ((hExcelAtt + aExcelDef) / 2) * 1.06 : (hExcelAtt !== null ? hExcelAtt : null);
            let excelAwayXg = (aExcelAtt !== null && hExcelDef !== null) ? ((aExcelAtt + hExcelDef) / 2) * 0.94 : (aExcelAtt !== null ? aExcelAtt : null);

            let goalooHomeXg = hasGoaloo ? (inHxG + inAxGA) / 2 : null;
            let goalooAwayXg = hasGoaloo ? (inAxG + inHxGA) / 2 : null;

            let baseHomeXg, baseAwayXg;
            if (excelHomeXg !== null && goalooHomeXg !== null) {
                baseHomeXg = (excelHomeXg * 0.5) + (goalooHomeXg * 0.5);
                baseAwayXg = (excelAwayXg * 0.5) + (goalooAwayXg * 0.5);
            } else if (goalooHomeXg !== null) {
                baseHomeXg = goalooHomeXg;
                baseAwayXg = goalooAwayXg;
            } else {
                baseHomeXg = excelHomeXg !== null ? excelHomeXg : 1.35;
                baseAwayXg = excelAwayXg !== null ? excelAwayXg : 1.05;
            }

            // V36.1: SAVUNMA ÇÖKÜŞÜ + OMURGA ÇÖKÜŞÜ + NET İLK 11 EKSİK FARKI
            let hNetMissing = hInj.starterCount - aInj.starterCount;
            let aNetMissing = aInj.starterCount - hInj.starterCount;

            let hBackboneCollapse = !hInj.defCollapse && (
                (hInj.defStarterCount >= 1 && hInj.gkStarterCount >= 1 && hNetMissing >= 1) ||
                (hInj.starterCount >= 3 && hNetMissing >= 2)
            );
            let aBackboneCollapse = !aInj.defCollapse && (
                (aInj.defStarterCount >= 1 && aInj.gkStarterCount >= 1 && aNetMissing >= 1) ||
                (aInj.starterCount >= 3 && aNetMissing >= 2)
            );

            let singleHomeCollapse = hInj.defCollapse && !aInj.defCollapse;
            let singleAwayCollapse = aInj.defCollapse && !hInj.defCollapse;
            let bothDefCollapse = hInj.defCollapse && aInj.defCollapse;

            let singleHomeBackbone = hBackboneCollapse && !aInj.defCollapse && !aBackboneCollapse;
            let singleAwayBackbone = aBackboneCollapse && !hInj.defCollapse && !hBackboneCollapse;

            let homeDefAdvRate = singleAwayCollapse ? 0.65 : (singleAwayBackbone ? 0.55 : (bothDefCollapse ? 0.25 : 0.32));
            let awayDefAdvRate = singleHomeCollapse ? 0.65 : (singleHomeBackbone ? 0.55 : (bothDefCollapse ? 0.25 : 0.32));
            let cautionFactor = bothDefCollapse ? 0.94 : 1.0;

            let homeGapBoost = (!bothDefCollapse && aNetMissing >= 2) ? (1 + Math.min(0.12, (aNetMissing - 1) * 0.05)) : 1.0;
            let awayGapBoost = (!bothDefCollapse && hNetMissing >= 2) ? (1 + Math.min(0.12, (hNetMissing - 1) * 0.05)) : 1.0;
            let homeGapDrag = (!bothDefCollapse && hNetMissing >= 2) ? (1 - Math.min(0.10, (hNetMissing - 1) * 0.04)) : 1.0;
            let awayGapDrag = (!bothDefCollapse && aNetMissing >= 2) ? (1 - Math.min(0.10, (aNetMissing - 1) * 0.04)) : 1.0;

            let homeAttHealth = Math.max(0.70, 1 - hInj.attPen);
            let awayAttHealth = Math.max(0.70, 1 - aInj.attPen);

            let homeBoostMult = (1 + ((aInj.defPen * homeDefAdvRate) + aInj.gkPen) * homeAttHealth) * homeGapBoost;
            let awayBoostMult = (1 + ((hInj.defPen * awayDefAdvRate) + hInj.gkPen) * awayAttHealth) * awayGapBoost;

            let homeBoostPct = Math.round((homeBoostMult * cautionFactor - 1) * 100);
            let awayBoostPct = Math.round((awayBoostMult * cautionFactor - 1) * 100);

            baseHomeXg = Math.max(0.30, baseHomeXg * (1 - hInj.attPen) * homeGapDrag * homeBoostMult * cautionFactor);
            baseAwayXg = Math.max(0.25, baseAwayXg * (1 - aInj.attPen) * awayGapDrag * awayBoostMult * cautionFactor);

            // 8x8 GERÇEK DIXON-COLES MATRİSİ (rho = -0.13)
            const RHO = -0.13;
            let scoreMatrix = [];
            let totalProb = 0, pHomeWin = 0, pDraw = 0, pAwayWin = 0, m1BttsProb = 0;
            let m1Over15Prob = 0, m1Over25Prob = 0, m1Over35Prob = 0, m1Over45Prob = 0, m1SelectedOverProb = 0;

            for (let h = 0; h <= 8; h++) {
                for (let a = 0; a <= 8; a++) {
                    let tau = dixonColesTau(h, a, baseHomeXg, baseAwayXg, RHO);
                    let p = poissonProb(baseHomeXg, h) * poissonProb(baseAwayXg, a) * tau;
                    scoreMatrix.push({home: h, away: a, prob: p});
                    totalProb += p;
                }
            }

            scoreMatrix.forEach(s => {
                s.prob = s.prob / totalProb;
                let tot = s.home + s.away;
                if (s.home > s.away) pHomeWin += s.prob;
                else if (s.home === s.away) pDraw += s.prob;
                else pAwayWin += s.prob;
                if (tot > 1.5) m1Over15Prob += s.prob;
                if (tot > 2.5) m1Over25Prob += s.prob;
                if (tot > 3.5) m1Over35Prob += s.prob;
                if (tot > 4.5) m1Over45Prob += s.prob;
                if (tot > goalLine) m1SelectedOverProb += s.prob;
                if (s.home > 0 && s.away > 0) m1BttsProb += s.prob;
            });
            scoreMatrix.sort((a, b) => b.prob - a.prob);

            let m1SelectedUnderProb = Math.max(0, 1 - m1SelectedOverProb);
            let m1SelectedOverPct = Math.round(m1SelectedOverProb * 100);
            let m1Over25Pct = Math.round(m1Over25Prob * 100);
            let m1Over35Pct = Math.round(m1Over35Prob * 100);
            let m1Over45Pct = Math.round(m1Over45Prob * 100);

            let htHomeXg = baseHomeXg * 0.44;
            let htAwayXg = baseAwayXg * 0.44;
            let pHt1 = 0, pHtX = 0, pHt2 = 0, htTotalProb = 0, pHtOver05 = 0;
            for (let h = 0; h <= 5; h++) {
                for (let a = 0; a <= 5; a++) {
                    let tauHt = dixonColesTau(h, a, htHomeXg, htAwayXg, -0.10);
                    let p = poissonProb(htHomeXg, h) * poissonProb(htAwayXg, a) * tauHt;
                    htTotalProb += p;
                    if (h > a) pHt1 += p;
                    else if (h === a) pHtX += p;
                    else pHt2 += p;
                    if ((h + a) > 0.5) pHtOver05 += p;
                }
            }
            let m1Ht1Pct = Math.round((pHt1 / htTotalProb) * 100);
            let m1HtXPct = Math.round((pHtX / htTotalProb) * 100);
            let m1Ht2Pct = Math.max(0, 100 - m1Ht1Pct - m1HtXPct);
            let m1HtOver05Pct = Math.round((pHtOver05 / htTotalProb) * 100);
            let m1HtTarafPick = (m1Ht1Pct >= m1HtXPct && m1Ht1Pct >= m1Ht2Pct) ? "İY 1" : ((m1Ht2Pct >= m1HtXPct && m1Ht2Pct > m1Ht1Pct) ? "İY 2" : "İY X");

            let m1BttsPct = Math.round(m1BttsProb * 100);
            let m1TarafPick = (pHomeWin >= pAwayWin && pHomeWin >= pDraw) ? "MS 1" : ((pAwayWin > pHomeWin && pAwayWin >= pDraw) ? "MS 2" : "MS 0");
            let m1TarafProb = Math.max(pHomeWin, pDraw, pAwayWin);
            let m1TarafConf = Math.round(m1TarafProb * 100);

            let m1Note = '';
            if (singleHomeCollapse) m1Note = ` <span style="color:var(--accent-cyan);">(${awayTeam} +%${awayBoostPct} savunma avantajı)</span>`;
            else if (singleAwayCollapse) m1Note = ` <span style="color:var(--accent-cyan);">(${homeTeam} +%${homeBoostPct} savunma avantajı)</span>`;
            else if (singleHomeBackbone) m1Note = ` <span style="color:var(--accent-purple);">(${awayTeam} +%${awayBoostPct} omurga avantajı)</span>`;
            else if (singleAwayBackbone) m1Note = ` <span style="color:var(--accent-purple);">(${homeTeam} +%${homeBoostPct} omurga avantajı)</span>`;
            else if (bothDefCollapse) m1Note = ` <span style="color:var(--accent-orange);">(Çift savunma eksiği: Temkinli oyun freni)</span>`;

            document.getElementById('m1Text').innerHTML = `<b>Dixon-Coles xG:</b> Ev: <b>${baseHomeXg.toFixed(2)}</b> | Dep: <b>${baseAwayXg.toFixed(2)}</b> (Toplam: <b>${(baseHomeXg + baseAwayXg).toFixed(2)}</b>)${m1Note}`;
            let gridHtml = '';
            scoreMatrix.slice(0, 6).forEach(s => { gridHtml += `<div class="score-item"><div class="sc">${s.home}-${s.away}</div><div class="pr">%${(s.prob*100).toFixed(1)}</div></div>`; });
            document.getElementById('scoreGrid').innerHTML = gridHtml;
            document.getElementById('m1PredictionsText').innerHTML = `
                🎯 <b>Taraf Bahsi:</b> ${m1TarafPick} (MS1:%${Math.round(pHomeWin*100)} | MS0:%${Math.round(pDraw*100)} | MS2:%${Math.round(pAwayWin*100)}) <br>
                • <b>İlk Yarı Taraf:</b> ${m1HtTarafPick} (İY1:%${m1Ht1Pct} | İYX:%${m1HtXPct} | İY2:%${m1Ht2Pct}) <br>
                • <b>Seçili Barem (${glStr} Gol):</b> <span style="color:var(--accent-gold); font-weight:bold;">${m1SelectedOverPct >= 50 ? "ÜST" : "ALT"} (%${m1SelectedOverPct >= 50 ? m1SelectedOverPct : 100-m1SelectedOverPct})</span> <br>
                • <b>Tüm Gol Baremleri:</b> 2.5Ü: %${m1Over25Pct} | 3.5Ü: %${m1Over35Pct} | 4.5Ü: %${m1Over45Pct} <br>
                • <b>KG:</b> ${m1BttsPct >= 50 ? "VAR" : "YOK"} (%${m1BttsPct >= 50 ? m1BttsPct : 100-m1BttsPct})
            `;

            // MOTOR 2: ARŞİV HESAPLARI
            let overSelCount = 0, over25Count = 0, over35Count = 0, over45Count = 0, bttsCount = 0, ht05Count = 0, validRows = 0;
            let ht1Count = 0, htXCount = 0, ht2Count = 0, validHtRows = 0;

            combinedRows.forEach(r => {
                let sc = getRowMsScore(r);
                if (sc) {
                    validRows++;
                    let tot = sc.h + sc.a;
                    if (tot > goalLine) overSelCount++;
                    if (tot > 2.5) over25Count++;
                    if (tot > 3.5) over35Count++;
                    if (tot > 4.5) over45Count++;
                    if (sc.h > 0 && sc.a > 0) bttsCount++;
                }
                let scIy = getRowHtScore(r);
                if (scIy) {
                    validHtRows++;
                    if ((scIy.h + scIy.a) > 0.5) ht05Count++;
                    if (scIy.h > scIy.a) ht1Count++;
                    else if (scIy.h === scIy.a) htXCount++;
                    else ht2Count++;
                }
            });

            let m2HasData = validRows > 0;
            let m2SelectedOverPct = m2HasData ? Math.round((overSelCount / validRows) * 100) : m1SelectedOverPct;
            let m2Over25Pct = m2HasData ? Math.round((over25Count / validRows) * 100) : m1Over25Pct;
            let m2Over35Pct = m2HasData ? Math.round((over35Count / validRows) * 100) : m1Over35Pct;
            let m2Over45Pct = m2HasData ? Math.round((over45Count / validRows) * 100) : m1Over45Pct;
            let m2BttsPct = m2HasData ? Math.round((bttsCount / validRows) * 100) : m1BttsPct;
            let m2Ht05Pct = validHtRows > 0 ? Math.round((ht05Count / validHtRows) * 100) : m1HtOver05Pct;
            let m2Ht1Pct = validHtRows > 0 ? Math.round((ht1Count / validHtRows) * 100) : m1Ht1Pct;
            let m2HtXPct = validHtRows > 0 ? Math.round((htXCount / validHtRows) * 100) : m1HtXPct;
            let m2Ht2Pct = validHtRows > 0 ? Math.max(0, 100 - m2Ht1Pct - m2HtXPct) : m1Ht2Pct;
            let m2HtTarafPick = (m2Ht1Pct >= m2HtXPct && m2Ht1Pct >= m2Ht2Pct) ? "İY 1" : ((m2Ht2Pct >= m2HtXPct && m2Ht2Pct > m2Ht1Pct) ? "İY 2" : "İY X");

            if (m2HasData) {
                document.getElementById('m2Text').innerHTML = `Arşivde <b>${homeFound.matchedLabel || homeTeam}</b> (${homeFound.rows.length} maç) ve <b>${awayFound.matchedLabel || awayTeam}</b> (${awayFound.rows.length} maç) için toplam <b>${validRows}</b> gerçek MS skoru işlendi.`;
            } else {
                document.getElementById('m2Text').innerHTML = `⚠️ Arşivde bu takımlara ait okunabilir skor bulunamadı. Arşiv ağırlığı otomatik %0'a çekildi.`;
            }

            document.getElementById('statsGrid').innerHTML = `
                <div class="stat-card"><div class="val">%${m2SelectedOverPct}</div><div class="lbl">${glStr} ÜST İHTİMALİ</div></div>
                <div class="stat-card"><div class="val">%${100-m2SelectedOverPct}</div><div class="lbl">${glStr} ALT İHTİMALİ</div></div>
                <div class="stat-card"><div class="val">%${m2BttsPct}</div><div class="lbl">KG VAR İHTİMALİ</div></div>
                <div class="stat-card"><div class="val">%${m2Ht05Pct}</div><div class="lbl">İLK YARI 0.5 ÜST</div></div>
            `;
            document.getElementById('m2HtText').innerHTML = `
                📊 <b>Arşiv Gol Baremleri:</b> 2.5Ü: %${m2Over25Pct} | 3.5Ü: %${m2Over35Pct} | 4.5Ü: %${m2Over45Pct}<br>
                ⏳ <b>Arşiv İlk Yarı Taraf:</b> ${m2HtTarafPick} (İY1: %${m2Ht1Pct} | İYX: %${m2HtXPct} | İY2: %${m2Ht2Pct})
            `;

            // MOTOR 3 & 4: ADİL ORAN VE +EV
            let fairMs1 = (1 / Math.max(0.02, pHomeWin)).toFixed(2);
            let fairMs0 = (1 / Math.max(0.02, pDraw)).toFixed(2);
            let fairMs2 = (1 / Math.max(0.02, pAwayWin)).toFixed(2);
            let fairSelOver = (1 / Math.max(0.02, m1SelectedOverProb)).toFixed(2);
            let fairSelUnder = (1 / Math.max(0.02, m1SelectedUnderProb)).toFixed(2);
            let fairO25 = (1 / Math.max(0.02, m1Over25Prob)).toFixed(2);
            let fairO35 = (1 / Math.max(0.02, m1Over35Prob)).toFixed(2);
            let fairO45 = (1 / Math.max(0.02, m1Over45Prob)).toFixed(2);

            let odd1 = parseNum('oddMs1');
            let odd0 = parseNum('oddMs0');
            let odd2 = parseNum('oddMs2');
            let oddGoalOver = parseNum('oddGoalOver');
            let oddGoalUnder = parseNum('oddGoalUnder');

            let m3Html = `
                <b>Taraf Adil Oranları:</b> MS1: <b>${fairMs1}</b> | MS0: <b>${fairMs0}</b> | MS2: <b>${fairMs2}</b><br>
                <b>Seçili Barem (${glStr}):</b> ${glStr} Üst: <b style="color:var(--accent-gold);">${fairSelOver}</b> | ${glStr} Alt: <b>${fairSelUnder}</b><br>
                <span style="font-size:11px; color:var(--text-muted);">Referans Adil Oranlar ➔ 2.5Ü: ${fairO25} | 3.5Ü: ${fairO35} | 4.5Ü: ${fairO45}</span><br>
            `;

            let evList = [];
            const KELLY_CAP = 5.0;

            function checkEV(label, prob, mktOdd) {
                if (isNaN(mktOdd) || mktOdd <= 1.01) return null;
                let ev = (prob * mktOdd) - 1;
                let evPct = (ev * 100).toFixed(1);
                let rawKelly = ev > 0 ? (((mktOdd - 1) * prob - (1 - prob)) / (mktOdd - 1)) * 0.25 * 100 : 0;
                rawKelly = Math.max(0, rawKelly);
                let cappedKelly = Math.min(KELLY_CAP, rawKelly);
                return { label, prob, mktOdd, ev, evPct, rawKelly, kelly: cappedKelly, isCapped: rawKelly > KELLY_CAP };
            }

            let ev1 = checkEV("MS 1", pHomeWin, odd1);
            let ev0 = checkEV("MS 0", pDraw, odd0);
            let ev2 = checkEV("MS 2", pAwayWin, odd2);
            let evOver = checkEV(`${glStr} ÜST`, m1SelectedOverProb, oddGoalOver);
            let evUnder = checkEV(`${glStr} ALT`, m1SelectedUnderProb, oddGoalUnder);
            [ev1, ev0, ev2, evOver, evUnder].forEach(x => { if (x) evList.push(x); });

            if (evList.length > 0) {
                m3Html += `⚡ Girilen piyasa oranları <b>${glStr}</b> baremine göre adil oranlarla karşılaştırıldı.`;
                let m4Html = '';
                evList.forEach(item => {
                    let color = item.ev > 0 ? 'var(--accent-green)' : 'var(--accent-red)';
                    let tag = item.ev > 0 ? '✅ +EV DEĞER VAR' : '❌ -EV DÜŞÜK ORAN';
                    m4Html += `• <b>${item.label}</b> (Oran: ${item.mktOdd.toFixed(2)} | İhtimal: %${(item.prob*100).toFixed(1)}): <span style="color:${color}; font-weight:bold;">${item.ev > 0 ? '+' : ''}%${item.evPct} ${tag}</span><br>`;
                });
                document.getElementById('m4Text').innerHTML = m4Html;
            } else {
                m3Html += `ℹ️ 6. bölüme güncel piyasa oranlarını girerseniz piyasa sapması ve +EV otomatik hesaplanır.`;
                document.getElementById('m4Text').innerHTML = `💎 Değer oranı tespiti için 6. bölüme büro oranlarını girin. Adil eşikler: <b>${m1TarafPick} &gt; ${(1/m1TarafProb).toFixed(2)}</b> | <b>${glStr} ÜST &gt; ${fairSelOver}</b>`;
            }
            document.getElementById('m3Text').innerHTML = m3Html;

            // MOTOR 5: SAVUNMA & OMURGA ÖZETİ
            let hFormStr = homeStats ? `%${homeStats.ewmaForm} (${homeStats.played} maç)` : "Arşiv verisi yok";
            let aFormStr = awayStats ? `%${awayStats.ewmaForm} (${awayStats.played} maç)` : "Arşiv verisi yok";
            let advLines = [];
            if (bothDefCollapse) {
                advLines.push(`⚖️ <b>Çift Savunma Çöküşü:</b> Her iki takımda da 2+ savunma eksiği olduğundan karşılıklı xG şişirmesi kısıldı (Temkinli Oyun Freni).`);
            } else {
                if (homeBoostPct >= 8) {
                    let tagType = singleAwayCollapse ? 'savunma çöküşü' : (singleAwayBackbone ? 'omurga çöküşü' : 'kadro eksikleri');
                    advLines.push(`⚡ <b>${homeTeam}</b>, rakip ${tagType} ile <b>+%${homeBoostPct} xG avantajı</b> kazandı.`);
                }
                if (awayBoostPct >= 8) {
                    let tagType = singleHomeCollapse ? 'savunma çöküşü' : (singleHomeBackbone ? 'omurga çöküşü' : 'kadro eksikleri');
                    advLines.push(`⚡ <b>${awayTeam}</b>, rakip ${tagType} ile <b>+%${awayBoostPct} xG avantajı</b> kazandı.`);
                }
            }
            let advSummary = advLines.length > 0 ? `<br>${advLines.join('<br>')}` : '';

            document.getElementById('m5Text').innerHTML = `
                🏥 <b>${homeTeam}:</b> ${hInj.note} | <b>EWMA Form:</b> ${hFormStr}<br>
                🏥 <b>${awayTeam}:</b> ${aInj.note} | <b>EWMA Form:</b> ${aFormStr}${advSummary}
            `;

            // MOTOR 6
            let pAhHomeM05 = 0, pAhHomeM15 = 0, pAhAwayP05 = 0, pAhAwayM05 = 0;
            scoreMatrix.forEach(s => {
                let diff = s.home - s.away;
                if (diff >= 1) pAhHomeM05 += s.prob;
                if (diff >= 2) pAhHomeM15 += s.prob;
                if (diff <= 0) pAhAwayP05 += s.prob;
                if (diff <= -1) pAhAwayM05 += s.prob;
            });
            let bestAhProb = pAhHomeM05 >= 0.55 ? pAhHomeM05 : (pAhAwayM05 >= 0.52 ? pAhAwayM05 : pAhAwayP05);
            let bestAh = pAhHomeM05 >= 0.55 ? `${homeTeam} -0.5 AH (%${Math.round(pAhHomeM05*100)})`
                       : (pAhAwayM05 >= 0.52 ? `${awayTeam} -0.5 AH (%${Math.round(pAhAwayM05*100)})`
                       : `${awayTeam} +0.5 AH (%${Math.round(pAhAwayP05*100)})`);
            document.getElementById('m6Text').innerHTML = `
                ⚖️ <b>Ev -0.5 AH:</b> %${Math.round(pAhHomeM05*100)} | <b>Ev -1.5 AH:</b> %${Math.round(pAhHomeM15*100)}<br>
                ⚖️ <b>Dep +0.5 AH:</b> %${Math.round(pAhAwayP05*100)} | <b>Dep -0.5 AH:</b> %${Math.round(pAhAwayM05*100)}<br>
                🎯 <b>Önerilen Handikap:</b> <span style="color:var(--accent-yellow); font-weight:bold;">${bestAh}</span>
            `;

            // MOTOR 7
            let totalXg = baseHomeXg + baseAwayXg;
            let xgGap = Math.abs(baseHomeXg - baseAwayXg);
            let tempoLabel = totalXg >= 2.85 ? "YÜKSEK TEMPO (Açık Oyun)" : (totalXg >= 2.25 ? "ORTA TEMPO (Dengeli)" : "DÜŞÜK TEMPO (Kapalı/Sert)");
            let cardRisk = xgGap < 0.35 ? "YÜKSEK (Kafa Kafaya Mücadele ➔ 4.5 Üst Kart Eğilimi)" : (xgGap < 0.75 ? "ORTA (3.5 - 4.5 Kart Bandı)" : "DÜŞÜK (Tek Taraflı Oyun)");
            document.getElementById('m7Text').innerHTML = `
                ⚡ <b>Beklenen Tempo:</b> ${tempoLabel} (Toplam xG: ${totalXg.toFixed(2)})<br>
                🟨 <b>Sertlik / Kart Profili:</b> ${cardRisk}
            `;

            // MOTOR 8
            let hHomeWin = homeStats ? `%${homeStats.homeWinRate}` : "Veri Yok";
            let aAwayWin = awayStats ? `%${awayStats.awayWinRate}` : "Veri Yok";
            let sahaYorum = (homeStats && awayStats)
                ? (homeStats.homeWinRate > awayStats.awayWinRate + 15 ? `${homeTeam} iç sahada belirgin üstün.` : (awayStats.awayWinRate > homeStats.homeWinRate + 10 ? `${awayTeam} deplasmanda çok dirençli.` : `İç/dış saha güçleri dengeli.`))
                : "Saha kıyaslaması için her iki takımın Excel verisi gereklidir.";
            document.getElementById('m8Text').innerHTML = `
                🏟️ <b>${homeTeam} İç Saha Galibiyet:</b> ${hHomeWin} | <b>${awayTeam} Dep. Galibiyet:</b> ${aAwayWin}<br>
                📊 <b>Değerlendirme:</b> ${sahaYorum}
            `;

            // MOTOR 9
            let remXg20 = totalXg * (70 / 90);
            let pOver05After20 = Math.round((1 - Math.exp(-remXg20)) * 100);
            let pOver15After20 = Math.round((1 - (Math.exp(-remXg20) * (1 + remXg20))) * 100);
            let lateGoalProb = Math.round((1 - Math.exp(-(totalXg * (20 / 90)))) * 100);
            document.getElementById('m9Text').innerHTML = `
                ⏱️ <b>20. Dakika 0-0 Geçilirse:</b> Maçta 0.5 Üst ihtimali <b>%${pOver05After20}</b>, 1.5 Üst ihtimali <b>%${pOver15After20}</b>.<br>
                🔥 <b>70. Dakika Sonrası Gol İhtimali:</b> <b>%${lateGoalProb}</b> (Geç gol senaryosu).
            `;

            // MOTOR 12: GOALOO ANALİZİ
            let hXgVal = hasGoaloo ? inHxG : (homeStats ? homeStats.avgScored : 1.40);
            let hXgaVal = hasGoaloo ? inHxGA : (homeStats ? homeStats.avgConceded : 1.15);
            let aXgVal = hasGoaloo ? inAxG : (awayStats ? awayStats.avgScored : 1.20);
            let aXgaVal = hasGoaloo ? inAxGA : (awayStats ? awayStats.avgConceded : 1.25);

            let rawEvGol = (hXgVal + aXgaVal) / 2;
            let rawDepGol = (aXgVal + hXgaVal) / 2;
            let adjEvGol = Math.max(0.30, rawEvGol * (1 - hInj.attPen * 0.85) * homeGapDrag * homeBoostMult * cautionFactor);
            let adjDepGol = Math.max(0.25, rawDepGol * (1 - aInj.attPen * 0.85) * awayGapDrag * awayBoostMult * cautionFactor);
            let beklenenGolNum = adjEvGol + adjDepGol;
            let beklenenGol = beklenenGolNum.toFixed(2);
            let rawBeklenenGol = (rawEvGol + rawDepGol).toFixed(2);

            let fStateH = homeStats ? homeStats.ewmaForm : Math.min(95, Math.max(30, Math.round(50 + (hXgVal - hXgaVal) * 20)));
            let fAttackH = Math.min(98, Math.max(20, Math.round((45 + hXgVal * 24) * (1 - hInj.attPen * 0.5) * homeGapDrag * Math.min(1.20, homeBoostMult * cautionFactor))));
            let fDefH = Math.min(98, Math.max(12, Math.round((92 - hXgaVal * 26) * (1 - (hInj.defPen * 0.85 + hInj.gkPen * 0.5)))));

            let fStateA = awayStats ? awayStats.ewmaForm : Math.min(95, Math.max(30, Math.round(50 + (aXgVal - aXgaVal) * 20)));
            let fAttackA = Math.min(98, Math.max(20, Math.round((45 + aXgVal * 24) * (1 - aInj.attPen * 0.5) * awayGapDrag * Math.min(1.20, awayBoostMult * cautionFactor))));
            let fDefA = Math.min(98, Math.max(12, Math.round((92 - aXgaVal * 26) * (1 - (aInj.defPen * 0.85 + aInj.gkPen * 0.5)))));

            let hPowerScore = (fStateH * 0.40) + (fAttackH * 0.30) + (fDefH * 0.30);
            let aPowerScore = (fStateA * 0.40) + (fAttackA * 0.30) + (fDefA * 0.30);
            let m12TarafRes = hPowerScore > aPowerScore + 6 ? "MS 1" : (aPowerScore > hPowerScore + 6 ? "MS 2" : "MS 0 (Beraberlik)");

            let m5SelectedOverPct = Math.round(poissonOverTotalProb(beklenenGolNum, goalLine) * 100);
            let m12GoalRes = m5SelectedOverPct >= 50 ? `${glStr} ÜST` : `${glStr} ALT`;
            let m12BttsRes = (adjEvGol >= 0.95 && adjDepGol >= 0.85) ? "KG VAR" : "KG YOK";
            let m12Home15Prob = Math.round((1 - (poissonProb(adjEvGol, 0) + poissonProb(adjEvGol, 1))) * 100);
            let m12Away15Prob = Math.round((1 - (poissonProb(adjDepGol, 0) + poissonProb(adjDepGol, 1))) * 100);
            let m12Home15 = m12Home15Prob >= 50 ? `EVET (%${m12Home15Prob})` : `HAYIR (%${100 - m12Home15Prob})`;
            let m12Away15 = m12Away15Prob >= 50 ? `EVET (%${m12Away15Prob})` : `HAYIR (%${100 - m12Away15Prob})`;

            document.getElementById('m12Text').innerHTML = `
                📶 <b>Güç Kıyaslaması (State - Attack - Defence):</b><br>
                • <b>Ev Sahibi:</b> Form %${fStateH} | Hücum %${fAttackH} | Savunma %${fDefH}<br>
                • <b>Deplasman:</b> Form %${fStateA} | Hücum %${fAttackA} | Savunma %${fDefA}<br><br>
                <span class="m12-subtit">🎯 Motor 12 Kesin Tahminleri (Seçili Barem: ${glStr}):</span>
                • <b>Taraf Bahsi:</b> ${m12TarafRes}<br>
                • <b>Alt / Üst:</b> ${m12GoalRes} (Düzeltilmiş Beklenen: <b>${beklenenGol}</b> | Ham: ${rawBeklenenGol})<br>
                • <b>KG Var / Yok:</b> ${m12BttsRes}<br>
                • <b>Ev Sahibi 1.5 Üst:</b> ${m12Home15}<br>
                • <b>Deplasman 1.5 Üst:</b> ${m12Away15}
            `;

            // MOTOR 11: DİNAMİK AĞIRLIK VE OMURGA / KADRO YÖNELİMİ
            let formGap = Math.abs(fStateH - fStateA);
            let defInjuryImpact = (hInj.defStarterCount + aInj.defStarterCount) * 4.5 + (hInj.defCollapse ? 5 : 0) + (aInj.defCollapse ? 5 : 0);
            let backboneImpact = (hBackboneCollapse ? 6 : 0) + (aBackboneCollapse ? 6 : 0);
            let gkInjuryImpact = (hInj.gkStarterCount + aInj.gkStarterCount) * 1.5;
            let otherInjuryImpact = (hInj.attMidStarterCount + aInj.attMidStarterCount) * 1.2;

            let rawW1 = (!m2HasData ? 38 : 30) + (!hasGoaloo ? 8 : 0);
            let rawW2 = validRows === 0 ? 0 : (validRows < 10 ? 12 : (validRows < 20 ? 19 : (validRows >= 35 ? 27 : 23)));
            let rawW3 = 10 + Math.min(20, defInjuryImpact + backboneImpact + gkInjuryImpact + otherInjuryImpact) + (formGap >= 25 ? 4 : (formGap >= 15 ? 2 : 0));
            let rawW4 = (evList.length > 0 || bestAhProb >= 0.62) ? 12 : 9;
            let rawW5 = !hasGoaloo ? 5 : (validRows < 10 ? 24 : 20);

            let dynW = normalizeWeights({ w1: rawW1, w2: rawW2, w3: rawW3, w4: rawW4, w5: rawW5 });

            let m3GoalSignalPct = m1SelectedOverPct;
            if (singleHomeCollapse || singleAwayCollapse) {
                m3GoalSignalPct = Math.min(90, m1SelectedOverPct + 8);
            } else if (singleHomeBackbone || singleAwayBackbone) {
                m3GoalSignalPct = Math.min(88, m1SelectedOverPct + 5);
            } else if (bothDefCollapse) {
                m3GoalSignalPct = Math.max(20, m1SelectedOverPct - 4);
            }
            let m4GoalSignalPct = m1SelectedOverPct;

            let finalSelOverPct = Math.round(
                (dynW.w1 * m1SelectedOverPct +
                 dynW.w2 * m2SelectedOverPct +
                 dynW.w3 * m3GoalSignalPct +
                 dynW.w4 * m4GoalSignalPct +
                 dynW.w5 * m5SelectedOverPct) / 100
            );
            let finalGoalPick = finalSelOverPct >= 50 ? `${glStr} ÜST` : `${glStr} ALT`;
            let finalGoalConf = finalSelOverPct >= 50 ? finalSelOverPct : 100 - finalSelOverPct;
            let goalAgree = (m1SelectedOverPct >= 50 && m2SelectedOverPct >= 50) || (m1SelectedOverPct < 50 && m2SelectedOverPct < 50);

            let k3Direction = fStateH >= fStateA ? 'Ev Formda' : 'Dep Formda';
            if (singleHomeCollapse || singleHomeBackbone || (!bothDefCollapse && hNetMissing >= 2)) k3Direction = 'Dep Avantaj';
            else if (singleAwayCollapse || singleAwayBackbone || (!bothDefCollapse && aNetMissing >= 2)) k3Direction = 'Ev Avantaj';
            else if (bothDefCollapse) k3Direction = 'Temkinli / Dengeli';

            let k3Summary = `EWMA: Ev %${fStateH} vs Dep %${fStateA}`;
            if (bothDefCollapse) k3Summary += ` • ⚠️ Çift Sav. Eksiği`;
            else if (singleHomeCollapse) k3Summary += ` • 🚨 Ev Sav. Çöküş`;
            else if (singleAwayCollapse) k3Summary += ` • 🚨 Dep Sav. Çöküş`;
            else if (singleHomeBackbone) k3Summary += ` • ⚡ Ev Omurga Çöküşü`;
            else if (singleAwayBackbone) k3Summary += ` • ⚡ Dep Omurga Çöküşü`;

            document.getElementById('optaTableBody').innerHTML = `
                <tr>
                    <td><b>1) Dixon-Coles xG</b></td>
                    <td>Ev ${baseHomeXg.toFixed(2)} - Dep ${baseAwayXg.toFixed(2)} xG (${glStr}Ü %${m1SelectedOverPct})</td>
                    <td style="text-align:center;"><span class="opta-badge">${m1TarafPick} (%${m1TarafConf})</span></td>
                    <td class="opta-weight">%${dynW.w1}</td>
                </tr>
                <tr>
                    <td><b>2) Excel Arşiv</b></td>
                    <td>${validRows} gerçek maç tarandı (${glStr}Ü %${m2SelectedOverPct})</td>
                    <td style="text-align:center;"><span class="opta-badge">${m2HasData ? (m2SelectedOverPct >= 50 ? glStr + ' ÜST' : glStr + ' ALT') : 'Veri Yok'}</span></td>
                    <td class="opta-weight">%${dynW.w2}</td>
                </tr>
                <tr>
                    <td><b>3) Kadro & Omurga</b></td>
                    <td>${k3Summary}</td>
                    <td style="text-align:center;"><span class="opta-badge">${k3Direction}</span></td>
                    <td class="opta-weight">%${dynW.w3}</td>
                </tr>
                <tr>
                    <td><b>4) Asya Handikap</b></td>
                    <td>En güvenli çizgi: ${bestAh}</td>
                    <td style="text-align:center;"><span class="opta-badge">AH Onay</span></td>
                    <td class="opta-weight">%${dynW.w4}</td>
                </tr>
                <tr>
                    <td><b>5) Goaloo Çapraz</b></td>
                    <td>Düzeltilmiş Gol: ${beklenenGol} (${glStr}Ü %${m5SelectedOverPct})</td>
                    <td style="text-align:center;"><span class="opta-badge">${hasGoaloo ? m12GoalRes : 'Tahmini'}</span></td>
                    <td class="opta-weight">%${dynW.w5}</td>
                </tr>
                <tr class="opta-final-row">
                    <td class="opta-final-title">DİNAMİK SENTEZ KARARI</td>
                    <td>Adil Oran: ${(1/m1TarafProb).toFixed(2)} • Kesin Skor: ${scoreMatrix[0].home}-${scoreMatrix[0].away} & ${scoreMatrix[1].home}-${scoreMatrix[1].away}</td>
                    <td style="text-align: center;"><span class="opta-badge" style="background:#ff9900;border-color:#ff9900;color:#000;">${m1TarafPick} / ${finalGoalPick}</span></td>
                    <td class="opta-weight" style="color:var(--accent-green);">%${dynW.w1 + dynW.w2 + dynW.w3 + dynW.w4 + dynW.w5}</td>
                </tr>
            `;

            // MOTOR 10: YÖN UYUMLU VE GÜVEN TAVANLI KELLY KASA
            let kellyTaraf = 0, kellyTarafCapNote = "", kellyGoal = 0, kellyGoalCapNote = "", kellyNote = "";
            let pickedTarafEv = m1TarafPick === "MS 1" ? ev1 : (m1TarafPick === "MS 2" ? ev2 : ev0);

            if (pickedTarafEv) {
                kellyTaraf = pickedTarafEv.kelly;
                if (pickedTarafEv.isCapped) kellyTarafCapNote = ` <span style="font-size:11px; color:var(--accent-orange);">(Ham %${pickedTarafEv.rawKelly.toFixed(1)} ➔ %5 tavan)</span>`;
                kellyNote = "Gerçek piyasa oranlarıyla 1/4 Fractional Kelly + Gol Güven Filtresi uygulandı.";
            } else {
                kellyTaraf = m1TarafConf > 52 ? Math.min(KELLY_CAP, (m1TarafConf - 48) * 0.18) : 0;
                kellyNote = "Eksik oran alanları için model güven eşiğine göre sınırlı kasa önerisi verildi.";
            }

            let goalPickIsOver = finalGoalPick === `${glStr} ÜST`;
            let targetGoalEv = goalPickIsOver ? evOver : evUnder;
            let oppGoalEv = goalPickIsOver ? evUnder : evOver;

            let goalKellyCap = KELLY_CAP;
            let goalCapLabel = "";
            if (finalGoalConf < 55) {
                goalKellyCap = 0.0;
                goalCapLabel = "güven <%55 ➔ Pas";
            } else if (finalGoalConf < 60 || !goalAgree) {
                goalKellyCap = 1.5;
                goalCapLabel = !goalAgree ? "karma sentez %1.5 tavan" : "güven <%60 ➔ %1.5 tavan";
            }

            if (targetGoalEv) {
                let rawG = targetGoalEv.rawKelly;
                kellyGoal = Math.min(goalKellyCap, rawG);
                if (rawG > 0 && goalKellyCap === 0) {
                    kellyGoalCapNote = ` <span style="font-size:11px; color:var(--accent-orange);">(Ham %${rawG.toFixed(1)} ➔ ${goalCapLabel})</span>`;
                } else if (rawG > goalKellyCap) {
                    kellyGoalCapNote = ` <span style="font-size:11px; color:var(--accent-orange);">(Ham %${rawG.toFixed(1)} ➔ ${goalCapLabel || '%5 tavan'})</span>`;
                }
            } else if (!evOver && !evUnder) {
                let rawG = finalGoalConf >= 55 ? Math.min(4.5, (finalGoalConf - 50) * 0.18) : 0;
                kellyGoal = Math.min(goalKellyCap, rawG);
                if (rawG > goalKellyCap && goalKellyCap > 0) {
                    kellyGoalCapNote = ` <span style="font-size:11px; color:var(--accent-orange);">(${goalCapLabel})</span>`;
                }
            } else {
                kellyGoal = 0;
                if (oppGoalEv && oppGoalEv.ev > 0) {
                    kellyGoalCapNote = ` <span style="font-size:11px; color:var(--text-muted);">(Ters yön ${oppGoalEv.label} oranlı; seçilen yön ${finalGoalPick} pas)</span>`;
                }
            }

            let totalKellyNum = kellyTaraf + kellyGoal;
            let totalKelly = totalKellyNum.toFixed(1);
            document.getElementById('m10Text').innerHTML = `
                💰 <b>Taraf (${m1TarafPick}) Kasa:</b> ${kellyTaraf > 0 ? '%' + kellyTaraf.toFixed(1) + kellyTarafCapNote : '<span style="color:var(--accent-orange);">%0.0 (Pas Geç)</span>'}<br>
                💰 <b>Gol (${finalGoalPick}) Kasa:</b> ${kellyGoal > 0 ? '%' + kellyGoal.toFixed(1) + kellyGoalCapNote : '<span style="color:var(--accent-orange);">%0.0 (Pas Geç)</span>' + kellyGoalCapNote}<br>
                ℹ️ ${kellyNote}
            `;

            // ÜÇLÜ SENTEZ MÜHRÜ (YEŞİL TAHMİN KUTUSU)
            document.getElementById('consensusTitle').innerHTML = `👑 ${homeTeamUpper} - ${awayTeamUpper} 👑<br><span style="font-size:12px; color:#fff; font-weight:normal; letter-spacing:1px; opacity: 0.9;">ÜÇLÜ SENTEZ MÜHRÜ (M1 + M2 + KELLY // BAREM ${glStr})</span>`;

            let bttsW1 = m2HasData ? (dynW.w1 + dynW.w3 + dynW.w5) : 100;
            let bttsW2 = m2HasData ? (dynW.w2 + dynW.w4) : 0;
            let finalBttsPct = Math.round((m1BttsPct * bttsW1 + m2BttsPct * bttsW2) / (bttsW1 + bttsW2));
            let finalBttsPick = finalBttsPct >= 50 ? "KG VAR" : "KG YOK";
            let finalBttsConf = finalBttsPct >= 50 ? finalBttsPct : 100 - finalBttsPct;

            let finalHt05Pct = Math.round((m1HtOver05Pct * bttsW1 + m2Ht05Pct * bttsW2) / (bttsW1 + bttsW2));
            let finalHt05Pick = finalHt05Pct >= 50 ? "İY 0.5 ÜST" : "İY 0.5 ALT";
            let finalHt05Conf = finalHt05Pct >= 50 ? finalHt05Pct : 100 - finalHt05Pct;

            let finalHt1 = Math.round((m1Ht1Pct * bttsW1 + m2Ht1Pct * bttsW2) / (bttsW1 + bttsW2));
            let finalHtX = Math.round((m1HtXPct * bttsW1 + m2HtXPct * bttsW2) / (bttsW1 + bttsW2));
            let finalHt2 = Math.max(0, 100 - finalHt1 - finalHtX);
            let finalHtTarafPick = (finalHt1 >= finalHtX && finalHt1 >= finalHt2) ? "İY 1" : ((finalHt2 >= finalHtX && finalHt2 > finalHt1) ? "İY 2" : "İY X");
            let finalHtTarafConf = Math.max(finalHt1, finalHtX, finalHt2);

            let bttsAgree = (m1BttsPct >= 50 && m2BttsPct >= 50) || (m1BttsPct < 50 && m2BttsPct < 50);

            let tarafKellyHtml = kellyTaraf > 0
                ? `<b>Kelly Kasa: %${kellyTaraf.toFixed(1)}</b>`
                : `<span class="pas-text">Kelly Kasa: %0.0 (Pas Geç)</span>`;

            let goalKellyHtml = kellyGoal > 0
                ? `<b>Kelly Kasa: %${kellyGoal.toFixed(1)}</b>`
                : `<span class="pas-text">Kelly Kasa: %0.0 (Pas Geç)</span>`;

            let goalBadge = '';
            if (goalAgree && kellyGoal > 0) {
                goalBadge = `<span class="seal-badge seal-triple">👑 M1+M2+KELLY ONAMLI</span>`;
            } else if (goalAgree && kellyGoal <= 0) {
                goalBadge = `<span class="seal-badge seal-diff">⚠️ M1+M2 UYUMLU (ORAN DEĞERSİZ / PAS)</span>`;
            } else if (!goalAgree && kellyGoal > 0) {
                goalBadge = `<span class="seal-badge seal-ok">⚖️ KARMA SENTEZ (SINIRLI +EV)</span>`;
            } else {
                goalBadge = `<span class="seal-badge seal-pass">⛔ KARMA SENTEZ (PAS GEÇ)</span>`;
            }

            let bttsBadge = bttsAgree
                ? `<span class="seal-badge seal-triple">👑 M1+M2 TAM UYUMLU</span>`
                : `<span class="seal-badge seal-diff">⚖️ KARMA SENTEZ</span>`;

            let alertHtml = '';
            if (singleHomeCollapse) {
                alertHtml += `<div class="def-alert">🚨 <b>SAVUNMA ÇÖKÜŞÜ AVANTAJI:</b> ${homeTeam} savunma hattında ${hInj.defStarterCount} ilk 11 eksiği var ➔ <b>${awayTeam}</b> hücumuna <b>+%${awayBoostPct} xG avantajı</b> işlendi.</div>`;
            } else if (singleAwayCollapse) {
                alertHtml += `<div class="def-alert">🚨 <b>SAVUNMA ÇÖKÜŞÜ AVANTAJI:</b> ${awayTeam} savunma hattında ${aInj.defStarterCount} ilk 11 eksiği var ➔ <b>${homeTeam}</b> hücumuna <b>+%${homeBoostPct} xG avantajı</b> işlendi.</div>`;
            } else if (singleHomeBackbone) {
                alertHtml += `<div class="backbone-alert">⚡ <b>OMURGA ÇÖKÜŞÜ AVANTAJI:</b> ${homeTeam} kadrosunda ${hInj.starterCount} kritik ilk 11 eksiği var (${awayTeam} kadrosu daha sağlıklı) ➔ <b>${awayTeam}</b> hücumuna <b>+%${awayBoostPct} xG avantajı</b> işlendi.</div>`;
            } else if (singleAwayBackbone) {
                alertHtml += `<div class="backbone-alert">⚡ <b>OMURGA ÇÖKÜŞÜ AVANTAJI:</b> ${awayTeam} kadrosunda ${aInj.starterCount} kritik ilk 11 eksiği var (${homeTeam} kadrosu daha sağlıklı) ➔ <b>${homeTeam}</b> hücumuna <b>+%${homeBoostPct} xG avantajı</b> işlendi.</div>`;
            } else if (bothDefCollapse) {
                alertHtml += `<div class="caution-alert">⚠️ <b>ÇİFT SAVUNMA ÇÖKÜŞÜ (TEMKİNLİ OYUN FRENİ):</b> Her iki takımda da 2+ savunma eksiği var (${homeTeam}: ${hInj.defStarterCount}, ${awayTeam}: ${aInj.defStarterCount}) ➔ Karşılıklı xG şişirmesi kısıldı ve temkinli oyun katsayısı uygulandı.</div>`;
            }

            // V36.1: SÜRPRİZ / DEĞER (+EV) RADARI
            let activeLabels = new Set();
            if (kellyTaraf > 0) activeLabels.add(m1TarafPick);
            if (kellyGoal > 0) activeLabels.add(finalGoalPick);

            let radarCandidates = evList
                .filter(x => x.ev >= 0.05 && !activeLabels.has(x.label))
                .sort((a, b) => b.ev - a.ev);

            if (radarCandidates.length > 0 && (kellyTaraf === 0 || kellyGoal === 0)) {
                let topR = radarCandidates[0];
                let radarKelly = Math.min(2.5, topR.kelly).toFixed(1);
                alertHtml += `<div class="radar-alert">💎 <b>SÜRPRİZ / DEĞER (+EV) RADARI:</b> Ana tercihler pas geçilirken Motor 4, <b>${topR.label}</b> (Oran: <b>${topR.mktOdd.toFixed(2)}</b> | İhtimal: %${(topR.prob*100).toFixed(1)}) seçeneğinde <b>+%${topR.evPct} +EV</b> tespit etti (Sürpriz Kasa: <b>%${radarKelly}</b>).</div>`;
            }

            document.getElementById('consensusText').innerHTML = `
                📌 <b>1. Taraf Mührü:</b> ${m1TarafPick} (Güven: %${m1TarafConf}) ➔ ${tarafKellyHtml}<br>
                ⚽ <b>2. Gol Mührü:</b> ${finalGoalPick} (Net Güven: %${finalGoalConf}) ➔ ${goalKellyHtml} ${goalBadge}<br>
                🔥 <b>3. KG Mührü:</b> ${finalBttsPick} (Net Güven: %${finalBttsConf}) ${bttsBadge}<br>
                ⏱️ <b>4. İlk Yarı Gol Mührü:</b> ${finalHt05Pick} (Net Güven: %${finalHt05Conf})<br>
                ⏳ <b>5. İlk Yarı Taraf Mührü:</b> ${finalHtTarafPick} (Net Güven: %${finalHtTarafConf})<br>
                🏆 <b>6. Nihai Skor Çifti:</b> ${scoreMatrix[0].home}-${scoreMatrix[0].away} veya ${scoreMatrix[1].home}-${scoreMatrix[1].away}
                ${alertHtml}
            `;

            let trueConfScore = Math.min(96, Math.round((m1TarafConf + finalGoalConf + finalBttsConf) / 3));
            let totalKellyFooterHtml = totalKellyNum > 0
                ? `%${totalKelly}`
                : `<span class="pas-text">%0.0 (PAS GEÇ - DEĞER ORANI YOK)</span>`;

            document.getElementById('sealFooter').innerHTML = `
                🔒 ÜÇLÜ KANTİTATİF GÜVEN MÜHRÜ: %${trueConfScore}<br>
                💼 ÖNERİLEN TOPLAM OPTİMAL KASA RİSKİ (KELLY): ${totalKellyFooterHtml}
            `;

            document.getElementById('loadingText').style.display = 'none';
            document.getElementById('resultsArea').style.display = 'block';
        } catch (err) {
            document.getElementById('loadingText').style.display = 'none';
            alert("Analiz sırasında hata oluştu: " + err.message);
        }
    }, 300);
}
</script>

</body>
</html>