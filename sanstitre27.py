# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:55:46 2024

@author: pc
"""

import cv2
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort
import torch
from torchvision.transforms import functional as F

# Initialisation du tracker DeepSORT
tracker = DeepSort(max_age=30, nn_budget=100)

# Exemple de fonction pour simuler des détections (ex: venant de YOLO)
def dummy_detections(frame):
    # Simulation : Une boîte englobante aléatoire sur le cadre
    h, w, _ = frame.shape
    box = [
        np.random.randint(0, w // 2),  # xmin
        np.random.randint(0, h // 2),  # ymin
        np.random.randint(w // 2, w),  # xmax
        np.random.randint(h // 2, h),  # ymax
    ]
    confidence = np.random.uniform(0.6, 1.0)  # Confiance aléatoire
    return [box], [confidence]

# Initialisation de la capture vidéo
video_path = 0  # Mettre 0 pour la caméra en temps réel, ou un chemin pour une vidéo
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo ou la caméra.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fin de la vidéo ou erreur de lecture.")
        break

    # Obtenir des détections fictives (remplacez cette partie avec votre modèle)
    detections, confidences = dummy_detections(frame)

    # Convertir en format numpy array
    detections = np.array(detections, dtype=np.float32)
    confidences = np.array(confidences, dtype=np.float32)

    # Mise à jour du tracker avec les détections
    tracks = tracker.update_tracks(detections, confidences, frame)

    # Afficher les pistes sur l'image
    for track in tracks:
        if not track.is_confirmed():  # Ignorer les pistes non confirmées
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()  # Obtenir les coordonnées de la boîte : [xmin, ymin, xmax, ymax]

        # Dessiner la boîte englobante et l'ID
        x1, y1, x2, y2 = map(int, ltrb)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Afficher la vidéo avec le suivi
    cv2.imshow("Suivi avec DeepSORT", frame)

    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
