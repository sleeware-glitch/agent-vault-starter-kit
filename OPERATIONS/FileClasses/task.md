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
  style: {}
  path: ''
  id: TSKsta1
- name: scope
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': core
      '2': craft
      '3': research
      '4': all
  style: {}
  path: ''
  id: TSKsco1
- name: priority
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': urgent
      '2': important
      '3': exploratory
  style: {}
  path: ''
  id: TSKpri1
- name: assigned-to
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': core
      '2': craft
      '3': research
      '4': lee
  style: {}
  path: ''
  id: TSKass1
- name: track
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': plotting
      '2': prose
      '3': characters
      '4': worldbuilding
      '5': research
      '6': voice
      '7': editorial
      '8': infrastructure
  style: {}
  path: ''
  id: TSKtrk1
- name: phase
  type: Input
  options: {}
  style: {}
  path: ''
  id: TSKpha1
- name: book
  type: Select
  options:
    sourceType: ValuesList
    valuesList:
      '1': '1'
      '2': '2'
      '3': '3'
      '4': all
  style: {}
  path: ''
  id: TSKbok1
- name: gates
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: TSKgat1
- name: flagged-for
  type: Multi
  options:
    sourceType: ValuesList
    valuesList:
      '1': core
      '2': craft
      '3': research
      '4': lee
  style: {}
  path: ''
  id: TSKflg1
- name: depends-on
  type: MultiFile
  options: {}
  style: {}
  path: ''
  id: TSKdep1
- name: due-by
  type: Date
  options: {}
  style: {}
  path: ''
  id: TSKdue1
- name: created-date
  type: Date
  options: {}
  style: {}
  path: ''
  id: TSKcre1
version: '2.1'
limit: 20
mapWithTag: false
icon: check-square
savedViews: []
fieldsOrder:
- TSKsta1
- TSKtrk1
- TSKpha1
- TSKbok1
- TSKsco1
- TSKpri1
- TSKass1
- TSKdep1
- TSKgat1
- TSKflg1
- TSKdue1
- TSKcre1
summary: >
  Task fileClass for the LEDGER/Tasks/ system. Tracks creative production
  (plotting, prose, characters, worldbuilding, research, voice, editorial)
  and infrastructure. Fields: status, track, phase, book, scope, priority,
  assignment, dependencies, gates, flagged-for, dates.
  Body ## Log section for agent notes and feedback.
scope: core
document-role: operations
status: active
fileClass: tracked-item
---
