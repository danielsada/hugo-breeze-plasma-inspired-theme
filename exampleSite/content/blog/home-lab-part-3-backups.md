---
title: "Home lab, part 3: backups that actually restore"
date: 2026-04-18
description: A backup you have never restored is a hope, not a backup. How I test mine every month without thinking about it.
tags: [homelab, backups, linux]
series: [Home lab]
---

The first two parts were about *running* things. This one is about getting them back.

## The rule

Every backup job has a matching restore job, and the restore job runs on a schedule. If the restore fails, I get an email, the same way I would if the backup failed.

## The setup

- Nightly snapshots of every service's data directory with `restic`.
- A second copy on an external disk that lives in a drawer at a friend's house (rotated monthly).
- A monthly job that restores the latest snapshot into a scratch VM and runs each service's health check against it.

```bash
restic restore latest --target /srv/restore-test
docker compose -f /srv/restore-test/compose.yaml up -d
curl --fail http://localhost:8080/healthz
```

## What it caught

In the first three months the restore test failed twice: once because a database dump was taken mid-write, and once because a config file lived outside the backed-up directory. Neither would have shown up until the day I needed them.