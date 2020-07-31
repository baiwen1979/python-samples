function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
% GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESCENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters
%   == Method 1 ==
    % compute gradient for theta(1)
    g1 = sum((X * theta - y) .* X(:,1));
    % Print gradient of theta(1)
    fprintf('Gradient of theta(1): %f\n', g1);
    % compute gradient for theta(2)
    g2 = sum((X * theta - y) .* X(:,2));
    % Print gradient of theta(2)
    fprintf('Gradient of theta(2): %f\n', g2);

    % Update theta with gradient
    t1 = theta(1, 1) - (alpha / m) * g1;
    t2 = theta(2, 1) - (alpha / m) * g2;
    theta(1, 1) = t1;
    theta(2, 1) = t2;

%   == Method 2 ==
    % theta = theta - (alpha /m) * (X' * (X * theta - y));

    % Save the cost J in every iteration
    costJ = computeCost(X, y, theta);
    % Print the cost J
    % fprintf('Cost: %f\n', costJ);
    J_history(iter) = costJ;
end

end
