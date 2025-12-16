from dataclasses import dataclass

@dataclass
class Student:
    """Model data mahasiswa."""
    name: str
    current_sks: int
    has_completed_prerequisite: bool

# === KODE BURUK (SEBELUM REFACTOR) ===
class RegistrationValidator: # Melanggar SRP, OCP, DIP
    
    def validate_registration(self, student: Student, rule_type: str) -> bool:
        print(f"Memulai validasi untuk Mahasiswa: {student.name}")
        
        # LOGIKA GABUNGAN (Pelanggaran SRP, OCP, DIP)
        if rule_type == "sks_limit":
            # Tanggung jawab 1
            MAX_SKS = 24
            if student.current_sks > MAX_SKS:
                print(f"❌ Validasi Gagal: SKS melebihi batas {MAX_SKS}.")
                return False
            print("✅ Validasi SKS Sukses.")
            return True

        elif rule_type == "prerequisite":
            # Tanggung jawab 2
            if not student.has_completed_prerequisite:
                print("❌ Validasi Gagal: Prasyarat mata kuliah belum dipenuhi.")
                return False
            print("✅ Validasi Prasyarat Sukses.")
            return True
            
        else:
            print("Metode validasi tidak valid.")
            return False

# --- PENGGUNAAN KODE BURUK ---
andi = Student("Andi Gagal SKS", 25, True) 
budi = Student("Budi Gagal Prasyarat", 18, False) 

validator = RegistrationValidator()

print("\n--- Skenario 1: Validasi SKS (Andi) ---")
validator.validate_registration(andi, "sks_limit")

print("\n--- Skenario 2: Validasi Prasyarat (Budi) ---")
validator.validate_registration(budi, "prerequisite")