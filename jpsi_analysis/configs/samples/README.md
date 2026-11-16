# Sample configs

One file per production (`signal.yaml`, `data.yaml`, ...). Each file holds one or more
groups of samples:

```yaml
# ZPrime signal samples, one directory per mass point
nanoaod_v1:                                 # the group (tag)
  path: root://cmseos.fnal.gov//store/user/<you>/signal/
  samples:
    ZPrime_M500_W5:                         # the sample's name
      files:
      - nano_1.root
      # - nano_7.root  # a file that cannot be read can be commented out
      path: ZPrime_M-500_W-5/nano/
```

A file is read from the group's `path`, then the sample's `path`, then its name in
`files` (a complete path or url in `files` is taken as it is). A sample can also say
`is_data: true` (data), `year` (its run period in `configs/run_periods.yaml`) and
`skim_factor` (the fraction of the original events a skim kept). A sample without a
`year` takes its group's, if the group has one, or else `YEAR` of
`jpsi_analysis/__init__.py`, the project's run period. So data states its year, and
simulation only a year that is not `YEAR`. Simulated samples take their cross section
from `configs/cross_sections.yaml`, under the sample's name.

Every file here is read: `utilities.make_fileset(["ZPrime_M500_W5"])` finds the sample
wherever it is. A name used in two groups needs its group (`tag=`), and in two files
with the same group name also its file (`location_cfg=`); the check says so.

To add the samples of a directory, local or `root://`, in this layout: the first
command writes the group above, one sample per sub-directory, and the second makes a
directory of data one sample.

```bash
python -m jpsi_analysis.scripts.add_samples -o signal.yaml -t nanoaod_v1 \
    -d root://cmseos.fnal.gov//store/user/<you>/signal/ \
    -c "ZPrime signal samples, one directory per mass point" --name-format "ZPrime_M{M}_W{W}"
python -m jpsi_analysis.scripts.add_samples -o data.yaml -t nanoaod_v1 -c "2018 data" \
    -d root://cmseos.fnal.gov//store/user/<you>/data/SingleMuon/ \
    --name SingleMuon_2018C --data --year 2018
```
