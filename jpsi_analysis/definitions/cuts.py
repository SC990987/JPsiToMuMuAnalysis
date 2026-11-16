"""Every available cut, by name.

obj_cut_defs[object][name]  lambda objs, obj: <one True/False per object>
    Object cuts slim a collection; they never reject an event. ``obj`` is the
    collection being cut, after the cuts listed before this one. ``objs`` holds the
    other objects as they are at that point, for cuts that compare collections:
    primary objects defined above this one in objects.py after their cuts, those
    below it before theirs. Derived objects do not exist yet when primary objects
    are cut; the cuts of a derived object see the derived objects built before it.

evt_cut_defs[name]          lambda objs: <one True/False per event>
    Event cuts reject whole events. They are applied after the object cuts, one
    after another, and each becomes a row of the cutflow.

Defining a cut here does nothing by itself: a selection in configs/selections.yaml
has to list its name.

The thresholds below were written by the scaffold so that there is something to
run. They are starting values, not this analysis's cuts: replace them.
"""

import awkward as ak


# small factories, so that each entry below reads as what it does
def pt_above(threshold):
    return lambda objs, obj: obj.pt > threshold


def abs_eta_below(threshold):
    return lambda objs, obj: abs(obj.eta) < threshold


def at_least(name, n):
    return lambda objs: ak.num(objs[name], axis=1) >= n


obj_cut_defs = {
    "muons": {
        "pT > 5 GeV": pt_above(5),
        "pT > 10 GeV": pt_above(10),
        "pT > 20 GeV": pt_above(20),
        "pT > 30 GeV": pt_above(30),
        "|eta| < 2.4": abs_eta_below(2.4),
        "looseId": lambda objs, obj: obj.looseId,
        "mediumId": lambda objs, obj: obj.mediumId,
        "tightId": lambda objs, obj: obj.tightId,
    },
    "electrons": {
        "pT > 10 GeV": pt_above(10),
        "pT > 20 GeV": pt_above(20),
        "pT > 30 GeV": pt_above(30),
        "|eta| < 2.4": abs_eta_below(2.4),
        "|eta| < 2.5": abs_eta_below(2.5),
        "cutBased >= 2": lambda objs, obj: obj.cutBased >= 2,
        "cutBased >= 4": lambda objs, obj: obj.cutBased >= 4,
    },
    "photons": {
        "pT > 20 GeV": pt_above(20),
        "pT > 30 GeV": pt_above(30),
        "|eta| < 2.5": abs_eta_below(2.5),
        "cutBased >= 1": lambda objs, obj: obj.cutBased >= 1,
        "electronVeto": lambda objs, obj: obj.electronVeto,
    },
    "jets": {
        "pT > 20 GeV": pt_above(20),
        "pT > 30 GeV": pt_above(30),
        "pT > 50 GeV": pt_above(50),
        "|eta| < 2.4": abs_eta_below(2.4),
        "|eta| < 4.7": abs_eta_below(4.7),
        "jetId >= 2": lambda objs, obj: obj.jetId >= 2,
    },
    "gens": {
        "pT > 5 GeV": pt_above(5),
        "pT > 10 GeV": pt_above(10),
        "pT > 20 GeV": pt_above(20),
        "|eta| < 2.4": abs_eta_below(2.4),
        "status 1": lambda objs, obj: obj.status == 1,
        "isLastCopy": lambda objs, obj: obj.hasFlags("isLastCopy"),
        "isPrompt": lambda objs, obj: obj.hasFlags("isPrompt"),
        "|pdgId| == 11": lambda objs, obj: abs(obj.pdgId) == 11,
        "|pdgId| == 13": lambda objs, obj: abs(obj.pdgId) == 13,
    },
}

evt_cut_defs = {
    "PV filter": lambda objs: objs["pvs"].npvsGood >= 1,
    ">=1 muons": at_least("muons", 1),
    ">=2 muons": at_least("muons", 2),
    ">=1 electrons": at_least("electrons", 1),
    ">=2 electrons": at_least("electrons", 2),
    ">=1 photons": at_least("photons", 1),
    ">=2 photons": at_least("photons", 2),
    ">=1 jets": at_least("jets", 1),
    ">=2 jets": at_least("jets", 2),
    "MET filters": lambda objs: objs["flags"].METFilters,
}
