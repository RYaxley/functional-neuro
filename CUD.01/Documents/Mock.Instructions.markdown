# CUD.01 Scan Protocol

**Draft Date: November 13, 2010**

This is a draft of the tasks necessary to train participants at the Brightleaf mock scanner. The process described here is similar, but not the same as the training process used at Duke hospital. This process is new and will be refined over the coming days, weeks, and months. Please provide feedback if any information seems to be unclear or missing.

* * *

## Mock Scanner @ Brightleaf

This will be the first opportunity to train participants in our risky decision-making task. At Brightleaf we don't have the same time restrictions that we have at the hospital making this initial training opportunity ideal for taking as much time as necessary to ensure that our participants understand how to perform the task and to remain still in the scanner.

### Computers 

To login you will need to use your **DHE\Username** and password.

The left screen controls MATLAB and MoTrak.

## Experiment: Risky decision-making task

### Experiment Presentation

We are using a programming environment named MATLAB to present the risky decision-making task. We also use a toolbox, or library of code, called Psychtoolbox that enables us to present the images on the screen and record subject's responses. 

#### MATLAB Setup

The `startup.m` file automatically loads settings, add paths, etc. when MATLAB
is started. The file needs to be created and placed in the
`C:\\Username\My Documents\` directory.

##### Brightleaf 

- Launch MATLAB 
- Navigate to `My Documents\` 
- Create new MATLAB script entitled `startup.m`
- Add these lines to startup.m 
	- `addpath(genpath('C:\Psychtoolbox-2'))` 
	- `cd C:\Tasks` 
- Save file.

##### BIAC 

- Launch MATLAB 
- Navigate to `My Documents\` 
- Create new MATLAB script entitled `startup.m`
- Add these lines to startup.m 
	- `addpath(genpath('\\Munin\Programs\MATLAB\Psychtoolbox\2.54'))` 
	- `addpath(genpath('\\Munin\DeBellis\CUD.01\Stimuli'))`
	- `addpath(genpath('\\Munin\DeBellis\CUD.01\Stimuli'))`
	- `cd \\Munin\DeBellis` 
- Save file.

#### Run Experiment

- Set screen resolution to 800x600. 
- Launch MATLAB
- Navigate to the CUD.01 Task directory.

	>> cd ~/CUD.01/Stimuli/

- Type the name of the experiment script.

	>> run_CUD.01_brightleaf
	
- Add arguments in parentheses to specify Subject ID#, Run #, input device (0 = arrow keys on keyboard; 1 = 1 & 2 keys on keyboard and button box).

	run_CUD.01_brightleaf('SubjectID#', Run#, InputDevice)
    
For example,
 
	>> run_CUD.01_brightleaf('99999', 1, 1)

### Task Instructions ###

In each trial the participants will be presented with a shape (star, square, circle, trapezoid, or triangle). After seeing the response prompt (?), the participant will respond with their index or middle finger in order to win money. After each response, the participant will receive feedback that they won ($$) or not (X).

The probabilities are as follows: 

* No Risk: Star or Square 100% payout of $0.15
* Reward Risk: Circle or Trapezoid 50% payout of $0.15 
* Behavioral Risk: Triangle 50%/50%

### Practice Task 

Have subject read experiment instructions and briefly explain the task. Please remind them to answer immediately once the question mark appears. Let them do a practice run in the whisper room and make sure they are winning!
	
#### Duration

Each session of the the task is 6 m. For the real scan, we will run through 6 sessions of the task. Thus, our participants will perform the task for a total of 36 m. However, for the purposes of training, we will only perform the task as long as necessary to ensure satisfactory understanding and performance of the task.

### Head Tracking

The purpose of the head tracker is to measure the magnitude of the participant's head motion. It is of utmost importance that participants remain still at the scanner. Recording images of the brain over time require that all of the images line up. If the head moves, our brain images move, and we cannot identify with confidence the brain activation we are looking for. Remember that our results are only as good as our data.

- Toggle Mock to 'ON'. 
- Toggle Flock of Birds to 'Fly'. 
- Put participant in bore.
- Put motion sensor on 
- Put head coil on 
- Adjust mirror so they can see the screen.
- Press 'Table' button to slide the table into the bore. 
- Launch MoTrak 
	- `Tools > Run`
	- `Tools > Zero Crosshairs` 
- Change scale to ~1 mm


## Scheduling Scan on BIAC Calendar

The first step in analyzing data is to get the data. So, once a participant has completed Part I, someone should inform you that said participant is approved for Part II, tell you what group they are in, and their contact information.

Use the online calendar to schedule them. To open the calendar, go to [BIAC](http://www.biac.duke.edu "BIAC") and then click on [Scheduling Calendar](https://www.biac.duke.edu/calendar/]). To login in you will type your BIAC_Username and your BIAC_password.

Blue spaces are scheduled events. Pale yellow spaces are available. But don’t be deceived, there aren’t techs for the entire time shown on the calendar. The scanner is open 9am-9pm Monday-Thursday, 9am-5pm on Friday, and 9am-12pm on Saturday.

Use the drop down menu in the upper left corner to choose the schedule you want to look at: the 3T is the magnet we use, and it is 'BIAC3'. We also use MOCK1 and WSPR1. 'BIAC5' is the other scanner, which you will sometimes have to reserve Null.01 time when there is only one tech working.

To schedule from 9am-5pm, Monday-Thursday, you don’t have to Null anything—-you just select the starting point for your scan on the BIAC3 and a new screen will open where you choose your end time, yourself as the experimenter, and CUD.01 as the experiment. You don’t enter the subject at this point. The scan takes 2 hours but the prep time is about 15-20 minutes depending on how quick the participant and his/her parent are. Given the variation in some participants’ ability to even walk at a normal pace in the hospital, you should have the participant arrive 30 minutes before the time their scan starts. These 30 minutes should be scheduled on the MOCK1 page, and Null.01’d on the WSPR1 page. It is the same as scheduling for BIAC3, except that the experiment on MOCK1 is CUD.51, and Null.01 on the WSPR1.

If you are scheduling on the scanner from 5pm-9pm Monday-Thursday, you will have to use the Null.01 experiment to block out the same time on the BIAC2 because there is only one tech during those hours. You will also have to do this on Fridays and Saturdays.

### Instruction to Parents

**Check with Bobbi about this section.**

You should then send them a letter with dates and directions—you can do this either via email or snail mail, depending on their preference. The total time is 2.5 hours, and you should tell the parent this when scheduling rather than tell that the first half hour is paper work, etc… They are more likely to show up on time if they think the scan actually starts at the time they are told to be there. It’s also worth mentioning that the parent doesn’t have to be there for the scan of subjects 14 years and older. They will need to meet you at the end to sign the payment form and get the money, but they can either drop the kid off and come back, or swing by at the end if the subject drove themselves.

You will also need to either send the parent an email or letter with date, time, directions, etc… These can be found in the following directory

	\\Munin\Debellis\CUD.01\Notes\CUD

Please note that mental health subjects do not get the ‘Subject’ letters—ONLY cannabis kids get the ‘Subject’ letters, everyone else gets the control letters unless for Dominion reasons you are meeting them at Gary’s.


## Prescan Instructions

### Items Needed for Scan

- Payment form and money (CUD.01 doesn’t use BIAC funds money so money must be
collected from Jan at Dr. DeBellis’ office to pay the subject). 
- BIAC Safety form 
- Scan Information and Comment Sheet 
- Instruction sheet for the subject
- Drug screen and paperwork appropriate for the participant's group 
	* Controls: Redi-Cup 
	* Hi-risk and Cannabis abusers: Dominion cup mailed via DHL 
- Latex gloves

### Meeting the Subject

If you are meeting a Control, meet them in the main lobby of Duke North.
However, if it’s a Subject you’ll meet them in the waiting lobby of the Durham
Child Development & Behavioral Health Clinic. To get there, Go out onto Trent
Dr., cross Erwin and keep going on Trent past the John Hope Franklin Center,
you’ll see a two story building with a parking lot surrounded/elevated with
bricks.

### BIAC Safety form

Have subject and/or parents fill out the Safety Form.


## Meeting the Subject

If you are meeting a Control, meet them in the main lobby of Duke North.  However, if it’s a Subject you’ll meet them in the waiting lobby of the Durham Child Development & Behavioral Health Clinic. To get there, Go out onto Trent Dr., cross Erwin and keep going on Trent past the John Hope Franklin Center, you’ll see a two story building with a parking lot surrounded/elevated with bricks.  

## Pre-Scanning Tasks

## Pregnancy Test

Collect urine sample and give this to MRI tech. 

## Drug Screening

* Please note that the following meeting/drug screen instructions are for high risk subjects and healthy controls NOT cannabis subjects—it is only where you meet them and their drug screen that is different.  Everything else is the same. For cannabis subjects, you will do the dominion drug screens and meet them at Gary’s to do so.

### Urine Test
Cannabis abusers will need to urinate in the Dominion cup.  Please see Gary at the Durham Child Development & Behavioral Health Clinic to properly seal the urine and for having it shipped.  

Controls will need to urinate in the Redi-Cup. Have them fill the cup that has a lid and leave it on the sink in one of the bathrooms in the MRI department.  Wearing gloves, open the nicotine test (it’s the skinny rectangle).  Use the little dropper to put three drops of urine in the small sample well.  Wait five minutes and see the package for pos/neg/invalid reading.  Meanwhile, pour the rest of the urine into the bigger sample cup.  Throw the small cup and lid away.  Then open the “Redi-Cup” lid.  Twist it onto the larger cup securely, set it on its lid for 30-45 seconds before turning it right side up.  It should be readable within 5 minutes.  Sometimes the lines are very faint, but there, so make sure not to jump to conclusions. Record the results.  Flush the remaining urine and dispose of all equipment.  Proceed to the mock scanner.


## Experiment Training and Practice at Mock Scanner


### BIAC Safety form

Have subject and/or parents fill out the Safety Form.

### Task Instructions ###


Instructions like those above except for:

You will run this script the same way for training and the actual experiment
by using a "0" as the last argument. Before we specified whether we wanted to
use the joystick ("1") or keyboard ("0"). Now we just use the same keyboard
codes and thus use "0" only.

### Mock Scanner @ Hospital

#### Practice Task

Have subject read experiment instructions and briefly explain the task.  Please remind them to answer immediately once the question mark appears.  Let them do a practice run in the whisper room and make sure they are winning!

First, navigate to the Scripts directory:

	cd \\Munin\DeBellis\CUD.01\Stimuli

For each practice run, type this exactly:

	run_CUD01new_8button('99999', 1, 1)
	
**October 7, 2008:** The code for the experiment has been altered so that the 8-button button-box will work. Participants will use the "1" and "2" keys along the top of the keyboard.

**Note:** You will run this script the same way for training and the actual
experiment by using a "0" as the last argument. Before we specified
whether we wanted to use the button box/joystick ("1") or keyboard ("0"). Now we just use the same key codes for the keyboard and button box and thus use "1" only.

## Mock Scanner

- Login to computer on right.
- Put participant in mock scanner while wearing headband with motion sensor.
- Explain importance of remaining still.
- Track head motion using the 'track' script in MATLAB:

	>> cd D:\Programs\mri_simulator
	>> track
	
- Play scanner sounds on CD player by pressing the Play button. 
- Ask them questions. Make sure they aren't moving their heads when answering. 
- After the mock scanner, explain that they must hold extremely still. Tell them that often in the MRI people don’t jerk their heads around, but they gradually drift, so remind them to be conscious of moving even between runs. 
- ASK SUBJECT IF SHE HAS ANY QUESTIONS OR CONCERNS, and tell her she can ask at any time during the experiment should one arise. Also tell the parents that they can come into the console room, but they do not have to if the subject will be comfortable alone. Guide them to an appropriate waiting area if necessary or they may leave the hospital entirely and pick the child up when the scan is finished, just be sure to establish a meeting area and time.

### Collect Urine Sample

Before taking the subject to the console room, take the participant to the restroom. Inform them that we must collect a urine sample. Have them fill the cup halfway. 

Inform the subject that if the subject has to interrupt the scanning session to use the restroom, valuable data will be lost, so it is important to go before hand if needed. Really emphasize that they should try to go right beforehand because I’ve had subjects not make it through scans despite urinating for the drug screen twenty minutes before the scan.

Take the subject to the 3T console room.

### Urine Test

#### Pregnancy Test

Urine sample needs to be given to the tech who will perform a pregnancy test
before the scan. Do not flush the urine of female control participants.

#### CUD and HR Participants

CUD and HR participants will need to urinate in the Dominion cup. Please see
Gary at the Durham Child Development & Behavioral Health Clinic to properly
seal the urine and for having it shipped.

#### Control Participants

Controls will need to urinate in the Redi-Cup. Have them fill the cup that has
a lid and leave it on the sink in one of the bathrooms in the MRI department.
Wearing gloves, open the nicotine test (it’s the skinny rectangle). Use the
little dropper to put three drops of urine in the small sample well. Wait five
minutes and see the package for pos/neg/invalid reading. Meanwhile, pour the
rest of the urine into the bigger sample cup. Throw the small cup and lid
away. Then open the Redi-Cup lid. Twist it onto the larger cup securely, set
it on its lid for 30-45 seconds before turning it right side up. It should be
readable within 5 minutes. Sometimes the lines are very faint, but there, so
make sure not to jump to conclusions. Record the results. If positive, send
sample to Dominion. If negative result for male participant, flush the
remaining urine and dispose of all equipment. Proceed to the mock scanner.


## Scan

### Scanner Tech

Introduce the participant to Susan, Luke, or Natalie.

Give the tech the BIAC Screening form. They will then provide a BIAC Subject # to use for the task.

### Video Output

The NTI Video Switcher application controls what the subject will see on the projector/goggles. At the beginning and end of the session we want to direct the DVD to the projector/goggles. However, for the task we need to direct the output of the computer to the projector (row 3) and goggles (row 4). To avoid confusion, always move Rows 3 & 4 together.

#### DVD Player

- Use the remote control for Power, Open/Close, etc.
- DVD = Column 3
- To view DVD on right monitor as well, move Row 2 to Column 3.

#### Computer Presentation

- Resolution must be set to 800x600
- Computer = Column 1

#### 

### Run Task

### Check Money

To calculate the participant's total earnings during the task, run:

	>> check_money('Subj#', 1:6)
	
Round up the total amount to the nearest dollar.








