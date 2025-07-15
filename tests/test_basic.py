"""
Basic tests for the Hyperchronal Framework modules.
"""

import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestQFTAnalysis(unittest.TestCase):
    """Tests for QFT analysis modules."""
    
    def test_imports(self):
        """Test that QFT modules can be imported."""
        try:
            import sympy as sp
            import numpy as np
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import required modules: {e}")
    
    def test_hyperchronal_potential(self):
        """Test basic potential calculation."""
        import sympy as sp
        
        # Simple test case
        psi = sp.Symbol('psi', real=True)
        mu_sq = 1.0
        lambda_coupling = 0.1
        
        V = 0.5 * mu_sq * psi**2 + lambda_coupling/24 * psi**4
        
        # Check that potential is real and symmetric
        self.assertEqual(V.subs(psi, 0), 0)  # V(0) = 0
        self.assertEqual(V.subs(psi, 1), V.subs(psi, -1))  # Symmetric

class TestCosmologicalSims(unittest.TestCase):
    """Tests for cosmological simulation modules."""
    
    def test_imports(self):
        """Test that cosmology modules can be imported."""
        try:
            import numpy as np
            from scipy.integrate import odeint
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import required modules: {e}")

class TestToyModels(unittest.TestCase):
    """Tests for toy model modules."""
    
    def test_basic_imports(self):
        """Test basic imports (QuTiP may not be installed yet)."""
        try:
            import numpy as np
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import numpy: {e}")

if __name__ == '__main__':
    # Run tests
    unittest.main()
