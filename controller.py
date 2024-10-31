import RPi.GPIO as GPIO
import time

# Configuration du mode de numérotation des pins (BCM pour le numéro GPIO)
GPIO.setmode(GPIO.BCM)

# Configuration du pin 23 en entrée avec une résistance pull-down
BUTTON_PIN = 23
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Fonction de callback pour détecter l'appui du bouton
def button_callback(channel):
    print("Bouton pressé !")

# Détection de l'appui du bouton avec un événement
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)

try:
    # Boucle infinie pour maintenir le programme en cours
    print("Appuyez sur le bouton (CTRL+C pour quitter)")
    while True:
        time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

except KeyboardInterrupt:
    print("Programme interrompu")

finally:
    # Nettoyage des configurations GPIO
    GPIO.cleanup()
