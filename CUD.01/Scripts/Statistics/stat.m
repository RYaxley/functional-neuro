function [mn, md, sd] = stat(x)

	n = length(x);
	mn = mean(x);
	md = median(x)
	sd = std(x); % sqrt(sum((x-mean).^2/n));  
	
return