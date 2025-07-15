"""
Toy Models - Quantum-Biological Coupling via Hyperchronal Field
===============================================================

This module explores how the hyperchronal field Ψ could couple to biological
quantum systems, particularly microtubules (MTs) in neurons, and produce
observable quantum Zeno effects (QZE).

The coupling Hamiltonian:
H = H_bio + H_Ψ + H_int
H_int = g Ψ σ_z (interaction between field and bio-qubits)

Author: Hyperchronal Framework Research Team
"""

import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from qutip import *

class QuantumBioCoupling:
    """
    Model for quantum-biological coupling through hyperchronal field.
    """
    
    def __init__(self, g_coupling=0.01, omega_bio=1.0, gamma_decoherence=0.1):
        """
        Initialize the quantum-bio system.
        
        Parameters:
        -----------
        g_coupling : float
            Coupling strength between hyperchronal field and bio-qubits
        omega_bio : float  
            Characteristic frequency of biological quantum states
        gamma_decoherence : float
            Decoherence rate due to thermal environment
        """
        self.g = g_coupling
        self.omega_bio = omega_bio
        self.gamma = gamma_decoherence
        
        # Pauli operators
        self.sigma_x = sigmax()
        self.sigma_y = sigmay() 
        self.sigma_z = sigmaz()
        self.identity = qeye(2)
        
    def biological_hamiltonian(self):
        """
        Hamiltonian for the biological quantum system (e.g., microtubule).
        
        H_bio = ω σ_z (simple two-level system)
        """
        return 0.5 * self.omega_bio * self.sigma_z
    
    def hyperchronal_field_state(self, psi_amplitude, phase=0):
        """
        Create a coherent state for the hyperchronal field.
        
        Parameters:
        -----------
        psi_amplitude : float
            Amplitude of the hyperchronal field
        phase : float
            Phase of the field
            
        Returns:
        --------
        qutip.Qobj
            Coherent state of the hyperchronal field
        """
        # Simplified: treat as classical background field
        return psi_amplitude * np.exp(1j * phase)
    
    def interaction_hamiltonian(self, psi_field):
        """
        Interaction between hyperchronal field and biological qubits.
        
        H_int = g Ψ σ_z
        """
        return self.g * psi_field * self.sigma_z
    
    def total_hamiltonian(self, psi_field):
        """
        Total Hamiltonian of the coupled system.
        """
        H_bio = self.biological_hamiltonian()
        H_int = self.interaction_hamiltonian(psi_field)
        return H_bio + H_int
    
    def lindblad_operators(self):
        """
        Lindblad operators for decoherence due to thermal environment.
        """
        # Dephasing
        L1 = np.sqrt(self.gamma) * self.sigma_z
        
        # Relaxation (if needed)
        L2 = np.sqrt(self.gamma/2) * sigmam()
        
        return [L1, L2]
    
    def evolve_with_decoherence(self, initial_state, tlist, psi_field):
        """
        Evolve the system with decoherence using master equation.
        
        Parameters:
        -----------
        initial_state : qutip.Qobj
            Initial state of the bio-qubit
        tlist : array
            Time points for evolution
        psi_field : float or function
            Hyperchronal field background
            
        Returns:
        --------
        qutip.solver.Result
            Evolution results
        """
        H = self.total_hamiltonian(psi_field)
        c_ops = self.lindblad_operators()
        
        # Solve master equation
        result = mesolve(H, initial_state, tlist, c_ops, 
                        [self.sigma_x, self.sigma_y, self.sigma_z])
        
        return result
    
    def quantum_zeno_effect(self, measurement_rate, tlist, psi_field):
        """
        Simulate quantum Zeno effect through frequent measurements.
        
        Parameters:
        -----------
        measurement_rate : float
            Rate of quantum measurements (Hz)
        tlist : array
            Time points for evolution
        psi_field : float
            Hyperchronal field amplitude
            
        Returns:
        --------
        dict
            Zeno effect analysis results
        """
        initial_state = (basis(2, 0) + basis(2, 1)).unit()  # Superposition state
        
        # Evolution without measurements
        result_no_meas = self.evolve_with_decoherence(initial_state, tlist, psi_field)
        
        # Evolution with frequent measurements (simplified)
        dt = tlist[1] - tlist[0]
        measurement_interval = 1.0 / measurement_rate
        n_measurements = int(measurement_interval / dt)
        
        # Approximate Zeno effect by modifying decoherence
        zeno_gamma = self.gamma / (1 + measurement_rate * self.g * psi_field)
        
        # Create modified system
        zeno_system = QuantumBioCoupling(self.g, self.omega_bio, zeno_gamma)
        result_with_meas = zeno_system.evolve_with_decoherence(
            initial_state, tlist, psi_field)
        
        return {
            'no_measurements': result_no_meas,
            'with_measurements': result_with_meas,
            'zeno_factor': self.gamma / zeno_gamma
        }
    
    def consciousness_correlation(self, psi_field_values, measurement_rates):
        """
        Explore correlation between hyperchronal field and consciousness indicators.
        
        This is highly speculative and for theoretical exploration only.
        """
        correlations = []
        
        for psi_val in psi_field_values:
            for meas_rate in measurement_rates:
                # Simple metric: coherence preservation under Zeno effect
                tlist = np.linspace(0, 1, 100)
                zeno_results = self.quantum_zeno_effect(meas_rate, tlist, psi_val)
                
                # Calculate final coherence
                final_state = zeno_results['with_measurements'].states[-1]
                coherence = abs(final_state[0, 1])  # Off-diagonal element
                
                correlations.append({
                    'psi_field': psi_val,
                    'measurement_rate': meas_rate,
                    'coherence': coherence
                })
        
        return correlations

def plot_zeno_effect(zeno_results, tlist):
    """
    Plot the quantum Zeno effect results.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Expectation values
    ax1.plot(tlist, zeno_results['no_measurements'].expect[0], 'b-', 
             label='No measurements', linewidth=2)
    ax1.plot(tlist, zeno_results['with_measurements'].expect[0], 'r--',
             label='With measurements', linewidth=2)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('⟨σ_x⟩')
    ax1.set_title('X-component Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(tlist, zeno_results['no_measurements'].expect[1], 'b-',
             label='No measurements', linewidth=2) 
    ax2.plot(tlist, zeno_results['with_measurements'].expect[1], 'r--',
             label='With measurements', linewidth=2)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('⟨σ_y⟩')
    ax2.set_title('Y-component Evolution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    ax3.plot(tlist, zeno_results['no_measurements'].expect[2], 'b-',
             label='No measurements', linewidth=2)
    ax3.plot(tlist, zeno_results['with_measurements'].expect[2], 'r--', 
             label='With measurements', linewidth=2)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('⟨σ_z⟩')
    ax3.set_title('Z-component Evolution')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Hyperchronal Framework - Quantum-Bio Coupling Toy Model")
    print("=======================================================")
    
    # Initialize the quantum-bio system
    qb_system = QuantumBioCoupling(g_coupling=0.05, omega_bio=1.0, gamma_decoherence=0.1)
    
    # Time evolution
    tlist = np.linspace(0, 10, 200)
    
    # Hyperchronal field amplitude
    psi_field = 2.0
    
    print(f"Coupling strength: g = {qb_system.g}")
    print(f"Hyperchronal field amplitude: Ψ = {psi_field}")
    
    # Simulate quantum Zeno effect
    measurement_rate = 5.0  # Hz
    print(f"Measurement rate: {measurement_rate} Hz")
    
    zeno_results = qb_system.quantum_zeno_effect(measurement_rate, tlist, psi_field)
    print(f"Zeno factor (decoherence suppression): {zeno_results['zeno_factor']:.2f}")
    
    # Plot results
    plot_zeno_effect(zeno_results, tlist)
    
    # Consciousness correlation analysis (highly speculative)
    print("\nExploring consciousness correlations (speculative)...")
    psi_values = np.linspace(0.1, 3.0, 5)
    meas_rates = np.linspace(1.0, 10.0, 5)
    
    correlations = qb_system.consciousness_correlation(psi_values, meas_rates)
    
    # Find optimal parameters for coherence preservation
    max_coherence = max(correlations, key=lambda x: x['coherence'])
    print(f"Maximum coherence at: Ψ = {max_coherence['psi_field']:.2f}, "
          f"measurement rate = {max_coherence['measurement_rate']:.2f} Hz")
    print(f"Coherence value: {max_coherence['coherence']:.3f}")
    
    print("\nNote: This is a highly simplified toy model.")
    print("Real biological systems involve many more degrees of freedom")
    print("and complex environmental interactions.")
