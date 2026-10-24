#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hardware_mocks — BLOCO 6. Physical-layer mocks (interface only).

These three patents describe PHYSICAL devices. The pilot does NOT and CANNOT
validate any energy/transport/fusion claim in software. Each mock exposes a
well-defined interface and returns an explicit [HARDWARE] status so the
SkyGrid-Sim graph can wire the topology without asserting physics.

  Supercondutor  (BR 10 2026 003450-9): holographic information supercond.
  Motor de Dobra (BR 10 2026 003452-5): dimensional-reflection transport.
  Fusao a Frio   (BR 10 2026 003456-8): psionic field by OH resonance.

Every method returns {"status": "HARDWARE_MOCK", "physical_verdict_allowed": False, ...}.
No number produced here is a physical measurement — only interface plumbing.
"""

import math

from . import tgl_core

OMEGA_OH_MHZ = 1667.359      # hydroxyl line quoted in the patents [DATA, not measured here]


class SupercondutorMock:
    """Interface for holographic information transport. Pipeline only."""

    def transport(self, information_bytes: int) -> dict:
        return {"status": "HARDWARE_MOCK", "device": "supercondutor_holografico",
                "patent": "BR 10 2026 003450-9",
                "throughput_modeled_bytes": information_bytes,
                "physical_verdict_allowed": False,
                "note": "translacao nao-EM alegada na patente; NAO validada em software"}


class MotorDobraMock:
    """Interface for dimensional-reflection transport. theta_M from tgl_core."""

    def fold(self, payload_id: str) -> dict:
        return {"status": "HARDWARE_MOCK", "device": "motor_de_dobra",
                "patent": "BR 10 2026 003452-5",
                "theta_miguel_rad": tgl_core.theta_m(),
                "payload_id": payload_id,
                "physical_verdict_allowed": False,
                "note": "transporte por reflexao dimensional; interface apenas"}


class FusaoFrioMock:
    """Interface for OH-resonance psionic coupling. No energy claim."""

    def couple(self, drive_freq_mhz: float) -> dict:
        on_resonance = abs(drive_freq_mhz - OMEGA_OH_MHZ) < 1.0
        return {"status": "HARDWARE_MOCK", "device": "fusao_a_frio_OH",
                "patent": "BR 10 2026 003456-8",
                "omega_OH_MHz": OMEGA_OH_MHZ, "on_resonance": on_resonance,
                "physical_verdict_allowed": False,
                "note": "acoplamento psionico por ressonancia OH; SEM alegacao de energia"}
