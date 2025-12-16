import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# [P12: Logging Setup]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s %(message)s'
)
LOGGER = logging.getLogger('Registration')

@dataclass
class Student:
    """
    Merepresentasikan data mahasiswa untuk keperluan validasi.
    
    Attributes:
        name (str): Nama lengkap mahasiswa.
        current_sks (int): Jumlah SKS yang sedang diambil.
        has_completed_prerequisite (bool): Status pemenuhan prasyarat mata kuliah.
    """
    name: str
    current_sks: int
    has_completed_prerequisite: bool

# ABSTRAKSI (Kontrak untuk OCP/DIP)
class IValidationRule(ABC):
    """
    Kontrak (Interface) untuk semua aturan validasi registrasi. (DIP)
    
    Semua aturan harus mengimplementasikan method validate().
    """
    @abstractmethod
    def validate(self, student: Student) -> bool:
        """
        Method yang akan dieksekusi untuk memvalidasi mahasiswa.
        
        Args:
            student (Student): Objek mahasiswa yang divalidasi.
            
        Returns:
            bool: True jika validasi sukses, False jika gagal.
        """
        pass

# IMPLEMENTASI KONKRIT (Memenuhi SRP)
class SksLimitRule(IValidationRule):
    """
    Aturan validasi tunggal untuk memastikan batas maksimum SKS tidak terlampaui. (SRP)
    """
    def validate(self, student: Student) -> bool:
        """Memeriksa apakah SKS mahasiswa melebihi batas (24 SKS)."""
        MAX_SKS = 24
        if student.current_sks > MAX_SKS:
            # [P12: Logging WARNING]
            LOGGER.warning(f"SKS Limit GAGAL untuk {student.name}. SKS: {student.current_sks} > {MAX_SKS}.")
            return False
        # [P12: Logging INFO]
        LOGGER.info(f"SKS Limit SUKSES: {student.name} ({student.current_sks} SKS).")
        return True

class PrerequisiteRule(IValidationRule):
    """
    Aturan validasi tunggal untuk memastikan prasyarat mata kuliah terpenuhi. (SRP)
    """
    def validate(self, student: Student) -> bool:
        """Memeriksa status pemenuhan prasyarat."""
        if not student.has_completed_prerequisite:
            # [P12: Logging WARNING]
            LOGGER.warning(f"Prasyarat GAGAL untuk {student.name}.")
            return False
        # [P12: Logging INFO]
        LOGGER.info(f"Prasyarat SUKSES: {student.name}.")
        return True

# KELAS KOORDINATOR (SRP & DIP)
class RegistrationService:
    """
    Kelas high-level untuk mengkoordinasi seluruh proses validasi registrasi. (SRP)
    Kelas ini bergantung pada Abstraksi IValidationRule (DIP).
    """
    def __init__(self, rules: list[IValidationRule]):
        """
        Menginisialisasi RegistrationService dengan daftar aturan validasi.
        
        Args:
            rules (list[IValidationRule]): Daftar objek aturan validasi yang akan disuntikkan (Dependency Injection).
        """
        self.rules = rules

    def register_student(self, student: Student) -> bool:
        """
        Menjalankan semua aturan validasi yang disuntikkan.
        
        Args:
            student (Student): Objek mahasiswa yang akan didaftarkan.
            
        Returns:
            bool: True jika semua validasi sukses, False jika ada yang gagal.
        """
        # [P12: Logging INFO]
        LOGGER.info(f"--- Memproses Pendaftaran: {student.name} ---")
        for rule in self.rules:
            if not rule.validate(student):
                # [P12: Logging ERROR]
                LOGGER.error(f"🛑 Pendaftaran GAGAL untuk {student.name} karena pelanggaran aturan.")
                return False
        
        # [P12: Logging INFO]
        LOGGER.info(f"🎉 Pendaftaran SUKSES untuk {student.name}.")
        return True

# --- PROGRAM UTAMA (Pembuktian OCP) ---

# Data Mahasiswa
andi = Student("Andi Gagal SKS", 25, True) 
budi = Student("Budi Gagal Prasyarat", 18, False) 
cindy = Student("Cindy Sukses", 18, True) 

# Setup Dependencies
sks_rule = SksLimitRule()
prereq_rule = PrerequisiteRule()
initial_rules = [sks_rule, prereq_rule]

# Skenario 1: Uji dengan 2 Aturan Awal
reg_service_initial = RegistrationService(rules=initial_rules)
reg_service_initial.register_student(andi) 
reg_service_initial.register_student(budi)

# Pembuktian OCP: Menambah Aturan Baru (Tanpa Mengubah RegistrationService) [cite: 208]
class TuitionPaymentRule(IValidationRule):
    """Aturan baru: Validasi pembayaran SPP."""
    def validate(self, student: Student) -> bool:
        # [P12: Logging INFO]
        LOGGER.info(f"Pembayaran SPP SUKSES: {student.name}.")
        return True

# Skenario 2: Uji dengan Aturan Baru (OCP Terpenuhi)
payment_rule = TuitionPaymentRule()
new_rules = [sks_rule, prereq_rule, payment_rule] # Ekstensi: Aturan baru ditambahkan melalui konfigurasi

reg_service_ocp = RegistrationService(rules=new_rules)
reg_service_ocp.register_student(cindy)