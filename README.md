# PlaylistMetadataPipeline

![System Architecture Diagram](Assets/HRDiagram.svg)

## About
A project in which a playlist is entered and the metadata is collected for later use. Furthermore, this program is used as a project to let the main programmer learn how to use factories, SQLite, and proper Python code.

## Overview
PlaylistMetadataPipeline is an automated, stealth-based data extraction tool designed to pull comprehensive song metadata from Spotify playlists. Built as the metadata-ingestion engine for local audio libraries, it safely navigates enterprise security firewalls (WAFs), extracts track data, and seamlessly pipelines the information into both a raw `.csv` format and a structured local SQLite database.

## Bare-Metal (No Docker Required)
This pipeline is designed to run directly on your local machine. Because the stealth browser requires direct interaction with the Windows operating system to bypass privacy prompts, **Docker is not required or recommended for this specific module.** This makes it fully accessible for users who do not have Docker installed.

## Key Features
* **Stealth Automation:** Utilizes SeleniumBase (Undetected Mode) to bypass advanced Cloudflare Turnstile checks and TLS fingerprinting.
* **Browser Factory Architecture:** Implements a scalable Factory pattern to cleanly generate and configure isolated, incognito browser instances.
* **Automated OS Navigation:** Uses `pyautogui` and native file scavenging to silently bypass Windows Explorer UI prompts and route data to the correct project directories.
* **SQLite Integration:** Automatically parses downloaded CSV data and logs Track IDs, Titles, Artists, Albums, Release Years, Durations, and ISRC codes into a persistent `.db` file.
