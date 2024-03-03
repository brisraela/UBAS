# UBAS
Unattended Baggage Alret System


The program utilizes computer vision to identify unattended baggage. It does so in the following steps. First, it captures a frame from a live camera (every 10 milliseconds), then using the yolov8m model it identifies people and suitcases. Finally, the program calculates overlap between each suitcase and person in the frame. If the program finds a suitcase without an owner - it sends an alert.


![צילום מסך 2024-02-29 225931](https://github.com/brisraela/UBAS/assets/93548885/221cd147-4178-4581-93d2-4ca16b37ef16)




Installation:
In order to run the program you will have to download all the files to the same folder 
For your convenience there is a requirements.txt file
(All necessary libraries can be downloaded at once by the command
path pip install -r requirements.txt)


If you would like to use our program in a security camera system, you can either use it as it is or even try modifying it to your needs by using a different detection model.

Attached here are recommended models to use from Roboflow:

https://universe.roboflow.com/singapore-institute-of-technology-4vowg/people_detection-smfuq/model/4
https://universe.roboflow.com/clment-le-padellec/luggage-cuaxr/model/1
https://universe.roboflow.com/school-f9hws/luggage-identifier/model/3
https://universe.roboflow.com/playground-v6gip/person-and-luggage/model/2
https://universe.roboflow.com/uni-ew5jo/peolpe-counting/model/1    


If you'd like to turn the code into an external application (an .exe file), then you may use the attached .ico file to be the icon of the app.

@Tehila Nissim @Bracha Israel
