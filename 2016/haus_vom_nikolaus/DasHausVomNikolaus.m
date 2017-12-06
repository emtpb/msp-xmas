%% Das Haus vom Nikolaus
% Sergei Olfert
% 2016

close all; clear all; clc

%%
figh = figure(1);
figh.Color = [1 1 1];

%%
x = [0 0 1 0.5 0 1 1 0 1];
y = [0 1 1 1.5 1 0 1 0 0];
satz = {'Das ' 'ist ' 'das ' 'Haus ' 'vom ' 'Ni' 'ko' 'laus'};

%%
lineh = plot(0, 0,'r-','LineWidth',4);
for ii = 2:numel(x)
    lineh.XData = x(1:ii);
    lineh.YData = y(1:ii);
    title(cell2mat(satz(1:ii-1)))
    axis([-0.5 1.5 0 1.8]);
    axis off
    drawnow
    pause(1)
end

