---
fields:
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
  id: DSHsco1
- name: document-role
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': dashboard
  style: {}
  path: ''
  id: DSHrol1
version: '2.1'
limit: 20
mapWithTag: false
icon: layout-dashboard
savedViews: []
fieldsOrder:
- DSHsco1
- DSHrol1
summary: NEEDS SUMMARY -- invisible to Vault Map and agent discovery
scope: core
document-role: operations
status: active
stale-after: '14'
fileClass: tracked-item
---
