from machine import Pin, PWM  
import time                   

sv_1 = PWM(Pin(18)) # เซอร์โวตัวที่ 1 ต่อขา 18 
sv_2 = PWM(Pin(19)) # เซอร์โวตัวที่ 2 ต่อขา 19 
sv_1.freq(50)       # ตั้งความถี่ 50Hz สำหรับเซอร์โวตัวยก 
sv_2.freq(50)       # ตั้งความถี่ 50Hz สำหรับเซอร์โวตัวคีบ 

sw1 = Pin(8, Pin.IN, Pin.PULL_UP) # ปุ่ม SW1 สำหรับสั่งคีบ 
sw2 = Pin(9, Pin.IN, Pin.PULL_UP) # ปุ่ม SW2 สำหรับสั่งวาง 

# --- กำหนดค่าองศามาตรฐาน *ตำแหน่งอาจต่างกัน จะต้องหาค่าที่เหมาะสมจากตัวอย่าง Listing 7-1, 7-2* ---
sv1Up = 5      # องศาสำหรับยกแขนขึ้น 
sv1Down = 90   # องศาสำหรับลดแขนลง 
sv2Pick = 100  # องศาสำหรับหุบมือคีบ 
sv2Drop = 30   # องศาสำหรับกางมือปล่อย 

# ฟังก์ชันเทียบเคียงค่าเพื่อแปลงองศาเป็นพัลส์หน่วยนาโนวินาที (ns) 
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# ฟังก์ชันสั่งงานเซอร์โวมอเตอร์ตามเลของศาที่ระบุ 
def set_servo_angle(servo_pwm, angle):
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    duty_ns = map_value(angle, 0, 180, 500000, 2500000)
    servo_pwm.duty_ns(int(duty_ns))

# ฟังก์ชันตั้งท่าเริ่มต้น (แขนยกขึ้นและกางมือออก) 
def servoSet():
    set_servo_angle(sv_1, sv1Up)   # ยกแขนขึ้น 
    time.sleep_ms(300)
    set_servo_angle(sv_2, sv2Drop) # กางมือจับออก 
    time.sleep_ms(300)

# ฟังก์ชันขั้นตอนการคีบ (Pick Up): ลง -> คีบ -> ยก 
def PickUp():
    set_servo_angle(sv_1, sv1Down) # ลดแขนลง 
    time.sleep_ms(300)
    set_servo_angle(sv_2, sv2Pick) # หุบมือคีบวัตถุ 
    time.sleep_ms(300)
    set_servo_angle(sv_1, sv1Up)   # ยกแขนขึ้นพร้อมวัตถุ 
    time.sleep_ms(300)

# ฟังก์ชันขั้นตอนการวาง (Drop Down): ลง -> ปล่อย -> ยกแขนเปล่า 
def DropDown():
    set_servo_angle(sv_1, sv1Down) # ลดแขนลง 
    time.sleep_ms(300)
    set_servo_angle(sv_2, sv2Drop) # กางมือปล่อยวัตถุ 
    time.sleep_ms(300)
    set_servo_angle(sv_1, sv1Up)   # ยกแขนเปล่ากลับขึ้นมา 
    time.sleep_ms(300)

servoSet() # เรียกใช้งานท่าเริ่มต้นเมื่อเปิดเครื่อง 

while True:
    sw1_pressed = (sw1.value() == 0) # อ่านสถานะปุ่ม SW1 
    sw2_pressed = (sw2.value() == 0) # อ่านสถานะปุ่ม SW2 
    
    # ถ้ากด SW1 ให้ทำงานตามขั้นตอนการคีบ 
    if sw1_pressed and not sw2_pressed:
        PickUp()
    # ถ้ากด SW2 ให้ทำงานตามขั้นตอนการวาง 
    elif not sw1_pressed and sw2_pressed:
        DropDown()
        
    time.sleep_ms(50) # หน่วงเวลาสั้นๆ เพื่อตรวจสอบปุ่มในรอบถัดไป
