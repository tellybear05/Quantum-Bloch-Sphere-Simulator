import numpy as np
import cmath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#Function to convert a normalized qubit state |ψ> = a|0> + b|1> into Bloch sphere angles (theta, phi) and coordinates (x,y,z).

def state_to_bloch(a, b):
    
    norm = abs(a)**2 + abs(b)**2
    if not np.isclose(norm, 1):
        a, b = a/np.sqrt(norm), b/np.sqrt(norm)

    theta = 2 * np.arccos(np.clip(abs(a), 0.0, 1.0))
    phi = (cmath.phase(b) - cmath.phase(a)) % (2*np.pi)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return theta, phi, (x, y, z)



#Function to convert Bloch angles (theta, phi) into state amplitudes a, b.

def bloch_to_state(theta, phi):
    
    a = np.cos(theta / 2)
    b = np.exp(1j * phi) * np.sin(theta / 2)
    return a, b

#Function to apply a single-qubit gate to the state vector.

def apply_gate(state, gate):
    
    return gate.dot(state)

#Funtion to return measurement probabilities in computational basis.

def measure_state(a, b):
   
    return abs(a)**2, abs(b)**2


def plot_bloch_vector(x, y, z):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # draw sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(xs, ys, zs, color='c', alpha=0.1, linewidth=0)
    # draw vector
    ax.quiver(0, 0, 0, x, y, z, length=1.0, normalize=True)
    # set labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])
    plt.show()

# Elementary gates definitions
GATES = {
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    'H': (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex),
}


def prompt_state():
    print("Select input method:")
    print("1) Bloch angles (theta, phi)")
    print("2) Complex amplitudes (a, b)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        th = float(input("theta (in radians): "))
        ph = float(input("phi (in radians): "))
        return bloch_to_state(th, ph)
    elif choice == '2':
        a = complex(input("Enter amplitude a (e.g., 0.707+0.0j): "))
        b = complex(input("Enter amplitude b: "))
        norm = np.sqrt(abs(a)**2 + abs(b)**2)
        return a/norm, b/norm
    else:
        print("Invalid choice. Defaulting to |0>.")
        return 1+0j, 0+0j


def main():
    print("=== Bloch Sphere Simulator ===")
    a, b = prompt_state()
    state = np.array([a, b], dtype=complex)

    while True:
        theta, phi, (x, y, z) = state_to_bloch(state[0], state[1])
        print(f"\nState: a={state[0]:.4f}, b={state[1]:.4f}")
        print(f"Angles: θ={theta:.4f}, φ={phi:.4f}")
        print(f"Vector: x={x:.4f}, y={y:.4f}, z={z:.4f}")
        p0, p1 = measure_state(state[0], state[1])
        print(f"Probabilities: P(0)={p0:.4f}, P(1)={p1:.4f}")

        print("\nOperations: X, Y, Z, H, PLOT, SET, EXIT")
        op = input("Enter operation: ").strip().upper()

        if op in GATES:
            state = apply_gate(state, GATES[op])
        elif op == 'PLOT':
            plot_bloch_vector(x, y, z)
        elif op == 'SET':
            a, b = prompt_state()
            state = np.array([a, b], dtype=complex)
        elif op == 'EXIT':
            print("Goodbye :(")
            break
        else:
            print("Unknown operation. Try again.")

if __name__ == '__main__':
    main()
1