% MSMP christmas challenge
% Nadine Feldmann emt.upb.de

% plot MATLAB logo
%(see MATLAB documentation 
% https://de.mathworks.com/help/matlab/examples/creating-the-matlab-logo.html)
% with minor changes
L = 160*membrane(1, 100);
map = [1, 0, 0];
f = figure('Name', 'Nikolausmuetze');
ax=axes;

s = surface(L);
s.EdgeColor='none';
view(3)
colormap(map)

ax.XLim = [1 201];
ax.YLim = [1 201];
ax.ZLim = [-53.4 250];

ax.Position = [0 0 1 1];
ax.DataAspectRatio = [1 1 .9];

l1 = light;
l1.Position = [160 400 80];
l1.Style = 'local';
l1.Color = [1, 1, 1];
 
l2 = light;
l2.Position = [.5 -1 .4];
l2.Color = [1, 1, 1];

s.FaceColor = [1, 0, 0];

s.FaceLighting = 'gouraud';
s.AmbientStrength = 0.3;
s.DiffuseStrength = 0.6; 
s.BackFaceLighting = 'lit';

s.SpecularStrength = 1;
s.SpecularColorReflectance = 1;
s.SpecularExponent = 7;

axis off
f.Color = 'black';

% Find max of logo and define/plot sphere
[p, m]  = max(L(:));
[m1, m2] = ind2sub(size(L), m);
[X, Y, Z] = sphere(150);
hold on

sigma = 0.01;
r = 30;
s = surf((X+sigma*randn(size(X)))*r + m2, ... 
         (Y+sigma*randn(size(Y)))*r + m1, ...
         (Z+sigma*randn(size(Z)))*r+p+22)
colormap([1, 1, 1])
s.EdgeColor='none';
view(3)
