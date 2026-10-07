# Reference Analysis

## Presence
**VERIFIED.** The synthetic resolved version is 4.2.0.

## Advisory applicability
**VERIFIED at version level.** Version 4.2.0 falls inside the synthetic affected range.

## Reachability
**UNVERIFIED.** Static usage evidence does not show direct use of the affected parser, but no controlled runtime reachability test was performed. Absence of a direct static match is not proof of non-reachability.

## Exploitation
**UNVERIFIED.** No supplied evidence demonstrates exploitation.

## Recommended action
Plan an upgrade to 4.2.3 or later compatible fixed release, then rerun dependency resolution, scanning and regression tests. If prioritization depends on exploitability, add a controlled reachability test.

## Reporting language
Prefer: **“Affected dependency version is verified; direct vulnerable-path reachability has not been demonstrated.”**

Avoid: **“The application is compromised because the scanner found a HIGH.”**
