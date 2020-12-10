#!/bin/bash
#############################################################################
#   >  qsub -v EXPERIMENT=Dummy.01  make.nifti.sh Subject#
#
# Written by Richard Yaxley
# Updated on April 17, 2009
#
#############################################################################
# BEGIN GLOBAL DIRECTIVE ####################################################

#$ -S /bin/sh
#$ -o $HOME/$JOB_NAME.$JOB_ID.out
#$ -e $HOME/$JOB_NAME.$JOB_ID.out

# END GLOBAL DIRECTIVE ######################################################
#############################################################################
# BEGIN PRE-USER ############################################################

TASK=$EXPERIMENT

source /etc/biac_sge.sh

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

for SUBJ in "$@"; do

    DATA=$EXPERIMENT/Data
    FDATA=$DATA/Func/*$SUBJ
    ADATA=$DATA/Anat/*$SUBJ
    OUTPUT=$EXPERIMENT/Analysis/Images/$SUBJ
    mkdir -p $OUTPUT

    # Set anatomical series # based on experiment;
    case $TASK in
        'CUD.01' )
            SERIES1=300
            SERIES2=003 # just in case the 300 doesn't exist
            SERIES3=400
            SERIES4=004 
            ;;
        'ExecInfo.03' )
            SERIES1=002
            SERIES2=200
            ;;
        'GSMS.01' )
            SERIES1=300 # T1 image - axial
            SERIES2=400 # Coplanar image - oblique axial (AC-PC)
            SERIES3=003
            SERIES4=004
            ;;
    esac

    for SERIES in "$SERIES1" "$SERIES2" "$SERIES3" "$SERIES4"; do

        # Reorient file
        IF=$ADATA/series${SERIES}/series${SERIES}*.bxh
        OF=$OUTPUT/${SERIES}_reorient.bxh

        bxhreorient --orientation=LAS $IF $OF

        # Convert BXH to NIfTI-1
        IF=$OF
        OF=$OUTPUT/${SERIES}_anat

        bxh2analyze --niigz -s -b --overwrite $IF $OF

        # Extract brain
        IF=${OF}.nii.gz
        OF=$OUTPUT/${SERIES}_brain.nii.gz

        bet $IF $OF -f 0.4

    done # Series loop

    # Convert Functional data
    for R in `ls -d $FDATA/run0??_??`; do

        # Set current run number
        RUN=${R:(-2):2}
        SERIES=${R:(-6):3}

        # Reorient functional data
        IF=$FDATA/run${SERIES}_${RUN}/run$SERIES*.bxh
        OF=$OUTPUT/${RUN}_reorient.bxh

        bxhreorient --orientation=LAS $IF $OF

        # Convert functional image to .nifti
        IF=$OF
        OF=$OUTPUT/$RUN

        bxh2analyze --niigz -s -b --overwrite $IF $OF

    done # Run loop

    # Cleanup
    rm -f $OUTPUT/*reorient*

done # Subject loop

# BEGIN POST-USER ###########################################################
    echo "----JOB [$JOB_NAME.$JOB_ID] STOP [`date`]----"
    OUTDIR=${OUTDIR:-$EXPERIMENT/Analysis} # Output directory
    mv $HOME/$JOB_NAME.$JOB_ID.out $OUTDIR/$JOB_NAME.$JOB_ID.out
    RETURNCODE=${RETURNCODE:-0}
    exit $RETURNCODE
fi
# END POST-USER #############################################################