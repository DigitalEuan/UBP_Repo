# UBP 3.7 API Reference

This document provides the real, working API for all UBP 3.7 modules.

## core.coherence_substrate.CoherenceState

A value in the UBP substrate isn't just a number - it's a coherence state.

**Critical Fix (from feedback)**: Uses log-NRCI space for accurate error accumulation.
Instead of multiplicative degradation (which decays too fast), we track the
logarithm of coherence error, allowing linear accumulation of true fidelity loss.

Every value knows:
- Its magnitude
- Its log_nrci_error (smaller = better coherence)
- Its net_refinements (tracks Y^n for closure testing)

This is information-first computation.

### Constructor
`CoherenceState(self, value: float, log_nrci_error: float = None, net_refinements: int = 0)`

### Methods
- **`apply_y_refinement(self, direction: str) -> 'CoherenceState'`**
  - Apply Y-refinement in the specified direction.

Args:
    direction: 'forward' or 'backward'
    
Returns:
    self (for method chaining)
- **`degrade_by(self, delta_log_error: float) -> 'CoherenceState'`**
  - Degrade coherence by adding to log-error.

This is the correct way to accumulate error - linearly in log space,
not multiplicatively in NRCI space.
- **`refine_backward(self) -> 'CoherenceState'`**
  - Apply inverse refinement (observer → geometry).

**Critical Fix**: Directional operator, not round-trip.
- **`refine_forward(self) -> 'CoherenceState'`**
  - Apply Y-refinement (geometry → observer).

**Critical Fix**: Y-refinement is now directional, not round-trip.
We apply Y *once* and track the net refinement count.
- **`test_closure(self) -> Tuple[float, bool]`**
  - Test bidirectional closure: (v ⊗ Y^n) ⊗ Y^(-n) → v

True closure isn't v * Y * Y_INVERSE (which introduces floating-point noise),
but tracking net refinements and verifying they cancel properly.

## core.state.OffBit

Immutable 24-bit UBP OffBit with layer properties.

Represents a fundamental unit of UBP computation with 24-bit data
and layer-based access patterns.

### Constructor
`OffBit(self, value: int) -> None`

### Methods
- **`extract_data(self) -> int`**
  - Extract 24-bit data for Golay correction.

Returns:
    24-bit data value
- **`get_bit(self, position: int) -> int`**
  - Get the value of a specific bit.

Args:
    position: Bit position (0-23)

Returns:
    Bit value (0 or 1)
- **`hamming_weight(self) -> int`**
  - Calculate the Hamming weight (number of 1 bits).
- **`set_bit(self, position: int, value: int) -> 'OffBit'`**
  - Create a new OffBit with a specific bit set.

Args:
    position: Bit position (0-23)
    value: Bit value (0 or 1)

Returns:
    New OffBit with specified bit set
- **`toggle(self) -> 'OffBit'`**
  - Create a new OffBit with toggled state.

Returns:
    New OffBit with inverted bits
- **`toggle_bit(self, position: int) -> 'OffBit'`**
  - Create a new OffBit with a specific bit toggled.

Args:
    position: Bit position to toggle (0-23)

Returns:
    New OffBit with specified bit toggled

## core.y_constants.YConstants

Container for Y constant family values and calculations.

All values are computed to 15 decimal places for maximum precision
in physical constant derivations.

### Constructor
`YConstants(self, /, *args, **kwargs)`

### Methods
No public methods.


## core.system_constants.UBPConstants

Collection of universal, mathematical, and UBP-specific constants.
All values are defined here for consistency across the framework.

### Constructor
`UBPConstants(self, /, *args, **kwargs)`

### Methods
No public methods.


## error_correction.golay_code.GolayG24

Binary Golay(24,12) error correcting code.

This is the CORRECT implementation using the proper extended Golay construction.

### Constructor
`GolayG24(self)`

### Methods
- **`correct_errors(self, received: numpy.ndarray) -> numpy.ndarray`**
  - Correct errors in a received 24-bit vector.

Uses syndrome decoding to identify and correct up to 3 bit errors.

Args:
    received: 24-bit received vector (possibly corrupted)

Returns:
    24-bit corrected codeword
- **`decode(self, codeword: numpy.ndarray) -> numpy.ndarray`**
  - Decode a 24-bit codeword to extract the 12-bit message.

Args:
    codeword: 24-bit codeword

Returns:
    12-bit message
- **`detect_errors(self, received: numpy.ndarray) -> Tuple[bool, int]`**
  - Detect if there are errors in a received vector.

Args:
    received: 24-bit received vector

Returns:
    (has_errors, estimated_error_count)
- **`encode(self, message: numpy.ndarray) -> numpy.ndarray`**
  - Encode a 12-bit message into a 24-bit codeword.

c = m * G (mod 2)

Args:
    message: 12-bit message vector

Returns:
    24-bit codeword
- **`hamming_distance(self, v1: numpy.ndarray, v2: numpy.ndarray) -> int`**
  - Compute Hamming distance between two vectors.
- **`hamming_weight(self, vector: numpy.ndarray) -> int`**
  - Compute Hamming weight (number of 1s).
- **`is_codeword(self, vector: numpy.ndarray) -> bool`**
  - Check if a vector is a valid codeword.

A vector is a codeword if H * v^T = 0 (mod 2).

## error_correction.leech_lattice.LeechLattice

The Leech lattice Λ24 - a 24-dimensional even unimodular lattice.

Construction via the Golay code:
The Leech lattice can be constructed from the binary Golay code G24
using the "Construction A" method.

Key properties:
- Dimension: 24
- Minimum norm: 4 (no vectors of norm 2)
- Kissing number: 196,560
- Automorphism group: Conway group Co0

### Constructor
`LeechLattice(self)`

### Methods
- **`distance_to_lattice(self, vector: numpy.ndarray) -> float`**
  - Compute the distance from a vector to the nearest lattice point.

Args:
    vector: 24-dimensional real vector

Returns:
    Euclidean distance to nearest lattice point
- **`generate_shell(self, norm_squared: int, max_points: int = 1000) -> List[error_correction.leech_lattice.LeechLatticePoint]`**
  - Generate lattice points with a given squared norm.

Args:
    norm_squared: Target squared norm (e.g., 4 for minimal vectors)
    max_points: Maximum number of points to generate

Returns:
    List of LeechLatticePoints with the specified norm
- **`inner_product(self, p1: error_correction.leech_lattice.LeechLatticePoint, p2: error_correction.leech_lattice.LeechLatticePoint) -> float`**
  - Compute the inner product of two lattice points.
- **`is_in_lattice(self, point: error_correction.leech_lattice.LeechLatticePoint) -> bool`**
  - Check if a point is actually in the Leech lattice.

Args:
    point: Candidate lattice point

Returns:
    True if point is in Λ24
- **`nearest_lattice_point(self, vector: numpy.ndarray) -> error_correction.leech_lattice.LeechLatticePoint`**
  - Find the nearest lattice point to a given 24-dimensional vector.

This is the "vector quantization" or "decoding" problem for the lattice.

Args:
    vector: 24-dimensional real vector

Returns:
    Nearest LeechLatticePoint
- **`point_from_coordinates(self, coords: numpy.ndarray) -> error_correction.leech_lattice.LeechLatticePoint`**
  - Create a lattice point from 24-dimensional coordinates.

Args:
    coords: 24-dimensional vector (integer or half-integer)

Returns:
    LeechLatticePoint
- **`verify_kissing_number(self, sample_size: int = 1000) -> Tuple[int, bool]`**
  - Verify the kissing number by generating minimal vectors.

Args:
    sample_size: Number of minimal vectors to generate

Returns:
    (number_found, is_consistent_with_theory)
- **`zero_point(self) -> error_correction.leech_lattice.LeechLatticePoint`**
  - Return the zero point (origin) of the lattice.

## error_correction.vector_offbit.VectorOffBit

24-dimensional vector representation of OffBit state.

This is a TRUE 24-dimensional vector, not a scalar with bit representation.

Properties:
- vector: numpy array of shape (24,)
- coherence: CoherenceState tracking computational fidelity
- Supports vector space operations: addition, dot product, norm, etc.

### Constructor
`VectorOffBit(self, vector: numpy.ndarray, coherence: core.coherence_substrate.CoherenceState) -> None`

### Methods
- **`and_op(self, other: 'VectorOffBit') -> 'VectorOffBit'`**
  - Bitwise AND (on binary representation).
- **`angle(self, other: 'VectorOffBit') -> float`**
  - Angle between vectors (in radians).
- **`copy(self) -> 'VectorOffBit'`**
  - Create a copy.
- **`distance(self, other: 'VectorOffBit') -> float`**
  - Euclidean distance to another vector.
- **`dot(self, other: 'VectorOffBit') -> float`**
  - Dot product (inner product).
- **`hamming_distance(self, other: 'VectorOffBit') -> int`**
  - Hamming distance (number of differing elements).
- **`hamming_weight(self) -> int`**
  - Number of non-zero elements.
- **`norm(self) -> float`**
  - Euclidean norm (L2 norm).
- **`norm_squared(self) -> float`**
  - Squared norm.
- **`normalize(self) -> 'VectorOffBit'`**
  - Return normalized vector (unit length).
- **`not_op(self) -> 'VectorOffBit'`**
  - Bitwise NOT (on binary representation).
- **`or_op(self, other: 'VectorOffBit') -> 'VectorOffBit'`**
  - Bitwise OR (on binary representation).
- **`project_onto(self, other: 'VectorOffBit') -> 'VectorOffBit'`**
  - Project this vector onto another vector.
- **`to_binary(self) -> numpy.ndarray`**
  - Convert to binary (0/1) representation.
- **`to_bipolar(self) -> numpy.ndarray`**
  - Convert to bipolar (±1) representation.
- **`to_golay_codeword(self) -> numpy.ndarray`**
  - Convert to Golay G24 codeword (24-bit binary).
- **`to_leech_point(self)`**
  - Convert to Leech lattice point.

Returns:
    LeechLatticePoint (if leech_lattice module available)
- **`to_scalar(self) -> int`**
  - Convert to 24-bit integer (scalar OffBit).
- **`xor(self, other: 'VectorOffBit') -> 'VectorOffBit'`**
  - Bitwise XOR (on binary representation).

## analysis.resonance_detector_fft.ResonanceDetectorFFT

FFT-based resonance detector for UBP coherence states.

This is a REAL signal processing implementation using numpy.fft.

### Constructor
`ResonanceDetectorFFT(self, sample_rate: float = 1.0, window: str = 'hann', min_peak_height: float = 0.1, min_peak_distance: int = 5)`

### Methods
- **`analyze_spectrum(self, signal: numpy.ndarray) -> analysis.resonance_detector_fft.SpectrumAnalysis`**
  - Perform complete spectral analysis of a signal.

Args:
    signal: Time-domain signal (real-valued)

Returns:
    SpectrumAnalysis object
- **`detect_coherence_resonance(self, states: List[core.coherence_substrate.CoherenceState]) -> Optional[analysis.resonance_detector_fft.SpectrumAnalysis]`**
  - Detect resonances in the coherence (NRCI) values.

Args:
    states: List of CoherenceState objects

Returns:
    SpectrumAnalysis if resonances detected, None otherwise
- **`detect_resonance(self, states: List[core.coherence_substrate.CoherenceState]) -> Optional[analysis.resonance_detector_fft.SpectrumAnalysis]`**
  - Detect resonances in a sequence of CoherenceStates.

Args:
    states: List of CoherenceState objects

Returns:
    SpectrumAnalysis if resonances detected, None otherwise
- **`spectrogram(self, signal: numpy.ndarray, window_size: int, hop_size: int) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]`**
  - Compute spectrogram (time-frequency representation).

Args:
    signal: Time-domain signal
    window_size: Size of analysis window
    hop_size: Hop size between windows

Returns:
    (times, frequencies, spectrogram_matrix)

## simulation.simulation.PhysicsSimulator

Physics simulation engine with time evolution.

This is a REAL numerical integration engine, not a placeholder.

### Constructor
`PhysicsSimulator(self, dimension: int = 1, integration_method: str = 'rk4')`

### Methods
- **`simulate(self, initial_state: simulation.simulation.SimulationState, force_func: Callable, energy_func: Callable, t_final: float, dt: float = 0.01, save_every: int = 1) -> simulation.simulation.SimulationResult`**
  - Run a physics simulation with time evolution.

Args:
    initial_state: Initial state
    force_func: Function(t, q, v) -> acceleration
    energy_func: Function(q, v) -> energy
    t_final: Final time
    dt: Time step
    save_every: Save state every N steps

Returns:
    SimulationResult

## reversible.reversible_coherence_state.ReversibleCoherenceState

**ERROR:** Could not inspect module: No module named 'reversible_rational'

## realms.atomic_realm.AtomicRealm

Atomic/Chemical realm calculator using UBP 3.4 framework.

### Constructor
`AtomicRealm(self)`

### Methods
- **`calculate_atomic_energy_soc(self, atomic_state: realms.atomic_realm.AtomicState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate atomic energy using SOC equation.

Args:
    atomic_state: Atomic system state
    
Returns:
    SOCEnergyResult with energy in CU
- **`model_co2_vibrations(self, mode: str = 'asymmetric_stretch', temperature_k: float = 300.0) -> Dict[str, float]`**
  - Model CO₂ molecular vibrations.

NEW TEST PHENOMENON: CO₂ IR absorption
Real data: Asymmetric stretch 2349 cm⁻¹ (4.26 μm)

Args:
    mode: Vibrational mode ("asymmetric_stretch", "symmetric_stretch", "bend")
    temperature_k: Temperature (K)
    
Returns:
    Dictionary with vibrational analysis
- **`model_hydrogen_spectrum(self, n_initial: int = 3, n_final: int = 2, series_name: str = 'Balmer') -> Dict[str, float]`**
  - Model hydrogen spectral lines using Rydberg formula.

NEW TEST PHENOMENON: Balmer series (visible light)
Real data: H-alpha 656.3 nm, H-beta 486.1 nm, H-gamma 434.0 nm

Args:
    n_initial: Initial principal quantum number
    n_final: Final principal quantum number
    series_name: Spectral series name
    
Returns:
    Dictionary with spectral analysis

## realms.electromagnetic_realm.ElectromagneticRealm

Electromagnetic realm calculator using UBP 3.4 framework.

### Constructor
`ElectromagneticRealm(self)`

### Methods
- **`calculate_em_energy_soc(self, em_state: realms.electromagnetic_realm.EMFieldState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate EM energy using SOC equation.

Args:
    em_state: Electromagnetic field state
    
Returns:
    SOCEnergyResult with energy in CU
- **`model_cavity_resonator(self, cavity_length_cm: float, cavity_radius_cm: float, mode: str = 'TE011', material_conductivity: float = 58000000.0) -> Dict[str, float]`**
  - Model microwave cavity resonator Q-factor.

NEW TEST PHENOMENON: Cylindrical cavity resonator (verifiable)
Real data: Copper cavity at X-band should have Q > 10,000

Args:
    cavity_length_cm: Cavity length (cm)
    cavity_radius_cm: Cavity radius (cm)
    mode: Resonant mode (TE011, TM010, etc.)
    material_conductivity: Wall conductivity (S/m)
    
Returns:
    Dictionary with cavity analysis
- **`model_dipole_antenna_resonance(self, frequency_GHz: float, antenna_length_cm: float, input_power_W: float, environment: str = 'free_space') -> Dict[str, float]`**
  - Model dipole antenna resonance at WiFi frequencies.

NEW TEST PHENOMENON: 2.4 GHz dipole antenna (verifiable)
Real data: λ/2 dipole at 2.4 GHz should be ~6.25 cm

Args:
    frequency_GHz: Operating frequency (GHz)
    antenna_length_cm: Physical antenna length (cm)
    input_power_W: Input power (Watts)
    environment: "free_space" or "ground_plane"
    
Returns:
    Dictionary with antenna analysis

## realms.optical_realm.OpticalRealm

Enhanced Optical Realm implementation for the UBP Framework.

This class provides comprehensive photonics modeling with photonic lattices,
WGE charge quantization, advanced optical calculations, and validation.

### Constructor
`OpticalRealm(self, bitfield: Optional[core.state.MutableBitfield] = None)`

### Methods
- **`calculate_coupling_efficiency(self, mode1: realms.optical_realm.PhotonicModeProfile, mode2: realms.optical_realm.PhotonicModeProfile) -> float`**
  - Calculate coupling efficiency between two photonic modes.

Args:
    mode1: First photonic mode
    mode2: Second photonic mode
    
Returns:
    Coupling efficiency (0 to 1)
- **`calculate_dispersion_effects(self, wavelength_range: numpy.ndarray) -> Dict[str, Any]`**
  - Calculate chromatic dispersion effects.

Args:
    wavelength_range: Array of wavelengths (meters)
    
Returns:
    Dictionary containing dispersion results
- **`calculate_nonlinear_optics(self, input_power: float, length: float) -> Dict[str, Any]`**
  - Calculate nonlinear optical effects.

Args:
    input_power: Input optical power (Watts)
    length: Propagation length (meters)
    
Returns:
    Dictionary containing nonlinear optical results
- **`calculate_photonic_bandgap(self, k_vector: numpy.ndarray) -> Dict[str, Any]`**
  - Calculate photonic bandgap structure.

Args:
    k_vector: Wave vector array
    
Returns:
    Dictionary containing bandgap information
- **`calculate_wge_charge_quantization(self, field_strength: float) -> Dict[str, float]`**
  - Calculate WGE charge quantization effects.

Args:
    field_strength: Electromagnetic field strength
    
Returns:
    Dictionary containing quantization results
- **`get_optical_metrics(self) -> realms.optical_realm.OpticalRealmMetrics`**
  - Get current optical realm metrics.
- **`run_optical_computation(self, input_data: numpy.ndarray, computation_type: str = 'full') -> Dict[str, Any]`**
  - Run comprehensive optical realm computation.

Args:
    input_data: Input data for optical computation
    computation_type: Type of computation ('bandgap', 'wge', 'nonlinear', 'dispersion', 'full')
    
Returns:
    Dictionary containing computation results
- **`validate_optical_realm(self) -> Dict[str, Any]`**
  - Comprehensive validation of optical realm implementation.

Returns:
    Dictionary containing validation results

## realms.nuclear_realm.NuclearRealm

Complete Nuclear Realm implementation for the UBP Framework.

This class provides nuclear physics modeling with E8-to-G2 symmetry,
Zitterbewegung dynamics, CARFE field equations, and NMR validation.

### Constructor
`NuclearRealm(self, bitfield: Optional[core.state.MutableBitfield] = None)`

### Methods
- **`calculate_e8_g2_coherence(self, field_data: numpy.ndarray) -> float`**
  - Calculate coherence based on E8-to-G2 symmetry breaking.

Args:
    field_data: Field configuration data
    
Returns:
    Coherence value between 0 and 1
- **`calculate_nmr_validation(self, nucleus_type: str = 'proton') -> Dict[str, float]`**
  - Calculate NMR validation metrics for nuclear realm verification.

Args:
    nucleus_type: Type of nucleus ('proton', 'neutron', 'deuteron')
    
Returns:
    Dictionary containing NMR validation metrics
- **`calculate_nuclear_binding_energy(self, mass_number: int, atomic_number: int) -> float`**
  - Calculate nuclear binding energy using semi-empirical mass formula.

Args:
    mass_number: Mass number (A)
    atomic_number: Atomic number (Z)
    
Returns:
    Binding energy in MeV
- **`calculate_zitterbewegung_dynamics(self, time_array: numpy.ndarray) -> Dict[str, numpy.ndarray]`**
  - Calculate Zitterbewegung dynamics for given time array.

Args:
    time_array: Array of time values (seconds)
    
Returns:
    Dictionary containing position, velocity, and spin dynamics
- **`get_nuclear_metrics(self) -> realms.nuclear_realm.NuclearRealmMetrics`**
  - Get current nuclear realm metrics.
- **`run_nuclear_computation(self, input_data: numpy.ndarray, computation_type: str = 'full') -> Dict[str, Any]`**
  - Run comprehensive nuclear realm computation.

Args:
    input_data: Input data for nuclear computation
    computation_type: Type of computation ('zitterbewegung', 'carfe', 'nmr', 'full')
    
Returns:
    Dictionary containing computation results
- **`solve_carfe_equation(self, initial_field: numpy.ndarray, time_steps: int = 100) -> Dict[str, Any]`**
  - Solve the Cykloid Adelic Recursive Expansive Field Equation (CARFE).

Args:
    initial_field: Initial field configuration
    time_steps: Number of temporal evolution steps
    
Returns:
    Dictionary containing field evolution and stability metrics
- **`validate_nuclear_realm(self) -> Dict[str, Any]`**
  - Comprehensive validation of nuclear realm implementation.

Returns:
    Dictionary containing validation results

## realms.gravitational_realm.GravitationalRealm

Gravitational realm calculator using UBP 3.4 framework.

### Constructor
`GravitationalRealm(self)`

### Methods
- **`calculate_gravitational_energy_soc(self, grav_state: realms.gravitational_realm.GravitationalState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate gravitational energy using SOC equation.

Args:
    grav_state: Gravitational system state
    
Returns:
    SOCEnergyResult with energy in CU
- **`model_jupiter_europa_resonance(self, jupiter_mass_kg: Optional[float] = None, europa_mass_kg: Optional[float] = None, europa_orbital_radius_km: float = 671100.0, io_orbital_radius_km: float = 421800.0) -> Dict[str, float]`**
  - Model Jupiter-Europa orbital resonance.

NEW TEST PHENOMENON: 2:1 mean-motion resonance with Io
Real data: Europa orbits twice for every Io orbit

Args:
    jupiter_mass_kg: Jupiter mass (kg)
    europa_mass_kg: Europa mass (kg)
    europa_orbital_radius_km: Europa semi-major axis (km)
    io_orbital_radius_km: Io semi-major axis (km)
    
Returns:
    Dictionary with orbital resonance analysis
- **`model_ligo_gravitational_wave(self, event_name: str = 'GW150914', m1_solar_masses: float = 36.0, m2_solar_masses: float = 29.0, distance_mpc: float = 410.0, peak_frequency_hz: float = 250.0) -> Dict[str, float]`**
  - Model LIGO gravitational wave detection.

NEW TEST PHENOMENON: GW150914 binary black hole merger
Real data: First gravitational wave detection, September 14, 2015

Args:
    event_name: GW event name
    m1_solar_masses: Primary mass (solar masses)
    m2_solar_masses: Secondary mass (solar masses)
    distance_mpc: Luminosity distance (Megaparsecs)
    peak_frequency_hz: Peak GW frequency (Hz)
    
Returns:
    Dictionary with GW analysis

## realms.biological_realm.BiologicalRealm

Biological realm calculator using UBP 3.4 framework.

### Constructor
`BiologicalRealm(self)`

### Methods
- **`calculate_biological_energy_soc(self, bio_state: realms.biological_realm.BiologicalState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate biological energy using SOC equation.

Args:
    bio_state: Biological system state
    
Returns:
    SOCEnergyResult with energy in CU
- **`model_alpha_brain_waves(self, frequency_hz: float = 10.0, amplitude_uv: float = 50.0, electrode_count: int = 19, subject_state: str = 'relaxed_eyes_closed') -> Dict[str, float]`**
  - Model alpha brain wave oscillations from EEG.

NEW TEST PHENOMENON: Alpha waves (8-13 Hz)
Real data: Typical alpha waves are 8-13 Hz, 20-60 μV amplitude

Args:
    frequency_hz: Alpha wave frequency (Hz)
    amplitude_uv: Signal amplitude (microvolts)
    electrode_count: Number of EEG electrodes
    subject_state: Subject's mental state
    
Returns:
    Dictionary with brain wave analysis
- **`model_dna_breathing_mode(self, base_pair_count: int = 100, temperature_k: float = 310.15, hydration_level: float = 0.8) -> Dict[str, float]`**
  - Model DNA breathing mode vibrations.

NEW TEST PHENOMENON: DNA base pair opening/closing
Real data: Breathing modes ~10^10-10^11 Hz, crucial for replication

Args:
    base_pair_count: Number of base pairs in DNA segment
    temperature_k: Temperature (Kelvin)
    hydration_level: Hydration level (0-1, affects stiffness)
    
Returns:
    Dictionary with DNA vibration analysis

## realms.plasma_realm.PlasmaRealm

Plasma realm calculator using UBP 3.4 framework.

### Constructor
`PlasmaRealm(self)`

### Methods
- **`calculate_plasma_energy_soc(self, plasma_state: realms.plasma_realm.PlasmaState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate plasma energy using SOC equation.

Args:
    plasma_state: Plasma system state
    
Returns:
    SOCEnergyResult with energy in CU
- **`calculate_plasma_parameters(self, electron_density_m3: float, temperature_ev: float) -> Dict[str, float]`**
  - Calculate fundamental plasma parameters.

Args:
    electron_density_m3: Electron density (m⁻³)
    temperature_ev: Temperature (eV)
    
Returns:
    Dictionary with plasma parameters
- **`model_solar_corona(self, electron_density_m3: float = 1000000000000000.0, temperature_mk: float = 2.0, magnetic_field_t: float = 0.01, loop_length_mm: float = 100.0) -> Dict[str, float]`**
  - Model solar corona plasma dynamics.

NEW TEST PHENOMENON: Coronal loops
Real data: T~2MK, n~10^15 m⁻³, B~0.01T

Args:
    electron_density_m3: Electron density (m⁻³)
    temperature_mk: Temperature (Mega-Kelvin)
    magnetic_field_t: Magnetic field (T)
    loop_length_mm: Coronal loop length (Mm)
    
Returns:
    Dictionary with corona analysis
- **`model_tokamak_plasma(self, major_radius_m: float = 6.2, minor_radius_m: float = 2.0, electron_density_m3: float = 1e+20, temperature_kev: float = 15.0, magnetic_field_t: float = 5.3, confinement_time_s: float = 3.7) -> Dict[str, float]`**
  - Model tokamak plasma confinement.

NEW TEST PHENOMENON: ITER-like tokamak parameters
Real data: ITER design - R=6.2m, T=15keV, B=5.3T

Args:
    major_radius_m: Major radius (m)
    minor_radius_m: Minor radius (m)
    electron_density_m3: Electron density (m⁻³)
    temperature_kev: Temperature (keV)
    magnetic_field_t: Toroidal magnetic field (T)
    confinement_time_s: Energy confinement time (s)
    
Returns:
    Dictionary with tokamak analysis

## realms.cosmological_realm.CosmologicalRealm

Cosmological realm calculator using UBP 3.4 framework.

### Constructor
`CosmologicalRealm(self)`

### Methods
- **`calculate_cosmological_energy_soc(self, cosmo_state: realms.cosmological_realm.CosmologicalState) -> core.soc_energy.SOCEnergyResult`**
  - Calculate cosmological energy using SOC equation.

Args:
    cosmo_state: Cosmological system state
    
Returns:
    SOCEnergyResult with energy in CU
- **`model_cmb_fluctuations(self, multipole_l: int = 200, temperature_k: float = 2.725, fluctuation_amplitude_uk: float = 70.0) -> Dict[str, float]`**
  - Model CMB temperature fluctuations.

NEW TEST PHENOMENON: CMB power spectrum
Real data: Planck satellite measured ΔT/T ~ 10^-5 at l~200

Args:
    multipole_l: Multipole moment (angular scale)
    temperature_k: Mean CMB temperature (K)
    fluctuation_amplitude_uk: RMS fluctuation amplitude (μK)
    
Returns:
    Dictionary with CMB analysis
- **`model_hubble_expansion(self, distance_mpc: float = 1000.0, include_dark_energy: bool = True) -> Dict[str, float]`**
  - Model Hubble expansion and dark energy.

NEW TEST PHENOMENON: Cosmic acceleration
Real data: H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685

Args:
    distance_mpc: Distance to observe (Mpc)
    include_dark_energy: Include dark energy effects
    
Returns:
    Dictionary with expansion analysis

