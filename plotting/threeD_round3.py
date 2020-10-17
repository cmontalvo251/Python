# Import data
import time
import numpy as np
import plotly.graph_objects as go

def frame_args(duration):
    return {"frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
            }

# Generate curve data
t = np.linspace(0, 2*np.pi, 1000)
gamma = 45*np.pi/180.0
xorbit = np.sin(gamma)*np.cos(t)
yorbit = np.sin(t)
zorbit = np.cos(gamma)*np.cos(t)
xm = np.min(xorbit) - 1.5
xM = np.max(xorbit) + 1.5
ym = np.min(yorbit) - 1.5
yM = np.max(yorbit) + 1.5
zm = np.min(zorbit) - 1.5
zM = np.max(zorbit) + 1.5

skip = int(0.01*len(t))
xanimation = xorbit[0:len(t):skip]
yanimation = yorbit[0:len(t):skip]
zanimation = zorbit[0:len(t):skip]
nb_frames = len(xanimation)

fig = go.Figure(frames=[go.Frame(data=go.Scatter3d(
    x=[xanimation[k]],
    y=[yanimation[k]],
    z=[zanimation[k]],
    mode="markers",
    marker=dict(color="red", size=10),
    ),
    name=str(k) # you need to name the frame for the animation to behave properly
    )
    for k in range(nb_frames)]) #Loop through all frames

# Add data to be displayed before animation starts
fig.add_trace(go.Scatter3d(
    x=[xanimation[0]],
    y=[yanimation[1]],
    z=[zanimation[2]],
    mode="markers",
    marker=dict(color="red", size=10)
    ))

##Add Full orbit
fig.add_trace(go.Scatter3d(
    x=xorbit,
    y=yorbit,
    z=zorbit,
    mode="lines",line=dict(width=2, color="blue")
    ))

sliders = [{"pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [{"args": [[f.name], frame_args(0)],
                       "label": str(k),
                       "method": "animate",
                    }
            for k, f in enumerate(fig.frames)],}]

# Layout
fig.update_layout(
        title='3D Orbit',
        width=600,
        height=600,
        scene=dict(
            xaxis=dict(range=[xm,xM]),
            yaxis=dict(range=[ym,yM]),
            zaxis=dict(range=[zm,zM],autorange=False),
        aspectratio=dict(x=1, y=1, z=1),
                    ),
         updatemenus = [{
                "buttons": [{
                        "args": [None, frame_args(50)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",},
                        {"args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",},
                        ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }],
         sliders=sliders
        )

fig.show()