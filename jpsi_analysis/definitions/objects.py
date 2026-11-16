"""Object definitions: what the analysis calls things, and where each comes from.

primary_objs  name -> lambda evts: ...   read straight from the events.
derived_objs  name -> lambda objs: ...   built from the *selected* objects of a
              channel, in the order they are defined here, so a derived object may
              use any primary object and any derived object defined before it.

Jagged collections (several objects per event) are ordered by pT by the processor,
primary and derived alike, and can take object cuts. One-per-event records (MET,
PV, HLT, Flag) take event cuts only. Because every collection is ordered and cut
on its own, two of them do not stay aligned object by object: to keep something
with each object (the track a muon points to, say), attach it as a field of that
object with ak.with_field instead of defining it as a second object.
"""

import awkward as ak  # noqa: F401


# helpers for generator-level objects
def pid(part, val):
    """Particles whose |pdgId| is val."""
    return part[abs(part.pdgId) == val]


def to_pid(part, val):
    """Particles that decay, with every daughter of |pdgId| val."""
    daughters = abs(part.children.pdgId)
    return part[(ak.num(daughters, axis=-1) > 0) & ak.all(daughters == val, axis=-1)]


def from_pid(part, val):
    """Particles whose mother has |pdgId| val."""
    return part[ak.fill_none(abs(part.parent.pdgId) == val, False)]


# Objects read straight from the events.
primary_objs = {}
primary_objs["pvs"]       = lambda evts: evts.PV
primary_objs["muons"]     = lambda evts: evts.Muon
primary_objs["electrons"] = lambda evts: evts.Electron
primary_objs["photons"]   = lambda evts: evts.Photon
primary_objs["jets"]      = lambda evts: evts.Jet
primary_objs["met"]       = lambda evts: evts.MET
primary_objs["hlt"]       = lambda evts: evts.HLT
primary_objs["flags"]     = lambda evts: evts.Flag
primary_objs["gens"]      = lambda evts: evts.GenPart

# Objects a sample is allowed not to have: generator-level objects on data, a
# collection only some productions carry. Whatever needs one of them is skipped
# there, with a warning. A derived object built from an optional object needs no
# entry of its own: it is absent wherever its input is. List a derived object only
# if its own definition reads a branch some samples lack (a simulation-only field
# of the muons, say). Every other object must build in every sample: if one does
# not, a strict run stops and names it.
optional_objs = ["gens"]

# Objects built from the selected objects of a channel, evaluated in this order.
derived_objs = {}
# For example, the two leading muons of each event:
# derived_objs["leading_muons"] = lambda objs: objs["muons"][:, :2]
