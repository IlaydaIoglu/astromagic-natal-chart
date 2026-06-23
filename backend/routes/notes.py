# Astroloji özel notları için Flask Blueprint route tanımlamaları

from flask import Blueprint, request, jsonify
import sys
import os

# Üst dizini Python yoluna ekleyerek special_notes modülüne erişim sağla
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from special_notes import SpecialNotes

# Blueprint tanımı: tüm not route'ları bu blueprint altında toplanır
notes_bp = Blueprint('notes', __name__)

# SpecialNotes sınıfından tek bir örnek oluştur (uygulama genelinde paylaşılır)
sn = SpecialNotes()


@notes_bp.route('/api/special-notes', methods=['POST'])
def get_special_notes():
    """
    Gönderilen doğum haritası verisine göre eşleşen tüm özel notları döndürür.

    Beklenen JSON gövdesi:
        - all_positions: Gezegen pozisyonları sözlüğü
        - houses: Ev cusps sözlüğü

    Döndürür:
        JSON: { count: int, notes: list }
    """
    try:
        # İstek gövdesinden doğum haritası verisini al
        chart_data = request.get_json()
        if not chart_data:
            return jsonify({'error': 'Chart verisi eksik'}), 400

        # Koşullarla eşleşen notları hesapla
        matches = sn.evaluate_notes(chart_data)

        # Eşleşen not sayısı ve not listesini döndür
        return jsonify({
            'count': len(matches),
            'notes': matches
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notes_bp.route('/api/random-note', methods=['POST'])
def get_random_note():
    """
    Gönderilen doğum haritası verisine göre eşleşen notlardan rastgele birini döndürür.

    Beklenen JSON gövdesi:
        - all_positions: Gezegen pozisyonları sözlüğü
        - houses: Ev cusps sözlüğü

    Döndürür:
        JSON: Tek bir not nesnesi
    """
    import random
    try:
        # İstek gövdesinden doğum haritası verisini al
        chart_data = request.get_json()
        if not chart_data:
            return jsonify({'error': 'Chart verisi eksik'}), 400

        # Koşullarla eşleşen notları hesapla
        matches = sn.evaluate_notes(chart_data)

        # Hiç eşleşme yoksa 404 döndür
        if not matches:
            return jsonify({'error': 'Eşleşen not bulunamadı'}), 404

        # Eşleşen notlardan rastgele birini seç ve döndür
        note = random.choice(matches)
        return jsonify(note)
    except Exception as e:
        return jsonify({'error': str(e)}), 500