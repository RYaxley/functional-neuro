function [result] = se(x) 
	
	result = nanstd(x)/sqrt(sum(~isnan(x)));

return