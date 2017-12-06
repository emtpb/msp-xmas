%% Weihnachten MSMP
% Hanna Schmiegel, 2016

close all;
clear all;
clc;

%% Frohe Weihnachten

name_str = 'Weihnachten MSMP';
figure('Name',name_str,'NumberTitle','off'); 

% Schnee
s_begin = -200;
s_end = 200;
x_s = s_begin:0.177:s_end;
s = 140*sin(1000*x_s);

plot(x_s, s, 'LineStyle', 'none', 'Marker', '*', 'MarkerEdgeColor', [0.75 1 1]);
hold on;

% Baum
t_t = 0:0.01:100;
tanne = (100-t_t).*asin(sin(t_t));

plot(tanne, t_t, 'color', [0 0.8 0], 'LineWidth', 3);
xlim([-200 200]);
ylim([0 140]);
set(gca, 'dataaspectratio', [5.5,2,1]);
set(gca,'XTickLabel',{});
set(gca,'YTickLabel',{});
xlabel('schön warm hier drinnen');
ylabel('Schnee da draußen');
title('Frohe Weihnachten', 'Color', [0.8 0 0], 'FontSize', 20);
hold on;

% Boden
bodenx = -200:1:200;
bodeny = 3+sin(0.05*bodenx);
plot(bodenx, bodeny, 'color', [0.75 1 1], 'LineWidth', 15);
hold on;

% Stern
sternx = 0;
sterny = 100;
plot(sternx, sterny, 'LineStyle', 'none', 'Marker', 'h', 'MarkerSize', 20, 'MarkerFaceColor', 'y', 'MarkerEdgeColor', [1 0.95 0]);
hold on;

% Lichterkette
% 50
l_beg = -80;
l_end = 82;
x = l_beg:0.01:l_end;
L = 50-5*abs(sin(0.1*x)+sin(0.1*2*x+0.88)+sin(0.1*2*x+0.25));

plot(x, L, 'color', [0 0.3 0], 'LineWidth', 1.5);
hold on;

x_p = l_beg:4:l_end;
L_p = 50-5*abs(sin(0.1*x_p)+sin(0.1*2*x_p+0.88)+sin(0.1*2*x_p+0.25));
plot(x_p, L_p, 'LineStyle', 'none', 'Marker', '*', 'MarkerEdgeColor', [1 0.95 0], 'MarkerSize', 10 );
hold on;

% 25
l_beg = -124.5;
l_end = 121.5;
x = l_beg:0.01:l_end;
L = 25-5*abs(sin(0.1*x)+sin(0.1*2*x+0.88)+sin(0.1*2*x+0.25));

plot(x, L, 'color', [0 0.3 0], 'LineWidth', 1.5);
hold on;

x_p = l_beg:4:l_end;
L_p = 25-5*abs(sin(0.1*x_p)+sin(0.1*2*x_p+0.88)+sin(0.1*2*x_p+0.25));
plot(x_p, L_p, 'LineStyle', 'none', 'Marker', '*', 'MarkerEdgeColor', [1 0.95 0] );
hold on;


% 75
l_beg = -36;
l_end = 39;
x = l_beg:0.01:l_end;
L = 75-5*abs(sin(0.1*x)+sin(0.1*2*x+0.88)+sin(0.1*2*x+0.25));

plot(x, L, 'color', [0 0.3 0], 'LineWidth', 1.5);
hold on;

x_p = l_beg:4:l_end;
L_p = 75-5*abs(sin(0.1*x_p)+sin(0.1*2*x_p+0.88)+sin(0.1*2*x_p+0.25));
plot(x_p, L_p, 'LineStyle', 'none', 'Marker', '*', 'MarkerEdgeColor', [1 0.95 0] );
hold on;

% Schneemann
a=30; 
b=10; 
x0=150; 
y0=10;
t=-pi:0.001:pi;
x=x0+a*cos(t);
y=y0+b*sin(t);
plot(x,y, 'LineWidth', 5, 'Color', [0 1 1])
hold on;

a=25; 
b=8.3; 
x0=150; 
y0=28;
t=-pi:0.001:pi;
x=x0+a*cos(t);
y=y0+b*sin(t);
plot(x,y, 'LineWidth', 5, 'Color', [0 1 1])
hold on;

a=18;
b=6;
x0=150;
y0=42;
t=-pi:0.001:pi;
x=x0+a*cos(t);
y=y0+b*sin(t);
plot(x,y, 'LineWidth', 5, 'Color', [0 1 1])
hold on;

plot(142, 44, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
plot(158, 44, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;

plot(150, 5, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
plot(150, 10, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
plot(150, 15, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
plot(150, 25, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
plot(150, 30, 'Marker', 'o', 'MarkerFaceColor', [0 0 0], 'MarkerEdgeColor', 'none', 'MarkerSize', 5);
hold on;
% Rahmen

rx = -200:1:200;
ry1 = 0:1:140; rx1 = -200*ones(length(ry1), 1);
ry2 = 140 * ones(length(rx), 1);
ry3 = 0:1:140; rx3 = 200*ones(length(ry3), 1);
ry4 = 0 * rx;

plot(rx1, ry1, 'color', [0.2 0.2 0.2], 'LineWidth', 10);
hold on;
plot(rx, ry2, 'color', [0.2 0.2 0.2], 'LineWidth', 10);
hold on;
plot(rx3, ry3, 'color', [0.2 0.2 0.2], 'LineWidth', 10);
hold on;
plot(rx, ry4, 'color', [0.2 0.2 0.2], 'LineWidth', 10);
hold on;

% Lichterkette im Fenster

x = -200:0.01:200;
L = 140-20*abs(sin(0.05*x)+sin(0.05*2*x+2.5)+sin(0.05*2*x+5.8634));

plot(x, L, 'color', [0 0.3 0], 'LineWidth', 2);
hold on;

x_p = -200:8:200;
L_p = 140-20*abs(sin(0.05*x_p)+sin(0.05*2*x_p+2.5)+sin(0.05*2*x_p+5.8634));
plot(x_p, L_p, 'LineStyle', 'none', 'Marker', '*', 'MarkerEdgeColor', [1 0.95 0], 'MarkerSize', 10);
hold on;
