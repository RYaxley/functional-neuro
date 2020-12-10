#!/bin/bash
#############################################################################
#   >  qsub -v EXPERIMENT=Dummy.01  script.sh args
#############################################################################
# BEGIN GLOBAL DIRECTIVE ####################################################

#$ -S /bin/sh
#$ -o $HOME/$JOB_NAME.$JOB_ID.out
#$ -e $HOME/$JOB_NAME.$JOB_ID.out   

# END GLOBAL DIRECTIVE ######################################################
#############################################################################
# BEGIN PRE-USER ############################################################

source /etc/biac_sge.sh # moved this from below

# Name of experiment whose data you want to access
EXPERIMENT=${EXPERIMENT:?"Experiment not provided"}
EXPERIMENT=`biacmount $EXPERIMENT`
EXPERIMENT=${EXPERIMENT:?"Returned NULL Experiment"}

# If experiment cannot be mounted exit script.
if [ $EXPERIMENT = "ERROR" ]; then
    exit 32
else
    #Timestamp
    echo "----JOB [$JOB_NAME.$JOB_ID] START [`date`] on HOST [$HOSTNAME]----"

    # Set output directory
    OUTDIR=$EXPERIMENT/Analysis/cluster_logs

# END PRE-USER ##############################################################
#############################################################################
# BEGIN USER SCRIPT #########################################################

# Specify FSL 4.1
# FSLDIR=/usr/local/fsl-4.1.4-centos4_64
# export FSLDIR
# source $FSLDIR/etc/fslconf/fsl.sh

GROUP=_group_
SUBJECT=_subject_
RUN=_run_
FSF_TEMPLATE=_template_
#############################################################################
ANALYSIS=$EXPERIMENT/Analysis
SCRIPTS=$EXPERIMENT/Scripts
PRESTATS=$ANALYSIS/_outputdir_
SUBDIR=$PRESTATS/$SUBJECT
    mkdir -p $SUBDIR
TEMPLATE=$SCRIPTS/PS/${FSF_TEMPLATE}
DATA=$EXPERIMENT/Analysis/Images
HIRES=$DATA/MNI152_T1_2mm_brain
# ANATOMICAL1=$DATA/$SUBJECT/300_brain.nii.gz
ANATOMICAL2=$DATA/$SUBJECT/400_brain.nii.gz
FUNCTIONAL=$DATA/$SUBJECT/$RUN.nii.gz
#############################################################################
SMOOTH=5
case $GROUP in
    '4' ) # Adults Exp.1
        VOLUMES=410
        # DISDAQS=8 # already deleted 8 in Melodic
        DISDAQS=4
        REPTIME=1.5
        ANATOMICAL1=$DATA/$SUBJECT/002_brain.nii.gz
        ;;
    '5' ) # Adults Exp.2
        VOLUMES=410
        # DISDAQS=4 # already deleted 4 at scanner & 4 in Melodic
        DISDAQS=4
        REPTIME=1.5
        ANATOMICAL1=$DATA/$SUBJECT/002_brain.nii.gz
        ;;
    '1' ) # Controls Adolescents
        VOLUMES=180
        DISDAQS=4
        REPTIME=2
        ANATOMICAL1=$DATA/$SUBJECT/300_brain.nii.gz
        # ANATOMICAL1=$DATA/$SUBJECT/003_brain.nii.gz
        ;;
    '2' ) # Hirisk Adolescents
        VOLUMES=180
        DISDAQS=4
        REPTIME=2
        ANATOMICAL1=$DATA/$SUBJECT/300_brain.nii.gz
        ;;
    '3' ) # Cannabis Adolescents
        VOLUMES=180
        DISDAQS=4
        REPTIME=2
        # ANATOMICAL1=$DATA/$SUBJECT/300_brain.nii.gz
        ANATOMICAL1=$DATA/$SUBJECT/003_brain.nii.gz
        ;;
esac
#############################################################################
LOG=$PRESTATS/log.txt
echo `date` > $LOG
echo $TEMPLATE >> $LOG
echo $HIRES >> $LOG

if [ -f $FUNCTIONAL ]; then # If Run data exist...

    if [[ ! -d ${SUBDIR}/$RUN.feat ]]; then

        OUTPUT=$SUBDIR/$RUN
        DESIGN=$SUBDIR/$RUN.fsf

        # Generate .fsf file from template
        sed -e 's:OUTPUT:'$OUTPUT':g' \
            -e 's:ANATOMICAL:'$ANATOMICAL1':g' \
            -e 's:FUNCTIONAL:'$FUNCTIONAL':g' \
            -e 's:VOLUMES:'$VOLUMES':g' \
            -e 's:DISDAQS:'$DISDAQS':g' \
            -e 's:REPTIME:'$REPTIME':g' \
            -e 's:SMOOTH:'$SMOOTH':g' \
            -e 's:/usr/local/fsl/data/standard/MNI152_T1_2mm_brain:'$HIRES':g' \
            $TEMPLATE > $DESIGN

        # Run FEAT
        $FSLDIR/bin/feat $DESIGN

        # Cleanup unnecessary files
        rm -f  $DESIGN

    fi

fi
# END USER SCRIPT ###########################################################
#############################################################################
# BEGIN POST-USER ###########################################################
    echo "----JOB [$JOB_NAME.$JOB_ID] STOP [`date`]----"
    OUTDIR=${OUTDIR:-$EXPERIMENT/Analysis} # Output directory
    mv $HOME/$JOB_NAME.$JOB_ID.out $OUTDIR/$JOB_NAME.$JOB_ID.out
    RETURNCODE=${RETURNCODE:-0}
    exit $RETURNCODE
fi
# END POST-USER #############################################################