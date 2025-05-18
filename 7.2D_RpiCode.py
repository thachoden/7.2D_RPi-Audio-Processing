import speech_recognition as sr 
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)

led_pins=[17,27,22]
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
def test_microphone():
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Configure the microphone with higher quality settings
    mic = sr.Microphone(
        sample_rate=48000,  # Higher sample rate
        chunk_size=4096,    # Larger chunk size for better quality
    )
    print("\nInitializing microphone...")
    # Suppress ALSA warnings

    with mic as source:
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please be quiet.")
        r.adjust_for_ambient_noise(source, duration=1)
        
        # Configure recognition parameters
        r.energy_threshold = 4000        # Increase sensitivity
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8          # Shorter pause threshold
        r.phrase_threshold = 0.3         # More sensitive phrase detection
        
        print("\nPlease say something...")
        try:
            audio = r.listen(
                source,
                timeout=5,               # 5 second timeout
                phrase_time_limit=10     # Maximum phrase length
            )
            
            print("Processing audio...")
            # Use more accurate language model
            text = r.recognize_google(
                audio,
                language="en-US",        # Specify language
                show_all=False           # Set to True for debugging
            )
            print("You said:", text)
            
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return None
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def turn_on():
    for pin in led_pins:
        GPIO.output(pin, GPIO.HIGH)

def turn_off():
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)

def voice_process():
    try:
        command = test_microphone()

        if command:
            if "turn on" in command:
                turn_on()
            elif "turn off" in command:
                turn_off()
        else: 
            print("Command is not recognized.")
    except Exception as e:
        return None
if __name__ == "__main__":
    try:
        while True:
            voice_process()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()  # Ensure GPIO pins are cleaned up
