"""Tests for the llm_proxy config generation and firewall env helpers.

These avoid starting any containers (that's covered by pre_run smoke tests);
they validate the pure logic: config generation, allowlist loading,
env var composition.
"""

from pathlib import Path

from tamaringym.firewall import load_allowlist
from tamaringym.firewall.proxy import (
    DEFAULT_ALLOWLIST_PATH,
    FirewallProxyManager,
)
from tamaringym.llm_proxy import LLMProxyManager


class TestAllowlist:
    def test_default_allowlist_loads(self):
        domains = load_allowlist(DEFAULT_ALLOWLIST_PATH)
        assert ".anthropic.com" in domains
        assert ".openai.com" in domains
        # comments and blank lines skipped
        assert all(d and not d.startswith("#") for d in domains)

    def test_no_redundant_subdomain_entries(self):
        """Squid 6 rejects an entry that is a subdomain of another dotted
        entry in the same ACL (fatal at startup)."""
        domains = load_allowlist(DEFAULT_ALLOWLIST_PATH)
        for d in domains:
            if not d.startswith("."):
                continue
            parent = d
            for other in domains:
                if other == d:
                    continue
                if other.endswith(parent) and other != parent:
                    # 'other' is a subdomain of dotted 'parent' -> redundant
                    raise AssertionError(
                        f"redundant allowlist entry: {other} under {parent}"
                    )

    def test_load_allows_extra(self):
        tmp = Path("/tmp/opencode/test_allowlist.txt")
        tmp.write_text("# comment\n.example.com\n\nother.org\n")
        assert load_allowlist(tmp) == [".example.com", "other.org"]


class TestFirewallManager:
    def test_env_vars_shape(self):
        m = FirewallProxyManager()
        env = m.env_vars()
        assert env["HTTP_PROXY"].startswith("http://")
        assert env["HTTPS_PROXY"] == env["HTTP_PROXY"]
        assert "localhost" in env["NO_PROXY"]

    def test_install_manager_uses_separate_resources(self):
        m = FirewallProxyManager.for_install()
        assert m.allow_all is True
        assert m.container_name != FirewallProxyManager().container_name
        assert m.network_name != FirewallProxyManager().network_name
        assert m.proxy_port != FirewallProxyManager().proxy_port


class TestLLMProxyConfig:
    def test_config_from_claude_style_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok-123")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        monkeypatch.setenv("ANTHROPIC_MODEL", "glm-5.3")
        monkeypatch.delenv("GLM_PROVIDER", raising=False)
        monkeypatch.delenv("GLM_MODEL", raising=False)
        m = LLMProxyManager(port=4999, workdir=tmp_path)
        entries = m._model_entries()
        assert len(entries) == 1
        assert entries[0]["model_name"] == "glm-5.3"
        assert entries[0]["litellm_params"]["api_key"] == "tok-123"
        assert entries[0]["litellm_params"]["api_base"].endswith("/api/anthropic")

    def test_config_glm_provider_passthrough(self, monkeypatch, tmp_path):
        monkeypatch.setenv("GLM_PROVIDER", "anthropic")
        monkeypatch.setenv("GLM_MODEL", "deepseek/deepseek-v4-pro")
        monkeypatch.setenv("GLM_API_KEY", "fk-test")
        monkeypatch.setenv("GLM_API_BASE", "https://api.360.cn")
        m = LLMProxyManager(port=4998, workdir=tmp_path)
        entries = m._model_entries()
        assert (
            entries[0]["litellm_params"]["model"]
            == "anthropic/deepseek/deepseek-v4-pro"
        )

    def test_write_config(self, monkeypatch, tmp_path):
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok-123")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        m = LLMProxyManager(port=4997, workdir=tmp_path)
        path = m.write_config()
        assert path.is_file()
        import yaml

        cfg = yaml.safe_load(path.read_text())
        assert "model_list" in cfg
        assert cfg["general_settings"]["master_key"].startswith("tg-master-")
