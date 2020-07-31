function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

m = length(y);                      % number of training examples
sqrError = 0;                       % squared errors
sumOfErrors = 0;                    % sum of squared errors
for i = [1 : m]                     % compute the total squared errors
    prediction = theta(1) * X(i,1) + theta(2) * X(i,2); % prediction of hypotheis of i-th example
    sqrError = (prediction - y(i)) ^ 2;                 % squared error of the prediciton
    sumOfErrors = sumOfErrors + sqrError;              % sum of squared errors
end;

J = sumOfErrors / (2 * m);          % compute the cost

end
