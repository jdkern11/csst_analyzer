from typing import List

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from csst.experiment import Experiment
from csst.experiment.models import Reactor

__version__ = "0.1.0"

# Colorblind friendly colors
cmap = ["#2D3142", "#E1DAAE", "#058ED9", "#848FA2"]
tempc = "#CC2D35"


def experiment(experiment: Experiment, figsize=(8, 6)) -> Figure:
    """Plots transmission vs time and temperature vs time for one experiment"""
    # Change parameters for plot
    font = {"size": 18}

    matplotlib.rc("font", **font)

    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax1 = fig.add_subplot(111)
    # Make ax2
    ax2 = ax1.twinx()
    ax2.set_ylabel(str(experiment.actual_temperature).capitalize(), color=tempc)
    ax2.tick_params(axis="y", labelcolor=tempc)
    ax2.plot(
        experiment.time_since_experiment_start.values,
        experiment.actual_temperature.values,
        color=tempc,
        linestyle="dashed",
        alpha=0.5,
    )

    # plot ax1
    ax1.set_xlabel(str(experiment.time_since_experiment_start).capitalize())
    ax1.set_ylabel(str(experiment.reactors[0].transmission).capitalize())

    ax1.set_xlim([0, max(experiment.time_since_experiment_start.values)])
    ax1.tick_params(axis="y", labelcolor="black")
    curr = 0
    for reactor in experiment.reactors:
        ax1.plot(
            reactor.time_since_experiment_start.values,
            reactor.transmission.values,
            color=cmap[curr],
            linewidth=2.5,
            label=str(reactor),
        )
        curr += 1
    fs = 14
    if len(experiment.reactors) > 2:
        offset = -0.425
    else:
        offset = -0.35
    ax1.legend(
        bbox_to_anchor=(0, offset, 1, 0.1),
        loc="lower left",
        mode="expand",
        ncol=2,
        fontsize=fs,
    )
    return fig
