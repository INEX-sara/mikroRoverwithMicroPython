from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# ส่วนการตั้งค่าเบื้องต้น
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
display = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# ส่วนการคำนวณตำแหน่ง (Mathematics)
SCREEN_WIDTH = 128   # ความกว้างจอ
SCREEN_HEIGHT = 64   # ความสูงจอ
text = "Scrolling"   # ข้อความที่จะแสดง
text_width = len(text) * 8 # คำนวณความกว้างข้อความ (ตัวอักษรละ 8 พิกเซล)

y_pos = (SCREEN_HEIGHT // 2) - 4        # หาจุดกึ่งกลางแนวตั้ง
center_x = (SCREEN_WIDTH // 2) - (text_width // 2) # หาจุดกึ่งกลางแนวนอน
right_edge_x = SCREEN_WIDTH - text_width # ตำแหน่งขวาสุดที่ข้อความแสดงได้
left_edge_x = 0                          # ตำแหน่งซ้ายสุด

# แสดงข้อความนิ่งๆ ที่กึ่งกลางก่อน 1 วินาที
display.fill(0)
display.text(text, center_x, y_pos, 1)
display.show()
time.sleep(1)

# --- ส่วนการทำภาพเคลื่อนไหว (Main Loop) ---
while True:
    # เลื่อนจากกึ่งกลาง ไปทางซ้าย (Center -> Left)
    for x in range(center_x, left_edge_x - 1, -1):
        display.fill(0)
        display.text(text, x, y_pos, 1)
        display.show()
        time.sleep(0.01) 

    # เลื่อนจากซ้ายสุด ไปทางขวาสุด (Left -> Right)
    for x in range(left_edge_x, right_edge_x + 1, 1):
        display.fill(0)
        display.text(text, x, y_pos, 1)
        display.show()
        time.sleep(0.01)

    # เลื่อนจากขวาสุด กลับมาที่กึ่งกลาง (Right -> Center)
    for x in range(right_edge_x, center_x - 1, -1):
        display.fill(0)
        display.text(text, x, y_pos, 1)
        display.show()
        time.sleep(0.01)
