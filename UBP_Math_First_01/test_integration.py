"""
UBP Integration Tests

Integration tests for the UBP runtime and DSL components.
Tests complete workflows and system interactions.
"""

import unittest
import tempfile
import os
import json
from typing import Dict, Any

# Import UBP components
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ubp_vm import Runtime, parse_ubp_script, eval_program
from ubp_vm.dsl import DSLParser, UBPParseError, UBPRuntimeError
from ubp_semantics import OffBit, Bitfield


class TestRuntimeIntegration(unittest.TestCase):
    """Test Runtime system integration."""
    
    def setUp(self):
        """Set up test runtime."""
        self.runtime = Runtime("desktop_8gb")
    
    def test_runtime_initialization(self):
        """Test runtime initialization and configuration."""
        # Test initial state
        self.assertEqual(self.runtime.state.time_step, 0)
        self.assertEqual(self.runtime.state.active_realm, "quantum")
        self.assertEqual(self.runtime.bitfield.total_offbits, 0)
        
        # Test realm switching
        self.runtime.set_realm("electromagnetic")
        self.assertEqual(self.runtime.state.active_realm, "electromagnetic")
        
        # Test invalid realm
        with self.assertRaises(ValueError):
            self.runtime.set_realm("invalid_realm")
    
    def test_bitfield_initialization_patterns(self):
        """Test different Bitfield initialization patterns."""
        # Test sparse random
        self.runtime.initialize_bitfield("sparse_random", density=0.001, seed=42)
        self.assertGreater(self.runtime.bitfield.total_offbits, 0)
        
        # Test quantum bias
        self.runtime.initialize_bitfield("quantum_bias", density=0.001, seed=42)
        self.assertGreater(self.runtime.bitfield.total_offbits, 0)
        
        # Test realm specific
        self.runtime.set_realm("cosmological")
        self.runtime.initialize_bitfield("realm_specific", density=0.001, seed=42)
        self.assertGreater(self.runtime.bitfield.total_offbits, 0)
    
    def test_toggle_operations_execution(self):
        """Test execution of various toggle operations."""
        # Initialize with some OffBits
        self.runtime.initialize_bitfield("sparse_random", density=0.001, seed=42)
        
        coord1 = (10, 10, 10, 1, 0, 0)
        coord2 = (10, 10, 10, 1, 0, 1)
        
        # Set known OffBits
        self.runtime.bitfield.set_offbit(coord1, OffBit(1000))
        self.runtime.bitfield.set_offbit(coord2, OffBit(2000))
        
        # Test basic operations
        result_and = self.runtime.execute_toggle_operation("and", coord1, coord2)
        self.assertEqual(result_and.value, 1000)  # min(1000, 2000)
        
        result_xor = self.runtime.execute_toggle_operation("xor", coord1, coord2)
        self.assertEqual(result_xor.value, 1000)  # |1000 - 2000|
        
        result_or = self.runtime.execute_toggle_operation("or", coord1, coord2)
        self.assertEqual(result_or.value, 2000)  # max(1000, 2000)
        
        # Test advanced operations
        result_resonance = self.runtime.execute_toggle_operation(
            "resonance", coord1, frequency=100.0, time=0.1
        )
        self.assertIsInstance(result_resonance, OffBit)
        
        result_entanglement = self.runtime.execute_toggle_operation(
            "entanglement", coord1, coord2, coherence=0.96
        )
        self.assertIsInstance(result_entanglement, OffBit)
    
    def test_simulation_execution(self):
        """Test complete simulation execution."""
        # Initialize system
        self.runtime.initialize_bitfield("sparse_random", density=0.01, seed=42)
        initial_offbits = self.runtime.bitfield.total_offbits
        
        # Run simulation
        result = self.runtime.run_simulation(
            steps=10,
            operations_per_step=5,
            record_timeline=True
        )
        
        # Validate result structure
        self.assertIsNotNone(result.initial_state)
        self.assertIsNotNone(result.final_state)
        self.assertIsInstance(result.metrics, dict)
        self.assertGreater(result.execution_time, 0)
        self.assertEqual(len(result.timeline), 11)  # Initial + 10 steps
        
        # Validate metrics
        self.assertIn("nrci", result.metrics)
        self.assertIn("coherence_pressure", result.metrics)
        self.assertIn("fractal_dimension", result.metrics)
        self.assertIn("energy", result.metrics)
        
        # Validate state progression
        self.assertEqual(result.initial_state.time_step, 0)
        self.assertEqual(result.final_state.time_step, 10)
        self.assertGreater(result.final_state.total_toggles, 0)
    
    def test_realm_specific_operations(self):
        """Test realm-specific operation selection."""
        realms_to_test = ["quantum", "electromagnetic", "gravitational", "biological"]
        
        for realm in realms_to_test:
            with self.subTest(realm=realm):
                self.runtime.reset()
                self.runtime.set_realm(realm)
                self.runtime.initialize_bitfield("sparse_random", density=0.005, seed=42)
                
                # Run short simulation
                result = self.runtime.run_simulation(steps=5, operations_per_step=3)
                
                # Should complete without errors
                self.assertIsNotNone(result)
                self.assertEqual(result.final_state.active_realm, realm)
    
    def test_state_export_import(self):
        """Test state export functionality."""
        # Initialize and run simulation
        self.runtime.initialize_bitfield("sparse_random", density=0.01, seed=42)
        self.runtime.run_simulation(steps=5, operations_per_step=3)
        
        # Export state
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_path = f.name
        
        try:
            self.runtime.export_state(export_path, "json")
            
            # Verify file exists and contains data
            self.assertTrue(os.path.exists(export_path))
            
            with open(export_path, 'r') as f:
                exported_data = json.load(f)
            
            # Validate exported structure
            self.assertIn("runtime_state", exported_data)
            self.assertIn("bitfield_stats", exported_data)
            self.assertIn("realm_configs", exported_data)
            
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
    
    def test_performance_tracking(self):
        """Test performance statistics tracking."""
        # Initialize and run operations
        self.runtime.initialize_bitfield("sparse_random", density=0.005, seed=42)
        
        coord1 = (5, 5, 5, 0, 0, 0)
        coord2 = (5, 5, 5, 0, 0, 1)
        
        # Execute multiple operations
        for _ in range(10):
            self.runtime.execute_toggle_operation("xor", coord1, coord2)
        
        # Get performance stats
        stats = self.runtime.get_performance_stats()
        
        # Validate stats structure
        self.assertIn("elapsed_time", stats)
        self.assertIn("operations_per_second", stats)
        self.assertIn("total_operations", stats)
        self.assertIn("memory_efficiency", stats)
        
        # Validate values
        self.assertEqual(stats["total_operations"], 10)
        self.assertGreaterEqual(stats["elapsed_time"], 0)


class TestDSLIntegration(unittest.TestCase):
    """Test DSL parser and execution integration."""
    
    def setUp(self):
        """Set up DSL parser."""
        self.parser = DSLParser()
    
    def test_script_parsing(self):
        """Test UBP script parsing."""
        script = '''
        init-runtime hardware=desktop_8gb
        set-realm quantum
        init-bitfield pattern=sparse_random density=0.01 seed=42
        run-simulation steps=10 ops_per_step=5
        get-metrics
        '''
        
        commands = self.parser.parse_script(script)
        
        # Validate parsed commands
        self.assertEqual(len(commands), 5)
        
        # Check first command
        init_cmd = commands[0]
        self.assertEqual(init_cmd.command, "init-runtime")
        self.assertEqual(init_cmd.kwargs["hardware"], "desktop_8gb")
        
        # Check simulation command
        sim_cmd = commands[3]
        self.assertEqual(sim_cmd.command, "run-simulation")
        self.assertEqual(sim_cmd.kwargs["steps"], 10)
        self.assertEqual(sim_cmd.kwargs["ops_per_step"], 5)
    
    def test_parenthesized_syntax(self):
        """Test Lisp-style parenthesized command syntax."""
        script = '''
        (init-runtime hardware=desktop_8gb)
        (set-realm "quantum")
        (init-bitfield pattern="sparse_random" density=0.01)
        '''
        
        commands = self.parser.parse_script(script)
        
        self.assertEqual(len(commands), 3)
        self.assertEqual(commands[0].command, "init-runtime")
        self.assertEqual(commands[1].args[0], "quantum")
        self.assertEqual(commands[2].kwargs["pattern"], "sparse_random")
    
    def test_script_execution(self):
        """Test complete script execution."""
        script = '''
        init-runtime hardware=desktop_8gb
        set-realm quantum
        init-bitfield pattern=sparse_random density=0.005 seed=42
        run-simulation steps=5 ops_per_step=3 timeline=true
        get-metrics
        '''
        
        results = self.parser.execute_script(script)
        
        # Validate execution results
        self.assertIn("final_state", results)
        self.assertIn("runtime_state", results["final_state"])
        self.assertIn("performance_stats", results["final_state"])
        
        # Check that simulation ran
        runtime_state = results["final_state"]["runtime_state"]
        self.assertEqual(runtime_state["time_step"], 5)
        self.assertGreater(runtime_state["total_toggles"], 0)
    
    def test_variable_handling(self):
        """Test variable setting and usage."""
        script = '''
        set-var test_value 42
        set-var test_string "hello world"
        set-var test_list [1, 2, 3]
        '''
        
        results = self.parser.execute_script(script)
        
        # Check variables were set
        self.assertEqual(self.parser.variables["test_value"], 42)
        self.assertEqual(self.parser.variables["test_string"], "hello world")
        self.assertEqual(self.parser.variables["test_list"], [1, 2, 3])
    
    def test_toggle_operation_script(self):
        """Test toggle operation execution via script."""
        script = '''
        init-runtime
        init-bitfield pattern=sparse_random density=0.001 seed=42
        toggle xor [0,0,0,0,0,0] [0,0,0,0,0,1]
        toggle resonance [1,1,1,0,0,0] [1,1,1,0,0,1] frequency=1000.0
        '''
        
        results = self.parser.execute_script(script)
        
        # Should execute without errors
        self.assertIsInstance(results, dict)
        
        # Check toggle operation results
        toggle_results = [v for k, v in results.items() 
                         if k.startswith("line_") and isinstance(v, dict) 
                         and "operation" in v]
        
        self.assertGreater(len(toggle_results), 0)
    
    def test_export_functionality(self):
        """Test export commands in scripts."""
        script = '''
        init-runtime
        init-bitfield pattern=sparse_random density=0.005 seed=42
        run-simulation steps=3 ops_per_step=2
        '''
        
        # Execute script
        results = self.parser.execute_script(script)
        
        # Test state export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            state_export_path = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            results_export_path = f.name
        
        try:
            # Test export commands
            export_script = f'''
            export-state "{state_export_path}"
            export-results "{results_export_path}"
            '''
            
            export_results = self.parser.execute_script(export_script)
            
            # Verify files were created
            self.assertTrue(os.path.exists(state_export_path))
            self.assertTrue(os.path.exists(results_export_path))
            
            # Verify file contents
            with open(state_export_path, 'r') as f:
                state_data = json.load(f)
            self.assertIn("runtime_state", state_data)
            
            with open(results_export_path, 'r') as f:
                results_data = json.load(f)
            self.assertIn("initial_state", results_data)
            
        finally:
            for path in [state_export_path, results_export_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_error_handling(self):
        """Test error handling in script execution."""
        # Test parse error
        invalid_script = '''
        invalid-command with bad syntax
        '''
        
        with self.assertRaises(UBPRuntimeError):
            self.parser.execute_script(invalid_script)
        
        # Test runtime error
        runtime_error_script = '''
        set-realm invalid_realm
        '''
        
        with self.assertRaises(UBPRuntimeError):
            self.parser.execute_script(runtime_error_script)
    
    def test_multi_realm_workflow(self):
        """Test multi-realm simulation workflow."""
        script = '''
        init-runtime
        
        # Quantum phase
        use-realm quantum
        init-bitfield pattern=quantum_bias density=0.005 seed=42
        run-simulation steps=3 ops_per_step=2
        
        # Electromagnetic phase  
        use-realm electromagnetic
        run-simulation steps=3 ops_per_step=2
        
        get-metrics
        '''
        
        results = self.parser.execute_script(script)
        
        # Should complete successfully
        self.assertIn("final_state", results)
        
        # Final realm should be electromagnetic
        final_realm = results["final_state"]["runtime_state"]["active_realm"]
        self.assertEqual(final_realm, "electromagnetic")


class TestEvalProgram(unittest.TestCase):
    """Test high-level eval_program function."""
    
    def test_eval_program_basic(self):
        """Test basic program evaluation."""
        program = '''
        set-realm quantum
        init-bitfield pattern=sparse_random density=0.005 seed=42
        run-simulation steps=5 ops_per_step=3
        '''
        
        results = eval_program(program, "desktop_8gb")
        
        # Should auto-initialize runtime
        self.assertIn("final_state", results)
        
        # Should have run simulation
        runtime_state = results["final_state"]["runtime_state"]
        self.assertEqual(runtime_state["time_step"], 5)
        self.assertEqual(runtime_state["active_realm"], "quantum")
    
    def test_eval_program_with_explicit_init(self):
        """Test program with explicit runtime initialization."""
        program = '''
        init-runtime hardware=raspberry_pi
        set-realm biological
        init-bitfield pattern=sparse_random density=0.001 seed=123
        run-simulation steps=2 ops_per_step=1
        '''
        
        results = eval_program(program)
        
        # Should use explicit initialization
        self.assertIn("final_state", results)
        runtime_state = results["final_state"]["runtime_state"]
        self.assertEqual(runtime_state["active_realm"], "biological")
    
    def test_template_scripts(self):
        """Test predefined template scripts."""
        from ubp_vm.dsl import QUANTUM_SIMULATION_TEMPLATE, TOGGLE_OPERATIONS_TEMPLATE
        
        # Test quantum simulation template
        quantum_results = eval_program(QUANTUM_SIMULATION_TEMPLATE)
        self.assertIn("final_state", quantum_results)
        
        # Test toggle operations template
        toggle_results = eval_program(TOGGLE_OPERATIONS_TEMPLATE)
        self.assertIn("final_state", toggle_results)


class TestSystemIntegration(unittest.TestCase):
    """Test complete system integration scenarios."""
    
    def test_nrci_validation_workflow(self):
        """Test NRCI validation workflow."""
        # Create a simulation designed to test NRCI calculation
        script = '''
        init-runtime hardware=desktop_8gb
        set-realm quantum
        init-bitfield pattern=quantum_bias density=0.01 seed=42
        run-simulation steps=20 ops_per_step=10 timeline=true
        get-metrics
        '''
        
        results = eval_program(script)
        
        # Extract NRCI from results
        metrics_result = None
        for key, value in results.items():
            if isinstance(value, dict) and "bitfield_stats" in value:
                metrics_result = value
                break
        
        self.assertIsNotNone(metrics_result)
        
        # Validate NRCI is calculated
        runtime_state = results["final_state"]["runtime_state"]
        self.assertGreaterEqual(runtime_state["nrci_value"], 0.0)
        self.assertLessEqual(runtime_state["nrci_value"], 1.0)
    
    def test_energy_conservation_check(self):
        """Test energy conservation during operations."""
        runtime = Runtime("desktop_8gb")
        runtime.initialize_bitfield("sparse_random", density=0.01, seed=42)
        
        # Record initial energy
        initial_energy = runtime._calculate_current_energy()
        
        # Perform operations
        coord1 = (10, 10, 10, 1, 0, 0)
        coord2 = (10, 10, 10, 1, 0, 1)
        
        runtime.bitfield.set_offbit(coord1, OffBit(1000))
        runtime.bitfield.set_offbit(coord2, OffBit(2000))
        
        # Execute conservative operations (should preserve total information)
        for _ in range(5):
            result = runtime.execute_toggle_operation("xor", coord1, coord2)
            runtime.bitfield.set_offbit(coord1, result)
        
        # Check energy after operations
        final_energy = runtime._calculate_current_energy()
        
        # Energy should be related to active OffBit count
        self.assertGreater(final_energy, 0)
    
    def test_coherence_pressure_monitoring(self):
        """Test coherence pressure monitoring during simulation."""
        script = '''
        init-runtime
        set-realm quantum
        init-bitfield pattern=sparse_random density=0.02 seed=42
        run-simulation steps=15 ops_per_step=8 timeline=true
        '''
        
        results = eval_program(script)
        
        # Check coherence pressure in final state
        runtime_state = results["final_state"]["runtime_state"]
        self.assertIn("coherence_pressure", runtime_state)
        self.assertGreaterEqual(runtime_state["coherence_pressure"], 0.0)
    
    def test_hardware_profile_scaling(self):
        """Test different hardware profile configurations."""
        profiles = ["desktop_8gb", "mobile_4gb", "raspberry_pi"]
        
        for profile in profiles:
            with self.subTest(profile=profile):
                script = f'''
                init-runtime hardware={profile}
                init-bitfield pattern=sparse_random density=0.005 seed=42
                run-simulation steps=3 ops_per_step=2
                '''
                
                results = eval_program(script)
                
                # Should complete successfully for all profiles
                self.assertIn("final_state", results)
                
                # Performance should vary by profile
                perf_stats = results["final_state"]["performance_stats"]
                self.assertIn("memory_efficiency", perf_stats)


if __name__ == '__main__':
    # Run all integration tests
    unittest.main(verbosity=2)

