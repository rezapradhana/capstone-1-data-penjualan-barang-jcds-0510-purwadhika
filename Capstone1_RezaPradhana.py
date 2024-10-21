### CAPSTONE 1 DENGAN TEMA PENJUALAN BARANG BERUPA LAPTOP ###

### Fitur yang dibuat (Create, Read, Update, Delete, Sales, Sales History, Backup Data dan View Backup Data) ###

### Reza Pradhana (JCDS 0510)
from tabulate import tabulate

# Dataset awal dengan kolom id otomatis
laptops = [
    {"id": 1, "brand": "Asus", "model": "ZenBook", "price": 5000000, "stock": 10},
    {"id": 2, "brand": "HP", "model": "Pavilion", "price": 5000000, "stock": 8},
    {"id": 3, "brand": "Axioo", "model": "MyBook", "price": 5000000, "stock": 5},
    {"id": 4, "brand": "Lenovo", "model": "ThinkPad", "price": 5000000, "stock": 11},
    {"id": 5, "brand": "Acer", "model": "Aspire", "price": 5000000, "stock": 13}
]

sales_history = []

def get_input(prompt, input_type, allow_empty=False):
    """Fungsi untuk mendapatkan input dari pengguna dengan validasi."""
    while True:
        user_input = input(prompt).strip()
        if not allow_empty and not user_input:
            print("Input tidak boleh kosong.")
            continue
        
        if input_type == "alpha" and user_input.isalpha():
            return user_input
        elif input_type == "digit" and user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        elif input_type == "float":
            try:
                value = float(user_input)
                if value >= 0:
                    return value
                print("Input harus berupa angka positif.")
            except ValueError:
                print("Input harus berupa angka desimal.")
        elif input_type == "choice" and user_input in map(str, range(1, 11)):
            return user_input
        
        print(f"Input tidak valid untuk tipe '{input_type}'.")

def show_help():
    """Menampilkan bantuan tentang fitur-fitur dalam program."""
    help_text = """
    === PENJUALAN LAPTOP ===
    
    1. Tambah Laptop: Menambahkan laptop baru ke dalam daftar.
    2. Lihat Daftar Laptop: Menampilkan semua laptop yang tersedia.
    3. Update Laptop: Memperbarui informasi dari laptop yang sudah ada.
    4. Hapus Laptop: Menghapus laptop dari daftar.
    5. Jual Laptop: Menjual laptop dan mengurangi stok.
    6. Lihat Riwayat Penjualan: Menampilkan riwayat penjualan laptop.
    7. Cadangkan Data: Menyimpan data laptop ke dalam file untuk cadangan.
    8. Lihat Data Cadangan: Menampilkan data yang telah dicadangkan.
    9. Keluar: Menghentikan program.
    10. Bantuan: Menampilkan informasi tentang setiap fitur.
    """
    print(help_text)

def create_laptop():
    """Menambahkan laptop baru ke dalam daftar."""
    print("=== PENJUALAN LAPTOP ===")  
    brand = get_input("Masukkan merek laptop: ", "alpha")
    model = get_input("Masukkan model laptop: ", "alpha")
    
    if any(laptop['model'] == model and laptop['brand'] == brand for laptop in laptops):
        print("Laptop dengan merek dan model ini sudah ada.")
        return

    price = get_input("Masukkan harga laptop: ", "float")
    stock = get_input("Masukkan jumlah stok laptop: ", "digit")
    
    id_laptop = max(laptop['id'] for laptop in laptops) + 1 if laptops else 1
    laptops.append({"id": id_laptop, "brand": brand, "model": model, "price": price, "stock": stock})
    
    print(f"Laptop {model} dari {brand} berhasil ditambahkan.")

def read_laptops(sort_by='id', search=None, price_range=None, stock_available=None):
    """Menampilkan daftar laptop dengan opsi pencarian dan pengurutan."""
    print("\nDaftar Laptop:")
    
    filtered_laptops = laptops.copy()
    
    if search:
        filtered_laptops = [laptop for laptop in filtered_laptops if search.lower() in laptop['brand'].lower() or search.lower() in laptop['model'].lower()]
    
    if price_range:
        filtered_laptops = [laptop for laptop in filtered_laptops if price_range[0] <= laptop['price'] <= price_range[1]]
    
    if stock_available:
        filtered_laptops = [laptop for laptop in filtered_laptops if laptop['stock'] > 0]
    
    sorted_l aptops = sorted(filtered_laptops, key=lambda x: x[sort_by])
    
    if sorted_laptops:
        print(tabulate(sorted_laptops, headers='keys', tablefmt="double_outline"))  
    else:
        print("Tidak ada laptop yang tersedia.")

def update_laptop():
    """Memperbarui informasi dari laptop yang sudah ada."""
    if not laptops:
        print("Tidak ada laptop yang tersedia untuk diupdate.")
        return
    
    read_laptops()
    
    index = get_input("Masukkan ID laptop yang ingin diupdate: ", "digit") - 1
    if 0 <= index < len(laptops):
        brand = input("Masukkan merek baru (biarkan kosong untuk tidak mengubah): ").strip()
        if brand:
            laptops[index]["brand"] = brand
        
        model = input("Masukkan model baru (biarkan kosong untuk tidak mengubah): ").strip()
        if model:
            laptops[index]["model"] = model
        
        price = input("Masukkan harga baru (biarkan kosong untuk tidak mengubah): ").strip()
        if price:
            laptops[index]["price"] = float(price)
        
        stock = input("Masukkan jumlah stok baru (biarkan kosong untuk tidak mengubah): ").strip()
        if stock:
            laptops[index]["stock"] = int(stock)
        
        print("Data laptop berhasil diupdate.")
    else:
        print("ID laptop tidak valid.")

def delete_laptop():
    """Menghapus laptop dari daftar."""
    if not laptops:
        print("Tidak ada laptop yang tersedia untuk dihapus.")
        return
    
    read_laptops()
    
    index = get_input("Masukkan ID laptop yang ingin dihapus: ", "digit") - 1
    if 0 <= index < len(laptops):
        removed_laptop = laptops.pop(index)
        print(f"Laptop {removed_laptop['model']} dari {removed_laptop['brand']} berhasil dihapus.")
    else:
        print("ID laptop tidak valid.")

def sell_laptop():
    """Menjual laptop dan mengurangi stok."""
    if not laptops:
        print("Tidak ada laptop yang tersedia untuk dijual.")
        return
    
    read_laptops()
    
    index = get_input("Masukkan ID laptop yang ingin dijual: ", "digit") - 1
    if 0 <= index < len(laptops):
        quantity = get_input("Masukkan jumlah yang ingin dijual: ", "digit")
        if quantity <= laptops[index]["stock"]:
            laptops[index]["stock"] -= quantity
            total_price = quantity * laptops[index]["price"]
            sales_history.append({
                "id": laptops[index]["id"],
                "brand": laptops[index]["brand"],
                "model": laptops[index]["model"],
                "quantity": quantity,
                "total_price": total_price
            })
            print(f"Laptop {laptops[index]['model']} dari {laptops[index]['brand']} berhasil dijual sebanyak {quantity} unit dengan harga total Rp {total_price:,}.")
        else:
            print("Jumlah stok tidak cukup.")
    else:
        print("ID laptop tidak valid.")

def view_sales_history():
    """Menampilkan riwayat penjualan laptop."""
    if sales_history:
        print("\nRiwayat Penjualan:")
        table = [[index + 1, sale["id"], sale["brand"], sale["model"], sale["quantity"], sale["total_price"]] for index, sale in enumerate(sales_history)]
        print(tabulate(table, headers=["No", "ID", "Merek", "Model", "Jumlah", "Harga Total"], tablefmt="double_outline"))  
    else:
        print("Tidak ada riwayat penjualan.")

def backup_data():
    """Menyimpan data laptop ke dalam file untuk cadangan."""
    if not laptops:
        print("Tidak ada data untuk dicadangkan.")
        return
    
    try:
        with open('laptops_backup.txt', 'w') as f:
            for laptop in laptops:
                f.write(f"ID: {laptop['id']}, Merek: {laptop['brand']}, Model: {laptop['model']}, Harga: {laptop['price']}, Stok: {laptop['stock']}\n")
        print("Data telah dicadangkan ke laptops_backup.txt.")
    except IOError as e:
        print(f"Terjadi kesalahan saat mencadangkan data: {e}")

def view_backup_data():
    """Menampilkan data laptop yang telah dicadangkan."""
    try:
        with open('laptops_backup.txt', 'r') as f:
            print(f.read())
    except IOError as e:
        print(f"Terjadi kesalahan saat membaca data cadangan: {e}")

def main():
    while True:
        print("\nMenu:")
        print("1. T ambah Laptop")
        print("2. Lihat Daftar Laptop")
        print("3. Update Laptop")
        print("4. Hapus Laptop")
        print("5. Jual Laptop")
        print("6. Lihat Riwayat Penjualan")
        print("7. Cadangkan Data")
        print("8. Lihat Data Cadangan")
        print("9. Keluar")
        print("10. Bantuan")
        
        choice = get_input("=== PENJUALAN LAPTOP ===\nMasukkan pilihan: ", "choice")
        
        if choice == "1":
            create_laptop()
        elif choice == "2":
            read_laptops()
        elif choice == "3":
            update_laptop()
        elif choice == "4":
            delete_laptop()
        elif choice == "5":
            sell_laptop()
        elif choice == "6":
            view_sales_history()
        elif choice == "7":
            backup_data()
        elif choice == "8":
            view_backup_data()
        elif choice == "9":
            break
        elif choice == "10":
            show_help()

main()