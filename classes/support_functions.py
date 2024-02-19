import librosa
import soundfile as sf


def change_pitch_without_affecting_speed(audio_file_path, n_steps):
    # Load the audio file
    y, sr = librosa.load(audio_file_path, sr=None)

    # Pitch shifting
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

    # Save the modified audio
    audio_file_path = audio_file_path[:-4] + "_shifted.mp3"
    sf.write(audio_file_path, y_shifted, sr)
