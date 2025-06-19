import sys
from PyQt6.QtWidgets import QApplication

try:
    app = QApplication(sys.argv)
    
    import HisConSetting
    print('✅ HisConSetting imports successfully')
    
    dialog = HisConSetting.HisConSetting()
    print('✅ Dialog creates successfully')
    
    worker = HisConSetting.ConnectionTestWorker({})
    print('✅ Worker creates successfully')
    
    print('🎉 All components working!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
