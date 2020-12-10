 function roi2bxh(region)

fid = strcat(region,'.roi');
roi = load(fid,'-MAT');
mask = roi2mask(roi.roi);
mrstruct = createmrstruct(mask);

fid = strcat(region,'.bxh');
writemr(mrstruct,fid,'BXH','OVERWRITE')

end 