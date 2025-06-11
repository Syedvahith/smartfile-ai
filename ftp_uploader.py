from ftplib import FTP
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

def upload_to_ftp(local_file_path):
    try:
        # Load FTP credentials from .env
        ftp_ip = os.getenv("ftp_ip")
        ftp_port = int(os.getenv("ftp_port"))
        ftp_user = os.getenv("ftp_user")
        ftp_pass = os.getenv("ftp_pass")
        ftp_target_base_dir = "/FTP_Test"

        # Prepare directory & filename
        current_date = datetime.now().strftime('%d%m%y')
        ftp_target_dir = f"{ftp_target_base_dir}/{current_date}"
        file_name = os.path.basename(local_file_path)

        # Connect to FTP
        ftp = FTP()
        ftp.connect(ftp_ip, ftp_port)
        ftp.login(ftp_user, ftp_pass)

        # Navigate or create dated folder
        try:
            ftp.cwd(ftp_target_dir)
        except Exception:
            ftp.cwd(ftp_target_base_dir)
            ftp.mkd(current_date)
            ftp.cwd(ftp_target_dir)

        # Upload file
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {file_name}', file)

        print(f"✅ File uploaded to FTP: {ftp_target_dir}/{file_name}")
        ftp.quit()
        return True

    except Exception as e:
        print(f"❌ FTP upload failed: {e}")
        return False
