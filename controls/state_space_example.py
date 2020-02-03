import control as ctl
G = ctl.tf([1,2],[1,3])
print(G)
Gss = ctl.tf2ss(G)
print(Gss)