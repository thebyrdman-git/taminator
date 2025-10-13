# Changelog

All notable changes to miraclemax infrastructure will be documented in this file.

## [Unreleased]

### Added
- Initial Infrastructure as Code implementation
- Podman-compose files for all services
- Deployment automation scripts
- Version pinning for all container images
- Health checks for all services
- Resource limits based on SRE capacity planning
- Comprehensive documentation

### Changed
- Migrated from ad-hoc container management to IaC

### Services
- Traefik v3.0.0 (reverse proxy)
- Home Assistant 2024.10.1 (home automation)
- Actual Budget 24.10.1 (personal finance)
- n8n 1.60.1 (workflow automation)
- cAdvisor v0.47.0 (container metrics)

## [Initial State] - 2025-10-12

### Existing Infrastructure
- RHEL 9.6 server
- Podman 5.4.0
- 5 containers running with `:latest` tags
- No version control
- Manual deployment process

