# Copyright 2019 The Blueqat Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import random
import numpy as np
from ..gate import *
from .backendbase import Backend

class GateListOutputBackend(Backend):
    """Backend for OpenQASM output."""
    def _preprocess_run(self, gates, n_qubits, args, kwargs):
        def _parse_run_args(shots=100, **_kwargs):
            return { 'shots': shots }

        args = _parse_run_args(*args, **kwargs)
        return gates, ([], n_qubits, args['shots'])

    def _postprocess_run(self, ctx):
        return "\n".join([f'{ctx[1]} {ctx[2]} {len(ctx[0])}'] + ctx[0])

    def _one_qubit_gate_noargs(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername} {idx};")
        return ctx

    gate_x = _one_qubit_gate_noargs
    gate_y = _one_qubit_gate_noargs
    gate_z = _one_qubit_gate_noargs
    gate_h = _one_qubit_gate_noargs

    def _two_qubit_gate_noargs(self, gate, ctx):
        for control, target in gate.control_target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername} {control} {target}")
        return ctx

    gate_cz = _two_qubit_gate_noargs
    gate_cx = _two_qubit_gate_noargs

    def _one_qubit_gate_args_theta(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername} {gate.theta} {idx}")
        return ctx

    gate_rx = _one_qubit_gate_args_theta
    gate_ry = _one_qubit_gate_args_theta
    gate_rz = _one_qubit_gate_args_theta

    def gate_i(self, gate, ctx):
        return ctx

    def gate_u3(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"u3 {gate.theta} {gate.phi} {gate.lambd} {idx}")
        return ctx

    def gate_measure(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"m {idx}")
        return ctx
