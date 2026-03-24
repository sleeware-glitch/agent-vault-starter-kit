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
  id: TRKsta1
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
  id: TRKsco1
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
  id: TRKrol1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: TRKdep1
- name: dep-check
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].every(d => { const p = dv.page(d); return p && p.status === "done" }) ? "all-clear" : "blocked" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: TRKfor1
- name: blocked-by
  type: Formula
  options:
    formula: 'current["depends-on"] && current["depends-on"].length > 0 ? current["depends-on"].filter(d => { const p = dv.page(d); return !p || p.status !== "done" }).map(d => { const p = dv.page(d); return p ? p.file.name + "(" + (p.status || "?") + ")" : "broken-link" }).join(", ") || "none" : "no-deps"'
    autoUpdate: true
  style: {}
  path: ''
  id: TRKblk1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: true
  style: {}
  path: ''
  id: TRKdwn1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? current["dep-check"] === "blocked" ? "waiting" : ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: true
  style: {}
  path: ''
  id: TRKstl1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: TRKnot1
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
  id: TRKflg1
- name: reading-cost
  type: Number
  options: {}
  style: {}
  path: ''
  id: TRKcst1
- name: source
  type: Input
  options: {}
  style: {}
  path: ''
  id: TRKsrc1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: TRKvrf1
- name: stale-after
  type: Input
  options: {}
  style: {}
  path: ''
  id: TRKsaf1
version: '2.1'
limit: 20
mapWithTag: false
icon: package
savedViews: []
fieldsOrder:
- TRKsta1
- TRKsco1
- TRKrol1
- TRKdep1
- TRKfor1
- TRKblk1
- TRKdwn1
- TRKstl1
- TRKnot1
- TRKflg1
- TRKcst1
- TRKsrc1
- TRKvrf1
- TRKsaf1
summary: NEEDS SUMMARY -- invisible to Vault Map and agent discovery
scope: core
document-role: operations
status: active
stale-after: '14'
fileClass: tracked-item
---
