function voxelspace = mni2voxel(inputvoxel) %inputvoxel should be [x y z] MNI coordinates

%my assumptions:
%voxel size == 2mm iso
%datasize=(91,109,91)
%mniorigin=[46 64 37] %identified as MNI coordinate [0 0 0] in MRIcron for fsl standard brain

mniorigin=[46 64 37];
yourvoxel=inputvoxel/2;

voxelspace = yourvoxel + mniorigin;