====== CUD.01 Guide ======


===== Locations =====

     - Documentation: [[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01]]     
     - Syntax: [[http://www.dokuwiki.org/syntax]]
     - Raw data: [[//munin/data/debellis/CUD.01/Data]]
     - Nifti-converted data: [[//munin/data/debellis/CUD.01/Analysis/Images]]
     - Prestats: [[//munin/data/debellis/CUD.01/Analysis/PS]]
     - EV (behavioral) files: [[//munin/data/debellis/CUD.01/Analysis/EV]]
     - Decision Model: [[//munin/data/debellis/CUD.01/Analysis/Decision/100423]]
     - Outcome Model: [[//munin/data/debellis/CUD.01/Analysis/Outcome/100708]]


===== Script Directories =====

- Need to place scripts in home directory on Hugin 
- Copy Scripts/ to ~/Scripts/ 
- Copy CUD.01/Scripts/ to ~/CUD.01/Scripts/




===== Prescan =====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_protocolinstructions]]


===== Scan =====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_experimenterinstructions]]



===== Analysis =====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_fsl)|FSL Analysis]]



==== Prestats ====

=== Generate NIFTI images ===

- Login to Hugin 
          $ ssh Username@hugin.biac.duke.edu

- Navigate to Scripts directory. For example:
          $ cd ~/Scripts

- Run conversion script on Hugin     
          $ qsub -v EXPERIMENT=CUD.01 make.nifti.sh 00001 00002 &


- This puts NIFTI-converted images here: [[\\munin\data\debellis\CUD.01\Analysis\Images\Subject#]]

- Functional images: 01.nii.gz, 02.nii.gz, etc.

- Brain-extracted anatomical image for coregistration: 300_brain.nii.gz

=== Quality Assurance ===

- Login to Hugin 
     $ ssh Username@hugin.biac.duke.edu

- Navigate to Scripts directory. For example:
     $ cd ~/Scripts

- Run QA script on Hugin
     $ qsub -v EXPERIMENT=CUD.01 qa.sh 00001 00002 &

- The QA script will place QA output here: [[\\munin\data\debellis\CUD.01\Data\Func\Subject#\QA\index.html]]



=== Quality Assurance Criteria  ===

     - SFNR ( >60 )
     - Motion ( <2mm )
     - per-slice variation (red stripes)
     - Red ringing



=== FSL Prestats ===

- Subject log: 
[[\\munin\data\debellis\CUD.01\Scripts\Subjects\CUD.01.ScanLog.xls]]

- Add Subject information to the subject dictionary: [[\\munin\data\debellis\CUD.01\Scripts\Subjects\subjects.py]]

- Navigate to Scripts directory
     $ cd ~/Scripts

- Login to Hugin

- On Hugin, navigate to:
     $ cd ~/CUD.01/Scripts/PS
     
- Run Prestats submission script:  
     $ python PS.submit.py CUD.01 PS.4disdaqs PS &

- Review Prestats output for motion.


=== Check Data ===

To ensure that analyses were completed successfully, run the following script. You can specify specify the experiment, model, and level (PS, L1, L2, and L3).

- Login to Hugin

- Login to Qinteract
     $ qinteract

- Mount experiment
     $ lnexp CUD.01

- Navigate to Scripts dir
     $ cd ~/Scripts
     
- Run script
     $ python check.data.py CUD.01 PS.4disdaqs PS
     or
     $ python check.data.py CUD.01 Decision.100423 L1


=== EV Files ===

- Navigate to Scripts/
     $ cd ~/Scripts

- Sync the behavioral data to the local machine. 
     $ python sync.behavioral.py CUD.01

- Navigate to EV directory on local machine:
     $ cd ~/CUD.01/Scripts/EV

- Run EV script.
     $ python EV.py

- This script extracts the time-course of events that need to be modeled in FSL. This script then creates individual text files for each type of event and saves them in the individual subjects' directories here:                     
     ~/CUD.01/Analysis/EV/Subject#

- Synchronize scripts:
     $ cd ~/Scripts
     $ python sync.scripts.py


===== Level 1 =====

- Navigate to L1 directory:
     $ cd ~/CUD.01/Scripts/L1

- Generate .fsf template files. To adjust the model, you must evaluate the L1 script and alter as necessary. 
     $ python L1.write.fsf.py 

- Sync .fsf templates to Munin
     $ cd ~/Scripts
     $ python sync.scripts.py CUD.01

- Login to Hugin

- Navigate to Scripts:
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py CUD.01 Model.Version Level Subject &

- For example,
     $ python submit.py CUD.01 Decision.100423 L1 00001 &



===== Level 2 =====

- Generate .fsf template files. To adjust the model, you must evaluate the L2.write.py script and alter as necessary. 
     $ python ~/CUD.01/Scripts/L2/L2.write.py

- Sync .fsf templates to Munin
     $ python ~/Scripts/sync.scripts.py CUD.01
     
- Login to Hugin
     $ ssh yaxley@hugin.biac.duke.edu
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py CUD.01 Model.Version L2 &

- For example,
     $ python submit.py CUD.01 Decision.100423 L2 &

- Check data
     : python check.data.py CUD.01 Model.Version L2 [DELETE]
     Note: 'DELETE' = **option to erase analyses with errors**



===== Level 3 =====

- Generate .fsf template files. To adjust the model, you must evaluate the L3.write.fsf.py script and alter as necessary. For instance, this script controls participant groupings, inclusion of covariates, and any exclusions based on age or other criteria. It is critical to review this script carefully.
     $ python ~/CUD.01/Scripts/L2/L3.write.fsf.py

- Sync .fsf templates to Munin
     : python ~/Scripts/sync.scripts.py CUD.01

 - Login to Hugin
     $ ssh yaxley@hugin.biac.duke.edu
     $ cd ~/Scripts

- Submit jobs to cluster
     $ python submit.py CUD.01 Model.Version L3 &

- For example,
     $ python submit.py CUD.01 Decision.100423 L3 &

- Check data
     : python check.data.py CUD.01 Model.Version L3 [DELETE]



===== ROI Analysis =====

[[http://shadow.biac.duke.edu/wiki/doku.php/huettel:cud.01_roi]]


===== Extracting Peak Voxels =====

We can extract the peak voxel from the L3 cope1.feat/stats/zstat1.nii.gz images.

- Use the command
     cluster --in=cope1.feat/ EEEstats/zstat1 --mm
     
To threshold (e.g., zstat = 4) add:
     cluster --in=cope1.feat/stats/zstat1 --mm --thresh=4
