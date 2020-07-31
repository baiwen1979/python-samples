function g = computeGradient(X, y, theta, m, j)
% COMPUTEGRADIENT compute the gradient of linear regression

g = 0;
% Compute the gradient of theta(j)
for i = 1 : m
    prediction = theta(1) * X(i,1) + theta(2) * X(i,2); 
    g = g + (prediction - y(i)) * X(i,j);
end

end