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
  id: COMsta1
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
  id: COMsco1
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
  id: COMrol1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: COMdep1
- name: dep-check
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].every(d => { const p = dv.page(d); return p && p.status === "done" }) ? "all-clear" : "blocked" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: COMdpc1
- name: blocked-by
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].filter(d => { const p = dv.page(d); return !p || p.status !== "done" }).map(d => { const p = dv.page(d); return p ? p.file.name + "(" + (p.status || "?") + ")" : "broken-link" }).join(", ") || "none" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: COMblk1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: COMdwn1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? current["dep-check"] === "blocked" ? "waiting" : ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: true
  style: {}
  path: ''
  id: COMstl1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: COMnot1
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
  id: COMflg1
- name: source
  type: Input
  options: {}
  style: {}
  path: ''
  id: COMsrc1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: COMvrf1
- name: stale-after
  type: Number
  options: {}
  style: {}
  path: ''
  id: COMsaf1
- name: protagonist
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': Family
      '2': Lin Yù
      '3': Savio Rai
      '4': Caleb Stray
      '5': Story
      '6': Reach
      '7': all
  style: {}
  path: ''
  id: COMpro1
- name: craft-domains
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': setting
      '2': character
      '3': institutional
      '4': sensory
      '5': historical
      '6': scientific
      '7': legal
      '8': psychological
      '9': theological
      '10': cosmological
      '11': geopolitical
      '12': financial
  style: {}
  path: ''
  id: COMcrd1
- name: consumption-status
  type: Formula
  options:
    formula: '(() => { try { const consumers = dv.pages("\"MANUSCRIPT\"").where(p => p["research-consumed"] && dv.func.contains(p["research-consumed"], dv.current().file.link)); return consumers.length === 0 ? "unconsumed" : "consumed-by-" + consumers.length } catch(e) { return "UNCOMPUTED" } })()'
    autoUpdate: false
  style: {}
  path: ''
  id: COMcsm1
- name: scene-consumers
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: research-consumed
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: COMscn1
- name: reading-cost
  type: Formula
  options:
    formula: 'Math.round((current.file && current.file.size ? current.file.size : 0) / 4)'
    autoUpdate: true
  style: {}
  path: ''
  id: COMcst1
version: '2.1'
limit: 20
mapWithTag: false
icon: file-search
savedViews: []
fieldsOrder:
- COMsta1
- COMpro1
- COMcrd1
- COMdep1
- COMsco1
- COMrol1
- COMcsm1
- COMscn1
- COMdpc1
- COMblk1
- COMstl1
- COMdwn1
- COMcst1
- COMnot1
- COMflg1
- COMsrc1
- COMvrf1
- COMsaf1
summary: >
  FileClass definition for completed research report documents (RESEARCH/Completed/).
  Renamed from 'commission' to 'research-report' (Core-13, 2026-03-16) to distinguish
  from research commissions/requests in RESEARCH/Proposed/. 18 fields: 13 inherited
  core nervous system, 2 domain-specific authored (protagonist, craft-domains),
  3 computed (consumption-status, scene-consumers lookup, reading-cost).
scope: core
document-role: operations
status: active
stale-after: 14
fileClass: tracked-item
---
