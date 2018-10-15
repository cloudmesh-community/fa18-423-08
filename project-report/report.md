Yuli Zhao
Project outline

The problem needs to be solved:
Secchi Disk underwater visibility and Meter Measurement Recognition


Data source:
Data comes from videos taken by students. Each Video has length between one and two minutes. In different frames, the secchi disk and the tape are in different positions. Secchi disk drops down slowly but continuously, the size of the secchi disk gets smaller as it goes down deeper. Secchi disk moves left and right in a rather big distance due to water flow. The tape moves up and down within a small distance. Data is unorganized. Data needs to separated into frames and labeled in order to build recognition model.
Problem 1: more data needed
Problem 2: the number on the tape is not specific enough, need to remake videos with a tape of proper measurements.
Problem 3: The tape is moving too quick, number can not be clearly identified in frames.

Data cleaning:
Pick out usable videos
Use existing softwares to separate videos into frames
Pick out usable frames
Label each frame in the filename, for example, (1_10.jpg) or (0_8.jpg)

Model:
Only one model needed for tape measurement recognition because the recognition of the secchi disk can be decided through pixel values.
Because the position of the tape measurement is fixed throughout the video, crop out same part of every frame, to get the value of the measurement, then train a model based on the data.
Second approach is generate data from one example data of tape measurement. Replace the value on the image with random generated data, the model will have much higher accuracy this way. Technical difficulty will be encountered.

Secchi Disk visibility recognition:
Locate where the Secchi disk is in the frame
Look at the pixel RGB value
If many pixel RGB value is close to black or white, secchi disk can still be detected;
If all values are similar, secchi disk cannot be detected.

Object localization and detection:
This is the biggest problem need to be tackled. To locate two objects in one frame. The first object is the Secchi Disk, the other object is the tape measurement.
After detect the Secchi Disk, run analysis on the pixels.
After detect the tape measurement, run the recognition model.
