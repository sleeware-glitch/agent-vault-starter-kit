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
  id: CHRsta1
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
  id: CHRsco1
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
  id: CHRrol1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: CHRdep1
- name: dep-check
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].every(d => { const p = dv.page(d); return p && p.status === "done" }) ? "all-clear" : "blocked" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: CHRdpc1
- name: blocked-by
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].filter(d => { const p = dv.page(d); return !p || p.status !== "done" }).map(d => { const p = dv.page(d); return p ? p.file.name + "(" + (p.status || "?") + ")" : "broken-link" }).join(", ") || "none" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: CHRblk1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: CHRdwn1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? current["dep-check"] === "blocked" ? "waiting" : ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: true
  style: {}
  path: ''
  id: CHRstl1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRnot1
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
  id: CHRflg1
- name: source
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRsrc1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRvrf1
- name: stale-after
  type: Number
  options: {}
  style: {}
  path: ''
  id: CHRsaf1
- name: tier
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': protagonist
      '2': major-secondary
      '3': recurring-minor
      '4': scene-character
      '5': named-background
      '6': hyperself
      '7': universal
      '8': named-god
  style: {}
  path: ''
  id: CHRtir1
- name: arc
  type: File
  options: {}
  style: {}
  path: ''
  id: CHRarc1
- name: naming-source
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRnam1
- name: visual-anchor
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRvis1
- name: behavioral-signature
  type: Input
  options: {}
  style: {}
  path: ''
  id: CHRbeh1
- name: core-need
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Sovereignty
      '2': Connection
      '3': Truth
      '4': Safety
      '5': Meaning
      '6': Control
      '7': Recognition
      '8': Transcendence
  style: {}
  path: ''
  id: CHRcnd1
- name: hamartia
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Overconfidence
      '2': Obsession
      '3': Pride
      '4': Naivete
      '5': Passivity
      '6': Distrust
      '7': Stubbornness
      '8': Impulsiveness
  style: {}
  path: ''
  id: CHRham1
- name: sympathizing-trait
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Vulnerability
      '2': Competence
      '3': Moral Courage
      '4': Humor
      '5': Tenderness
      '6': Intensity
      '7': Sacrifice
      '8': Defiance
  style: {}
  path: ''
  id: CHRsym1
- name: self-awareness
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': High
      '2': Medium
      '3': Low
  style: {}
  path: ''
  id: CHRsaw1
- name: spouse-partner
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: CHRsps1
- name: parents
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: CHRpar1
- name: siblings
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: CHRsib1
- name: children
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: CHRchl1
- name: scene-count
  type: Formula
  options:
    formula: '(() => { try { const scenes = dv.pages("\"MANUSCRIPT\"").where(p => p["characters-present"] && dv.func.contains(p["characters-present"], dv.current().file.link)); return scenes.length } catch(e) { return "UNCOMPUTED" } })()'
    autoUpdate: false
  style: {}
  path: ''
  id: CHRscn1
- name: completeness
  type: Formula
  options:
    formula: '(() => { const tier = current["tier"] || "unknown"; let fields; if (tier === "protagonist" || tier === "major-secondary") { fields = ["visual-anchor", "behavioral-signature", "naming-source", "arc", "core-need", "hamartia", "sympathizing-trait", "self-awareness"] } else if (tier === "recurring-minor") { fields = ["visual-anchor", "arc", "sympathizing-trait"] } else if (tier === "hyperself" || tier === "universal" || tier === "named-god") { fields = ["arc", "core-need"] } else { fields = ["visual-anchor", "arc"] } const filled = fields.filter(f => current[f] && current[f] !== "").length; return Math.round((filled / fields.length) * 100) + "%" })()'
    autoUpdate: true
  style: {}
  path: ''
  id: CHRcmp1
- name: consistency-alert
  type: Formula
  options:
    formula: '(() => { try { const charModified = new Date(current.modified); const scenes = dv.pages("\"MANUSCRIPT\"").where(p => p["characters-present"] && dv.func.contains(p["characters-present"], dv.current().file.link) && new Date(p.modified) < charModified); return scenes.length > 0 ? scenes.length + " scenes may need revision" : "all scenes current" } catch(e) { return "UNCOMPUTED" } })()'
    autoUpdate: false
  style: {}
  path: ''
  id: CHRcon1
- name: reading-cost
  type: Formula
  options:
    formula: 'Math.round((current.file && current.file.size ? current.file.size : 0) / 4)'
    autoUpdate: true
  style: {}
  path: ''
  id: CHRcst1
version: '2.1'
limit: 20
mapWithTag: false
icon: user
savedViews: []
fieldsOrder:
- CHRsta1
- CHRtir1
- CHRarc1
- CHRvis1
- CHRbeh1
- CHRnam1
- CHRcnd1
- CHRham1
- CHRsym1
- CHRsaw1
- CHRsps1
- CHRpar1
- CHRsib1
- CHRchl1
- CHRdep1
- CHRsco1
- CHRrol1
- CHRcmp1
- CHRscn1
- CHRcon1
- CHRdpc1
- CHRblk1
- CHRstl1
- CHRdwn1
- CHRcst1
- CHRnot1
- CHRflg1
- CHRsrc1
- CHRvrf1
- CHRsaf1
summary: >
  FileClass definition for character documents. FINAL RECONCILED SCHEMA
  (Core-13 + Craft-18 + Lee). 30 fields: identity (3), craft anchors (2),
  psychology (4 — core-need, hamartia, sympathizing-trait, self-awareness
  with Craft-revised vocabularies), relational (4), computed (4 — scene-
  count, tier-aware completeness, consistency-alert, reading-cost),
  inherited core (13). Tier vocabulary expanded for hyperselves, universals,
  named gods across full trilogy.
scope: core
document-role: operations
status: active
stale-after: 14
fileClass: tracked-item
---
