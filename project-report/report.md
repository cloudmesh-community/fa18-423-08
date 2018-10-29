# Secchi Disk Visibility Recognition

Yuli Zhao <br/>
Indiana University<br/>
Bloomington, Indiana<br/>
yulizhao@iu.edu<br/>

## Abstract

Computer vision is designed to imitate human vision. In order to imitate human vision, enabling computer to see is not enough, computer needs to be able to analyze what it sees. What computer sees is essentially frames of images which means nothing to it, but computer is able to analyze the images and extract useful information out following specific instructions from the programmer. Due to the nature of computer, it is able to perform analyzes on a large scale with specific instructions. This paper will discuss how computer vision is used in determining water turbidity through recognizing the secchi disk and extracting measurements as useful information, and how computer vision is applied to a big data set.

## Introductions

Secchi disk is an eight-inch circular disk has alternating black and white color on the surface. It is used to determine the turbidity or the transparency of the water. The way it works is that secchi disk is lowered into the water slowly using a tape that has measurements, and the researcher would record the measurement when the secchi disk is no longer visible. But one single measurement does not offer many information to be useful, useful information can only be extracted by researchers when there are many more measurements. But it would take researcher enormous amount of time to keep in track with each and every measurement. And computer vision is needed here to replace all that workload.
Instead of having researcher record every measurement, a camera can be placed by the measurement that has visual on both the tape measurement and the secchi disk. The process of lowering secchi disk can be repeated in different locations, and each process will return result in the format of a video. And computer will be able to extract the necessary information from the video and mitigate the workload for the researcher. 

## Data Flow

One of the purposes of this project is to create a continuous data flow from the raw video input, to the output of whether if the secchi disk is visible and the measurements of the tape. To maximize efficiency, multiple machines are needed to implement a master/slave architecture. One machine will be the master, the rest of the machines are slaves. The master machine retrieves raw video data and assigns the data to one of the slave machines. Each slave machine is programmed to break down the video into frames and perform analysis on each frame, then return two lists of results with secchi disk visibility and the measurements of the tape. When a slave machine is done with one analysis, it will tell the master machine that it is available, and the master machine will assign another raw video to the slave machine. This cycle will repeat to maximize the efficiency of analyzing the big data.

<img width="866" alt="screen shot 2018-10-28 at 9 30 32 pm" src="https://user-images.githubusercontent.com/43068990/47626088-b00da500-daff-11e8-9c4c-50a47da08207.png">

## Slave Machine

The first step slave machine needs to do is to take apart the raw video into separate frames. The analysis need to be performed on each individual frames. Within each frame, the slave machine needs to run two functions. One function is to correctly identify the position of the secchi disk, and analyze the pixel colors of the position, to determine the visibility of the secchi disk. The other function is to correctly identify the position of the tape measurement, and then run an Optical Character Recognition (OCR) on the position that reads the number of measurement. The slave machine will return a list of pair data matching each frame. At last, the slave machine will let the master machine know that it has finished all its work and available to work on the next one.

:o: use real table an d not image

<img width="444" alt="screen shot 2018-10-28 at 10 21 55 pm" src="https://user-images.githubusercontent.com/43068990/47626128-efd48c80-daff-11e8-9ae1-36a69a84b59a.png">
