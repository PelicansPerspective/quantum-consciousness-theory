"""
Cosmological Simulations - Hyperchronal Dark Energy
===================================================

This module simulates the cosmological evolution with hyperchronal field 
acting as quintessence dark energy.

The Friedmann equations with hyperchronal field:
H² = (8πG/3)(ρ_m + ρ_Ψ)
ä/a = -(4πG/3)(ρ_m + ρ_Ψ + 3P_Ψ)

where ρ_Ψ and P_Ψ are the energy density and pressure of the Ψ field.

Author: Hyperchronal Framework Research Team
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from astropy import units as u
from astropy import constants as const

# Cosmological parameters
H0 = 70 * u.km / u.s / u.Mpc  # Hubble constant
Omega_m0 = 0.3                # Matter density parameter today
Omega_Lambda0 = 0.7           # Dark energy density parameter today
c = const.c.to(u.km/u.s)      # Speed of light

class HyperchronalCosmology:
    """
    Class for simulating cosmological evolution with hyperchronal field.
    """
    
    def __init__(self, H0=70, Omega_m0=0.3, psi_params=None):
        """
        Initialize cosmological parameters.
        
        Parameters:
        -----------
        H0 : float
            Hubble constant in km/s/Mpc
        Omega_m0 : float
            Present-day matter density parameter
        psi_params : dict
            Parameters for hyperchronal field potential
        """
        self.H0 = H0
        self.Omega_m0 = Omega_m0
        self.Omega_psi0 = 1 - Omega_m0  # Assuming flat universe
        
        # Default hyperchronal field parameters
        if psi_params is None:
            self.psi_params = {
                'mass_squared': 1e-66,  # Very light field (eV²)
                'lambda': 1e-120,       # Extremely weak self-coupling
                'initial_psi': 1.0,     # Initial field value (Planck units)
                'initial_dpsi': 0.0     # Initial field velocity
            }
        else:
            self.psi_params = psi_params
    
    def hyperchronal_potential(self, psi):
        """
        Hyperchronal field potential V(Ψ).
        
        V(Ψ) = (1/2) m² Ψ² + (λ/4!) Ψ⁴
        """
        m_sq = self.psi_params['mass_squared'] 
        lam = self.psi_params['lambda']
        return 0.5 * m_sq * psi**2 + lam/24 * psi**4
    
    def potential_derivative(self, psi):
        """
        Derivative of the potential dV/dΨ.
        """
        m_sq = self.psi_params['mass_squared']
        lam = self.psi_params['lambda'] 
        return m_sq * psi + lam/6 * psi**3
    
    def energy_density_psi(self, psi, dpsi_dt, H):
        """
        Energy density of hyperchronal field.
        
        ρ_Ψ = (1/2) (dΨ/dt)² + V(Ψ)
        """
        kinetic = 0.5 * dpsi_dt**2
        potential = self.hyperchronal_potential(psi)
        return kinetic + potential
    
    def pressure_psi(self, psi, dpsi_dt, H):
        """
        Pressure of hyperchronal field.
        
        P_Ψ = (1/2) (dΨ/dt)² - V(Ψ)
        """
        kinetic = 0.5 * dpsi_dt**2
        potential = self.hyperchronal_potential(psi)
        return kinetic - potential
    
    def equation_of_state(self, psi, dpsi_dt, H):
        """
        Equation of state parameter w = P/ρ for hyperchronal field.
        """
        rho = self.energy_density_psi(psi, dpsi_dt, H)
        P = self.pressure_psi(psi, dpsi_dt, H)
        
        if rho == 0:
            return 0
        return P / rho
    
    def cosmological_equations(self, y, t):
        """
        System of ODEs for cosmological evolution.
        
        y = [a, psi, dpsi_dt]
        where a is scale factor, psi is field value, dpsi_dt is field velocity
        """
        a, psi, dpsi_dt = y
        
        # Hubble parameter
        H = np.sqrt((8 * np.pi / 3) * (
            self.Omega_m0 / a**3 + 
            self.energy_density_psi(psi, dpsi_dt, 0) / self.Omega_psi0
        )) * self.H0
        
        # Scale factor evolution
        da_dt = a * H
        
        # Field equation: d²Ψ/dt² + 3H dΨ/dt + dV/dΨ = 0
        d2psi_dt2 = -3 * H * dpsi_dt - self.potential_derivative(psi)
        
        return [da_dt, dpsi_dt, d2psi_dt2]
    
    def evolve(self, t_span, initial_conditions=None):
        """
        Evolve the cosmological system.
        
        Parameters:
        -----------
        t_span : array
            Time array for evolution
        initial_conditions : list
            [a0, psi0, dpsi_dt0]
            
        Returns:
        --------
        dict
            Evolution results
        """
        if initial_conditions is None:
            initial_conditions = [
                1.0,  # a0 = 1 (today)
                self.psi_params['initial_psi'],
                self.psi_params['initial_dpsi']
            ]
        
        # Solve ODEs
        solution = odeint(self.cosmological_equations, initial_conditions, t_span)
        
        a_vals = solution[:, 0]
        psi_vals = solution[:, 1] 
        dpsi_vals = solution[:, 2]
        
        # Calculate derived quantities
        H_vals = []
        w_vals = []
        
        for i, t in enumerate(t_span):
            a, psi, dpsi = solution[i]
            H = np.sqrt((8 * np.pi / 3) * (
                self.Omega_m0 / a**3 + 
                self.energy_density_psi(psi, dpsi, 0) / self.Omega_psi0
            )) * self.H0
            
            w = self.equation_of_state(psi, dpsi, H)
            
            H_vals.append(H)
            w_vals.append(w)
        
        return {
            'time': t_span,
            'scale_factor': a_vals,
            'field': psi_vals,
            'field_velocity': dpsi_vals,
            'hubble': np.array(H_vals),
            'equation_of_state': np.array(w_vals)
        }

def plot_evolution(results):
    """
    Plot the cosmological evolution results.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Scale factor
    ax1.plot(results['time'], results['scale_factor'], 'b-', linewidth=2)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Scale Factor a(t)')
    ax1.set_title('Cosmic Expansion')
    ax1.grid(True, alpha=0.3)
    
    # Hyperchronal field
    ax2.plot(results['time'], results['field'], 'r-', linewidth=2)
    ax2.set_xlabel('Time') 
    ax2.set_ylabel('Ψ(t)')
    ax2.set_title('Hyperchronal Field Evolution')
    ax2.grid(True, alpha=0.3)
    
    # Hubble parameter
    ax3.plot(results['time'], results['hubble'], 'g-', linewidth=2)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('H(t)')
    ax3.set_title('Hubble Parameter')
    ax3.grid(True, alpha=0.3)
    
    # Equation of state
    ax4.plot(results['time'], results['equation_of_state'], 'm-', linewidth=2)
    ax4.axhline(y=-1, color='k', linestyle='--', alpha=0.5, label='w = -1 (Λ)')
    ax4.axhline(y=-1/3, color='k', linestyle=':', alpha=0.5, label='w = -1/3')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('w(t)')
    ax4.set_title('Equation of State Parameter')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Hyperchronal Framework - Cosmological Simulation")
    print("================================================")
    
    # Initialize cosmology
    cosmo = HyperchronalCosmology()
    
    # Time span (in units where H0^-1 = 1)
    t_span = np.linspace(0, 2, 1000)
    
    # Run simulation
    print("Running cosmological evolution...")
    results = cosmo.evolve(t_span)
    
    # Plot results
    plot_evolution(results)
    
    # Print final state
    final_w = results['equation_of_state'][-1]
    print(f"Final equation of state parameter: w = {final_w:.3f}")
    
    if final_w < -0.9:
        print("Hyperchronal field acts as effective cosmological constant!")
    elif final_w < -0.5:
        print("Hyperchronal field provides accelerated expansion.")
    else:
        print("Hyperchronal field does not drive acceleration.")
        
    print("\nNote: This is a simplified model. Full analysis requires")
    print("perturbation theory and comparison with CMB/BAO data.")
