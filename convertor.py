#!/usr/bin/env python3

import time
import sys

try:
    from smartcard.System import readers
    from smartcard.Exceptions import NoCardException, CardConnectionException
except ImportError:
    print("ERROR: pyscard not installed")
    print("   Run: pip install pyscard")
    sys.exit(1)

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    print("WARNING: pyautogui not installed, will use clipboard only")
    print("   Run: pip install pyautogui")

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False
    print("WARNING: pyperclip not installed")
    print("   Run: pip install pyperclip")



def type_with_pyautogui(text):
    if not HAS_PYAUTOGUI:
        return False
    try:
        pyautogui.write(text, interval=0.01)
        return True
    except Exception as ex:
        print(f"   Type error: {ex}")
        return False


def copy_to_clipboard(text):
    if not HAS_PYPERCLIP:
        return False
    try:
        pyperclip.copy(text)
        return True
    except Exception as ex:
        print(f"   Clipboard error: {ex}")
        return False


def find_reader():
    reader_list = readers()
    
    if not reader_list:
        return None
    
    for r in reader_list:
        if "PICC" in str(r):
            return r
    
    return reader_list[0]


def main():
    print("=" * 55)
    print("  NFC Card Reader - Keyboard Typer Mode (Windows)")
    print("=" * 55)
    print()
    
    reader = find_reader()
    if reader is None:
        print("ERROR: No NFC reader found!")
        print("   Make sure your reader is connected and the PC/SC service is running.")
        sys.exit(1)
    
    print(f"Reader found: {reader}")
    
    if HAS_PYAUTOGUI:
        print("Auto-typing enabled (pyautogui)")
    else:
        print("WARNING: Auto-typing disabled - clipboard only mode")
        print("   Install pyautogui: pip install pyautogui")
    
    print()
    print("Instructions:")
    print("   1. Open the CRL web app in your browser")
    print("   2. Click on the 'UID Carte NFC' field")
    print("   3. Place a card on the reader")
    if HAS_PYAUTOGUI:
        print("   4. The UID will be typed automatically!")
    else:
        print("   4. Press Ctrl+V to paste the UID")
    print()
    print("   Press Ctrl+C to exit")
    print()
    print("-" * 55)
    
    connection = None
    last_paste_time = 0
    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    
    try:
        while True:
            try:
                if connection is None:
                    connection = reader.createConnection()
                    connection.connect()
                
                response, sw1, sw2 = connection.transmit(GET_UID)
                
                if sw1 == 0x90 and sw2 == 0x00:
                    uid = "".join("{:02X}".format(x) for x in response)
                    current_time = time.time()
                    
                    if last_paste_time == 0 or (current_time - last_paste_time) >= 30:
                        print(f"Card detected: {uid}")
                        
                        copy_to_clipboard(uid)
                        
                        if type_with_pyautogui(uid):
                            print(f"   Typed automatically")
                        else:
                            print(f"   Copied to clipboard - press Ctrl+V to paste")
                        
                        last_paste_time = current_time
                
            except NoCardException:
                if last_paste_time != 0:
                    print("   Card removed - ready for next scan")
                    last_paste_time = 0
                try:
                    if connection:
                        connection.disconnect()
                except:
                    pass
                connection = None
                
            except CardConnectionException:
                try:
                    if connection:
                        connection.disconnect()
                except:
                    pass
                connection = None
                time.sleep(0.1)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nExiting...")
        if connection:
            try:
                connection.disconnect()
            except:
                pass


if __name__ == '__main__':
    main()
