import { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const SIGN_SYMBOLS = {
  'Koç': '♈', 'Boğa': '♉', 'İkizler': '♊', 'Yengeç': '♋',
  'Aslan': '♌', 'Başak': '♍', 'Terazi': '♎', 'Akrep': '♏',
  'Yay': '♐', 'Oğlak': '♑', 'Kova': '♒', 'Balık': '♓'
};

const PLANET_SYMBOLS = {
  'Güneş ☉': '☉', 'Ay ☽': '☽', 'Merkür ☿': '☿',
  'Venüs ♀': '♀', 'Mars ♂': '♂', 'Jüpiter ♃': '♃',
  'Satürn ♄': '♄', 'Uranüs ♅': '♅', 'Neptün ♆': '♆',
  'Plüton ♇': '♇', 'Kuzey Node ☊': '☊', 'Güney Node ☋': '☋',
  'Lilith ⚸': '⚸', 'Şans Noktası ⊕': '⊕',
  'Chiron ⚷': '⚷', 'Ceres ⚳': '⚳', 'Vesta ⚶': '⚶',
  'Pallas ⚴': '⚴', 'Juno ⚵': '⚵'
};

const PLANET_COLORS = {
  'Güneş ☉': '#b8860b', 'Ay ☽': '#555577', 'Merkür ☿': '#2471a3',
  'Venüs ♀': '#a93226', 'Mars ♂': '#c0392b', 'Jüpiter ♃': '#6c3483',
  'Satürn ♄': '#444455', 'Uranüs ♅': '#148f77', 'Neptün ♆': '#1a5276',
  'Plüton ♇': '#6c3483', 'Kuzey Node ☊': '#1e8449', 'Güney Node ☋': '#1e8449',
  'Lilith ⚸': '#922b21', 'Şans Noktası ⊕': '#b8860b', 'Chiron ⚷': '#0e6655',
  'Ceres ⚳': '#7d6608', 'Vesta ⚶': '#784212', 'Pallas ⚴': '#1a5276',
  'Juno ⚵': '#6c3483'
};

const MAIN_PLANETS = [
  'Güneş ☉', 'Ay ☽', 'Merkür ☿', 'Venüs ♀', 'Mars ♂',
  'Jüpiter ♃', 'Satürn ♄', 'Uranüs ♅', 'Neptün ♆', 'Plüton ♇',
  'Kuzey Node ☊', 'Güney Node ☋', 'Lilith ⚸', 'Şans Noktası ⊕',
  'Chiron ⚷', 'Ceres ⚳', 'Vesta ⚶', 'Pallas ⚴', 'Juno ⚵'
];

const HOUSE_KEYS = [
  '1. Ev','2. Ev','3. Ev','4. Ev','5. Ev','6. Ev',
  '7. Ev','8. Ev','9. Ev','10. Ev','11. Ev','12. Ev',
  'Yükselen (ASC)', 'Orta Gökyüzü (MC)'
];

const ASPECT_DEFS = [
  { name: 'Kavuşum', angle: 0,   orb: 10, symbol: '☌', color: '#b8860b' },
  { name: 'Sextile',  angle: 60,  orb: 6,  symbol: '⚹', color: '#2471a3' },
  { name: 'Kare',     angle: 90,  orb: 8,  symbol: '□', color: '#c0392b' },
  { name: 'Üçgen',    angle: 120, orb: 8,  symbol: '△', color: '#1e8449' },
  { name: 'Karşıt',  angle: 180, orb: 10, symbol: '☍', color: '#922b21' },
  { name: 'Görmeyen', angle: 150, orb: 3,  symbol: '⚻', color: '#555577' },
];

function degStr(degree) {
  const deg = Math.floor(degree);
  const min = Math.floor((degree - deg) * 60);
  const sec = Math.floor(((degree - deg) * 60 - min) * 60);
  return `${String(deg).padStart(2,'0')}°${String(min).padStart(2,'0')}'${String(sec).padStart(2,'0')}"`;
}

function getPlanetHouse(longitude, houses) {
  const houseKeys12 = ['1. Ev','2. Ev','3. Ev','4. Ev','5. Ev','6. Ev',
                       '7. Ev','8. Ev','9. Ev','10. Ev','11. Ev','12. Ev'];
  const cusps = houseKeys12.map(k => houses[k]?.cusp_longitude);
  if (cusps.some(v => v === undefined)) return '';
  for (let i = 0; i < 12; i++) {
    const start = cusps[i];
    const end = cusps[(i + 1) % 12];
    if (start < end) {
      if (longitude >= start && longitude < end) return (i + 1) + '. Ev';
    } else {
      if (longitude >= start || longitude < end) return (i + 1) + '. Ev';
    }
  }
  return '';
}

function getAspects(planets) {
  const active = MAIN_PLANETS.filter(n => planets[n]);
  const aspects = [];
  for (let i = 0; i < active.length; i++) {
    for (let j = i + 1; j < active.length; j++) {
      const p1 = planets[active[i]], p2 = planets[active[j]];
      let diff = Math.abs(p1.longitude - p2.longitude);
      if (diff > 180) diff = 360 - diff;
      for (const asp of ASPECT_DEFS) {
        const orb = Math.abs(diff - asp.angle);
        if (orb <= asp.orb) {
          aspects.push({ p1: active[i], p2: active[j], asp, orb: orb.toFixed(2) });
          break;
        }
      }
    }
  }
  return aspects;
}

function drawNatalChart(canvas, chartData) {
  if (!canvas || !chartData) return;
  const size = Math.min(window.innerWidth - 40, 560);
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const cx = size / 2, cy = size / 2;
  const R = size / 2 - 8;

  const signs = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];
  const signColors = [
    '#c0392b','#8B4513','#2980b9','#16a085',
    '#d35400','#27ae60','#8e44ad','#c0392b',
    '#2471a3','#707b8e','#17a589','#6c3483'
  ];

  const rSignOuter = R * 0.98, rSignInner = R * 0.80;
  const rPlanetOuter = R * 0.78, rPlanetInner = R * 0.52;
  const rHouseOuter = R * 0.50, rHouseInner = R * 0.40;
  const rAspect = R * 0.38;

  const houses = chartData.houses || {};
  const ascLong = houses['Yükselen (ASC)']?.cusp_longitude || houses['1. Ev']?.cusp_longitude || 0;

  function toRad(longitude) {
    const angle = ((longitude - ascLong + 360) % 360);
    return (Math.PI - angle * Math.PI / 180);
  }

  // Arka plan
  ctx.fillStyle = '#faf8f3';
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fill();

  // Dış çember
  ctx.beginPath();
  ctx.arc(cx, cy, rSignOuter, 0, Math.PI * 2);
  ctx.strokeStyle = '#999'; ctx.lineWidth = 1.5; ctx.stroke();

  // Burç iç çember
  ctx.beginPath();
  ctx.arc(cx, cy, rSignInner, 0, Math.PI * 2);
  ctx.strokeStyle = '#aaa'; ctx.lineWidth = 1; ctx.stroke();

  // Burç dilimleri
  for (let i = 0; i < 12; i++) {
    const startLong = i * 30;
    const startRad = toRad(startLong), endRad = toRad(startLong + 30);
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(startRad) * rSignInner, cy + Math.sin(startRad) * rSignInner);
    ctx.arc(cx, cy, rSignOuter, startRad, endRad, true);
    ctx.arc(cx, cy, rSignInner, endRad, startRad, false);
    ctx.closePath();
    ctx.fillStyle = signColors[i] + '20'; ctx.fill();

    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(startRad) * rSignInner, cy + Math.sin(startRad) * rSignInner);
    ctx.lineTo(cx + Math.cos(startRad) * rSignOuter, cy + Math.sin(startRad) * rSignOuter);
    ctx.strokeStyle = '#ccc'; ctx.lineWidth = 0.5; ctx.stroke();

    const midRad = toRad(startLong + 15);
    const symR = (rSignOuter + rSignInner) / 2;
    ctx.fillStyle = signColors[i];
    ctx.font = `${size * 0.038}px 'Segoe UI Symbol', 'Apple Symbols', serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(signs[i], cx + Math.cos(midRad) * symR, cy + Math.sin(midRad) * symR);
  }

  // Halka çemberleri
  [rPlanetOuter, rPlanetInner, rHouseOuter].forEach(r => {
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.strokeStyle = '#aaa'; ctx.lineWidth = 0.8; ctx.stroke();
  });
  ctx.beginPath(); ctx.arc(cx, cy, rHouseInner, 0, Math.PI * 2);
  ctx.strokeStyle = '#999'; ctx.lineWidth = 1; ctx.stroke();
  ctx.beginPath(); ctx.arc(cx, cy, rAspect, 0, Math.PI * 2);
  ctx.strokeStyle = '#ddd'; ctx.lineWidth = 0.5; ctx.stroke();

  // Ev çizgileri
  const houseKeys12 = ['1. Ev','2. Ev','3. Ev','4. Ev','5. Ev','6. Ev',
                        '7. Ev','8. Ev','9. Ev','10. Ev','11. Ev','12. Ev'];
  houseKeys12.forEach((key, i) => {
    const houseData = houses[key];
    if (!houseData) return;
    const rad = toRad(houseData.cusp_longitude);
    const isAngular = i % 3 === 0;

    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(rad) * rHouseInner, cy + Math.sin(rad) * rHouseInner);
    ctx.lineTo(cx + Math.cos(rad) * rPlanetOuter, cy + Math.sin(rad) * rPlanetOuter);
    ctx.strokeStyle = isAngular ? '#b8860b' : '#cccccc';
    ctx.lineWidth = isAngular ? 1.5 : 0.5;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(rad) * rHouseInner, cy + Math.sin(rad) * rHouseInner);
    ctx.lineTo(cx + Math.cos(rad) * (rAspect + 1), cy + Math.sin(rad) * (rAspect + 1));
    ctx.strokeStyle = isAngular ? '#b8860b55' : '#cccccc44';
    ctx.lineWidth = isAngular ? 1 : 0.3;
    ctx.stroke();

    const nextHouse = houses[houseKeys12[(i + 1) % 12]];
    if (nextHouse) {
      let midLong = (houseData.cusp_longitude + nextHouse.cusp_longitude) / 2;
      if (Math.abs(nextHouse.cusp_longitude - houseData.cusp_longitude) > 180) midLong += 180;
      const midRad = toRad(midLong);
      const nr = (rHouseOuter + rHouseInner) / 2;
      ctx.fillStyle = '#888888';
      ctx.font = `${size * 0.020}px sans-serif`;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(i + 1, cx + Math.cos(midRad) * nr, cy + Math.sin(midRad) * nr);
    }
  });

  // Gezegenler — collision avoidance YOK, birebir longitude pozisyonu
  const planets = chartData.all_positions || {};
  const planetR = (rPlanetOuter + rPlanetInner) / 2;

  MAIN_PLANETS.forEach(name => {
    const pdata = planets[name];
    if (!pdata) return;
    const rad = toRad(pdata.longitude);
    const col = PLANET_COLORS[name] || '#333333';

    // İnce çizgi (gezegenden ev halkasına)
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(rad) * rPlanetInner, cy + Math.sin(rad) * rPlanetInner);
    ctx.lineTo(cx + Math.cos(rad) * rHouseOuter, cy + Math.sin(rad) * rHouseOuter);
    ctx.strokeStyle = col + '33'; ctx.lineWidth = 0.5; ctx.stroke();

    // Gezegen sembolü
    ctx.fillStyle = pdata.retrograde ? '#c0392b' : col;
    ctx.font = `bold ${size * 0.042}px serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(PLANET_SYMBOLS[name] || '', cx + Math.cos(rad) * planetR, cy + Math.sin(rad) * planetR);

    // Retrograde ℞
    if (pdata.retrograde) {
      ctx.font = `${size * 0.018}px sans-serif`;
      ctx.fillStyle = '#c0392b';
      ctx.fillText('R', cx + Math.cos(rad) * planetR + size * 0.022, cy + Math.sin(rad) * planetR - size * 0.018);
    }

    // Gezegen kısa ismi
    const shortName = name.split(' ')[0];
    ctx.font = `${size * 0.016}px sans-serif`;
    ctx.fillStyle = col + 'bb';
    ctx.fillText(shortName, cx + Math.cos(rad) * (planetR - size * 0.038), cy + Math.sin(rad) * (planetR - size * 0.038));

    // Derece etiketi
    const deg = Math.floor(pdata.degree);
    ctx.fillStyle = col;
    ctx.font = `${size * 0.017}px sans-serif`;
    ctx.fillText(`${deg}°`, cx + Math.cos(rad) * (rSignInner - size * 0.022), cy + Math.sin(rad) * (rSignInner - size * 0.022));
  });

  // Aspect çizgileri
  MAIN_PLANETS.forEach((n1, i, arr) => {
    if (!planets[n1]) return;
    arr.slice(i + 1).forEach(n2 => {
      if (!planets[n2]) return;
      const p1 = planets[n1], p2 = planets[n2];
      let diff = Math.abs(p1.longitude - p2.longitude);
      if (diff > 180) diff = 360 - diff;
      for (const asp of ASPECT_DEFS) {
        if (Math.abs(diff - asp.angle) <= asp.orb) {
          const r1 = toRad(p1.longitude), r2 = toRad(p2.longitude);
          ctx.beginPath();
          ctx.moveTo(cx + Math.cos(r1) * rAspect, cy + Math.sin(r1) * rAspect);
          ctx.lineTo(cx + Math.cos(r2) * rAspect, cy + Math.sin(r2) * rAspect);
          ctx.strokeStyle = asp.color + '88'; ctx.lineWidth = 0.8; ctx.stroke();
          break;
        }
      }
    });
  });

  // ASC etiketi
  if (houses['1. Ev']) {
    const r = toRad(houses['1. Ev'].cusp_longitude);
    ctx.fillStyle = '#8B6914';
    ctx.font = `bold ${size * 0.022}px sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('ASC', cx + Math.cos(r) * (rHouseInner - size * 0.035), cy + Math.sin(r) * (rHouseInner - size * 0.035));
  }

  // MC etiketi
  if (houses['Orta Gökyüzü (MC)']) {
    const r = toRad(houses['Orta Gökyüzü (MC)'].cusp_longitude);
    ctx.fillStyle = '#1a5276';
    ctx.font = `bold ${size * 0.022}px sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('MC', cx + Math.cos(r) * (rHouseInner - size * 0.035), cy + Math.sin(r) * (rHouseInner - size * 0.035));
  }
}

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const canvasRef = useRef(null);

  const { chartData, formData } = location.state || {};
  const [loading, setLoading] = useState(true);
  const [allNotes, setAllNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!chartData) { navigate('/'); return; }
    fetch((import.meta.env.VITE_API_URL || '') + '/api/special-notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(chartData),
    })
      .then(r => r.json())
      .then(data => { setAllNotes(data.notes || []); setLoading(false); })
      .catch(() => { setError('Bir hata oluştu.'); setLoading(false); });
  }, []);

  useEffect(() => {
    if (!loading && canvasRef.current && chartData) {
      drawNatalChart(canvasRef.current, chartData);
    }
  }, [loading]);

  function getRandomNote() {
    if (!allNotes.length) return;
    setCurrentNote(allNotes[Math.floor(Math.random() * allNotes.length)]);
  }

  if (!chartData) return null;

  const planets = chartData.all_positions || {};
  const houses = chartData.houses || {};
  const aspects = getAspects(planets);

  return (
    <div className="container result-container" style={{ width: '100%' }}>
      <div className="result-header">
        <a href="/" className="back-btn" onClick={e => { e.preventDefault(); navigate('/'); }}>← Geri</a>
        <h1>✨ {formData?.name} ✨</h1>
        <p className="birth-info">{formData?.birth_date} · {formData?.birth_time} · {formData?.birth_city}</p>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Haritanız hesaplanıyor...</p>
        </div>
      )}

      {error && <p style={{ color: '#c0392b', textAlign: 'center' }}>{error}</p>}

      {!loading && !error && (
        <div>
          {/* Doğum Haritası */}
          <div className="section">
            <h2>Doğum Haritası</h2>
            <div className="chart-wrapper">
              <canvas ref={canvasRef} />
            </div>
          </div>

          {/* Özel Notlar */}
          <div className="section">
            <h2>Özel Notlar ✨</h2>
            <div className="random-note-box">
              {!currentNote ? (
                <div className="note-text">Butona bas, sana özel bir not görelim ✨</div>
              ) : (
                <>
                  <div className="note-title">{currentNote.title}</div>
                  <div className="note-context">→ {currentNote.context}</div>
                  <div className="note-body">{currentNote.text}</div>
                </>
              )}
              <button onClick={getRandomNote}>Yeni Not Göster 🎲</button>
            </div>
          </div>

          {/* Gezegenler & Evler */}
          <div className="section">
            <h2>Gezegenler & Evler</h2>
            <div className="two-col" style={{ gap: '0.5rem' }}>
              <div style={{ borderRight: '1px solid #1e1e3a', paddingRight: '2rem' }}>
                <table className="planet-table">
                  <tbody>
                    {MAIN_PLANETS.filter(n => planets[n]).map(name => {
                      const p = planets[name];
                      const signName = p.sign.split(' ')[0];
                      const house = getPlanetHouse(p.longitude, houses);
                      return (
                        <tr key={name}>
                          <td className="pt-sym">{PLANET_SYMBOLS[name] || ''}</td>
                          <td className="pt-name">
                            {name.split(' ').slice(0, -1).join(' ')}
                            {p.retrograde && <span style={{ color: '#c0392b', fontSize: '0.85rem' }}> ℞</span>}
                          </td>
                          <td className="pt-ssym">{SIGN_SYMBOLS[signName] || ''}</td>
                          <td className="pt-sign">{signName}</td>
                          <td className="pt-house">{house}</td>
                          <td className="pt-deg">{degStr(p.degree)}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              <div>
                <table className="planet-table">
                  <tbody>
                    {HOUSE_KEYS.filter(k => houses[k]).map(key => {
                      const h = houses[key];
                      const signName = h.sign.split(' ')[0];
                      const shortKey = key.replace('Yükselen (ASC)', 'ASC').replace('Orta Gökyüzü (MC)', 'MC');
                      return (
                        <tr key={key}>
                          <td className="pt-name" style={{ padding: '0.9rem 0.6rem' }}>{shortKey}</td>
                          <td className="pt-ssym" style={{ padding: '0.9rem 0.6rem' }}>{SIGN_SYMBOLS[signName] || ''}</td>
                          <td className="pt-sign" style={{ padding: '0.9rem 0.6rem' }}>{signName}</td>
                          <td className="pt-deg" style={{ padding: '0.9rem 0.6rem' }}>{degStr(h.degree)}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Açılar */}
          <div className="section">
            <h2>Açılar</h2>
            <div id="aspectGrid">
              <table className="planet-table">
                <thead>
                  <tr>
                    <th style={{ color: '#c9a96e', fontSize: '0.78rem', letterSpacing: '0.08em', textTransform: 'uppercase', padding: '0.6rem 1rem', borderBottom: '1px solid #1e1e3a', textAlign: 'left' }}>Gezegen</th>
                    <th style={{ color: '#c9a96e', fontSize: '0.78rem', letterSpacing: '0.08em', textTransform: 'uppercase', padding: '0.6rem 1rem', borderBottom: '1px solid #1e1e3a', textAlign: 'left' }}>Açı</th>
                    <th style={{ color: '#c9a96e', fontSize: '0.78rem', letterSpacing: '0.08em', textTransform: 'uppercase', padding: '0.6rem 1rem', borderBottom: '1px solid #1e1e3a', textAlign: 'left' }}>Gezegen</th>
                    <th style={{ color: '#c9a96e', fontSize: '0.78rem', letterSpacing: '0.08em', textTransform: 'uppercase', padding: '0.6rem 1rem', borderBottom: '1px solid #1e1e3a', textAlign: 'left' }}>Orb</th>
                  </tr>
                </thead>
                <tbody>
                  {aspects.map((a, i) => (
                    <tr key={i}>
                      <td className="pt-name">{PLANET_SYMBOLS[a.p1] || ''} {a.p1.split(' ')[0]}</td>
                      <td className="pt-sign" style={{ color: a.asp.color, fontWeight: 'bold' }}>{a.asp.symbol} {a.asp.name}</td>
                      <td className="pt-name">{PLANET_SYMBOLS[a.p2] || ''} {a.p2.split(' ')[0]}</td>
                      <td className="pt-deg">{a.orb}°</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}