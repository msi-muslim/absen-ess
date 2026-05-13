import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# --- CONFIG ---
URL_LOGIN = "https://ess.mastersystem.co.id/SignIn/tabid/78/Default.aspx?returnurl=%2fHome.aspx"
URL_ROSTER = "https://ess.mastersystem.co.id/Transaction/Attendance/Roster.aspx"

USERNAME = "<INPUT_YOUR_USERNAME>"
PASSWORD = "<INPUT_YOUR_PASSWORD>"

# PARAMETER TANGGAL (Ganti di sini)
# Format: MM/DD/YYYY (Bulan/Tanggal/Tahun)
TGL_FROM = "<INPUT_DATE_FROM>" 
TGL_TO   = "<INPUT_DATE_TO>"

# Folder session
PROFILE_PATH = os.path.join(os.getcwd(), "selenium_profile")

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={PROFILE_PATH}") 
options.add_argument("--profile-directory=Default")
options.add_experimental_option("detach", True) 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    wait = WebDriverWait(driver, 15)
    
    # 1. Buka halaman (Cek session)
    print("Mengecek status session...")
    driver.get(URL_LOGIN)
    time.sleep(3) 

    if "SignIn" in driver.current_url:
        print("🔑 Memulai proses login...")
        wait.until(EC.presence_of_element_located((By.ID, "dnn_ctr466_Login_Login_DNN_txtUsername"))).send_keys(USERNAME)
        driver.find_element(By.ID, "dnn_ctr466_Login_Login_DNN_txtPassword").send_keys(PASSWORD)
        driver.find_element(By.ID, "dnn_ctr466_Login_Login_DNN_cmdLogin").click()
        time.sleep(5)
    else:
        print("✅ Session masih aktif!")

    # 2. Masuk ke Halaman Roster
    print(f"Navigasi ke: {URL_ROSTER}")
    driver.get(URL_ROSTER)
    
    # 3. Isi Tanggal
    print(f"Mengisi Roster dari {TGL_FROM} sampai {TGL_TO}...")
    
    def isi_tanggal_manual(selector_id, text):
        def eksekusi():
            print(f"Proses input ke {selector_id}...")
            # 1. Cari elemen fresh
            element = wait.until(EC.element_to_be_clickable((By.ID, selector_id)))
            
            # 2. Pastikan fokus
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            element.click()
            driver.execute_script("arguments[0].focus();", element)
            time.sleep(1)
            
            # 3. Hapus isi lama
            element.send_keys(Keys.COMMAND, "a")
            element.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            
            # 4. Ketik satu per satu
            for char in text:
                element.send_keys(char)
                time.sleep(0.1)
            
            time.sleep(1)
            element.send_keys(Keys.ENTER)

        try:
            print(f"\n--- Memulai input: {selector_id} ---")
            eksekusi()
        except:
            # Jika kena StaleElement atau error karena refresh mendadak, coba sekali lagi
            print("⚠️ Web melakukan refresh mendadak. Menunggu 5 detik dan mencoba ulang...")
            time.sleep(5)
            eksekusi()
        
        # Jeda krusial untuk sinkronisasi postback web
        print("Menunggu sinkronisasi sistem (7 detik)...")
        time.sleep(7)

    print("Step 1: Mengisi From Date...")
    isi_tanggal_manual("dnn_ctr435_RosterRequest_ASPxFormLayout1_cmbFromDate_I", TGL_FROM)
    
    print("Step 2: Mengisi To Date...")
    isi_tanggal_manual("dnn_ctr435_RosterRequest_ASPxFormLayout1_cmbToDate_I", TGL_TO)

    # 4. Klik Tombol ADD
    print("\nStep 3: Mencoba klik tombol ADD...")
    try:
        # Tunggu tombol Add muncul dan bisa diklik
        btn_add = wait.until(EC.element_to_be_clickable((By.ID, "dnn_ctr435_RosterRequest_ASPxFormLayout1_ASPxGridView1_EmptyRow_btnAdd_0")))
        
        # Scroll biar keliatan
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_add)
        time.sleep(1)
        
        btn_add.click()
        print("✅ Tombol ADD berhasil diklik!")
        
        # 5. Centang Checkbox & Klik OK (Pop-up)
        print("\nStep 4: Mencoba centang Checkbox & Klik OK...")
        time.sleep(3) # Tunggu pop-up muncul
        
        # Klik SPAN checkbox (karena input aslinya di-hide/opacity 0)
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "dnn_ctr435_RosterRequest_EmployeeTransaction_infoleft2_ASPxGridView1_DXSelBtn0_D")))
        checkbox.click()
        print("✅ Checkbox dicentang.")
        
        time.sleep(1.5)
        
        # Klik tombol OK
        btn_ok = wait.until(EC.element_to_be_clickable((By.ID, "dnn_ctr435_RosterRequest_EmployeeTransaction_btnEmployeeTransactionOk")))
        btn_ok.click()
        print("✅ Tombol OK awal berhasil diklik!")
        
        # 6. Set Paging ke "All" (Biar semua baris muncul, gak kepotong halaman)
        print("\nStep 4.5: Mengubah Page Size ke 'All'...")
        try:
            # Buka menu dropdown paging
            pager_button = wait.until(EC.element_to_be_clickable((By.ID, "dnn_ctr435_RosterRequest_ASPxSplitter1_ASPxGridView2_DXPagerBottom_PSB")))
            pager_button.click()
            time.sleep(1.5)
            
            # Pilih opsi "All" (ID DXI5 sesuai HTML lu)
            all_option = wait.until(EC.element_to_be_clickable((By.ID, "dnn_ctr435_RosterRequest_ASPxSplitter1_ASPxGridView2_DXPagerBottom_PSP_DXI5_")))
            all_option.click()
            
            print("✅ Page Size diubah ke 'All'. Menunggu grid refresh...")
            time.sleep(6) # Tunggu grid nampilin semua data
        except Exception as e:
            print(f"⚠️ Gagal set paging ke 'All' (Mungkin tombolnya beda atau data sudah tampil semua), lanjut...")

        # 7. Looping Pilih Row & Isi Detail
        print("\nStep 5: Memulai Looping Pengisian Roster...")
        time.sleep(3)

        # Loop untuk tiap baris (DXSelBtn0, DXSelBtn1, dst)
        for i in range(32): # Maksimal 31 hari
            selector_row = f"dnn_ctr435_RosterRequest_ASPxSplitter1_ASPxGridView2_DXSelBtn{i}_D"
            
            try:
                # Cari elemen row
                rows = driver.find_elements(By.ID, selector_row)
                if not rows:
                    print(f"\n--- Selesai! Semua baris ({i}) sudah diproses. ---")
                    break
                
                # --- PRE-CHECK JAM KERJA ---
                try:
                    selector_jam = f"dnn_ctr435_RosterRequest_ASPxSplitter1_ASPxGridView2_tccell{i}_3"
                    jam_element = driver.find_element(By.ID, selector_jam)
                    teks_jam = jam_element.text.replace("\n", " ")
                    
                    print(f"\n>>> Baris ke-{i+1} | Jam: {teks_jam}")
                    
                    # Syarat: Harus mengandung 08:00 dan 17:00
                    if "08:00" not in teks_jam or "17:00" not in teks_jam:
                        print(f"⚠️ Jam tidak sesuai (Bukan 08:00 - 17:00). SKIP baris ini.")
                        continue
                except:
                    print(f"⚠️ Gagal baca jam di baris ke-{i+1}, skip.")
                    continue

                # --- CLEAR ALL SELECTIONS FIRST ---
                # Bersihkan centang yang mungkin tersisa dari baris sebelumnya
                print("Membersihkan centang lain...")
                try:
                    checked_boxes = driver.find_elements(By.CLASS_NAME, "dxWeb_edtCheckBoxChecked_Moderno")
                    for box in checked_boxes:
                        driver.execute_script("arguments[0].click();", box)
                    if checked_boxes: time.sleep(2)
                except:
                    pass

                # 1. Centang row
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rows[0])
                time.sleep(1)
                rows[0].click()
                print(f"Row {i+1} dipilih.")
                time.sleep(4) # Tunggu form detail muncul/sinkronisasi

                # 2. Isi "Set To" -> Attendance
                isi_tanggal_manual("dnn_ctr435_RosterRequest_ASPxSplitter1_RosterDetail_ASPxFormLayout20_CmbRosterDetailSetTo_I", "Attendance")
                
                # 3. Isi "Attendance Code" -> H (Hadir)
                isi_tanggal_manual("dnn_ctr435_RosterRequest_ASPxSplitter1_RosterDetail_ASPxPageControl1_ASPxFormLayout2_cmbAttendanceCode_I", "H (Hadir)")

                # 4. Klik Tombol OK Roster (Gunakan JavaScript untuk menghindari ElementClickIntercepted)
                print("Menyimpan baris (Force Click JS)...")
                btn_ok_roster = wait.until(EC.presence_of_element_located((By.ID, "dnn_ctr435_RosterRequest_ASPxSplitter1_RosterDetail_ctl11_btnOKRoster")))
                
                # Pastikan terlihat
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_ok_roster)
                time.sleep(1)
                
                # Klik lewat JS
                driver.execute_script("arguments[0].click();", btn_ok_roster)
                
                print(f"✅ Baris ke-{i+1} BERHASIL DISIMPAN.")
                
                # Jeda krusial agar postback beres dan centang hilang/pindah
                print("Menunggu sinkronisasi postback sistem (8 detik)...")
                time.sleep(8)

            except Exception as row_err:
                print(f"❌ Gagal di baris ke-{i+1}: {row_err}")
                # Kita coba lanjut ke baris berikutnya kalau satu baris gagal
                continue

    except Exception as e:
        print(f"❌ Terjadi kesalahan fatal: {e}")

    print("\n✅ SELURUH PROSES OTOMASI SELESAI!")

except Exception as e:
    print(f"⚠️ Terjadi error: {e}")

except Exception as e:
    print(f"⚠️ Terjadi error: {e}")


# driver.quit() 

