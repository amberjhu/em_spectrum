# em_spectrum.py
#
# Copyright (c) 2026 Antoni AUGÉ
# License: MIT License
# Author: Antoni AUGÉ
# Generates a figure of the electromagnetic spectrum.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import LogLocator, LogFormatterMathtext

# ------------------------------------------------------------
# Publication settings (LaTeX, font, size)
# ------------------------------------------------------------
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 13
})

# ------------------------------------------------------------
# Physical conversions: wavelength <-> wavenumber
# ------------------------------------------------------------
def wavelength_to_wavenumber(lmbd):
    """Convert wavelength (µm) to wavenumber (cm^-1)"""
    return 1e4 / lmbd

def wavenumber_to_wavelength(eta):
    """Convert wavenumber (cm^-1) to wavelength (µm)"""
    return 1e4 / eta

# ------------------------------------------------------------
# Draw spectral regions
# ------------------------------------------------------------
def draw_spectral_zones(ax):
    zones = [
        ("$\gamma$ rays", 1e-6, 1e-4),
        ("X-rays", 0.0001, 0.01),
        ("UV", 0.01, 0.4),
        ("Visible", 0.4, 0.7),
        ("IR", 0.7, 100),
        ("Microwave/ Radio waves", 100, 1e5)
    ]

    for name, start, end in zones:
        rect = patches.Rectangle(
            (start, 0),
            end - start,
            3,
            linewidth=2,
            edgecolor='black',
            facecolor='none'
        )
        ax.add_patch(rect)

        if name != "Visible":
            ax.text(
                np.sqrt(start * end),
                1.5,
                name,
                ha='center',
                va='center'
            )

# ------------------------------------------------------------
# Draw the visible band (perceptual colormap)
# ------------------------------------------------------------
def draw_visible_band(ax):
    cmap = plt.cm.turbo
    n = 120

    for i in range(n):
        frac = i / n
        x0 = 0.4 + frac * (0.7 - 0.4)
        dx = (0.7 - 0.4) / n

        ax.add_patch(
            patches.Rectangle(
                (x0, 0),
                dx,
                3,
                color=cmap(1 - frac),
                linewidth=0
            )
        )

    ax.text(
        0.53,
        1.5,
        r"\textbf{Visible}",
        ha='center',
        va='center',
        rotation=90,
        rotation_mode='anchor'
    )

# ------------------------------------------------------------
# Highlight thermal radiation region
# ------------------------------------------------------------
def draw_thermal_region(ax):
    start, end = 0.120, 100

    # Draw red lines to mark the thermal region
    ax.plot([start, end], [3.5, 3.5], lw=2, linestyle="-", color='red')
    ax.plot([start, start], [2.8, 3.5], lw=2, linestyle="-", color='red')
    ax.plot([end, end], [2.8, 3.5], lw=2, linestyle="-", color='red')
    ax.plot([(3.5+2.8)/2, (3.5+2.8)/2], [3.5, 3.8], lw=2, linestyle="-", color='red')

    ax.text(
        np.sqrt(start * end),
        3.9,
        r"\textbf{Thermal radiation}",
        ha='center'
    )

# ------------------------------------------------------------
# Create figure and plot everything
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.set_xscale('log')
ax.set_xlim(1e-6, 1e5)
ax.set_ylim(-1, 5)

draw_spectral_zones(ax)
draw_visible_band(ax)
draw_thermal_region(ax)

# Primary axis — wavelength
ax.set_xlabel(r"Wavelength $\lambda \; (\mu m)$")

# Major ticks every power of 10
ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=15))
ax.xaxis.set_major_formatter(LogFormatterMathtext(base=10.0))

# Secondary axis — wavenumber
secax = ax.secondary_xaxis('bottom', functions=(wavelength_to_wavenumber, wavenumber_to_wavelength))
secax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=15))
secax.xaxis.set_major_formatter(LogFormatterMathtext(base=10.0))
secax.set_xlabel(r"Wavenumber $\sigma \; (cm^{-1})$")
secax.spines['bottom'].set_position(('outward', 90))

# Remove y-axis ticks and top/right spines
ax.set_yticks([])
ax.spines[['left', 'right', 'top']].set_visible(False)

plt.tight_layout()

# Save outputs
plt.savefig("em_spectrum.pdf", bbox_inches='tight')
plt.savefig("em_spectrum.png", dpi=600)

# plt.show()  # optional interactive display
