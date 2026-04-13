# ADR: 0012-migrate-to-sqlite
**Date**: 2017-08-22
**Status**: Accepted

## Context
Move from JSON to SQLite to support concurrent local reads.

## Decision
We will implement this immediately to support our scaling needs.

## Consequences
Significant refactoring required, but it positions us for the next 5 years of growth.
