import requests
import bs4 #import BeautifulSoup
#import gempaterkini

class GempaTerkini:
    def __init__(self):

        self.description = 'To get the latest earthquake in Indonesian from BMKG.go.id'
        self.result = None

    def ekstraksi_data(self):

        """
        Tanggal: 07 Juni 2022
        Waktu:   13:03:13 WIB
        Magnitudo: 4.6
        Kedalaman: 10 km
        Lokasi: LS=8.17 BT= - 117.31 BT
        Pusat Gempa: Pusat gempa berada di laut 37 km Barat Laut Sumbawa
        dirasakan: Dirasakan (Skala MMI): II - III Sumbawa
        :return:
        """
        #global soup
        try:
            content = requests.get('https://www.bmkg.go.id/')
        except Exception:
            return None

        if content.status_code == 200:
            soup = bs4.BeautifulSoup(content.text, 'html.parser')

            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            tanggal = result[0]
            waktu = result[1]

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')
            i = 0
            magnitudo = None
            ls = None
            bt = None
            dirasakan = None
            kedalaman = None
            lokasi = None

            for res in result:
                #print(i, res)
                if  i == 1:
                    magnitudo = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    dirasakan = res.text
                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitudo'] = magnitudo
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print("Tidak Bisa Menemukan Data Gempa Terkini")
            return

        print('\nGempa Terakhir Berdasarkan BMKG')
        print(f"Tanggal {self.result['tanggal']}")
        print(f"Waktu {self.result['waktu']}")
        print(f"Magnitudo {self.result['magnitudo']}")
        print(f"Kedalaman {self.result['kedalaman']}")
        print(f"Koordinat LS={self.result['koordinat']['ls']}, BT={self.result['koordinat']['bt']}")
        print(f"Lokasi {self.result['lokasi']}")
        print(f"Dirasakan {self.result['dirasakan']}")

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini()
    print('Deskripsi package', gempa_di_indonesia.description)
    gempa_di_indonesia.run()
    #gempa_di_indonesia.ekstraksi_data()
    #gempa_di_indonesia.tampilkan_data()
