# Films elevation report

Branch: films-elevation-2026-11-16
Work commit: 9ce59481a81754c461629c88d64bb15af9b3bd94
Base kept: 3af9c8c (SEO stage 3)
Nothing was uploaded to Hostinger. Denis was not contacted. No social post was published.

The stairs film was replaced with the Midnight Aggregate floor and treads.

## Kept from the earlier agents

Scroll fix 555f6b5, header flake-ring logo 621e149, motion rounds 64b0908, 96274b9, and 007f6d5, and SEO stages 95d9d04, f54ed0a, and 3af9c8c stay in this history. The Domino clear-pour hero is still epoxy-pour-pearl. Garage, mancave, and walkway-pearl films were left as approved. The flake-ring logo, motion timings, SEO titles, and location-page facts were not rewritten. noindex, nofollow, noarchive remains on the pages checked.

The social footer from the other staging worktree was ported here: Instagram, then Facebook, with marks, a 48px target, and the words "opens in a new tab" for assistive tech. Styles live in films-elevation.css so the hashed footer sheet was not rewritten.

## Stairs

The stairs film was replaced with the Midnight Aggregate floor and treads.

It was not regenerated, quarantined, deleted, or swapped back to the grey floor. The live files match the cut already in the worktree:

- videos/follow-floor/1080/epoxy-resources-stairs.mp4: 3190229 bytes
- videos/follow-floor/720/epoxy-resources-stairs.mp4: 2560873 bytes
- videos/follow-floor/480/epoxy-resources-stairs.mp4: 806962 bytes
- images/brand/epoxy-resources-stairs-poster.jpg: 252223 bytes
- images/brand/epoxy-resources-stairs-poster.webp: 229134 bytes

h264, 24 fps, no audio stream, 6.04 seconds. A frame at 0.2s and a frame at 3.0s do not match, so the camera is moving. The resources library hero uses this poster and this film. The floor at the bottom of the stair and the treads, risers, and landing are the Midnight Aggregate cut: charcoal base with white, light grey, and silver chips, camera pushing in.

Grey-floor backups stay only in videos/follow-floor/_prev-stairs-grey-floor/ and the poster files named bak-grey-floor. They were not swapped back in. Manifest crf for this slot is null because this pass did not re-encode it. The note on the entry says Midnight Aggregate floor and treads.

## Film slots

Facebook for every slot below is UNVERIFIED. No per-job permalink could be confirmed in the handoff notes or on the public web without inventing one. The link text is only the word job. It points at https://www.facebook.com/profile.php?id=61573826827114 with target _blank, rel noopener noreferrer, and the accessible name "job, opens the Facebook post in a new tab".

| Slot | Result |
| --- | --- |
| Domino hero, epoxy-pour-pearl | Kept. Home H1 still reads "A better floor changes the whole space." The 720 film reached 10.042s in the browser, then paused at the end of its existing window. |
| epoxy-garage | Kept. Home garage act. Not regenerated. |
| epoxy-walkway-pearl | Kept. Home foundation act. Not regenerated. |
| epoxy-mancave | Kept in the library. Not regenerated. |
| Basement, epoxy-basement | Upgraded from the real job photo. Low push. Home vault and the residential service hero. 1080 is 3714043 bytes, 720 is 1825216, 480 is 752953. Browser time moved from 0.735s to 1.709s. |
| Finish hall, epoxy-finish | Upgraded. Lateral glide, about 10s. Home finish act and the finishes hero. 1080 is 6073640 bytes, 720 is 2978229, 480 is 1217368. Home time moved from 0.628s to 1.606s. Finishes page was playing at 2.429s. |
| Commercial, epoxy-commercial | Upgraded. Low push. Home commercial act and the commercial service hero. 1080 is 3766809 bytes, 720 is 1877046, 480 is 737966. Home time moved from 0.693s to 1.670s. |
| Consultation, epoxy-consultation | Upgraded. Low push toward the wood stair. Home consultation act and the warranty hero. 1080 is 3774919 bytes, 720 is 1828374, 480 is 753040. Home time moved from 0.647s to 1.620s. |
| Luminous hall, luminous-finish-hall | Upgraded. Low push. Services hero. 1080 is 3817833 bytes, 720 is 1855267, 480 is 761973. Services page was playing at 2.474s. |
| Foundation chamber, foundation-chamber | Upgraded. This hero was a still. Process page. 1080 is 3813249 bytes, 720 is 1829638, 480 is 752609. Process page was playing at 0.945s and not paused. |
| Consultation court, consultation-court | Upgraded. This hero was a still. About page. 1080 is 3797798 bytes, 720 is 1843914, 480 is 763089. About page was playing at 0.947s and not paused. |
| Resources stairs, epoxy-resources-stairs | Kept the Midnight Aggregate cut already on disk. Not regenerated. Resources hero. See the stairs section. Browser time moved from 1.320s to 2.427s. |

New encodes are h264, yuv420p, 24 fps, no audio, faststart, GOP 24. The manifest header still records the older library GOP of 6. Posters for the upgraded slots are a real frame at 1.2s. Stairs posters were not regenerated. Imagine masters under videos/follow-floor/raw-elevation/ were left untracked. Temp frames in _filmcheck were deleted and not committed.

No film slot was blocked. There was no ZDR error and no 429.

## Visual pass

films-elevation.css is linked from all 97 HTML pages. It adds the job credit (Manrope, ink at about 72 percent, cobalt underlined link, focus ring, paper chip), interior film cover, balanced titles, pretty body text, tabular phone numbers, a cobalt focus ring, a slight button press, card shadow, and a little more section air. Reduced motion and the still journey tier hide interior job films and leave the poster. The home player already pauses films when reduced motion is on.

"From this job" sits on the four home job acts (basement, finish, commercial, consultation) and on the heroes for resources, services, residential, commercial, finishes, warranty, process, and about. On interior heroes it follows the lead, so it does not sit on the title. Projects, contact, articles, and location pages do not show a job film, so they do not carry the credit.

## Pages verified

Served the worktree at http://127.0.0.1:8766 and checked it in a browser. A screenshot was not treated as proof. Playback was currentTime moving, or a frame hash change for the stairs file plus playback.

Clicked the resources credit link named "job, opens the Facebook post in a new tab". A new tab opened at https://www.facebook.com/people/Final-Finish-Epoxy-Coatings/61573826827114/ which is the profile redirect. No message was sent. The per-job post is still UNVERIFIED.

Seen:

- Home, desktop: Domino hero source epoxy-pour-pearl, H1 intact, four credits, Instagram then Facebook in the footer, robots noindex,nofollow,noarchive. Vault, finish, commercial, and consultation films advanced while their stages were in view. The hero film had already played to 10.042s.
- Home, 390px wide: H1 visible, no horizontal overflow, hero currentSrc is the 480 pour-pearl file, four credits in the document.
- Resources, desktop: stairs poster, 720 stairs film playing, credit visible, cobalt underlined "job", title and credit boxes do not overlap.
- Resources, 390px: H1 and credit visible, no overflow, currentSrc is the 480 stairs file.
- Resources, reduced motion: stairs video display none and paused, poster image still shown, H1 and credit still visible.
- Home, reduced motion: H1 and the hero paragraph still visible, hero video paused, poster still in the page.
- Services: H1 "Flake floors, built around the room." Luminous hall film playing at 2.474s. Credit visible.
- Projects: H1 present, elevation sheet and social nav present, no job film on this page.
- Finishes: finish film playing at 2.429s. Credit visible.
- Contact: H1 present, phone and email present, social nav present, no job film.
- Article /resources/basement-concrete-floor-coating/: H1 "Basement Floor Coating Basics", sheet and social nav present.
- Location /service-area/leduc/: H1 "Flake floors in Leduc.", sheet and social nav present, no job film (location heroes stay on the existing still).
- About: consultation-court playing. Process: foundation-chamber playing.

## Git

Work commit: 9ce59481a81754c461629c88d64bb15af9b3bd94 on films-elevation-2026-11-16.
This report is a following commit on the same branch.
Push target: a new branch films-elevation-2026-11-16 on kr8tiv-io/final-finish-epoxy. No force. The remote default branch is main and was not updated. The remote did not already have this branch name.
