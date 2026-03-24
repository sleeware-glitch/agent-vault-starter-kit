---
fields:
- name: document-role
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': reference
      '2': doctrine
      '3': framework
  style: {}
  path: ''
  id: REFrol1
- name: is-stale
  type: Formula
  options:
    formula: 'current["stale-after"] ? ((new Date() - new Date(current.modified)) / 86400000 > parseInt(current["stale-after"])) ? "stale" : "fresh" : "no-expiry"'
    autoUpdate: true
  style: {}
  path: ''
  id: REFstl1
- name: downstream
  type: Lookup
  options:
    dvQueryString: dv.pages()
    targetFieldName: depends-on
    outputType: LinksList
    autoUpdate: true
  style: {}
  path: ''
  id: REFdwn1
- name: reading-cost
  type: Number
  options: {}
  style: {}
  path: ''
  id: REFcst1
- name: verified
  type: Input
  options: {}
  style: {}
  path: ''
  id: REFvrf1
- name: agent-note
  type: Input
  options: {}
  style: {}
  path: ''
  id: REFnot1
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
  id: REFflg1
- name: stale-after
  type: Input
  options: {}
  style: {}
  path: ''
  id: REFsaf1
version: '2.1'
limit: 20
mapWithTag: false
icon: book-open
savedViews: []
fieldsOrder:
- REFrol1
- REFstl1
- REFdwn1
- REFcst1
- REFvrf1
- REFnot1
- REFflg1
- REFsaf1
summary: NEEDS SUMMARY -- invisible to Vault Map and agent discovery
scope: core
document-role: operations
status: active
stale-after: '14'
fileClass: tracked-item
---
