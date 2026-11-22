---
title: How I built a commute-time tracker
date: 2025-11-20
description: Polling a routing API every 15 minutes for a year, and what a week-by-hour heat map taught me about leaving the house.
tags: [go, data, side-project]
params:
  mark: Project
---

My commute takes anywhere from 22 to 61 minutes. I wanted to know *when* to leave, not just how long it usually takes.

## Collect

A small Go program asks a routing API for the door-to-door time every 15 minutes and appends the answer to a SQLite table. It has run on the home-lab server since last November.

```go
type Sample struct {
	At      time.Time
	Minutes int
}
```

## Show

A nightly job turns the table into a JSON file, and a static page draws a heat map: days of the week down the side, 15-minute slots across the top.

## What I learned

Leaving at 7:40 instead of 8:00 saves eleven minutes on average — and, more importantly, makes the slowest days much less slow.

The live chart is on the [projects page](/projects/).