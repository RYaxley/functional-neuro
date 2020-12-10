function [Y,M]=demean(X)
%DEMEAN - Remove mean from columns of matrix
% DEMEAN(X) removes the column mean from each column of matrix X.
%
% [Y,Z]=DEMEAN(X) returns the normalized matrix in Y and the 
% means of the columns of the matrix X in Z.

% Demean data matrix X
M=mean(X);
Y=X-ones(size(X(:,1)))*M;
if nargout==1,M=[];,end