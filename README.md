# Hospital Management System - PyQt6 Login Application

A professional PyQt6-based login system for hospital management applications with OAuth integration using Thailand's MOPH Health ID and Provider ID services.

## Features

- **Two-Panel Design**: WebEngine OAuth panel and progress/control panel
- **Real OAuth Integration**: Uses official moph.id.th and provider.id.th services
- **Step-by-Step Progress**: Visual feedback for each authentication step
- **Professional UI**: Modern, responsive design with Thai language support
- **Secure Authentication**: OAuth 2.0 flow with proper token handling

## Screenshots

The application features a clean two-panel interface:
- **Panel 1**: WebEngine view for OAuth authentication
- **Panel 2**: Progress display and application launch controls

## Requirements

- Python 3.8+
- PyQt6
- PyQt6-WebEngine
- requests

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mock_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure authentication:**
   ```bash
   cp config_auth_ex.py config_auth.py
   ```
   
   Edit `config_auth.py` with your actual credentials:
   ```python
   AUTH_CONFIG = {
       "HEALTH_CLIENT_ID": "your_health_client_id",
       "HEALTH_CLIENT_SECRET": "your_health_client_secret",
       "PROVIDER_CLIENT_ID": "your_provider_client_id", 
       "PROVIDER_CLIENT_SECRET": "your_provider_client_secret",
       "REDIRECT_URI": "your_redirect_uri"
   }
   ```

## Usage

### Running the Login Application

```bash
python Login.py
```

### Running Individual Modules

```bash
# Main application window
python Main.py

# House management module
python House.py

# About dialog
python About.py
```

## Project Structure

```
mock_app/
├── Login.py              # OAuth login logic
├── Login_ui.py           # Login UI components
├── Main.py              # Main application window
├── Main_ui.py           # Main UI components
├── House.py             # House management module
├── House_ui.py          # House UI components
├── About.py             # About dialog
├── About_ui.py          # About UI components
├── config_auth_ex.py    # Example auth configuration
├── config_auth.py       # Auth configuration (not in git)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Authentication Flow

1. **Step 1**: Authorization Code - User authenticates via MOPH Health ID
2. **Step 2**: Access Token - Exchange auth code for access token
3. **Step 3**: Provider Token - Get provider-specific token
4. **Step 4**: Profile Data - Retrieve user profile and display success

## Configuration

### Authentication Settings

The application requires proper OAuth credentials configured in `config_auth.py`:

- `HEALTH_CLIENT_ID`: Your Health ID client ID
- `HEALTH_CLIENT_SECRET`: Your Health ID client secret  
- `PROVIDER_CLIENT_ID`: Your Provider ID client ID
- `PROVIDER_CLIENT_SECRET`: Your Provider ID client secret
- `REDIRECT_URI`: Your configured redirect URI

### UI Customization

The UI can be customized by modifying the stylesheet properties in the `*_ui.py` files:

- Colors, fonts, and spacing
- Window dimensions and positioning
- Button styles and animations

## Development

### Adding New Modules

1. Create new UI file: `YourModule_ui.py`
2. Create logic file: `YourModule.py`
3. Follow the existing pattern for consistency

### Testing

```bash
# Test individual components
python -c "from Login_ui import Login_ui; print('UI OK')"
python -c "from Login import Login; print('Logic OK')"
```

## Security Notes

- Never commit `config_auth.py` to version control
- Keep OAuth credentials secure
- Use HTTPS for all redirect URIs
- Validate all authentication responses

## Dependencies

- **PyQt6**: Main GUI framework
- **PyQt6-WebEngine**: Web-based OAuth interface
- **requests**: HTTP client for API calls

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions:
- Check the documentation
- Review the example configuration
- Ensure all dependencies are installed correctly

## Changelog

### v1.0.0
- Initial release with OAuth login
- Two-panel UI design
- Step-by-step progress display
- Professional Thai language interface
