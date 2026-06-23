# Doğum haritası hesaplama route'ları için Flask Blueprint
# /api/natal-chart endpoint'i burada tanımlanır.

from flask import Blueprint, request, jsonify
import sys
import os

# Üst dizini Python yoluna ekle - natal_chart modülüne erişim için
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from natal_chart import NatalChart

chart_bp = Blueprint('chart', __name__)

# NatalChart örneği: uygulama genelinde tek seferde oluşturulur
nc = NatalChart()


@chart_bp.route('/api/natal-chart', methods=['POST'])
def get_natal_chart():
    """
    Doğum tarihi, saati ve şehrine göre natal harita hesaplar.

    Beklenen JSON gövdesi:
        - birth_date: "dd.mm.yyyy" formatında doğum tarihi
        - birth_time: "HH:MM" formatında doğum saati
        - birth_city: Doğum şehri adı
        - name (opsiyonel): Kullanıcı adı soyadı

    Döndürür:
        JSON: { all_positions, houses, coordinates, julian_day }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Veri eksik'}), 400

        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        birth_city = data.get('birth_city')

        if not all([birth_date, birth_time, birth_city]):
            return jsonify({'error': 'Doğum tarihi, saati ve şehri gerekli'}), 400

        result = nc.generate_natal_chart(birth_date, birth_time, birth_city)

        if not result:
            return jsonify({'error': 'Harita hesaplanamadı'}), 500

        # Sadece gerekli alanları döndür (longitude, degree, sign, sign_num)
        return jsonify({
            'all_positions': {
                k: {
                    'longitude': v['longitude'],
                    'degree': v['degree'],
                    'sign': v['sign'],
                    'sign_num': v['sign_num'],
                    'retrograde': v.get('retrograde', False)
                }
                for k, v in result['all_positions'].items()
            },
            'houses': {
                k: {
                    'cusp_longitude': v['cusp_longitude'],
                    'sign': v['sign'],
                    'degree': v['degree']
                }
                for k, v in result['houses'].items()
            },
            'coordinates': result['coordinates'],
            'julian_day': result['julian_day']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
