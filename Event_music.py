import csv
import os

NAMA_EVENT = "FLAMENGGO MUSIC EVENT"
FILE_CSV = "data_peserta.csv"
HEADER_CSV = ["id_peserta", "nama", "email", "no_telepon", "jenis_tiket"]

JENIS_TIKET_VALID = {
    "vip": "VIP",
    "festival": "Festival",
    "regular": "Regular"
}


class NodePeserta:
    def __init__(self, id_peserta, nama, email, no_telepon, jenis_tiket):
        self.id_peserta = id_peserta
        self.nama = nama
        self.email = email
        self.no_telepon = no_telepon
        self.jenis_tiket = jenis_tiket
        self.next = None


class LinkedListPeserta:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def tambah(self, id_peserta, nama, email, no_telepon, jenis_tiket):
        node_baru = NodePeserta(id_peserta, nama, email, no_telepon, jenis_tiket)
        if self.is_empty():
            self.head = node_baru
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node_baru

    def hapus(self, id_peserta):
        current = self.head
        prev = None
        while current is not None:
            if current.id_peserta == id_peserta:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def cari_by_id(self, id_peserta):
        current = self.head
        while current is not None:
            if current.id_peserta == id_peserta:
                return current
            current = current.next
        return None

    def ke_list(self):
        hasil = []
        current = self.head
        while current is not None:
            hasil.append({
                "id_peserta": current.id_peserta,
                "nama": current.nama,
                "email": current.email,
                "no_telepon": current.no_telepon,
                "jenis_tiket": current.jenis_tiket
            })
            current = current.next
        return hasil

    def dari_list(self, data_list):
        self.head = None
        for d in data_list:
            self.tambah(d["id_peserta"], d["nama"], d["email"],
                        d["no_telepon"], d["jenis_tiket"])

    def jumlah(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

class NodeQueue:
    def __init__(self, data):
        self.data = data
        self.next = None


class QueueCheckIn:
    def __init__(self):
        self.front = None
        self.rear = None 
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        node_baru = NodeQueue(data)
        if self.is_empty():
            self.front = node_baru
            self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        node = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return node.data

    def lihat_antrean(self):
        hasil = []
        current = self.front
        while current is not None:
            hasil.append(current.data)
            current = current.next
        return hasil


def muat_data_dari_csv (linked_list, filename=FILE_CSV):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER_CSV)
        return

    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            linked_list.tambah(
                row["id_peserta"], row["nama"], row["email"],
                row["no_telepon"], row["jenis_tiket"]
            )


def simpan_data_ke_csv(linked_list, filename=FILE_CSV):
    data = linked_list.ke_list()
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_CSV)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


def bubble_sort_nama(data_list, ascending=True):
    data = data_list.copy()
    n = len(data)
    for i in range(n-1):
        for j in range(n-1-i):
            nama_a = data[j]["nama"].lower()
            nama_b = data[j+1]["nama"].lower()
            if ascending:
                tukar=nama_a>nama_b
            else:
                tukar=nama_a<nama_b
            if tukar:
                data[j], data[j+1] =data[j+1], data[j]
    return data

def cetak_header(judul=""):
    print("\n" + "=" * 64)
    print("    EVENT ORGANIZER")
    print(f"   {NAMA_EVENT}")
    if judul:
        print("   " + "-" * 58)
        print(f"   >> {judul}")
    print("=" * 64)


def potong(teks, panjang):
    teks = str(teks)
    if len(teks) > panjang:
        return teks[:panjang - 2] + ".."
    return teks


def cetak_tabel(data_list):
    if not data_list:
        print("\n(Tidak ada data peserta)")
        return

    print()
    print(f"{'ID':<6}{'Nama':<20}{'Email':<24}{'No. Telepon':<15}{'Tiket':<10}")
    print("-" * 75)
    for d in data_list:
        print(f"{potong(d['id_peserta'], 6):<6}"
              f"{potong(d['nama'], 20):<20}"
              f"{potong(d['email'], 24):<24}"
              f"{potong(d['no_telepon'], 15):<15}"
              f"{potong(d['jenis_tiket'], 10):<10}")
    print("-" * 75)
    print(f"Total Peserta : {len(data_list)}")


def input_tidak_kosong(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("Input tidak boleh kosong, silakan ulangi.")


def input_jenis_tiket(default=None):
    while True:
        if default:
            prompt = (f"Jenis Tiket [{default}] (VIP/Festival/Regular, "
                      f"kosongkan = tetap): ")
        else:
            prompt = "Jenis Tiket (VIP/Festival/Regular): "

        nilai = input(prompt).strip().lower()

        if not nilai and default:
            return None  # tidak diubah
        if nilai in JENIS_TIKET_VALID:
            return JENIS_TIKET_VALID[nilai]
        print("Jenis tiket tidak valid! Pilih salah satu: VIP, Festival, Regular.")


def generate_id(linked_list):
    data = linked_list.ke_list()
    nomor_terbesar = 0
    for d in data:
        id_str = d["id_peserta"]
        if id_str.startswith("P") and id_str[1:].isdigit():
            nomor = int(id_str[1:])
            nomor_terbesar = max(nomor_terbesar, nomor)
    return f"P{nomor_terbesar + 1:03d}"

def fitur_tambah_peserta(linked_list):
    cetak_header("TAMBAH PESERTA BARU")

    id_baru = generate_id(linked_list)
    print(f"ID Peserta (otomatis): {id_baru}")

    nama = input_tidak_kosong("Nama Peserta  : ")
    email = input_tidak_kosong("Email         : ")
    telp = input_tidak_kosong("No. Telepon   : ")
    tiket = input_jenis_tiket()

    linked_list.tambah(id_baru, nama, email, telp, tiket)
    simpan_data_ke_csv(linked_list)

    print(f"\n[OK] Peserta '{nama}' berhasil ditambahkan dengan ID {id_baru}.")


def fitur_lihat_semua_peserta(linked_list):
    cetak_header("DAFTAR SEMUA PESERTA")
    cetak_tabel(linked_list.ke_list())


def fitur_cari_peserta(linked_list):
    cetak_header("CARI PESERTA (LINEAR SEARCH)")

    if linked_list.is_empty():
        print("\n(Belum ada data peserta)")
        return

    id_cari = input_tidak_kosong("Masukkan ID Peserta yang dicari : ")
    hasil = linked_list.cari_by_id(id_cari)

    if hasil is not None:
        print(f"\n[OK] Peserta dengan ID '{id_cari}' ditemukan:")
        cetak_tabel([{
            "id_peserta": hasil.id_peserta,
            "nama": hasil.nama,
            "email": hasil.email,
            "no_telepon": hasil.no_telepon,
            "jenis_tiket": hasil.jenis_tiket
        }])
    else:
        print(f"\n[GAGAL] Peserta dengan ID '{id_cari}' tidak ditemukan.")


def fitur_update_peserta(linked_list):
    cetak_header("UPDATE DATA PESERTA")

    if linked_list.is_empty():
        print("\n(Belum ada data peserta)")
        return

    id_update = input_tidak_kosong("Masukkan ID Peserta yang akan diupdate : ")
    node = linked_list.cari_by_id(id_update)

    if node is None:
        print(f"\n[GAGAL] Peserta dengan ID '{id_update}' tidak ditemukan.")
        return

    print("\nData saat ini:")
    cetak_tabel([{
        "id_peserta": node.id_peserta, "nama": node.nama, "email": node.email,
        "no_telepon": node.no_telepon, "jenis_tiket": node.jenis_tiket
    }])

    print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah field tersebut):")
    nama_baru = input(f"Nama Peserta [{node.nama}] : ").strip()
    email_baru = input(f"Email [{node.email}] : ").strip()
    telp_baru = input(f"No. Telepon [{node.no_telepon}] : ").strip()
    tiket_baru = input_jenis_tiket(default=node.jenis_tiket)

    if nama_baru:
        node.nama = nama_baru
    if email_baru:
        node.email = email_baru
    if telp_baru:
        node.no_telepon = telp_baru
    if tiket_baru:
        node.jenis_tiket = tiket_baru

    simpan_data_ke_csv(linked_list)
    print(f"\n[OK] Data peserta dengan ID '{id_update}' berhasil diperbarui.")


def fitur_hapus_peserta(linked_list):
    cetak_header("HAPUS PESERTA")

    if linked_list.is_empty():
        print("\n(Belum ada data peserta)")
        return

    id_hapus = input_tidak_kosong("Masukkan ID Peserta yang akan dihapus : ")
    node = linked_list.cari_by_id(id_hapus)

    if node is None:
        print(f"\n[GAGAL] Peserta dengan ID '{id_hapus}' tidak ditemukan.")
        return

    print("\nData yang akan dihapus:")
    cetak_tabel([{
        "id_peserta": node.id_peserta, "nama": node.nama, "email": node.email,
        "no_telepon": node.no_telepon, "jenis_tiket": node.jenis_tiket
    }])

    konfirmasi = input("\nYakin ingin menghapus data ini? (y/n): ").strip().lower()
    if konfirmasi == "y":
        linked_list.hapus(id_hapus)
        simpan_data_ke_csv(linked_list)
        print(f"\n[OK] Peserta dengan ID '{id_hapus}' berhasil dihapus.")
    else:
        print("\nPenghapusan dibatalkan.")


def fitur_urutkan_peserta(linked_list):
    cetak_header("URUTKAN DATA PESERTA (BUBBLE SORT)")

    data = linked_list.ke_list()
    if not data:
        print("\n(Belum ada data peserta)")
        return

    print("Urutkan berdasarkan nama:")
    print("  1. A - Z (Ascending)")
    print("  2. Z - A (Descending)")
    pilihan = input("Pilih (1/2): ").strip()
    ascending = pilihan != "2"

    data_terurut = bubble_sort_nama(data, ascending)
    print("\nHasil pengurutan:")
    cetak_tabel(data_terurut)

    simpan = input("\nSimpan urutan ini secara permanen ke CSV? (y/n): ").strip().lower()
    if simpan == "y":
        linked_list.dari_list(data_terurut)
        simpan_data_ke_csv(linked_list)
        print("\n[OK] Urutan data berhasil disimpan ke file CSV.")
    else:
        print("\nUrutan tidak disimpan (hanya ditampilkan).")

def fitur_antrean_checkin(linked_list, queue):
    while True:
        cetak_header("KELOLA ANTREAN CHECK-IN")
        print(f"Jumlah peserta dalam antrean saat ini : {queue.size}")
        print()
        print("  1. Tambahkan peserta ke antrean check-in")
        print("  2. Proses check-in (peserta paling depan)")
        print("  3. Lihat seluruh antrean")
        print("  4. Kembali ke Menu Utama")
        pilihan = input("\nPilih menu (1-4): ").strip()

        if pilihan == "1":
            if linked_list.is_empty():
                print("\n(Belum ada data peserta)")
            else:
                id_peserta = input_tidak_kosong("Masukkan ID Peserta : ")
                node = linked_list.cari_by_id(id_peserta)
                if node is None:
                    print(f"\n[GAGAL] Peserta dengan ID '{id_peserta}' tidak ditemukan.")
                else:
                    queue.enqueue({
                        "id_peserta": node.id_peserta,
                        "nama": node.nama,
                        "jenis_tiket": node.jenis_tiket
                    })
                    print(f"\n[OK] '{node.nama}' ditambahkan ke antrean check-in "
                          f"(posisi ke-{queue.size}).")

        elif pilihan == "2":
            if queue.is_empty():
                print("\n(Antrean check-in kosong)")
            else:
                data = queue.dequeue()
                print("\n[CHECK-IN BERHASIL]")
                print(f"  ID Peserta   : {data['id_peserta']}")
                print(f"  Nama         : {data['nama']}")
                print(f"  Jenis Tiket  : {data['jenis_tiket']}")
                print(f"  Sisa antrean : {queue.size} orang")

        elif pilihan == "3":
            antrean = queue.lihat_antrean()
            if not antrean:
                print("\n(Antrean check-in kosong)")
            else:
                print(f"\nDaftar antrean check-in ({len(antrean)} peserta):")
                print("-" * 50)
                for i, d in enumerate(antrean, start=1):
                    keterangan = "  <-- berikutnya" if i == 1 else ""
                    print(f"{i}. {d['id_peserta']} - {d['nama']} "
                          f"({d['jenis_tiket']}){keterangan}")
                print("-" * 50)

        elif pilihan == "4":
            break
        else:
            print("\nPilihan tidak valid! Silakan pilih 1-4.")

        input("\nTekan ENTER untuk lanjut...")


# ============================================================
# MODUL: MENU UTAMA & PROGRAM UTAMA
# ============================================================
def tampilkan_menu_utama(linked_list):
    cetak_header("MENU UTAMA")
    print(f"Jumlah peserta terdaftar : {linked_list.jumlah()}")
    print()
    print("  1. Tambah Peserta")
    print("  2. Lihat Semua Peserta")
    print("  3. Cari Peserta")
    print("  4. Update Data Peserta")
    print("  5. Hapus Peserta")
    print("  6. Urutkan Data Peserta")
    print("  7. Kelola Antrean Check-in")
    print("  8. Keluar")
    print("-" * 64)


def main():
    linked_list = LinkedListPeserta()
    queue = QueueCheckIn()

    muat_data_dari_csv(linked_list)

    print("\nSelamat datang di Sistem Event Organizer")
    print(f'"{NAMA_EVENT}"')
    print(f"Data berhasil dimuat dari '{FILE_CSV}'.")

    while True:
        tampilkan_menu_utama(linked_list)
        pilihan = input("Pilih menu (1-8): ").strip()

        if pilihan == "1":
            fitur_tambah_peserta(linked_list)
        elif pilihan == "2":
            fitur_lihat_semua_peserta(linked_list)
        elif pilihan == "3":
            fitur_cari_peserta(linked_list)
        elif pilihan == "4":
            fitur_update_peserta(linked_list)
        elif pilihan == "5":
            fitur_hapus_peserta(linked_list)
        elif pilihan == "6":
            fitur_urutkan_peserta(linked_list)
        elif pilihan == "7":
            fitur_antrean_checkin(linked_list, queue)
        elif pilihan == "8":
            simpan_data_ke_csv(linked_list)
            print("\nData telah disimpan.")
            print("Terima kasih telah menggunakan Sistem Manajemen")
            print(f'Event Organizer "{NAMA_EVENT}".')
            print("Sampai jumpa di acara berikutnya!\n")
            break
        else:
            print("\nPilihan tidak valid! Silakan pilih menu 1-8.")

        if pilihan != "8":
            input("\nTekan ENTER untuk kembali ke Menu Utama...")


if __name__ == "__main__":
    main()