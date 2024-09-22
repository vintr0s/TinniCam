# Tinnitus Treatment System Using Auditory-Somatosensory Stimulation

## Introduction

This system is an **experimental tinnitus treatment** based on the combination of **auditory and somatosensory inputs**. It uses a camera to detect **head movements** (a form of somatosensory input) and triggers an auditory signal that mimics tinnitus. The goal is to leverage the brain's natural plasticity to reduce tinnitus perception. This approach is inspired by scientific evidence but remains experimental, and its efficacy is not guaranteed. Results may vary, and the system could potentially induce a **placebo effect**.

## Scientific Basis

Tinnitus often arises from maladaptive changes in the **dorsal cochlear nucleus (DCN)**, where auditory and somatosensory information is integrated. Studies show that **somatosensory stimuli**—like head or neck movements—can modulate tinnitus by influencing neural circuits in the DCN.

The system takes advantage of **stimulus-timing-dependent plasticity (STDP)**, where the timing between somatosensory (head movement) and auditory stimuli affects neural activity. Research indicates that if somatosensory input precedes auditory input by a few milliseconds, it can reduce the hyperactivity in the DCN linked to tinnitus [^1][^2]. The camera's natural delay of 10 ms aligns with this optimal timing.

## Limitations

Unlike studies that used **direct electrical stimulation** for more precise control, this system relies on natural head movements, which may reduce its efficacy. While based on strong scientific foundations, the system’s effects may not be as reliable or potent. **Placebo effects** could also influence perceived improvements.

## Conclusion

This is an **experimental approach** grounded in scientific research on auditory-somatosensory integration and plasticity. However, its success is not assured, and users should approach it with realistic expectations about its potential benefits or limitations.

---

## Requirements

### Hardware Requirements

- A webcam (for detecting head movements)
- Headphones or earphones (for receiving the auditory feedback)

### Software Requirements

This system is implemented in Python, and the following Python libraries are required:

- `opencv-python` (cv2)
- `mediapipe`
- `threading`
- `numpy`
- `sounddevice`

### Installation

1. Install Python 3.x from the [official website](https://www.python.org/downloads/).

2. Clone the repository or download the code.

3. Install the necessary Python packages. You can install all dependencies via `pip` using the following command:

   ```bash
   pip install opencv-python mediapipe numpy sounddevice
   ```
4. Ensure your webcam is connected and your headphones/earphones are plugged in.

---

## Running the System

1. Once all dependencies are installed, run the main Python script that initializes the webcam and processes head movements to trigger the auditory signal.
   
   ```bash
   python main.py
   ```
2. The system will start detecting head movements through the webcam and deliver an auditory signal based on the detected motion.
---

## References

[^1]: Shore, S. E., et al. (2013). *Stimulus-Timing Dependent Multisensory Plasticity in the Guinea Pig Dorsal Cochlear Nucleus*. PLoS ONE. [Link](https://doi.org/10.1371/journal.pone.0059828).
[^2]: Shore, S. E., et al. (2023). *Reversing Synchronized Brain Circuits Using Targeted Auditory-Somatosensory Stimulation to Treat Phantom Percepts: A Randomized Clinical Trial*. JAMA Network Open. [Link](https://doi.org/10.1001/jamanetworkopen.2023.15914).