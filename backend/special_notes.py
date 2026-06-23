#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kişiye özel ek notları kontrol eder ve uygun olanları kişinin klasörüne kaydeder.

Not kuralları python dict listesi olarak tutulur; eklemek için `self.notes` içine
yeni sözlük ekleyebilirsiniz. Örnek kural tipleri:

				"title": "8. Ev Gölge Teması",
				"text": "Güneş 8. evdeyse (veya 8. ev Aslan) için buraya açıklama eklenecek."
- planet_in_sign: Gezegenin bulunduğu burç.
- planet_in_house: Gezegenin bulunduğu ev.
- house_sign_is: İlgili evin burcunun belirli bir burç olması.

Her kuralda `text` alanı rapora yazılır.
"""
			
import os
from typing import Dict, List, Optional, Tuple


class SpecialNotes:
	def __init__(self):
		self.notes: List[Dict] = (
			self._eight_house_shadow_notes()
			+ self._degree_7_notes() 
			+ self._degree_28_notes()
			+ self._four_house_career_notes()
			+ self._feeling_overwhelmed_notes()
			+ self._rare_house_aspect_notes()
			+ self._degree_17_notes()
			+ self._insecurity_notes()
			+ self._shame_reasons_notes()
			+ self._universe_protection_notes()
			+ self._twins_luck_notes()
			+ self._uranus_manifesto_notes()
			+ self._childhood_notes()
			+ self._father_figure_notes()
			+ self._mother_figure_notes()
			+ self._life_teaching_notes()
			+ self._fears_notes()
			+ self._colors_abundance()
		)

	# -------------------- Yardımcılar --------------------
	def _normalize_sign(self, sign: str) -> str:
		# İlk kelimeyi (burç adını) döndürür.
		return sign.split()[0] if sign else ""

	def _normalize_planet(self, name: str) -> str:
		return name.strip()

	def _degree_7_notes(self) -> List[Dict]:
		title = "7° Kazanma Enerjisidir. Haritanızda 7° hangi gezegen yer alıyorsa o gezegenin konularında yarışmalara katılabilirsiniz"
		return [
			{   # Jüpiter 7°
				"id": "jupiter_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Jüpiter ♃",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Jüpiter 7° ise seyehat ödülü olan yarışmalara katılmanızı tavsiye ederim. Jüpiter bir eğitimle alakalı olduğu için burs kazanma şansınız artabilir."
			},
			{   # Venüs 7°
				"id": "venus_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Venüs ♀",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Venüs 7° ise maddi ödüllü yarışmaları kazanabilirsiniz. Kıyafet, takı, kozmetik ürünleri hediye eden çekilişleri de kazanabilirsiniz."
			},
			{   # Merkür 7°
				"id": "mercury_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Merkür ☿",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Merkür 7° kitap çekilişlerine, eğitim çekilişlerine katılabilirsiniz."
			},
			{   # Mars 7°   
				"id": "mars_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Mars ♂",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Mars 7° ise yarışmalara katılmanızı tavsiye ederim. Çünkü çok heyecan verici deneyimler yaşayabilirsiniz. Fiziksel dayanıklılık, spor veya kondisyon gerektiren yarışmalarda güzel bir şey kazanabilirsiniz."
			},
			{   # Şans Noktası 7°
				"id": "part_of_fortune_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Şans Noktası",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Şans Noktası 7° özellikle de Koç, Boğa, Terazi, Yay ve Balık burcundaysa yarışma ve ödül kazanma şansınız ciddi şekilde yüksek olabilir."
			},
			{   # Kuzey Ay Düğümü 7°
				"id": "north_node_at_7deg",
				"type": "planet_degree_equals",
				"planet": "Kuzey Ay Düğümü",
				"degree_min": 7.0,
				"degree_max": 7.9,
				"title": title,
				"text": "Kuzey Ay Düğümü 7° olması en iyisi. Çok büyük ödüllerin verildiği yarışmaları kazanma potansiyeliniz yüksek."
			},
		]
	def _degree_28_notes(self) -> List[Dict]:
		title = "28° 'Büyük Bir Eve Sahip Olma' Enerjisidir." 
		return [ 
			{   # Güneş 28°
				"id": "sun_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Güneş ☉",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Güneş 28° ise hayatınızın bir döneminde büyük pencereleri olan geniş bir eve sahip olabilirsiniz. Ya da eviniz gerçekten çok fazla ışık alır. Tavanda bir penceresi olabilir mesela."
			},
			{   # Ay 28°
				"id": "moon_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Ay ☽",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Ay'ınız 28° ise büyük bir mutfağa sahip olabilirsiniz. Oturma odanız da büyük olabilir."
			},
			{   # Merkür 28°
				"id": "mercury_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Merkür ☿",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Büyük bir çalışma odanız olabilir, evinizde büyük bir kitaplık olabilir. Evinizde garaj olabilir."
			},
			{   # Venüs 28°
				"id": "venus_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Venüs ♀",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Haritanızda Venüs 28° ise büyük bir dolaba sahip olabilirsiniz, yatak odanız çok geniş olabilir. Balkonda çok geniş olabilir. Eğer durumunuz el verirse evinizde Ziyagil köşkündeki gibi bir müzik odası bile olabilir :D "
			},
			{   # Mars 28°
				"id": "mars_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Mars ♂",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Mars 28° ise evinizde spor aletleri olabilir. Şömine olabilir."
			},
			{   # Jüpiter 28°
				"id": "jupiter_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Jüpiter ♃",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Jüpiter 28° ise başka bir ülke veya şehirde büyük bir ev sahibi olabilirsiniz. Evinizde içki dolabı olabilir. "
			},
			{   # Satürn 28°
				"id": "saturn_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Satürn ♄",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Satürn 28° ise rahat ve davetkar hissettiren geniş bir eve sahip olabilirsiniz. Evinizde büyük bir antre olabilir. Daha eski ve tarihi bir çekiciliğe sahip bir eviniz olabilir"
			},
			{   # Uranüs 28°
				"id": "uranus_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Uranüs ♅",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Uranüs 28° ise beklenmedik bir şekilde büyük bir eve sahip olabilirsiniz. Evinizde ilginç ve sıra dışı dekorasyonlar olabilir. Evinizde teknoloji, oyun odası olabilir."
			},
			{   # Neptün 28°
				"id": "neptune_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Neptün ♆",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Neptün 28° ise havuzlu bir eviniz olur ya da havuzlu bir sitede yaşarsınız. Evinizde yoga yapmak için özel bir alan olabilir."
			},
			{   # Plüton 28°
				"id": "pluto_at_28deg",
				"type": "planet_degree_equals",
				"planet": "Plüton ♇",
				"degree_min": 28.0,
				"degree_max": 28.9,
				"title": title,
				"text": "Plüton 28° ise geniş bir bodrum katına sahip olabilirsiniz. Aynı zamanda evinizin boyutunu değiştiren ve artıran büyük bir tadilat yapmak durumunda kalabilirsiniz."
			}
		]
	def _eight_house_shadow_notes(self) -> List[Dict]:
		title = "8.Ev Gölge Teması"
		return [
			{   # 8. ev Güneş / Aslan
				"id": "sun_in_8th_or_leo_8th",
				"type": "planet_in_house",
				"planet": "Güneş ☉",
				"house": 8,
				"title": title,
				"text": "Kendini yeterince iyi hissetmemenin getirdiği utançla büyümüş olabilirsiniz ancak kim olduğunuzu kabul etmeyi ve kendinizle gurur duymayı öğrenmek zorundasınız. Gerçek benliğinizi kucaklamayı bilmemeniz özellikle büyüme çağında başkalarıyla, belki de ebeveynlerizden biriyle sıkça karşılaştırılmış olmanızdan kaynaklanıyor olabilir. Bu durum istemeseniz bile onların izinden gitmek zorundaymışsınız gibi hissetmenize neden olmuş olabilir. Çoğu zaman insanların kıskançlıkları ve güvensizlikleri size yansıtılmış olabilir, bu da ilgi ya da iltifatın ardında bir tuzak olduğunu hissetmenize yol açabilir. Belki birileri sizden bir şeyler bekliyor ya da size yaklaşarak hayatınızı sabote etmeye çalışıyor gibi gelmiş olabilir. Kendinizi bu utançtan kurtardığınızda ve geçmişte hoşlanmadığınız tüm eski versiyonlarınızla barıştığınızda, gerçekten durdurulamaz olabilirsiniz. Ancak önce kendinizi affetmeyi öğrenmeniz gerekiyor."
			},
			{   # 8. ev Güneş / Aslan
				"id": "house_8_leo",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Aslan",
				"title": title,
				"text": "Kendini yeterince iyi hissetmemenin getirdiği utançla büyümüş olabilirsiniz ancak kim olduğunuzu kabul etmeyi ve kendinizle gurur duymayı öğrenmek zorundasınız. Gerçek benliğinizi kucaklamayı bilmemeniz özellikle büyüme çağında başkalarıyla, belki de ebeveynlerizden biriyle sıkça karşılaştırılmış olmanızdan kaynaklanıyor olabilir. Bu durum istemeseniz bile onların izinden gitmek zorundaymışsınız gibi hissetmenize neden olmuş olabilir. Çoğu zaman insanların kıskançlıkları ve güvensizlikleri size yansıtılmış olabilir, bu da ilgi ya da iltifatın ardında bir tuzak olduğunu hissetmenize yol açabilir. Belki birileri sizden bir şeyler bekliyor ya da size yaklaşarak hayatınızı sabote etmeye çalışıyor gibi gelmiş olabilir. Kendinizi bu utançtan kurtardığınızda ve geçmişte hoşlanmadığınız tüm eski versiyonlarınızla barıştığınızda, gerçekten durdurulamaz olabilirsiniz. Ancak önce kendinizi affetmeyi öğrenmeniz gerekiyor."
			},
			{   # 8. ev Ay / Yengeç
				"id": "moon_in_8th_or_cancer_8th",
				"type": "planet_in_house",
				"planet": "Ay ☽",
				"house": 8,
				"title": title,
				"text": "Sıklıkla başkalarının duygularına yeterince önem vermediğiniz söylenmiş olabilir. Ancak bu geçmişte duygusal manipülasyonlara maruz kalmanız ve suçluluk duygusuyla bir şeyler yapmaya zorlanmanız nedeniyle olabilir. Belki de çocuklukta özellikle anne figürünüze çok yakın olmankz, onun duygularını içselleştirip kendi duygularınızdan ayırt edememenizi sağlamış olabilir. Bu durum, etrafınızdaki insanların hissettiklerinden kendinizi sorumlu hissetmenize yol açmış olabilir. Ancak, başkalarının duygularını hissetmenizin, onların sorumluluğunu almak anlamına gelmediğini anlamalısınız. Kendinizi korumak için duygusal sınırlar belirlemek sizin hakkınız."
			},
			{   # 8. ev Ay / Yengeç
				"id": "house_8_cancer",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Yengeç",
				"title": title,
				"text": "Sıklıkla başkalarının duygularına yeterince önem vermediğiniz söylenmiş olabilir. Ancak bu geçmişte duygusal manipülasyonlara maruz kalmanız ve suçluluk duygusuyla bir şeyler yapmaya zorlanmanız nedeniyle olabilir. Belki de çocuklukta özellikle anne figürünüze çok yakın olmankz, onun duygularını içselleştirip kendi duygularınızdan ayırt edememenizi sağlamış olabilir. Bu durum, etrafınızdaki insanların hissettiklerinden kendinizi sorumlu hissetmenize yol açmış olabilir. Ancak, başkalarının duygularını hissetmenizin, onların sorumluluğunu almak anlamına gelmediğini anlamalısınız. Kendinizi korumak için duygusal sınırlar belirlemek sizin hakkınız."
			},
			{   # 8. ev Merkür / İkizler / Başak
				"id": "mercury_in_8th_or_gemini_8th",
				"type": "planet_in_house",
				"planet": "Merkür ☿",
				"house": 8,
				"title": title,
				"text": "Düşüncelerinizin, fikirlerinizin ve ifade biçimlerinizin uygunsuz olduğu sıkça söylenmiş olabilir, bu da kendinizi ifade etmekten utanmanıza neden olmuş olabilir. Kardeşleriniz varsa onların davranışlarından sorumlu tutulmuş ya da suçlanmış olabilirsiniz. Arkadaşlarınızın ebeveynleri tarafından durum böyle olmasa bile kötü bir etki olarak görülmüş olabilirsiniz. Ancak siz insanlara hemen açılan biri olmayabilirsiniz. Buna rağmen insanlar size doğal bir şekilde güvenebilir ve en karanlık sırlarını paylaşabilir. 8.evdeki Merkür enerjisi keskin bir gözlemci ve doğal bir dedektif yeteneği kazandırır. Kalıpları fark eder, doğru sonuçlar çıkarır ve bunları kanıtlarla destekleyebilirsiniz. Bu becerilerinizi hem kendini, hem de başkaları için anlamlı şekilde kullanabilirsiniz."
			},
			{   # 8. ev Merkür / İkizler / Başak
				"id": "house_8_gemini",
				"type": "house_sign_is",
				"house": 8,
				"sign": "İkizler",
				"title": title,
				"text": "Düşüncelerinizin, fikirlerinizin ve ifade biçimlerinizin uygunsuz olduğu sıkça söylenmiş olabilir, bu da kendinizi ifade etmekten utanmanıza neden olmuş olabilir. Kardeşleriniz varsa onların davranışlarından sorumlu tutulmuş ya da suçlanmış olabilirsiniz. Arkadaşlarınızın ebeveynleri tarafından durum böyle olmasa bile kötü bir etki olarak görülmüş olabilirsiniz. Ancak siz insanlara hemen açılan biri olmayabilirsiniz. Buna rağmen insanlar size doğal bir şekilde güvenebilir ve en karanlık sırlarını paylaşabilir. 8.evdeki Merkür enerjisi keskin bir gözlemci ve doğal bir dedektif yeteneği kazandırır. Kalıpları fark eder, doğru sonuçlar çıkarır ve bunları kanıtlarla destekleyebilirsiniz. Bu becerilerinizi hem kendini, hem de başkaları için anlamlı şekilde kullanabilirsiniz."
			},
			{   # 8. ev Merkür / İkizler / Başak
				"id": "house_8_virgo",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Başak",
				"title": title,
				"text": "Düşüncelerinizin, fikirlerinizin ve ifade biçimlerinizin uygunsuz olduğu sıkça söylenmiş olabilir, bu da kendinizi ifade etmekten utanmanıza neden olmuş olabilir. Kardeşleriniz varsa onların davranışlarından sorumlu tutulmuş ya da suçlanmış olabilirsiniz. Arkadaşlarınızın ebeveynleri tarafından durum böyle olmasa bile kötü bir etki olarak görülmüş olabilirsiniz. Ancak siz insanlara hemen açılan biri olmayabilirsiniz. Buna rağmen insanlar size doğal bir şekilde güvenebilir ve en karanlık sırlarını paylaşabilir. 8.evdeki Merkür enerjisi keskin bir gözlemci ve doğal bir dedektif yeteneği kazandırır. Kalıpları fark eder, doğru sonuçlar çıkarır ve bunları kanıtlarla destekleyebilirsiniz. Bu becerilerinizi hem kendini, hem de başkaları için anlamlı şekilde kullanabilirsiniz."
			},
			{   # 8. ev Venüs / Boğa / Terazi
				"id": "venus_in_8th_or_taurus_8th",
				"type": "planet_in_house",
				"planet": "Venüs ♀",
				"house": 8,
				"title": title,
				"text": "Zevkleriniz ve özellikle moda anlayışınız ya da harcama alışkanlıklarınız üzerinde aileden, özellikle de büyürken yakın olduğunuz kadınlardan gelen etkiler hissedebilirsiniz. Eğer bir kadınsanız ailenizdeki kadınlar sizi ataerkil sistemin tehlikeleri konusunda uyararak dünyayı kadınlar için daha temkinli bir yer olarak algılamanıza yol açmış olabilir. Bu durum erkeklere olan güvensizliğinizi artırabilir ve onların sizi kendi çıkarları doğrultusunda kullanabileceklerine dair farkındalığınızı güçlendirebilir. ilişkilerinizde maddi kayıplar yaşıyorsanız bu durum o kişinin sizin için uygun olmadığının bir işareti olabilir. Bu yerleşim takıntılı partnerleri çekme eğilimi yaratabilir bu nedenle sezgilerinize güvenmeyi ve erken dönemde kırmızı bayrakları görmezden gelmemeyi öğrenmek önemlidir. Unutmayın, ilişkilerinizde yaşadığınız kötü deneyimler asla sizin suçunuz değildir ve hiçbir şekilde sizin davranışlarınızla kışkırtılmamıştır."
			},
			{   # 8. ev Venüs / Boğa / Terazi
				"id": "house_8_taurus",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Boğa",
				"title": title,
				"text": "Zevkleriniz ve özellikle moda anlayışınız ya da harcama alışkanlıklarınız üzerinde aileden, özellikle de büyürken yakın olduğunuz kadınlardan gelen etkiler hissedebilirsiniz. Eğer bir kadınsanız ailenizdeki kadınlar sizi ataerkil sistemin tehlikeleri konusunda uyararak dünyayı kadınlar için daha temkinli bir yer olarak algılamanıza yol açmış olabilir. Bu durum erkeklere olan güvensizliğinizi artırabilir ve onların sizi kendi çıkarları doğrultusunda kullanabileceklerine dair farkındalığınızı güçlendirebilir. ilişkilerinizde maddi kayıplar yaşıyorsanız bu durum o kişinin sizin için uygun olmadığının bir işareti olabilir. Bu yerleşim takıntılı partnerleri çekme eğilimi yaratabilir bu nedenle sezgilerinize güvenmeyi ve erken dönemde kırmızı bayrakları görmezden gelmemeyi öğrenmek önemlidir. Unutmayın, ilişkilerinizde yaşadığınız kötü deneyimler asla sizin suçunuz değildir ve hiçbir şekilde sizin davranışlarınızla kışkırtılmamıştır."
			},
			{   # 8. ev Venüs / Boğa / Terazi
				"id": "house_8_libra",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Terazi",
				"title": title,
				"text": "Zevkleriniz ve özellikle moda anlayışınız ya da harcama alışkanlıklarınız üzerinde aileden, özellikle de büyürken yakın olduğunuz kadınlardan gelen etkiler hissedebilirsiniz. Eğer bir kadınsanız ailenizdeki kadınlar sizi ataerkil sistemin tehlikeleri konusunda uyararak dünyayı kadınlar için daha temkinli bir yer olarak algılamanıza yol açmış olabilir. Bu durum erkeklere olan güvensizliğinizi artırabilir ve onların sizi kendi çıkarları doğrultusunda kullanabileceklerine dair farkındalığınızı güçlendirebilir. ilişkilerinizde maddi kayıplar yaşıyorsanız bu durum o kişinin sizin için uygun olmadığının bir işareti olabilir. Bu yerleşim takıntılı partnerleri çekme eğilimi yaratabilir bu nedenle sezgilerinize güvenmeyi ve erken dönemde kırmızı bayrakları görmezden gelmemeyi öğrenmek önemlidir. Unutmayın, ilişkilerinizde yaşadığınız kötü deneyimler asla sizin suçunuz değildir ve hiçbir şekilde sizin davranışlarınızla kışkırtılmamıştır."
			},
			{   # 8. ev Mars / Koç / Akrep
				"id": "mars_in_8th_or_aries_scorpio_8th",
				"type": "planet_in_house",
				"planet": "Mars ♂",
				"house": 8,
				"title": title,
				"text": "Çatışmaları ele alma ve öfke ile başa çıkma biçimlerinizi büyük ölçüde miras almış olabilirsiniz. Ayrıca cinselliğe dair algılarınızı da aileden gelen etkiler şekillendirmiş olabilir. Bu durum cinselliğinizi keşfetmekte ve arzularınızı kabullenmekte zorluk yaşamanıza neden olabilir. Küçük yaşlardan itibaren mendinizi savunmayı öğrenmek zorunda kalmış olabilirsiniz çünkü bunu yapmazsanız destek bulamayacağınız hissine kapılmış olabilirsiniz. İnsanların sizi olduğunuzdan daha güçlü görmesi başkalarından yardım alamamanıza yol açabilir ve bu nedenle içsel gücünüzle başa çıkmayı öğrenmiş olabilirsiniz. Kendinizi savunduğunuzda bile bazen kötü kişi olarak algılanabilirsiniz. Yine de lendi haklarınızı korumaktan vazgeçmemeniz önemlidir. Bunun yanında, doğaüstü konulara müdahil olmamak sizin için daha iyi olabilir."
			},
			{   # 8. ev Mars / Koç / Akrep
				"id": "house_8_aries",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Koç",
				"title": title,
				"text": "Çatışmaları ele alma ve öfke ile başa çıkma biçimlerinizi büyük ölçüde miras almış olabilirsiniz. Ayrıca cinselliğe dair algılarınızı da aileden gelen etkiler şekillendirmiş olabilir. Bu durum cinselliğinizi keşfetmekte ve arzularınızı kabullenmekte zorluk yaşamanıza neden olabilir. Küçük yaşlardan itibaren mendinizi savunmayı öğrenmek zorunda kalmış olabilirsiniz çünkü bunu yapmazsanız destek bulamayacağınız hissine kapılmış olabilirsiniz. İnsanların sizi olduğunuzdan daha güçlü görmesi başkalarından yardım alamamanıza yol açabilir ve bu nedenle içsel gücünüzle başa çıkmayı öğrenmiş olabilirsiniz. Kendinizi savunduğunuzda bile bazen kötü kişi olarak algılanabilirsiniz. Yine de lendi haklarınızı korumaktan vazgeçmemeniz önemlidir. Bunun yanında, doğaüstü konulara müdahil olmamak sizin için daha iyi olabilir."
			},
			{   # 8. ev Mars / Koç / Akrep
				"id": "house_8_scorpio",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Akrep",
				"title": title,
				"text": "Çatışmaları ele alma ve öfke ile başa çıkma biçimlerinizi büyük ölçüde miras almış olabilirsiniz. Ayrıca cinselliğe dair algılarınızı da aileden gelen etkiler şekillendirmiş olabilir. Bu durum cinselliğinizi keşfetmekte ve arzularınızı kabullenmekte zorluk yaşamanıza neden olabilir. Küçük yaşlardan itibaren mendinizi savunmayı öğrenmek zorunda kalmış olabilirsiniz çünkü bunu yapmazsanız destek bulamayacağınız hissine kapılmış olabilirsiniz. İnsanların sizi olduğunuzdan daha güçlü görmesi başkalarından yardım alamamanıza yol açabilir ve bu nedenle içsel gücünüzle başa çıkmayı öğrenmiş olabilirsiniz. Kendinizi savunduğunuzda bile bazen kötü kişi olarak algılanabilirsiniz. Yine de lendi haklarınızı korumaktan vazgeçmemeniz önemlidir. Bunun yanında, doğaüstü konulara müdahil olmamak sizin için daha iyi olabilir."
			},
			{   # 8. ev Jüpiter / Yay
				"id": "jupiter_in_8th_or_sag_8th",
				"type": "planet_in_house",
				"planet": "Jüpiter ♃",
				"house": 8,
				"title": title,
				"text": "Dini ve manevi inançlarınızı veya bu konulara yaklaşımınızı büyük ölçüde ailenizden miras almış olabilirsiniz. Ancak bu inançların sizin için gerçekten uygun olup olmadığını sorgulamak önemlidir. Hayatınızda büyük nimetler elde etmeden önce önemli değişimler yaşayabilirsiniz ve bu değişimlerle başa çıkmayı öğrenmek büyümeniz için kritik bir adımdır. Küçük yaştan itibaren yeteneklerinizin ve potansiyelinizin farkına varılmış olabilir bu da üzerinizde bir baskı yaratmış olabilir. Ancak bu baskıyı bir yük olarak değil bir motivasyon kaynağı olarak görmeyi öğrenmelisiniz. Kendinize inandığınızda büyük başarılar elde etmeniz mümkün. Çünkü inanç her şeyin başlangıç noktasıdır."
			},
			{   # 8. ev Jüpiter / Yay
				"id": "house_8_sagittarius",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Yay",
				"title": title,
				"text": "Dini ve manevi inançlarınızı veya bu konulara yaklaşımınızı büyük ölçüde ailenizden miras almış olabilirsiniz. Ancak bu inançların sizin için gerçekten uygun olup olmadığını sorgulamak önemlidir. Hayatınızda büyük nimetler elde etmeden önce önemli değişimler yaşayabilirsiniz ve bu değişimlerle başa çıkmayı öğrenmek büyümeniz için kritik bir adımdır. Küçük yaştan itibaren yeteneklerinizin ve potansiyelinizin farkına varılmış olabilir bu da üzerinizde bir baskı yaratmış olabilir. Ancak bu baskıyı bir yük olarak değil bir motivasyon kaynağı olarak görmeyi öğrenmelisiniz. Kendinize inandığınızda büyük başarılar elde etmeniz mümkün. Çünkü inanç her şeyin başlangıç noktasıdır."
			},
			{   # 8. ev Satürn / Oğlak / Kova
				"id": "saturn_in_8th_or_cap_8th",
				"type": "planet_in_house",
				"planet": "Satürn ♄",
				"house": 8,
				"title": title,
				"text": "Muhtemelen her durumda kendinizi toparlayıp sorunları çözebilecek bir şekilde yetiştirildiniz, bu da kriz anlarını yönetme konusunda sizi oldukça yetkin kılıyor. Ancak bu etrafınızdaki herkes için sonsuza dek sorumluluk üstlenmek zorunda olduğunuz anlamına gelmez. Kontrollü olma ihtiyacınız sizi şaşırtıcı durumlara karşı küçümseyici bir tavır almaya itebilir çünkü nasıl tepki vereceğinizi bilememek sizi utandırabilir. Ayrıca büyürken ve belki de bugün hala, sorumluluk almamanız veya liderlik yapmamanız durumunda eleştirilmiş olabilirsiniz, sanki her şey sizin hatanızmış gibi suçlanmış olabilirsiniz. Bunun bir yük olmadığını, sadece insan olduğunuzu ve bazen sınırlar koymanız gerektiğini kendinize hatırlatmalısınız."
			},
			{   # 8. ev Satürn / Oğlak / Kova
				"id": "house_8_capricorn",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Oğlak",
				"title": title,
				"text": "Muhtemelen her durumda kendinizi toparlayıp sorunları çözebilecek bir şekilde yetiştirildiniz, bu da kriz anlarını yönetme konusunda sizi oldukça yetkin kılıyor. Ancak bu etrafınızdaki herkes için sonsuza dek sorumluluk üstlenmek zorunda olduğunuz anlamına gelmez. Kontrollü olma ihtiyacınız sizi şaşırtıcı durumlara karşı küçümseyici bir tavır almaya itebilir çünkü nasıl tepki vereceğinizi bilememek sizi utandırabilir. Ayrıca büyürken ve belki de bugün hala, sorumluluk almamanız veya liderlik yapmamanız durumunda eleştirilmiş olabilirsiniz, sanki her şey sizin hatanızmış gibi suçlanmış olabilirsiniz. Bunun bir yük olmadığını, sadece insan olduğunuzu ve bazen sınırlar koymanız gerektiğini kendinize hatırlatmalısınız."
			},
			{   # 8. ev Satürn / Oğlak / Kova
				"id": "house_8_aquarius",
				"type": "house_sign_is",
				"house": 8,
				"sign": "Kova",
				"title": title,
				"text": "Muhtemelen her durumda kendinizi toparlayıp sorunları çözebilecek bir şekilde yetiştirildiniz, bu da kriz anlarını yönetme konusunda sizi oldukça yetkin kılıyor. Ancak bu etrafınızdaki herkes için sonsuza dek sorumluluk üstlenmek zorunda olduğunuz anlamına gelmez. Kontrollü olma ihtiyacınız sizi şaşırtıcı durumlara karşı küçümseyici bir tavır almaya itebilir çünkü nasıl tepki vereceğinizi bilememek sizi utandırabilir. Ayrıca büyürken ve belki de bugün hala, sorumluluk almamanız veya liderlik yapmamanız durumunda eleştirilmiş olabilirsiniz, sanki her şey sizin hatanızmış gibi suçlanmış olabilirsiniz. Bunun bir yük olmadığını, sadece insan olduğunuzu ve bazen sınırlar koymanız gerektiğini kendinize hatırlatmalısınız."
			},
			{   # 8. ev Uranüs
				"id": "uranus_in_8th",
				"type": "planet_in_house",
				"planet": "Uranüs ♅",
				"house": 8,
				"title": title,
				"text": "Kontrol ihtiyacınızı bırakmayı öğrenmek sizin için hayati önem taşıyor çünkü ani ve beklenmedik değişimler hayatınızda diğer insanlardan daha sık meydana gelebilir. Bu, 'hiçbir şey kalıcı değildir' mottosunu yaşamınızın bir parçası haline getirmenizi gerektirebilir. Hayatınızdaki olaylara çok fazla bağlanmamak ve ne olursa olsun başa çıkabileceğinize güvenmek sizi bu yerleşimin getirdiği zorluklardan koruyacaktır."
			},
			{   # 8. ev Neptün
				"id": "neptune_in_8th",
				"type": "planet_in_house",
				"planet": "Neptün ♆",
				"house": 8,
				"title": title,
				"text": "Bu yerleşim, ailenizden bağımlılık eğilimleri miras alabileceğinizi gösterebilir. Bu nedenle, kendi davranışlarınıza dikkat etmeniz ve gerektiğinde yardım istemeniz önemlidir. Aynı zamanda ailenizden psişik veya sezgisel yetenekler miras almış olma ihtimaliniz de bulunuyor. Siz olayların yüzeyindeki değil derinliklerindeki anlamları görebilme yeteneğine sahipsiniz ve hayatınızdaki her türlü deneyimi, kötü olanlar da dahil birer öğretici an olarak değerlendirebilirsiniz."
			},
			{   # 8. ev Plüton
				"id": "pluto_in_8th",
				"type": "planet_in_house",
				"planet": "Plüton ♇",
				"house": 8,
				"title": title,
				"text": "Hayatınızdaki dönüşümler sıradan bir insana kıyasla çok daha yoğun ve yıkıcı hissedilebilir. Bu tür olaylarla karşılaştığınızda korkuya kapılmamak, sabırlı olmak ve durumun sonuçlarını görmek için beklemek önemlidir. Ancak bu bekleme süresince aceleci davranmaktan kaçınarak bilinçli adımlar atmanız gerekir. Bu yerleşim, en kötü ihtimalle ebeveynlerinizin mirasından mahrum kalmayı gösterebilir. Ancak bu dönüşüm ve yeniden doğuş konularında ustalaşarak büyük bir güç elde etmenizi de sağlar."
			},
		]
	def _four_house_career_notes(self) -> List[Dict]:   
		title = "4.Ev Eşin Kariyerini Anlatır"
		return [
            {   # 4. ev İkizler
                "id": "4th_house_gemini",
                "type": "house_sign_is",
                "house": 4,
				"sign": "İkizler",
                "title": title,
                "text": "4.ev ikizler ise iletişim ile ilgili alanlarda çalışabilir, gazeteci, yazar ya da öğretmen olabilir."
            },
			{   # 4. ev Koç
                "id": "4th_house_aries",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Koç",
                "title": title,
                "text": "4.ev koç ise eşiniz kariyerinde bir lider olabilir, başkalarıyla rekabet halinde olabilir, devamlı fiziksel aktivite halinde olabilir. Mesela antrenör, asker veya girișimci olabilir."
            },
			{   # 4. ev Boğa
                "id": "4th_house_taurus",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Boğa",
                "title": title,
                "text": "4.Eviniz Boğaysa finans ya da emlak sektöründe yer alabilir, sanatla ilgili bir kariyeri olabilir. Bankacı olabilir en basitinden."
            },
			{   # 4. ev Yengeç
                "id": "4th_house_cancer",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Yengeç",
                "title": title,
                "text": "4.Eviniz Yengeç ise 4. sosyal hizmetlerde çalışabilir, hemşire olabilir, aşçı olabilir."
            },
			{   # 4. ev Aslan
                "id": "4th_house_leo",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Aslan",
                "title": title,
                "text": "4.Eviniz Aslan ise 4. eğlence sektöründe olabilir, oyuncu, müzisyen veya performans sanatçısı olabilir."
            },
			{   # 4. ev Başak
                "id": "4th_house_virgo",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Başak",
                "title": title,
                "text": "4.Eviniz Başak ise 4. hizmet sektöründe, sağlık sektöründe çalışabilir. Bir şeyleri analiz etmesini gerektiren işlerde çalışabilir. Doktor ya da danışman olabilir."
            },
			{   # 4. ev Terazi
                "id": "4th_house_libra",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Terazi",
                "title": title,
                "text": "4.Eviniz Terazi ise hukuk alanında çalışabilir, avukat olabilir, diplomasi ile ilgili işlerde yer alabilir ya da estetik işlerde çalışabilir mesela tasarımcı olabilir."
            },
			{   # 4. ev Akrep
                "id": "4th_house_scorpio",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Akrep",
                "title": title,
                "text": "4.Eviniz Akrep ise 4. araştırmacı gazeteci olabilir, psikolog, psikiyatr olabilir ya da finans alanında çalışabilir, vergi uzmanı olabilir ya da mali danışman olabilir."
            },
			{   # 4. ev Yay
                "id": "4th_house_sagittarius",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Yay",
                "title": title,
                "text": "4.Eviniz Yay ise 4. öğretmen, akademisyen, yazar veya seyahat ile ilgili işlerde çalışabilir."
            },
			{   # 4. ev Oğlak
                "id": "4th_house_capricorn",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Oğlak",
                "title": title,
                "text": "4.Eviniz Oğlak ise işletmeci, yönetici olabilir, kamu sektöründe çalışabilir, politika ile ilgilenebilir.."
            },
			{   # 4. ev Kova
                "id": "4th_house_aquarius",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Kova",
                "title": title,
                "text": "4.Eviniz Kova ise 4. geleceğin mesleklerinden birini yapabilir, teknoloji ile ilgili bir işi olabilir, mühendis, yazılımcı olabilir."
            },
			{   # 4. ev Balık
                "id": "4th_house_pisces",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Balık",
                "title": title,
                "text": "4.Eviniz Balık ise 4. sanatla ilgili bir işi olabilir, müzisyen, ressam veya spiritüel alanlarda çalışabilir."
            }
        ]
	def _feeling_overwhelmed_notes(self) -> List[Dict]:
		title = "Yengeç Burcunun Bulunduğu Ev Kendinizi Bunalmış Hissettiğinizde ve Bir Molaya İhtiyaç Duyduğunuzda Ne Yapmanız Gerektiğini Gösterir"
		return [
            {   # 1. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_1",
                "type": "house_sign_is",
				"house": 1,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 1.evinizdeyse yani yükselen yengeçseniz kuaföre gidin, kişisel bakımınızı yapın."
            },
			{   # 2. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_2",
                "type": "house_sign_is",
				"house": 2,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 2.evinizdeyse masaja gidin."
            },
			{   # 3. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_3",
                "type": "house_sign_is",
				"house": 3,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 3.evinizdeyse yürüyüşler yapın."
            },
			{   # 4. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_4",
                "type": "house_sign_is",
				"house": 4,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 4.evinizdeyse odanızın dekorasyonunu değiştirin."
            },
			{   # 5. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_5",
                "type": "house_sign_is",
				"house": 5,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 5.evinizdeyse hobilerinizle meşgul olun."
            },
			{   # 6. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_6",
                "type": "house_sign_is",
				"house": 6,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 6.evinizdeyse spor yapın."
            },
			{   # 7. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_7",
                "type": "house_sign_is",
				"house": 7,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 7.evinizdeyse aynanın karşısında kendi kendinize konuşun (bu arada buna gülmeyin ingilizce çalışırken çok işe yarıyor)."
            },
			{   # 8. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_8",
                "type": "house_sign_is",
				"house": 8,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 8.evinizdeyse daha önce hiç gitmediğiniz bir yere gidin."
            },
			{   # 9. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_9",
                "type": "house_sign_is",
				"house": 9,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 9.evinizdeyse yeni bir dil öğrenin."
            },
			{   # 10. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_10",
                "type": "house_sign_is",
				"house": 10,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 10.evinizdeyse motivasyon konuşmaları izleyin."
            },
			{   # 11. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_11",
                "type": "house_sign_is",
				"house": 11,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 11.evinizdeyse kendinize yeni bir sosyal medya hesabı açın."
            },
			{   # 12. ev Yengeç- mola önerisi
                "id": "feeling_overwhelmed_12",
                "type": "house_sign_is",
				"house": 12,
				"sign": "Yengeç",
                "title": title,
                "text": "Yengeç burcu 12.evinizdeyse uyuyun ya da meditasyon yapın."
            }
        ]
	def _rare_house_aspect_notes(self) -> List[Dict]:
		title = "Haritada Kova Burcunun Olduğu Ev Sizi Eşsiz Kılan Yerdir"
		return [
			{   # 1.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_1",
				"type": "house_sign_is",
			"house": 1,
			"sign": "Kova",
				"title": title,
				"text": "Yükselen Kovaysanız zaten kişiliğiniz eşsizdir."
			},
			{   # 2.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_2",
				"type": "house_sign_is",
			"house": 2,
			"sign": "Kova",
				"title": title,
				"text": "2.evinde Kova olanların sıradışı yetenekleri olabilir, insanların aklına gelmeyecek alanlardan para kazanabilirler."
			},
			{   # 3.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_3",
				"type": "house_sign_is",
			"house": 3,
			"sign": "Kova",
				"title": title,
				"text": "3.evinizde Kova varsa çok ilginç öğrenme stilleriniz olabilir."
			},
			{   # 4.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_4",
				"type": "house_sign_is",
			"house": 4,
			"sign": "Kova",
				"title": title,
				"text": "4.evinizde Kova varsa evinizin dekorasyonu çok sıradışı olabilir."
			},
			{   # 5.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_5",
				"type": "house_sign_is",
			"house": 5,
			"sign": "Kova",
				"title": title,
				"text": "5.evinizde Kova varsa çocuklarınız çok özel ve sıradışı bireyler olur."
			},
			{   # 6.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_6",
				"type": "house_sign_is",
			"house": 6,
			"sign": "Kova",
				"title": title,
				"text": "6.evinizde Kova varsa sağlık ve iş hayatınızda sıra dışı yaklaşımlarınız olabilir."
			},
			{   # 7.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_7",
				"type": "house_sign_is",
			"house": 7,
			"sign": "Kova",
				"title": title,
				"text": "7.evinizde Kova varsa standartın dışında bir eşiniz ve evliliğiniz olur."
			},
			{   # 8.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_8",
				"type": "house_sign_is",
			"house": 8,
			"sign": "Kova",
				"title": title,
				"text": "8.evinizde Kova varsa eşiniz ilginç yollardan para kazanabilir."
			},
			{   # 9.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_9",
				"type": "house_sign_is",
			"house": 9,
			"sign": "Kova",
				"title": title,
				"text": "9.evinizde Kova varsa akademik hayatınız farklı olabilir."
			},
			{   # 10.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_10",
				"type": "house_sign_is",
			"house": 10,
			"sign": "Kova",
				"title": title,
				"text": "10.evinizde Kova varsa eşsiz başarılar kazanabilirsiniz."
			},
			{   # 11.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_11",
				"type": "house_sign_is",
			"house": 11,
			"sign": "Kova",
				"title": title,
				"text": "11.evinizde Kova varsa marjinal arkadaş çevreleriniz olur, sosyal medyada farklı bir persona yaratabilirsiniz."
			},
			{   # 12.ev Kova - eşsiz kılınan nokta
				"id": "rare_house_12",
				"type": "house_sign_is",
			"house": 12,
			"sign": "Kova",
				"title": title,
				"text": "12.evinizde Kova varsa rüyalarınız çok acayip olur."
			}
		]
	def _degree_17_notes(self) -> List[Dict]:
		title = "17° Aslan Derecesidir ve Yalnızca Sevimli Oluşuyla Bile Fırsatları Kendine Çeken Birini Temsil Eder"
		return [
            {   # Güneş 17°
				"id": "sun_at_17deg",
				"type": "planet_degree_equals",
				"planet": "Güneş ☉",
				"degree_min": 17.0,
				"degree_max": 17.9,
				"title": title,
				"text": "Güneş 17° ise sadece kim olduğunuz ve kendinizi nasıl ifade ettiğinizle bile fırsatları hayatınıza çekebileceğinizi gösterir. Popülerlik kazanabilirsiniz, size daha tazla kapı açılabilir bu sayede ve özellikle yaratıcı alanlarda parlayabilirsiniz. Yeteneğinizle fark edilirsiniz. Bazı kişiler bu yerleşim sayesinde babaları ya da hayatlarındaki erkek figürler aracılığıyla da fırsatlar elde edebilir."
			},
			{   # Venüs 17°
				"id": "venus_at_17deg",
				"type": "planet_degree_equals",
				"planet": "Venüs ♀",
				"degree_min": 17.0,
				"degree_max": 17.9,
				"title": title,
				"text": "Venüs 17° ise insanlar tarzınızı çok beğenir ve sırf bu sayede fırsatları kendinize çekebilirsiniz. Giyinme ve aksesuar kullanma biçiminiz size daha fazla kapı açabilir. Network edinmek de size fayda saglar. Enerjinizin ne kadar hoş olduğunu fark edip sizi takdir eden kişiler olacaktır. Ve bu kişiler sayesinde fırsat yakalayabilirsiniz."
			},
			{   # Şans Noktası 17°
				"id": "part_of_fortune_at_17deg",
				"type": "planet_degree_equals",
				"planet": "Şans Noktası",
				"degree_min": 17.0,
				"degree_max": 17.9,
				"title": title,
				"text": "Şans Noktası 17°'de ise bu derece aktif hale geldiğinde hayatınıza daha fazla şans ve keyifli deneyimler çekebilirsiniz. Örneğin Şans Noktanız Terazi'dedir. Güneş gökyüzünde Terazideyken şansınız artabilir. Bu dönemde insanlar size karşı daha nazik olabilir ve hayat daha keyifli akabilir.."
			},
			{   # Satürn 17°
				"id": "saturn_at_17deg",
				"type": "planet_degree_equals",
				"planet": "Satürn ♄",
				"degree_min": 17.0,
				"degree_max": 17.9,
				"title": title,
				"text": "Satürn 17°'de olması kariyer konularında önemli fırsatları kendinize çekebileceğinizi gösterir çünkü insanlar sizi çalışkan, sorumlu ve yetenekli biri olarak görebilir. Ayrıca sizden yaşça büyük kişiler ya da otorite figürleri enerjinizi takdir ederek size yeni kapılar açabilir. Ancak bu yerleşim her fırsatın arkasında ciddi bir emek ve sorumluluk olacağını da bize hatırlatır. Kazanmak için çaba şarttır."
			},
			{   # Jüpiter 17°
				"id": "jupiter_at_17deg",
				"type": "planet_degree_equals",
				"planet": "Jüpiter ♃",
				"degree_min": 17.0,
				"degree_max": 17.9,
				"title": title,
				"text": "Jüpiter 17°'de olması ilahi bir yerleşimdir. Bu konum insanların size karşı daha cömert ve nazik davranmasını saglayabilir çünkü enerjiniz çevrenizi pozitif etkiler. Yurtdışı seyahatlerinde şans sizden yana olabilir, bazı ülkelerde daha çok ilgi görüp takdir edildiginizi bile fark edebilirsiniz. Ayrıca bu yerleşim zekanız ya da spiritüel bakış açınız sayesinde size çeşitli fırsatlar sunulmasına da yol açabilir. Özellikle üniversite eğitimi esnasında başarı kazanabilir ya da burs alabilirsiniz."
			}
			
        ]
	def _insecurity_notes(self) -> List[Dict]:
		title = "Haritada Akrep Burcunun Bulunduğu Ev En Güvensiz Hissettiğiniz Alanı Temsil Eder"
		return [
            {   # 1. ev Akrep - güvensizlik hissi
                "id": "insecurity_1",
                "type": "house_sign_is",
				"house": 1,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 1.evinizdeyse kendinizden şüphe edebilirsiniz zaman zaman..."
            },
			{   # 2. ev Akrep - güvensizlik hissi
                "id": "insecurity_2",
                "type": "house_sign_is",
				"house": 2,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 2.evinizdeyse her an param bitecek korkusu yaşayabilirsiniz."
            },
			{   # 3. ev Akrep - güvensizlik hissi
                "id": "insecurity_3",
                "type": "house_sign_is",
				"house": 3,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 3.evinizdeyse kardeşlerinize, akrabalarınıza güvenmeyebilirsiniz."
            },
			{   # 4. ev Akrep - güvensizlik hissi
                "id": "insecurity_4",
                "type": "house_sign_is",
				"house": 4,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 4.evinizdeyse belki de kendinizi ev ortamında yeterince güvende hissedemiyorsunuz."
            },
			{   # 5. ev Akrep - güvensizlik hissi
                "id": "insecurity_5",
                "type": "house_sign_is",
				"house": 5,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 5.evinizdeyse aşk yaşarken güvende hissetmeyebilirsiniz."
            },
			{   # 6. ev Akrep - güvensizlik hissi
                "id": "insecurity_6",
                "type": "house_sign_is",
				"house": 6,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 6.evinizdeyse sağlığınız hakkında endişeleriniz olabilir."
            },
			{   # 7. ev Akrep - güvensizlik hissi
                "id": "insecurity_7",
                "type": "house_sign_is",
				"house": 7,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 7.evinizdeyse evlilik korkunuz olabilir."
            },
			{   # 8. ev Akrep - güvensizlik hissi
                "id": "insecurity_8",
                "type": "house_sign_is",
				"house": 8,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 8.evinizdeyse biriyle yakınlaşmak sizi korkutabilir."
            },
			{   # 9. ev Akrep - güvensizlik hissi
                "id": "insecurity_9",
                "type": "house_sign_is",
				"house": 9,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 9.evinizdeyse eğitim hayatınızda kendinize güvenmeyebilirsiniz."
            },
			{   # 10. ev Akrep - güvensizlik hissi
                "id": "insecurity_10",
                "type": "house_sign_is",
				"house": 10,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 10.evinizdeyse kariyerinizde kendinize yeteri kadar güven duymayabilirsiniz."
            },
			{   # 11. ev Akrep - güvensizlik hissi
                "id": "insecurity_11",
                "type": "house_sign_is",
				"house": 11,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 11.evinizdeyse arkadaş ortamında kendinizi güvensiz hissedebilirsiniz."
            },
			{   # 12. ev Akrep - güvensizlik hissi
                "id": "insecurity_12",
                "type": "house_sign_is",
				"house": 12,
				"sign": "Akrep",
                "title": title,
                "text": "Akrep burcu 12.evinizdeyse bilinçaltınızda derin güvensizlikler olabilir."
            }
		]
	def _shame_reasons_notes(self) -> List[Dict]:
		title = "Lilith'in Ev Konumu Hangi Konularda Utandığınızı Anlatır"
		return [
            {   # 1. ev Lilith - utanç konuları
                "id": "shame_reasons_1",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 1.evinizdeyse belki de kendinizi her ifade etmeye çalıştığınızda yargılandığınızı hissediyorsunuz, görünüşünüzden, tarzınızdan, tavrınızdan utanıyorsunuz hatta hayatınızın bir döneminde insanlar sizi bu konularda eleştirmiş olabilir."
            },
			{   # 2. ev Lilith - utanç konuları
                "id": "shame_reasons_2",
                "type": "planet_in_house",
				"house": 2,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 2.evinizdeyse sahip oldugunuz paradan utanabilirsiniz, mal varlığınızı gizlemeye meyilli olabilirsiniz, yeteneklerinizi açığa çıkartmaktan utanabilirsiniz. İnsanlar yeteneklerinizi küçümsemiş olabilir ve siz de kendinizi yetersiz hissetmiş olabilirsiniz."
            },
			{   # 3. ev Lilith - utanç konuları
                "id": "shame_reasons_3",
                "type": "planet_in_house",
				"house": 3,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 3.evinizdeyse fikirlerinizden utanmış olabilirsiniz ya da ses tonunuzdan... Konuşmaktan korkmuş olabilirsiniz. İletişim tarzınız alay konusu olmuş olabilir ya da insanlar sizi kardeşlerinizden vurmuş olabilir, kardeşlerinizle olan ilişkiniz alay konusu olmuş olabilir. Ya da belki de doğrudan kardeşiniz, kuzenleriniz, akrabalarınız sizinle alay etti."
            },
			{   # 4. ev Lilith - utanç konuları
                "id": "shame_reasons_4",
                "type": "planet_in_house",
				"house": 4,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 4.evinizdeyse ailenizde dışlanmış olabilirsiniz. Evde kabul görmediginizi hissetmiş olabilirsiniz. Çocukken yaptığınız bir şey yüzünden çok utanıyor olabilirsiniz. İnsanlar sizin nerden geldiğinizi yani kökeninizi çok fazla eleştirilebilir, sizi ailenizden vurmaya çalışabilirler. Aile içinde de sizinle alay eden insanlar olabilir."
            },
			{   # 5. ev Lilith - utanç konuları
                "id": "shame_reasons_5",
                "type": "planet_in_house",
				"house": 5,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 5.evinizdeyse flört ederken çok utanabilirsiniz. İnsanlar sizin aşk hayatınızı alay konusu edebilirler, flört etme tarzınız çok eleştirilebilir. Eğlenceyi hak etmediğinizi düşünebilirsiniz. İnsanlar sizin eğlence tarzınızı da çok eleştirirler, yargılarlar. Çocukken canlı oluşunuz nedeniyle insanlar sizi eleştirmiş olabilir ve siz de sonucunda eğlenceden kendinizi mahrum etmiş olabilirsiniz."
            },
			{   # 6. ev Lilith - utanç konuları
                "id": "shame_reasons_6",
                "type": "planet_in_house",
				"house": 6,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 6.evinizdeyse iş ortamında belki iş arkadaşlarınız belki de patronlarınız tarafından aşağılanmış olabilirsiniz. iş yerindeki performansınız beğenilmemiş olabilir. Bedeniniz, sağlığınız alay konusu olabilir. Her gün yaptığınız bir şey insanların diline dolanabilir."
            },
			{   # 7. ev Lilith - utanç konuları
                "id": "shame_reasons_7",
                "type": "planet_in_house",
				"house": 7,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 7.evinizdeyse bir partner sizi aşağılamış ve çok utandırmış olabilir. İlişkilerde kendinizi yetersiz hissedebilirsiniz, sürekli yanlış bir şeyler yaptığınızı düşünebilirsiniz. Eski sevgililerinizden çok utanabilirsiniz."
            },
			{   # 8. ev Lilith - utanç konuları
                "id": "shame_reasons_8",
                "type": "planet_in_house",
				"house": 8,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 8.evinizdeyse biriyle beraberlik yaşamaktan korkabilirsiniz çünkü güven sorunlarınız olabilir. Birine bir sır verebilirsiniz daha sonra o kişi o sırrı herkese yayar ve bu alay konusu olabilir. Sınırlarınızın ihlal olduğunu hissedebilirsiniz. Korkularınız olabilir ve bu korkularınız nedeniyle utanabilir ya da utandırılabilirsiniz."
            },
			{   # 9. ev Lilith - utanç konuları
                "id": "shame_reasons_9",
                "type": "planet_in_house",
				"house": 9,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 9.evinizdeyse inançlarınızı gizleyebilirsiniz neye inandığınızı söylemek istemeyebilirsiniz. Insanlar sizin egitim durumunuzu aşağılayabilir. Yaşam felsefenizi saçma bulabilirler. Fikirleriniz eleştirilebilir. Belki uzaklara gitmek istersiniz ama insanlar bunu alay konusu yapabilir."
            },
			{   # 10. ev Lilith - utanç konuları
                "id": "shame_reasons_10",
                "type": "planet_in_house",
				"house": 10,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 10.evinizdeyse toplum önünde yaptıklarınız eleştirilebilir. Kariyerinizde birileri sizi yaptıklarınız nedeniyle eleştirir. Başarınız küçümsenir, sizi kıskanan, sizi çekemeyen çok fazla insan olabilir."
            },
			{   # 11. ev Lilith - utanç konuları
                "id": "shame_reasons_11",
                "type": "planet_in_house",
				"house": 11,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 11.evinizdeyse kime arkadaş dediğinize dikkat etmelisiniz, sizi eleştiren, sizinle alay eden insanlardan uzak durmalısınız. Sosyal medyada bir gün linç de yiyebilirsiniz. Bazı gruplardan dışlanabilirsiniz ya da yanlış anlaşılabilirsiniz."
            },
			{   # 12. ev Lilith - utanç konuları
                "id": "shame_reasons_12",
                "type": "planet_in_house",
				"house": 12,
				"planet": "Lilith ⚸",
                "title": title,
                "text": "Lilith 12.evinizdeyse kendi kendinizden utanabilir, kendi kendinizin düşmanı olabilirsiniz. Bilinçaltınızda bir utanç teması yatabilir. Gördüğünüz rüyalardan utanabilirsiniz. Gizli kompleksleriniz olabilir, korkularınız olabilir. Kendinizi görünmez, anlaşılmamış ve yanlış hissedebilirsiniz."
            },
        ]
	def _universe_protection_notes(self) -> List[Dict]:
		title = "Jüpiter'in Bulunduğu Ev Evrenin Sizi Nelerden Koruyabileceğini Gösterir"
		return [
            {   # 1.ev Jüpiter - evrenin koruması
                "id": "universe_protection_1",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 1.evinizdeyse zaten şans mıknatısı olabilirsiniz, sürekli korunduğunuzu hissedebilirsiniz hatta bulunduğunuz ortama da şans getirebilirsiniz."
            },
			{   # 2.ev Jüpiter - evrenin koruması
                "id": "universe_protection_2",
                "type": "planet_in_house",
				"house": 2,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 2.evinizdeyse bir para çıkışı olur ama bu sizi korumak içindir."
            },
			{   # 3.ev Jüpiter - evrenin koruması
                "id": "universe_protection_3",
                "type": "planet_in_house",
				"house": 3,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 3.evinizdeyse bir otobüs kaçar, taksi gelmez, arabanız çalışmaz ve bu sizin hayrınızadır aslında."
            },
			{   # 4.ev Jüpiter - evrenin koruması
                "id": "universe_protection_4",
                "type": "planet_in_house",
				"house": 4,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 4.evinizdeyse çıkmak istediginiz ev bir türlü olmuyordur ama belki de evren sizi komşu sıkıntısından kurtarmaya çalışıyordur."
            },
			{   # 5.ev Jüpiter - evrenin koruması
                "id": "universe_protection_5",
                "type": "planet_in_house",
				"house": 5,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 5.evinizdeyse sizin fırsat sandığınız yatırım belki de başka bir şey çıkacaktı o yüzden istediginiz olmadı."
            },
			{   # 6.ev Jüpiter - evrenin koruması
                "id": "universe_protection_6",
                "type": "planet_in_house",
				"house": 6,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 6.evinizdeyse istedigim işe giremedim diye üzülmeyin belki de o işte mobbinge uğrayacaktınız."
            },
			{   # 7.ev Jüpiter - evrenin koruması
                "id": "universe_protection_7",
                "type": "planet_in_house",
				"house": 7,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 7.evinizdeyse jüpiter var evren sizi kötü iş ortaklıklarından, anlaşmalardan korur. İstediğiniz kişinin sizi sevmemesinde de bir hayır olabilir."
            },
			{   # 8.ev Jüpiter - evrenin koruması
                "id": "universe_protection_8",
                "type": "planet_in_house",
				"house": 8,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 8.evinizdeyse verdiginiz borç size gelmedi mi, olsun daha fazlası gelir."
            },
			{   # 9.ev Jüpiter - evrenin koruması
                "id": "universe_protection_9",
                "type": "planet_in_house",
				"house": 9,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 9.evinizdeyse belki de o seyahate çıkmamanızda bir hayır vardır..."
            },
			{   # 10.ev Jüpiter - evrenin koruması
                "id": "universe_protection_10",
                "type": "planet_in_house",
				"house": 10,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 10.evinizdeyse belki de o terfi size verilmedi ama daha iyisi gelecektir."
            },
			{   # 11.ev Jüpiter - evrenin koruması
                "id": "universe_protection_11",
                "type": "planet_in_house",
				"house": 11,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 11.evinizdeyse evren sizi zararlı arkadaşlıklardan koruyor olabilir."
            },
			{   # 12.ev Jüpiter - evrenin koruması
                "id": "universe_protection_12",
                "type": "planet_in_house",
				"house": 12,
				"planet": "Jüpiter ♃",
                "title": title,
                "text": "Jüpiter 12.evinizdeyse zaten ilahi koruma altındasınız unutmayın."
            }
        ]
	def _twins_luck_notes(self) -> List[Dict]:
		title = "Haritanızda İkizler Burcunun Bulunduğu Bu Hayatta Birden Fazla Neye Sahip Olabileceğinizi Gösterir"
		return [
            {   # 1. ev İkizler- birden fazla..
                "id": "twins_luck_1",
                "type": "house_sign_is",
				"house": 1,
				"sign": "İkizler",
                "title": title,
                "text": "Yükseleniniz İkizler'se çift yönlü bir kişilik sergileyebilirsiniz, maskeleriniz olabilir mesela."
            },
			{   # 2. ev İkizler- birden fazla..
                "id": "twins_luck_2",
                "type": "house_sign_is",
				"house": 2,
				"sign": "İkizler",
                "title": title,
                "text": "2. eviniz İkizler'se birden fazla yeteneğiniz vardır."
            },
			{   # 3. ev İkizler- birden fazla..
                "id": "twins_luck_3",
                "type": "house_sign_is",
				"house": 3,
				"sign": "İkizler",
                "title": title,
                "text": "3. eviniz İkizler'se birden fazla okul (ilkokul, lise gibi) değiştirmiş olabilirsiniz."
            },
			{   # 4. ev İkizler- birden fazla..
                "id": "twins_luck_4",
                "type": "house_sign_is",
				"house": 4,
				"sign": "İkizler",
                "title": title,
                "text": "4. evinizde İkizler varsa birden fazla eviniz olabilir mesela yazlığınız olur."
            },
			{   # 5. ev İkizler- birden fazla..
                "id": "twins_luck_5",
                "type": "house_sign_is",
				"house": 5,
				"sign": "İkizler",
                "title": title,
                "text": "5. evinizde İkizler varsa iyi olduğunuz birden fazla hobiniz vardır. Mesela hem resim yaparsınız hem müzikle ilgilenirsiniz."
            },
			{   # 6. ev İkizler- birden fazla..
                "id": "twins_luck_6",
                "type": "house_sign_is",
				"house": 6,
				"sign": "İkizler",
                "title": title,
                "text": "6. evinizde İkizler varsa hayatınızın bir döneminde meslek değiştirebilirsiniz ya da 2 işe aynı anda sahip olursunuz."
            },
			{   # 7. ev İkizler- birden fazla..
                "id": "twins_luck_7",
                "type": "house_sign_is",
				"house": 7,
				"sign": "İkizler",
                "title": title,
                "text": "7. evinizde İkizler varsa hayat boyu birden fazla ciddi ilişkiniz olabilir"
            },
			{   # 8. ev İkizler- birden fazla..
                "id": "twins_luck_8",
                "type": "house_sign_is",
				"house": 8,
				"sign": "İkizler",
                "title": title,
                "text": "8. evinizde İkizler varsa hayatınızda birden fazla dönüm noktası olabilir."
            },
			{   # 9. ev İkizler- birden fazla..
                "id": "twins_luck_9",
                "type": "house_sign_is",
				"house": 9,
				"sign": "İkizler",
                "title": title,
                "text": "9. evinizde İkizler varsa birden fazla okul okuyabilirsiniz."
            },
			{   # 10. ev İkizler- birden fazla..
                "id": "twins_luck_10",
                "type": "house_sign_is",
				"house": 10,
				"sign": "İkizler",
                "title": title,
                "text": "10. evinizde İkizler varsa hayatınızın bir döneminde meslek değiştirebilirsiniz ya da 2 işe aynı anda sahip olursunuz."
            },
			{   # 11. ev İkizler- birden fazla..
                "id": "twins_luck_11",
                "type": "house_sign_is",
				"house": 11,
				"sign": "İkizler",
                "title": title,
                "text": "11. evinizde İkizler varsa bir sosyal medya uygulamasında birden fazla hesabınız olabilir ya da birden fazla grup içerisinde yer alırsınız, dernekte faaliyet gösterebilirsiniz mesela."
            },
			{   # 12. ev İkizler- birden fazla..
                "id": "twins_luck_12",
                "type": "house_sign_is",
				"house": 12,
				"sign": "İkizler",
                "title": title,
                "text": "12. evinizde İkizler varsa üzgünüm, birden fazla gizli düşmanınız olabilir."
            },
        ]
	def _uranus_manifesto_notes(self) -> List[Dict]:
		title = "Bir şeyleri sadece izleyerek o şeyi hayatınıza çekebilirsiniz desem... Uranüs teknoloji, video, film, sinematografi, ani değişimler ve beklenmeyen süprizler gibi pek çok şeyle ilgilidir."
		return [
            {   # 1.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_1",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 1.evinizdeyse vlogları izleyerek manifest yapabilirsiniz. Hayalini kurduğunuz hayatı içeren şeyleri izleyin. Kendinizin en iyi versiyonu olmaya başlamanıza yardımcı olabilecek şeyleri hayatınıza çekme olasılığınız daha yüksek olduğundan size daha fazla ilham veren insanları izlemeniz gerekiyor."
            },
			{   # 2.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_2",
                "type": "planet_in_house",
				"house": 2,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 2.evinizdeyse lüks içerikler izleyin. Finansal bolluk içeren, insanların dünya nimetlerinden faydalandığı içerikler izleyin. Bu sayede geliriniz artabilir ya da beklenmedik hediyeler almaya başlayabilirsiniz. Eğer özsaygı konusunda sıkıntılarınız varsa özgüven yayan insanları izleyin. Kendileri hakkında iyi hisseden insanları sürekli izleyerek istediginiz özgüveni hayatınıza çekebilirsiniz."
            },
			{   # 3.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_3",
                "type": "planet_in_house",
				"house": 3,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 3.evinizdeyse istediğiniz arabaya sahip olan kişileri izlemelisiniz. Çok iyi bir içerik üreticisi de olabilirsiniz, bu tarz kişileri düzenli olarak izleyin, bir şeyler öğrenmeye çalışın."
            },
			{   # 4.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_4",
                "type": "planet_in_house",
				"house": 4,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 4.evinizdeyse rahat ev vloglarını izleyin veya aile merkezli içerikler tüketin. Hayalinizdeki evi içeren videoları izleyin. Ev ortamınızda bolluk bereket olur bu sayede. Daha fazla iç tasarım veya emlak videosu izlemelisiniz. Rahat bir hayatı olan insanları izleyerek daha fazla konfor, rahatlama ve dinlenmeyi hayatınıza çekebilirsiniz."
            },
			{   # 5.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_5",
                "type": "planet_in_house",
				"house": 5,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 5.evinizdeyse yaratıcı ya da romantik içerikler izleyin. Hobi videoları olabilir, eğlenceli deneyim videoları olabilir. Ünlü insanların içeriklerini tüketin, onların videolarını izlemek enerjilerini kendinize çekmenizi sağlayabilir. Mesela bu sayede daha popüler olabilirsiniz ya da neşeli, özgüvenli biri haline dönüşebilirsiniz."
            },
			{   # 6.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_6",
                "type": "planet_in_house",
				"house": 6,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 6.evinizdeyse sağlığınızı iyileştirmek için sağlık videoları izleyebilirsiniz ya da üretkenlikle aşamaşı videoları izleyin. Aniden hayalinizdeki yaşam tarzına mükemmel şekilde uyan bir iş teklifi alabilirsiniz bu sayede. Bir şeyleri derleyip düzenleyen insanların videolarını izleyebilirsiniz, alışkanlık videoları size iyi gelir. Hayatınızı bir rutine oturmak istiyorsanız rutin içeren videolar izleyin."
            },
			{   # 7.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_7",
                "type": "planet_in_house",
				"house": 7,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 7.evinizdeyse ilişki tavsiyeleri, düğün, ruh eşi enerjisiyle ilgili videolar izleyin. Bu sayede hayatınıza ruh eşinizi çekebilirsiniz. Mutlu evli çiftleri veya ciddi ilişkisi olan insanları izleyerek hayatınıza daha fazla romantizm katabilirsiniz. Ayrıca huzurlu yaşam içerikli insanları izleyerek daha huzurlu, dengeli ve uyumlu bir hayat yaratabilirsiniz. Eğer işiniz içerik üreticiliği ise sürekli olarak sponsorluk çeken insanları izleyerek daha fazla marka anlaşması imzalayabilirsiniz."
            },
			{   # 8.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_8",
                "type": "planet_in_house",
				"house": 8,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 8.evinizdeyse bol bol manifest videoları izleyin. Dönüşüm veya finansal yatırımlar hakkında videolar izleyin. Bu sayede borçlarınız azalabilir. Güçlü insanların videolarını sürekli izleyerek daha fazla güç elde edebilirsiniz. Ayrıca bu tekniği psişik yeteneklerinizi güçlendirmek için de kullanabilirsiniz. Zor bir hayat yaşamaktan aniden daha pozitif bir hayat yaşamaya geçen insanları izlemeniz gerekiyor. Acılarını güce nasıl dönüştüreceklerini bilen insanları izleyin."
            },
			{   # 9.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_9",
                "type": "planet_in_house",
				"house": 9,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 9.evinizdeyse bol bol seyahat vlogu izleyin ya da kişisel gelişim içerikleri tüketin. Bir bakarsınız yolculuğa çıkmışsınız. Hayatına sürekli olarak şans çeken ya da kendini dine adamış insanları izleyerek hayatınıza şans çekebilirsiniz. Hayatlarını iyileştiren ve bir şeyde daha iyi hale gelen insanları izleyerek büyüme, gelişme ve ilerleme kaydedebilirsiniz."
			},
			{   # 10.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_10",
                "type": "planet_in_house",
				"house": 10,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 10.evinizdeyse başarı hikayelerini izleyin, kariyerinde iyi yere gelmiş insanları izleyin. Tavsiye veren içerikler de olabilir. Olumlu davranışlarda bulunan insanları izleyerek siz de kariyer hayatınızı güzelleştirebilirsiniz. Hatta popüler insanları izleyin ve siz de popüler olun."
			},
			{   # 11.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_11",
                "type": "planet_in_house",
				"house": 11,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 11.evinizdeyse  arkadaşlıklarla ilgili videolar izleyin, hedef videoları izleyin. Bu sayede doğru insanlar aniden hayatınıza girebilir ya da hedefinizle alakalı önemli bir gelişme ortaya çıkar. Iyi arkadaşlara sahip kişilerin hayatını izleyin. Arkadaşlarıyla video çeken insanlardan daha fazla içerik izleyin. Ayrıca kendi hedeflerini sürekli olarak gerçekleştiren insanları izleyerek hedeflerinize ulaşabilirsiniz. Çok özel fırsatları kendilerine çekmiş insanları izleyerek özel fırsatları hayatınıza alabilirsiniz. "
			},
			{   # 12.ev Uranüs - manifest için izlencekler
                "id": "uranus_manifesto_12",
                "type": "planet_in_house",
				"house": 12,
				"planet": "Uranüs ♅",
                "title": title,
                "text": "Uranüs 12.evinizdeyse spiritüel içerikler izleyin, meditasyon videoları izleyin ya da rüya günlügü videoları izleyin. Kendilerini ve acılarını iyileştiren insanların videolarını izleyerek şifayı hayatınıza çekebilirsiniz. Ayrıca mucizeleri kendilerine çeken insanların daha fazla içeriğini izleyerek mucizeleri de hayatınıza çekebilirsiniz. Çok rahatlatıcı içerikler yapan insanları izleyerek daha fazla dinlenme ve rahatlamayı hayatınıza alabilirsiniz."
			},
        ]
	def _childhood_notes(self) -> List[Dict]:
		title = " 4.Evi Kesen Burca Göre Çocukluğunuz... "
		return [
            {   # 4.ev - Koç
                "id": "childhood_aries",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Koç",
                "title": title,
                "text": "4.ev Koç ise çocukluğunuzda çok fazla sorumluluk almış ve erken yaşlardan itibaren bağımsız olmaya zorlanmış olabilirsiniz. Kaotik bir çocukluk geçirmiş ve ne yazık ki muhtemelen etrafinızda şiddet eğilimleri olan insanların bulunduğu bir ortamda bulunmuş olabilirsiniz ama tabii ki de bu en kötü senaryodur. Huzurunuzu korumak için her zaman savaşmanız gerektiğini hissettmiş olabilirsiniz ve çocukluk travmalarının dogrudan bir sonucu olarak kimi ve neyi gerçekten sevdiğinizi düşünmeye başladınız ve o kişileri koruma dürtüsüne sahip oldunuz. Aile üyeleriyle sık sık tartışmalar yaşamış olabilirsiniz hatta belki de bugün bile aileyle ilgili herhangi bir şeyle başa çıkmanız zor olabilir. Kontrolcü aile üyelerine karşı direnmeye çalışmışsınızdır ve yalnız bırakılıp kendi isteklerinizi gerçekleştirmek istediğinizde ailenizde asi bir çocuk olarak görülmüş olabilirsiniz."
            },
			{   # 4.ev - Boğa
                "id": "childhood_taurus",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Boğa",
                "title": title,
                "text": "4.ev Boğa ise genel olarak oldukça güzel ve istikrarlı bir çocukluk geçirmiş olabilirsiniz. Ancak muhtemelen ailenizin finansal ve maddi kaynakları etrafında çok merkezlenmiş bir çocukluk geçirmiş olabilirsiniz. Finansal olarak istikrarlı olmak aileniz için çok önemliydi hatta oldukça zengin bir ailede büyümüş olabilirsiniz ve paranın hayatınızda önemli bir rol oynadığı öğretilmiş olabilir çünkü paranın hayatta istediğiniz hemen hemen her şeye erişimin bir yolu olduğu düşünülmüş olabilir. Bu tür bir çocukluk yetişkinliğinizde aynı türden maddi konforu istemenize ve kendinizi geçindirmek için çok çalışmanıza yol açan bir tür ayrıcalıklı çocukluk geçirmiş olmanızı sağlayabilir."
			},
			{   # 4.ev - İkizler
                "id": "childhood_gemini",
                "type": "house_sign_is",
                "house": 4,
				"sign": "İkizler",
                "title": title,
                "text": "4.ev İkizler ise eğlenceli ve öğrenme deneyimleriyle dolu bir çocukluk geçirmiş olabilirsiniz. Kardeşleriniz ve arkadaşlarınız, büyürken hayatınızdaki en önemli insanlar olabilir ve onların sizi anlayabilen tek kişiler gibi hissedebilirsiniz. Çocukluğunuzdan beri yetişkinlere karşı güvensizlik gösterebilir, onları sık sık sıkıcı bulabilirsiniz ve onları sadece eğlencenizi mahvetmek isteyen insanlar olarak görebilirsiniz. Büyürken onlar gibi olmayı reddetmiş ve içinizdeki çocuğu kaybetmek istememiş olabilirsiniz. Çocukluğunuzda kardeşlerinizle veya arkadaşlarınızla çok zaman geçirmiş, onlarla saatlerce oynayarak harika anılar yaratmış olabilirsiniz. Kötü şeylerden, gerçek hayattan, kaostan kaçmak için hayal gücünüzü çalıştırıp kendi kendinizle de oyun oynamış olabilirsiniz."
			},
			{   # 4.ev - Yengeç
                "id": "childhood_cancer",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Yengeç",
                "title": title,
                "text": "4.ev Yengeç ise çocukluğunuz aile etkinlikleri etrafinda oldukça yoğun geçmiş olabilir. illa ki keyifli geçmiş diye bir şey yok ancak aile üyeleriyle çok fazla zaman geçirmek zorunda kalmanız vurgulanmış olabilir. Aile kavramı sizin için gerçek aile üyeleriniz dahil olmasa bile yine de çok önemli olabilir ve kendi arkadaşlarınız, eşiniz gibi sevdiklerinizle de bağlantıyı güçlü tutmak isteyebilirsiniz. Evinizin sevdikleriniz için güvenli bir alan olmasını sağlamaya çalışırsınız ve onları kendinize yakın tutmak için sevdiğiniz herkesin dahil olduğu ve ilgilenildiği, düzenli olarak yapılan akşam yemekleri ve sosyal toplantılar düzenleyebilirsiniz, harika bir ev sahibi olabilirsiniz."
			},
			{   # 4.ev - Aslan
                "id": "childhood_leo",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Aslan",
                "title": title,
                "text": "4.ev Aslan ise çocukluğunuzda çok fazla ilgi görmüş olabilirsiniz, belki de ailenizdeki çocuklar arasında en sevilenlerden biri olabilirsiniz. Ailenizin sosyal statüsüne büyük bir vurgu yapılmış olabilir ve bu l durum bugün bile etkisini sürdürüyor olabilir. Tanınmış ve prestijli bir aileye sahip olabilirsiniz. Aileniz belirli bir şekilde davranmanıza büyük önem vermiş olabilir, onları utandırmamak için sürekli gözlenmiş olabilirsiniz. Ailenizde gerçekten ünlü kişiler olabilir, bu da statünün aileniz için neden bu kadar önemli olduğunu açıklıyor olabilir. Aileniz her türlü doğum günü, mezuniyet gibi aile etkinliğinin kutlanmasına düşkün olabilir ve bu hala yapmak istediğiniz bir şey olabilir."
			},
			{   # 4.ev - Başak
                "id": "childhood_virgo",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Başak",
                "title": title,
                "text": "4.ev Başak ise çocukluğunuzda oldukça sıkı bir programin kural olduğu bir ortamda büyümüş olabilirsiniz, sürekli farklı ders dışı aktivitelerle meşgul olan ve birçok beceri, dil, sanat, spor vb. öğretilen bir çocuk olmuş olabilirsiniz. Rahatlamak için zaman bulmanız nadirdir ve hala kendinizi sürekli meşgul tutmak zorundaymışsınız gibi hissedebilirsiniz. Sanki belirli bir şey yapmadan zaman geçirmek bir tür zaman kaybıymış gibi hissediyor olabilirsiniz. Bu potansiyel olarak sizi bitkin düşüren bir durum olabilir ve hobileriniz veya başka bir şeyiniz yokmuş gibi hissediyor olabilirsiniz ancak yine de bunun için suçluluk duyabilirsiniz çünkü ailenizin beklentilerini karşılamak için yetenekli bir çocuk olarak görülmüş olabilirsiniz. Bir yetişkin olarak, kendinize zaman ayırmayı, gerçekten rahatlamayı ve eğlenmeyi öğrenmeniz gerekebilir çünkü bu gerçekten aşina olduğunuz bir şey olmayabilir. Üretken olarak görülmeyen bir şeyi yapmaktan hala derinlerde suçluluk duyabilirsiniz."
			},
			{   # 4.ev - Terazi
                "id": "childhood_libra",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Terazi",
                "title": title,
                "text": "4.ev Terazi ise çocukluğunuzda sessiz, başkalarıyla barışı koruyan ve aile üyeleri arasında arabuluculuk yapan biri olarak bir deneyim yaşamış olabilirsiniz. Yetişkin hayatınızda bile arkadaş grubunuzda veya çevrenizdeki insanlarla bir arada olmak ve herkesin en iyi şekilde geçinmesini sağlamak, çatışmaları çözmek için bir sorumluluk hissetmiş olabilirsiniz. Ayrıca hayatınızın çok erken dönemlerinde, herkese aynı şekilde davranmanın önemli olduğu hatta bunu yapmadığınızda veya belirli insanlara ve şeylere daha fazla ilgi gösterdiğinizde cezalandırılacağınız da öğretilmiş olabilir. Dengeyi saglamak burada kritik bir unsurdur."
			},
			{   # 4.ev - Akrep
                "id": "childhood_scorpio",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Akrep",
                "title": title,
                "text": "4.ev Akrep ise çocukluğunuzda başkalarıyla konuşmanın zor olduğu dönemler yaşamış olabilirsiniz ve bu yüzden bazı şeyleri genellikle gizli tutmuş olabilirsiniz. Ailenizdeki birçok kişi arasında sağlıksız güç dinamikleri olabilir ve sadakatinizin nerede olduğunu sorgulamış olabilirler. Sevdiklerinize karşı güçlü bir sadakat duygusu geliştirmiş olabilirsiniz, hatta size acı çektirenlere bile... Çünkü çocukluk size insanlarla aynı cehennemde yaşamanın aynı zamanda güçlü bağlar kurmak anlamına geldiğini öğretmiş olabilir. Ancak bu doğru değildir."
			},
			{   # 4.ev - Yay
                "id": "childhood_sagittarius",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Yay",
                "title": title,
                "text": "Çocukluğunuz çok farklı geçmişlere (çeşitli kültürler, dinler, farklı diller konuşan insanlar) sahip insanlarla çevrili bir ortamda geçmiş olabilir. Bu sizi erken yaşlardan itibaren hoşgörülü ve açık fikirli bir birey yapmış olabilir ve hatta bu size çocukken tanıştığınız insanlar nedeniyle dünyayı daha fazla keşfetme isteği uyandırmış olabilir. Başka bir (veya birkaç) ülkede büyümüş ve çocukluk döneminde sık sık taşınmış olmanız bir yere aitmiş gibi hissetmenizi zorlaştırabilir. Bu durum sık sık taşınmayı ve aynı yerde uzun süre kalmamayı sevmek olarak yansıyabilir. Öte yandan çocukluğunuzda böyle bir deneyim yaşamamışsanız uzun bir süre ev diyebileceğiniz bir yeri arayacaksınız."
			},
			{   # 4.ev - Oğlak
                "id": "childhood_capricorn",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Oğlak",
                "title": title,
                "text": "4.ev Oğlak ise çocukluğunuzda her zaman en iyi şekilde davranmanız gerektigi hatırlatılmış olabilir, aslında olduğunuz çocuk gibi davranmanıza pek izin verilmemiş gibi hissedebilirsiniz. Gerçek yaşınızda davrandığınız her an rahatsızlık gibi bile algılanmış olabilir. Size sorumluluk sahibi olmanız öğretildi ve etrafınızdaki birçok yetişkinden daha fazla sorumluluk almanız gerekebilir. Bu ilişkilerinizde hala devam eden bir kalıp olarak karşınıza çıkabilir, ne olursa olsun başkalarının yanında olmanız ve sürekli olarak iyi olduklarından ve gerektiğinde size güvenebileceklerinden emin olmanız gerektigini hissedersiniz. Bu süreçte kendi ihtiyaçlarınızı çok fazla unutmuş olabilirsiniz. Büyürken, aileniz küçük yaştan itibaren size daha fazla baskı uygulayacağı konusunda sık sık hatırlatma yapmış olabilir bu da ilerleyen dönemlerde sizin altyapınızda kendini göstermiş olabilir."
			},
			{   # 4.ev - Kova
                "id": "childhood_aquarius",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Kova",
                "title": title,
                "text": "Çocukluğunuzda, çevrenizdekilerden, ailenizden ve arkadaşlarınızdan çok farklı hissetmiş olabilirsiniz ve bu durum zaman zaman izole hissetmenize neden olabilir. Gerçekten uyum sağladığınızı hissetmediniz ve bunun istediğiniz olup olmadığını bile bilmediniz. Bu kafa karıştırıcı bir süreç olmuş olabilir ve başkalarıyla bağlantı kurmak için deneme yanılma süreci yaşamış olabilirsiniz. Diğer çocuklar ve aileleri tarafından genellikle garip biriymişsiniz gibi görülmüş olabilirsiniz, bu da farklılıklarınız nedeniyle dışlanmanıza ve kendi aileniz içinde bile değersiz görülmenize yol açmış olabilir. Bu çocukken nasıl adlandıracağınızı ve başa çıkacağınızı bilmediğiniz durumlarla alakalı olabilir, örneğin alevi olmak gibi..."
			},
			{   # 4.ev - Balık
                "id": "childhood_pisces",
                "type": "house_sign_is",
                "house": 4,
				"sign": "Balık",
                "title": title,
                "text": "4.ev Balık ise çocukluğunuzda çelişkili deneyimler yaşamış olabilirsiniz ve bunlar hayatınızın ilerleyen dönemlerine kadar anlam ifade etmemiş olabilir. Muhtemelen o dönemden kafa karıştırıcı anılarınız vardır çünkü belirli durumların karmaşıklığını kavrayamayacak kadar küçüktünüz ve birçok şeyi saklamış olabilirsiniz. Hayal gücünüze güvenmek ve her şeyi anlamlandırmak için kafanızda bir şeyler uydurmuş olabilirsiniz. Aile üyelerinizin bu tür konularla bağlantılı olmaları nedeniyle spiritüel ve hatta paranormal deneyimlerle karşılaşmış olabilirsiniz. Bu, bu tür konuların ortalama bir insana kıyasla sizin için neden daha az korkutucu olduğunu açıklayabilir."
			},
        ]
	def _father_figure_notes(self) -> List[Dict]:
		title = "Güneş'in ev konumu da baba figürü hakkında bilgi verir... Baba figürü diyorum çünkü belki de babanız değil dedeniz büyüttü sizi ve siz onu baba olarak gördünüz. "
		return [
            {   # 1.ev Güneş - baba ile ilişki
                "id": "father_figure_1",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 1.evinizdeyse babanıza hayran olabilirsiniz. Siz büyürken otoriter bir yapıya sahip olmuş olabilir ve sizi kendi uzantısı gibi görebilir. Bu nedenle, sınırlar konusunda zayıf olabilir ama yine de kendi seçimlerinizi yapmanıza, hayatınızı yaşamanıza izin vermek konusunda daha esnek olmuştur. Baba figürü, kendi kişiliğinizi geliştirme konusunda sizi teşvik etmiş olabilir ancak bazen kendi isteklerini ve arzularını size dayatmış olabilir. Bu nedenle, bazen bağımsızlığınızı kazanma konusunda zorluk çekmiş olabilirsiniz."
			},
			{   # 2.ev Güneş - baba ile ilişki
                "id": "father_figure_2",
                "type": "planet_in_house",
				"house": 2,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 2.evinizdeyse iyi bir ilişki geliştirebileceğiniz ve sizi şımartabilecek bir baba figürüne sahipsinizdir. Bu baba figürü şanslı bir geçmişe sahip olup olmadığınıza bakılmaksızın finansal işlerle oldukça meşgul olmuş olabilir ve kendi finansal alışkanlıklarınızı ondan almış olabilirsiniz. Harika zevklere sahip olabilir ve bu da onu sevilen bir figür yapabilir. Baba figürünüz güzel yemekler yapma, bahçecilik veya fırınlama gibi becerilerde yetenekli olabilir ve bu aktiviteleri sizinle paylaşarak size güvenli bir aile ortamı oluşturmuş olabilir."
			},
			{   # 3.ev Güneş - baba ile ilişki
                "id": "father_figure_3",
                "type": "planet_in_house",
				"house": 3,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 3.evinizdeyse çocukluğunuzda hayatınızda önemli bir yer tutan bir baba figürüne sahip olabilirsiniz. Bu baba figürü, çevresindeki herkes tarafından sevilen, komşuları tarafından beğenilen ve toplumda önemli olan bir figür olabilir. Konuşma ve yazma gibi yeteneklerde güçlü olmayabilir ancak pratik ve somut işlerde yetenekli olabilir. Baba figürü, sosyal yaşamda aktif ve insanlarla sürekli iletişimde olmayı seven biri olabilir. Bu nedenle, çocukluğunuzda sık sık sosyal etkinlikler düzenlemiş ve çevresindeki insanlarla güçlü ilişkiler kurmuş olabilir."
			},
			{   # 4.ev Güneş - baba ile ilişki
                "id": "father_figure_4",
                "type": "planet_in_house",
				"house": 4,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 4.evinizdeyse baba figürü, aileyle vakit geçirme konusunda çok büyük bir rol oynamış olabilir. Evde sık sık aile etkinlikleri düzenlemiş ve bu ortamı güvenli bir alan olarak göstermiş olabilir. Baba figürü, yemek pişirme, fırınlama veya bahçecilik gibi becerilerde yetenekli olabilir ve bu faaliyetleri sizinle paylaşarak evinizi bir tür sığınak gibi hissettirmiş olabilir. Aileyi bir arada tutma ve evde güvenliği sağlama konusunda büyük bir çaba göstermiş olabilir."
				},
			{   # 5.ev Güneş - baba ile ilişki
                "id": "father_figure_5",
                "type": "planet_in_house",
				"house": 5,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 5.evinizdeyse baba figürü, hobileriniz ve tutkularınızla yakından ilişki kurmuş olabilir. Hobilerini sizinle paylaşmış ve size kendi tutkularınızın değerini göstermiş olabilir. Baba figürü, sanatsal bir figür olabilir veya belirli bir hobiyle ilgili olabilir (örneğin spor, müzik veya başka bir sanat). Bu, sizin de bu hobileri benimsemenize ve kendi tutkunuzu keşfetmenize olanak sağlamış olabilir."
			},
			{   # 6.ev Güneş - baba ile ilişki
                "id": "father_figure_6",
                "type": "planet_in_house",
				"house": 6,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 6.evinizdeyse baba figürü sorumluluklarını yerine getiren ve işine çok bağlı bir ebeveyn olabilir. Muhtemelen her zaman oldukça meşgul olmuş olabilir ve iş hayatına çok zaman harcamış olabilir. Bu nedenle bazen sizi ihmal edilmiş hissettirmiş olabilir. Baba figürü, işine ve meslektaşlarına karşı oldukça tutkulu olabilir ve bu nedenle evde çok fazla zaman geçirmemiş olabilir. Bu durum, çocuklarının kişisel ihtiyaçlarını karşılamada eksiklikler yaratmış olabilir."
			},
			{   # 7.ev Güneş - baba ile ilişki
                "id": "father_figure_7",
                "type": "planet_in_house",
				"house": 7,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 7.evinizdeyse baba figürü başkaları için daha fazla ulaşılabilir olan bir konumda olabilir. Muhtemelen rastgele insanlara yardım etmeye her zaman hazır olmuş ve bu yüzden size daha az zaman ayırmış olabilir. Bu baba figürü, arkadaşlarınız gibi diğer insanlardan destek aramanıza yol açmış olabilir ve ne olursa olsun sizi destekleyecek özel bir kişi (partner) bulma ihtiyacı yaratmış olabilir. Baba figürü, başkalarının ihtiyaçlarına öncelik vermekle beraber sizin ihtiyaçlarınızı göz ardı etmiş olabilir ve bu da kendinizi yalnız veya yeterince desteklenmemiş hissetmenize yol açmış olabilir. "
			},
			{   # 8.ev Güneş - baba ile ilişki
                "id": "father_figure_8",
                "type": "planet_in_house",
				"house": 8,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 8.evinizdeyse baba figürü, sizin için birçok sırrı saklamış olabilir ve sizinle bazen sağlıksız bir duygusal bağ kurmuş olabilir. Hem gizlice hayran olunabilecek hem de hayatınızın ilerleyen dönemlerinde öğrendiğiniz şeyler için içerleyebileceğiniz bir baba figürüdür. Onu affetmek, kendinizi de affetmenize ve onun bir uzantısı olmadığınızı anlamanıza yardımcı olabilir. Baba figürü, hayatınızı yönetme şeklinizden utanç duyabilir ve bu, sizin hatalarınızı tekrarlayacağınız korkusundan kaynaklanmış olabilir. Sadece sizinle gurur duymak ister ancak kendi yaşam biçiminizi oluşturmanızdan rahatsızlık duyar. Sizi yönetme biçimine karşı bir tür çekimserlik hissedebilirsiniz bu nedenden ötürü."
			},
			{   # 9.ev Güneş - baba ile ilişki
                "id": "father_figure_9",
                "type": "planet_in_house",
				"house": 9,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 9.evinizdeyse baba figürü, inançlarınızı ve bilgiye yaklaşımınızı gerçekten şekillendirmiş olabilir. Size çok şey ögretmiş olabilir ve hayatta bilgili olmanın ne kadar önemli olduğunu vurgulamış olabilir. Kültürel veya dini geçmişine çok bağlı olabilir ve bu değerleri size de aktararak onların ne kadar önemli olduğunu öğretmiş olabilir. Bu büyürken ona tepki olarak uzaklaşmanıza yol açmış olabilir ve kendi yolunuzu bulma çabanızı artırmış olabilir."
			},
			{   # 10.ev Güneş - baba ile ilişki
                "id": "father_figure_10",
                "type": "planet_in_house",
				"house": 10,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 10.evinizdeyse baba figürü kariyerine ve itibarına çok fazla odaklanmış olabilir. Size bu şekilde başarılı olmanın doğru olduğunu öğretmiş olabilir ve bu nedenle sizin başarılı olmanızı istemiş olabilir. Baba figürü, iş yerinde gerçekten mücadele etmiş olabilir ve bu sizin kendi kariyerinizi oluşturmanızda daha istekli olmanıza yol açmış olabilir. Ancak genel olarak ona karşı yakın hissetmeyebilir ve kendi yolunuzu çizmeye çalışırken onun beklentilerini yerine getirmekte zorlanmış olabilirsiniz."
			},
			{   # 11.ev Güneş - baba ile ilişki
                "id": "father_figure_11",
                "type": "planet_in_house",
				"house": 11,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 11.evinizdeyse baba figürü hayallerinizi desteklemeye adamış bir figür olabilir. Hayallerinizi gerçekleştirmek için elinden gelen her şeyi yapmış olabilir ve hatta hayatını bu amaca adamış olabilir. Baba figürü sosyal amaçlara çok bağlı olabilir ve sizi de aynısını yapmaya teşvik etmiş olabilir. Onların desteğiyle hayallerinizi gerçekleştirmek için güçlü bir motivasyon bulmuş olabilirsiniz."
			},
			{   # 12.ev Güneş - baba ile ilişki
                "id": "father_figure_12",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Güneş ☉",
                "title": title,
                "text": "Güneş 12.evinizdeyse baba figürü çeşitli sebeplerden dolayı çok fazla tanıyamayadığınız bir figür olabilir. Bağımlılıkları olabilir. Marjinalleştirilmiş insanlarla çalışmış olabilir. Marjinalleştirilmiş bir sosyal grubun parçası olmak, size ortalama bir insandan daha derin bir anlayış kazandırmış olabilir ve dünyayı daha geniş bir perspektifle görmenizi sağlamış olabilir."
			}
        ]
	def _mother_figure_notes(self) -> List[Dict]:
		title = "Anneniz nasıl biri? Bunu Ay'ın yerleştiği evden okuyabiliriz..."
		return [
            {   # 1.ev Ay - anne ile ilişki
                "id": "mother_figure_1",
                "type": "planet_in_house",
				"house": 1,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 1. evde ise duygularını yoğun bir şekilde gösteren bir anne figürü ile büyümüş olabilirsiniz. Bu durum sizin de aynı şekilde davranmanıza veya kendi duygularınıza alan bulamamanıza neden olmuş olabilir. Anne figürünüz sizinle çok fazla özdeşleşmiş ve sağlıksız duygusal bağlar geliştirmiş olabilir. Bu bağlamda kendi bireysel alanınızı yaratmakta zorlanmış olabilirsiniz."
			},
			{   # 2.ev Ay - anne ile ilişki
                "id": "mother_figure_2",
                "type": "planet_in_house",
				"house": 2,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 2. evde ise sizi çok seven ve şımartan bir anne figürü ile büyümüş olabilirsiniz. Çocukken 'favori çocuk' gibi hissetmiş olabilirsiniz. Finansal konularla yoğun bir şekilde meşgul olan bir anne figürü olabilir. Onun finansal sorunlara yaklaşımını örnek almış olabilirsiniz. Ayrıca zevk sahibi olması ve estetik anlayışı ile çevresinde takdir edilen bir figür olabilir."
			},
			{   # 3.ev Ay - anne ile ilişki
                "id": "mother_figure_3",
                "type": "planet_in_house",
				"house": 3,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 3. evde ise her şeyi rahatça konuşabildiğiniz, iletişim kurmaya önem veren bir anne figürü olabilir. Çocukken arkadaş edinmenizi ve çevrenize uyum sağlamanızı desteklemiş olabilir. Anne figürünüz, yazma ve konuşma gibi iletişim becerilerinde oldukça başarılı biri olarak sizi bu yönde teşvik etmiş olabilir."
			},
			{   # 4.ev Ay - anne ile ilişki
                "id": "mother_figure_4",
                "type": "planet_in_house",
				"house": 4,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 4. evde ise aile içinde favori bir konumda olmuş olabilirsiniz. Anne figürünüz, aile bağlarını güçlendirmeye önem veren biriydi. Evde sık sık aile etkinlikleri ve toplantılar düzenleyerek bu bağları korumayı amaçlamış olabilir. Ayrıca, size evin bir güven alanı olması gerektiğini öğretmiş olabilir. Yemek pişirme, bahçecilik veya evle ilgili diğer aktivitelerde yetenekli bir figür olabilir."
			},
			{   # 5.ev Ay - anne ile ilişki
                "id": "mother_figure_5",
                "type": "planet_in_house",
				"house": 5,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 5. evde ise sizinle gurur duyan ve başarılarınızı sık sık takdir eden bir anne figürü olabilir. Hayatına tutku ile yaklaşan, yaptığı işlerden heyecan duyan bir kişilik sergileyebilir. Kendi tutkularınızı geliştirmenin önemini size göstermiştir. Anne figürü sanatsal ya da yaratıcı yönleriyle dikkat çeken biri olabilir."
			},
			{   # 6.ev Ay - anne ile ilişki
                "id": "mother_figure_6",
                "type": "planet_in_house",
				"house": 6,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 6. evde ise bazı durumlarda, ebeveyn rolünü üstlenmek zorunda kaldığınız bir anne figürü olabilir. Duygusal ya da fiziksel olarak destek beklemek yerine, ona yardımcı olmanız gerekmiş olabilir. Çok meşgul bir hayat süren ve bu nedenle sizi ihmal edilmiş hissettiren bir anne figürü olabilir."
			},
			{   # 7.ev Ay - anne ile ilişki
                "id": "mother_figure_7",
                "type": "planet_in_house",
				"house": 7,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 7. evde ise anne figürünüz, aşk ve sevginin nasıl olması gerektiğine dair size özel bir bakış açısı kazandırmış olabilir. Bu durum, ilişkileriniz üzerinde güçlü bir etki yaratmış olabilir. Belki de arkadaşlarınızdan veya diğer insanlardan destek arama eğilimi geliştirmişsinizdir. Bu durum, hayatınızda ne olursa olsun sizi destekleyecek özel bir kişiyi (partneri) bulma ihtiyacı yaratmış olabilir."
			},
			{   # 8.ev Ay - anne ile ilişki
                "id": "mother_figure_8",
                "type": "planet_in_house",
				"house": 8,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 8. evde ise anne figürünüzle sağlıksız bir duygusal bağ geliştirmiş olabilirsiniz. Sır saklama ve bazı şeyleri gizli tutma konusunda etkisi olmuş olabilir. Anne figürünüz, hem gizlice hayranlık duyduğunuz hem de bazı geçmiş davranışlarından dolayı içerlediginiz biri olabilir. Onu affetmek, kendinizi de affetmenize ve onun hayatının bir uzantısı olmadığınızı anlamanıza yardımcı olabilir. Belki de onun geçmişteki hatalarını tekrarlamanızdan korktuğu için hayatınızı yönetme tarzınıza müdahale etmiş olabilir. Ancak sizinle gurur duymasını beklerken, bu korku aranızda bir gerginlik yaratmış olabilir."
			},
			{   # 9.ev Ay - anne ile ilişki
                "id": "mother_figure_9",
                "type": "planet_in_house",
				"house": 9,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 9. evde ise anne figürünüz, inançlarınızı ve bilgiye yaklaşımınızı derinden şekillendirmiş biri olabilir. Size Öğrenmenin ve bilgili olmanın önemini sıklıkla vurgulamış olabilir. Kültürel veya dini geçmişine çok bağlı bir figür olarak, bu değerleri size ögretmiş olabilir. Ancak, siz büyüdükçe, belki de bu inançlardan uzaklaşma ihtiyacı hissetmiş olabilirsiniz."
			},
			{   # 10.ev Ay - anne ile ilişki
                "id": "mother_figure_10",
                "type": "planet_in_house",
				"house": 10,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 10. evde ise anne figürünüzle duygusal anlamda yakın hissetmemiş olabilirsiniz. Kariyerine ve itibarına çok fazla odaklanmış bir anne figürü olabilir ve bu durumun doğru bir yaşam biçimi olduğunu size öğretmiş olabilir. Aynı zamanda, iş hayatında zorluklar yaşamış ve bu nedenle sizin daha başarılı olmanızı istemiş olabilir. Onun mücadeleleri, sizin başarıya olan motivasyonunuzu şekillendirmiş olabilir."
			},
			{   # 11.ev Ay - anne ile ilişki
                "id": "mother_figure_11",
                "type": "planet_in_house",
				"house": 11,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 11. evde ise anne figürünüz, sosyal amaçlar ve aktivizm konularına çok ilgi duymuş olabilir. Sizi de bu tür çalışmalara teşvik etmiş olabilir. Kendisinin büyük hayalleri olmuştur ya kendi hayallerini sizin gerçekleştirebilmenizi istemiş ya da kendi hedeflerinize ulaşmanız için sizi motive etmiş olabilir."
			},
			{   # 12.ev Ay - anne ile ilişki
                "id": "mother_figure_12",
                "type": "planet_in_house",
				"house": 12,
				"planet": "Ay ☽",
                "title": title,
                "text": "Ay 12. evde ise anne figürünüzle zor bir ilişkiniz olmuş olabilir. Belki de anne figürünüz hayatınızda çok aktif bir rol oynamamış ya da size destek olmamış biridir. Daha kötüsü, bazı durumlarda başınıza gelen iyi şeyleri sabote etmeye çalışmış olabilir. Hatta bağımlılık gibi ciddi sorunlar yaşamış bir anne figürüyle büyümüş olabilirsiniz."
			},
        ]
	def _life_teaching_notes(self) -> List[Dict]:
		title = " 8.Ev = Bu Hayatta Neyi Öğrenmeniz Gerekiyor?"
		return [
            {   # 8.ev - Koç
                "id": "life_teaching_aries",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Koç",
                "title": title,
                "text": "Başkalarının liderlik yapmasına izin vermekten korkmamayı öğrenin çünkü güven böyle inşa edilir. Sürekli her şeyle savaşmanız gerekmiyor zaten güçlü olduğunuzu, kazanabileceğinizi ve istediginizi elde edebileceginizi biliyorsunuz. Ancak uzlaşmayı öğrenmeye ve başkalarına kendilerini ifade etmeleri için öncelik tanımaya ne dersiniz? Başkalarının sizin adınıza karar vermesine izin vermek onların sizi kontrol edeceği veya geçmişte olduğu gibi bu gücü kötüye kullanacakları anlamına gelmez. Bazı insanlar gerçekten size yardım etmek ister. Yardım almayı kabul etmek tıpkı hasta olduğunuzda başkalarının sizin için bir şeyler yapmasına ihtiyaç duymanız gibi bir şeydir. İçinizdeki küçük çocuğa, herkesle tartışmak ve kavga etmek yerine barışmayı öğrenmesi gerektigini söyleyin. Çünkü o, ihtiyaçlarını nasıl ifade edeceğini bilmiyor. Artık siz bunu nasıl yapacağınızı biliyorsunuz, sesinizi bağırmak için değil duyulmak için kullanın."
			}, 
			{   # 8.ev - Boğa
                "id": "life_teaching_taurus",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Boğa",
                "title": title,
                "text": "Kendinizden ve sahip olduklarınızdan daha fazlasını paylaşmayı öğrenin. Hayatın sunduğu zevkleri derinlemesine deneyimleyebilmenin yolu rahatsızlıkları kabul etmekten geçer. Bir şeylerin ve hayatın çirkin tarafları hakkında konuşmayı veya en azından buna daha açık olmayı öğrenmelisiniz. Hiçbir şey mükemmel değildir ve bu gayet normaldir. İşlerin tam istediğiniz gibi gitmemesi başarısız olduğunuz veya kimsenin size güvenmeyeceği anlamına gelmez. Hepimiz hata yaparız ve bunu kabul edebilmek insanların yanınızda kalmasını sağlamanın anahtarıdır. İnsanlar hatalarınızdan dolayı sizden nefret etmez ancak bunu anlayacak olgunlukta degillerse zaten hayatınızda olmaları gereken kişiler değildir. Kimin ve neyin zamanınıza değer olduğunu her zaman bilemeyebilirsiniz. Bu yüzden, kendinizi fazla suçlamayın ve hem kendinizi hem de başkalarını affetmeyi öğrenin."
			}, 
			{   # 8.ev - İkizler
                "id": "life_teaching_gemini",
                "type": "house_sign_is",
                "house": 8,
				"sign": "İkizler",
                "title": title,
                "text": "Bilginizin bir gün işe yarayacağına güvenin. Ancak sürekli olarak bir gün anlam kazanacakları umuduyla gerçekleri toplamaya çalışarak zaman harcamayın. Bazı şeyler hiçbir zaman işe yaramayabilir ama sizin inanılmaz bir araştırma yeteneğiniz var, hatta başkalarının rahatsız edici bulabileceği şeyler hakkında bile. Zaman zaman yeni şeyler denemek isteyebilirsiniz, özellikle riskli görünüyorsa. Çünkü bu hayatınıza heyecan katar ve başkalarına anlatacak daha çok hikaye biriktirmenizi sağlar. Bu süreç korkularınızı azaltır. Bir şeyleri tamamlayamamak ya da ustalaşamamak sorun değildir, bazen önemli olan sonuç değil yaşanan deneyimdir. Herkesle aynı ögrenme sürecine sahip olmayabilirsiniz ama bu asla daha az zeki veya yetenekli olduğunuz anlamına gelmez. Hayatı keşfetme ve deneyimleme şekliniz benzersizdir, bundan utanmayın."
			}, 
			{   # 8.ev - Yengeç
                "id": "life_teaching_cancer",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Yengeç",
                "title": title,
                "text": "Kendinize güvenmekle başkalarına aşırı bağımlı olmak arasında bir denge kurmayı öğrenmeniz gerekiyor. Gerçek yakınlığı deneyimlemek istiyorsanız duygusal olarak açılmanız şart. Başkalarına yakınlaşmak ve kendinizle ilgili önemli şeyleri paylaşmak sizi zorlayan bir süreç olmak zorunda değil. Kendi hızınızda ilerleyebilir ve zamana yayabilirsiniz. Ancak bunun kişisel bir tercih olduğunu paylaştığınız kişilerin aynı şekilde karşılık verme zorunluluğu olmadığını bilmelisiniz. Bu, alınması gereken bir risktir. Güven ve karşılıklı destek üzerine kurulu, kırılganlığın paylaşıldığı harika ilişkiler inşa edebilirsiniz. Ama ne yazık ki, bu çabanız her zaman başkaları tarafından takdir edilmeyebilir ve bu da kabul edilmesi gereken bir gerçektir. Unutmayın, kendinizi tamamen başkalarına vermiyorsunuz. Ne kadarını paylaşacağınızı siz seçersiniz ve bu seçim hayatınızın kontrolünü kaybettiğiniz anlamına gelmez. Sonuçta, kendi kalbinizin sahibi ve koruyucusu yalnızca sizsiniz. Endişelenmeyin."
			}, 
			{   # 8.ev - Aslan
                "id": "life_teaching_leo",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Aslan",
                "title": title,
                "text": "8. Kendinizle gurur duymayı ve mükemmel olmasa bile yaptıklarınızı takdir etmeyi öğrenmelisiniz. Size övünmenin kibirli bir davranış olduğu ve bunun güvensizliğin bir işareti olduğu öğretilmiş olabilir. Belki de 'Değerini bilen biri, iltifat beklemez' gibi bir fikirlerle büyüdünüz. Ancak bu gerçekten doğru mu? Kendi degerinizin fark edilmesini istemek ve motive olabilmek için cesaretlendirilme ihtiyacı hissetmek gayet normaldir ve asla bir zayıflık göstergesi degildir. Bazı insanlar sizi bu yüzden utandırmaya çalışabilir. Kendinizi ifade ettiğinizde, sizi küçümseyerek veya alenen eleştirerek kendinizi bir daha asla iyi hissetmemenizi umabilirler. Ancak bu onların kendi güvensizliklerinden kaynaklanır ve sizin kendiniz hakkında olumlu düşünmenizle ilgisi yoktur. Kendi değerinizi bilmek ve bunu sahiplenmekten utanmayın."
			}, 
			{   # 8.ev - Başak
                "id": "life_teaching_virgo",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Başak",
                "title": title,
                "text": "Hayatınızın zorluklarından ve en kötü anlarından sürekli bir şeyler öğrenme eğilimindesiniz. Ancak bazen konuşulması zor veya travmatik konular bulamamak sizi hayal kırıklığına ugratabilir. Yine de herkesin sizinle aynı şekilde olmadığını ve bu tür konuşmaları kaldıramayabileceğini anlamanız gerekiyor. Bu tarz konular sizin için büyüleyici olabilir ama bu durum herkes için geçerli değildir. Yine de tüm bu yaşananların anlamını bulmak için derinlemesine araştırma yapma hakkınız var. Başkalarının rahatsız olması bu ihtiyacınızdan vazgeçmeniz gerektiği anlamına gelmez (sadece bulduğunuz sonuçları kendinize saklamanız daha iyi olabilir). Hayatınızda neye ihtiyaç duyduğunuzu anlamak konusunda güçlü bir sezgiye sahipsiniz ve bunu kesinlikle kullanmalısınız. Ancak unutmayın, sadece siz karanlıklarınızla yüzleşmekte rahat olduğunuz için başkalarını da kendi karanlıklarıyla yüzleşmeye zorlamayın."
			}, 
			{   # 8.ev - Terazi
                "id": "life_teaching_libra",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Terazi",
                "title": title,
                "text": "Ne istediğinizi ve neye ihtiyacınız olduğunu ifade etmenin doğru yolunu bulmayı öğrenin. Ancak bu süreçte başkalarının hoşuna gitmeyebilir diye kalbinizin arzuladığı şeylerden sürekli kendinizi mahrum bırakmamalısınız. Tüm hayatınızı yalnızca başkalarının duygularına hitap ederek ve kendiniz için hiçbir şey yapmadan geçirmek gerçekten istediğiniz șey mi? Kabul edelim, eğer bazen kendinizi seçmezseniz bunu sizin için kim yapacak? Bu nedenle kendinizi seçmeyi başkalarına karşı bir haksızlık olarak görmeme fikrini benimsemelisiniz. Kendinize ve başkalarına adil olmanın birden fazla yolu vardır bu sadece bir tarafa odaklanmak zorunda değildir. Ayrıca hayatın seçimler içerdiğini, her şeyi aynı anda yapamayacağınızı ama doğru olanları - sizi en mutlu edecek olanları - yapacağınıza güvenmeniz gerektiğini hatırlatmalısınız. Evren sizinle, yanlış cevaplar ya da yanlış yollar yoktur."
			}, 
			{   # 8.ev - Akrep
                "id": "life_teaching_scorpio",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Akrep",
                "title": title,
                "text": "Dünyaya açılmayı ve herkesin düşmanınız olmadığını öğrenmelisiniz. Güven karmaşık testlerden geçmeden de verilebilir, insanların size güvenmek için yalnızca sözlerinize inanması yeterlidir. Başkalarının kendilerini size kanıtlamak zorunda kalması haksızlık değil mi? Sizi inciten insanların kullandığı manipülatif yöntemleri tekrar etmemelisiniz. Güven, korkunun getirdigi kontrolcü davranışlarla değil açık bir kalple inşa edilir. Evet, güvenmek ve kalbinizi açmak risk içerir, hayal kırıklığı veya zarar görmek gibi. Ancak bu risklerle birlikte daha büyük ödüller gelir. Kendinize hatırlatmanız gereken şey, ne kadar çok verirseniz o kadar çok alacağınızdır, hatta beklediğinizden fazlasını bile."
			}, 
			{   # 8.ev - Yay
                "id": "life_teaching_sagittarius",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Yay",
                "title": title,
                "text": "Kendi ruhunuzun derinliklerini keşfetmeye istekli olmayı öğrenmeli ve keşfedeceğiniz şeyler karşısında açık fikirli olmalısınız. En karanlık düşünceleriniz bile yargılanmayı veya korkulmayı hak etmez, oldukları gibi kabul edilmelidir. Eğer bu düşünceler sizi aşırı zorluyorsa bir terapist gibi profesyonel bir destek almayı düşünmelisiniz. Kendinizde saklamanız gereken ya da sürekli dikkatinizi başka şeylere yönlendirmek zorunda olduğunuz kadar korkunç, utanç verici veya ürkütücü hiçbir şey yok. Belki de sizin kabul etmekte zorlandığınız ve başkalarının sizi nasıl algıladığını düşündüğünüzle ilgisi olmayan daha fazla parçanız vardır. Kendinizdeki bu projeksiyonu fark etmelisiniz. Ayrıca hayatın keşif yolculuğunda daha derinlere inemediğinizi ya da daha uzağa gidemediğinizi düşünüyor ve bu durumdan dolayı utanıyor olabilirsiniz. Ancak acele etmeyin. Kendinizi neden zorladığınızı ve bu şekilde daha fazla içsel sınırlama yarattığınızı sorgulayın. Zamanla her şey yerine oturacaktır."
			}, 
			{   # 8.ev - Oğlak
                "id": "life_teaching_capricorn",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Oğlak",
                "title": title,
                "text": "Zaferlerinize ve başarısızlıklarınıza yaklaşımınızda bir denge kurmayı öğrenmelisiniz. Tamamen gerçekçi ya da tamamen duygusal olmak zorunda değilsiniz. En kötü anlarınızla gerçekçi bir şekilde başa çıkmayı tercih etseniz ve olayları mantıklı hale getirmeye çalışsanız bile korkmayun, duygusal teselli ve destek isteme hakkınız her zaman vardır. Başkalarının, sizin acılarınızı 'soğuk' ya da başka bir şekilde değerlendirme biçimlerine göre hareket etmek zorunda değilsiniz. Onların bunu kabul etmesi gerekir. En derin hayal kırıklıklarınız ve acılarınızla başa çıkmak için başkalarına güvenmek zorunda değilsiniz, bu tamamen sizin özel alanınızdır. Ancak güvendiğiniz birine kalbinizdeki duyguları açmanın ve anlaşılmış hissetmenin ne kadar rahatlatıcı olabileceğini de unutmamalısınız. Bu bağımlılık veya zayıflık değil, insan olmanın bir parçasıdır."
			},
			{   # 8.ev - Kova
                "id": "life_teaching_aquarius",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Kova",
                "title": title,
                "text": "Hayatta her şeyi tek başınıza yaşamak zorunda olmadığınızı ve yalnız olmadığınızı anlamayı öğrenmelisiniz. Bazen, başkaları tarafından dahil edilmek istemekten o kadar utanabilirsiniz ki 'yapışkan' ya da zayıf bir birey olarak görünmek istemezsiniz. Ancak başkalarıyla bağlantı kurma izni vermediğinizde farkında olmadan kendinizi dışlayabilirsiniz. Başkaları için her zaman orada oluyorsunuz, öyleyse onların da sizin için orada olmasının abartılı bir fikir gibi gelmesine neden izin veriyorsunuz? İnsanların sizinle ilgilenmesine alan tanımalı ve onların denemelerine izin verdiğinizi göstermelisiniz. Bazen başkaları size ne zaman destek olmaları gerektiğini anlamak için yalnızca küçük bir işarete ihtiyaç duyar."
			},
			{   # 8.ev - Balık
                "id": "life_teaching_pisces",
                "type": "house_sign_is",
                "house": 8,
				"sign": "Balık",
                "title": title,
                "text": "Hayallerinize inanmayı ve onları gerçekleştirmeyi hak ettiğinizi kabul etmeyi öğrenmelisiniz. Kendinizi isteklerinizin gerçekçi olmadığını veya çocukça olduğunu düşünmekten alıkoymalısınız. Belki de çevrenizden 'Büyümen gerek' türünden eleştiriler veya bakışlar almış olabilirsiniz ancak bu hayallerinizi küçümsemeniz gerektiği anlamına gelmez. Duygularınızı düzenleyememek ya da onlarda boğulmak konusunda derin bir utanç duymanız da muhtemeldir. Öfkenizi, üzüntünüzü ya da diğer duygularınızı ifade etmeye çalışırken, nasıl başa çıkacağınızı bilmediğiniz için her şeyin yolundaymış gibi davranma eğilimi gösterebilirsiniz. Ancak bu davranış sizi içten içe daha çok yıpratır. Duygularınızı tanımak ve ifade etmek onları bastırmaktan çok daha sağlıklıdır."
			},
        ]
	def _fears_notes(self) -> List[Dict]:
		title = " 12.Ev ve Korkularımız.."
		return [
            {   # 12.ev - Koç
                "id": "fears_aries",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Koç",
                "title": title,
                "text": "Hayattan istediklerinizi açıkça ifade etmekten korkuyor olabilirsiniz çünkü bu durum başkaları tarafından küstah veya fazla talepkar olarak görülme kaygısını beraberinde getirebilir. Bu yüzden işler istediğiniz gibi gitmediğinde önemsemiyor gibi davranarak sakin kalmayı tercih edebilirsiniz. Ancak bu bilinçaltınızda bir öfke birikimine neden olabilir. Öfkenizden korkmak yerine onunla yüzleşmek ve uygun bir şekilde ifade etmek çok daha sağlıklı olacaktır. Ofke kötü bir duygu değildir aslında, hak ettiğinizi düşündüğünüz şeylere verdiğiniz bir tepki olarak olumlu bir işaret olabilir. Bu duyguyu bir düşman olarak değil, sizi harekete geçiren bir dost olarak görmeyi öğrenmek önemlidir."
			}, 
			{   # 12.ev - Boğa
                "id": "fears_taurus",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Boğa",
                "title": title,
                "text": "Dinlenme konusunda bilinçaltınızda bir engel olabilir, yeterince bir şey yapmadığınızda ya da hareket etmediğinizde tembel olarak görülmekten çekiniyor olabilirsiniz. Ancak sürekli bir şeylerle meşgul olmak sizi yıpratabilir. Kendinize zaman ayırmanın sizi geri götürmeyeceğini aksine daha iyi sonuçlar elde etmenize yardımcı olacağını kabul etmelisiniz. Iyi şeylerin zaman aldığını ve kendinize baskı yaparak sonuçları hızlandırmaya çalışmanın kaygınızı artıracağını hatırlamanız faydalı olacaktır."
			},
			{   # 12.ev - İkizler
                "id": "fears_gemini",
                "type": "house_sign_is",
                "house": 12,
				"sign": "İkizler",
                "title": title,
                "text": "Tutarlılık konusundaki endişeleriniz nedeniyle bir fikrinizi değiştirdiğinizde bunun sizi ciddiyetsiz biri gibi göstereceğinden korkabilirsiniz. Bu başkalarını hayal kırıklığına uğratma kaygısını da beraberinde getirebilir. Ancak değişkenliğinizi bir zayıflık değil bir güç olarak görmeyi ögrenmeniz gerekiyor. Zihinsel esneklik ve uyum sağlama yeteneğiniz sizi diğerlerinden farklı kılan güçlü bir özellik olabilir. Bununla birlikte özellikle başkalarını da planlarınıza dahil ettiğinizde son dakikada fikir değiştirmenin ve verilen sözleri tutmamanın olumsuz etkiler yaratabileceğini unutmamalısınız. Yapabileceğinizden emin olmadığınız bir şeyi taahhüt etmekten kaçınmalısınız. Planlara bağlı kalmak özellikle uzun vadede kendiniz için de faydalı olabilir. Aksi takdirde hiçbir şeyi tamamlayamamanın verdiği hayal kırıklığını yaşayabilirsiniz. Bu konuda farkındalık geliştirmek ve daha kararlı adımlar atmak kendinize olan güveninizi artıracaktır."
			},
			{   # 12.ev - Yengeç
                "id": "fears_cancer",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Yengeç",
                "title": title,
                "text": "Çok hassas ve kırılgan olduğunuzdan başkalarının sizi yeterince ciddiye almadığını düşünüyorsunuz. Bu nedenle kendi işlerinizi yapma konusunda endişe duyuyor ve korunmaya ihtiyaç duyuyormuş gibi davranıyorsunuz. Ancak aslında bu sadece normal bir durumdur ve bu şekilde görünmek bilinçaltınız için bir ihtiyaç olabilir. Diğer insanların ne kadar güçlü olabileceğinizi görmelerini ve sizi kendi sorunlarını yönetemeyen biri olarak düşünmemelerini istiyorsunuz. Aynı zamanda destek arıyor ve hayatın zorluklarıyla başa çıkarken yanınızda birinin olmasını umuyorsunuz. Bu tekrar küçük bir çocuk gibi hissetme ve ağlama ihtiyacınızı da içerir, en doğal duygularınızı göstermek ve olgunlaşmamış olarak yargılanmamak istiyorsunuz."
			},
			{   # 12.ev - Aslan
                "id": "fears_leo",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Aslan",
                "title": title,
                "text": "Kendi projelerinize ve hedeflerinize odaklanmak istediğinizde başkalarına bencil ve aşırı hırslı gibi görünebilirsiniz. Ancak bu durum dengeyi sağlamak için başkalarına yardım etmeye çalışmanıza neden olabilir. Başarı ve başarısızlık korkusu kendi kendini sabote etme endișesi yaratabilir. İçsel olarak başarı göstermek ve yeteneklerinizi kanıtlamak için bir çeye ihtiyaç duyuyorsunuz ama aynı zamanda daha önce başarısız olduğunuzda nasıl hissettiğinizi biliyorsunuz ve bu da güvensizliklerinizi artırıyor. İnsanların size gerçekten inandığını görmek istiyorsunuz çünkü tek destekçiniz kendiniz olması zor olabilir ve bu yüzden yorucu bir hale gelebilir. Çok fazla dikkat çekmek istemeyebilirsiniz, ancak başkalarına ne kadar yetenekli olduğunuzu göstermek için bir şans arıyorsunuz."
			},
			{   # 12.ev - Başak
                "id": "fears_virgo",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Başak",
                "title": title,
                "text": "Başarıya fazla odaklanarak herhangi bir tercihte bulunursanız herkese ve her şeye eşit davrandığınız konusunda suçlanmaktan korkuyorsunuz. Bu yüzden başkalarının sizden istediği her şeye evet demek zorunda hissediyorsunuz. Bilinçaltınızda her şeyin yolunda gitmesi için bir ihtiyaç var çünkü eğer siz yapmazsanız kimsenin aynı şekilde yapamayacağını düşünüyorsunuz. Yani kendi standartlarınıza uygun olmamak ve başkalarına bu konuyu itiraf etmek istemiyorsunuz çünkü bu onları incitebilir veya sürekli tartışmalara yol açabilir. Ancak kendinizi çok fazla tüketiyorsunuz çünkü her şeyi mükemmel yapmak istiyorsunuz, bu durum sadece bir şeyi doğru bir şekilde yapmak yerine sürekli yeniden başlama isteğinizi körükleyebilir. Unutmayın, her şeyi mükemmel yapmak için aylarınızı hatta yıllarınızı harcamak zorunda değilsiniz. En önemli şey, işleri yapmaktır ve ardından bir sonraki adıma geçmektir."
			},
			{   # 12.ev - Terazi
                "id": "fears_libra",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Terazi",
                "title": title,
                "text": "Başkalarının ne kadar çok başkalarını önemsediğinizi görmesinden korkuyorsunuz çünkü insanlar sevdiklerinizi manipüle edebilir veya incitebilir. Bu yüzden, yalnız kalmak sorun olmuyormuş gibi davranarak kimleri ve neyi sevdiğinizi korumak zorundasınız. Bilinçaltınızda gittiğiniz her yerde barışı sağlama ve herkesin adaletsizliklere karşı korunmasını ve savunulmasını sağlama ihtiyacı var. Ancak bu çok fazla zaman ve enerji gerektirir ve başkalarının sizin için aynısını yapmasını bekleyebilirsiniz. Ancak onlar her zaman sizin için bunu yapmalarına gerek olmadığını düşünebilir ve bu destek eksikliği nedeniyle ihanete uğramış gibi hissedebilirsiniz. Güçlü bir kişi olarak görülmek bu dinamikleri yaratabilir ve bazen sadece bir kez bile olsa sizi savunmalarını istersiniz. Ya her şey ters giderse ve yanlış taraf için savaşılırsa?"
			},
			{   # 12.ev - Akrep
                "id": "fears_scorpio",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Akrep",
                "title": title,
                "text": "Kızgın olduğunuzda nasıl tepki vereceğinizden ve bir şeylerin sizi ne kadar derinden etkileyebileceğinden korkuyorsunuz bu yüzden aldırış etmiyormuş gibi davranmaya çalışıyorsunuz. Bilinçaltınızda anlaşılmaya ve gerçekten açılmaya yönelik bir ihtiyaç var ama aynı zamanda kontrol sahibi hissetmek ve başkaları hakkında sizin hakkınızda bildiklerinden daha fazlasını bilmek istiyorsunuz. Bu olmadan insanların size ihanet etmesini nasıl önleyebilirsiniz? Davranışlarınız ve kararlarınızla başkalarını incitebileceğinizi anlamalısınız, belirli durumlarda maalesef geçmişte sizi inciten insanlar gibi hareket edebileceğinizi de anlamalısınız. Bu sizi özünde kötü bir insan yapmaz ama kabul edilmesi ve ele alınması gereken bir durumdur. İnsanlar size nasıl incittiğinizi veya işleri nasıl mahvettiğinizi ifade ettiklerinde onları kesmemelisiniz."
			},
			{   # 12.ev - Yay
                "id": "fears_sagittarius",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Yay",
                "title": title,
                "text": "Ne istediğinizi ve neye ihtiyacınız olduğunu asla öğrenemeyecek kadar deneyimsiz olma korkunuz var, bu yüzden genellikle çalışmaya ve yaşamın tadını çıkarmak için yeterli zamanı harcamaya çalışıyorsunuz. Bilinçaltınızda daha maceracı olma ve daha az gidilen yolu seçme ihtiyacı var ancak bunun kötü sonuçlarından korkuyorsunuz. Örneğin bir noktada normal hayatınıza geri dönememek gibi. Hayatınızdaki köklü değişiklikleri istediğiniz zaman yapamayacağınızı hissetmek, sadece öyle olsun diye hayatınızın tamamen farklı bir hal almasını istemediğiniz anlamına gelir. Bu yetişkin hayatınızın sorumluluklarını üstlenemeyecek kadar ciddi olmamakla ilgili değil özgürlüğün ulaşılmaz bir rüya olmadığını hissetmekle ilgilidir. Ancak bazı seçimlerin görmezden gelinemeyecek ve geri alınamayacak uzun vadeli sonuçları vardır. Eğer bu yolu kendiniz seçtiyseniz kendinizi tuzağa düşmüş hissetmemelisiniz ve sorumluluk almak da gereklidir."
			},
			{   # 12.ev - Oğlak
                "id": "fears_capricorn",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Oğlak",
                "title": title,
                "text": "Hedeflerinize ulaşamayacak kadar ciddi olmaktan korkuyorsunuz çünkü bu insanların size, işinize ve olası mirasınıza saygı göstermeyeceği anlamına geliyor. Ayrıca büyük kurumlar ve önemli insanlar tarafından tanınmayı küçümsediğinizi iddia ediyorsunuz. Bilinçaltınızda toplumun standartlarına göre işe yaramaz biri olarak görülme korkusu vardır. Bu yüzden kendinizi sürekli meşgul tutma ihtiyacı duyuyorsunuz. Zamanla bunun gerçekten istediğiniz hayat tarzı olup olmadığını sorgulamaya başlıyorsunuz. Kendi hayalleriniz ve arzularınız şartlanmalarınızın baskın çıktığını gösteriyor ve bu durum hayal kırıklığı yaratabilir. Bu duygularla yüzleşmeniz ve toplumun sizden istediği hayatı yaşamaya zorlamak yerine, gerçekten ne istediğinizi belirlemeniz gerek. Aksi takdirde, kendinizi giderek daha mutsuz hissedebilirsiniz ve bundan çok daha iyisini hak ediyorsunuz."
			},
			{   # 12.ev - Kova
                "id": "fears_aquarius",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Kova",
                "title": title,
                "text": "Benzersizliğinizi kabul etmekte zorluk çekiyorsunuz ve başkalarının sizi farklı bulmasından korkuyorsunuz. Bilinçaltınızda kendinizi tanımak ve farklı yönlerinizi kabul etme ihtiyacı var. Bu başkalarında hayranlık duyduğunuz bir şeydir ancak zorlandığınız bir şeydir. Başkaları bunu yaptığında daha kolay görünebilir, sanki onların karşılaşabileceği türden tepkiyle karşılaşmayacaklarmış gibi. Ancak herkes başkaları tarafından kabul edilmekle mücadele ediyor. Kendinizi olduğu gibi ortaya koymak korkutucu olabilir ama buna rağmen kim olduğunuzu göstermeyi seçmelisiniz. Uzun vadede kendinizi kabul ettiğinizde ve insanların sizi kabul ettiğini gördüğünüzde daha iyi hissedeceksiniz."
			},
			{   # 12.ev - Balık
                "id": "fears_pisces",
                "type": "house_sign_is",
                "house": 12,
				"sign": "Balık",
                "title": title,
                "text": "Rüyalarınızda kaybolmaktan ve duygularınızın en iyi halinizi etkilemesinden korkuyorsunuz, bu yüzden güçlü davranmaya çalışıyorsunuz. Bilinçaltınızda, ruhsal ve psişik yönlerinizi benimseme ihtiyacı var ancak nereden başlayacağınızı bilmiyorsunuz. Bu yönünüzle ilişkilendirilmek istemiyorsunuz çünkü çok az kişi bu tür konulara ilgi duyuyor ve hala ciddiye alınmak istiyorsunuz. Bu sezginizi ve kalbinizin size fısıldadıklarını daha fazla dinlemekle ilgilidir ancak aynı zamanda bunları daha dikkatle dinlemeli ve sadece kafanızın içindeki garip sesler gibi davranmayı bırakmalısınız. Bunlar sizi kurtarmak için burada sizi rahatsız etmek için değil. Dinlemezseniz, sonradan şikayet edemezsiniz."
			},
        ]
	def _colors_abundance(self) -> List[Dict]:
		title = "Eğer Haritanızda Yücelim Gezegenleri Varsa; Hayatınıza Daha Fazla Bolluk ve Bereket Getirmek İçin Giyiminizde Kullanmanız Gereken Bazı Renk Kombinasyonları Vardır. Bu Renk Kombinasyonlarını Kullanarak Gezegenlerin Yücelim Enerjisini Aktifleştirebilirsiniz."
		return [
			{	# Güneş - Koç
				"id": "colors_abundance_sun",
				"type": "planet_in_sign",
				"planet": "Güneş ☉",
				"sign": "Koç",
				"title": title,
				"text": "Gold ve Kırmızı. Bu renkler hayatınıza ilham katar."
			},
			{	# Ay - Boğa
				"id": "colors_abundance_moon",
				"type": "planet_in_sign",
				"planet": "Ay ☽",
				"sign": "Boğa",
				"title": title,
				"text": "Beyaz ve Yeşil. Bu renkler hayatınıza duygusal güvence katar."
			},
			{	# Merkür - Başak
				"id": "colors_abundance_mercury",
				"type": "planet_in_sign",
				"planet": "Merkür ☿",
				"sign": "Başak",
				"title": title,
				"text": "Yeşil ve Kahverengi. Bu renkler hayatınıza iletişim yeteneği katar."
			},
			{	# Venüs - Balık
				"id": "colors_abundance_venus",
				"type": "planet_in_sign",
				"planet": "Venüs ♀",
				"sign": "Balık",
				"title": title,
				"text": "Pembe veya Yeşil ile pastel Mavi. Bu renkler hayatınıza sevgi ve uyum katar."
			},
			{	# Mars - Oğlak
				"id": "colors_abundance_mars",
				"type": "planet_in_sign",
				"planet": "Mars ♂",
				"sign": "Oğlak",
				"title": title,
				"text": "Kırmızı ve Siyah. Bu renkler hayatınıza disiplin katar."
			},
			{	# Jüpiter - Yengeç
				"id": "colors_abundance_jupiter",
				"type": "planet_in_sign",
				"planet": "Jüpiter ♃",
				"sign": "Yengeç",
				"title": title,
				"text": "Beyaz ve Mavi. Bu renkler hayatınıza bolluk ve bereket katar."
			},
			{	# Satürn - Terazi
				"id": "colors_abundance_saturn",
				"type": "planet_in_sign",
				"planet": "Satürn ♄",
				"sign": "Terazi",
				"title": title,
				"text": "Siyah ve Pembe. Bu renkler hayatınıza adalet katar."
			},
		]

	def find_person_folder(self, person_name: str) -> Tuple[Optional[str], str]:
		safe_name = "".join(c for c in person_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
		safe_name = safe_name.replace(' ', '_')

		users_root = os.path.join(os.getcwd(), "users")
		search_roots = [users_root] if os.path.isdir(users_root) else [os.getcwd()]

		possible_folders = [
			f"{safe_name}_DoğumHaritası",
			safe_name,
			f"{person_name.replace(' ', '_')}_DoğumHaritası",
			person_name.replace(' ', '_')
		]

		for root in search_roots:
			for folder_name in possible_folders:
				candidate = os.path.join(root, folder_name)
				if os.path.exists(candidate):
					return candidate, safe_name

		return None, safe_name

	# -------------------- Veri Okuma --------------------
	def load_natal_data(self, folder_path: str) -> Optional[Dict]:
		try:
			report_files = [f for f in os.listdir(folder_path) if f.endswith('_natal_report.txt')]
			if not report_files:
				print("❌ Natal chart rapor dosyası bulunamadı!")
				return None

			report_file = report_files[0]
			report_path = os.path.join(folder_path, report_file)
			return self.parse_natal_report(report_path)
		except Exception as exc:
			print(f"Veri yükleme hatası: {exc}")
			return None

	def parse_natal_report(self, report_path: str) -> Optional[Dict]:
		try:
			with open(report_path, 'r', encoding='utf-8') as f:
				content = f.read()

			lines = content.split('\n')
			all_positions: Dict[str, Dict] = {}
			houses: Dict[str, Dict] = {}

			in_planet_section = False
			in_house_section = False

			sign_names = [
				"Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak",
				"Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"
			]

			for line in lines:
				line = line.strip()

				if '🪐 GEZEGEN VE ASTEROID POZİSYONLARI:' in line:
					in_planet_section = True
					in_house_section = False
					continue
				if '🏠 EV SİSTEMİ' in line:
					in_planet_section = False
					in_house_section = True
					continue
				if '✨ TEMEL ASTROLOJİK YORUMLAR:' in line:
					break

				# Gezegenler
				if in_planet_section and line and not line.startswith('-'):
					parts = line.split()
					if len(parts) >= 3:
						sign_index = -1
						sign_part_index = -1
						for i, part in enumerate(parts):
							for s_name in sign_names:
								if s_name in part:
									sign_index = sign_names.index(s_name)
									sign_part_index = i
									break
							if sign_part_index >= 0:
								break

						if sign_part_index < 0:
							continue

						planet_name = ' '.join(parts[:sign_part_index])
						sign = ' '.join(parts[sign_part_index:sign_part_index + 2])
						degree_str = parts[-1].replace('°', '')

						try:
							degree = float(degree_str)
						except ValueError:
							continue

						longitude = sign_index * 30 + degree

						all_positions[planet_name] = {
							'longitude': longitude,
							'sign': sign,
							'degree': degree,
							'sign_num': sign_index
						}

				# Evler
				if in_house_section and line and not line.startswith('-'):
					parts = line.split()
					if len(parts) >= 3 and ('Ev' in line or 'ASC' in line or 'MC' in line):
						if 'Yükselen (ASC)' in line:
							house_name = 'Yükselen (ASC)'
							sign = ' '.join(parts[2:4])
							degree_str = parts[-1].replace('°', '')
						elif 'Orta Gökyüzü (MC)' in line:
							house_name = 'Orta Gökyüzü (MC)'
							sign = ' '.join(parts[3:5])
							degree_str = parts[-1].replace('°', '')
						else:
							house_name = ' '.join(parts[:2])
							sign = ' '.join(parts[2:4])
							degree_str = parts[-1].replace('°', '')

						try:
							degree = float(degree_str)
						except ValueError:
							continue

						sign_num = 0
						for i, s_name in enumerate(sign_names):
							if s_name in sign:
								sign_num = i
								break

						cusp_longitude = sign_num * 30 + degree
						houses[house_name] = {
							'cusp_longitude': cusp_longitude,
							'sign': sign,
							'degree': degree
						}

			if all_positions and houses:
				return {
					'all_positions': all_positions,
					'houses': houses
				}
			return None
		except Exception as exc:
			print(f"Dosya parsing hatası: {exc}")
			return None

	# -------------------- Ev Hesapları --------------------
	def _house_cusps(self, houses: Dict[str, Dict]) -> List[float]:
		cusps = []
		for i in range(1, 13):
			key = f"{i}. Ev"
			if key in houses:
				cusps.append(houses[key]['cusp_longitude'])
		return cusps

	def _planet_houses(self, chart_data: Dict) -> Dict[str, int]:
		planets = chart_data.get('all_positions', {})
		houses = chart_data.get('houses', {})
		cusps = self._house_cusps(houses)
		if len(cusps) != 12:
			return {}

		planet_houses: Dict[str, int] = {}
		for planet_name, pdata in planets.items():
			lng = pdata.get('longitude')
			if lng is None:
				continue
			planet_houses[planet_name] = self._find_house(lng, cusps)
		return planet_houses

	def _find_house(self, longitude: float, cusps: List[float]) -> int:
		# Ev aralıklarını dolaşarak hangi evde olduğunu bul
		for idx in range(12):
			start = cusps[idx]
			end = cusps[(idx + 1) % 12]

			if start <= end:
				if start <= longitude < end:
					return idx + 1
			else:  # 360/0 derecelik geçiş
				if longitude >= start or longitude < end:
					return idx + 1
		return 12

	# -------------------- Not Değerlendirme --------------------
	def evaluate_notes(self, chart_data: Dict) -> List[Dict]:
		matches: List[Dict] = []
		planets = chart_data.get('all_positions', {})
		houses = chart_data.get('houses', {})
		planet_houses = self._planet_houses(chart_data)

		for note in self.notes:
			ntype = note.get('type')

			if ntype == 'planet_degree_equals':
				target_degree = note.get('degree')
				tolerance = float(note.get('tolerance', 0.5))
				min_deg = note.get('degree_min')
				max_deg = note.get('degree_max')
				target_planet = self._normalize_planet(note.get('planet', 'any'))

				for pname, pdata in planets.items():
					if target_planet.lower() != 'any' and self._normalize_planet(pname) != target_planet:
						continue
					degree = pdata.get('degree')
					if degree is None:
						continue
					if min_deg is not None and max_deg is not None:
						if min_deg <= degree <= max_deg:
							matches.append({
								'id': note.get('id'),
								'title': note.get('title'),
								'text': note.get('text'),
								'context': f"{pname} {degree:.2f}°"
							})
							break
					elif target_degree is not None and abs(degree - float(target_degree)) <= tolerance:
						matches.append({
							'id': note.get('id'),
							'title': note.get('title'),
							'text': note.get('text'),
							'context': f"{pname} {degree:.2f}°"
						})
						break

			elif ntype == 'planet_in_sign':
				target_planet = self._normalize_planet(note.get('planet', ''))
				target_sign = self._normalize_sign(note.get('sign', ''))
				for pname, pdata in planets.items():
					if self._normalize_planet(pname) != target_planet:
						continue
					sign_now = self._normalize_sign(pdata.get('sign', ''))
					if sign_now == target_sign:
						matches.append({
							'id': note.get('id'),
							'title': note.get('title'),
							'text': note.get('text'),
							'context': f"{pname} {sign_now}"
						})
						break

			elif ntype == 'planet_in_house':
				target_planet = self._normalize_planet(note.get('planet', ''))
				target_house = int(note.get('house', 0))
				for pname, hnum in planet_houses.items():
					if self._normalize_planet(pname) != target_planet:
						continue
					if hnum == target_house:
						matches.append({
							'id': note.get('id'),
							'title': note.get('title'),
							'text': note.get('text'),
							'context': f"{pname} {hnum}. ev"
						})
						break

			elif ntype == 'house_sign_is':
				target_house = int(note.get('house', 0))
				target_sign = self._normalize_sign(note.get('sign', ''))
				house_key = f"{target_house}. Ev"
				if house_key in houses:
					sign_now = self._normalize_sign(houses[house_key].get('sign', ''))
					if sign_now == target_sign:
						matches.append({
							'id': note.get('id'),
							'title': note.get('title'),
							'text': note.get('text'),
							'context': f"{house_key} {sign_now}"
						})

		return matches

	# -------------------- Raporlama --------------------
	def save_report(self, person_name: str, folder_path: str, safe_name: str, matches: List[Dict]) -> Optional[str]:
		filename = os.path.join(folder_path, f"{safe_name}_special_notes.txt")
		try:
			with open(filename, 'w', encoding='utf-8') as f:
				f.write("=" * 70 + "\n")
				f.write(f"    {person_name.upper()} - ÖZEL NOTLAR\n")
				f.write("=" * 70 + "\n\n")

				if not matches:
					f.write("Bu harita için eşleşen özel not bulunamadı.\n")
				else:
					for item in matches:
						title = item.get('title')
						text = item.get('text')
						context = item.get('context')

						if title:
							f.write(f"{title}\n")
						if context:
							f.write(f"   → {context}\n")
						if text:
							f.write(f"{text}\n")

						f.write("-" * 70 + "\n")
			print(f"📄 Özel not raporu oluşturuldu: {filename}")
			return filename
		except Exception as exc:
			print(f"Dosya kaydetme hatası: {exc}")
			return None

	# -------------------- Çalıştır --------------------
	def run_for_person(self, person_name: str) -> None:
		folder_path, safe_name = self.find_person_folder(person_name)
		if not folder_path:
			print(f"❌ '{person_name}' için klasör bulunamadı!")
			return

		chart_data = self.load_natal_data(folder_path)
		if not chart_data:
			print("❌ Harita verisi yüklenemedi.")
			return

		matches = self.evaluate_notes(chart_data)
		self.save_report(person_name, folder_path, safe_name, matches)


if __name__ == "__main__":
	sn = SpecialNotes()
	name = input("İsim / Soyisim girin: ").strip()
	if name:
		sn.run_for_person(name)
	else:
		print("İsim boş olamaz.")
