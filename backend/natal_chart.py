#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doğum Haritası (Natal Chart) Hesaplayıcısı
Doğum tarihi, saati ve yerini girince astrolojik doğum haritasını çıkarır
"""
import matplotlib
matplotlib.use('Agg')

import swisseph as swe
import math
from datetime import datetime, timezone
import pytz
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import numpy as np
import os
import time


class NatalChart:
    # Rate limiting için son istek zamanı
    _last_api_request = 0
    
    def __init__(self):
        # Swiss Ephemeris dosya yolu - asteroidler için gerekli
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ephe_path = os.path.join(script_dir, 'ephe')
        if os.path.exists(ephe_path):
            swe.set_ephe_path(ephe_path)
        else:
            swe.set_ephe_path('')  # Varsayılan yol
        
        # Gezegen isimleri
        self.planets = {
            swe.SUN: "Güneş ☉",
            swe.MOON: "Ay ☽", 
            swe.MERCURY: "Merkür ☿",
            swe.VENUS: "Venüs ♀",
            swe.MARS: "Mars ♂",
            swe.JUPITER: "Jüpiter ♃",
            swe.SATURN: "Satürn ♄",
            swe.URANUS: "Uranüs ♅",
            swe.NEPTUNE: "Neptün ♆",
            swe.PLUTO: "Plüton ♇"
        }
        
        # Ek astrolojik noktalar (sadece mevcut dosyalarla hesaplanabilir olanlar)
        self.asteroids = {
            swe.TRUE_NODE: "Kuzey Node ☊"  # TRUE_NODE: gerçek pozisyon (çoğu site bunu kullanır)
        }
        
        # Chiron ve diğer asteroidler
        self.optional_points = {
            swe.CHIRON: "Chiron ⚷",
            swe.CERES: "Ceres ⚳",
            swe.PALLAS: "Pallas ⚴",
            swe.JUNO: "Juno ⚵",
            swe.VESTA: "Vesta ⚶"
        }
        
        # Hesaplanacak özel noktalar
        self.calculated_points = {
            'south_node': "Güney Node ☋",
            'lilith': "Lilith ⚸",
            'part_fortune': "Sans Noktası ⊕",
            'vertex': "Vertex Vx"
        }
        
        # Burç isimleri
        self.signs = [
            "Koç ♈", "Boğa ♉", "İkizler ♊", "Yengeç ♋",
            "Aslan ♌", "Başak ♍", "Terazi ♎", "Akrep ♏",
            "Yay ♐", "Oğlak ♑", "Kova ♒", "Balık ♓"
        ]
        
        # Ev isimleri
        self.houses = [
            "1. Ev (Kişilik)", "2. Ev (Değerler)", "3. Ev (İletişim)", "4. Ev (Ev/Aile)",
            "5. Ev (Yaratıcılık)", "6. Ev (Sağlık/İş)", "7. Ev (İlişkiler)", "8. Ev (Dönüşüm)",
            "9. Ev (Felsefe)", "10. Ev (Kariyer)", "11. Ev (Arkadaşlık)", "12. Ev (Bilinçaltı)"
        ]

    def get_coordinates(self, city_name):
        """Şehir isminden koordinat bulma"""
        # Türkiye'nin 81 ili için offline koordinatlar
        turkish_cities = {
            # A
            'adana': (37.0000, 35.3213),
            'adiyaman': (37.7648, 38.2786),
            'afyon': (38.7507, 30.5567),
            'afyonkarahisar': (38.7507, 30.5567),
            'agri': (39.7191, 43.0503),
            'aksaray': (38.3687, 34.0370),
            'amasya': (40.6499, 35.8353),
            'ankara': (39.9334, 32.8597),
            'antalya': (36.8969, 30.7133),
            'ardahan': (41.1105, 42.7022),
            'artvin': (41.1828, 41.8183),
            'aydin': (37.8560, 27.8416),
            # B
            'balikesir': (39.6484, 27.8826),
            'bartin': (41.6344, 32.3375),
            'batman': (37.8812, 41.1351),
            'bayburt': (40.2552, 40.2249),
            'bilecik': (40.0567, 30.0665),
            'bingol': (38.8854, 40.4966),
            'bitlis': (38.4004, 42.1095),
            'bolu': (40.7392, 31.6089),
            'burdur': (37.7203, 30.2906),
            'bursa': (40.1826, 29.0665),
            # C-Ç
            'canakkale': (40.1553, 26.4142),
            'cankiri': (40.6013, 33.6134),
            'corum': (40.5506, 34.9556),
            # D
            'denizli': (37.7765, 29.0864),
            'diyarbakir': (37.9144, 40.2306),
            'duzce': (40.8438, 31.1565),
            # E
            'edirne': (41.6818, 26.5623),
            'elazig': (38.6810, 39.2264),
            'erzincan': (39.7500, 39.5000),
            'erzurum': (39.9000, 41.2700),
            'eskisehir': (39.7667, 30.5256),
            # G
            'gaziantep': (37.0662, 37.3833),
            'giresun': (40.9128, 38.3895),
            'gumushane': (40.4386, 39.5086),
            # H
            'hakkari': (37.5833, 43.7333),
            'hatay': (36.4018, 36.3498),
            # I-İ
            'igdir': (39.9167, 44.0333),
            'isparta': (37.7648, 30.5566),
            'istanbul': (41.0082, 28.9784),
            'izmir': (38.4192, 27.1287),
            # K
            'kahramanmaras': (37.5858, 36.9371),
            'karabuk': (41.2061, 32.6204),
            'karaman': (37.1759, 33.2287),
            'kars': (40.6167, 43.1000),
            'kastamonu': (41.3887, 33.7827),
            'kayseri': (38.7312, 35.4787),
            'kilis': (36.7184, 37.1212),
            'kirikkale': (39.8468, 33.5153),
            'kirklareli': (41.7333, 27.2167),
            'kirsehir': (39.1425, 34.1709),
            'kocaeli': (40.8533, 29.8815),
            'konya': (37.8667, 32.4833),
            'kutahya': (39.4167, 29.9833),
            # M
            'malatya': (38.3552, 38.3095),
            'manisa': (38.6191, 27.4289),
            'mardin': (37.3212, 40.7245),
            'mersin': (36.8000, 34.6333),
            'mugla': (37.2153, 28.3636),
            'mus': (38.9462, 41.7539),
            # N
            'nevsehir': (38.6244, 34.7239),
            'nigde': (37.9667, 34.6833),
            # O-Ö
            'ordu': (40.9839, 37.8764),
            'osmaniye': (37.0742, 36.2478),
            # R
            'rize': (41.0201, 40.5234),
            # S-Ş
            'sakarya': (40.6940, 30.4358),
            'samsun': (41.2867, 36.3300),
            'sanliurfa': (37.1591, 38.7969),
            'urfa': (37.1591, 38.7969),
            'siirt': (37.9333, 41.9500),
            'sinop': (42.0231, 35.1531),
            'sirnak': (37.5164, 42.4611),
            'sivas': (39.7477, 37.0179),
            # T
            'tekirdag': (40.9833, 27.5167),
            'tokat': (40.3167, 36.5500),
            'trabzon': (41.0015, 39.7178),
            'tunceli': (39.1079, 39.5401),
            # U-Ü
            'usak': (38.6823, 29.4082),
            # V
            'van': (38.4891, 43.4089),
            # Y
            'yalova': (40.6500, 29.2667),
            'yozgat': (39.8181, 34.8147),
            # Z
            'zonguldak': (41.4564, 31.7987),
        }
        
        # Şehir adını normalize et
        city_normalized = city_name.lower().strip()
        city_normalized = city_normalized.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u')
        city_normalized = city_normalized.replace('ş', 's').replace('ç', 'c').replace('ö', 'o')
        
        # Önce offline listeden bul
        if city_normalized in turkish_cities:
            lat, lon = turkish_cities[city_normalized]
            return lat, lon
        
        # Online arama dene (rate limiting ile)
        try:
            # Rate limiting: En az 1 saniye bekle (offline'da bulunmazsa)
            elapsed = time.time() - NatalChart._last_api_request
            if elapsed < 1.0:
                wait_time = 1.0 - elapsed
                print(f"⏳ Rate limiting: {wait_time:.2f} saniye bekleniyor...")
                time.sleep(wait_time)
            
            NatalChart._last_api_request = time.time()
            
            geolocator = Nominatim(user_agent="natal_chart", timeout=5)
            
            # Önce girilen isimle dene
            location = geolocator.geocode(city_name, timeout=5)
            
            # Bulunamazsa Türkiye ekleyerek dene
            if not location and 'turkey' not in city_name.lower() and 'türkiye' not in city_name.lower():
                location = geolocator.geocode(f"{city_name}, Turkey", timeout=5)
            
            if location:
                return location.latitude, location.longitude
            else:
                print(f"'{city_name}' şehri bulunamadı! Varsayılan İstanbul koordinatları kullanılıyor.")
                return turkish_cities['istanbul']  # Varsayılan İstanbul
        except Exception as e:
            print(f"Koordinat bulma hatası: {e}. Varsayılan İstanbul koordinatları kullanılıyor.")
            return turkish_cities['istanbul']  # Varsayılan İstanbul

    def get_julian_day(self, birth_date, birth_time, timezone_str):
        """Doğum tarih/saatini Julian Day'e çevirme"""
        try:
            # Timezone'u ayarla
            tz = pytz.timezone(timezone_str)
            
            # Tarih ve saat string'ini parse et - farklı formatları dene
            datetime_str = f"{birth_date} {birth_time}"
            
            # Farklı tarih formatlarını dene
            for date_format in ["%d.%m.%Y %H:%M", "%Y-%m-%d %H:%M", "%Y %m %d %H:%M", "%d/%m/%Y %H:%M"]:
                try:
                    dt = datetime.strptime(datetime_str, date_format)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Tarih formatı tanınmadı: {datetime_str}")
            
            # Timezone bilgisi ekle
            dt_with_tz = tz.localize(dt)
            
            # UTC'ye çevir
            dt_utc = dt_with_tz.astimezone(pytz.UTC)
            
            # Julian Day hesapla
            jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                           dt_utc.hour + dt_utc.minute/60.0)
            
            return jd
        except Exception as e:
            print(f"Tarih dönüşüm hatası: {e}")
            return None

    def calculate_planets(self, jd):
        """Gezegen ve asteroid pozisyonlarını hesapla"""
        planet_positions = {}
        
        # Ana gezegenler
        for planet_id, planet_name in self.planets.items():
            try:
                result = swe.calc_ut(jd, planet_id)
                longitude = result[0][0]
                speed = result[0][3]  # Hız bilgisi — negatifse retrograd
                
                sign_num = int(longitude / 30)
                degree_in_sign = longitude % 30
                
                planet_positions[planet_name] = {
                    'longitude': longitude,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign,
                    'sign_num': sign_num,
                    'retrograde': speed < 0
                }
            except Exception as e:
                print(f"{planet_name} hesaplama hatası: {e}")
        
        # Temel ek noktalar (Mean Node gibi)
        for asteroid_id, asteroid_name in self.asteroids.items():
            try:
                result = swe.calc_ut(jd, asteroid_id)
                longitude = result[0][0]
                sign_num = int(longitude / 30)
                degree_in_sign = longitude % 30
                
                planet_positions[asteroid_name] = {
                    'longitude': longitude,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign,
                    'sign_num': sign_num
                }
            except Exception as e:
                pass  # Sessizce atla
        
        # Opsiyonel noktalar (Chiron gibi - varsa ekle, yoksa atla)
        for point_id, point_name in self.optional_points.items():
            try:
                result = swe.calc_ut(jd, point_id)
                longitude = result[0][0]
                sign_num = int(longitude / 30)
                degree_in_sign = longitude % 30
                
                planet_positions[point_name] = {
                    'longitude': longitude,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign,
                    'sign_num': sign_num
                }
            except Exception as e:
                # Chiron hesaplanamadı, sessizce devam et
                pass
        
        # Özel hesaplanmış noktalar
        try:
            # Güney Node (Kuzey Node'un karşısı)
            if "Kuzey Node ☊" in planet_positions:
                north_node_long = planet_positions["Kuzey Node ☊"]['longitude']
                south_node_long = (north_node_long + 180) % 360
                sign_num = int(south_node_long / 30)
                degree_in_sign = south_node_long % 30
                
                planet_positions["Güney Node ☋"] = {
                    'longitude': south_node_long,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign,
                    'sign_num': sign_num
                }
            
            # Lilith (Mean Apogee)
            result = swe.calc_ut(jd, swe.MEAN_APOG)
            longitude = result[0][0]
            sign_num = int(longitude / 30)
            degree_in_sign = longitude % 30
            
            planet_positions["Lilith ⚸"] = {
                'longitude': longitude,
                'sign': self.signs[sign_num],
                'degree': degree_in_sign,
                'sign_num': sign_num
            }
            
        except Exception as e:
            print(f"Özel noktalar hesaplama hatası: {e}")
                
        return planet_positions
    
    def calculate_special_points(self, jd, latitude, longitude, planet_positions, house_info):
        """Özel astrolojik noktaları hesapla (Part of Fortune, Vertex)"""
        special_points = {}
        
        try:
            # Part of Fortune hesaplama
            # Gündüz doğum: ASC + Ay - Güneş
            # Gece doğum: ASC + Güneş - Ay
            if 'Güneş ☉' in planet_positions and 'Ay ☽' in planet_positions and 'Yükselen (ASC)' in house_info:
                sun_long = planet_positions['Güneş ☉']['longitude']
                moon_long = planet_positions['Ay ☽']['longitude']
                asc_long = house_info['Yükselen (ASC)']['cusp_longitude']
                
                # Gündüz mü gece mi kontrolü (Güneş 7-12. evlerde ise gündüz)
                houses_list = swe.houses(jd, latitude, longitude, b'P')
                sun_house = self._find_house(sun_long, houses_list[0])
                
                if sun_house >= 7:  # Gündüz doğum
                    pof_long = (asc_long + moon_long - sun_long) % 360
                else:  # Gece doğum
                    pof_long = (asc_long + sun_long - moon_long) % 360
                
                sign_num = int(pof_long / 30)
                degree_in_sign = pof_long % 30
                
                special_points['Şans Noktası ⊕'] = {
                    'longitude': pof_long,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign,
                    'sign_num': sign_num
                }
            
            # Vertex hesaplama (houses[1][3] = Vertex)
            houses_list = swe.houses(jd, latitude, longitude, b'P')
            vertex_long = houses_list[1][3]  # Vertex pozisyonu
            sign_num = int(vertex_long / 30)
            degree_in_sign = vertex_long % 30
            
            special_points['Vertex Vx'] = {
                'longitude': vertex_long,
                'sign': self.signs[sign_num],
                'degree': degree_in_sign,
                'sign_num': sign_num
            }
                
        except Exception as e:
            print(f"Özel noktalar hesaplama hatası: {e}")
        
        return special_points
    
    def save_detailed_report(self, full_name, birth_date, birth_time, birth_city, chart_data, filename):
        """Detaylı astrolojik raporu dosyaya kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Başlık
                f.write("=" * 60 + "\n")
                f.write(f"         {full_name.upper()} - DOĞUM HARITASİ\n")
                f.write("=" * 60 + "\n\n")
                
                # Kişisel bilgiler
                f.write("📝 KİŞİSEL BİLGİLER:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Ad Soyad      : {full_name}\n")
                f.write(f"Doğum Tarihi  : {birth_date}\n")
                f.write(f"Doğum Saati   : {birth_time}\n")
                f.write(f"Doğum Yeri    : {birth_city}\n")
                
                coords = chart_data['coordinates']
                f.write(f"Koordinatlar  : {coords[0]:.2f}°K, {coords[1]:.2f}°D\n")
                f.write(f"Julian Day    : {chart_data['julian_day']:.6f}\n\n")
                
                # Gezegen pozisyonları
                f.write("🪐 GEZEGEN VE ASTEROID POZİSYONLARI:\n")
                f.write("-" * 50 + "\n")
                
                all_pos = chart_data['all_positions']
                for planet_name, data in all_pos.items():
                    f.write(f"{planet_name:<20} {data['sign']:<12} {int(data['degree']):>3}°\n")
                
                f.write("\n")
                
                # Ev sistemi
                f.write("🏠 EV SİSTEMİ (Placidus):\n")
                f.write("-" * 50 + "\n")
                
                houses = chart_data['houses']
                for house_name, data in houses.items():
                    f.write(f"{house_name:<18} {data['sign']:<12} {int(data['degree']):>3}°\n")
                
                f.write("\n")
                
                # Astrolojik yorumlar (basit)
                f.write("✨ TEMEL ASTROLOJİK YORUMLAR:\n")
                f.write("-" * 50 + "\n")
                
                # Güneş burcu
                sun_sign = all_pos.get('Güneş ☉', {}).get('sign', 'Bilinmiyor')
                f.write(f"Güneş Burcu: {sun_sign}\n")
                f.write("  - Temel kişilik özelliklerin ve ego yapın\n\n")
                
                # Ay burcu
                moon_sign = all_pos.get('Ay ☽', {}).get('sign', 'Bilinmiyor')
                f.write(f"Ay Burcu: {moon_sign}\n")
                f.write("  - Duygusal yapın ve iç dünyan\n\n")
                
                # Yükselen
                asc_sign = houses.get('Yükselen (ASC)', {}).get('sign', 'Bilinmiyor')
                f.write(f"Yükselen: {asc_sign}\n")
                f.write("  - Dış görünümün ve ilk izlenim\n\n")
                
                # Önemli aspectler (basit)
                f.write("🔍 ÖNEMLİ ASTROLOJİK NOKTALAR:\n")
                f.write("-" * 50 + "\n")
                
                # Kuzey Node
                if 'Kuzey Node ☊' in all_pos:
                    nn_sign = all_pos['Kuzey Node ☊']['sign']
                    f.write(f"Kuzey Node ({nn_sign}): Ruhsal gelişim yönü\n")
                
                # Lilith
                if 'Lilith ⚸' in all_pos:
                    lilith_sign = all_pos['Lilith ⚸']['sign']
                    f.write(f"Lilith ({lilith_sign}): Bastırılmış feminine enerji\n")
                
                # Part of Fortune
                if 'Şans Noktası ⊕' in all_pos:
                    pof_sign = all_pos['Şans Noktası ⊕']['sign']
                    f.write(f"Şans Noktası ({pof_sign}): Maddi ve manevi başarı alanı\n")
                
                f.write("\n")
                f.write("=" * 60 + "\n")
                f.write("Bu rapor otomatik olarak oluşturulmuştur.\n")
                f.write(f"Oluşturma tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write("=" * 60 + "\n")
                
        except Exception as e:
            print(f"Rapor kaydetme hatası: {e}")
    
    def create_readme_file(self, full_name, birth_date, birth_time, birth_city, filename):
        """Klasör için README dosyası oluştur"""
        try:
            safe_name = "".join(c for c in full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{full_name} - Doğum Haritası Dosyaları\n")
                f.write("=" * 50 + "\n\n")
                f.write("Bu klasörde şu dosyalar bulunmaktadır:\n\n")
                f.write(f"📊 {safe_name}_natal_chart.png\n")
                f.write("   → Doğum haritası görsel grafiği\n\n")
                f.write(f"📄 {safe_name}_natal_report.txt\n")
                f.write("   → Detaylı astrolojik analiz raporu\n\n")
                f.write(f"📝 README.txt\n")
                f.write("   → Bu açıklama dosyası\n\n")
                f.write("Kişi Bilgileri:\n")
                f.write(f"• Ad Soyad: {full_name}\n")
                f.write(f"• Doğum Tarihi: {birth_date}\n")
                f.write(f"• Doğum Saati: {birth_time}\n")
                f.write(f"• Doğum Yeri: {birth_city}\n\n")
                f.write(f"Oluşturma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write("\nNot: Bu dosyalar otomatik doğum haritası programı ile oluşturulmuştur.\n")
        except Exception as e:
            print(f"README kaydetme hatası: {e}")
    
    def _find_house(self, longitude, house_cusps):
        """Bir boylamın hangi evde olduğunu bul"""
        for i in range(12):
            next_house = (i + 1) % 12
            if house_cusps[i] <= longitude < house_cusps[next_house]:
                return i + 1
        return 1  # Varsayılan

    def calculate_houses(self, jd, latitude, longitude):
        """Ev sistemini hesapla (Placidus)"""
        try:
            # Ev cusps'larını hesapla
            houses = swe.houses(jd, latitude, longitude, b'P')  # 'P' = Placidus
            house_cusps = houses[0]  # İlk 12 ev cusp'u
            ascendant = houses[1][0]  # Yükselen (ASC)
            mc = houses[1][1]  # Orta Gökyüzü (MC)
            
            house_info = {}
            for i, cusp in enumerate(house_cusps[:12]):
                sign_num = int(cusp / 30)
                degree_in_sign = cusp % 30
                
                house_info[f"{i+1}. Ev"] = {
                    'cusp_longitude': cusp,
                    'sign': self.signs[sign_num],
                    'degree': degree_in_sign
                }
            
            # Özel noktalar
            house_info['Yükselen (ASC)'] = {
                'cusp_longitude': ascendant,
                'sign': self.signs[int(ascendant / 30)],
                'degree': ascendant % 30
            }
            
            house_info['Orta Gökyüzü (MC)'] = {
                'cusp_longitude': mc,
                'sign': self.signs[int(mc / 30)],
                'degree': mc % 30
            }
            
            return house_info
            
        except Exception as e:
            print(f"Ev hesaplama hatası: {e}")
            return {}

    def create_chart_wheel(self, all_positions, house_info):
        """Doğum haritası tekerleğini çiz - Astrolojik standart format"""
        fig, ax = plt.subplots(figsize=(14, 14))
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # ASC pozisyonunu al (1. Ev başlangıcı)
        asc_longitude = house_info.get('Yükselen (ASC)', {}).get('cusp_longitude', 0)
        
        # Dış çemberler (burçlar için)
        circle_outer = plt.Circle((0, 0), 1.1, fill=False, linewidth=2.5, color='#2c3e50')
        ax.add_patch(circle_outer)
        
        circle_zodiac_inner = plt.Circle((0, 0), 0.95, fill=False, linewidth=1.5, color='#34495e')
        ax.add_patch(circle_zodiac_inner)
        
        # İç çemberler (evler için)
        circle_houses_outer = plt.Circle((0, 0), 0.85, fill=False, linewidth=2, color='#3498db')
        ax.add_patch(circle_houses_outer)
        
        circle_houses_inner = plt.Circle((0, 0), 0.3, fill=False, linewidth=1, color='#95a5a6')
        ax.add_patch(circle_houses_inner)
        
        # Merkez noktası
        ax.plot(0, 0, 'ko', markersize=3)
        
        # BURÇ ÇİZGİLERİ VE İSİMLERİ
        # Burçlar da ASC'ye göre yerleştirilmeli
        zodiac_symbols = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
        zodiac_names = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", 
                       "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
        
        for i in range(12):
            # Burç başlangıç boylamı (0° = Koç başlangıcı)
            zodiac_longitude = i * 30
            
            # ASC'ye göre harita üzerindeki açı
            # ASC solda (180°), evler saat yönünde
            zodiac_angle = 180 + (zodiac_longitude - asc_longitude)
            zodiac_angle_rad = math.radians(zodiac_angle)
            
            # Burç ayırıcı çizgiler
            x1 = 0.95 * math.cos(zodiac_angle_rad)
            y1 = 0.95 * math.sin(zodiac_angle_rad)
            x2 = 1.1 * math.cos(zodiac_angle_rad)
            y2 = 1.1 * math.sin(zodiac_angle_rad)
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.7)
            
            # Burç sembolü ve ismi (burçların ortasında)
            next_zodiac_angle = 180 + ((i+1) * 30 - asc_longitude)
            mid_zodiac_angle = (zodiac_angle + next_zodiac_angle) / 2
            mid_zodiac_angle_rad = math.radians(mid_zodiac_angle)
            
            text_x = 1.025 * math.cos(mid_zodiac_angle_rad)
            text_y = 1.025 * math.sin(mid_zodiac_angle_rad)
            
            ax.text(text_x, text_y, f"{zodiac_symbols[i]}\n{zodiac_names[i]}", 
                   ha='center', va='center', fontsize=9, fontweight='bold', color='#8e44ad')
        
        # EV ÇİZGİLERİ VE NUMARALARI
        # 1. Ev = ASC, solda başlar (180° pozisyonunda)
        # Evler SAAT YÖNÜNde gider (1→2→3... yukarı doğru)
        
        for i in range(1, 13):
            if f"{i}. Ev" in house_info:
                house_cusp_longitude = house_info[f"{i}. Ev"]['cusp_longitude']
                
                # ASC'den itibaren evleri hesapla
                # 1. Ev solda (180°), sonra saat yönünde (2.ev sol üst, 3.ev üst...)
                house_angle = 180 + (house_cusp_longitude - asc_longitude)
                house_angle_rad = math.radians(house_angle)
                
                # Ev çizgisi (merkezden dış halka içine)
                x1, y1 = 0, 0
                x2 = 0.85 * math.cos(house_angle_rad)
                y2 = 0.85 * math.sin(house_angle_rad)
                ax.plot([x1, x2], [y1, y2], color='#3498db', linewidth=1.5, alpha=0.8)
                
                # Ev numarası
                label_x = 0.6 * math.cos(house_angle_rad)
                label_y = 0.6 * math.sin(house_angle_rad)
                ax.text(label_x, label_y, str(i), 
                       ha='center', va='center', fontsize=11, 
                       fontweight='bold', color='#2980b9',
                       bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='none', alpha=0.7))
                
                # Sonraki ev ile arasındaki bölgeye derece bilgisi
                if i < 12:
                    next_house_cusp = house_info[f"{i+1}. Ev"]['cusp_longitude']
                else:
                    next_house_cusp = house_info["1. Ev"]['cusp_longitude']
                
                next_house_angle = 180 + (next_house_cusp - asc_longitude)
                mid_angle = (house_angle + next_house_angle) / 2
                mid_angle_rad = math.radians(mid_angle)
                
                sign_num = int(house_cusp_longitude / 30)
                degree_in_sign = house_cusp_longitude % 30
                
                mid_x = 0.75 * math.cos(mid_angle_rad)
                mid_y = 0.75 * math.sin(mid_angle_rad)
                
                ax.text(mid_x, mid_y, f"{zodiac_symbols[sign_num]}\n{degree_in_sign:.0f}°", 
                       ha='center', va='center', fontsize=7, color='#7f8c8d', alpha=0.8)
        
        # GEZEGENLER VE ÖZEL NOKTALAR
        planet_colors = {
            'Güneş': '#f39c12', 'Ay': '#95a5a6', 'Merkür': '#f1c40f', 
            'Venüs': '#e91e63', 'Mars': '#e74c3c', 'Jüpiter': '#9b59b6',
            'Satürn': '#34495e', 'Uranüs': '#16a085', 'Neptün': '#3498db',
            'Plüton': '#8e44ad', 'Kuzey': '#27ae60', 'Güney': '#27ae60',
            'Lilith': '#c0392b', 'Şans': '#f39c12', 'Chiron': '#d35400'
        }
        
        planet_symbols = {
            'Güneş': '☉', 'Ay': '☽', 'Merkür': '☿', 'Venüs': '♀', 'Mars': '♂',
            'Jüpiter': '♃', 'Satürn': '♄', 'Uranüs': '♅', 'Neptün': '♆', 'Plüton': '♇',
            'Kuzey': '☊', 'Güney': '☋', 'Lilith': '⚸', 'Şans': '⊕', 'Chiron': '⚷'
        }
        
        for planet_name, planet_data in all_positions.items():
            planet_longitude = planet_data['longitude']
            
            # Gezegenin harita üzerindeki açısını hesapla
            # ASC solda (180°), saat yönünde
            planet_angle = 180 + (planet_longitude - asc_longitude)
            planet_angle_rad = math.radians(planet_angle)
            
            # Gezegen pozisyonu (evler bölgesinde)
            radius = 0.72
            x = radius * math.cos(planet_angle_rad)
            y = radius * math.sin(planet_angle_rad)
            
            # Renk seçimi
            color = '#2c3e50'
            for key, col in planet_colors.items():
                if key in planet_name:
                    color = col
                    break
            
            # Gezegen sembolü
            symbol = '●'
            for key, sym in planet_symbols.items():
                if key in planet_name:
                    symbol = sym
                    break
            
            # Gezegeni çiz
            ax.plot(x, y, 'o', markersize=10, color=color, markeredgecolor='white', markeredgewidth=0.5)
            
            # Gezegen ismini ve derecesini yaz
            planet_name_short = planet_name.split()[0]  # İlk kelime (Güneş, Ay, vs.)
            degree_text = f"{planet_data['degree']:.0f}°"
            sign_symbol = self.signs[planet_data['sign_num']].split()[-1]  # Sadece sembol
            
            # Metin pozisyonu (gezegenden biraz dışarıda)
            text_offset = 0.1
            text_x = x + text_offset * math.cos(planet_angle_rad)
            text_y = y + text_offset * math.sin(planet_angle_rad)
            
            ax.text(text_x, text_y, f"{symbol}\n{planet_name_short}\n{degree_text}", 
                   ha='center', va='center', fontsize=10, color=color, fontweight='bold')
        
        # Başlık
        plt.title("Doğum Haritası (Natal Chart)", fontsize=18, fontweight='bold', pad=20, color='#2c3e50')
        
        return fig
    
    def create_table_chart(self, all_positions, house_info):
        """Grid tablo formatında doğum haritası - görseldeki gibi detaylı"""
        fig = plt.figure(figsize=(20, 12))
        
        # Sol taraf: Açılar tablosu (Aspects Grid)
        ax_grid = fig.add_subplot(1, 3, 1)
        ax_grid.set_xlim(0, 13)
        ax_grid.set_ylim(0, 13)
        ax_grid.set_aspect('equal')
        ax_grid.axis('off')
        
        # Gezegen sembolleri ve renkleri
        planet_symbols = {
            'Güneş': ('☉', '#FF6B00'), 'Ay': ('☽', '#808080'), 'Merkür': ('☿', '#00CED1'),
            'Venüs': ('♀', '#FF1493'), 'Mars': ('♂', '#FF0000'), 'Jüpiter': ('♃', '#FF8C00'),
            'Satürn': ('♄', '#8B4513'), 'Uranüs': ('♅', '#00CED1'), 'Neptün': ('♆', '#4169E1'),
            'Plüton': ('♇', '#8B008B'), 'Kuzey': ('☊', '#32CD32'), 'Güney': ('☋', '#32CD32'),
            'Chiron': ('⚷', '#FF4500'), 'Lilith': ('⚸', '#DC143C')
        }
        
        # Aspect sembolleri ve açıları
        aspect_info = {
            'conjunction': ('☌', 0, '#000000'),
            'sextile': ('⚹', 60, '#0000FF'),
            'square': ('□', 90, '#FF00FF'),
            'trine': ('△', 120, '#00FF00'),
            'opposition': ('☍', 180, '#FF0000')
        }
        
        # Grid çizgileri (13x13)
        for i in range(14):
            ax_grid.plot([i, i], [0, 13], 'k-', linewidth=0.5)
            ax_grid.plot([0, 13], [i, i], 'k-', linewidth=0.5)
        
        # Gezegen listesi (sol ve üst kenarda)
        planet_list = list(all_positions.keys())[:13]  # Maksimum 13 gezegen
        
        for idx, planet_name in enumerate(planet_list):
            symbol = '●'
            color = '#000000'
            for key, (sym, col) in planet_symbols.items():
                if key in planet_name:
                    symbol = sym
                    color = col
                    break
            
            # Sol kenarda (y ekseninde)
            ax_grid.text(0.5, 12.5 - idx, symbol, fontsize=14, color=color, ha='center', va='center')
            
            # Üst kenarda (x ekseninde)
            ax_grid.text(idx + 1.5, 12.5, symbol, fontsize=14, color=color, ha='center', va='center')
        
        # Aspectleri hesapla ve grid'e yerleştir
        orb = 8  # Orb toleransı
        for i, planet1_name in enumerate(planet_list):
            planet1_long = all_positions[planet1_name]['longitude']
            
            for j, planet2_name in enumerate(planet_list):
                if j >= i:  # Sadece alt üçgen
                    continue
                    
                planet2_long = all_positions[planet2_name]['longitude']
                
                # Açı farkı hesapla
                diff = abs(planet1_long - planet2_long)
                if diff > 180:
                    diff = 360 - diff
                
                # Aspect kontrolü
                for aspect_name, (aspect_symbol, aspect_angle, aspect_color) in aspect_info.items():
                    if abs(diff - aspect_angle) <= orb:
                        grid_x = j + 1.5
                        grid_y = 12.5 - i
                        ax_grid.text(grid_x, grid_y, aspect_symbol, 
                                   fontsize=10, color=aspect_color, ha='center', va='center')
                        break
        
        # Orta: Açı göstergeleri (Legend)
        ax_legend = fig.add_subplot(1, 3, 2)
        ax_legend.set_xlim(0, 1)
        ax_legend.set_ylim(0, 1)
        ax_legend.axis('off')
        
        y_pos = 0.9
        ax_legend.text(0.5, y_pos, 'Açılar', fontsize=14, fontweight='bold', ha='center')
        y_pos -= 0.1
        
        for aspect_name, (aspect_symbol, aspect_angle, aspect_color) in aspect_info.items():
            ax_legend.text(0.1, y_pos, aspect_symbol, fontsize=12, color=aspect_color)
            ax_legend.text(0.3, y_pos, f"{aspect_angle}°", fontsize=10)
            
            aspect_names = {
                'conjunction': 'Kavuşum',
                'sextile': 'Sextile',
                'square': 'Kare',
                'trine': 'Üçgen',
                'opposition': 'Karşıt'
            }
            ax_legend.text(0.5, y_pos, aspect_names[aspect_name], fontsize=10)
            y_pos -= 0.08
        
        # Sağ taraf: Gezegen listesi
        ax_list = fig.add_subplot(1, 3, 3)
        ax_list.axis('off')
        
        # Başlık
        y_pos = 0.98
        ax_list.text(0.05, y_pos, 'Gezegen', fontsize=12, fontweight='bold', color='#2c3e50')
        ax_list.text(0.45, y_pos, 'Burç', fontsize=12, fontweight='bold', color='#2c3e50')
        ax_list.text(0.75, y_pos, 'Derece', fontsize=12, fontweight='bold', color='#2c3e50')
        
        y_pos -= 0.04
        
        # Burç sembolleri
        zodiac_symbols = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
        zodiac_names = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", 
                       "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
        
        for planet_name, planet_data in all_positions.items():
            symbol = '●'
            color = '#000000'
            planet_short = planet_name.split()[0]
            
            for key, (sym, col) in planet_symbols.items():
                if key in planet_name:
                    symbol = sym
                    color = col
                    break
            
            sign_num = planet_data['sign_num']
            sign_symbol = zodiac_symbols[sign_num]
            sign_name = zodiac_names[sign_num]
            
            # Derece formatı: DD°MM'SS"
            degree = planet_data['degree']
            deg = int(degree)
            minutes = int((degree - deg) * 60)
            seconds = int(((degree - deg) * 60 - minutes) * 60)
            degree_text = f"{deg:02d}°{minutes:02d}'{seconds:02d}\""
            
            ax_list.text(0.02, y_pos, symbol, fontsize=12, color=color)
            ax_list.text(0.08, y_pos, planet_short, fontsize=10, color=color)
            ax_list.text(0.42, y_pos, sign_symbol, fontsize=12, color='#8e44ad')
            ax_list.text(0.50, y_pos, sign_name, fontsize=9, color='#34495e')
            ax_list.text(0.73, y_pos, degree_text, fontsize=9, color='#2c3e50')
            
            y_pos -= 0.04
            
            if y_pos < 0.05:
                break
        
        plt.suptitle("Doğum Haritası Tablosu", fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        return fig

    def generate_natal_chart(self, birth_date, birth_time, birth_city, timezone_str='Europe/Istanbul'):
        """Ana fonksiyon: Doğum haritasını oluştur"""
        print(f"\n🌟 Doğum Haritası Hesaplanıyor...")
        print(f"📅 Doğum Tarihi: {birth_date}")
        print(f"🕐 Doğum Saati: {birth_time}")
        print(f"📍 Doğum Yeri: {birth_city}")
        print("-" * 50)
        
        # Koordinatları al
        latitude, longitude = self.get_coordinates(birth_city)
        if latitude is None:
            return None
            
        print(f"🌍 Koordinatlar: {latitude:.2f}°, {longitude:.2f}°")
        
        # Julian Day hesapla
        jd = self.get_julian_day(birth_date, birth_time, timezone_str)
        if jd is None:
            return None
            
        print(f"📊 Julian Day: {jd:.6f}")
        
        # Gezegenları hesapla
        planet_positions = self.calculate_planets(jd)
        
        # Evleri hesapla
        house_info = self.calculate_houses(jd, latitude, longitude)
        
        # Özel noktaları hesapla
        special_points = self.calculate_special_points(jd, latitude, longitude, planet_positions, house_info)
        
        # Özel noktaları ana listeye ekle
        all_positions = {**planet_positions, **special_points}
        
        # Sonuçları yazdır
        print("\n🪐 GEZEGEN VE ASTEROID POZİSYONLARI:")
        print("-" * 50)
        for planet_name, data in all_positions.items():
            print(f"{planet_name:20} {data['sign']:10} {int(data['degree']):>3}°")
        
        print("\n🏠 EV SİSTEMİ (Placidus):")
        print("-" * 50)
        for house_name, data in house_info.items():
            print(f"{house_name:15} {data['sign']:10} {int(data['degree']):>3}°")
        
        # Grafik çiz
        fig = self.create_chart_wheel(all_positions, house_info)
        
        return {
            'planets': planet_positions,
            'special_points': special_points,
            'all_positions': all_positions,
            'houses': house_info,
            'chart_figure': fig,
            'coordinates': (latitude, longitude),
            'julian_day': jd
        }

def main():
    """Test fonksiyonu"""
    chart = NatalChart()
    
    # Örnek kullanım
    print("🌟 Doğum Haritası Hesaplayıcısı")
    print("=" * 40)
    
    # Kullanıcıdan veri al
    full_name = input("İsim Soyisim: ").strip()
    birth_date = input("Doğum tarihi (DD.MM.YYYY): ").strip()
    birth_time = input("Doğum saati (HH:MM): ").strip()
    birth_city = input("Doğum yeri (şehir): ").strip()
    
    if not full_name:
        full_name = "Test Kişisi"  # Örnek isim
    if not birth_date:
        birth_date = "15.06.1990"  # Örnek tarih
    if not birth_time:
        birth_time = "14:30"  # Örnek saat
    if not birth_city:
        birth_city = "İstanbul"  # Örnek şehir
    
    # Doğum haritasını oluştur
    result = chart.generate_natal_chart(birth_date, birth_time, birth_city)
    
    if result:
        print("\n✅ Doğum haritası başarıyla hesaplandı!")
        
        # Dosya isimleri ve klasör oluştur
        safe_name = "".join(c for c in full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        # users klasörü altında kişi adına klasör oluştur
        users_folder = "users"
        person_folder = os.path.join(users_folder, safe_name)
        os.makedirs(person_folder, exist_ok=True)
        
        # Dosya yolları
        image_filename = os.path.join(person_folder, f"{safe_name}_natal_chart.png")
        report_filename = os.path.join(person_folder, f"{safe_name}_natal_report.txt")
        readme_filename = os.path.join(person_folder, "README.txt")
        
        # Grafiği kaydet
        result['chart_figure'].savefig(image_filename, dpi=300, bbox_inches='tight')
        
        # Detaylı rapor dosyası oluştur
        chart.save_detailed_report(full_name, birth_date, birth_time, birth_city, result, report_filename)
        
        # README dosyası oluştur
        chart.create_readme_file(full_name, birth_date, birth_time, birth_city, readme_filename)
        
        # Grafiği göster
        print(f"📁 Klasör '{person_folder}' oluşturuldu!")
        print(f"💾 Çark grafiği kaydedildi: {image_filename}")
        if result.get('table_figure'):
            print(f"📊 Tablo grafiği kaydedildi: {table_filename}")
        print(f"📁 Klasör '{person_folder}' oluşturuldu!")
        print(f"💾 Grafik kaydedildi: {image_filename}")
        print(f"📄 Detaylı rapor kaydedildi: {report_filename}")
        print(f"📝 README dosyası oluşturuldu!")
        print(f"\n✨ Tüm dosyalar '{person_folder}' klasörüne kaydedildi!")

if __name__ == "__main__":
    main()