====== GSMS.01 Guide ======


===== Locations =====

     - Documentation: [[http://shadow.biac.duke.edu/wiki/doku.php/huettel:gsms.01]]     
     - Syntax: [[http://www.dokuwiki.org/syntax]]
     - Raw data: [[//munin/data/debellis/GSMS.01/Data]]
     - Nifti-converted data: [[//munin/data/debellis/GSMS.01/Analysis/Images]]
     - Prestats: [[//munin/data/debellis/GSMS.01/Analysis/PS]]
     - EV (behavioral) files: [[//munin/data/debellis/GSMS.01/Analysis/EV]]


===== Subject Info =====

- Scan Log: [[/Users/richardyaxley/GSMS.01/Documents/GSMS.01.ScanLog.xls]]

- GSMS Administration: [[https://devepi.duhs.duke.edu/gsms/]]

- Contact Tim Blitchington [[mailto:timothy.blitchington@duke.edu]] or Jürgen Henn [[mailto:jurgen.henn@duke.edu]] to gain access to the tracking system.



===== Groups =====

**(Ss with usable behavioral data as of October 21, 2010)**

- SUD and psychiatric disorder (N=28)

- SUD with no psychiatric disorder (N=16)

- Psychiatric disorder with no SUD (N=18)

- No SUD or psychiatric disorder (N=24)



===== Experiment Protocol =====

==== Prescan ====
 
   * Navigate to Mock Scanner (Room #?)
   * Have participant complete BIAC safety questionnaire
   * Meet participant and give brief description about the planned events
   * Have participant read printed instructions on Loss Aversion & Temporal 
   * Review instructions with participant orally
   * Walk through both tasks on computer
   * Give participant $20 endowment for the LA task. Place money in envelope for safe-keeping.
   * Leave time for restroom break.

==== Scan ====
   * Navigate to 3T Scanner (Room #)
   * Have the participant select a movie to view during anatomicals
   * Hand over participant to MR Tech
   * 

==== Scan Parameters ====

Scanning will be performed on the Duke University BIAC’s 3T scanner system. We will use an EPI sequence for functional imaging with 34 axial slices for full-brain coverage (3.75 mm x 3.75 mm x 3.8 mm voxel size) and a 2-second TR. We will also collect high resolution structural MR images and Diffusion Tensor Imaging data (b=1000 s/mm^2).
 
=== Computers ===
   * Login to both computers in corner
   * Right computer controls what the subject sees on the projector/goggles
   * Launch video controller application
   * Select checkboxes in R3C1 & R4C1 to display task; R3C3 & R4C3 to display movie
   * Left computer controls stimulus presentation

== Setup tasks ==
   * Launch MATLAB
   * Navigate to GSMS.01: $ cd D:/Tasks/GSMS.01/Stimuli
   * Enable Psychtoolbox3: $ addPTB3
   * Run Task #1: Temporal Discounting Task
   * $ cd TD
   * $ TD_task('12345',1')  # 5-digit subject ID; run #
   * Once instruction screen appears, hand keyboard to MR tech who will press the spacebar to start task
   * Iterate through all 4 runs of task
   * Run Task #2: Loss Aversion Task
   * $ cd ../LA
   * $ LA_Task('12345',1) # 5-digit subject ID; run #
   * Once instruction screen appears, hand keyboard to MR tech who will press the spacebar to start task
   * Iterate through 4 runs of task
   * The 5th and final run is the outcome sequence of the gambles the participant accepted
   * An amount (+40 to -20) of money will be presented on the CLI indicating the payout

== Post scan == 
   * Thank participant again
   * Pay participant
   * Return participant to case worker


===== fMRI Analysis =====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_fsl)|General FSL Analysis Information]]

==== Prepare Data for Analysis ====

=== Generate NIFTI images ===

- Login to Hugin 
          $ ssh Username@hugin.biac.duke.edu

- Navigate to Scripts directory. For example:
          $ cd ~/Scripts

- Run conversion script on Hugin     
          $ qsub -v EXPERIMENT=GSMS.01 make.nifti.sh 00001 00002 &


- This puts NIFTI-converted images here: [[\\munin\data\debellis\GSMS.01\Analysis\Images\Subject#]]


==== Quality Assurance ====

- Login to Hugin 
     $ ssh Username@hugin.biac.duke.edu

- Navigate to Scripts directory. For example:
     $ cd ~/Scripts

- Run QA script on Hugin
     $ qsub -v EXPERIMENT=GSMS.01 qa.sh 00001 00002 &

- The QA script will place QA output here: [[\\munin\data\debellis\GSMS.01\Data\Func\Subject#\QA\index.html]]

=== Quality Assurance Criteria  ===

     - SFNR ( >60 )
     - Motion ( <2mm )
     - per-slice variation (red stripes)
     - Red ringing


==== FSL Prestats ====

- Subject log: 
[[\\munin\data\debellis\GSMS.01\Scripts\Subjects\GSMS.01.ScanLog.xls]]

- Add Subject information to the subject dictionary: [[\\munin\data\debellis\GSMS.01\Scripts\Subjects\subjects.py]]

- Login to Hugin

- On Hugin, navigate to:
     $ cd ~/GSMS.01/Scripts/PS

- Run Prestats
     $ python PS.submit.py
- Run Prestats submission script:  
     $ python PS.submit.py GSMS.01 PS.5disdaqs PS &     

- Functional images: 01.nii.gz, 02.nii.gz, etc.

- Brain-extracted anatomical image for coregistration: 300_brain.nii.gz

- Review Prestats output for motion.


=== Check Data ===

To ensure that analyses were completed successfully, run the following script. You can specify specify the experiment, model, and level (PS, L1, L2, and L3). This script checks for the existence of files that are created
during an FSL analysis. If any files are missing or error messages are found, an error message is displayed.


- Login to Hugin

- Login to Qinteract
     $ qinteract

- Mount experiment
     $ lnexp GSMS.01

- Navigate to Scripts dir
     $ cd ~/Scripts
     
- Run script
     $ python check.data.py GSMS.01 PS.5disdaqs PS
     or
     $ python check.data.py GSMS.01 TD.100423 L1
     

=== Add QA information to GSMS Tracking System ===

GSMS Tracking System: [[https://devepi.duhs.duke.edu/gsms/]]
          

=== EV Files ===

- Navigate to Scripts/
     $ cd ~/Scripts

- Sync the behavioral data to the local machine. 
     $ python sync.behavioral.py GSMS.01

- Navigate to EV directory on local machine:
     $ cd ~/GSMS.01/Scripts/EV

- Run EV script.
     $ python EV.py

- This script extracts the time-course of events that need to be modeled in FSL. This script then creates individual text files for each type of event and saves them in the individual subjects' directories here:                     
     ~/GSMS.01/Analysis/EV/Subject#

- Synchronize scripts:
     $ cd ~/Scripts
     $ python sync.scripts.py


==== Level 1 ====

- Navigate to L1 directory:
     $ cd ~/GSMS.01/Scripts/L1

- Generate .fsf template files. To adjust the model, you must evaluate the L1 script and alter as necessary. 
     $ python L1.write.fsf.py 

- Sync .fsf templates to Munin
     $ cd ~/Scripts
     $ python sync.scripts.py GSMS.01

- Login to Hugin

- Navigate to Scripts:
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py GSMS.01 Model.Version Level Subject &

- For example,
     $ python submit.py GSMS.01 Decision.100423 L1 00001 &



==== Level 2 ====

- Generate .fsf template files. To adjust the model, you must evaluate the L2.write.py script and alter as necessary. 
     $ python ~/GSMS.01/Scripts/L2/L2.write.py

- Sync .fsf templates to Munin
     $ python ~/Scripts/sync.scripts.py GSMS.01
     
- Login to Hugin
     $ ssh yaxley@hugin.biac.duke.edu
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py GSMS.01 Model.Version L2 &

- For example,
     $ python submit.py GSMS.01 Decision.100423 L2 &

- Check data
     : python check.data.py GSMS.01 Model.Version L2 [DELETE]
     Note: 'DELETE' = **option to erase analyses with errors**



==== Level 3 ====

- Generate .fsf template files. To adjust the model, you must evaluate the L3.write.fsf.py script and alter as necessary. For instance, this script controls participant groupings, inclusion of covariates, and any exclusions based on age or other criteria. It is critical to review this script carefully.
     $ python ~/GSMS.01/Scripts/L2/L3.write.fsf.py

- Sync .fsf templates to Munin
     : python ~/Scripts/sync.scripts.py GSMS.01

 - Login to Hugin
     $ ssh yaxley@hugin.biac.duke.edu
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py GSMS.01 Model.Version L3 &

- For example,
     $ python submit.py GSMS.01 Decision.100423 L3 &

- Check data
     : python check.data.py GSMS.01 Model.Version L3 [DELETE]



==== ROI Analysis ====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_roi]]


==== Extracting Peak Voxels ====

We can extract the peak voxel from the L3 cope1.feat/stats/zstat1.nii.gz images.

- Use the command
     cluster --in=cope1.feat/ EEEstats/zstat1 --mm
     
To threshold (e.g., zstat = 4) add:
     cluster --in=cope1.feat/stats/zstat1 --mm --thresh=4



===== Background on tasks =====

This study is one portion of a broad-scale longitudinal study investigating the cohort from the Great Smoky Mountains Study (GSMS) led by Jane Costello,  Adrian Angold, Helen Egger, and Mike DeBellis. This fMRI study, entitled GSMS.01, is the first brain imaging study with this population  (Age x-y years; Gender x% Female). This study is designed to investigate the differential brain-activation patterns that support decision-making processes across the four groups of people that comprise the GSMS population: 1) those with persistent substance abuse disorders, 2) short-term substance abuse, 3) substance abuse and psychiatric disorders, 4) and those without a history of either substance abuse or psychiatric disorders. We will be using fMRI to compare the differential brain activation patterns across these four groups in two financial decision-making tasks.

==== Temporal Discounting Task ====

This study has been designed to investigate the neural regions that support financial decisions involving intertemporal choice. We used fMRI to examine brain activation in subjects making a series of binary choices between sooner, smaller and larger, later monetary rewards.
This task is based on the temporal-discounting study described in [Kable & Glimcher (Nature Neuroscience, 2007)](http://www.nature.com/neuro/journal/v10/n12/abs/nn2007.html).  During each trial participants decided whether to accept a smaller, immediate reward and a larger, delayed reward. For example, a monetary gain of $20 today vs. $40 in one month. Immediate gambles involved a known monetary gain that would be mailed immediately in the form of a check. Delay gambles involved a known monetary gain that would be mailed after some known interval (e.g., $40 in 4 weeks). This manipulation is expected to elicit activation in the ventral striatum,  medial PFC, and posterior cingulate that corresponds to the subjective valuation of delayed monetary amounts.
	
=== Task ===

At the beginning of each trial, a pair of delayed amounts is shown and subjects have up to 4 s to select their preferred option. Their selected option is then highlighted for 0.5 s before the inter-trial interval (jittered between x–y s).

- Each trial includes an 1) Immediate Amount and a 2) Delayed Amount
- Delays: 'Today', '1 Week', '2 Weeks', '4 Weeks', '8 Weeks'
- Amounts: SSR: $10–30; LLR: $30–60

At the end of the experiment one trial is selected at random and participants are paid either the SSR or LLR based on their choice.

=== Questions ===

- Does subjective valuation of monetary rewards at different delays predict brain activation?

- Does group predict delay discounting behavior?



=== fMRI ===

== Using Behavioral Data ==

- Smallest # of variables to predict discounting rates
- Most interesting to find interaction between Psychiatric and SUD groups
- Few predictors of discounting (SES, other covariates?)

== Explanatory Variables ==

1. Simple Model
	- EV1 = Stimulus
	- EV2 = Subjective value of choice (as in Kable & Glimcher)
		- selection of SSR = SSR; LLR = discounted LLR based on subject's discounting rate
		- normalized
		- orthogonalized WRT 1 
	- EV3 = Choice difficulty (as in McClure's easy vs hard)
		- relative difference between subjective value of SSR and LLR
		- orthogonalized WRT 2
	- EV4 = Missed stimulus
	
2. Add to #1
	- Delay amount (parametric?)

=== Group Analysis ===

- First, setup all models with everyone in one group

- Then, Scott and Adrian both suggest using ROIs to investigate the four groups: Control, Psychiatric, SUD only, and SUD+Psychiatric

- Individual impulsivity (discounting of future rewards) predict brain activation

- Covariates from CANTAB, SES, etc.


=== Papers to review ===

- Weber & Huettel
	
- Thaler, 1981
	
- Green et al., 1999
	
- Rachlin et al., 1991
 	
- McClure et al. (2004, 2007) 

- Mitchell, 1999

- Ohmura et al., 2005


=== Notes/Predictions ===

From Kable & Glimcher 2007:
	
- main point: subjective value of potential rewards is explicitly represented in the human brain

-  The subjective value of a $20 gain declines as the imposed delay to its receipt increases, a phenomenon known as temporal discounting ($30–34). This decline in subjective value can differ across individuals—a second person might accept as little as $10 immediately in lieu of $20 in a month. Therefore, the objective amount and delay associated with each gain alone cannot predict choice; an idiosyncratic function that relates delay to subjective value is required.

- Match between "the subjective preferences of our subjects and neural activity in the ventral striatum, medial prefrontal cortex and posterior cingulate cortex."


From McClure et al. 2004:

- Beta-Delta Quasi Hyperbolic Discounting model

	- Beta: Reward regions ("limbic grasshopper")

	- Delta: Executive control regions ("prefrontal ant")

- Easy vs Difficult (closer amounts) decisions

- Our analysis shows that the $ areas, which are activated dis- proportionately when choices involve an opportunity for near-term reward, are associated with limbic and paralimbic cortical structures, known to be rich in dopaminergic innervation. These structures have consistently been implicated in impulsive behavior (37), and drug addiction is commonly thought to involve disturbances of dopaminergic neurotransmission in these systems (38).

- If impatient behavior is driven by limbic activation, it follows that any factor that produces such activation may have effects similar to that of immediacy (10). Thus, for example, heroin addicts temporally discount not only heroin but also money more steeply when they are in a drug-craving state (im- mediately before receiving treatment with an opioid agonist) than when they are not in a drug-craving state (immediately after treat- ment) (39)

- Parts of the limbic system associated with the midbrain do- pamine system, including paralimbic cortex, are preferentially activated by decisions involving immediately available rewards. In contrast, regions of the lateral prefrontal cortex and posterior parietal cortex are engaged uniformly by intertemporal choices irrespective of delay. Furthermore, the relative en- gagement of the two systems is directly associated with subjects’ choices, with greater relative fronto-parietal activity when subjects choose longer term options.


From Weber & Huettel:
	
- "Regions whose activation significantly increased when delay was present included the lateral parietal cortex, the vmPFC, dlPFC, the posterior cingulate and adjacent precuneus.We note that while some of these regions have been associated with evaluation of delayed rewards (Kable and Glimcher, 2007; McClure et al. 2004, 2007), they have also been implicated in task-independent (i.e., default-network) processing (Gusnard and Raichle, 2001; Raichle et al., 2001)"

- "We found that three of these regions also exhibited increased activation to delay trials compared to control trials: the posterior cingulate/precuneus, the caudate, and dlPFC."
	
- "Choices of the later option were predicted by increased dlPFC activation (Table 3); there were no regions whose activation predicted choices of the more-immediate option."


	

==== Loss Aversion Task ====

This task is based on the loss-aversion study described in [Tom, Fox, Trepel & Poldrack (Science, 2007)](http://www.sciencemag.org/cgi/content/abstract/sci;315/5811/515). This task has been designed to investigate the neural regions underlying aversion to monetary losses in financial decisions. Participants will be making a series acceptability judgments on a virtual coin-flip task where they stand a 50% probability of winning or losing a variable amount of money on each trial. This manipulation is intended to elicit activation in regions that have been shown to be activated in response to monetary rewards such as the dorsal and ventral striatum, ventromedial and ventrolateral PFC, and anterior cingulate.

- Participants decided whether to accept or reject balanced mixed gambles (50/50) of gaining one amount or losing another amount.

- In order to allow for separate estimates of neural responses to gains and losses, the sizes of the potential gain and loss were manipulated independently, with gains ranging from $10 to $40 and losses ranging from $5 to $20. These ranges were chosen, because people are on average roughly twice as sensitive to losses as to gains. To introduce incentive-compatible payoffs, we endowed participants with $20 before scanning, and told participants that one decision from the task would be honored for real money; gain or loss.

- Need to assess behavioral sensitivity to gains and losses by fitting a logistic regression to each Ps acceptability judgments collected during scanning, using the size of the gain and loss as independent variables. We can then compute a measure of behavioral loss aversion as the ratio of the absolute loss response to the gain response.

- Analyze imaging data to identify regions whose activation correlated with the size of the potential gain or loss, using parametric regressors. Which regions are responsive to the size of potential gains? losses?
 What is the gain response network? Loss response network?

- Overall positive expected value of the gambles, so we compared activity evoked by the worst possible gambles ($10:16,-$17:-20) and the best gambles ($34:40, -$5:-8). Contrast Best > Worst and Best < Worst.

- 16 X 16 matrix for gamble values. We collapsed to 4 X 4 to simplify analysis. In each cell, calculate probability of acceptance and average response time.

=== Explanatory Variables ===

- EV1 = Stimulus (all stim responded to)

- EV2 = Response (all responses)

- EV3 = Gain magnitude (parametric based on transformed values)

- EV4 = Loss magnitude (parametric based on transformed values)

=== Questions ===

- Individual differences of impulsivity or temporal discounting  
