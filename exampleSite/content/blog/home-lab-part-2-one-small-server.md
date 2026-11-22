---
title: "Home lab, part 2: one small server, many services"
date: 2026-03-09
description: Running a dozen services on a fanless mini PC, with one compose file per service and nothing exposed to the internet.
tags: [homelab, docker, linux]
series: [Home lab]
---

A fanless mini PC with 16 GB of RAM turns out to be plenty for a family's worth of services.

## One folder per service

Each service gets its own folder with a `compose.yaml`, a `.env` and a `data/` directory. Updating one never touches another.

```yaml
services:
  photos:
    image: example/photos:1.42
    restart: unless-stopped
    volumes:
      - ./data:/data
    ports:
      - "127.0.0.1:8081:8080"
```

## Nothing on the open internet

Everything binds to localhost and is reached through a VPN. It's slower to set up a new device, and I sleep much better.

## Updates

A weekly job pulls new images, restarts services one at a time and checks their health endpoints. If a check fails, it rolls back and tells me.