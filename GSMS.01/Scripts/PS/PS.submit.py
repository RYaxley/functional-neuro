#!/usr/bin/env python

import sys, os, re, time, datetime

# USER SECTION ##############################################################

# Define user specific constants
username        = os.getlogin() # Cluster username
experiment      = "GSMS.01" # Experiment name for qsub
template_f      = file("PS.submit.sh") # Job template (on head node)
fsf_template    = "PS.fsf"
output_dir      = "PS/5disdaqs"
runs = range(1,10) # range cuts the last number off

f = file(os.path.join(os.path.expanduser('~'), experiment, 'Scripts/Subjects/subjects.py'))
exec(f)
f.close()
subjects = dict(subjects)


#############################################################################    
max_run_time = 60
nodes = 350
sleep_time = 1
maintain_n_jobs = 100
#############################################################################

#build allowed timedelta
kill_time_limit = datetime.timedelta(minutes=max_run_time)

def _check_jobs(username, kill_time_limit):
    #set number of jobs to maintain based on time of day.
    time = datetime.datetime.now()
    if (time.weekday > 4) | (time.hour < 8) | (time.hour > 17):
        n_other_jobs = 0
    else: #its a weekday, fake an extra 6 jobs to leave 5 nodes open
        n_other_jobs = maintain_n_jobs * .25
    
    n_jobs = 0
    status = os.popen("qstat")
    status_list = status.readlines()
    for line in status_list:
        if (line.find(" r ") > -1):
             running = 1
        elif (line.find(" qw ") > -1):   #all following jobs are in queue not running
             running = 0
    
        #if job is mine
        if (line.find(username) > 0) & (line.find("interact.q") < 0):   #name is in the line, not including first spot
           n_jobs = n_jobs + 1
           if running == 1:   #if active job, check how long its been running and delete it if too long
              job_info = line.split()  #get job information
              start_date = job_info[5].split("/")  #split job start date
              start_time = job_info[6].split(":")  #split time from hours:minutes:seconds format
              started = datetime.datetime(int(start_date[2]), int(start_date[0]), int(start_date[1]),
                                          int(start_time[0]), int(start_time[1]), int(start_time[2]))
              if ((time - started) > kill_time_limit) & (line.find("stalled") == -1):   #if the active job is over max run time, delete it
                 os.system("qdel %s" % (job_info[0]))   #delete the runaway job
                 print("Job %s was deleted because it ran for more than the maximum time." % (job_info[0]))
        
        # if line starts " ###" and isnt an interactive job
        elif bool(re.match( "^\d+", line )) & (line.find("interact") < 0) & (line.find("(Error)") < 0):
            n_other_jobs = n_other_jobs + 1
    return n_jobs, n_other_jobs


#make a directory to write job files to and store the start directory
start_dir = os.getcwd()
tmp_dir = str(os.getpid())
os.mkdir(tmp_dir)

#read in template
template = template_f.read()
template_f.close()
os.chdir(tmp_dir)

#############################################################################

for s, info in sorted(subjects.iteritems(), reverse=True):

   for run in runs:  # Loop through each "run"

      subject = str(s)
      group = str(info[0])

      if run < 9:
          volumes = str(info[1])
      elif run == 9:
          volumes = str(info[2])

      tmp_job = template.replace( "_run_", str(run).zfill(2) )
      tmp_job = tmp_job.replace( "_subject_", subject )
      tmp_job = tmp_job.replace( "_group_", group )
      tmp_job = tmp_job.replace( "_volumes_", volumes )
      tmp_job = tmp_job.replace( "_template_", fsf_template )
      tmp_job = tmp_job.replace( "_outputdir_", output_dir )

      # Make filename and write job file to cwd
      tmp_fid = "_".join( [ "PS", subject, str(run) ])
      tmp_fid = ".".join( [ tmp_fid, 'job' ])
      tmp_job_f = file( tmp_fid, "w" )
      tmp_job_f.write(tmp_job)
      tmp_job_f.close()
      
#############################################################################           

      #wait to submit the job until we have fewer than maintain in q
      n_jobs = maintain_n_jobs
      while n_jobs >= maintain_n_jobs:
         #count jobs, delete jobs that are too old
         n_jobs, n_other_jobs = _check_jobs(username, kill_time_limit)
      
         #adjust job submission by how may jobs are submitted
         #set to minimum number if all nodes are occupied
         #should still try to leave # open on weekdays
         if ((n_other_jobs + n_jobs) > (nodes+1)):
            n_jobs = n_jobs + maintain_n_jobs - min_jobs
         if n_jobs >= maintain_n_jobs:
            time.sleep(sleep_time)
         elif n_jobs < maintain_n_jobs:
            cmd = "qsub -v EXPERIMENT=%s %s"  % (experiment, tmp_fid)
            dummy, f = os.popen2(cmd)

#############################################################################
# Wait for jobs to complete or delete them if they run too long
n_jobs = 1
while n_jobs > 0:
   n_jobs, n_other_jobs = _check_jobs(username, kill_time_limit)
   time.sleep(sleep_time)

#remove tmp job files move to start dir and delete tmpdir
#terminated jobs will prevent this from executing
#you will then have to clean up a "#####" directory with
# ".job" files written in it.
cmd = "rm tmp_fid"
os.system(cmd)
os.chdir(start_dir)
os.rmdir(tmp_dir)