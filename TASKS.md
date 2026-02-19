# Project Tasks

## Build and verification checklist
- [x] Run frontend production build (`npm --prefix frontend run build`).
- [ ] Run backend unit tests (`python -m pytest tests/unit/server`).
- [ ] Run full test suite (`python -m pytest`).

## Notes
- Backend unit tests failed during collection due to missing dependencies (for example, `async_timeout` and `openhands.agent_server`).
- Full test suite collection failed with missing optional dependencies (for example, `async_timeout`, `numpy`, `torch`, `datasets`) and Python 3.10 incompatibilities in enterprise tests.
