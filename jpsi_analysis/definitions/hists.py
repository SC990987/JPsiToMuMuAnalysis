"""Every available histogram and counter, by name.

Histograms are Histogram objects: a list of Axis objects, each bundling a hist axis
with the function that fills it, ``lambda objs, mask: values``. ``objs`` are the
selected objects of one channel. An optional ``evt_mask`` restricts the events
used (for example to events with two muons) and is passed to the fill functions
as ``mask`` so they can apply it before indexing. Storage is weighted by default.

Defining a histogram here does nothing by itself: a collection in
configs/hist_collections.yaml has to list its name. Every collection named at
run time is filled in every channel named at run time, so a fill function that
picks a position (``objs["muons"][mask, 0]``) needs an ``evt_mask`` for the
events that have none; a slice (``objs["muons"][:, :1]``) does not. Counters
are different: all of them are filled, in every channel.
"""

import math

import awkward as ak  # noqa: F401
import hist  # noqa: F401

from jpsi_analysis.tools import histogram as h


# counters: one plain (unweighted) number per channel and sample, summed over
# the events that pass the channel's event cuts
counter_defs = {
    "Selected muons": lambda objs: ak.sum(ak.num(objs["muons"], axis=1)),
    "Selected electrons": lambda objs: ak.sum(ak.num(objs["electrons"], axis=1)),
    "Selected photons": lambda objs: ak.sum(ak.num(objs["photons"], axis=1)),
    "Selected jets": lambda objs: ak.sum(ak.num(objs["jets"], axis=1)),
}


# Default labels and binnings. The binnings are the scaffold's defaults, not
# choices of this analysis: change them here, or per histogram with nbins, xmin
# and xmax. A new object gets its axis label from an entry in obj_labels.
obj_labels = {
    "pvs": "PV",
    "muons": "Muon",
    "electrons": "Electron",
    "photons": "Photon",
    "jets": "Jet",
    "met": "MET",
    "hlt": "HLT",
    "flags": "Flag",
    "gens": "Gen particle",
}
attr_labels = {
    "pt": r"$p_T$ (GeV)",
    "eta": r"$\eta$",
    "phi": r"$\phi$",
    "mass": "Mass (GeV)",
}
default_binnings = {
    "n": (10, 0, 10),
    "pt": (100, 0, 200),
    "eta": (50, -3, 3),
    "phi": (50, -math.pi, math.pi),
    "mass": (100, 0, 200),
}


# convenience functions for the common cases
def make_label(obj, attr, absval=False):
    obj_label = obj_labels.get(obj, obj)
    if attr == "n":
        return f"Number of {obj_label}s"
    attr_label = attr_labels.get(attr, attr)
    if absval:
        attr_label = f"|{attr_label}|"
    return f"{obj_label} {attr_label}"


def obj_attr(obj, attr, absval=False, nbins=None, xmin=None, xmax=None, label=None):
    """One-axis histogram of objs[obj].attr; attr "n" counts the objects per event.

    Binning: nbins, xmin and xmax where given, else default_binnings[attr], else
    (100, 0, 100). The axis is named "<obj>_<attr>"; absval histograms |attr|.
    """
    default_nbins, default_xmin, default_xmax = default_binnings.get(attr, (100, 0, 100))
    nbins = default_nbins if nbins is None else nbins
    xmin = default_xmin if xmin is None else xmin
    xmax = default_xmax if xmax is None else xmax
    label = make_label(obj, attr, absval) if label is None else label
    return h.Histogram.simple_hist(obj, attr, absval, nbins, xmin, xmax, label)


def make_2d(h1, h2):
    """Two-axis histogram from the (last) axes of two one-axis histograms."""
    return h.Histogram([h1.axes[-1], h2.axes[-1]])


def obj_eta_phi(obj):
    return make_2d(obj_attr(obj, "eta"), obj_attr(obj, "phi"))


hist_defs = {
    "pv_n": obj_attr("pvs", "npvs", nbins=100, xmin=0, xmax=100, label="Number of PVs"),
    "pv_z": obj_attr("pvs", "z", nbins=100, xmin=-25, xmax=25, label="PV z (cm)"),
    "muon_n": obj_attr("muons", "n"),
    "muon_pt": obj_attr("muons", "pt", xmax=500),
    "muon_eta_phi": obj_eta_phi("muons"),
    "electron_n": obj_attr("electrons", "n"),
    "electron_pt": obj_attr("electrons", "pt", xmax=500),
    "electron_eta_phi": obj_eta_phi("electrons"),
    "photon_n": obj_attr("photons", "n"),
    "photon_pt": obj_attr("photons", "pt", xmax=500),
    "photon_eta_phi": obj_eta_phi("photons"),
    "jet_n": obj_attr("jets", "n"),
    "jet_pt": obj_attr("jets", "pt", xmax=500),
    "jet_eta_phi": obj_eta_phi("jets"),
    "met_pt": obj_attr("met", "pt", xmax=500),
    "met_phi": obj_attr("met", "phi"),
    "gen_n": obj_attr("gens", "n", nbins=100, xmin=0, xmax=500),
    "gen_pt": obj_attr("gens", "pt", xmax=500),
    "gen_eta_phi": obj_eta_phi("gens"),
    "muon_muon_invmass": h.Histogram(
        [
            h.Axis(hist.axis.Regular(300, 0.2, 1000., transform=hist.axis.transform.log,
                                     name="muon_muon_invmass", label="Invariant mass of the two leading muons (GeV)"),
                   lambda objs, mask: objs["muons"][mask, :2].sum().mass),
        ],
        evt_mask=lambda objs: ak.num(objs["muons"], axis=1) > 1,
    ),
}
