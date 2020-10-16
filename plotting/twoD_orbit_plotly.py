import plotly.graph_objects as go
import numpy as np

# Generate curve data
t = np.linspace(0, 2*np.pi, 1000)
xorbit = np.cos(t)
yorbit = np.sin(t)
xm = np.min(xorbit) - 1.5
xM = np.max(xorbit) + 1.5
ym = np.min(yorbit) - 1.5
yM = np.max(yorbit) + 1.5

skip = int(0.01*len(t))
xanimation = xorbit[0:len(t):skip]
yanimation = yorbit[0:len(t):skip]

args_ = [None, {"frame": {"duration": 0, "redraw": False},"fromcurrent": True, "transition": {"duration": 0,"easing": "quadratic-in-out"}}]
#args_ = [None]

frames_ = []
for k in range(len(xanimation)):
  frames_.append(go.Frame(data=go.Scatter(x=[xanimation[k]],y=[yanimation[k]],mode="markers",marker=dict(color="red", size=10))))

# Create figure
fig = go.Figure(
  data=[go.Scatter(x=xorbit, y=yorbit,mode="lines",line=dict(width=2, color="blue")),go.Scatter(x=xorbit, y=yorbit,mode="lines",line=dict(width=2, color="blue"))],
  layout=go.Layout(xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
  title_text="Circular Orbit", hovermode="closest",
  updatemenus=[dict(type="buttons",buttons=[dict(label="Play",method="animate",args=args_)])]),
  frames=frames_
)


fig.show()