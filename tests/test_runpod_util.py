"""RunPod worker-count policy tests."""

from __future__ import annotations

import os
from unittest.mock import patch

from sim.runpod_util import effective_vcpu, runpod_worker_count


def test_runpod_cpu_count_env_overrides_host() -> None:
    with patch.dict(os.environ, {"RUNPOD_CPU_COUNT": "32"}, clear=False):
        assert effective_vcpu() == 32
        assert runpod_worker_count() == 31


def test_cgroup_vcpu_when_host_inflated() -> None:
    env = {k: v for k, v in os.environ.items() if k != "RUNPOD_CPU_COUNT"}
    with patch.dict(os.environ, env, clear=True):
        with patch("sim.runpod_util._cgroup_vcpu", return_value=32):
            with patch("sim.runpod_util.os.cpu_count", return_value=256):
                assert effective_vcpu() == 32
                assert runpod_worker_count() == 31


def test_worker_count_never_below_one() -> None:
    with patch.dict(os.environ, {"RUNPOD_CPU_COUNT": "1"}, clear=False):
        assert runpod_worker_count() == 1
