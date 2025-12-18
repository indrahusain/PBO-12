import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# ==========================================
# KONFIGURASI LOGGING (Langkah 2 - Gambar 1)
# ==========================================
# Pastikan import logging ada di awal file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# Tambahkan logger untuk kelas yang akan kita gunakan
LOGGER = logging.getLogger('Checkout')

# ==========================================
# MODEL & ABSTRAKSI
# ==========================================
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

class IPaymentProcessor(ABC):
    """Kontrak: Semua prosesor pembayaran harus punya method 'process'."""
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    """Kontrak: Semua layanan notifikasi harus punya method 'send'."""
    @abstractmethod
    def send(self, order: Order):
        pass

# ==========================================
# IMPLEMENTASI KONKRIT
# ==========================================
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        # Kita gunakan print di sini karena ini simulasi proses eksternal
        print("Payment: Memproses Kartu Kredit.") 
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# ==========================================
# KELAS UTAMA (Target Modifikasi)
# ==========================================
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran.
    
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """

    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Menginisialisasi CheckoutService dengan dependensi yang diperlukan.

        Args:
            payment_processor (IPaymentProcessor): Implementasi interface pembayaran.
            notifier (INotificationService): Implementasi interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.

        Args:
            order (Order): Objek pesanan yang akan diproses.

        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """
        # Implementasi Logging (Langkah 2 & 3 - Gambar 1 & 4)
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}")

        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            
            # Log sukses
            LOGGER.info("Checkout Sukses. Status pesanan: PAID.")
            return True
        else:
            # Log error/warning jika gagal
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.")
            return False

# ==========================================
# PROGRAM UTAMA (Main)
# ==========================================
if __name__ == "__main__":
    # Setup Dependencies
    andi_order = Order("Andi", 500000)
    email_service = EmailNotifier()
    cc_processor = CreditCardProcessor()

    # Injeksi Dependensi
    checkout_service = CheckoutService(payment_processor=cc_processor, notifier=email_service)
    
    # Jalankan Checkout
    print("\n--- Log Output ---")
    checkout_service.run_checkout(andi_order)