import sys
import json
from urllib.parse import urlparse, parse_qs

import requests
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

from config_auth import AUTH_CONFIG
from Login_ui import Login_ui


class Login(QWidget, Login_ui):
    # Signal to emit when authentication is complete
    auth_complete = pyqtSignal(str)  # Emits username

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Fixed username for dummy login
        self.username = "doctor001"
        # Store reference to main window
        self.main_window = None  # Store authentication data
        self.auth_code = None
        self.hash_cid = None

        # Connect button signals
        self.btn_start_main_window.clicked.connect(
            self.start_main_form
        )  # Connect web view URL changes
        self.web_view.urlChanged.connect(self.on_url_changed)

        # Connect to handle webview resize for better fitting
        self.web_view.loadFinished.connect(self.adjust_zoom_to_fit)

        # Connect to update status when page loads
        self.web_view.loadFinished.connect(
            self.on_page_loaded
        )        # Load initial OAuth URL
        self.load_initial_url()

    def load_initial_url(self):
        """Load the initial OAuth URL"""
        initial_url = f"https://moph.id.th/oauth/redirect?client_id={AUTH_CONFIG['HEALTH_CLIENT_ID']}&redirect_uri={AUTH_CONFIG['REDIRECT_URI']}&response_type=code"
        self.web_view.setUrl(QUrl(initial_url))

        # Set up webview for better display
        self.setup_webview_display()

    def setup_webview_display(self):
        """Configure webview for optimal display"""
        # Set zoom factor to fit content better (adjust as needed)
        self.web_view.setZoomFactor(1.0)

        # Get webview page and set up viewport
        page = self.web_view.page()

        # Enable JavaScript (usually enabled by default)
        settings = page.settings()
        from PyQt6.QtWebEngineCore import QWebEngineSettings

        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

        # Inject CSS to make content responsive
        css_injection = """
        (function() {
            var meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
            document.getElementsByTagName('head')[0].appendChild(meta);
            
            // Add CSS to make content fit better
            var style = document.createElement('style');
            style.textContent = `
                body { 
                    margin: 0 !important; 
                    padding: 10px !important; 
                    box-sizing: border-box !important;
                    overflow-x: hidden !important;
                }
                * { 
                    box-sizing: border-box !important; 
                }
                .container, .main-content, .content {
                    max-width: 100% !important;
                    width: 100% !important;
                }
            `;
            document.head.appendChild(style);
        })();
        """

        # Execute the CSS injection when page loads
        page.loadFinished.connect(lambda: page.runJavaScript(css_injection))

    def adjust_zoom_to_fit(self):
        """Adjust zoom level to fit content better"""
        # Get webview dimensions
        webview_width = self.web_view.width()

        # Adjust zoom based on webview width (typical mobile-first websites expect ~375px width)
        if webview_width > 0:
            # Calculate zoom factor (assuming optimal mobile width is around 375px)
            optimal_zoom = min(webview_width / 400.0, 1.5)  # Max zoom of 1.5x
            optimal_zoom = max(optimal_zoom, 0.8)  # Min zoom of 0.8x            self.web_view.setZoomFactor(optimal_zoom)
            print(
                f"Adjusted zoom to {optimal_zoom:.2f} for webview width {webview_width}px"
            )

    def on_page_loaded(self, success):
        """Called when a page finishes loading"""
        # Progress will be shown via label_progress_login_status instead
        pass

    def on_url_changed(self, qurl):
        """Called whenever the URL changes in the web view"""
        url_string = qurl.toString()        # Check if this is a redirect URL with authorization code
        if "code=" in url_string:
            # Extract authorization code
            auth_code = self.extract_auth_code(url_string)
            if auth_code:
                self.handle_auth_code(auth_code)

        elif "error=" in url_string:
            error = self.extract_error(url_string)
            QMessageBox.warning(self, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการเข้าสู่ระบบ: {error}")
        # Other URL changes are handled by progress updates in methods

    def extract_auth_code(self, url_string):
        """Extract authorization code from URL"""
        try:
            parsed_url = urlparse(url_string)
            params = parse_qs(parsed_url.query)
            if "code" in params:
                return params["code"][0]
        except Exception as e:
            print(f"Error extracting code: {str(e)}")
        return None

    def extract_error(self, url_string):
        """Extract error from URL"""
        try:
            parsed_url = urlparse(url_string)
            params = parse_qs(parsed_url.query)
            if "error" in params:
                return params["error"][0]
        except Exception as e:
            print(f"Error extracting error: {str(e)}")
        return "Unknown error"

    def handle_auth_code(self, auth_code):
        """Handle the received authorization code"""
        # Hide panel1 (webview) and show panel2 (process status and buttons)
        self.panel1.setVisible(False)
        self.panel2.setVisible(True)
        
        # Store auth code
        self.auth_code = auth_code

        # Update progress status label - append first step
        self.append_progress_step("ขั้นตอนที่ 1: ได้รับ Authorization Code แล้ว กำลังดำเนินการ...")
        
        # Update status
        # Status updates are now shown in label_progress_login_status

        # ขั้นตอนที่ 2: แลก authorization code เป็น access token (หน่วงเวลาเล็กน้อย)
        QTimer.singleShot(1000, lambda: self.exchange_code_for_token(auth_code))

    def append_progress_step(self, step_text, style_color="#0984e3", border_color="#e9ecef"):
        """Append a new step to the progress label with new line"""
        current_text = self.label_progress_login_status.text()
        
        # If there's existing text, add a new line
        if current_text and current_text.strip():
            new_text = current_text + "\n" + step_text
        else:
            new_text = step_text
        
        self.label_progress_login_status.setText(new_text)
        self.label_progress_login_status.setStyleSheet(f"""
            QLabel {{
                color: {style_color}; 
                font-size: 18px; 
                margin: 20px; 
                padding: 20px; 
                font-weight: bold;
                text-align: center;
                background-color: #f8f9fa;
                border: 2px solid {border_color};
                border-radius: 8px;
                min-height: 60px;
                line-height: 1.6;
                max-width: 600px;
            }}
        """)

    def set_progress_final(self, final_text, style_color="#00b894", border_color="#00b894"):
        """Set the final progress message (replaces all previous text)"""
        self.label_progress_login_status.setText(final_text)
        self.label_progress_login_status.setStyleSheet(f"""
            QLabel {{
                color: {style_color}; 
                font-size: 20px; 
                margin: 20px; 
                padding: 25px; 
                font-weight: bold; 
                line-height: 1.8;
                text-align: center;
                background-color: #f8f9fa;
                border: 2px solid {border_color};
                border-radius: 12px;
                min-height: 120px;
                max-width: 600px;
            }}
        """)

    def exchange_code_for_token(self, auth_code):
        """Exchange authorization code for access token (ขั้นตอนที่ 2)"""
        client_id = AUTH_CONFIG["HEALTH_CLIENT_ID"]
        client_secret = AUTH_CONFIG["HEALTH_CLIENT_SECRET"]
        redirect_uri = AUTH_CONFIG["REDIRECT_URI"]

        if not all([client_id, client_secret, redirect_uri]):
            print("Missing required configuration variables")
            return None

        # Token endpoint URL
        token_url = "https://moph.id.th/api/v1/token"

        # ข้อมูลสำหรับขอ access token
        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        # Headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # แสดงข้อมูลที่จะส่ง (สำหรับ debug)
        print(f"Token URL: {token_url}")
        print(f"Request Data: {token_data}")
        print(f"Headers: {headers}")        # ส่ง request ขอ access token
        self.append_progress_step("ขั้นตอนที่ 2: กำลังขอ Access Token...")

        try:
            response = requests.post(
                token_url, data=token_data, headers=headers, timeout=30
            )

            # แสดงข้อมูล response แบบละเอียด
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Text: {response.text}")

            if response.status_code == 200:
                token_response = response.json()
                print(f"Token Response: {json.dumps(token_response, indent=2)}")
                access_token = token_response.get("data").get("access_token")
                print("Access Token :", access_token)
                self.append_progress_step("ขั้นตอนที่ 2: ได้รับ Access Token แล้ว กำลังเชื่อมต่อ Provider...")
                QTimer.singleShot(1000, lambda: self.get_provider_token(access_token))
            else:
                print(f"Token exchange failed: {response.text}")

        except Exception as e:
            print(f"Error during token exchange: {str(e)}")

    def get_provider_token(self, access_token):
        """Get provider token from Health ID service (ขั้นตอนที่ 3)"""
        provider_token_url = "https://provider.id.th/api/v1/services/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        body = {
            "client_id": AUTH_CONFIG["PROVIDER_CLIENT_ID"],
            "secret_key": AUTH_CONFIG["PROVIDER_CLIENT_SECRET"],
            "token_by": "Health ID",
            "token": access_token,
        }
        print("get provider token body", body)

        try:
            response = requests.post(provider_token_url, headers=headers, data=body)

            if response.status_code == 200:
                print("Provider Token Response:", response.json())
                provider_token = response.json().get("data").get("access_token")
                self.append_progress_step(
                    "ขั้นตอนที่ 3: กำลังทำการตรวจสอบข้อมูลผู้ให้บริการ..."
                )

                QTimer.singleShot(
                    1000, lambda: self.get_provider_profile(provider_token)
                )
            else:
                print("Error getting provider token:", response.text)

        except Exception as e:
            print(f"Error getting provider token: {str(e)}")

    def get_provider_profile(self, provider_access_token):
        """Get provider profile from Provider ID service (ขั้นตอนที่ 4)"""
        url = f"https://provider.id.th/api/v1/services/profile?position_type=1"
        headers = {
            "client-id": AUTH_CONFIG["PROVIDER_CLIENT_ID"],
            "secret-key": AUTH_CONFIG["PROVIDER_CLIENT_SECRET"],
            "Authorization": f"Bearer {provider_access_token}",
        }

        try:
            response = requests.get(url, headers=headers)
            print("Provider Profile Response:", response.json())

            if response.status_code == 200:
                profile_data = response.json().get("data")
                if profile_data:
                    title_th = profile_data.get("title_th")
                    name_th = profile_data.get("name_th")
                    hash_cid = profile_data.get("hash_cid")
                    self.hash_cid = hash_cid  # Store hash_cid
                    organization = profile_data.get("organization")
                    org = organization[0] if organization else None

                    hcode = org.get("hcode") if org else None
                    position = org.get("position") if org else None
                    organization_name = (
                        org.get("hname_th") if org else None
                    )  # Update username with real data
                    self.username = f"{title_th}{name_th}"                    # Add step 4 progress first
                    self.append_progress_step("ขั้นตอนที่ 4: ได้รับข้อมูลโปรไฟล์แล้ว กำลังเตรียมระบบ...")
                    
                    # Then show final success message
                    self.set_progress_final(
                        f"🎉 เข้าสู่ระบบสำเร็จ!\n\n{title_th}{name_th}\nตำแหน่ง: {position}\nหน่วยงาน: ({hcode}) {organization_name}"
                    )

                    # Update status bar

                    # Show the start button only after getting hash_cid
                    self.btn_start_main_window.setVisible(True)
                else:
                    QMessageBox.warning(self, "ข้อผิดพลาด", "ไม่พบข้อมูลโปรไฟล์ผู้ให้บริการ")
            else:
                print("Error getting provider profile:", response.text)

        except Exception as e:
            print(f"Error getting provider profile: {str(e)}")

    def start_main_form(self):
        """Close the login form and start the main application form."""
        print("Attempting to start MainForm...")

        # Import Main here to avoid circular imports
        from Main import Main

        # Create Main instance with  hash_cid passed at constructor
        self.main_window = Main(hash_cid=self.hash_cid)
        # Show main window
        self.main_window.show()

        # Close the login window
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Hospital Management System")
    window = Login()
    window.show()
    sys.exit(app.exec())
