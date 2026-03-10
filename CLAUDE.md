# Project: NHL Data Pipeline

## What
This project is a python-based data pipeline. The objective of this data pipeline is to have a mapping of the entire NHL EDGE API to be able to crawl the data and rebuild that database locally.

## Project Structure
* `src/api/handlers`: contains the request handlers for different NHL EDGE API routes
* `src/services/`: contains interactions with the database where data will be stored
* `src/models`: database models and schemas
* `tests/`: unit and integration tests

## Commands
* Create virtual environment: python3 -m venv venv
* Install dependencies: pip install

## Code Style
* use 4-space indentation
* adhere to pep8 standards
* always statically type variables - functions, variables, etc
* code should favor simplicity over complex logic
* code should be pythonic
* code should use latest libraries
* test-driven development - start with tests first and then write the code
* all new features should be following a branching-PR-merge strategy
* add docstrings for clarity about functions
* always update documentation

## Safety Rules
*   🚨 **Do not** rename public API routes unless explicitly requested.
*   🚨 **Do not** change the database schema without calling it out clearly in the plan.
*   **Do not** modify authentication flows unless the current task explicitly requires it.
*   Preserve backward compatibility for all shared components.

## Interaction Guidelines
*   Criticism is welcome. Please tell me when a better approach exists.
*   Be skeptical of the existing code; it may contain bugs.
*   If you are in doubt of my intent, do not guess; ask a clarifying question.
*   Do not include flattery or unnecessary pleasantries in your responses.