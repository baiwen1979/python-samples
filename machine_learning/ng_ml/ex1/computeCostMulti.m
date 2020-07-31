function J = computeCostMulti(X, y, theta)
%COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
%   J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

m = length(y);                      % number of training examples
predictions = X * theta;            % predictions of hypotheis on all m examples
sqrErrors = (predictions - y)' * (predictions - y); % squared Errors

J = 1 / (2 * m) * sum(sqrErrors);   % compute the cost

end
