### Examples

#### Variables

---

TR = total_releases
TBOBP = TOTAL_NUMBER_OF_BUGS_PRODUCED // only bugs not hotfixes
TTDINPR = TOTAL_TICKETS_DONE_IN_THE_PREVIOUS_RELEASE // features + bugs + hotfixes

TNOF = TOTAL_NUMBER_OF_FAILURES // this includes bugs, hotfixes
TNOFe = TOTAL_NUMBER_OF_FEATURES // previous total features + current features
TRWB = TOTAL_RELEASES_WITHOUT_BUGS
TNOHR = TOTAL_NUMBER_OF_HOTFIX_RELEASES

---

#### Formulas

CFR*HOTFIX_TO_TOTAL = (TNOHR / TR * 100)
CFR*BUG_TO_TASKS_RATIO = CFR_BUG_TO_TASKS_RATIO * TR + ((TBOBP / TTDINPR) _ 100) / TR + 1
CFR_BUG_TO_FEATURE = CFR_BUG_TO_FEATURE _ TR + (TNOF / TNOFe) \* 100) / TR + 1
CFR_BUG_RELEASE_RATIO = TRWB / TR

---

- Breakdown of sample `data.yaml` :-
  _please refer to the variables stated above to understand the structure_

```
total_releases: # TR
total_feature_releases: # TNOFe
total_bugfix_releases: # TBOBP
total_hotfix_releases: # TNOHR
total_releases_without_bugs: TRWB
average_features_per_release: # TNOFe/TR
average_bugs_per_release: # TBOBP/TR
average_hotfixes_per_release: # TNOHR/TR
cfr_hotfix_to_release: # (TNOHR / TR * 100)
cfr_bugs_to_tasks_ratio: # PREV_CFR_BUG_TO_TASKS_RATIO * TR + ((TBOBP / TTDINPR) * 100) / TR + 1
cfr_bug_to_feature: CFR_BUG_TO_FEATURE * TR + (TNOF / TNOFe) * 100) / TR + 1
cfr_bug_release_ratio: TRWB / TR
last_release:
  date: 23-08-2023 11:52 AM
  total_tickets: TTDINPR
  features: 0
  bugs: 0
  hotfixes: 0
  is_hotfix: false

```

- Breakdown of sample `releases.yaml` :-

```
releases:
  - number: 1
    date: 24-08-2023 09:00 AM # the time at which the metrics was calculated for the respective release
    features: 31  # total number of features that followed the recent release
    bugs: 18 # total number of bugfixes that followed the recent release
    hotfixes: 1 # if the recent PR/release was a hotfix, it will be populated
    is_hotfix: false  # if its a hotfix release, it will be true

  - number: 2
    date: 23-08-2023 10:54 AM
    features: 2
    bugs: 1
    hotfixes: 1
    is_hotfix: false
  - number: 3
    date: 23-08-2023 11:12 AM
    features: 0
    bugs: 0
    hotfixes: 1
    is_hotfix: true
  - number: 4
    date: 23-08-2023 11:52 AM
    features: 0
    bugs: 0
    hotfixes: 0
    is_hotfix: false

```

- Sample `releases.yaml` _when calcualted to existing repository_ with git history _(-e True flag)_ :-

```
releases:
  - number: 1
    date: 23-08-2023 10:45 AM # the time at which the metrics was calculated
    features: 31  # total number of features that are present in the base branch
    bugs: 18 # total number of bugfixes that went into the base branch
    hotfixes: 7 # total number of hotfixes that went into the base branch
    is_hotfix: false

```