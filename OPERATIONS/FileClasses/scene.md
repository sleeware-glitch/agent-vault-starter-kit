---
fields:
- name: status
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': todo
      '2': in-progress
      '3': blocked
      '4': done
      '5': ready
  style: {}
  path: ''
  id: SCNsta1
- name: scope
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': core
      '2': craft
      '3': research
      '4': all
  style: {}
  path: ''
  id: SCNsco1
- name: document-role
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': canon
      '2': reference
      '3': research
      '4': planning
      '5': operations
      '6': commission
      '7': scene
      '8': dashboard
  style: {}
  path: ''
  id: SCNrol1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNdep1
- name: dep-check
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].every(d => { const p = dv.page(d); return p && p.status === "done" }) ? "all-clear" : "blocked" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNdpc1
- name: blocked-by
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].filter(d => { const p = dv.page(d); return !p || p.status !== "done" }).map(d => { const p = dv.page(d); return p ? p.file.name + "(" + (p.status || "?") + ")" : "broken-link" }).join(", ") || "none" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNblk1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: SCNdwn1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? current["dep-check"] === "blocked" ? "waiting" : ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNstl1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNnot1
- name: flagged-for
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': core
      '2': craft
      '3': research
  style: {}
  path: ''
  id: SCNflg1
- name: source
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNsrc1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNvrf1
- name: stale-after
  type: Number
  options: {}
  style: {}
  path: ''
  id: SCNsaf1
- name: scene-type
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': episode
      '2': stasimon
      '3': prologue
      '4': epilogue
      '5': interlude
      '6': chorus
      '7': overture
      '8': passage
      '9': address
  style: {}
  path: ''
  id: SCNtyp1
- name: act
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNact1
- name: chapter
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNcha1
- name: scene-order
  type: Number
  options: {}
  style: {}
  path: ''
  id: SCNord1
- name: protagonist
  type: File
  options: {}
  style: {}
  path: ''
  id: SCNpro1
- name: preceding-scene
  type: File
  options: {}
  style: {}
  path: ''
  id: SCNpre1
- name: following-scene
  type: File
  options: {}
  style: {}
  path: ''
  id: SCNfol1
- name: story-date-start
  type: Date
  options: {}
  style: {}
  path: ''
  id: SCNsds1
- name: story-date-end
  type: Date
  options: {}
  style: {}
  path: ''
  id: SCNsde1
- name: location
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNloc1
- name: setting
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNset1
- name: arc-color
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNarc1
- name: draft-pass
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': unwritten
      '2': skeleton
      '3': voice
      '4': hyperself
      '5': polish
      '6': complete
  style: {}
  path: ''
  id: SCNdrf1
- name: synopsis
  type: Input
  options: {}
  style: {}
  path: ''
  id: SCNsyn1
- name: characters-present
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNchr1
- name: research-consumed
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNres1
- name: foreshadows
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNfsh1
- name: pays-off
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: SCNpay1
- name: hyperself-organism
  type: File
  options: {}
  style: {}
  path: ''
  id: SCNhso1
- name: interiority-mode
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': specious-present
      '2': memory-as-architecture
      '3': negative-space
      '4': cosmopsychist-inversion
      '5': cognitive-light-cones
      '6': phase-transitions
      '7': fifty-percent-reserve
      '8': pace-layering
      '9': substrate-construction
      '10': cancer-defection
      '11': collective-brain
      '12': feeding-conversion
      '13': design-principles
      '14': the-departure
      '15': continuusparity
      '16': alien-familiar-modulation
  style: {}
  path: ''
  id: SCNint1
- name: mood
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Danger
      '2': Excitement
      '3': Fearful
      '4': Ominous
      '5': Melancholy
      '6': Mysterious
      '7': Lonely
      '8': Sensual
      '9': Humor
      '10': Comfort
      '11': Hopeful
      '12': Intrigue
      '13': Reflective
      '14': Awe
      '15': Sacred
      '16': Grief
  style: {}
  path: ''
  id: SCNmod1
- name: tension
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': Catatonic
      '2': Relaxed
      '3': Neutral
      '4': Alert
      '5': Suspense
      '6': Passionate
      '7': Tragic
  style: {}
  path: ''
  id: SCNten1
- name: pace
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': Glacial
      '2': Slow
      '3': Moderate
      '4': Fast
      '5': Overwhelming
  style: {}
  path: ''
  id: SCNpac1
- name: atmosphere
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Dangerous
      '2': Eerie
      '3': Bustling
      '4': Warm
      '5': Intimate
      '6': Vast
      '7': Alien
      '8': Sacred
      '9': Industrial
      '10': Feral
  style: {}
  path: ''
  id: SCNatm1
- name: context-pack
  type: Formula
  options:
    formula: '(() => { const deps = (current["depends-on"] || []); const chars = (current["characters-present"] || []); const research = (current["research-consumed"] || []); const prev = current["preceding-scene"] ? [current["preceding-scene"]] : []; const all = [...deps, ...chars, ...research, ...prev]; return all.filter(Boolean).map(d => { const p = dv.page(d); return p ? p.file.name : null }).filter(Boolean).join(", ") || "none" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNctx1
- name: completeness
  type: Formula
  options:
    formula: '(() => { const checks = [current["characters-present"] && current["characters-present"].length > 0, current["protagonist"], current["research-consumed"] && current["research-consumed"].length > 0, current["preceding-scene"] || current["following-scene"], current["story-date-start"], current["location"]]; const filled = checks.filter(Boolean).length; return Math.round((filled / checks.length) * 100) + "%" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNcmp1
- name: chain-status
  type: Formula
  options:
    formula: '(() => { const prev = current["preceding-scene"]; const next = current["following-scene"]; if (!prev && !next) return "orphan"; if (!prev) return "chain-start"; if (!next) return "chain-end"; return "linked" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNchn1
- name: revision-flag
  type: Formula
  options:
    formula: '(() => { const chars = current["characters-present"] || []; if (!chars.length) return "no-characters"; const sceneModified = new Date(current.modified); const staleChars = chars.filter(c => { const p = dv.page(c); return p && new Date(p.modified) > sceneModified }).map(c => { const p = dv.page(c); return p ? p.file.name : "?" }); return staleChars.length > 0 ? "check: " + staleChars.join(", ") : "current" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNrev1
- name: dep-stale
  type: Formula
  options:
    formula: '(() => { const deps = current["depends-on"] || []; if (!deps.length) return "no-deps"; const staleDeps = deps.filter(d => { const p = dv.page(d); return p && p["is-stale"] === "stale" }).map(d => { const p = dv.page(d); return p ? p.file.name : "?" }); return staleDeps.length > 0 ? "dep-stale: " + staleDeps.join(", ") : "deps-fresh" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNdps1
- name: reading-cost
  type: Formula
  options:
    formula: 'Math.round((current.file && current.file.size ? current.file.size : 0) / 4)'
    autoUpdate: true
  style: {}
  path: ''
  id: SCNcst1
version: '2.1'
limit: 20
mapWithTag: false
icon: clapperboard
savedViews: []
fieldsOrder:
- SCNsta1
- SCNdrf1
- SCNtyp1
- SCNpro1
- SCNact1
- SCNcha1
- SCNord1
- SCNchr1
- SCNloc1
- SCNset1
- SCNsds1
- SCNsde1
- SCNarc1
- SCNpre1
- SCNfol1
- SCNfsh1
- SCNpay1
- SCNres1
- SCNsyn1
- SCNhso1
- SCNint1
- SCNdep1
- SCNsco1
- SCNrol1
- SCNmod1
- SCNten1
- SCNpac1
- SCNatm1
- SCNctx1
- SCNcmp1
- SCNchn1
- SCNrev1
- SCNdps1
- SCNdpc1
- SCNblk1
- SCNstl1
- SCNdwn1
- SCNcst1
- SCNnot1
- SCNflg1
- SCNsrc1
- SCNvrf1
- SCNsaf1
summary: >
  FileClass definition for scene documents. FINAL RECONCILED SCHEMA (Core-13
  + Craft-18 + Lee). 42 fields: structural authored (16), editorial authored
  (4 — mood/tension/pace/atmosphere, excluded from completeness), stasimon-
  specific (2), relational (5 incl foreshadows/pays-off), computed (7),
  inherited core (13). Scene-type vocabulary expanded for full trilogy.
  Interiority-mode populated from 16 WHI techniques.
scope: core
document-role: operations
status: active
stale-after: 14
fileClass: tracked-item
---
