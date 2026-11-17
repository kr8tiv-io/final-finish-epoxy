# Motion pass, 2026-11-16

## Video revert, 2026-11-17

The elevation film encodes were put back to the 15 Nov job films. Posters for those films were put back with them. The Domino pour, garage, walkway, and mancave files were already unchanged. About and Process had no earlier film, so those two new clips were removed and the previous stills returned. Captions, motion, and the other build additions stayed.

Three keep-or-revert cycles on the films elevation cut. Staging already had that cut before this pass. The Domino pour files and the Midnight Aggregate stairs files were not rewritten.

## Cycle 1, kept: paper seams

Each homepage act after the hero gets an enter veil and an exit veil. Opacity only, eased on scroll. The hero has no veil. Pause visual motion sets the seam to 0 and hides it.

Measured on the local homepage at 1440px: foundation enter opacity 0.994 while the act was arriving, and 0 once it was pinned. Hero veil count 0. Ten veils total (five acts, enter and exit).

## Cycle 2, kept: titles and captions

The offscreen skew entrance is gone from both homepage script bundles. Titles rise 14px and fade. Caption travel is 6vw.

Measured: the strings skewX:-26 and xPercent:-560 are absent. The foundation title sat inside the viewport (left 44, right 791 at 1440px; left 20, right 355 at 390px).

## Cycle 3, kept: play the films, do not re-encode

Frame difference on the 720 masters (mean absolute difference, 96x54 grey, start to mid / start to end):

- basement 37 / 57, commercial 42 / 67, consultation 41 / 64, finish 40 / 40, garage 38 / 67, mancave 25 / 27, foundation chamber 35 / 55, luminous hall 35 / 77, consultation court 37 / 42. These already move.
- stairs 8 / 16, a slow push. Bytes kept (720 is 2560873).
- walkway pearl 6 / 8, a slow drift. Bytes kept.
- epoxy-pour and epoxy-pour-pearl were not sampled for a rewrite and were not touched.

The 180ms delay before act films start is now one animation frame. Interior job films play while the hero is on screen and pause off screen, including when motion is paused. Resources stairs advanced from 4.80s to 6.00s, opacity 1, sources epoxy-resources-stairs.mp4.

## Check

Hero H1 remains "A better floor changes the whole space." Hero sources remain epoxy-pour-pearl.mp4. Phone Lighthouse on the local homepage: performance 52, LCP 11.2s, CLS 0. That sits on the low end of the last 52 to 57 phone band, so the pour file was not compressed. PageSpeed Insights was not re-run (quota was already exhausted). "From this job" still points at the Facebook profile. Per-job permalinks are unverified.
