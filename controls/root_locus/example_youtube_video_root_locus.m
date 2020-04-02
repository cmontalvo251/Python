clear
clc
close all

G = tf([1],[1,0,0])
C = tf([1],[1,10])
C2 = tf([1,3],[1,10])

rlocus(G)

figure()
rlocus(C*G)

figure()
rlocus(C2*G)