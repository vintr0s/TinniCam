import cv2
import mediapipe as mp
import threading
import numpy as np
import sounddevice as sd

def get_user_input():
    THRESHOLD_MOVEMENT = float(input("Enter the movement threshold (default: 12): ") or 12)
    INTERVAL = float(input("Enter the interval for auditory stimulation (default: 0, The camera already has delay): ") or 0)
    SOUND_TIME = float(input("Enter the duration of the sound stimulus (default: 0.2): ") or 0.2)
    FREQUENCY_MIN = int(input("Enter the minimum frequency (Hz) for sound (default: 9000): ") or 9000)
    FREQUENCY_MAX = int(input("Enter the maximum frequency (Hz) for sound (default: 12000): ") or 12000)
    RIGHT_EAR = input("Play sound in the right ear? (True/False): ").lower() == 'true'
    LEFT_EAR = input("Play sound in the left ear? (True/False): ").lower() == 'true'
    
    return THRESHOLD_MOVEMENT, INTERVAL, SOUND_TIME, FREQUENCY_MIN, FREQUENCY_MAX, RIGHT_EAR, LEFT_EAR

def generate_white_noise(sample_rate=44100, duration=0.2, freq_min=2000, freq_max=8000, l_channel=True, r_channel=True):
    samples = duration * sample_rate
    noise = np.random.normal(0, 1, int(samples))
    fft_noise = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(int(samples), 1 / sample_rate)
    fft_noise[(freqs < freq_min) | (freqs > freq_max)] = 0
    filtered_noise = np.fft.irfft(fft_noise)
    filtered_noise = filtered_noise / np.max(np.abs(filtered_noise))
    return np.column_stack((filtered_noise if l_channel else np.zeros_like(filtered_noise), filtered_noise if r_channel else np.zeros_like(filtered_noise)))

def generate_auditory_stimulus(sample_rate, sound_time, freq_min, freq_max, left_ear, right_ear):
    activate_inhibition()
    white_noise = generate_white_noise(sample_rate, sound_time, freq_min, freq_max, l_channel=left_ear, r_channel=right_ear)
    sd.play(white_noise, sample_rate)
    sd.wait()
    deactivate_inhibition()

last_stimulus_time = 0
inhibited = False
audio_thread = None

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def detect_head_movement(THRESHOLD_MOVEMENT, INTERVAL, SOUND_TIME, FREQUENCY_MIN, FREQUENCY_MAX, RIGHT_EAR, LEFT_EAR):
    global last_stimulus_time, inhibited, audio_thread
    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        previous_nose_position = None
        previous_chin_position = None
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Could not obtain the camera image.")
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose = face_landmarks.landmark[1]
                    chin = face_landmarks.landmark[199]
                    x_nose, y_nose = int(nose.x * frame.shape[1]), int(nose.y * frame.shape[0])
                    x_chin, y_chin = int(chin.x * frame.shape[1]), int(chin.y * frame.shape[0])
                    current_nose_position = (x_nose, y_nose)
                    current_chin_position = (x_chin, y_chin)
                    if previous_nose_position is not None:
                        nose_movement = distance(current_nose_position, previous_nose_position)
                        chin_movement = distance(current_chin_position, previous_chin_position)
                        if (nose_movement >= THRESHOLD_MOVEMENT or chin_movement >= THRESHOLD_MOVEMENT) and not inhibited:
                            if audio_thread is not None:
                                audio_thread.cancel()
                            audio_thread = threading.Timer(INTERVAL, generate_auditory_stimulus, args=(44100, SOUND_TIME, FREQUENCY_MIN, FREQUENCY_MAX, LEFT_EAR, RIGHT_EAR))
                            audio_thread.start()
                    previous_nose_position = current_nose_position
                    previous_chin_position = current_chin_position
                    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))
            cv2.imshow('Head Movement Detection', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

def deactivate_inhibition():
    global inhibited
    inhibited = False

def activate_inhibition():
    global inhibited
    inhibited = True

if __name__ == "__main__":
    THRESHOLD_MOVEMENT, INTERVAL, SOUND_TIME, FREQUENCY_MIN, FREQUENCY_MAX, RIGHT_EAR, LEFT_EAR = get_user_input()
    detect_head_movement(THRESHOLD_MOVEMENT, INTERVAL, SOUND_TIME, FREQUENCY_MIN, FREQUENCY_MAX, RIGHT_EAR, LEFT_EAR)
