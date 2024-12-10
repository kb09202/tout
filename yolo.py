import cv2
from ultralytics import YOLO

# Charger le modèle YOLOv5
model = YOLO("yolov5s.pt")  # Modèle pré-entraîné

# Ouvrir la webcam (index 0 pour la caméra par défaut)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'accéder à la webcam.")
    exit()

print("Appuyez sur 'q' pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire le flux vidéo.")
        break

    # Appliquer YOLO pour détecter les objets
    results = model(frame)

    # Annoter l'image avec les résultats
    annotated_frame = results[0].plot()

    # Afficher la vidéo dans une fenêtre
    cv2.imshow("Détection d'objets en temps réel", annotated_frame)

    # Vérifier si l'utilisateur appuie sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Fin de la détection.")
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
