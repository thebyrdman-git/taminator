#!/usr/bin/env bash
# Launcher for Taminator (browser-based UI).
# Double-click in Finder to start the app and open it in your browser.

cd "$(dirname "$0")"
exec ./tam-rfe serve
