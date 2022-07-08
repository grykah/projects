
import pyautogui
import time

def prevent_lock(button):
    try:
        print ('Press CTRL+C to stop.')
        while True:
            pyautogui.press(button)     # Key pressed
            time.sleep(10)

    except Exception as ex:
        print ('no_lock | Error: ', ex)

def main():
    try:
        print ('\nPrevent Windows screenlock')
        kb_button = str(input('Enter keyboard button: '))
        
        print ('\nRunning')
        prevent_lock(kb_button)

    except KeyboardInterrupt:
        print('\nStopped')

    except Exception as ex:
        print ('main | Error: ', ex)

if __name__ == "__main__":
    main()
