"""
Script to create a custom application icon for the Finding Data theme.
Creates a magnifying glass with data symbols inside.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QBrush
from PyQt6.QtCore import Qt
import sys

def create_finding_data_icon(size=64):
    """Create a custom icon representing 'Finding Data' theme"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Colors for a professional healthcare theme
    primary_color = QColor("#2c3e50")    # Dark blue-gray
    accent_color = QColor("#3498db")     # Medical blue
    data_color = QColor("#27ae60")       # Data green
    highlight_color = QColor("#e74c3c")  # Important red
    
    # Calculate proportions
    center_x = size // 2
    center_y = size // 2
    glass_radius = int(size * 0.35)
    handle_length = int(size * 0.25)
    handle_width = max(2, size // 16)
    
    # Draw magnifying glass circle with gradient effect
    painter.setPen(QPen(primary_color, max(2, size // 20)))
    painter.setBrush(QBrush(QColor(255, 255, 255, 200)))  # Semi-transparent white
    glass_x = center_x - glass_radius // 2
    glass_y = center_y - glass_radius // 2
    painter.drawEllipse(glass_x, glass_y, glass_radius, glass_radius)
    
    # Draw handle with rounded end
    painter.setPen(QPen(primary_color, handle_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    handle_start_x = glass_x + int(glass_radius * 0.7)
    handle_start_y = glass_y + int(glass_radius * 0.7)
    handle_end_x = handle_start_x + handle_length
    handle_end_y = handle_start_y + handle_length
    painter.drawLine(handle_start_x, handle_start_y, handle_end_x, handle_end_y)
    
    # Draw data visualization inside the glass
    inner_radius = int(glass_radius * 0.6)
    inner_x = glass_x + (glass_radius - inner_radius) // 2
    inner_y = glass_y + (glass_radius - inner_radius) // 2
    
    # Draw mini bar chart
    painter.setPen(QPen(data_color, 1))
    painter.setBrush(QBrush(data_color))
    
    bar_width = max(1, inner_radius // 8)
    bar_spacing = max(1, bar_width + 1)
    chart_heights = [0.3, 0.7, 0.5, 0.9, 0.4]  # Relative heights
    
    for i, height in enumerate(chart_heights):
        if i * bar_spacing >= inner_radius * 0.8:
            break
        bar_height = int(inner_radius * height * 0.6)
        bar_x = inner_x + int(inner_radius * 0.1) + i * bar_spacing
        bar_y = inner_y + inner_radius - int(inner_radius * 0.1) - bar_height
        painter.drawRect(bar_x, bar_y, bar_width, bar_height)
    
    # Add a small data point/dot
    painter.setPen(QPen(highlight_color, 1))
    painter.setBrush(QBrush(highlight_color))
    dot_size = max(2, size // 20)
    dot_x = inner_x + int(inner_radius * 0.7)
    dot_y = inner_y + int(inner_radius * 0.3)
    painter.drawEllipse(dot_x, dot_y, dot_size, dot_size)
    
    # Add small text "DATA" if size is large enough
    if size >= 48:
        font = QFont("Arial", max(6, size // 12))
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(accent_color)
        
        # Position text below the magnifying glass
        text_y = glass_y + glass_radius + int(size * 0.15)
        text_rect = painter.fontMetrics().boundingRect("DATA")
        text_x = center_x - text_rect.width() // 2
        painter.drawText(text_x, text_y, "DATA")
    
    painter.end()
    return pixmap

def main():
    app = QApplication(sys.argv)
    
    # Create icons in different sizes
    sizes = [16, 24, 32, 48, 64, 128]
    
    for size in sizes:
        icon_pixmap = create_finding_data_icon(size)
        icon_pixmap.save(f"finding_data_icon_{size}.png")
        print(f"Created finding_data_icon_{size}.png")
    
    # Create a default icon (32x32)
    default_icon = create_finding_data_icon(32)
    default_icon.save("app_icon.png")
    print("Created app_icon.png")
    
    app.quit()

if __name__ == "__main__":
    main()
