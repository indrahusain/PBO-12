import logging
from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod

# -------------------------
# Konfigurasi Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# -------------------------
# Models
# -------------------------
ScheduleEntry = Tuple[str, int, int]  # (day, start_minute, end_minute)

@dataclass
class Course:
    code: str
    name: str
    sks: int
    prerequisites: List[str]
    schedule: List[ScheduleEntry]

@dataclass
class Registration:
    student_name: str
    completed_courses: List[str]
    selected_courses: List[Course]

# -------------------------
# Abstraksi: Validation Rule
# -------------------------
class IValidationRule(ABC):
    """
    Interface abstrak untuk semua aturan validasi pendaftaran.
    Menerapkan prinsip Open/Closed Principle (OCP).
    """

    @abstractmethod
    def validate(self, registration: Registration) -> Tuple[bool, str]:
        """
        Memvalidasi data pendaftaran berdasarkan aturan tertentu.

        Args:
            registration (Registration): Objek data pendaftaran mahasiswa yang berisi
                                         mata kuliah yang dipilih dan riwayat studi.

        Returns:
            Tuple[bool, str]: Tuple berisi status validasi (True/False) dan pesan 
                              keterangan (sukses atau error).
        """
        pass

# -------------------------
# Implementasi Rule
# -------------------------
class SksLimitRule(IValidationRule):
    """
    Aturan validasi untuk memeriksa batas maksimum SKS yang diambil.
    """

    def __init__(self, max_sks: int):
        """
        Inisialisasi rule batas SKS.

        Args:
            max_sks (int): Batas maksimum total SKS yang diizinkan.
        """
        self.max_sks = max_sks

    def validate(self, registration: Registration) -> Tuple[bool, str]:
        """
        Memeriksa apakah total SKS dari mata kuliah yang dipilih melebihi batas.

        Args:
            registration (Registration): Data pendaftaran.

        Returns:
            Tuple[bool, str]: (False, Pesan Error) jika melebihi batas, 
                              (True, "SKS OK") jika aman.
        """
        total = sum(c.sks for c in registration.selected_courses)
        logger.info(f"Memeriksa total SKS: {total}/{self.max_sks}")
        
        if total > self.max_sks:
            msg = f"Total SKS ({total}) melebihi batas maksimum ({self.max_sks})."
            logger.warning(msg)
            return False, msg
        
        return True, "SKS OK."

class PrerequisiteRule(IValidationRule):
    """
    Aturan validasi untuk memeriksa prasyarat mata kuliah.
    """

    def validate(self, registration: Registration) -> Tuple[bool, str]:
        """
        Memastikan mahasiswa sudah lulus semua mata kuliah prasyarat
        untuk mata kuliah yang dipilih.

        Args:
            registration (Registration): Data pendaftaran.

        Returns:
            Tuple[bool, str]: (False, Daftar Prasyarat Kurang) jika gagal,
                              (True, "Prasyarat OK") jika sukses.
        """
        missing = []
        completed = set(registration.completed_courses)
        
        logger.info("Memeriksa prasyarat mata kuliah...")
        
        for course in registration.selected_courses:
            for pre in course.prerequisites:
                if pre not in completed:
                    missing.append((course.code, pre))
        
        if missing:
            msgs = [f"{c} butuh {p}" for c, p in missing]
            full_msg = "Prasyarat tidak terpenuhi: " + ", ".join(msgs)
            logger.warning(full_msg)
            return False, full_msg
        
        return True, "Prasyarat OK."

class JadwalBentrokRule(IValidationRule):
    """
    Aturan validasi untuk mendeteksi jadwal bentrok antar mata kuliah.
    """

    def validate(self, registration: Registration) -> Tuple[bool, str]:
        """
        Memeriksa apakah ada irisan waktu (bentrok) antara jadwal 
        mata kuliah yang dipilih.

        Args:
            registration (Registration): Data pendaftaran.

        Returns:
            Tuple[bool, str]: (False, Detail Bentrok) jika ada jadwal tumpang tindih,
                              (True, "Tidak ada jadwal bentrok") jika aman.
        """
        entries = []  # (day, start, end, course_code)
        
        logger.info("Memeriksa bentrok jadwal...")

        for course in registration.selected_courses:
            for (day, s, e) in course.schedule:
                entries.append((day, s, e, course.code))
        
        for i in range(len(entries)):
            day_i, s_i, e_i, c_i = entries[i]
            for j in range(i+1, len(entries)):
                day_j, s_j, e_j, c_j = entries[j]
                
                if day_i != day_j:
                    continue
                
                # Cek overlap waktu
                if s_i < e_j and s_j < e_i:
                    start_str = format_time(s_i)
                    end_str = format_time(e_i)
                    start_j_str = format_time(s_j)
                    end_j_str = format_time(e_j)
                    
                    msg = (f"Jadwal bentrok antara {c_i} ({start_str}-{end_str}) "
                           f"dan {c_j} ({start_j_str}-{end_j_str})")
                    logger.warning(msg)
                    return False, msg
                    
        return True, "Tidak ada jadwal bentrok."

def format_time(minutes: int) -> str:
    """Helper untuk format menit ke HH:MM."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

# -------------------------
# Koordinator: RegistrationService
# -------------------------
class RegistrationService:
    """
    Service utama untuk menangani proses validasi pendaftaran mahasiswa.
    Menggunakan Dependency Injection untuk menerima daftar aturan validasi.
    """

    def __init__(self, rules: List[IValidationRule]):
        """
        Inisialisasi RegistrationService.

        Args:
            rules (List[IValidationRule]): Daftar aturan validasi yang akan diterapkan.
        """
        self.rules = rules

    def run_registration(self, registration: Registration) -> Tuple[bool, List[str]]:
        """
        Menjalankan semua validasi terhadap data pendaftaran.

        Args:
            registration (Registration): Objek data pendaftaran.

        Returns:
            Tuple[bool, List[str]]: (True, Success Messages) jika semua lolos,
                                    (False, Error Messages) jika ada satu saja yang gagal.
        """
        logger.info(f"Memulai validasi pendaftaran untuk: {registration.student_name}")
        
        errors = []
        for rule in self.rules:
            ok, msg = rule.validate(registration)
            if not ok:
                errors.append(msg)
        
        if errors:
            logger.error(f"Validasi gagal dengan {len(errors)} error.")
            return False, errors
        
        logger.info("Semua validasi berhasil.")
        return True, ["Validasi sukses."]

# -------------------------
# Demo / Main
# -------------------------
def minutes(h, m=0):
    return h*60 + m

def demo():
    # Setup Data Dummy
    mat101 = Course("MAT101", "Matematika Dasar", 3, [], [("Senin", minutes(9,0), minutes(11,0))])
    fis201 = Course("FIS201", "Fisika I", 4, ["MAT101"], [("Senin", minutes(10,30), minutes(12,0))]) # Bentrok dengan MAT101
    ifs300 = Course("IFS300", "Ilmu Komputer Lanjut", 3, ["MAT101", "FIS201"], [("Selasa", minutes(9,0), minutes(11,0))])

    # Skenario: Ani belum lulus FIS201, tapi mengambil IFS300 (Gagal Prasyarat)
    # Dan jadwal MAT101 bentrok dengan FIS201
    reg = Registration(student_name="Ani", completed_courses=["MAT101"], selected_courses=[mat101, fis201, ifs300])

    rules = [
        SksLimitRule(max_sks=24),
        PrerequisiteRule(),
        JadwalBentrokRule(),
    ]

    service = RegistrationService(rules=rules)

    print("\n--- OUTPUT TERMINAL ---")
    ok, messages = service.run_registration(reg)
    
    # Bagian print() di bawah ini boleh tetap ada untuk menampilkan hasil akhir ke User (UI Console)
    # Tugas hanya meminta mengganti print() DI DALAM logic class (RegistrationService & Rules)
    if not ok:
        print("\nHASIL: Registrasi Ditolak")
        for m in messages:
            print(f"- {m}")
    else:
        print("\nHASIL: Registrasi Diterima")

if __name__ == "__main__":
    demo()