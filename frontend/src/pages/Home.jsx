import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../img/logo.png';

const MONTHS = [
  { value: '01', label: 'Ocak' }, { value: '02', label: 'Şubat' },
  { value: '03', label: 'Mart' }, { value: '04', label: 'Nisan' },
  { value: '05', label: 'Mayıs' }, { value: '06', label: 'Haziran' },
  { value: '07', label: 'Temmuz' }, { value: '08', label: 'Ağustos' },
  { value: '09', label: 'Eylül' }, { value: '10', label: 'Ekim' },
  { value: '11', label: 'Kasım' }, { value: '12', label: 'Aralık' },
];

const CITIES = [
  'adana','adıyaman','afyonkarahisar','ağrı','aksaray','amasya','ankara','antalya',
  'ardahan','artvin','aydın','balıkesir','bartın','batman','bayburt','bilecik',
  'bingöl','bitlis','bolu','burdur','bursa','çanakkale','çankırı','çorum',
  'denizli','diyarbakır','düzce','edirne','elazığ','erzincan','erzurum','eskişehir',
  'gaziantep','giresun','gümüşhane','hakkari','hatay','ığdır','isparta','istanbul',
  'izmir','kahramanmaraş','karabük','karaman','kars','kastamonu','kayseri','kilis',
  'kırıkkale','kırklareli','kırşehir','kocaeli','konya','kütahya','malatya','manisa',
  'mardin','mersin','muğla','muş','nevşehir','niğde','ordu','osmaniye','rize',
  'sakarya','samsun','şanlıurfa','siirt','sinop','şırnak','sivas','tekirdağ',
  'tokat','trabzon','tunceli','uşak','van','yalova','yozgat','zonguldak',
];

// Şehir adını option value'ya dönüştür (türkçe karakterler → ascii)
function cityToValue(city) {
  return city
    .toLowerCase()
    .replace(/ş/g,'s').replace(/ı/g,'i').replace(/ğ/g,'g')
    .replace(/ü/g,'u').replace(/ö/g,'o').replace(/ç/g,'c')
    .replace(/İ/g,'i');
}

export default function Home() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    birth_day: '',
    birth_month: '',
    birth_year: '',
    birth_hour: '',
    birth_minute: '',
    birth_city: '',
  });
  const [loading, setLoading] = useState(false);

  // Dinamik yıl/gün/saat/dakika seçenekleri
  const years = Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i);
  const days = Array.from({ length: 31 }, (_, i) => String(i + 1).padStart(2, '0'));
  const hours = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'));
  const minutes = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'));

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.id]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const birth_date = `${form.birth_day}.${form.birth_month}.${form.birth_year}`;
      const birth_time = `${form.birth_hour}:${form.birth_minute}`;
      const payload = {
        name: form.name,
        birth_date,
        birth_time,
        birth_city: form.birth_city,
      };
      const res = await fetch((import.meta.env.VITE_API_URL || '') + '/api/natal-chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (data.error) {
        alert(data.error);
      } else {
        navigate('/result', { state: { chartData: data, formData: { ...form, birth_date, birth_time } } });
      }
    } catch (err) {
      alert('Bir hata oluştu. Lütfen tekrar dene.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="home-header">
        <img src={logo} alt="logo" className="home-logo" />
        <div className="home-header-text">
          <h1>Astro Magic</h1>
          <p className="subtitle">Doğum haritanı keşfet</p>
        </div>
      </div>

      <form id="chartForm" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Ad Soyad</label>
          <input
            type="text"
            id="name"
            placeholder="Adın Soyadın"
            required
            value={form.name}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Doğum Tarihi</label>
          <div className="date-row">
            <select id="birth_day" required value={form.birth_day} onChange={handleChange}>
              <option value="">Gün</option>
              {days.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
            <select id="birth_month" required value={form.birth_month} onChange={handleChange}>
              <option value="">Ay</option>
              {MONTHS.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
            </select>
            <select id="birth_year" required value={form.birth_year} onChange={handleChange}>
              <option value="">Yıl</option>
              {years.map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Doğum Saati</label>
          <div className="time-row">
            <select id="birth_hour" required value={form.birth_hour} onChange={handleChange}>
              <option value="">Saat</option>
              {hours.map(h => <option key={h} value={h}>{h}</option>)}
            </select>
            <span className="time-sep">:</span>
            <select id="birth_minute" required value={form.birth_minute} onChange={handleChange}>
              <option value="">Dakika</option>
              {minutes.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Doğum Yeri</label>
          <select id="birth_city" required value={form.birth_city} onChange={handleChange}>
            <option value="">Şehir seç</option>
            {CITIES.map(city => (
              <option key={city} value={cityToValue(city)}>
                {city.charAt(0).toUpperCase() + city.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" id="submitBtn" disabled={loading}>
          {loading ? 'Hesaplanıyor...' : 'Haritamı Oluştur ✨'}
        </button>
      </form>
    </div>
  );
}