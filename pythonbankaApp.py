#Dilek Yılmaz 21360859045
import json


class Transaction:
    def __init__(self, account, miktar):
        self.account = account
        self.miktar = miktar

    def paraDondur(self):
        return self.miktar

    @staticmethod
    def paraCek(transaction, miktar):
        account = transaction.account
        account.balance -= miktar
        return -miktar

    @staticmethod
    def paraEkle(transaction, miktar):
        account = transaction.account
        account.balance += miktar
        return miktar

def paraCek(miktar):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if miktar < 0:
                print("Negatif miktar para çekilemez.")
            else:
                func(self, *args, **kwargs)
        return wrapper
    return decorator

def paraEkle(miktar):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if miktar < 0:
                print("Negatif miktar para eklenemez.")
            else:
                func(self, *args, **kwargs)
        return wrapper
    return decorator

class Account:
    def __init__(self, account_type, account_name, balance):
        self._account_type = account_type
        self._account_name = account_name
        self._balance = balance

        if balance < 0:
            raise ValueError("Hesap bakiyesi negatif olamaz.")

    @property
    def account_type(self):
        return self._account_type

    @property
    def account_name(self):
        return self._account_name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Hesap bakiyesi negatif olamaz.")
        else:
            self._balance = value

    def hesapKapat(self):
        pass

class SavingAccount(Account):
    def hesapKapat(self):
        closing_miktar = self.balance * 0.1
        self.balance -= closing_miktar
        print(f"{self.account_name} ({self.account_type}) hesabı kapatıldı. Kapanma miktarı: {closing_miktar}, Yeni bakiye: {self.balance}")

class NormalAccount(Account):
    def hesapKapat(self):
        print(f"{self.account_name} ({self.account_type}) hesabı kapatıldı. Bakiye: {self.balance}")

class BankApp:
    def __init__(self):
        self.accounts = {}

    def hesapOlustur(self, account_name, account_type, balance):
        if account_name in self.accounts:
            print("Hesap zaten var.")
        else:
            if account_type == "SavingAccount":
                account = SavingAccount(account_type, account_name, balance)
            elif account_type == "NormalAccount":
                account = NormalAccount(account_type, account_name, balance)
            else:
                print("Geçersiz hesap türü.")
                return
            self.accounts[account_name] = account
            print(f"{account_name} adlı hesap oluşturuldu.")

    def hesapKapat(self, account_name):
        if account_name in self.accounts:
            account = self.accounts[account_name]
            account.hesapKapat()
            del self.accounts[account_name]
        else:
            print("Hesap bulunamadı.")

    def paraTransfer(self, sender_name, receiver_name, miktar):
        if sender_name in self.accounts and receiver_name in self.accounts:
            sender_account = self.accounts[sender_name]
            receiver_account = self.accounts[receiver_name]
            if sender_account.balance >= miktar:
                sender_transaction = Transaction(sender_account, miktar)
                receiver_transaction = Transaction(receiver_account, miktar)
                self.paraGuncelle(sender_transaction, 'paraCek')
                self.paraGuncelle(receiver_transaction, 'paraEkle')
                print(f"{miktar} TL, {sender_name} hesabından {receiver_name} hesabına transfer edildi.")
            else:
                print(f"{sender_name} hesabında yeterli bakiye yok.")
        else:
            print("Hesap(lar) bulunamadı.")

    def kaydetVeYukle(self):
        try:
            with open("accounts.json", "w") as file:
                json.dump([{"_account_type": acc.account_type, "_account_name": acc.account_name, "_balance": acc.balance} for acc in self.accounts.values()], file)
            print("Hesaplar başarıyla dosyaya kaydedildi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")

        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                self.accounts = {acc["_account_name"]: SavingAccount(acc["_account_type"], acc["_account_name"], acc["_balance"]) if acc["_account_type"] == "SavingAccount" else NormalAccount(acc["_account_type"], acc["_account_name"], acc["_balance"]) for acc in data}
            print("Hesaplar başarıyla dosyadan yüklendi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def paraGuncelle(self, transaction, operation):
        if isinstance(transaction, Transaction):
            if operation == 'paraCek':
                transaction.paraCek(transaction, transaction.miktar)
            elif operation == 'paraEkle':
                transaction.paraEkle(transaction, transaction.miktar)
            else:
                raise ValueError("Geçersiz işlem türü. (paraCek veya paraEkle)")
        else:
            raise TypeError("Geçersiz Transaction nesnesi.")

    def goster(self):
        if not self.accounts:
            print("Henüz hesap bulunmamaktadır.")
        else:
            print(" ---------------------------")
            for account_name, account in self.accounts.items():
                print(f"{account_name} ({account.account_type}) : {account.balance}")

    def hesaplariYukle(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                self.accounts = {acc["_account_name"]: SavingAccount(acc["_account_type"], acc["_account_name"], acc["_balance"]) if acc["_account_type"] == "SavingAccount" else NormalAccount(acc["_account_type"], acc["_account_name"], acc["_balance"]) for acc in data}
            print("Hesaplar başarıyla dosyadan yüklendi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")

# İşlem Menüsü
bank_app = BankApp()

while True:
    print(">>>>>>İŞLEM MENÜSÜ<<<<<<")
    print("1. Hesap oluştur")
    print("2. Hesap kapat")
    print("3. Kaydet ve yükle")
    print("4. Para çek")
    print("5. Para yatır")
    print("6. Para transferi")
    print("7. Göster")
    print("8. Çıkış")

    choice = input("Yapmak istediğiniz işlemi seçin (1-8): ")

    if choice == "1":
        account_name = input("Hesap adını girin: ")
        account_type = input("Hesap türünü girin (SavingAccount/NormalAccount): ")
        balance = float(input("Hesap bakiyesini girin: "))
        bank_app.hesapOlustur(account_name, account_type, balance)
    elif choice == "2":
        account_name = input("Kapatmak istediğiniz hesabın adını girin: ")
        bank_app.hesapKapat(account_name)
    elif choice == "3":
        bank_app.kaydetVeYukle()
    elif choice == "4":
        account_name = input("Para çekmek istediğiniz hesabın adını girin: ")
        miktar = float(input("Çekmek istediğiniz miktarı girin: "))
        transaction = Transaction(bank_app.accounts[account_name], miktar)
        bank_app.paraGuncelle(transaction, 'paraCek')
        print(f"{miktar} TL çekildi. Yeni bakiye: {bank_app.accounts[account_name].balance}")
    elif choice == "5":
        account_name = input("Para yatırmak istediğiniz hesabın adını girin: ")
        miktar = float(input("Yatırmak istediğiniz miktarı girin: "))
        transaction = Transaction(bank_app.accounts[account_name], miktar)
        bank_app.paraGuncelle(transaction, 'paraEkle')
        print(f"{miktar} TL yatırıldı. Yeni bakiye: {bank_app.accounts[account_name].balance}")
    elif choice == "6":
        sender_name = input("Para transferi yapmak istediğiniz hesabın adını girin: ")
        receiver_name = input("Para transferi almak istediğiniz hesabın adını girin: ")
        miktar = float(input("Transfer etmek istediğiniz miktarı girin: "))
        bank_app.paraTransfer(sender_name, receiver_name, miktar)
    elif choice == "7":
        bank_app.goster()
    elif choice == "8":
        break
    else:
        print("Geçersiz seçenek. Lütfen tekrar deneyin.")
