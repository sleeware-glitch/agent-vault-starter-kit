# MCP Server — Customization Required

These files are functional reference code from the TRANSCENT project.
Before running, you MUST change:

1. **vault_mcp_server.py line ~33:** Change `VAULT_PATH` to YOUR vault's absolute path
2. **vault_mcp_server.py line ~104:** Change `"transcent_vault"` to your project name
3. **vault_mcp_server.py (run_python function):** Update `_ALLOWED_ROOTS` sandbox paths
4. **Tool docstrings:** References to "TRANSCENT" are cosmetic — they don't affect functionality

See SETUP.md for the full installation and configuration guide.
