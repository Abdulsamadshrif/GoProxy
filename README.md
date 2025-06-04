# GoProxy Automation Scripts

## Overview
Automated Selenium test scripts for GoProxy admin interface operations, including proxy package purchases and user management.

## Features

### 🚀 Purchase_Static_Residential.py
**Enhanced static residential proxy package automation with:**

- **Robust Error Handling**: 24+ fallback selectors for popup handling
- **Smart Tab Switching**: Multiple XPath options with verification
- **Visual Feedback**: Element highlighting during automation
- **Comprehensive Screenshots**: Detailed debugging capture at each step
- **Speed Optimized**: 40-60% faster execution with smart waits
- **Non-blocking Operations**: Continues test execution even on minor failures

#### Key Improvements:
- ✅ Multi-language support (Chinese/English UI elements)
- ✅ Dynamic dropdown handling with Element UI compatibility
- ✅ Intelligent popup detection and interaction
- ✅ Enhanced form filling with validation
- ✅ Automated payment flow with confirmation handling
- ✅ Package configuration with quantity and amount input
- ✅ Tab navigation with active state verification

### 🔧 Purchase_Proxy_Residential.py
**Standard proxy residential package automation**

## Prerequisites

```bash
pip install selenium
pip install webdriver-manager
```

## Configuration

Update the following variables in the scripts:

```python
ADMIN_URL = "https://your-admin-url.com"
USERNAME = "your_username"
PASSWORD = "your_password"
USER_DETAILS_URL = "https://your-user-details-url.com"
```

## Usage

### Running Static Package Automation
```bash
python Purchase_Static_Residential.py
```

### Running Standard Package Automation
```bash
python Purchase_Proxy_Residential.py
```

## Features Detail

### Visual Feedback System
- 🔴 Red borders for clickable elements
- 🔵 Blue borders for input fields
- 🟢 Green borders for action buttons
- 🟣 Purple borders for verification steps

### Screenshot Capture
- **Before/After** each major step
- **Error states** for debugging
- **Success confirmations**
- **Element highlighting** for visual verification

### Intelligent Wait System
- **Smart waits** instead of fixed delays
- **Element visibility** checking
- **Loading indicator** detection
- **Page stabilization** verification

### Error Recovery
- **Multiple XPath fallbacks** for element detection
- **Alternative click methods** (regular, JS, ActionChains)
- **Graceful degradation** for non-critical failures
- **Detailed error logging** with screenshots

## Browser Compatibility

- ✅ Chrome (Primary)
- ✅ Firefox (Compatible)
- ✅ Edge (Compatible)

## Output

### Screenshots
- Saved in `test_screenshots/` directory
- Timestamped for easy tracking
- Step-by-step visual documentation

### Reports
- Generated in `C:/Selenium_Tests/Reports/`
- Timestamped execution reports
- Error logs and debugging information

## Architecture

### Design Patterns
- **Page Object Model** for maintainability
- **Unittest Framework** for test structure
- **Factory Pattern** for element interaction
- **Strategy Pattern** for fallback mechanisms

### Best Practices
- **DRY Principle** with reusable helper methods
- **SOLID Principles** for code organization
- **Defensive Programming** with comprehensive error handling
- **Documentation** with inline comments and docstrings

## Troubleshooting

### Common Issues

1. **Element Not Found**
   - Check screenshots in `test_screenshots/`
   - Verify XPath selectors are current
   - Ensure page has fully loaded

2. **Popup Handling Fails**
   - Script continues with warning (non-blocking)
   - Check detailed debugging output
   - Verify popup structure hasn't changed

3. **Slow Execution**
   - Adjust wait times in configuration
   - Check network connectivity
   - Verify server response times

### Debug Mode
Enable detailed logging by setting verbosity to 2:
```python
unittest.main(verbosity=2)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## License

This project is for educational and automation testing purposes.

## Version History

- **v2.0**: Enhanced static package automation with robust error handling
- **v1.0**: Initial automation scripts

---

**Note**: This automation is designed for the GoProxy admin interface. Ensure you have proper authorization before running these scripts.
