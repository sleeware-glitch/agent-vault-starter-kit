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
  id: WBLsta1
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
  id: WBLsco1
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
      '6': scene
      '7': worldbuilding
      '8': dashboard
  style: {}
  path: ''
  id: WBLrol1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: WBLdep1
- name: dep-check
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].every(d => { const p = dv.page(d); return p && p.status === "done" }) ? "all-clear" : "blocked" : "no-deps"'
    autoUpdate: false
  style: {}
  path: ''
  id: WBLdpc1
- name: blocked-by
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].filter(d => { const p = dv.page(d); return !p || p.status !== "done" }).map(d => { const p = dv.page(d); return p ? p.file.name + "(" + (p.status || "?") + ")" : "broken-link" }).join(", ") || "none" : "no-deps"'
    autoUpdate: false
  style: {}
  path: ''
  id: WBLblk1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: WBLdwn1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? current["dep-check"] === "blocked" ? "waiting" : ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: false
  style: {}
  path: ''
  id: WBLstl1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: WBLnot1
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
  id: WBLflg1
- name: source
  type: Input
  options: {}
  style: {}
  path: ''
  id: WBLsrc1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: WBLvrf1
- name: stale-after
  type: Number
  options: {}
  style: {}
  path: ''
  id: WBLsaf1
- name: environment-type
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': city
      '2': institution
      '3': ecosystem
      '4': digital
      '5': historical-era
      '6': natural
      '7': domestic
      '8': sacred
  style: {}
  path: ''
  id: WBLenv1
- name: protagonist
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: WBLpro1
- name: book
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': '1'
      '2': '2'
      '3': '3'
  style: {}
  path: ''
  id: WBLbok1
- name: time-period
  type: Input
  options: {}
  style: {}
  path: ''
  id: WBLtim1
- name: research-sources
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: WBLres1
- name: scenes-consuming
  type: Lookup
  options:
    dvQueryString: dv.pages('"MANUSCRIPT"')
    targetFieldName: setting
    outputType: LinksList
    autoUpdate: false
  style: {}
  path: ''
  id: WBLscn1
- name: reading-cost
  type: Formula
  options:
    formula: 'Math.round((current.file && current.file.size ? current.file.size : 0) / 4)'
    autoUpdate: false
  style: {}
  path: ''
  id: WBLcst1
version: '2.1'
limit: 20
mapWithTag: false
icon: globe
savedViews: []
fieldsOrder:
- WBLsta1
- WBLenv1
- WBLpro1
- WBLbok1
- WBLtim1
- WBLres1
- WBLdep1
- WBLsco1
- WBLrol1
- WBLscn1
- WBLdpc1
- WBLblk1
- WBLstl1
- WBLdwn1
- WBLcst1
- WBLnot1
- WBLflg1
- WBLsrc1
- WBLvrf1
- WBLsaf1
summary: >
  FileClass definition for worldbuilding documents. The RENDERING layer between
  research (facts) and scenes (moments). 20 fields: 13 inherited core, 5 domain-
  specific authored (environment-type, protagonist, book, time-period, research-
  sources), 2 computed (scenes-consuming lookup, reading-cost). Core-13, 2026-03-16.
  Designed with Craft-18's four-layer architecture: Physical Environment, Cultural
  Texture, Hyperself Ecology, Story's Perception, plus Scene-Ready Inventory.
scope: core
document-role: operations
status: active
stale-after: 14
fileClass: tracked-item
---
